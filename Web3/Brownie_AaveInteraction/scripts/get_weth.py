from scripts.utils import get_account

from brownie import interface, config, network, accounts
from web3 import Web3


def get_weth():
    """
    Mint wETH by depositing ETH
    """

    account = get_account()

    # Need to get the ABI and the Address of the contract
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])

    # Deposit
    print("Getting wETH...")
    amount = 0.1
    tx = weth.deposit(
        {
            "from": account,
            "value": Web3.toWei(amount, "ether"),
        }
    )

    print(f"Deposited {amount} ETH. Current balance: {account.balance()} ETH.")

    tx.wait(1)

    return tx


def main():
    get_weth()
