from web3_sim import connectProvider, get_abi, connectContract
from web3 import Web3
from web3_deployed_contract import DeployedContract

class ERC20(DeployedContract):
    def __init__(self, address, abi_path, web3):
        super().__init__(address, abi_path, web3)

    def balance(self, address):
        return self.contract.caller.balanceOf(address)

    def approve(self, from_account, spender, amount):
        return self.contract.functions.approve(spender, amount).transact({'from': from_account})
