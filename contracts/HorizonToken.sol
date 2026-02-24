// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract HorizonToken is ERC20, ERC20Burnable, Pausable, Ownable {
    uint256 public lastBurnTime;
    uint256 public constant BURN_COOLDOWN = 24 hours;
    uint256 public constant MAX_DAILY_BURN_PERCENT = 5; // 0.5% = 5/1000

    event OracleBurn(uint256 amount, string reason);

    constructor() ERC20("HorizonToken", "HZN") Ownable(msg.sender) {
        _mint(msg.sender, 1000000000 * 10 ** decimals());
    }

    function pause() public onlyOwner {
        _pause();
    }

    function unpause() public onlyOwner {
        _unpause();
    }

    function oracleBurn(uint256 amount, string memory reason) public onlyOwner {
        require(block.timestamp >= lastBurnTime + BURN_COOLDOWN, "Burn cooldown active");
        uint256 maxBurn = (totalSupply() * MAX_DAILY_BURN_PERCENT) / 1000;
        require(amount <= maxBurn, "Burn amount exceeds limit");

        _burn(msg.sender, amount);
        lastBurnTime = block.timestamp;
        emit OracleBurn(amount, reason);
    }

    // The following functions are overrides required by Solidity.
    function _update(address from, address to, uint256 value)
        internal
        override(ERC20)
    {
        whenNotPaused();
        super._update(from, to, value);
    }
}
