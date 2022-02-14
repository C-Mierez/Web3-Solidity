from brownie import (
    accounts,
    network,
    config,
    Contract
)

from web3 import Web3

import eth_utils

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

    if (
        network.show_active() in ENV_LOCAL
        or network.show_active() in ENV_FORK
    ):
        # Use local accounts if in development env
        return accounts[0]

    # Default: Use the .env account
    return accounts.add(config["wallets"]["from_key"])

def get_config(config_name, config_group=None, config_network=None):
    """
    Grab a value from the brownie-config.yaml file if defined.
    If working on a local environment, the value is taken from the specified default network config instead.

        Args:
            config_name (string): Name of the config.
            config_group (string, optional): Defined group in the brownie-config.yaml file. Defaults to None.
            config_network (string, optional): Override network search and use config_network instead. Defaults to None.
    """
    ntwork = network.show_active()
    
    
    if config_network is not None:
        # Use the network sent as parameter
        ntwork = config_network            
    elif ntwork in ENV_LOCAL:
        # Use the settings defined from a live network. This network is defined in the brownie-config.yaml file.
        ntwork = config["networks"]["development"]["default_config_network"]
    
    # Get the desired settings from the config group
    cnfig = config["networks"][ntwork]["config"]
    return cnfig[config_group][config_name] if config_group else cnfig[config_name]

def get_contract(contract_name, contract_group=None):
    """
    Grab the contract addresses from the brownie-config.yaml file if defined.
    Otherwise, deploy Mocks of the contracts used (if not already deployed) and return it.

        Args:
            contract_name (string): Name of the contract.
            contract_group (string, optional): Defined group in the brownie-config.yaml file. Defaults to None. 

        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed version of the contract.
    """
    # Mapping of contract names to their corresponding Mock type 
    contract_to_mock = {
        # "vrf_coordinator": VRFCoordinatorMock,
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
        config = config["networks"][network.show_active()]["contracts"]
        contract_address = config[contract_group][contract_name] if contract_group else config[contract_name]
        
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

def fund_with_erc20(
    to_fund_address, erc20_token_contract, ether_amount=0.1, account=None
):
    """Send a specified amount of an ERC20 token to an address.

    Args:
        to_fund_address (address): Address to send to the tokens to.
        erc20_token_contract (Contract): Contract of the ERC20 token.
        ether_amount (float, optional): Amount to be sent, in ETHER. Defaults to 0.1.
        account (address, optional): Account from which to send the transaction. Defaults to None.

    Returns:
        TransactionReceipt
    """            
    account = account if account else get_account()

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

def encode_function_data(function=None, *args):
    """Encodes the function call.
    Commonly used for Initializers.

    Args:
        function ([brownie.network.contract.ContractTx], optional):
        The function we want to call. Example: `box.store`.
        Defaults to None.
        args (Any, optional):
        The arguments to pass to the function.
    Returns:
        [bytes]: Return the encoded bytes.
    """
    if len(args) == 0 or not function:
        # This is needed if the args are 0
        return eth_utils.to_bytes(hexstr="0x")

    # Brownie offers an encode_input() function for this
    return function.encode_input(*args)