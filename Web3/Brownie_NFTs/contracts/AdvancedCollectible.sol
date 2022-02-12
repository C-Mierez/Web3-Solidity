// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;

    // VRF
    bytes32 public keyHash;
    uint256 public fee;

    // Mappings
    mapping(uint256 => StonkType) public tokenIdToStonkType;
    mapping(bytes32 => address) public requestIdToSender;

    enum StonkType {
        UltraStonks,
        Stonks,
        NoStonks
    }

    // Events
    event requestedCollectible(
        bytes32 indexed requestId,
        address indexed requester
    );
    event stonkTypeAssigned(
        uint256 indexed tokenId,
        StonkType indexed stonkType
    );

    constructor(
        address _vrfCoordinator,
        address _link,
        bytes32 _keyHash,
        uint256 _fee,
        string memory _tokenName,
        string memory _tokenSymbol
    )
        public
        VRFConsumerBase(_vrfCoordinator, _link)
        ERC721(_tokenName, _tokenSymbol)
    {
        tokenCounter = 0;
        keyHash = _keyHash;
        fee = _fee;
    }

    // No need to have the tokenURI sent as a parameter since this method won't do the actual
    // minting, unlike the SimpleCollectible contract
    function createCollectible() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyHash, fee);
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomness)
        internal
        override
    {
        StonkType stonkType = StonkType(randomness % 3);

        uint256 newTokenId = tokenCounter;
        tokenIdToStonkType[newTokenId] = stonkType;
        emit stonkTypeAssigned(newTokenId, stonkType);

        _safeMint(requestIdToSender[requestId], newTokenId);

        tokenCounter += 1;
    }

    // This could be made from the fulfillRandomness method, instead of relying on the centralized
    // party for calling  this method
    function setTokenURI(uint256 tokenId, string memory tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: caller is not approved or owner."
        );
        _setTokenURI(tokenId, tokenURI);
    }
}
