from web3_deployed_contract import DeployedContract

class UniswapFactory(DeployedContract):
    def __init__(self, web3):
        super().__init__("0x1F98431c8aD98523631AE4a59f267346ea31F984", '../uniswap/v3-core/artifacts/contracts/UniswapV3Factory.sol/UniswapV3Factory.json', web3)

    def create_pool(self, side1, side2, sender):
        address = self.pool_address(side1, side2, sender)
        self.contract.functions.createPool(side1.contract.address, side2.contract.address, 3000).transact({"from": sender})
        return address

    def pool_address(self, side1, side2, sender):
        return self.contract.functions.createPool(side1.contract.address, side2.contract.address, 3000).call({"from": sender})
