from brownie import FundMe

from scripts.utils import get_account
from web3 import Web3


def fund():
    contract_fm = FundMe[-1]
    account = get_account()

    # Contract interaction
    entrance_fee = contract_fm.getEntranceFee() + 100
    print(
        f"Funding with {Web3.fromWei(entrance_fee, 'ether')} fee... from {account.address}"
    )
    print(f"Account Balance: {account.balance()}")
    print(f"Contract Balance: {contract_fm.balance()}")
    tx = contract_fm.fund(
        {
            "from": account,
            "value": entrance_fee,
        }
    )
    tx.wait(1)
    print("Funded.")
    print(f"Account Balance: {account.balance()}")
    print(f"Contract Balance: {contract_fm.balance()}")


def withdraw():
    contract_fm = FundMe[-1]
    account = get_account()

    print("Withdrawing...")
    tx = contract_fm.withdraw({"from": account})
    tx.wait(1)
    print(f"Account Balance: {account.balance()}")
    print(f"Contract Balance: {contract_fm.balance()}")
    print("Withdrawn.")


def main():
    fund()
    withdraw()
