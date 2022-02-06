from brownie import network, exceptions
from web3 import Web3

from scripts.deploy_lottery import deploy_lottery
from scripts.utils import (
    LOCAL_BLOCKCHAIN_ENV,
    get_account,
    fund_with_link,
    get_contract,
)

import pytest

ETH_PRICE = 2000
USD_FEE = 50
RNG_NUMBER = 128


def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()

    contract_lottery = deploy_lottery()

    # Expecting
    exp_entrance_fee = Web3.toWei(USD_FEE / ETH_PRICE, "ether")
    # Act
    entrance_fee = contract_lottery.getEntranceFee()

    # Assert
    # Establishing an approximate range with a 0.01 eth margin of error
    assert entrance_fee == exp_entrance_fee
    # assert entranceFee < Web3.toWei(USD_FEE / ETH_PRICE + 0.01, "ether")
    # assert entranceFee > Web3.toWei(USD_FEE / ETH_PRICE - 0.01, "ether")


def test_cant_bid_unless_started():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()

    contract_lottery = deploy_lottery()

    # Shouldnt be able to bid
    with pytest.raises(exceptions.VirtualMachineError):
        contract_lottery.bid(
            {"from": get_account(), "value": contract_lottery.getEntranceFee()}
        )


def test_can_bid():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()

    contract_lottery = deploy_lottery()
    account = get_account()

    # Act
    contract_lottery.startLottery({"from": account})
    contract_lottery.bid(
        {
            "from": account,
            "value": contract_lottery.getEntranceFee(),
        }
    )

    # Assert
    assert contract_lottery.participants(0) == account


def test_can_end():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()

    contract_lottery = deploy_lottery()
    account = get_account()

    # Act
    contract_lottery.startLottery({"from": account})
    contract_lottery.bid(
        {
            "from": account,
            "value": contract_lottery.getEntranceFee(),
        }
    )
    tx = fund_with_link(contract_lottery.address, account)
    tx.wait(1)
    tx = contract_lottery.endLottery({"from": account})
    tx.wait(1)

    # Assert
    assert contract_lottery.lottery_state() == 2


def test_can_pick_winner():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()

    contract_lottery = deploy_lottery()
    account = get_account()

    contract_lottery.startLottery({"from": account})
    contract_lottery.bid(
        {
            "from": account,
            "value": contract_lottery.getEntranceFee(),
        }
    )
    for i in range(1, 4):
        contract_lottery.bid(
            {
                "from": get_account(index=i),
                "value": contract_lottery.getEntranceFee(),
            }
        )
    fund_with_link(contract_lottery.address, account)

    starting_account_balance = account.balance()
    lottery_balance = contract_lottery.balance()

    tx = contract_lottery.endLottery({"from": account})

    request_id = tx.events["RequestedRandomness"]["requestId"]
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id,
        RNG_NUMBER,
        contract_lottery.address,
        {"from": account},
    )

    # Assert
    # 128 % 4 = 1
    assert contract_lottery.recentWinner() == account
    assert contract_lottery.balance() == 0
    assert account.balance() == starting_account_balance + lottery_balance
