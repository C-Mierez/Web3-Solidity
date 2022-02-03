from tracemalloc import start
from brownie import SimpleStorage, accounts

#? Brownie uses PYTEST
    
def test_deploy():
    # Using Ganache local account
    account = accounts[0]
    
    contract_ss = SimpleStorage.deploy({"from": account})
    starting_value = contract_ss.retrieve()
    
    # Expecting the initial value to be 0
    expected = 0
    assert(starting_value == expected)
    
def test_updating_storage():
    # Using Ganache local account
    account = accounts[0]
    
    contract_ss = SimpleStorage.deploy({"from": account})
    
    # Looking to store the value 15
    to_store = 15
    contract_ss.store(to_store, {"from": account})
    retrieved = contract_ss.retrieve()
    
    # Expecting the stored value to be the [to_store] value
    assert(to_store == retrieved)
    
    