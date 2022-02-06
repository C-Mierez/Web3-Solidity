from brownie import accounts, Lottery, config, network

from scripts.utils import get_account, get_contract, fund_with_link


def deploy_lottery():
    account = get_account(id="cmdev")
    print("Deploying contracts...")
    contract = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed.")
    return contract


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    print("Starting lottery...")
    tx = lottery.startLottery({"from": account})
    tx.wait(1)
    print("Lottery started.")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]

    print("Entering lottery...")
    # Entrance Fee
    value = lottery.getEntranceFee() + (10**7)
    tx = lottery.bid({"from": account, "value": value})
    tx.wait(1)
    print("Entered lottery.")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]

    tx = fund_with_link(lottery.address, account)
    tx.wait(1)

    print("Ending lottery...")
    tx = lottery.endLottery({"from": account})
    tx = tx.wait(1)
    print("Ended lottery.")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
