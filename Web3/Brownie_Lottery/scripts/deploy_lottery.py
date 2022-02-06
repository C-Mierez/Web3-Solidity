from brownie import accounts, Lottery, config, network

from scripts.utils import get_account, get_contract


def deploy_lottery():
    account = get_account(id="cmdev")
    contract_l = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed.")


def main():
    deploy_lottery()
