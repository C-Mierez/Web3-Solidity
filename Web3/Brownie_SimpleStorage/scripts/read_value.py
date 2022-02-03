from brownie import SimpleStorage, accounts, config

def read_contract():
    # Grab the most recent deployment
    contract_addr = SimpleStorage[-1]
    
    # Brownie already has the ABI and the Address stored
    value = contract_addr.retrieve()
    print(f"Value: {value}")

def main():
    read_contract()

