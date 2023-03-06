from web3_deployed_contract import DeployedContract
from web3 import Web3
from eth_abi.packed import encode_abi_packed
from eth_abi import encode_abi
from constants import MIN_TICK, MAX_TICK, _tick_spacing
from web3_prediction_token import PredictionToken
from web3_univ3_position_manager import UniV3PositionManager
import math

class UniswapPool(DeployedContract):
    def __init__(self, address, web3):
        super().__init__(address, '../uniswap/v3-core/artifacts/contracts/UniswapV3Pool.sol/UniswapV3Pool.json', web3)

    @staticmethod
    def derive_pool_address(token_a, token_b, fee=3000):
        factory = '0x1F98431c8aD98523631AE4a59f267346ea31F984'
        POOL_INIT_CODE_HASH = '0xe34f199b19b2b4f47f68442619d555527d244f78a3297ea89325f843f87b8b54'
        token_0 = Web3.toChecksumAddress(token_a)
        token_1 = Web3.toChecksumAddress(token_b)
        abiEncoded_1 = encode_abi(['address', 'address', 'uint24'], (token_0, token_1, fee)) if int(token_0,16)<int(token_1, 16) else encode_abi(['address', 'address', 'uint24'], (token_1, token_0, fee))
        salt = Web3.solidityKeccak(['bytes'], ['0x' + abiEncoded_1.hex()])
        abiEncoded_2 = encode_abi_packed([ 'address', 'bytes32' ], (factory, salt))
        resPair = Web3.solidityKeccak(
            ['bytes', 'bytes'], ['0xff' + abiEncoded_2.hex(), POOL_INIT_CODE_HASH]
        )[12:]
        return resPair.hex()

    @staticmethod
    def get_min_tick(fee: int) -> int:
        min_tick_spacing: int = _tick_spacing[fee]
        return -(MIN_TICK // -min_tick_spacing) * min_tick_spacing

    @staticmethod
    def get_max_tick(fee: int) -> int:
        max_tick_spacing: int = _tick_spacing[fee]
        return (MAX_TICK // max_tick_spacing) * max_tick_spacing

    def default_tick_range(self, fee: int) -> tuple[int, int]:
        min_tick = self.get_min_tick(fee)
        max_tick = self.get_max_tick(fee)
        return min_tick, max_tick

    def nearest_tick(self, tick: int, fee: int) -> int:
        min_tick, max_tick = self.default_tick_range(fee)
        assert(
            min_tick <= tick <= max_tick
        ), f"Provided tick is out of bounds: {(min_tick, max_tick)}"

        tick_spacing = _tick_spacing[fee]
        rounded_tick_spacing = round(tick, tick_spacing) * tick_spacing

        if rounded_tick_spacing < min_tick:
            return rounded_tick_spacing + tick_spacing
        elif rounded_tick_spacing > max_tick:
            return rounded_tick_spacing - tick_spacing
        else:
            return rounded_tick_spacing

    @staticmethod
    def encode_sqrt_ratioX96(amount_0: int, amount_1: int) -> int:
        numerator = amount_1 << 192
        denominator = amount_0
        ratioX192 = numerator // denominator
        return int(math.sqrt(ratioX192))

    @classmethod
    def pool_factory_from_tokens(cls, token_a, token_b, web3, fee=3000):
        address = cls.derive_pool_address(token_a, token_b, fee)
        return cls(address, web3)

    def token_0(self):
        return self.contract.caller().token0()

    def token_1(self):
        return self.contract.caller().token1()

    def token_0_instance(self):
        return PredictionToken(self.token_0(), self.web3)

    def token_1_instance(self):
        return PredictionToken(self.token_1(), self.web3)

    def token_0_balance(self, address):
        return self.token_0_instance().balance(address)

    def token_1_balance(self, address):
        return self.token_1_instance().balance(address)

    def fee(self):
        return self.contract.caller().fee()

    def get_pool_state(
        self
    ):
        liquidity = self.contract.caller().liquidity()
        slot = self.contract.caller().slot0()
        pool_state = {
            "liquidity": liquidity,
            "sqrtPriceX96": slot[0],
            "tick": slot[1],
            "observationIndex": slot[2],
            "observationCardinality": slot[3],
            "observationCardinalityNext": slot[4],
            "feeProtocol": slot[5],
            "unlocked": slot[6],
        }
        return pool_state

    def token_0_price(self):
        sqrtPriceX96 = self.get_pool_state()['sqrtPriceX96']
        return (sqrtPriceX96**2) / 2**192

    def token_1_price(self):
        sqrtPriceX96 = self.get_pool_state()['sqrtPriceX96']
        return (2**192) / (sqrtPriceX96**2)

    def token_0_percent_price(self):
        price0 = self.token_0_price()
        price1 = self.token_1_price()
        return price0 / (price0+price1)

    def token_1_percent_price(self):
        price0 = self.token_0_price()
        price1 = self.token_1_price()
        return price1 / (price0+price1)


    def mint_liquidity(
        self,
        account: str,
        amount_0: int,
        amount_1: int,
        tick_lower: int,
        tick_upper: int,
        deadline: int = 2**64
    ):
        token_0 = self.token_0()
        token_1 = self.token_1()
        fee = self.fee()
        tick_lower = self.nearest_tick(tick_lower, fee)
        tick_upper = self.nearest_tick(tick_upper, fee)
        assert tick_lower < tick_upper, "invalid tick range"
        *_, isInit = self.contract.caller().slot0()
        if isInit is False:
            print("Executing init")
            sqrt_pricex96 = self.encode_sqrt_ratioX96(amount_0, amount_1)
            self.contract.functions.initialize(sqrt_pricex96).transact(
                {"from": account}
            )

        nft_manager = UniV3PositionManager(self.web3)
        self.token_0_instance().approve(account, nft_manager.contract.address, amount_0)
        self.token_1_instance().approve(account, nft_manager.contract.address, amount_1)
        return nft_manager.mint(
            token_0,
            token_1,
            fee,
            tick_lower,
            tick_upper,
            amount_0,
            amount_1,
            account,
            deadline
        )



