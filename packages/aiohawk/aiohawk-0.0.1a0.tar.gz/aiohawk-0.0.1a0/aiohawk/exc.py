class HawkError(Exception):
    pass


class ParseError(HawkError):
    pass


class InvalidCredentials(HawkError):
    pass


class CredentialsLookupError(HawkError):
    pass


class MacMismatch(HawkError):
    pass


class ContentHashMismatch(HawkError):
    pass


class InvalidNonce(HawkError):
    pass


class TokenExpired(HawkError):
    pass


class MissingAuthorization(HawkError):
    pass


class MissingContent(HawkError):
    pass


class InvalidBewit(HawkError):
    pass
