from brownie import Lottery, accounts, config, network
from web3 import Web3

ETH_PRICE = 3000
USD_FEE = 50


def test_get_entrance_fee():
    account = accounts[0]
    contract_l = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )
    entranceFee = contract_l.getEntranceFee()

    # Establishing an approximate range with a 0.01 eth margin of error
    assert entranceFee < Web3.toWei(USD_FEE / ETH_PRICE + 0.01, "ether")
    assert entranceFee > Web3.toWei(USD_FEE / ETH_PRICE - 0.01, "ether")
