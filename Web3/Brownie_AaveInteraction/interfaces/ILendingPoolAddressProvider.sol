// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

interface ILendingPoolAddressesProvider {
    function getLendingPool() external view returns (address);
}

// It is possible to manually define the interface of a contract
// That way only the neccesary methods are used
// Of course, copying the entire interface when available can be beneficial to avoid issues
