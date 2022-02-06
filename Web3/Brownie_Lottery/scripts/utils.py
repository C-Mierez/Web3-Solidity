from brownie import (
    accounts,
    network,
    config,
    Contract,
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
)


LOCAL_BLOCKCHAIN_ENV = ["development", "ganache-local"]
FORKED_LOCAL_ENV = ["mainnet-fork", "mainnet-fork-dev"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]

    if id:
        return accounts.load(id)

    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENV
        or network.show_active() in FORKED_LOCAL_ENV
    ):
        # Use local accounts if in development env
        return accounts[0]

    # Default: Use the .env account
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": VRFCoordinatorMock,
}


def get_contract(contract_name):
    """
    Grab the contract addresses from the brownie-config.yaml file if defined
    Otherwise, deploy a mock version of the contract and return it.

        Args:
            contract_name (string)

        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed version of this contract.
    """
    # Map the contract to its corresponding Mock type
    contract_type = contract_to_mock[contract_name]

    # Check the network
    if network.show_active() in LOCAL_BLOCKCHAIN_ENV:
        if len(contract_type) <= 0:
            _deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]

        # Using Contract class to interact with contracts that already exist and are deployed but are NOT in the project
        # Docs https://eth-brownie.readthedocs.io/en/stable/api-network.html?highlight=from_abi#brownie.network.contract.Contract
        # This is returning a mock contract based on the already existing contract abi
        contract = Contract.from_abi(
            contract_type._name,
            contract_address,
            contract_type._abi,
        )
    return contract


DECIMALS = 8
INITIAL_VALUE = 200000000000


def _deploy_mocks():
    account = get_account()
    MockV3Aggregator.deploy(
        DECIMALS,
        INITIAL_VALUE,
        {"from": account},
    )
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(
        link_token.address,
        {"from": account},
    )
    print("Deployed mock Price Feed.")


# My own take on a cohesive and dynamic method
# Would likely need some kind of dynamic parameter storing
# And would need to adjust to the amount of parameters that particular contract's constructor takes
# mock_default_params = {
#     MockV3Aggregator: [DECIMALS,  INITIAL_VALUE]
# }
#
# def _deploy_mock(contract_type):
#     account = get_account()
#     contract_type.deploy(
#         # Dynamic parameter count here
#         DECIMALS,
#         INITIAL_VALUE,
#         {"from": account},
#     )
#     print("Deployed mock Price Feed.")
