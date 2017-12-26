from mserver.player.exceptions import MServerException


class SearchException(MServerException):
    pass


class SearchError(SearchException):
    pass


class DownloadError(SearchException):
    pass
