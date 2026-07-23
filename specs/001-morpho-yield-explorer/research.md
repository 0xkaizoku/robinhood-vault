# Research Artifact: Morpho Yield Explorer Architecture & Tech Stack

**Feature**: Morpho Yield Explorer & Social Signal Vaults  
**Date**: 2026-07-23  

---

## 1. Network Selection: Robinhood Chain vs Mainnet/Other L2s

* **Decision**: Target **Robinhood Chain** (Chain ID: `4663`, Arbitrum Orbit L2).
* **Rationale**: 
  - Sub-250ms block times and micro-cent gas fees (<$0.01).
  - Direct exposure to 23M+ retail Robinhood users.
  - Eligibility for the $1,000,000+ Arbitrum Open House grant pool.
* **Alternatives Considered**: Arbitrum One (higher competition), Base (no direct Robinhood Wallet integration).

---

## 2. Web3 Client Library: Viem + Wagmi vs Ethers.js v6

* **Decision**: **Viem + Wagmi**.
* **Rationale**: Viem is modular, lightweight, tree-shakeable, and natively supports custom chain definitions (`defineChain`) with zero footprint overhead.
* **Alternatives Considered**: Ethers.js (larger bundle size, slower TypeScript inferencing).

---

## 3. DeFi Yield Protocol: Morpho Blue & MetaMorpho

* **Decision**: **Morpho Blue + MetaMorpho Vaults** using `@morpho-org/blue-sdk`.
* **Rationale**: Morpho Blue allows isolated lending pairs (e.g. Tokenized T-Bills / USDC) with custom liquidation loan-to-value (LLTV) ratios. MetaMorpho vaults aggregate yield automatically for retail users.
* **Alternatives Considered**: Aave v3 (less custom collateral flexibility for RWAs).

---

## 4. Copy-Trading Vault Standard: ERC-4626

* **Decision**: **ERC-4626 Tokenized Vault Standard**.
* **Rationale**: Industry standard for vault shares. When retail users deposit USDC into a strategist's signal vault, they receive vault shares representing their proportional ownership.
* **Alternatives Considered**: Custom non-standard staking contracts (harder to audit and integrate).
