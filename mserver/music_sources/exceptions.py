from mserver.exceptions import MServerException


class SearchException(MServerException):
    pass


class SearchError(SearchException):
    pass


class DownloadError(SearchException):
    pass


class NotFoundError(SearchError):
    pass
