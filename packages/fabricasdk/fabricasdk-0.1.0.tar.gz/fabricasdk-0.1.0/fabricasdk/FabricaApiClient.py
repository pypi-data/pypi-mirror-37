from posixpath import join
import json
import requests


class FabricaApiClient:
    def __init__(self, fabrica_api_url, fabrica_api_key):
        self.fabrica_api_url = fabrica_api_url
        self.fabrica_api_key = fabrica_api_key

    def _request(self, method, function_name, data=None):
        if isinstance(data, dict):
            data = json.dumps(data)

        r = getattr(requests, method)(
            join(self.fabrica_api_url, function_name),
            headers={
                "x-secret": self.fabrica_api_key,
                "content-type": "application/json"
            },
            data=data
        )

        if r.ok:
            return r.json()
        else:
            raise ConnectionError(r.json())

    def create_ipfs_metadata(self, metadata):
        return self._request("post", "programmatic/createIpfsMetadata", data=metadata)["ipfsUri"]

    def create_ipfs_document(self, data, document_type):
        return self._request("post", "programmatic/createIpfsDocument", data={"type": document_type, "data": data})["ipfsUri"]
