from brownie import accounts, network, config, MockV3Aggregator


# priceFeed Mock Parameters
DECIMALS = 8
STARTING_PRICE = 200000000000

# Environment definitions
LOCAL_BLOCKCHAIN_ENV = ["development", "ganache-local"]
FORKED_BLOCKCHAIN_ENV = ["mainnet-fork", "mainnet-fork-dev"]


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENV
        or network.show_active() in FORKED_BLOCKCHAIN_ENV
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mock_priceFeed():
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(
            DECIMALS,
            STARTING_PRICE,
            {"from": get_account()},
        )
        print("Mock priceFeed contract deployed.")
    else:
        print("Mock priceFeed contract already deployed.")
