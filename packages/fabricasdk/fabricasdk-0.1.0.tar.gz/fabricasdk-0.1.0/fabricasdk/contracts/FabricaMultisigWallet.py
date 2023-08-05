from ..Contract import Contract


class FabricaMultisigWallet(Contract):
    def __init__(self, eth_client):
        super().__init__(eth_client, "fabrica-multisig-wallet")
        self.contracts = {}

    def get_contract(self, customer_address):
        if customer_address not in self.contracts:

            wallet_address = self.eth_client.factory.multisig_wallet_address(customer_address)

            if wallet_address is None:
                raise Exception("no multisig wallets deployed for {}".format(customer_address))

            self.contracts[customer_address] = self.eth_client.w3.eth.contract(address=wallet_address, abi=self.contract_def["abi"])

        return self.contracts[customer_address]

    # AUTO GENERATED #

    def transactions(self, customer_address, arg0):
        result = self.get_contract(customer_address).functions.transactions(Contract.type_converter(arg0, "uint256")).call() 
        return {"destination": result[0], "value": result[1], "data": result[2], "executed": result[3]}

    def get_transaction_count(self, customer_address, pending, executed):
        result = self.get_contract(customer_address).functions.getTransactionCount(**{"pending": Contract.type_converter(pending, "bool"), "executed": Contract.type_converter(executed, "bool")}).call() 
        return {"count": result[0] if isinstance(result, list) else result}

    def get_owners(self, customer_address):
        result = self.get_contract(customer_address).functions.getOwners().call() 
        return result

    def get_transaction_ids(self, customer_address, from_address, to_address, pending, executed):
        result = self.get_contract(customer_address).functions.getTransactionIds(**{"from": Contract.type_converter(from_address, "uint256"), "to": Contract.type_converter(to_address, "uint256"), "pending": Contract.type_converter(pending, "bool"), "executed": Contract.type_converter(executed, "bool")}).call() 
        return {"transaction_ids": result[0] if isinstance(result, list) else result}
