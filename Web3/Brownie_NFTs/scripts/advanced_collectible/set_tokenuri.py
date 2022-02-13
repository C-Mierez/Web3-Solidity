from brownie import network, AdvancedCollectible
from scripts.advanced_collectible.create_metadata import STONK_MAPPING
from scripts.utils import get_account, OPENSEA_URL

import json


def main():
    print(f"Settings TokenURI on network {network.show_active()}.")

    advanced_collectible = AdvancedCollectible[-1]

    advanced_collectible_count = advanced_collectible.tokenCounter()
    print(f"Found {advanced_collectible_count} tokens.")
    for token_id in range(advanced_collectible_count):
        stonkType = STONK_MAPPING[advanced_collectible.tokenIdToStonkType(token_id)]

        # Check if the token already has a tokenURI set
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print(f"Setting TokenURI for token {token_id}.")

            with open(
                f"./meta/{network.show_active()}/{advanced_collectible}/{token_id}-{stonkType}-INFO.json"
            ) as f:
                tokenURI = json.load(f)["ipfs_uri"]

            set_tokenURI(
                token_id,
                advanced_collectible,
                tokenURI,
            )
        else:
            print(f"Token {token_id} already has a tokenURI set.")


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(
        token_id,
        tokenURI,
        {"from": account},
    )
    tx.wait(1)
    print(
        f"TokenURI set for Token {token_id}: {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
