from brownie import accounts, exceptions
from scripts.utils import get_account, ENV_LOCAL, network
from scripts.deploy import deploy_stonk_token
from web3 import Web3
import pytest


def _init():
    if network.show_active() not in ENV_LOCAL:
        pytest.skip("Only for Local testing.")
    return get_account(), deploy_stonk_token()


def test_deploy_with_no_supply():
    _, reward_token = _init()

    assert reward_token.totalSupply() == 0


def test_cant_give_minter_role_if_not_admin():
    account, reward_token = _init()

    with pytest.raises(exceptions.VirtualMachineError):
        reward_token.addMinter(accounts[2], {"from": accounts[1]})

    assert not reward_token.hasRole(reward_token.MINTER_ROLE(), accounts[2])


def test_can_give_minter_role_if_admin():
    account, reward_token = _init()

    reward_token.addMinter(accounts[1], {"from": account})

    assert reward_token.hasRole(reward_token.MINTER_ROLE(), accounts[1])


def test_cant_mint_if_not_minter():
    account, reward_token = _init()

    initial_supply = reward_token.totalSupply()
    to_address = account.address

    with pytest.raises(exceptions.VirtualMachineError):
        reward_token.mint(
            to_address,
            Web3.toWei(1000, "ether"),
            {"from": account},
        ).wait(1)

    current_supply = reward_token.totalSupply()

    assert initial_supply == 0
    assert reward_token.balanceOf(to_address) == 0
    assert current_supply == 0


def test_can_mint_if_minter():
    account, reward_token = _init()

    initial_supply = reward_token.totalSupply()
    minter_address = accounts[1]
    to_address = accounts[2]
    amount_to_mint = 1000

    reward_token.addMinter(minter_address, {"from": account})

    reward_token.mint(
        to_address,
        Web3.toWei(amount_to_mint, "ether"),
        {"from": minter_address},
    ).wait(1)

    current_supply = reward_token.totalSupply()

    assert initial_supply == 0
    assert reward_token.balanceOf(to_address) == Web3.toWei(amount_to_mint, "ether")
    assert current_supply == initial_supply + Web3.toWei(amount_to_mint, "ether")
