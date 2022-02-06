// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery is VRFConsumerBase, Ownable {
    // Keep track of the participants
    // These can have token transfers, hence they are declared as [payable]
    address payable[] public participants;
    address payable public recentWinner;
    uint256 randomness;

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

    // Chainlink VRF variables
    uint256 public vrf_fee;
    bytes32 public vrf_keyhash;

    constructor(
        address _priceFeedAddress,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyhash
    ) public VRFConsumerBase(_vrfCoordinator, _link) {
        minimumUSD = 50 * (10**18); // 50$ fee
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
        vrf_fee = _fee;
        vrf_keyhash = _keyhash;
    }

    // Enter the lottery
    function bid() public payable {
        // Require the lottery to be open
        require(
            lottery_state == LOTTERY_STATE.OPEN,
            "The lottery is not currently open."
        );
        // Require minimum of 50$
        require(msg.value >= getEntranceFee(), "Not enough ETH.");
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

        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;

        // Request VRF to chainlink oracle
        // Method already returns a bytes32 [requestId]
        requestRandomness(vrf_keyhash, vrf_fee);
    }

    // Chainlink VRF node response method
    // internal method - This shouldnt be called by anything else other than the VRFCoordinator
    // override - Fulfill the interface declaration
    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        require(
            lottery_state == LOTTERY_STATE.CALCULATING_WINNER,
            "Lottery is not expecting a winner."
        );
        require(_randomness > 0, "Random number not found.");

        // Choose the winner
        uint256 winnerIndex = _randomness % participants.length;
        recentWinner = participants[winnerIndex];

        // Transfer the prize to the winner
        recentWinner.transfer(address(this).balance);

        // Reset the lottery
        participants = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
        randomness = _randomness;
    }
}
