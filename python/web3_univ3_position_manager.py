from web3_deployed_contract import DeployedContract
class UniV3PositionManager(DeployedContract):
    def __init__(self, web3):
        super().__init__("0xC36442b4a4522E871399CD717aBDD847Ab11FE88", '../uniswap/v3-periphery/artifacts/contracts/NonfungiblePositionManager.sol/NonfungiblePositionManager.json', web3)

    def mint(self, token_0, token_1, fee, tick_lower, tick_upper, amount_0, amount_1, account, deadline):
        return self.contract.functions.mint(
            (
                token_0,
                token_1,
                fee,
                tick_lower,
                tick_upper,
                amount_0,
                amount_1,
                0,
                0,
                account,
                deadline
            )
        ).transact({"from": account})
