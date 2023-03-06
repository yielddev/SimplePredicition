from web3_sim import connectProvider, get_abi, connectContract
from web3 import Web3

class DeployedContract:
    def __init__(self, address, abi_path, web3):
        self.web3 = web3
        self.abi = get_abi(abi_path)
        self.contract = connectContract(self.web3, Web3.toChecksumAddress(address), self.abi)


