pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

abstract contract MockToken is ERC20 {
    function faucet(uint256 _amount) public {
        _mint(msg.sender, _amount);
    }
}
