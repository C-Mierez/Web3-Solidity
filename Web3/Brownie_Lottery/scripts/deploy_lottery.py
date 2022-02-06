from brownie import accounts, Lottery

from scripts.utils import get_account, get_contract


def deploy_lottery():
    account = get_account(id="cmdev")
    contract_l = Lottery.deploy(
        get_contract("eth_usd_price_feed"),
        {"from": account},
    )


def main():
    deploy_lottery()
