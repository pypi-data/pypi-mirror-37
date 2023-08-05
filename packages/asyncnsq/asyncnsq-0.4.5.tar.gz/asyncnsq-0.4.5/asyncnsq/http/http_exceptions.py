

class NsqHttpException(Exception):
    """XXX"""


class TransportError(NsqHttpException):
    """XXX"""
    @property
    def status_code(self):
        """XXX"""
        return self.args[0]

    @property
    def error(self):
        """A string error message."""
        return self.args[1]

    @property
    def info(self):
        """Dict of returned error info from ES, where available."""
        return self.args[2]

    def __str__(self):
        return 'TransportError(%s, %r)' % (self.status_code, self.error)


class HttpConnectionError(TransportError):
    """XXX"""

    def __str__(self):
        return 'HttpConnectionError(%s) caused by: %s(%s)' % (
            self.error, self.info.__class__.__name__, self.info)


class NotFoundError(TransportError):
    """Exception representing a 404 status code."""


class ConflictError(TransportError):
    """Exception representing a 409 status code."""


class RequestError(TransportError):
    """Exception representing a 400 status code."""

# more generic mappings from status_code to python exceptions
HTTP_EXCEPTIONS = {
    400: RequestError,
    404: NotFoundError,
}
