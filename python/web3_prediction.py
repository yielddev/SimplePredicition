from web3_deployed_contract import DeployedContract
from web3_prediction_token import PredictionToken

class Prediction(DeployedContract):
    def __init__(self, address, web3):
        super().__init__(address, '../artifacts/contracts/Prediction.sol/Prediction.json', web3)
        self.side_one = self.get_side_one()
        self.side_two = self.get_side_two()
    def get_side_one(self):
        address = self.contract.caller.side1()
        return PredictionToken(address, self.web3)

    def get_side_two(self):
        address = self.contract.caller.side2()
        return PredictionToken(address, self.web3)

    def mint_two_sides(self, from_address, amount):
        return self.contract.functions.mint(from_address, amount).transact({"from": from_address})

    def get_both_sides_balance(self, address):
        side_one_balance = self.side_one.balance(address)
        side_two_balance = self.side_two.balance(address)
        return {
            "side_one": side_one_balance,
            "side_two": side_two_balance
        }


