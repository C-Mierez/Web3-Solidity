from web3 import Web3

import os

import json

from dotenv import load_dotenv


load_dotenv()

# Load contract json
with open("./abi.json", "r") as file:
    fundme_json = json.load(file)

# Get abi
abi = fundme_json


# Connecting to chain
w3 = Web3(Web3.HTTPProvider(os.getenv("ALCHEMY_URL")))
chain_id = 42
my_address = os.getenv("PUBLIC_KEY")
private_key = os.getenv("PRIVATE_KEY")
contract_address = "0x20e0C0026C54cF9d29A8A7E5A0606E2417c45F12"

# Creating the contract
contract = w3.eth.contract(address=contract_address, abi=abi)

# Testing
print(contract.functions.getPrice().call())

print(f"Account balance: {w3.fromWei(w3.eth.get_balance(my_address), 'ether')} ETH.")
print(
    f"Contract balance: {w3.fromWei(w3.eth.get_balance(contract_address), 'ether')} ETH."
)

# Getting back the funds
tx = contract.functions.withdraw().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": w3.eth.getTransactionCount(my_address),
    }
)

stx = w3.eth.account.sign_transaction(tx, private_key)

tx_hash = w3.eth.send_raw_transaction(stx.rawTransaction)
w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Account balance: {w3.fromWei(w3.eth.get_balance(my_address), 'ether')} ETH.")
print(
    f"Contract balance: {w3.fromWei(w3.eth.get_balance(contract_address), 'ether')} ETH."
)
