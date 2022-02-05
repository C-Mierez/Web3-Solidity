import pytest
from scripts.utils import get_account, LOCAL_BLOCKCHAIN_ENV
from scripts.deploy import deploy_fund_me
from brownie import FundMe, network, accounts, exceptions


def test_can_fund_and_withdraw():
    account = get_account()
    contract_fm = deploy_fund_me()

    entrance_fee = contract_fm.getEntranceFee()
    tx = contract_fm.fund(
        {
            "from": account,
            "value": entrance_fee,
        }
    )
    tx.wait(1)

    amountFunded = contract_fm.addressToAmountFunded(account.address)
    assert amountFunded == entrance_fee

    tx2 = contract_fm.withdraw({"from": account})
    tx2.wait(1)

    amountFunded = contract_fm.addressToAmountFunded(account.address)
    assert amountFunded == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip("Only for local testing.")
    account = get_account()
    contract_fm = deploy_fund_me()

    # Take whatever account
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        contract_fm.withdraw({"from": bad_actor})
