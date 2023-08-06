import logging

from .abs import AsyncHawkAuthority, Artifact, EmptyValue
from .utils import calculate_mac

# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class Sender(AsyncHawkAuthority):

    async def __init__(self,
                       url,
                       method,
                       credentials,
                       content=EmptyValue,
                       content_type=EmptyValue,
                       is_hash_content=True,
                       nonce=None,
                       **kwargs):
        # TODO: validate url

        self.artifacts = Artifact(**{
            **credentials,
            **dict(
                url=url,
                method=method,
                nonce_func=None,
                ts=kwargs.get('ts'),
                content_type=content_type,
                nonce=nonce,
                content=content,
                is_hash_content=is_hash_content
            )})
        if is_hash_content:
            self.artifacts.hash = self.artifacts.generate_content_hash().decode()

        mac = calculate_mac('header',
                            self.artifacts)

        log.debug(mac)
        self.request_header = self._make_header(mac)

