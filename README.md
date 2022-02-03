# Web3-Solidity
Initial approach to Web3 and Solidity Contracts

## 1 | SimpleStorage
Extremely simple first Solidity contract, which allows users to store a number associated to them and retrieve it.

### 🐍 Web3
A simple ``deploy.py`` script is used to deploy a contract from a local workplace, instead of the usual use of Remix IDE.

The library ``solcx`` is used for the compiling of the contract. 

In order to deploy a contract, both the **ABI** and **Bytecode** are needed.



## 2 | FundMe
Simple Solidity contract that allows users to donate ETH. 
- Users that donate are saved and the amount donated is tracked.
- The owner (and only the owner) can retrieve all the accumulated ETH on the contract.
- A minimum amount of $50 in ETH is set, using a **``Chainlink Oracle``** price feed, to check the value of ETH in real time and thus calculate its current USD value.

# Ganache
Using [Ganache](https://trufflesuite.com/ganache/) to run a personal Ethereum blockchain locally to easily deploy and test and learn how the chain operates. 