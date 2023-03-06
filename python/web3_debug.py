from web3 import Web3
from web3_sim import ether, wei
from web3_prediction import Prediction
from web3_mock_usdc import MockUsdc
from web3_simulated_lp import SimulatedLP
from web3_uniswap_factory import UniswapFactory
from web3_uniswap_pool import UniswapPool
from web3_univ3_quoter import UniV3Quoter
import numpy as np
import matplotlib.pyplot as plt
from constants import PREDICTION_ADDRESS, USDC_ADDRESS

def main():
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    prediction = Prediction(PREDICTION_ADDRESS, w3)

    print(prediction.side_one.contract.address)
    print(prediction.side_two.contract.address)

    usd = MockUsdc(USDC_ADDRESS, w3)
    account_19 = w3.eth.accounts[19]
    usd.mint(account_19, ether(1000))
    usd.approve(account_19, prediction.contract.address, ether(1000))
    #account_one = w3.eth.accounts[1]
    #print(usd.mint(account_one, ether(10)))
    #print(usd.approve(account_one, prediction.contract.address, ether(2)))
    #print(prediction.mint_two_sides(account_one, ether(2)))

    #print(wei(prediction.side_one.balance(account_one)))
    #print(wei(prediction.side_two.balance(account_one)))

    #lp1 = SimulatedLP(w3.eth.accounts[2], usd, ether(100))
    #print(wei(lp1.usd_balance()))
    #lp1.get_two_sided_tokens(prediction, ether(10))
    #inventory = lp1.get_inventory(prediction)
    #print(wei(inventory["side_one"]))
    #print(wei(inventory["side_two"]))

    # ================SIM LP TWO SIDED BALANCES ==================
    simulated_balances = simulated_lp_hoarde()
    for index, bal in enumerate(simulated_balances):
        if index%20 == 0:
            print("working on: ", index)
        lp = SimulatedLP(w3.eth.accounts[index], usd, ether(bal))
        #print("usdc Fetched balance: ", wei(lp.usd_balance()))
        lp.get_two_sided_tokens(prediction, ether(bal))
        #print("bal: ", bal)
        #print("bal in wei: ", ether(bal))
        #print("inventory side 1: ", wei(lp.get_inventory(prediction)["side_one"]))
    # ==============================================================

    print(wei(prediction.side_one.contract.caller().totalSupply()))
    print(wei(prediction.side_two.contract.caller().totalSupply()))

    uniV3 = UniswapFactory(w3)
    #pool_address = uniV3.create_pool(prediction.side_one, prediction.side_two, w3.eth.accounts[0])
    #pool_address = uniV3.pool_address(prediction.side_one, prediction.side_two, w3.eth.accounts[0])
    pool_address = UniswapPool.derive_pool_address(
        prediction.side_one.contract.address,
        prediction.side_two.contract.address
    )
    print(pool_address)
    pool = UniswapPool.pool_factory_from_tokens(
        prediction.side_one.contract.address,
        prediction.side_two.contract.address,
        w3
    )
    print("Existing Liquidity: ", pool.contract.caller().liquidity())
    user_one = w3.eth.accounts[1]
    print(pool.token_0())
    print(pool.token_1())
    bal_0 = pool.token_0_balance(user_one)
    bal_1 = pool.token_1_balance(user_one)
    print(wei(bal_0))
    print(wei(bal_1))
    quoter = UniV3Quoter(w3)
    # print(
    #     quoter.get_token_token_price(pool.token_0(), pool.token_1(), 3000, ether(1), 0)
    # )
    # pool.mint_liquidity(
    #     user_one,
    #     bal_0,
    #     bal_1,
    #     0,
    #     1
    # )
    # sim_lp(w3.eth.accounts[2], pool)
    for x in range(3, 20):
        sim_lp(w3.eth.accounts[x], pool)
    price0 = pool.token_0_price() #(pool_info['sqrtPriceX96']**2) / 2**192
    price1 = pool.token_1_price() #(2**192) / (pool_info['sqrtPriceX96']**2)
    print(price0)
    print(price1)
    print(pool.token_0_percent_price())
    print(pool.token_1_percent_price())

    pool_info = pool.get_pool_state()
    print("Pool Info: ", wei(pool_info['liquidity']))

def sim_lp(account, pool):
    bal_0 = pool.token_0_balance(account)
    bal_1 = pool.token_1_balance(account)
    pool.mint_liquidity(
        account,
        bal_0,
        bal_1,
        0,
        1
    )

# def tick_from_price_0(price_0):


def simulated_lp_hoarde():
    a, m = 2., 100.
    s = (np.random.pareto(a, 20) + 1) * m
    print(s)
    count = 0
    for x in s:
        count = count + x
    print("Aggregate: ", str(count))
    count, bins, _ = plt.hist(s, 1000, density=True)
    fit = a*m**a / bins**(a+1)
    plt.plot(bins, max(count)*fit/max(fit), linewidth=2, color='r')
    plt.savefig("./graph.png")
    return s

def sim_univ3():
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    uniV3 = UniswapFactory(w3)
    print(uniV3.contract.caller().owner())


#sim_univ3()
#simulated_lp_hoarde()
main()
