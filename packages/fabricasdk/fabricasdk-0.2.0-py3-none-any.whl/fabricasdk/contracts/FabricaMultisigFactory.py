from ..Contract import Contract


class FabricaMultisigFactory(Contract):
    def __init__(self, eth_client):
        super().__init__(eth_client, "fabrica-multisig-factory")

    def _check_config(self):
        if self.eth_client.user_address is None:
            raise ValueError("the user_address must be not None")

        if self.eth_client.cosigner_address is None:
            raise ValueError("the cosigner_address must be not None")

        if self.eth_client.cosigner_address == self.eth_client.user_address:
            raise ValueError("the cosigner_address must be different from the user_address")

    def create(self, customer_address):
        self._check_config()

        customer_address = self.eth_client.w3.toChecksumAddress(customer_address)

        if customer_address in (self.eth_client.user_address, self.eth_client.cosigner_address):
            raise ValueError("the customer_address must be different from the user_address and the cosigner_address")

        wallet_address = self.get_wallet_of_customer(customer_address)
        if wallet_address is None:
            return self.create_raw([self.eth_client.user_address, customer_address, self.eth_client.cosigner_address], 2)
        else:
            raise Exception("{} address is already linked to {} wallet".format(customer_address, wallet_address))

    def get_wallet_of_customer(self, customer_address):
        result = self.get_wallet_of_customer_raw(self.eth_client.user_address, customer_address)
        if result == "0x0000000000000000000000000000000000000000":
            return None
        else:
            return result

    # AUTO GENERATED #

    def get_users(self):
        result = self.contract.functions.getUsers().call() 
        return result

    def user_count(self):
        result = self.contract.functions.userCount().call() 
        return result

    def user_exists(self, user):
        result = self.contract.functions.userExists(**{"_user": Contract.type_converter(user, "address")}).call() 
        return result

    def user_mapping(self, arg0):
        result = self.contract.functions.userMapping(Contract.type_converter(arg0, "address")).call() 
        return {"user_address": result[0] if isinstance(result, list) else result}

    def customer_exists(self, user, customer):
        result = self.contract.functions.customerExists(**{"_user": Contract.type_converter(user, "address"), "_customer": Contract.type_converter(customer, "address")}).call() 
        return result

    def get_user_customers(self, user):
        result = self.contract.functions.getUserCustomers(**{"_user": Contract.type_converter(user, "address")}).call() 
        return result

    def get_wallet_of_customer_raw(self, user, customer_address):
        result = self.contract.functions.getWalletOfCustomer(**{"_user": Contract.type_converter(user, "address"), "_customerAddress": Contract.type_converter(customer_address, "address")}).call() 
        return result

    def change_customer_address(self, user, old_address, new_address):
        return self._send_tx(self.contract.functions.changeCustomerAddress, **{"_user": Contract.type_converter(user, "address"), "_oldAddress": Contract.type_converter(old_address, "address"), "_newAddress": Contract.type_converter(new_address, "address")}, cosign=False)

    def user_customer_count(self, user):
        result = self.contract.functions.userCustomerCount(**{"_user": Contract.type_converter(user, "address")}).call() 
        return result

    def create_raw(self, owners, required):
        return self._send_tx(self.contract.functions.create, **{"_owners": Contract.type_converter(owners, "address[]"), "_required": Contract.type_converter(required, "uint256")}, cosign=False)
