class SimulatedLP:
    def __init__(self, account, usdc_contract, usdc_amount):
        self.address = account
        self.usdc = usdc_contract
        self.load_usdc(usdc_amount)

    def load_usdc(self, usdc_amount):
        self.usdc.mint(self.address, usdc_amount)

    def usd_balance(self):
        return self.usdc.balance(self.address)

    def get_two_sided_tokens(self, prediction, amount):
        self.usdc.approve(self.address, prediction.contract.address, amount)
        return prediction.mint_two_sides(self.address, amount)

    def get_inventory(self, prediction):
        return prediction.get_both_sides_balance(self.address)

