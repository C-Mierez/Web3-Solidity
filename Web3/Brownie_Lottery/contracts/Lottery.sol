// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery is Ownable {
    // Keep track of the participants
    // These can have token transfers, hence they are declared as [payable]
    address payable[] public participants;

    uint256 minimumUSD;

    // Chainlink price feed
    AggregatorV3Interface internal ethUsdPriceFeed;

    // Current state of the lottery
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lottery_state;

    constructor(address _priceFeedAddress) public {
        minimumUSD = 50 * (10**18); // 50$ fee
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
    }

    // Enter the lottery
    function bid() public payable {
        // Require the lottery to be open
        require(lottery_state == LOTTERY_STATE.OPEN);
        // Require minimum of 50$
        require(msg.value >= getEntranceFee(), "Not enough ETH");
        participants.push(msg.sender);
    }

    // Entrance fee getter
    function getEntranceFee() public view returns (uint256) {
        /** Calc:
        50$, $2000 / ETH
        50 / 2000
        50 * 100000 / 200
        */

        // Get the current ETH value
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        // Convert to uint256 and add the additional decimals
        uint256 uPrice = uint256(price) * (10**10);
        // Adding additional decimals to the USD price so it cancels out with the priceFeed price
        uint256 priceToEnter = (minimumUSD * 10**18) / uPrice;
        return priceToEnter;
    }

    // ADMIN: Start lottery
    function startLottery() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "There is already an active lottery."
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    // ADMIN: End lottery
    function endLottery() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.OPEN,
            "There is currently no active lottery."
        );
        lottery_state = LOTTERY_STATE.CLOSED;
    }
}
