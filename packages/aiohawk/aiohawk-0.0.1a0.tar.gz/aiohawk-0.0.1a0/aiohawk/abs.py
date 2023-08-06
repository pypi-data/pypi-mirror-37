import logging
import math
import types

from dataclasses import dataclass, field, InitVar
from typing import Any
from urllib.parse import urlparse

from .exc import (MacMismatch,
                  ContentHashMismatch,
                  InvalidNonce,
                  TokenExpired,
                  MissingContent)
from .utils import utc_now, calculate_mac, calculate_payload_hash, strings_match

# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

timestamp_skew_in_seconds = 60


class HawkEmptyValue:

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __bool__(self):
        return False

    def __repr__(self):
        return 'EmptyValve'


EmptyValue = HawkEmptyValue()


class AsyncHawkAuthority:
    async def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        await instance.__init__(*args, **kwargs)
        return instance

    async def __init__(self):
        pass

    async def _authorize(self,
                         mac_type,
                         credentials,
                         artifacts,
                         localtime_offset_in_seconds=0,
                         accept_untrusted_content=False):
        # 1.utc
        now = utc_now(offset_in_seconds=localtime_offset_in_seconds)

        # 7.calculate mac
        mac = calculate_mac(mac_type=mac_type, artifacts=artifacts)

        if not strings_match(mac, artifacts.mac):
            logging.error(f'MACs do not match:\n'
                          f'server: {mac}\n'
                          f'client: {artifacts.mac}')
            raise MacMismatch('Bad mac')

        # 8.check payload hash
        if 'hash' not in self.attributes and accept_untrusted_content:
            log.debug('Missing required payload hash.')
            check_hash = False
            content_hash = ''
        else:
            check_hash = True
            content_hash = artifacts.generate_content_hash()

        if check_hash:
            if not strings_match(content_hash, artifacts.hash):
                log.debug(f'Mismatch content: {artifacts.content}\n'
                          f'Mismatch content-type: {artifacts.content_type}')
                raise ContentHashMismatch(f'Bad payload hash')

        # 9.check nonce
        if artifacts.nonce_func:
            if await artifacts.nonce_func(credentials['key'],  # id or key?
                                          artifacts.nonce,
                                          artifacts.ts):
                raise InvalidNonce('Invalid nonce.')

        # 10.check time
        if math.fabs(float(artifacts.ts) - now) > timestamp_skew_in_seconds:
            # msg = f'timestamp {artifacts.ts} expired, now timestamp {now}'
            # tsm = calculate_ts_mac(now, credentials)
            raise TokenExpired(f'Stale timestamp')

        # 11.successful
        log.debug('Authorized Success.')

    def _make_header(self, mac):
        af = self.artifacts
        header = f'Hawk id="{af.id}"' \
                 f', ts="{af.ts}"' \
                 f', nonce="{af.nonce}"' \
                 f'''{', hash="'+af.hash+'"' if len(af.hash) != 0 else ''}''' \
                 f'''{', ext="'+af.ext+'", ' if len(af.ext) != 0 else ''}''' \
                 f', mac="{mac.decode()}"'

        if len(af.app) != 0:
            header = header + f', app="{af.app}", dlg="{af.dlg}"'

        log.debug(f'Generate header: {header}')

        return header


@dataclass
class Artifact:
    method: str
    ts: str
    nonce: str
    id: str
    url: InitVar[str]
    is_hash_content: bool = field(default=True)
    resource: str = field(init=False, default=None)
    content: Any = EmptyValue
    content_type: str = EmptyValue
    nonce_func: types.FunctionType = lambda _: False
    mac: str = ''
    host: str = ''
    port: str = ''
    key: str = ''
    algorithm: str = ''
    app: str = ''
    dlg: str = ''
    ext: str = ''
    hash: str = ''

    def __post_init__(self, url):
        if not url:
            raise ValueError('Empty url')
        # self.resource = url
        url_parts = self.generate_url_dict(url)
        log.debug(f'Parsed url parts:\n{url_parts}')
        self.resource = url_parts['url']
        self.host = url_parts['host']
        self.port = url_parts['port']

        self.ts = self.ts or utc_now()

    @property
    def content_hash(self):
        if not hasattr(self, '_content_hash'):
            raise AttributeError('Content hash has not been generated')
        return self._content_hash

    def generate_content_hash(self):
        if self.content == EmptyValue or self.content_type == EmptyValue:
            if self.is_hash_content:
                raise MissingContent('Can not hash content or content_type')
            self._content_hash = None
        else:
            self._content_hash = calculate_payload_hash(
                self.content, self.algorithm, self.content_type)
        return self.content_hash

    @staticmethod
    def generate_url_dict(url):
        url_parts = urlparse(url)
        url_dict = {
            'host': url_parts.hostname,
            'port': url_parts.port,
            'url': f'{url_parts.path}{"?"+url_parts.query if len(url_parts.query) > 0 else ""}'
        }
        return url_dict
