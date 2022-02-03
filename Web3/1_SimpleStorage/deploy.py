# Solidity Compiler wrapper
from solcx import compile_standard

import json

from web3 import Web3
import os
from dotenv import load_dotenv
load_dotenv()

# Load the contract source code
with open("../../Contracts/1_SimpleStorage/SimpleStorage.sol", "r") as file:
    source_code = file.read()


# Compiling the contract
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": source_code}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

# Save the compiled code in a file
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Get the bytecode from the file
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# Get the ABI from the file
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# Connecting to Ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
private_key = os.getenv("PRIVATE_KEY")


# Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get latest tx nonce
nonce = w3.eth.getTransactionCount(my_address)

# Build transaction
tx = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price, 
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)
# Sign transaction
signed_tx = w3.eth.account.signTransaction(tx, private_key)
# Send transaction
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
tx_recepit = w3.eth.waitForTransactionReceipt(tx_hash)

# Interacting with the contract
# Needed: Contract Address - Contract ABI
# It is possible to: Transact (Make a state change) - Call (Read and or get a value)
simple_storage = w3.eth.contract(address=tx_recepit.contractAddress, abi=abi)
print(simple_storage.functions.retrieve().call()) # Just a simple call

store_tx = simple_storage.functions.store(15).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": w3.eth.getTransactionCount(my_address),
    }
)
signed_store_tx = w3.eth.account.signTransaction(store_tx, private_key)
tx_hash = w3.eth.sendRawTransaction(signed_store_tx.rawTransaction)
tx_recepit = w3.eth.wait_for_transaction_receipt(tx_hash)

print(simple_storage.functions.retrieve().call()) # Checking if the new value is stored