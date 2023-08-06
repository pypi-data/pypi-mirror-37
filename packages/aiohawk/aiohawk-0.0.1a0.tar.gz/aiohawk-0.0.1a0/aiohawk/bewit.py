import base64
import logging
import re

from collections import namedtuple

from .abs import Artifact
from .exc import InvalidBewit
from .utils import utc_now, calculate_mac, strings_match

# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def get_bewit(url, credentials, ext='', ttl_sec=3600):
    log.debug(url)

    artifact = Artifact(
        url=url,
        method='GET',
        ext=ext,
        ts=utc_now() + ttl_sec,
        nonce='',
        **credentials
    )

    mac = calculate_mac('bewit', artifact)

    if isinstance(mac, (bytes, bytearray)):
        mac = mac.decode('ascii')

    inner_bewit = f'{artifact.id}\\{artifact.ts}\\{mac}\\{ext}'
    inner_bewit_bytes = inner_bewit.encode('ascii')
    bewit_bytes = base64.urlsafe_b64encode(inner_bewit_bytes)

    return bewit_bytes.decode('ascii')


bewittuple = namedtuple('bewittuple', ['id', 'exp', 'mac', 'ext'])


def parse_bewit(bewit):
    decoded_bewit = base64.b64decode(bewit).decode('ascii')
    bewit_parts = decoded_bewit.split('\\')
    if len(bewit_parts) != 4:
        raise InvalidBewit('Invalid bewit structure')
    return bewittuple(*bewit_parts)


def strip_bewit(url):
    m = re.search('[?&]bewit=([^&]+)', url)
    if not m:
        raise InvalidBewit('Empty bewit')
    bewit = m.group(1)
    stripped_url = url[:m.start()] + url[m.end():]
    return bewit, stripped_url


async def check_bewit(url, credentials_func):
    now = utc_now()

    raw_bewit, stripped_url = strip_bewit(url)
    bewit = parse_bewit(raw_bewit)

    try:
        credentials = await credentials_func(bewit.id)
    except LookupError:
        raise Exception

    artifact = Artifact(
        url=stripped_url,
        method='GET',
        ext=bewit.ext,
        ts=bewit.exp,
        nonce='',
        **credentials
    )

    mac = calculate_mac('bewit', artifact)
    mac = mac.decode('ascii')

    if not strings_match(mac, bewit.mac):
        raise Exception

    if int(bewit.exp) < now:
        raise Exception

    return True
