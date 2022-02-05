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

    // AggregatorV3Interface global declaration, instead of internal declarations
    // inside each method
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeedAddr) public {
        priceFeed = AggregatorV3Interface(_priceFeedAddr);
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner.");
        _;
    }

    function fund() public payable {
        // Set a threshold for funding in terms of USD value
        uint256 minimumUSD = 50 * (10**18);
        require(
            getConversionRate(msg.value) >= minimumUSD,
            "More ETH required."
        );
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer);
    }

    // 1 Eth = 1000000000 Gwei
    function getConversionRate(uint256 _ethAmount)
        public
        view
        returns (uint256)
    {
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
