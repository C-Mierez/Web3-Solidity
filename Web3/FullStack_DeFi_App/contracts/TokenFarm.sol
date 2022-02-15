// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

import "./RewardToken.sol";

contract TokenFarm is Ownable {
    /** Basic Farming contract
     *
     *   Functionalities:
     *   - Stake tokens
     *   - Unstake tokens
     *   - Mint reward tokens
     *   - Add Allowed tokens
     *   - Get ETH value
     */

    /* --------------------------------- Staking -------------------------------- */
    // User Address => Token Address => Balance
    mapping(address => mapping(address => uint256)) public stakedBalance;
    // User Address => Unique Tokens Staked count
    mapping(address => uint256) public uniqueStakedCount;

    // Unique staked users
    address[] public stakers;

    /* --------------------------------- Minting -------------------------------- */
    RewardToken public rewardToken;

    /* ------------------------------- Price Feed ------------------------------- */
    mapping(address => address) public tokenToPriceFeed;

    /* -------------------------------- Allowance ------------------------------- */
    mapping(address => bool) public allowedTokens;
    address[] public allowedTokensKeys;

    /* ------------------------------- Constructor ------------------------------ */
    constructor(address _rewardToken) public {
        rewardToken = RewardToken(_rewardToken);
    }

    /* --------------------------------- Staking -------------------------------- */

    function stakeTokens(uint256 _amount, address _token) public {
        require(_amount > 0, "Must stake more than 0.");
        require(isAllowedToken(_token), "Token not allowed.");

        // Transfer the tokens to the contract
        IERC20(_token).transferFrom(msg.sender, address(this), _amount);

        // Update user info after staking
        _updateUniqueStakedCount(msg.sender, _token);
        stakedBalance[msg.sender][_token] += _amount;

        // Add to list only if this is the first time staking
        if (uniqueStakedCount[msg.sender] == 1) {
            stakers.push(msg.sender);
        }
    }

    function unstakeTokens(address _token) public {
        require(
            stakedBalance[msg.sender][_token] > 0,
            "Must unstake more than 0."
        );

        IERC20(_token).transfer(msg.sender, stakedBalance[msg.sender][_token]);

        stakedBalance[msg.sender][_token] = 0;

        uniqueStakedCount[msg.sender] -= 1;

        // Remove from list if this is the last token unstake
        if (uniqueStakedCount[msg.sender] == 0) {
            for (uint256 i; i < stakers.length; i++) {
                if (stakers[i] == msg.sender) {
                    stakers[i] = stakers[stakers.length - 1];
                    stakers.pop();
                }
            }
        }
    }

    function _updateUniqueStakedCount(address _user, address _token) internal {
        if (stakedBalance[_user][_token] <= 0) {
            uniqueStakedCount[_user] += 1;
        }
    }

    /* ------------------------------- Price Feed ------------------------------- */

    function _setPriceFeed(address _token, address _priceFeed) internal {
        tokenToPriceFeed[_token] = _priceFeed;
    }

    function getUserTVL(address _user) public view returns (uint256) {
        require(uniqueStakedCount[_user] > 0, "User has no staked tokens.");
        uint256 tvl = 0;
        for (uint256 i; i < allowedTokensKeys.length; i++) {
            tvl += getUserTokenTVL(_user, allowedTokensKeys[i]);
        }
        return tvl;
    }

    function getUserTokenTVL(address _user, address _token)
        public
        view
        returns (uint256)
    {
        if (uniqueStakedCount[_user] <= 0) {
            return 0;
        }
        (uint256 price, uint256 decimals) = getTokenValue(_token);

        return (stakedBalance[_user][_token] * price) / (10**decimals);
    }

    function getTokenValue(address _token)
        public
        view
        returns (uint256, uint256)
    {
        address priceFeedAddress = tokenToPriceFeed[_token];
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            priceFeedAddress
        );
        (, int256 price, , , ) = priceFeed.latestRoundData();
        uint256 decimals = uint256(priceFeed.decimals());
        return (uint256(price), decimals);
    }

    /* --------------------------------- Minting -------------------------------- */

    function mintRewards() public onlyOwner {
        for (uint256 i = 0; i < stakers.length; i++) {
            address _user = stakers[i];
            uint256 _userTVL = getUserTVL(_user);

            // Send the usd value amount in Reward tokens
            // This is just for the sake of trying the minting function
            // Not an actual reward system
            rewardToken.mint(_user, _userTVL);
        }
    }

    /* -------------------------------- Allowance ------------------------------- */

    function addAllowedToken(address _token, address _priceFeed)
        public
        onlyOwner
    {
        allowedTokens[_token] = true;
        allowedTokensKeys.push(_token);

        // Add corresponding price feed for the new token
        _setPriceFeed(_token, _priceFeed);
    }

    function isAllowedToken(address _token) public view returns (bool) {
        return allowedTokens[_token];
    }
}
