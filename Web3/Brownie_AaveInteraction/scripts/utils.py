from brownie import (
    accounts,
    network,
    config,
)


LOCAL_BLOCKCHAIN_ENV = ["development", "ganache-local"]
FORKED_LOCAL_ENV = ["mainnet-fork-dev", "rinkeby-fork-dev", "kovan-fork-dev"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]

    if id and network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        return accounts.load(id)

    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENV
        or network.show_active() in FORKED_LOCAL_ENV
    ):
        # Use local accounts if in development env
        return accounts[0]

    # Default: Use the .env account
    return accounts.add(config["wallets"]["from_key"])
