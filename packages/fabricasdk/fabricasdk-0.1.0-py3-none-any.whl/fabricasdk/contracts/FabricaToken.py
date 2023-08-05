from ..Contract import Contract
import requests
from rfc3986 import uri_reference


class FabricaToken(Contract):
    def __init__(self, eth_client, ipfs_client, api):
        super().__init__(eth_client, "fabrica-token")
        self.ipfs_client = ipfs_client
        self.api = api

    def _get_token_metadata(self, uri):
        reference = uri_reference(uri)
        scheme = reference.scheme
        if scheme in ("http", "https"):
            try:
                return requests.get(uri).json()
            except:
                # todo: error handling here
                return None
        elif scheme == "ipfs":
            try:
                return self.ipfs_client.get_json(reference.path)
            except:
                # todo: error handling here
                return None
        else:
            return None

    def mint(
        self,
        token_id,
        geohash,
        holding_entity,
        token_metadata,
        cosign=True,
        customer_address=None
    ):
        if self.get_token(token_id) is not None:
            raise ValueError("token {} already exists".format(token_id))

        if isinstance(token_metadata, dict):
            if self.api is None:
                raise ValueError("\"fabrica_api_url\" and \"fabrica_api_key\" must be configured")

            if "document" in token_metadata and isinstance(token_metadata["document"], dict):
                token_metadata["document"] = self.api.create_ipfs_document(token_metadata["document"], "title-holding-trust")

            token_metadata = self.api.create_ipfs_metadata(token_metadata)

        return self.mint_raw(
            token_id=token_id,
            geohash=geohash,
            holding_entity=holding_entity,
            token_uri=token_metadata,
            cosign=cosign,
            customer_address=customer_address
        )

    # todo
    def update_token(self, *args, cosign=True, **kwargs):
        if self.api is not None:
            pass
        else:
            return self.update_token_raw(*args, cosign=cosign, **kwargs)

    def get_token(self, *args, **kwargs):
        token = self.get_token_raw(*args, **kwargs)
        token["metadata"] = self._get_token_metadata(token["token_uri"])
        for key, value in token.items():
            if key != "token_id" and value not in ('', None):
                break
        else:
            return None

        return token

    # AUTO GENERATED #

    def transfer_from(self, from_address, to_address, token_id, cosign=True, customer_address=None):
        return self._send_tx(self.contract.functions.transferFrom, **{"_from": Contract.type_converter(from_address, "address"), "_to": Contract.type_converter(to_address, "address"), "_tokenId": Contract.type_converter(token_id, "uint256")}, cosign=cosign, customer_address=customer_address)

    def mint_raw(self, token_id, geohash, holding_entity, token_uri, cosign=True, customer_address=None):
        return self._send_tx(self.contract.functions.mint, **{"_tokenId": Contract.type_converter(token_id, "uint256"), "_geohash": Contract.type_converter(geohash, "string"), "_holdingEntity": Contract.type_converter(holding_entity, "string"), "_tokenURI": Contract.type_converter(token_uri, "string")}, cosign=cosign, customer_address=customer_address)

    def set_token_uri(self, token_id, token_uri, cosign=True, customer_address=None):
        return self._send_tx(self.contract.functions.setTokenURI, **{"_tokenId": Contract.type_converter(token_id, "uint256"), "_tokenURI": Contract.type_converter(token_uri, "string")}, cosign=cosign, customer_address=customer_address)

    def update_token_raw(self, token_id, holding_entity, token_uri, cosign=True, customer_address=None):
        return self._send_tx(self.contract.functions.updateToken, **{"_tokenId": Contract.type_converter(token_id, "uint256"), "_holdingEntity": Contract.type_converter(holding_entity, "string"), "_tokenURI": Contract.type_converter(token_uri, "string")}, cosign=cosign, customer_address=customer_address)

    def get_token_raw(self, token_id):
        result = self.contract.functions.getToken(**{"_tokenId": Contract.type_converter(token_id, "uint256")}).call() 
        return {"token_id": result[0], "geohash": result[1], "holding_entity": result[2], "token_uri": result[3]}
