from brownie import network
from scripts.utils import LOCAL_BLOCKCHAIN_ENV, get_account, fund_with_link
from scripts.deploy_lottery import deploy_lottery
import pytest

# Here we need to test the actual integration of the Lottery contract with an external contract (Chainlink VRF)
def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()

    contract_lottery = deploy_lottery()
    account = get_account(id="cmdev")

    contract_lottery.startLottery({"from": account})

    # Enter two times
    contract_lottery.bid({"from": account, "value": contract_lottery.getEntranceFee()})
    contract_lottery.bid({"from": account, "value": contract_lottery.getEntranceFee()})

    # Fund with link
    fund_with_link(contract_address=contract_lottery.address, account=account)

    contract_lottery.endLottery({"from": account})

    # Assert
    assert contract_lottery.recentWinner() == account
    assert contract_lottery.balance() == 0
