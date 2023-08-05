from web3 import Web3
import json
import os
from pathlib import Path


class Contract:
    def __init__(self, eth_client, contract_name):
        self.eth_client = eth_client

        # contracts initialization
        self.contract_def = Contract.get_contract_def(contract_name)

        if self.contract_def["networks"] is not None:
            if eth_client.network_id not in self.contract_def["networks"]:
                raise Exception("{} network is not available in {} networks".format(eth_client.network_id, contract_name))

            self.address = eth_client.w3.toChecksumAddress(self.contract_def["networks"][eth_client.network_id]["address"])
            self.contract = eth_client.w3.eth.contract(address=self.address, abi=self.contract_def["abi"])

    def _send_tx(self, contract_function, *args, customer_address=None, cosign=True, **kwargs):
        transaction = contract_function(*args, **kwargs)
        if cosign:
            if customer_address is None:
                print(
                    "To execute {} with a cosigner the positional argument 'customer_address' is required, "
                    "otherwise set the positional argument 'cosign' = False".format(contract_function)
                )
            contract = self.eth_client.multisig.get_contract(customer_address)
            tx_params = {
                "from": self.eth_client.sender_address
            }
            transaction = transaction.buildTransaction(tx_params)
            transaction = contract.functions.submitTransaction(self.address, 0, transaction["data"])

        if self.eth_client.private_key:
            tx_params = {
                "nonce": self.eth_client.get_nonce(),
                "from": self.eth_client.sender_address,
                "value": 0,
                "gas": 4000000,
                "gasPrice": self.eth_client.w3.eth.gasPrice
            }
            transaction = transaction.buildTransaction(tx_params)
            raw_transaction = self.eth_client.w3.eth.account.signTransaction(transaction, self.eth_client.private_key).rawTransaction
            tx_hash = self.eth_client.w3.eth.sendRawTransaction(raw_transaction).hex()
        else:
            tx_params = {
                "from": self.eth_client.sender_address,
                "value": 0,
                "gas": 4000000,
                "gasPrice": self.eth_client.w3.eth.gasPrice
            }
            tx_hash = transaction.transact(tx_params).hex()

        receipt = self.eth_client.w3.eth.waitForTransactionReceipt(tx_hash)
        return receipt

    @staticmethod
    def type_converter(value, required_type):
        if required_type.endswith("[]"):
            return list(map(lambda x: Contract.type_converter(x, required_type.replace("[]", "")), value))
        else:
            if "int" in required_type:
                return Web3.toInt(text=value)
            elif "bytes32" in required_type:
                return Web3.toBytes(text=value).ljust(32, b"\0") \
                    if not value.startswith("0x") else Web3.toBytes(hexstr=value).ljust(32, b"\0")
            elif "byte" in required_type:
                return Web3.toBytes(text=value) \
                    if not value.startswith("0x") else Web3.toBytes(hexstr=value)
            elif "address" in required_type:
                return Web3.toChecksumAddress(value)
            elif "bool" in required_type:
                return bool(value)
            else:
                return str(value)

    @staticmethod
    def get_contract_def(contract_name, contract_artifacts_root=None):
        if contract_artifacts_root is None:
            contract_artifacts_root = Path(__file__).absolute().parent.joinpath("resources", "blockchain")

        contract_def = {}
        with open(Path(__file__).absolute().parent.joinpath(contract_artifacts_root, contract_name, "abi.json")) as f:
            contract_def["abi"] = json.load(f)

        networks_path = Path(__file__).absolute().parent.joinpath(contract_artifacts_root, contract_name, "networks.json")
        if os.path.isfile(networks_path):
            with open(networks_path) as f:
                contract_def["networks"] = json.load(f)
        else:
            contract_def["networks"] = None

        return contract_def
