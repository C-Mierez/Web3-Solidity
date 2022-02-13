from scripts.utils import (
    get_account,
    get_contract,
    fund_with_erc20,
)
from brownie import AdvancedCollectible


def fund_with_link():
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]

    print
    tx = fund_with_erc20(
        advanced_collectible.address,
        get_contract("link", "tokens"),
        account=account,
        ether_amount=0.2,
    )

    tx.wait(1)

    return tx


def main():
    return fund_with_link()
