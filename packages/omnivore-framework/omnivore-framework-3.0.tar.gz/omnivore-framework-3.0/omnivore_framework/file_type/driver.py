from traits.api import HasTraits, provides, List, Instance, Any

from ..utils.sortutil import before_after_wildcard_sort
from ..framework.document import DocumentError

from .i_file_recognizer import IFileRecognizer, IFileRecognizerDriver

import logging
log = logging.getLogger(__name__)


@provides(IFileRecognizerDriver)
class FileRecognizerDriver(HasTraits):
    """ Identify files using the available FileRecognizer extension point contributors
    
    """

    application = Any

    recognizers = List(Instance(IFileRecognizer))

    def recognize(self, guess):
        """Using the list of known recognizers, attempt to set the MIME of a FileGuess
        """
        if guess.raw_bytes is None:
            return self.application.document_class(metadata=guess.metadata, raw_bytes="")

        error = ""
        document = None
        mime = None
        log.debug("trying %d recognizers " % len(self.recognizers))

        if guess.force_mime:
            for recognizer in self.recognizers:
                log.debug(f"trying {recognizer.id} for MIME {guess.force_mime}")
                if recognizer.can_load_mime(guess.force_mime):
                    document = recognizer.load(guess)

        if document is None:
            for recognizer in self.recognizers:
                log.debug("trying %s recognizer: " % recognizer.id,)
                mime = recognizer.identify(guess)
                if mime is not None:
                    guess.metadata.mime = mime
                    log.debug("found %s for %s" % (mime, guess.metadata.uri))
                    try:
                        document = recognizer.load(guess)
                    except DocumentError as e:
                        error = "Error when using %s parser to create a document:\n\n%s\n\nA default document will be opened instead." % (recognizer.name, str(e))
                        document = None
                    break

        if mime is None:
            guess.metadata.mime = "application/octet-stream"
            log.debug("Not recognized; default is %s" % guess.metadata.mime)
        if document is None:
            document = self.application.document_class(metadata=guess.metadata, raw_bytes=guess.numpy,load_error=error)
        return document

    def _recognizers_changed(self, old, new):
        log.debug("_recognizers_changed: old=%s new=%s" % (str(old), str(new)))
        log.debug("  old order: %s" % ", ".join([r.id for r in self.recognizers]))
        s = before_after_wildcard_sort(self.recognizers)
        # Is there a proper way to set the value in the trait change callback?
        # Assigning a new list will get call the notification handler multiple
        # times, although it seems to end the cycle when it detects that the
        # list items haven't changed from the last time.  I'm working around
        # this by replacing the items in the list so that the list object
        # itself hasn't changed, only the members.
        self.recognizers[:] = s
        log.debug("  new order: %s" % ", ".join([r.id for r in s]))
