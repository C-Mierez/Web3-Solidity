// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/AccessControlEnumerable.sol";

contract RewardToken is ERC20, AccessControlEnumerable {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");

    constructor(string memory _name, string memory _symbol)
        public
        ERC20(_name, _symbol)
    {
        _setupRole(DEFAULT_ADMIN_ROLE, _msgSender());
    }

    function mint(address _to, uint256 _amount) public {
        require(
            hasRole(MINTER_ROLE, _msgSender()),
            "Must have printer role to mint."
        );
        _mint(_to, _amount);
    }

    // Disgusting, I know
    function addMinter(address _account) public {
        require(
            hasRole(MINTER_ROLE, _msgSender()),
            "Must have admin role to add minter."
        );
        _setupRole(MINTER_ROLE, _account);
    }
}
