from web3_deployed_contract import DeployedContract
class UniV3Quoter(DeployedContract):
    def __init__(self, web3):
        super().__init__(
            "0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6",
            "../uniswap/v3-periphery/artifacts/contracts/interfaces/IQuoter.sol/IQuoter.json",
            web3
        )

    def get_token_token_price(self, token0, token1, fee, qty, sqrtPriceLimitX96):
        return self.contract.functions.quoteExactOutputSingle(
            token0,
            token1,
            fee,
            qty,
            sqrtPriceLimitX96
        ).call()
