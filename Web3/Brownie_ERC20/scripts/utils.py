from brownie import (
    accounts,
    network,
    config,
)


LOCAL_BLOCKCHAIN_ENV = ["development", "ganache-local"]
FORKED_LOCAL_ENV = ["mainnet-fork", "mainnet-fork-dev", "rinkeby-fork-dev"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]

    if id and network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        return accounts.load(id)

    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENV
        or network.show_active() in FORKED_LOCAL_ENV
    ):
        # Use local accounts if in development env
        return accounts[0]

    # Default: Use the .env account
    return accounts.add(config["wallets"]["from_key"])


# contract_to_mock = {
#     "eth_usd_price_feed": MockV3Aggregator,
#     "vrf_coordinator": VRFCoordinatorMock,
#     "link_token": LinkToken,
# }


# def get_contract(contract_name):
#     """
#     Grab the contract addresses from the brownie-config.yaml file if defined
#     Otherwise, deploy a mock version of the contract and return it.

#         Args:
#             contract_name (string)

#         Returns:
#             brownie.network.contract.ProjectContract: The most recently deployed version of this contract.
#     """
#     # Map the contract to its corresponding Mock type
#     contract_type = contract_to_mock[contract_name]

#     # Check the network
#     if network.show_active() in LOCAL_BLOCKCHAIN_ENV:
#         if len(contract_type) <= 0:
#             _deploy_mocks()
#         contract = contract_type[-1]
#     else:
#         contract_address = config["networks"][network.show_active()][contract_name]

#         # Using Contract class to interact with contracts that already exist and are deployed but are NOT in the project
#         # Docs https://eth-brownie.readthedocs.io/en/stable/api-network.html?highlight=from_abi#brownie.network.contract.Contract
#         # This is returning a mock contract based on the already existing contract abi
#         contract = Contract.from_abi(
#             contract_type._name,
#             contract_address,
#             contract_type.abi,
#         )
#     return contract


# DECIMALS = 8
# INITIAL_VALUE = 200000000000


# def _deploy_mocks():
#     account = get_account()
#     MockV3Aggregator.deploy(
#         DECIMALS,
#         INITIAL_VALUE,
#         {"from": account},
#     )
#     link_token = LinkToken.deploy({"from": account})
#     VRFCoordinatorMock.deploy(
#         link_token.address,
#         {"from": account},
#     )
#     print("Deployed Mocks.")


# def fund_with_link(
#     contract_address,
#     account=None,
#     link_token=None,
#     amount=100000000000000000,  # 0.1 LINK
# ):
#     account = account if account else get_account()
#     link_token = link_token if link_token else get_contract("link_token")

#     print(f"Funding contract {contract_address} with LINK...")
#     # One straight forward way of doing the funding
#     # Possible since we have access to the entire LinkToken definition
#     tx = link_token.transfer(contract_address, amount, {"from": account})

#     # When we only have access to the Interface:
#     # link_token_contract = interface.LinkTokenInterface(link_token.address)
#     # tx = link_token_contract.transfer(contract_address, amount, {"from": account})
#     tx.wait(1)
#     print("Funded contract with LINK.")
#     return tx
