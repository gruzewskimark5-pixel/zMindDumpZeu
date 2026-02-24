// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract TeeBoxNFT is ERC721, Ownable {
    uint256 public constant MAX_SUPPLY = 500;
    uint256 public totalSupply;
    address public treasury;
    uint256 public mintPrice = 0.1 ether;

    constructor(address _treasury) ERC721("TeeBoxNFT", "TBN") Ownable(msg.sender) {
        require(_treasury != address(0), "Invalid treasury");
        treasury = _treasury;
    }

    function mint() public payable {
        require(totalSupply < MAX_SUPPLY, "Max supply reached");
        require(msg.value >= mintPrice, "Insufficient funds");

        (bool success, ) = treasury.call{value: msg.value}("");
        require(success, "Transfer failed");

        totalSupply++;
        _safeMint(msg.sender, totalSupply);
    }

    function setMintPrice(uint256 _price) public onlyOwner {
        mintPrice = _price;
    }

    function setTreasury(address _treasury) public onlyOwner {
        require(_treasury != address(0), "Invalid treasury");
        treasury = _treasury;
    }
}
