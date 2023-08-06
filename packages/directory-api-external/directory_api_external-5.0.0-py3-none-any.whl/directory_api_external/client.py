from django.conf import settings

from directory_client_core.base import AbstractAPIClient

from directory_api_external.supplier import SupplierAPIClient
from directory_api_external.version import __version__


class DirectoryAPIExternalClient(AbstractAPIClient):

    endpoints = {
        'ping': 'healthcheck/ping/',
    }

    version = __version__

    def __init__(self, *args, **kwargs):
        self.supplier = SupplierAPIClient(*args, **kwargs)
        super().__init__(*args, **kwargs)

    def ping(self):
        return self.get(url=self.endpoints['ping'])


api_client = DirectoryAPIExternalClient(
    base_url=settings.DIRECTORY_API_CLIENT_EXTERNAL_BASE_URL,
    api_key=settings.DIRECTORY_API_CLIENT_EXTERNAL_API_KEY,
    sender_id=settings.DIRECTORY_API_CLIENT_EXTERNAL_SENDER_ID,
    timeout=settings.DIRECTORY_API_CLIENT_EXTERNAL_DEFAULT_TIMEOUT,
)
