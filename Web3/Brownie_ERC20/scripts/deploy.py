from brownie import StonksToken
import time
from web3 import Web3

from scripts.utils import get_account


def deploy(initial_supply):
    account = get_account(id="cmdev")

    contract = StonksToken.deploy(initial_supply, {"from": account})
    time.sleep(1)
    print(contract.name())


def main():
    initial_supply = Web3.toWei(1000, "ether")
    deploy(initial_supply)
