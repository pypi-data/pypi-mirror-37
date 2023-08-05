from ..Contract import Contract


class FabricaMultisigFactory(Contract):
    def __init__(self, eth_client):
        super().__init__(eth_client, "fabrica-multisig-factory")

    def _check_config(self):
        if self.eth_client.sender_address is None:
            raise ValueError("the sender_address must be not None")

        if self.eth_client.cosigner_address is None:
            raise ValueError("the cosigner_address must be not None")

        if self.eth_client.cosigner_address == self.eth_client.sender_address:
            raise ValueError("the cosigner_address must be different from the sender_address")

    def create(self, customer_address):
        self._check_config()

        customer_address = self.eth_client.w3.toChecksumAddress(customer_address)

        if customer_address in (self.eth_client.sender_address, self.eth_client.cosigner_address):
            raise ValueError("the customer_address must be different from the sender_address and the cosigner_address")

        wallet_address = self.multisig_wallet_address(customer_address)
        if wallet_address is None:
            return self.create_raw([self.eth_client.sender_address, self.eth_client.cosigner_address, customer_address], 2)
        else:
            raise Exception("{} address is already linked to {} wallet".format(customer_address, wallet_address))

    def multisig_wallet_address(self, customer_address):
        result = self.multisig_wallet_address_raw(customer_address)
        if result == "0x0000000000000000000000000000000000000000":
            return None
        else:
            return result

    # AUTO GENERATED #

    def list_end_users(self):
        result = self.contract.functions.listEndUsers().call() 
        return result

    def multisig_wallet_address_raw(self, arg0):
        result = self.contract.functions.multisigWalletAddress(Contract.type_converter(arg0, "address")).call() 
        return result

    def change_address(self, old_address, new_address):
        return self._send_tx(self.contract.functions.changeAddress, **{"oldAddress": Contract.type_converter(old_address, "address"), "newAddress": Contract.type_converter(new_address, "address")}, cosign=False)

    def create_raw(self, owners, required):
        return self._send_tx(self.contract.functions.create, **{"_owners": Contract.type_converter(owners, "address[]"), "_required": Contract.type_converter(required, "uint256")}, cosign=False)
