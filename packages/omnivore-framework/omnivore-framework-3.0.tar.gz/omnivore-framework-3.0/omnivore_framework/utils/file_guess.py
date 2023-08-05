import os
import io

import numpy as np
import jsonpickle

from fs.opener import opener, fsopen
from fs.errors import FSError

from traits.api import HasTraits, Bool, Str, Unicode, Trait, TraitHandler, Property

from . import jsonutil
from .textutil import guessBinary
from ..templates import get_template

import logging
log = logging.getLogger(__name__)


def normalize_uri(uri):
    if uri.startswith("file://"):
        # FIXME: workaround to allow opening of file:// URLs with the
        # ! character
        uri = uri.replace("file://", "")
    if uri:
        fs, relpath = opener.parse(uri)
        if fs.haspathurl(relpath):
            uri = fs.getpathurl(relpath)
        elif fs.hassyspath(relpath):
            abspath = fs.getsyspath(relpath)
            if abspath.startswith("\\\\?\\UNC\\"):
                # Leave long UNC paths as raw paths because there is no
                # accepted way to convert to URI
                uri = abspath
            else:
                if abspath.startswith("\\\\?\\") and len(abspath) < 260:
                    # on windows, pyfilesystem returns extended path notation to
                    # allow paths greater than 256 characters.  If the path is
                    # short, change slashes to normal and remove the prefix
                    abspath = abspath[4:].replace("\\", "/")
                uri = "file://" + abspath
    return uri


def get_fs(uri):
    if uri.startswith("file://"):
        # FIXME: workaround to allow opening of file:// URLs with the
        # ! character
        uri = uri.replace("file://", "")
    fs, relpath = opener.parse(uri)
    log.debug("Filesystem: %s" % fs)
    fh = fs.open(relpath, "rb")
    return fh, fs, relpath


class TraitUriNormalizer(TraitHandler):
    """Trait validator to convert bytes to numpy array"""

    def validate(self, object, name, value):
        try:
            uri = normalize_uri(value)
            return uri
        except FSError:
            # Allow the error to be caught when the file is actually opened
            return value
        except:
            self.error(object, name, value)

    def info(self):
        return '**a string or unicode URI**'


class FileMetadata(HasTraits):
    uri = Trait("", TraitUriNormalizer())

    mime = Str(default="application/octet-stream")

    name = Property(Unicode, depends_on='uri')

    read_only = Bool(False)

    def __str__(self):
        return "uri=%s, mime=%s" % (self.uri, self.mime)

    def _get_name(self):
        return os.path.basename(self.uri)

    @property
    def syspath(self):
        fs, relpath = opener.parse(self.uri)
        self.read_only = fs.getmeta('read_only')
        if fs.hassyspath(relpath):
            return fs.getsyspath(relpath)
        raise TypeError("No system path for %s" % self.uri)

    def check_read_only(self):
        fs, relpath = opener.parse(self.uri)
        self.read_only = fs.getmeta('read_only')
        return self.read_only

    def get_stream(self):
        fh, fs, relpath = get_fs(self.uri)
        self.read_only = fs.getmeta('read_only')
        return fh


class FileGuess(object):
    """Loads the first part of a file and provides a container for metadata

    """
    # Arbitrary size header, but should be large enough that binary files can
    # be scanned for a signature. Make sure it's not a multiple of 1k for naive
    # parsers that rely on size detection
    head_size = 1024*1024 - 1

    metadata_exts = [".omnivore", ".omniemu"]

    def __init__(self, uri, metadata_ext=None):
        if metadata_ext is not None:
            # override class attribute
            self.metadata_exts = [metadata_ext]
        self.force_mime = None
        self._likely_binary = None
        log.debug("Attempting to load %s" % uri)
        self.reload(uri)

    @property
    def likely_binary(self):
        if self._likely_binary is None:
            t = self.get_bytes()
            self._likely_binary = guessBinary(t)
        return self._likely_binary

    @property
    def likely_text(self):
        if self._likely_binary is None:
            t = self.get_bytes()
            self._likely_binary = guessBinary(t)
        return not self._likely_binary

    def get_fs(self, uri=None):
        if uri is None:
            uri = self.metadata.uri
        return get_fs(uri)

    def reload(self, uri=None):
        fh, fs, relpath = self.get_fs(uri)

        # In order to handle arbitrarily sized files, only read the first
        # header bytes.  If the file is bigger, it will be read by the task
        # as needed.
        self._numpy = None
        self.raw_bytes = fh.read(self.head_size)
        fh.close()

        # Use the default mime type until it is recognized
        self.metadata = FileMetadata(uri=uri)
        try:
            self.metadata.read_only = fs.getmeta('read_only')
        except AttributeError:
            pass

        # Release filesystem resources
        fs.close()
        self.reload_json_metadata(uri)

    def reload_json_metadata(self, uri):
        self.json_metadata = {}
        for ext in self.metadata_exts:
            unserialized = self.load_unserialized_metadata(uri, ext)
            self.json_metadata[ext] = unserialized
            mime = unserialized.get("mime", None)
            if mime is not None and self.force_mime is not None:
                self.force_mime = mime
        print("JSON metadata for exts:", self.json_metadata)

    def load_unserialized_metadata(self, uri, ext):
        uri = uri + ext
        try:
            fh, fs, relpath = self.get_fs(uri)
        except FSError as e:
            log.debug(f"No json metadata found for {uri}")
            unserialized = {}
        else:
            raw = fh.read()
            fh.close()
            fs.close()
            unserialized = jsonutil.unserialize(uri, raw)
        return unserialized

    def __str__(self):
        return "guess: metadata: %s, %d bytes available for signature" % (self.metadata, len(self.raw_bytes))

    def get_bytes(self):
        return self.raw_bytes

    @property
    def numpy(self):
        if self._numpy is None:
            self._numpy = np.fromstring(self.raw_bytes, dtype=np.uint8)
        return self._numpy

    @property
    def bytes_as_stream(self):
        return io.BytesIO(self.raw_bytes)

    def get_metadata(self):
        return self.metadata.clone_traits()

    def get_stream(self):
        fh, fs, relpath = self.get_fs()
        return fh
