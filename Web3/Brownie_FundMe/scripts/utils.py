from brownie import accounts, network, config, MockV3Aggregator

from web3 import Web3

# priceFeed Mock Parameters
DECIMALS = 18
STARTING_PRICE = 2000

# Environment definitions
LOCAL_BLOCKCHAIN_ENV = ["development", "ganache-local"]


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENV:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mock_priceFeed():
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(
            DECIMALS,
            Web3.toWei(STARTING_PRICE, "ether"),
            {"from": get_account()},
        )
        print("Mock priceFeed contract deployed.")
    else:
        print("Mock priceFeed contract already deployed.")
