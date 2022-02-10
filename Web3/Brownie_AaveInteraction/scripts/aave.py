from scripts.utils import get_account, FORKED_LOCAL_ENV
from scripts.get_weth import get_weth

from brownie import config, network, interface
from web3 import Web3

AMOUNT = Web3.toWei(0.1, "ether")


def aave_deposit():
    account = get_account()

    erc20_address = config["networks"][network.show_active()]["weth_token"]

    if network.show_active() in FORKED_LOCAL_ENV:
        get_weth()

    # Interacting with the LendingPool
    # Though the Address of this contrat can vary
    lending_pool = get_lending_pool_from_provider()

    # Approve sending ERC20 token
    approve_erc20(AMOUNT, lending_pool.address, erc20_address, account)

    # Deposit wETH
    print("Depositing wETH...")
    tx = lending_pool.deposit(
        erc20_address,
        AMOUNT,
        account.address,
        0,
        {"from": account},
    )
    tx.wait(1)
    print(f"Deposited {Web3.fromWei(AMOUNT, 'ether')} wETH.")


def aave_borrow():
    account = get_account()
    lending_pool = get_lending_pool_from_provider()

    # Check current account status
    borrowable_eth, total_debt = get_borrowable_data(lending_pool, account)

    # Borrow DAI in terms of ETH value
    price_feed_address = config["networks"][network.show_active()]["dai_eth_price_feed"]
    dai_eth_price = get_asset_price(price_feed_address)

    dai_to_borrow = (1 / dai_eth_price) * (
        borrowable_eth * 0.95
    )  # 95% to add more margin
    dai_to_borrow = round(dai_to_borrow, 1)
    print(f"Attempting to borrow {dai_to_borrow} DAI...")

    dai_address = config["networks"][network.show_active()]["dai_token"]
    tx = lending_pool.borrow(
        dai_address,
        Web3.toWei(dai_to_borrow, "ether"),
        1,
        0,
        account.address,
        {"from": account},
    )
    tx.wait(1)
    print(f"Borrowed {dai_to_borrow} DAI.")


def aave_repay():
    account = get_account()
    lending_pool = get_lending_pool_from_provider()
    dai_address = config["networks"][network.show_active()]["dai_token"]

    # Get prices
    price_feed_address = config["networks"][network.show_active()]["dai_eth_price_feed"]
    eth_dai_price = 1 / get_asset_price(price_feed_address)

    (
        borrowable_eth,
        debt,
    ) = get_borrowable_data(lending_pool, account)

    # Repaying with DAI
    # Approve the use of DAI
    dai_to_repay = debt * eth_dai_price - 0.1
    approve_erc20(
        Web3.toWei(dai_to_repay, "ether"),
        lending_pool,
        dai_address,
        account,
    )

    # Repay debt
    print(f"Attempting to repay {dai_to_repay} DAI...")
    tx = lending_pool.repay(
        dai_address,
        Web3.toWei(dai_to_repay, "ether"),
        1,
        account.address,
        {"from": account},
    )
    tx.wait(1)
    print(f"Repaid {dai_to_repay} DAI.")

    get_borrowable_data(lending_pool, account)


def get_asset_price(price_feed_address):
    # Interacting with the PriceFeed contract
    dai_eth_price_feed = interface.IAggregatorV3(price_feed_address)

    latest_price = dai_eth_price_feed.latestRoundData()[
        1
    ]  # Second value in the returned tuple
    dai_eth_price = Web3.fromWei(latest_price, "ether")
    print(f"DAI/ETH price: {dai_eth_price}.")
    return float(dai_eth_price)


def get_borrowable_data(lending_pool, account):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)

    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")

    print(f"Account Data:")
    print(f"Total collateral ETH: {total_collateral_eth}")
    print(f"Total debt ETH: {total_debt_eth}")
    print(f"Available borrow ETH: {available_borrow_eth}")

    return (float(available_borrow_eth), float(total_debt_eth))


def approve_erc20(amount, spender_address, erc20_address, account):
    print("Approving ERC20 token...")
    erc20 = interface.ERC20(erc20_address)
    tx = erc20.approve(
        spender_address,
        amount,
        {"from": account},
    )
    tx.wait(1)
    print("Approved ERC20 spending.")
    return tx


def get_lending_pool_from_provider():
    # Interacting with the LendingPoolAddressesProvider
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )

    lending_pool_address = lending_pool_addresses_provider.getLendingPool()

    # Setting the LendingPool contract
    lending_pool = interface.ILendingPool(lending_pool_address)

    return lending_pool


def main():
    aave_deposit()
    aave_borrow()
    aave_repay()
    print("\n")
    print("DEPOSITED, BORROWED AND REPAID!")
