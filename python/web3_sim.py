from web3 import Web3
import json

def get_abi(file_name):
    with open(file_name) as file:
        file_contents = file.read()

    json_data = json.loads(file_contents)
    return json_data["abi"]

def connectProvider(endpoint):
    w3 = Web3(Web3.HTTPProvider(endpoint))
    if w3.isConnected():
        return w3
    else:
        raise ValueError('Web3 Not Connected')

def wei(amount_wei):
    return Web3.fromWei(amount_wei, "ether")

def ether(amount_eth):
    return Web3.toWei(amount_eth, "ether")

def connectContract(w3, address, abi):
    contract = w3.eth.contract(address=address, abi=abi)
    return contract


