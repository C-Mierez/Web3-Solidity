from brownie import TokenFarm, RewardToken
from scripts.utils import get_account, get_contract


def add_allowed_tokens():
    account = get_account()
    token_farm = TokenFarm[-1]

    print("Fetching allowed tokens contracts...")
    fau_token = get_contract("fau", "tokens")
    weth_token = get_contract("weth", "tokens")
    link_token = get_contract("link", "tokens")
    stonk_token = RewardToken[-1]

    print("Fetching allowed tokens price feed contracts...")
    tokens_to_price_feed = {
        fau_token: get_contract("dai_usd", "price_feeds"),
        weth_token: get_contract("eth_usd", "price_feeds"),
        link_token: get_contract("link_usd", "price_feeds"),
        stonk_token: get_contract("stonk_usd", "price_feeds"),
    }

    for token in tokens_to_price_feed:
        print(f"Adding {token._name} to TokenFarm allowed list...")
        token_farm.addAllowedToken(
            token.address,
            tokens_to_price_feed[token],
            {"from": account},
        ).wait(1)


def main():
    add_allowed_tokens()
