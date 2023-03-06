from web3 import Web3
from web3_sim import connectProvider, get_abi, connectContract
from web3_erc20 import ERC20
import json

class MockUsdc(ERC20):
    def __init__(self, address, web3):
        super().__init__(address, '../artifacts/contracts/MockUSDC.sol/MockUSDC.json', web3)

    # Amount in ether units
    # to_address
    # returns tx hash
    def mint(self, to_address, amount):
        receipt = self.contract.functions.mint(Web3.toChecksumAddress(to_address), amount).transact()
        return receipt

# def main():
#     usd = MockUsdc('0x909b91a21d0f86709c4eec651e82a4efb028c330')
#     account_zero = usd.web3.eth.accounts[0]
#     print(usd.mint(account_zero, 10))
#     print(Web3.fromWei(usd.balance(account_zero), "ether"))
#
#
# main()
