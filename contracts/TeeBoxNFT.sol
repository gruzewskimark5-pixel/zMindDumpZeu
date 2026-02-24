// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

contract TeeBoxNFT is ERC721, ERC721URIStorage, Ownable, ReentrancyGuard {
    uint256 public constant MAX_SUPPLY = 500;
    uint256 public nextTokenId;
    uint256 public price;
    address payable public treasury;

    event Minted(address indexed recipient, uint256 tokenId);
    event PriceUpdated(uint256 newPrice);
    event TreasuryUpdated(address newTreasury);

    constructor(
        address initialOwner,
        address payable _treasury,
        uint256 _price
    )
        ERC721("Horizon Tee Box", "H-TEE")
        Ownable(initialOwner)
    {
        require(_treasury != address(0), "Invalid treasury address");
        treasury = _treasury;
        price = _price;
        nextTokenId = 1; // Start from ID 1
    }

    function mint(string memory uri) external payable nonReentrant {
        require(nextTokenId <= MAX_SUPPLY, "Max supply reached");
        require(msg.value >= price, "Insufficient payment");

        // Transfer funds to treasury
        (bool success, ) = treasury.call{value: msg.value}("");
        require(success, "Transfer to treasury failed");

        uint256 tokenId = nextTokenId;
        _safeMint(msg.sender, tokenId);
        _setTokenURI(tokenId, uri);

        nextTokenId++;

        emit Minted(msg.sender, tokenId);
    }

    // Admin functions
    function setPrice(uint256 _newPrice) external onlyOwner {
        price = _newPrice;
        emit PriceUpdated(_newPrice);
    }

    function setTreasury(address payable _newTreasury) external onlyOwner {
        require(_newTreasury != address(0), "Invalid treasury address");
        treasury = _newTreasury;
        emit TreasuryUpdated(_newTreasury);
    }

    // Required overrides
    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
