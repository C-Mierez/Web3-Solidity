pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "./MockToken.sol";

contract MockLINK is ERC20, MockToken {
    constructor() public ERC20("Mock LINK", "LINK") {}
}
