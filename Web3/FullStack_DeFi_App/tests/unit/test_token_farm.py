from brownie import exceptions
from scripts.utils import (
    get_account,
    ENV_LOCAL,
    get_contract,
    network,
    DECIMALS,
    INITIAL_PRICE_FEED_VALUE,
)
from scripts.deploy import deploy_farm, deploy_stonk_token
from scripts.add_allowed_tokens import add_allowed_tokens
from web3 import Web3
import pytest

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


def _init():
    if network.show_active() not in ENV_LOCAL:
        pytest.skip("Only for Local testing.")
    return get_account(), deploy_stonk_token(), deploy_farm()


def test_farm_deployed_with_reward_token():
    account, reward_token, token_farm = _init()

    assert token_farm.rewardToken() == reward_token.address


def test_can_check_if_token_is_allowed():
    account, reward_token, token_farm = _init()

    assert type(token_farm.isAllowedToken(reward_token.address)) == bool


def test_can_set_new_allowed_token_and_price_feed():
    account, reward_token, token_farm = _init()

    to_allow_token = reward_token
    to_allow_token_price_feed = get_contract("stonk_usd", "price_feeds")

    token_farm.addAllowedToken(
        to_allow_token,
        to_allow_token_price_feed,
        {"from": account},
    )

    assert token_farm.isAllowedToken(to_allow_token.address)
    assert (
        token_farm.tokenToPriceFeed(to_allow_token.address)
        == to_allow_token_price_feed.address
    )


def test_cant_set_new_allowed_token_if_not_owner():
    account, reward_token, token_farm = _init()

    not_owner_account = get_account(index=1)
    to_allow_token = reward_token
    to_allow_token_price_feed = get_contract("stonk_usd", "price_feeds")

    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.addAllowedToken(
            to_allow_token,
            to_allow_token_price_feed,
            {"from": not_owner_account},
        )

    assert not token_farm.isAllowedToken(to_allow_token.address)
    assert token_farm.tokenToPriceFeed(to_allow_token.address) == ZERO_ADDRESS


def test_stake_tokens(to_stake_amount):
    account, reward_token, token_farm = _init()
    add_allowed_tokens()

    minter_account = get_account(index=1)
    staker_account = account
    to_stake_token = reward_token

    # Fund staker account
    reward_token.addMinter(minter_account, {"from": account})
    reward_token.mint(staker_account, to_stake_amount, {"from": minter_account})

    to_stake_token.approve(
        token_farm.address,
        to_stake_amount,
        {"from": staker_account},
    )

    token_farm.stakeTokens(
        to_stake_amount,
        to_stake_token.address,
        {"from": staker_account},
    )

    assert (
        token_farm.stakedBalance(staker_account.address, to_stake_token.address)
        == to_stake_amount
    )

    assert token_farm.uniqueStakedCount(staker_account.address) == 1

    assert token_farm.stakers(0) == staker_account.address
    return account, reward_token, token_farm


def test_mint_rewards(to_stake_amount):
    account, reward_token, token_farm = test_stake_tokens(to_stake_amount)

    initial_balance = reward_token.balanceOf(account.address)
    initial_supply = reward_token.totalSupply()

    reward_token.addMinter(
        token_farm.address,
        {"from": account},
    ).wait(1)

    token_farm.mintRewards(
        {"from": account},
    ).wait(1)

    assert reward_token.totalSupply() == initial_supply + Web3.toWei(
        INITIAL_PRICE_FEED_VALUE,
        "ether",
    )
    # [to_stake_amount] == 1, so 1 ETH is staked
    # 1 ETH == 3000 USD [INITIAL_PRICE]
    # Expecting to mint 3000 Stonks
    assert reward_token.balanceOf(account.address) == initial_balance + Web3.toWei(
        INITIAL_PRICE_FEED_VALUE,
        "ether",
    )
