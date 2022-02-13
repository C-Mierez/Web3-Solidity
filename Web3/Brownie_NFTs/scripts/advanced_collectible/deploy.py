from scripts.utils import (
    get_account,
    get_contract,
    get_config,
)
from brownie import AdvancedCollectible, config, network
from web3 import Web3


def deploy():
    account = get_account()

    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator", "vrf"),
        get_contract("link", "tokens"),
        get_config("keyhash", "vrf"),
        Web3.toWei(get_config("fee", "vrf"), "ether"),
        "Stonks",
        "STONK",
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )

    print(f"Deployed AdvancedCollectible at {advanced_collectible.address}.")
    return advanced_collectible


def main():
    return deploy()
