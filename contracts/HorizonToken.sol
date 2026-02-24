// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/Pausable.sol";

contract HorizonToken is ERC20, ERC20Burnable, Ownable, ReentrancyGuard, Pausable {
    address public oracle;

    // Constants for burn calculation
    uint256 public phi;
    uint256 public gamma;

    uint256 public lastBurnTimestamp;
    uint256 public constant BURN_COOLDOWN = 24 hours;
    uint256 public constant MAX_DAILY_BURN_BASIS_POINTS = 50; // 0.5% = 50 bps

    event OracleUpdated(address indexed previousOracle, address indexed newOracle);
    event BurnTriggered(uint256 greenFee, uint256 wagerVolume, uint256 burnAmount);
    event ParametersUpdated(uint256 newPhi, uint256 newGamma);

    constructor(
        address initialOwner,
        address _oracle,
        uint256 _phi,
        uint256 _gamma,
        uint256 initialSupply
    )
        ERC20("Horizon Protocol", "HORIZON")
        Ownable(initialOwner)
    {
        oracle = _oracle;
        phi = _phi;
        gamma = _gamma;
        _mint(msg.sender, initialSupply);
    }

    modifier onlyOracle() {
        require(msg.sender == oracle, "Caller is not the oracle");
        _;
    }

    function setOracle(address _newOracle) external onlyOwner {
        require(_newOracle != address(0), "Invalid oracle address");
        emit OracleUpdated(oracle, _newOracle);
        oracle = _newOracle;
    }

    function setParameters(uint256 _phi, uint256 _gamma) external onlyOwner {
        phi = _phi;
        gamma = _gamma;
        emit ParametersUpdated(_phi, _gamma);
    }

    function pause() external onlyOwner {
        _pause();
    }

    function unpause() external onlyOwner {
        _unpause();
    }

    function triggerBurn(uint256 greenFee, uint256 wagerVolume) external onlyOracle nonReentrant whenNotPaused {
        require(block.timestamp >= lastBurnTimestamp + BURN_COOLDOWN, "Burn cooldown active");

        uint256 burnAmount = (greenFee * phi + wagerVolume * gamma) / 1e18;

        // Cap burn at 0.5% of circulating supply
        uint256 maxBurn = (totalSupply() * MAX_DAILY_BURN_BASIS_POINTS) / 10000;
        if (burnAmount > maxBurn) {
            burnAmount = maxBurn;
        }

        // Ensure the oracle (caller) has enough tokens to burn
        require(balanceOf(msg.sender) >= burnAmount, "Insufficient balance to burn");

        _burn(msg.sender, burnAmount);
        lastBurnTimestamp = block.timestamp;

        emit BurnTriggered(greenFee, wagerVolume, burnAmount);
    }
}
