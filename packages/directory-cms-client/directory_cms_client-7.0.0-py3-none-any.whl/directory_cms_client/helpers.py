import abc
from functools import wraps
import json
import logging
from urllib.parse import urlencode

from django.conf import settings
from django.shortcuts import Http404

from requests.exceptions import HTTPError, RequestException
from w3lib.url import canonicalize_url


logger = logging.getLogger(__name__)


MESSAGE_CACHE_HIT = 'CMS fallback cache hit. Displaying cached content.'
MESSAGE_CACHE_MISS = 'CMS fallback cache miss. Cannot display any content.'
MESSAGE_NOT_FOUND = 'Page not found in CMS'


class AbstractCMSResponse(abc.ABC):

    def __init__(self, content, status_code, raw_response=None):
        self.content = content
        self.status_code = status_code
        self.raw_response = raw_response

    def raise_for_status(self):
        if not 200 <= self.status_code < 300:
            raise HTTPError(self.content)

    def json(self):
        return json.loads(self.content.decode('utf-8'))

    @classmethod
    def from_response(cls, response):
        return cls(
            content=response.content,
            status_code=response.status_code,
            raw_response=response,
        )


class CMSLiveResponse(AbstractCMSResponse):
    pass


class CMSCacheResponse(AbstractCMSResponse):
    pass


class CMSFailureResponse(AbstractCMSResponse):
    pass


def fallback(cache):
    """
    Caches CMS content retrieved by the client, thus allowing the cached
    content to be used later if the live CMS content cannot be retrieved.

    """

    def get_cache_response(cache_key):
        content = cache.get(cache_key)
        if content:
            return CMSCacheResponse(content=content, status_code=200)

    def closure(func):
        @wraps(func)
        def wrapper(client, url, params={}, *args, **kwargs):
            cache_key = canonicalize_url(url + '?' + urlencode(params))
            try:
                cms_response = func(
                    client, url=url, params=params, *args, **kwargs
                )
            except RequestException:
                # Failed to create the request e.g., the CMS is down, perhaps a
                # timeout occurred, or even connection closed by CMS, etc.
                response = get_cache_response(cache_key)
                if response:
                    logger.error(MESSAGE_CACHE_HIT, extra={'url': url})
                else:
                    raise
            else:
                log_context = {
                    'status_code': cms_response.status_code, 'url': url
                }
                if cms_response.status_code == 404:
                    logger.error(MESSAGE_NOT_FOUND, extra=log_context)
                    return CMSLiveResponse.from_response(cms_response)
                elif not cms_response.ok:
                    # Successfully requested the content, but the response is
                    # not OK (e.g., 500, 403, etc)
                    response = get_cache_response(cache_key)
                    if response:
                        logger.error(MESSAGE_CACHE_HIT, extra=log_context)
                    else:
                        logger.exception(MESSAGE_CACHE_MISS, extra=log_context)
                        response = CMSFailureResponse.from_response(
                            cms_response
                        )
                else:
                    cache.set(
                        cache_key,
                        cms_response.content,
                        settings.DIRECTORY_CMS_API_CLIENT_CACHE_EXPIRE_SECONDS
                    )
                    response = CMSLiveResponse.from_response(cms_response)
            return response
        return wrapper
    return closure


def handle_cms_response(response):
    if response.status_code == 404:
        raise Http404()
    response.raise_for_status()
    return response.json()


def handle_cms_response_allow_404(response):
    if response.status_code == 404:
        return {}
    response.raise_for_status()
    return response.json()
