from scripts.utils import get_account

from brownie import interface, config, network, accounts
from web3 import Web3


def unwrap_eth():
    """
    Withdraw ETH by depositing wETH
    """

    account = get_account()

    # Need to get the ABI and the Address of the contract
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])

    # Deposit
    amount = 0.1
    tx = weth.withdraw(
        Web3.toWei(amount, "ether"),
        {
            "from": account,
        },
    )

    print(f"Transfered {amount} wETH. Current balance: {account.balance()} ETH.")

    tx.wait(1)

    return tx


def main():
    unwrap_eth()
