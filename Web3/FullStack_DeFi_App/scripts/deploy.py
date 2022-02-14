from brownie import RewardToken, TokenFarm
from scripts.utils import get_account, get_verify


def deploy_stonk_token():
    account = get_account()

    reward_token = RewardToken.deploy(
        "Stonk Token",
        "STONK",
        {"from": account},
        publish_source=get_verify(),
    )

    print(f"Stonk Token deployed at {reward_token.address}")
    return reward_token


def deploy_farm():
    account = get_account()

    token_farm = TokenFarm.deploy(
        RewardToken[-1].address,
        {"from": account},
        publish_source=get_verify(),
    )
    print(f"Token Farm deployed at {token_farm.address}")
    return token_farm


def main():
    deploy_stonk_token()
    deploy_farm()
