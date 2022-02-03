# Easier way to work with accounts
import re
from brownie import accounts, config, SimpleStorage

import os

def deploy_simple_storage():
    # Grab the first account from the generated accounts (Ganache)
    # Only works with local networks
    localAccount = accounts[0]
    
    # In order to work with an actual account for an actual network
    # We can add the address to the Brownie accounts list from the cmd line
    # Then it can be accessed like this:
    realAccount = accounts.load("cmdev")
    
    # Or just like with the non-brownie way
    # Environemnt variables in the .env file can be used
    envAccount = accounts.add(os.getenv("PRIVATE_KEY"))
    
    # An even better option is to set and fetch the account from the .yaml config file
    configAccount = accounts.add(config["wallets"]["from_key"])
    
    #? I leave all the above in the code for demonstration purposes
    #? [account] is the one that's going to be used throughout this project
    account = localAccount
    
    # Deploying the contract
    contract_sp = SimpleStorage.deploy({"from": account})

    #! Simulating the original Web3 SimpleStorage script but with Brownie:
    # Call retrieve()
    stored_value = contract_sp.retrieve()
    print(f"Stored value: {stored_value}.")
    
    # Store a new value
    tx = contract_sp.store(15, {"from": account})
    # Wait for 1 block
    tx.wait(1)
    
    # Updated retrieve() value
    stored_value = contract_sp.retrieve()
    print(f"Updated stored value: {stored_value}.")

def main():
    deploy_simple_storage()