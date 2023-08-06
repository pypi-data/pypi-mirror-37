import asyncio

from .exceptions import BlobStorageUnrecognizedProviderError
from .providers import (Backblaze, ProviderAuthenticationError,
                        ProviderFileUploadError, PROVIDERS, )


class BlobStorage:
    PROVIDER_ADAPTER = {
        'backblaze': {
            'adapter': Backblaze,
            'required': ('account_id', 'app_key'),
        }
    }

    def __init__(self, provider, credentials):
        if provider not in PROVIDERS:
            raise BlobStorageUnrecognizedProviderError
        if not all(r in credentials.keys()
                   for r in self.PROVIDER_ADAPTER[provider]['required']):
            raise KeyError
        self.provider = self.PROVIDER_ADAPTER[provider]['adapter'](credentials)
        self.loop = asyncio.get_event_loop()

    async def _upload_file(self, bucket_id, file_to_upload):
        auth_response = await self.provider.authenticate()
        if not auth_response:
            raise ProviderAuthenticationError
        upload_file_response = await self.provider.upload_file(
            bucket_id, file_to_upload['path'], file_to_upload['content_type'])
        if not upload_file_response:
            raise ProviderFileUploadError
        return upload_file_response

    def upload_files(self, bucket_id, files_to_upload):
        async def _upload_files():
            futures = []
            for file_to_upload in files_to_upload:
                future = asyncio.ensure_future(
                    self._upload_file(bucket_id, file_to_upload))
                futures.append(future)
            return await asyncio.gather(*futures)
        return self.loop.run_until_complete(_upload_files())
