from brownie import accounts, network, config, Contract

# Global definition for Local Blockchain dev environment names
ENV_LOCAL = ["development", "ganache-local"]

# Global definition for Forked Blockchain dev environment names
ENV_FORK = ["mainnet-fork", "rinkeby-fork", "kovan-fork"]


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
        # "vrf_coordinator": VRFCoordinatorMock,
    }

    # Choose the contract depending on the current environment
    if network.show_active() in ENV_LOCAL:
        # Map the contract to its Mock type
        contract_type = contract_to_mock[contract_name]
        # Check if the needed Mock has already been deployed, otherwise deploy it
        if len(contract_type) <= 0:
            _deploy_mocks()
        # Grab the latest deployed contract
        contract = contract_type[-1]
    else:
        # Grab the contract address from the config file
        config = config["networks"][network.show_active()]["contracts"]
        contract_address = (
            config[contract_subtype][contract_name]
            if contract_subtype
            else config[contract_name]
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

    pass
