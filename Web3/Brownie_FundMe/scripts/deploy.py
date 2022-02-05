from brownie import FundMe

from scripts.utils import get_account

def deploy_fund_me():
    account = get_account()
    contract_fm = FundMe.deploy({"from": account}, publish_source=True)
    print(f"Contract deployed to: {contract_fm.address}")

def main():
    deploy_fund_me()