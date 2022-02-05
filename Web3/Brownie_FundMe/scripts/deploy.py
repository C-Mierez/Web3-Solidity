from brownie import FundMe, network, config, MockV3Aggregator

from scripts.utils import get_account, deploy_mock_priceFeed, LOCAL_BLOCKCHAIN_ENV

from web3 import Web3


def deploy_fund_me():
    account = get_account()
    # After the changes in the contract's constructor, it now needs an
    # additional parameter (Rinkeby Chainlink contract address)
    # This allows dynamically changing the used address depending on the env (Test, Local, Live,...)
    active_network = network.show_active()
    if active_network not in LOCAL_BLOCKCHAIN_ENV:
        priceFeed_address = config["networks"][active_network]["eth_usd_priceFeed"]
    else:
        # If in development, deploy a mock
        print(
            f"Active network: {active_network}.\nDeploying mock priceFeed contract..."
        )
        # Check whether the mock contract has already been deployed
        deploy_mock_priceFeed()
        priceFeed_address = MockV3Aggregator[-1].address

    contract_fm = FundMe.deploy(
        priceFeed_address,
        {"from": account},
        publish_source=config["networks"][active_network]["verify"],
    )
    print(f"Contract deployed to: {contract_fm.address}")


def main():
    deploy_fund_me()
