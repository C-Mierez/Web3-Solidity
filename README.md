# Web3-Solidity
Initial approach to Web3 and Solidity Contracts.

> ## Notice
> This `readme` file is primarily made for myself as a place where I can dump information that I find relevant throughout my learning process. It exists both to get a general idea of what is done in the project, and to serve as a reminder of all good the practicies that were (and should) be applied regularly.

## 1 | SimpleStorage
Extremely simple first Solidity contract, which allows users to store a number associated to them and retrieve it.

### 🐍 Web3
A simple ``deploy.py`` script is used to deploy a contract from a local workplace, instead of the usual use of Remix IDE.

The library ``solcx`` is used for the compiling of the contract. 

In order to deploy a contract, both the **ABI** and **Bytecode** are needed. Then using the Web3 library, transactions can be built, signed and sent to the blockchain to create or interact with the contract.

### 👩‍🍳 Brownie

Different ways to approach key 🔑 storage were seen: 
- Using a local account (i.e Ganache)
- Using Brownie's built-in account manager (It stores the private key itself)
- Using a `.env` file and loading the key from the OS.
- Declaring the key in `brownie-config.yaml` for better clarity. It also uses the `.env` file.

A couple scripts were created:
- `deploy.py` Used to simulate the same actions that were done manually when using Python Web3. (Compiling, Deploying, Interacting)
- `read_value.py` Used to test interacting with an already deployed contract (Saved and managed by Brownie on its own)
  
A simple **Test** was created to for an initial approach to testing using Brownie isntead of doing it straight from Solidity.

## 2 | FundMe
Simple Solidity contract that allows users to donate ETH. 
- Users that donate are saved and the amount donated is tracked.
- The owner (and only the owner) can retrieve all the accumulated ETH on the contract.
- A minimum amount of $50 in ETH is set, using a **``Chainlink Oracle``** price feed, to check the value of ETH in real time and thus calculate its current USD value.

### 👩‍🍳 Brownie
Added use of external contracts (i.e Chainlink).

Declared in `brownie-config.yaml`:
- Dependencies being used (`smartcontractkit/chainlink-brownie-contracts@1.1.1`)
- Compiler remapping needed (`@chainlink=smartcontractkit/chainlink-brownie-contracts@1.1.1'`)

Verifying the contracts on Etherscan (or alike) using its API key. Brownie performs the ***flattening*** of the contract so that all dependencies can be uploaded and verified.

In order to work on the contract in a local Ganache chain -- in which the Chainlink dependencies do not exist -- there are two ways to approach this:
- **Mocking:** Parameterize the `FundMe.sol` contract.
  - Adding a parameter to the constructor with the address of the contracts used. So instead of creating them inside functions, they are declared globally.

    This allows to later decide what contract to use when in the `deploy.py` script. Useful for local deployments in which the Chainlink contracts don't exist, and thus would require a mock in their place instead.

- **Forking** Taking a "snapshot" of the current state of a mainnet and running it locally to interact with existing contracts deployed in it. 

# 3 | Lottery 
Loterry app where any user can participate and win the prize pot.
- Users enter the lottery by paying a certain USD value of ETH.
- Admin can choose when to close the lottery.
- A random winner will be selected using ``Chainlink VRF``.

### 👩‍🍳 Brownie
A complete rework in favour of modularization is made in comparison to the previous projects.
- `utils.py` Contains far more generic methods that allow easier integration and switching between different working environments (Local networks, forks, testnets, mainnets).

  Additionally provides an easier and dynamic way of obtaining the contract address of the dependencies corresponding to the network being worked on.
- Deploying mocks is only done when mocks have not been previously created, and it's done transparently only when needed.

# 🍫 Ganache
Using [Ganache](https://trufflesuite.com/ganache/) to run a personal Ethereum blockchain locally to easily deploy and test and learn how the chain operates. 

# 👩‍🍳 Brownie
Using [Brownie](https://github.com/eth-brownie/brownie) to facilitate all of the above process that was done manually. (Compiling, Deploying, Interacting, ...)

Brownie project structure has the following features:
- `build` Tracks low-level information.
    - *Interfaces* being worked with or deployed.
    - *Deployments* accross all different chains used-
    - *Compiled Contracts*
- `contracts` Where the contracts to de compiled/deployed are located.
- `interfaces` Save and store different interfaces. (For example, Chainlink)
- `reports`
- `scripts` For automating tasks. (Like deploying, calling functions, ...)
- `tests` 

Used throughout the different sub-projects. Looking to see and compare how it facilitates development as opposed to doing things manually.

# 🧾 Tests
Due to ease of use, tests are run mainly on a local **Ganache** chain. In case of having dependencies, these should be **Mocked**.

Additionally, integration tests should later be performed on a live **Testnet**.

Optional further testing can be done using:
- Brownie mainnet forks
- Custom mainnet forks
- Local Ganache chains

# 👀 Other Notes
> There is a Solidity compiler-specific [reason](https://ethereum.stackexchange.com/a/64109) as to why `address` and `address payable` are two different types. 
>
> In short, it exists as a way to explicitly state whether an address will be involved in any kind of transfer operation. 
***
> Randomness in critical apps is tricky subject, and using pseudo-random methods can lead to potential security risks and vulnerability. Aformentioned methods are used for the sake of simplicity. But in a real production app, randomness should be handled using a different approach.  
>> One of the unsecure but used methods is using a *Globally available variable* value and play around with it somehow, for example, hashing together a bunch of data like block timestamp, difficulty, nonce, and so on.
>
>> In this project, a secure randomness approach is the use of `Chainlink VRF` (Verifiable Random Function), which is a far more secure way to handle this requirement. 
>>
>> - When using Chainlink VRF, it is actually an **asynchronous** operation. Our contract sends a tx (Request) to the chainlink node, paying the network gas fee *and* an oracle fee. But a result is not immediately available. Instead, the contract waits until the chainlink node interacts with it and delivers the requested random number (Response).
***
> Brownie has offers two classes that wrap functionality for **contract** interactions. 
> Further reading in the [docs](https://eth-brownie.readthedocs.io/en/stable/api-network.html?highlight=from_abi#brownie.network.contract.Contract).
> - `ProjectContract` is available inside the project, and since it is compiled by Brownie, it offers a wide range of contract-specific functionality.
> - `Contract` is used for contracts that are **NOT** in the project, but are already deployed in whatever environment being worked on.
> 
>   This was used for the Lottery dependencies, in which the Chainlink contracts already existed in the testnets and thus just needed to be interacted with. 
> 
> Additionally, when there's no access to a contract but its Interface is available, Brownie has an `interface` class which can be used to interact with the contract as well.
> 
> An example of this in this project is the following:
>      
>      interface.LinkTokenInterface(link_token.address)
***
> When using [PyTest](https://docs.pytest.org/en/7.0.x/), it is common to find a `conftest.py` file inside the `test` folder.
>
> This file is used to define *fixtures* on a global scope, so that they can be used in multiple test files.
>
> Fixtures are functions that allow an easier and less repetitive way of defining data for the tests, such as Database connection details, URLs, inputs, etc.
> 
> A fixture is defined using the following decorator below a function:
> 
>     @pytest.fixture
***