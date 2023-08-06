import base64
import calendar
import hashlib
import hmac
import logging
import math
import re
import time

from pprint import pformat

from .exc import (ParseError,
                  InvalidCredentials)

# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

HOST_HEADER_PTN = re.compile(r'^(?:(?:\r\n)?\s)*((?:[^:]+)|(?:\[[^\]]+\]))(?::(\d+))?(?:(?:\r\n)?\s)*$')
AUTH_HEADER_PTN = re.compile(r'(?P<key>\w+)="(?P<value>[^"\\]*)"\s*(?:,\s*|$)')

ALLOW_HEADER_KEYS = {'id', 'ts', 'nonce', 'hash', 'ext', 'mac', 'app', 'dlg'}
ALLOW_ALGORITHMS = {'sha1', 'sha256'}

HAWK_VERSION = '1'


def parse_host(request):
    # 解析host
    host_parts = HOST_HEADER_PTN.match(request.host).groups()
    return {
        'name': host_parts[0],
        'port': host_parts[1] if host_parts[1] else 80 if request.scheme is 'http' else 443
    }


def parse_request(request):
    # 判断是否是自己构建的request
    if 'headers' not in dir(request):
        return request

    host_parts = parse_host(request)
    headers = {
        'method': request.method,
        'url': f'{host_parts["name"]}:{host_parts["port"]}{request.path}'
               f'{"?"+request.query_string if len(request.query_string) > 0 else ""}',
        # 'host': host_parts['name'],
        # 'port': host_parts['port'],
        'authorization': request.headers.get('AUTHORIZATION'),
        'content_type': request.headers.get('CONTENT-TYPE', 'application/json')
    }

    return headers


def parse_authorization_header(header):
    """
        Hawk id="chiaki", ts="1538017451", nonce="HyDFh2", mac="p5P/6usb0us9e0JdPOmeQC88HXm/XsIDJ/mvIDOozsM="
    """
    scheme, attributes_string = (header.split(' ', 1))
    if scheme.lower() != 'hawk':
        raise ParseError(f'Unknown scheme: {scheme}')

    attributes = {}

    def replace_attribute(match):
        key, value = match.group('key', 'value')
        # Check valid attribute names
        if key not in ALLOW_HEADER_KEYS:
            raise ParseError(f'Unknown attribute: {key}')
        # Allowed attribute value characters
        # msg - Bad attribute value:

        # Check for duplicates
        if key in attributes:
            raise ParseError(f'Duplicate attribute: {key}')
        attributes[key] = value
        return ''

    leftover_header = AUTH_HEADER_PTN.sub(replace_attribute, attributes_string)
    if leftover_header != '':
        raise ParseError(f'Bad header format')

    log.debug(f'Attribute: \n{pformat(attributes)}')
    return attributes


def validate_credentials(creds):
    creds['id']
    creds['key']
    creds['algorithm']

    if creds['algorithm'] not in ALLOW_ALGORITHMS:
        raise InvalidCredentials(f'Unknown algorithm')


def utc_now(offset_in_seconds=0):
    # TODO: sntp support
    return int(math.floor(calendar.timegm(time.gmtime()) + float(offset_in_seconds)))


def calculate_mac(mac_type, artifacts):
    normalized = normalize_string(mac_type, artifacts)
    log.debug(f'Normalized:\n{normalized}')

    digest_mod = getattr(hashlib, artifacts.algorithm)  # ['algorithm']
    key = artifacts.key

    if not isinstance(normalized, (bytes, bytearray)):
        normalized = str.encode(normalized)
    if not isinstance(key, (bytes, bytearray)):
        key = str.encode(key)

    mac = hmac.new(key, normalized, digest_mod)
    return base64.b64encode(mac.digest())


def calculate_payload_hash(payload, algorithm, content_type):
    normalized = f'hawk.{HAWK_VERSION}.payload\n' \
                 f'{parse_content_type(content_type)}\n' \
                 f'{payload}\n'
    if not isinstance(normalized, (bytes, bytearray)):
        normalized = str.encode(normalized)

    p_hash = hashlib.new(algorithm)
    p_hash.update(normalized)
    return base64.b64encode(p_hash.digest())


def calculate_ts_mac(ts, credentials):
    normalized = f'hawk.{HAWK_VERSION}.ts\n' \
                 f'{ts}\n'
    logging.debug(f'ts mac: {normalized}')
    digest_mod = getattr(hashlib, credentials['algorithm'])
    key = credentials['key']

    if not isinstance(normalized, (bytes, bytearray)):
        normalized = str.encode(normalized)
    if not isinstance(key, (bytes, bytearray)):
        key = str.encode(key)

    mac = hmac.new(key, normalized, digest_mod)
    return base64.b64encode(mac.digest())


def normalize_string(mac_type, artifacts):
    normalized = f'hawk.{HAWK_VERSION}.{mac_type}\n' \
                 f'{artifacts.ts}\n' \
                 f'{artifacts.nonce}\n' \
                 f'{artifacts.method.upper()}\n' \
                 f'{artifacts.resource}\n' \
                 f'{artifacts.host.lower()}\n' \
                 f'{artifacts.port}\n' \
                 f'{artifacts.hash}\n'

    if artifacts.ext:
        normalized += artifacts.ext

    normalized += '\n'
    if artifacts.app:
        normalized += f'{artifacts.app}\n' \
                      f'{artifacts.dlg}\n'

    return normalized


def strings_match(a, b):
    if len(a) != len(b):
        return False
    result = 0

    def byte_ints(buf):
        for ch in buf:
            if not isinstance(ch, int):
                ch = ord(ch)
            yield ch

    for x, y in zip(byte_ints(a), byte_ints(b)):
        result |= x ^ y
    return result == 0


def parse_content_type(content_type):
    if content_type:
        return content_type.split(';')[0].strip().lower()
    else:
        return ''
