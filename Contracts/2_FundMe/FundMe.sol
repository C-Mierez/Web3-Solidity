// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256;

    address owner;

    // Store the address of the funder
    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;

    constructor() public {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner.");
        _;
    }

    function fund() public payable {
        // Set a threshold for funding in terms of USD value
        // Since we are operating with Wei, we need to add 18 decimals
        uint256 minimumUSD = 50 * (10**18);
        // [getConversionRate(_ethAmount)] returns a value with 18 decimals
        require(
            getConversionRate(msg.value) >= minimumUSD,
            "More ETH required."
        );
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0x9326BFA02ADD2366b30bacB125260Af641031331
        );
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0x9326BFA02ADD2366b30bacB125260Af641031331
        );
        (
            uint80 roundId,
            int256 answer,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();
        return uint256(answer);
    }

    // 1 Eth = 1000000000 Gwei
    function getConversionRate(uint256 _ethAmount)
        public
        view
        returns (uint256)
    {
        /** 
        Chainlink latestRoundData returns an 18 decimal value for ETH/X pairs. And 8 decimals for others.
        [ethPrice] has 8 decimals
        [_ethAmount] has 18 decimals.
        [ethAmountInUsd] needs to have 8 decimals removed after calculating. (So the value has 18 decimals)
        */
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (_ethAmount * ethPrice) / (10**8);
        return ethAmountInUsd;
    }

    function withdraw() public payable onlyOwner {
        msg.sender.transfer(address(this).balance);
        for (uint256 i = 0; i < funders.length; i++) {
            address funder = funders[i];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0);
    }
}
