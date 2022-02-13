from scripts.utils import (
    get_account,
    OPENSEA_URL,
)
from brownie import AdvancedCollectible


def create_collectible():
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]

    tx = advanced_collectible.createCollectible(
        {"from": account},
    )
    tx.wait(1)

    print(
        f"AdvancedCollectible created. OpenSea: {OPENSEA_URL.format(advanced_collectible.address, advanced_collectible.tokenCounter())}"
    )

    return tx


def main():
    return create_collectible()
