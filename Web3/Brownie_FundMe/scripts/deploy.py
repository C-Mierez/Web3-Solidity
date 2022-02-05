from brownie import FundMe, network, config, MockV3Aggregator

from scripts.utils import get_account


def deploy_fund_me():
    account = get_account()
    # After the changes in the contract's constructor, it now needs an
    # additional parameter (Rinkeby Chainlink contract address)
    # This allows dynamically changing the used address depending on the env (Test, Local, Live,...)
    active_network = network.show_active()
    if active_network != "development":
        priceFeed_address = config["networks"][active_network]["eth_usd_priceFeed"]
    else:
        # If in development, deploy a mock
        print(
            f"Active network: {active_network}.\nDeploying mock priceFeed contract..."
        )
        contract_mock_V3Agg = MockV3Aggregator.deploy(
            18,
            2000000000000000000000,
            {"from": account},
        )
        priceFeed_address = contract_mock_V3Agg.address
        print("Mock priceFeed contract deployed.")

    contract_fm = FundMe.deploy(
        priceFeed_address,
        {"from": account},
        publish_source=config["networks"][active_network]["verify"],
    )
    print(f"Contract deployed to: {contract_fm.address}")


def main():
    deploy_fund_me()
