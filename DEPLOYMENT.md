# Deployment Instructions for Horizon Protocol and Tee Box NFT

These smart contracts are designed to be deployed on EVM-compatible chains (e.g., Ethereum, Base, Arbitrum). Since this project environment does not support direct deployment, follow these steps to deploy using Remix or Hardhat in your local environment.

## Prerequisites

- **Remix IDE** (https://remix.ethereum.org) or a local **Hardhat** setup.
- **Metamask** or another wallet with funds for deployment.
- **OpenZeppelin Contracts**: The contracts import OpenZeppelin libraries. Remix handles this automatically. For Hardhat, install them via `npm install @openzeppelin/contracts`.

## 1. Deploy HorizonToken (HORIZON)

This is the ERC20 token with the burn logic.

### Constructor Arguments
1. `initialOwner` (address): The address that will own the contract (e.g., your wallet or a multi-sig).
2. `_oracle` (address): The address of the Oracle that can trigger burns.
3. `_phi` (uint256): The `phi` parameter for the burn formula (e.g., `500`).
4. `_gamma` (uint256): The `gamma` parameter for the burn formula (e.g., `500`).
5. `initialSupply` (uint256): The initial supply of tokens (in wei). E.g., for 100M tokens, use `100000000000000000000000000` (100,000,000 * 10^18).

### Deployment Steps (Remix)
1. Copy `contracts/HorizonToken.sol` to Remix.
2. Compile the contract using Solidity Compiler 0.8.20+.
3. In the "Deploy & Run" tab, select "HorizonToken".
4. Enter the arguments and click "Transact".

## 2. Deploy TeeBoxNFT (H-TEE)

This is the ERC721 NFT for the Tee Boxes.

### Constructor Arguments
1. `initialOwner` (address): The owner of the contract.
2. `_treasury` (address payable): The address where mint funds will be sent (Revolt Treasury).
3. `_price` (uint256): The price per NFT in wei. E.g., `50000000000000000` for 0.05 ETH.

### Deployment Steps (Remix)
1. Copy `contracts/TeeBoxNFT.sol` to Remix.
2. Compile the contract.
3. In the "Deploy & Run" tab, select "TeeBoxNFT".
4. Enter the arguments and click "Transact".

## Verification

After deployment, verify the contracts on Etherscan/Basescan using the source code or flattening the files.

## Integration

- Update the frontend with the deployed contract addresses.
- Ensure the Oracle backend uses the correct private key corresponding to the `_oracle` address set in `HorizonToken`.
