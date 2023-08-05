import json
import ipfsapi
from os.path import expanduser, isfile, join
from os import linesep
from .EthereumClient import EthereumClient
from .FabricaApiClient import FabricaApiClient
from .State import State
from .contracts.FabricaToken import FabricaToken
from .contracts.FabricaMultisigWallet import FabricaMultisigWallet
from .contracts.FabricaMultisigFactory import FabricaMultisigFactory


class FabricaSdk:
    def __init__(self, config=None, state_plugin=None):
        # config parser
        if config is None:
            default_path = join(expanduser("~"), "fabrica-config.json")
            if isfile(default_path):
                with open(default_path) as json_data_file:
                    self.config = json.load(json_data_file)
            else:
                self.config = {}
        elif isinstance(config, str):
            if isfile(config):
                with open(config) as json_data_file:
                    self.config = json.load(json_data_file)
            else:
                raise Exception("Config file not found")
        elif not isinstance(config, dict):
            raise Exception("Wrong config parameter")

        for key in "private_key", \
                   "cosigner_address", \
                   "fabrica_api_url", \
                   "fabrica_api_key", \
                   "network_url", \
                   "ipfs_endpoint", \
                   "ipfs_port", \
                   "local_state_path":
            if key not in self.config:
                self.config[key] = None

        # state initialization
        self.state = State(
            state_plugin=state_plugin,
            local_state_path=self.config["local_state_path"]
        )

        # ethereum client initialization
        try:
            self.eth_client = EthereumClient(
                self.state,
                network_url=self.config["network_url"],
                private_key=self.config["private_key"],
                cosigner_address=self.config["cosigner_address"]
            )
        except Exception as e:
            self.eth_client = None
            print("WARNING, EthereumClient initialization error:" + linesep + "{}".format(e))

        # api client initialization
        if self.config["fabrica_api_url"] is not None and self.config["fabrica_api_key"] is not None:
            self.api = FabricaApiClient(
                fabrica_api_url=self.config["fabrica_api_url"],
                fabrica_api_key=self.config["fabrica_api_key"]
            )
        else:
            self.api = None

        # ipfs client initialization
        self.ipfs_client = ipfsapi.connect(
            self.config["ipfs_endpoint"] if self.config["ipfs_endpoint"] is not None else "https://ipfs.infura.io",
            self.config["ipfs_port"] if self.config["ipfs_port"] is not None else 5001
        )

        # contracts initialization
        if self.eth_client:
            self.token = self.eth_client.token = FabricaToken(self.eth_client, self.ipfs_client, self.api)
            self.multisig = self.eth_client.multisig = FabricaMultisigWallet(self.eth_client)
            self.factory = self.eth_client.factory = FabricaMultisigFactory(self.eth_client)
        else:
            self.token = self.multisig = self.factory = None
