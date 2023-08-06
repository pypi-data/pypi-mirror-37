
class FatalErrorResponse:

    def __init__(self, message):
        self._message = message
        self.result = message
        self.id = "error"

    def get_audit_text(self):
        return 'error = "{0}", (NOT PUBLISHED)'.format(self._message)
