import logging
import sys

from pprint import pformat

from .abs import AsyncHawkAuthority, Artifact, EmptyValue
from .exc import (CredentialsLookupError,
                  InvalidCredentials,
                  MissingAuthorization)
from .utils import parse_request, parse_authorization_header, validate_credentials, calculate_mac

# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class Receiver(AsyncHawkAuthority):

    async def __init__(self,
                       incoming_request,
                       credentials_func,
                       content=EmptyValue,
                       nonce_func=None,
                       localtime_offset_in_seconds=0,
                       accept_untrusted_content=False):
        # 0.init
        self.credentials_func = credentials_func
        log.debug(f'Accepting incoming request:\n{pformat(incoming_request, indent=4)}')

        # 2.parse request
        self.request_headers = parse_request(incoming_request)
        if not self.request_headers:
            raise MissingAuthorization()

        # 3.parse auth header
        self.attributes = parse_authorization_header(self.request_headers.get('authorization'))

        del self.request_headers['authorization']  # del for dataclass

        try:
            # 5.verify required field

            # 6.fetch hawk credentials
            credentials = await self.credentials_func(self.attributes['id'])
            validate_credentials(credentials)
        except (KeyError, LookupError) as ex:
            e, val, _ = sys.exc_info()
            log.debug(f'Validate Catching {e}: {val}')
            if isinstance(ex, KeyError):
                raise InvalidCredentials(f'Invalid credentials.')
            raise CredentialsLookupError(f'Unknown credentials')
        else:
            log.debug(f'Credentials:\n {pformat(credentials)}')

        # 4.generate artifacts
        artifacts = Artifact(**{
            **self.request_headers,
            **self.attributes,
            **credentials,
            **dict(
                content=content,
                nonce_func=nonce_func
            )})
        await self._authorize('header',
                              credentials,
                              artifacts,
                              localtime_offset_in_seconds=localtime_offset_in_seconds,
                              accept_untrusted_content=accept_untrusted_content)

        self.artifacts = artifacts
        # Finish

    async def header(self,
                     content=None,
                     content_type=None,
                     ext=None):
        artifacts = Artifact(**dict(
            self.request_headers,
            **self.attributes,
            **{'ext': ext,
               'content': content,
               'content_type': content_type}))
        artifacts.generate_content_hash()

        mac = calculate_mac('response', artifacts)

