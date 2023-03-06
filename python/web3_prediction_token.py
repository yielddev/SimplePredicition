from web3_erc20 import ERC20

class PredictionToken(ERC20):
    def __init__(self, address, web3):
        super().__init__(address, '../artifacts/contracts/PredictionToken.sol/PredictionToken.json', web3)
