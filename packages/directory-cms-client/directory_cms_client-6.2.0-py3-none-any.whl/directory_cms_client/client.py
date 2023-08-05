import directory_client_core.base

from django.conf import settings
from django.core.cache import caches

from directory_cms_client.version import __version__
from directory_cms_client import helpers


def build_params(
    tag_slug=None, full_path=None,
    language_code=None, draft_token=None, fields=None
):
    params = {'fields': fields or ['*']}
    if language_code:
        params['lang'] = language_code
    if draft_token:
        params['draft_token'] = draft_token
    if full_path:
        params['full_path'] = full_path
    if tag_slug:
        params['tag_slug'] = tag_slug
    return params


class DirectoryCMSClient(directory_client_core.base.AbstractAPIClient):
    endpoints = {
        'ping': 'healthcheck/ping/',
        'page-by-type': '/api/pages/lookup-by-type/{page_type}/',
        'page-by-slug': '/api/pages/lookup-by-slug/{slug}/',
        'page-by-tag': '/api/pages/lookup-by-tag/',
        'page-by-full-path': '/api/pages/lookup-by-full-path/',
        'pages-by-type': '/api/pages/'
    }
    version = __version__

    def __init__(self, base_url, api_key, sender_id, timeout, service_name,):
        super().__init__(base_url, api_key, sender_id, timeout)
        self.service_name = service_name

    def ping(self):
        return self.get(url=self.endpoints['ping'])

    @helpers.fallback(cache=caches['cms_fallback'])
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def lookup_by_tag(
        self,
        tag_slug,
        fields=None,
        draft_token=None,
        language_code=None,
    ):
        params = build_params(
            tag_slug=tag_slug, fields=fields,
            language_code=language_code, draft_token=draft_token
        )
        return self.get(url=self.endpoints['page-by-tag'], params=params)

    def lookup_by_slug(
        self,
        slug,
        fields=None,
        draft_token=None,
        language_code=None,
    ):
        base_params = build_params(
            fields=fields, language_code=language_code, draft_token=draft_token
        )
        return self.get(
            url=self.endpoints['page-by-slug'].format(slug=slug),
            params={
                **base_params,
                'service_name': self.service_name
            },
        )

    def lookup_by_full_path(
        self,
        full_path,
        fields=None,
        draft_token=None,
        language_code=None,
    ):
        base_params = build_params(
            fields=fields, language_code=language_code,
            draft_token=draft_token, full_path=full_path
        )
        return self.get(
            url=self.endpoints['page-by-full-path'],
            params={
                **base_params,
            },
        )

    def list_by_page_type(
        self, page_type, fields=None, draft_token=None, language_code=None
    ):
        base_params = build_params(
            fields=fields, language_code=language_code, draft_token=draft_token
        )
        return self.get(
            url=self.endpoints['pages-by-type'],
            params={
                **base_params,
                'type': page_type,
            },
        )


cms_api_client = DirectoryCMSClient(
    base_url=settings.DIRECTORY_CMS_API_CLIENT_BASE_URL,
    api_key=settings.DIRECTORY_CMS_API_CLIENT_API_KEY,
    sender_id=settings.DIRECTORY_CMS_API_CLIENT_SENDER_ID,
    timeout=settings.DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT,
    service_name=settings.DIRECTORY_CMS_API_CLIENT_SERVICE_NAME,
)
