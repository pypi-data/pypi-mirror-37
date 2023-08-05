from web3.middleware import geth_poa_middleware
import web3
import hashlib
import ecdsa


class EthereumClient:
    def __init__(self, state, network_url=None, private_key=None, cosigner_address=None):
        self.state = state

        if network_url is None:
            network_url = "http://localhost:8545"

        self.w3 = web3.Web3(web3.HTTPProvider(network_url))
        self.network_id = self.w3.version.network

        if str(self.network_id) in ("4", "42", "77", "99"):
            self.w3.middleware_stack.inject(geth_poa_middleware, layer=0)

        if type(private_key) is str:
            if private_key.startswith("0x"):
                self.private_key = bytes(bytearray.fromhex(private_key[2:]))
            else:
                self.private_key = bytes(bytearray.fromhex(private_key))
        else:
            self.private_key = None

        if self.private_key is None:
            self.sender_address = self.w3.eth.accounts[0]
        else:
            self.sender_address = self.get_address_from_private_key(self.private_key)

        if cosigner_address is None:
            self.cosigner_address = cosigner_address
        else:
            self.cosigner_address = self.w3.toChecksumAddress(cosigner_address)

    def get_nonce(self):
        key = "{}_{}_nonce".format(self.network_id, self.sender_address)
        local_nonce = self.state.get_state(key)
        blockchain_nonce = self.w3.eth.getTransactionCount(self.sender_address)

        if local_nonce is None or blockchain_nonce > local_nonce:
            self.state.set_state(key, blockchain_nonce)
            return blockchain_nonce
        else:
            return local_nonce

    def get_address_from_private_key(self, private_key):
        return self.w3.toChecksumAddress("0x" + self.w3.sha3(hexstr=ecdsa.SigningKey.from_string(string=private_key, curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256).get_verifying_key().to_string().hex())[12:].hex())

