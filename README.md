# Web3-Solidity
Initial approach to Web3 and Solidity Contracts.

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