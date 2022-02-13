from brownie import accounts, network, config, Contract, LinkToken, VRFCoordinatorMock
from web3 import Web3

# Global definition for Local Blockchain dev environment names
ENV_LOCAL = ["development", "ganache-local"]

# Global definition for Forked Blockchain dev environment names
ENV_FORK = ["mainnet-fork", "rinkeby-fork", "kovan-fork"]

# OpenSea URL for collectibles
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"


def get_account(index=None, id=None):
    """Get the the most suitable account to be used in the current dev environment.
    Can return a specific account if parameters are provided.

    Args:
        index (integer, optional): Index of the local account associated to the current network, created by Brownie. Defaults to None.
        id (string, optional): Account ID defined by Brownie's built-in account manager. Defaults to None.

    Returns:
        Account: Most suitable account to be used in the current dev environment.
    """
    if index:
        return accounts[index]

    if id and network.show_active() not in ENV_LOCAL:
        return accounts.load(id)

    if network.show_active() in ENV_LOCAL or network.show_active() in ENV_FORK:
        # Use local accounts if in development env
        return accounts[0]

    # Default: Use the .env account
    return accounts.add(config["wallets"]["from_key"])


def get_config(config_name, config_subtype=None, config_network=None):
    """
    Grab a value from the brownie-config.yaml file if defined.
    If working on a local environment, the value is taken from the specified default network config instead.

        Args:
            config_name (string): Name of the config.
            config_subtype (string, optional): Defined subtype in the brownie-config.yaml file. Defaults to None.
            config_network (string, optional): Override network search and use config_network isntead. Defaults to None.
    """
    ntwork = network.show_active()
    if config_network is not None:
        ntwork = config_network
    elif ntwork in ENV_LOCAL:
        ntwork = config["networks"]["development"]["default_config_network"]
    cnfig = config["networks"][ntwork]["config"]
    return cnfig[config_subtype][config_name] if config_subtype else cnfig[config_name]


def get_contract(contract_name, contract_subtype=None):
    """
    Grab the contract addresses from the brownie-config.yaml file if defined.
    Otherwise, deploy Mocks of the contracts used (if not already deployed) and return it.

        Args:
            contract_name (string): Name of the contract.
            contract_subtype (string, optional): Defined subtype in the brownie-config.yaml file. Defaults to None.

        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed version of the contract.
    """
    # Mapping of contract names to their corresponding Mock type
    contract_to_mock = {
        "link": LinkToken,
        "vrf_coordinator": VRFCoordinatorMock,
    }
    # Map the contract to its Mock type
    contract_type = contract_to_mock[contract_name]

    # Choose the contract depending on the current environment
    if network.show_active() in ENV_LOCAL:
        # Check if the needed Mock has already been deployed, otherwise deploy it
        if len(contract_type) <= 0:
            _deploy_mocks()
        # Grab the latest deployed contract
        contract = contract_type[-1]
    else:
        # Grab the contract address from the config file
        cnfig = config["networks"][network.show_active()]["contracts"]
        contract_address = (
            cnfig[contract_subtype][contract_name]
            if contract_subtype
            else cnfig[contract_name]
        )

        # Using Contract class to interact with contracts that already exist and are deployed but are NOT in the project
        # Docs https://eth-brownie.readthedocs.io/en/stable/api-network.html?highlight=from_abi#brownie.network.contract.Contract
        # This is returning a contract based on the already existing contract abi (used for the mocks)
        # This could be implemented in other ways, for example using Interface instead
        contract = Contract.from_abi(
            contract_type._name,
            contract_address,
            contract_type.abi,
        )
    return contract


def _deploy_mocks():
    """Deploy all Mocks used in this project.
    Need to manually define which ones to be deployed, using their appropriate parameters, since they are
    pretty much project-specific.

    Mocks are meant to only be used on local blockchains, where the mocked contracts need to perform some kind of task.
    For example, Chainlink VRF.

    # Example
    # LinkToken.deploy({"from": account})
    # VRFCoordinatorMock.deploy(
    #     link_token.address,
    #     {"from": account},
    # )
    """
    print(f"Deploying Mocks for network {network.show_active()}...")
    account = get_account()

    print("Deploying LinkToken...")
    link_token = LinkToken.deploy({"from": account})
    print(f"Deployed LinkToken at {link_token.address}...")
    print("Deploying VRFCoordinatorMock...")
    vrf_coordinator = VRFCoordinatorMock.deploy(link_token, {"from": account})
    print(f"Deployed VRFCoordinatorMock at {vrf_coordinator.address}...")

    print("Deployed Mocks.")


def fund_with_erc20(
    to_fund_address, erc20_token_contract, ether_amount=None, account=None
):

    account = account if account else get_account()
    ether_amount = ether_amount if ether_amount else 0.1

    print(
        f"Funding {to_fund_address} with {ether_amount} {erc20_token_contract.symbol()}..."
    )
    tx = erc20_token_contract.transfer(
        to_fund_address,
        Web3.toWei(ether_amount, "ether"),
        {"from": account},
    )
    tx.wait(1)
    print(
        f"Funded {to_fund_address} with {ether_amount} {erc20_token_contract.symbol()}."
    )
    return tx
