from brownie import FundMe

from scripts.utils import get_account


def fund():
    contract_fm = FundMe[-1]
    account = get_account()

    # Contract interaction
    entrance_fee = contract_fm.getEntranceFee()
    print(f"Funding with {entrance_fee} fee...")
    contract_fm.fund(
        {
            "from": account,
            "value": entrance_fee,
        }
    )
    print("Funded.")


def withdraw():
    contract_fm = FundMe[-1]
    account = get_account()

    print("Withdrawing...")
    contract_fm.withdraw({"from": account})
    print("Withdrawn.")


def main():
    fund()
    withdraw()
