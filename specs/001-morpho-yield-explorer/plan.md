# Implementation Plan: Morpho Yield Explorer & Social Copy-Trading Vaults

**Branch**: `001-morpho-yield-explorer`  
**Feature Specification**: [`spec.md`](./spec.md)  
**Status**: In Design  

---

## Technical Context & Technology Choices

### Core Technologies
- **Target Network**: Robinhood Chain (Arbitrum Orbit L2, Chain ID `4663`, Native Gas Token ETH)
- **Frontend Framework**: Svelte + Vite (Fast, reactive, minimal bundle overhead)
- **Styling**: Vanilla CSS with modern Glassmorphism token design system
- **Web3 Client**: `viem` + `wagmi` for wallet connection (Robinhood Wallet, Web3Modal, MetaMask)
- **DeFi Protocol SDK**: `@morpho-org/blue-sdk` for Morpho market queries, LLTV calculations, and vault data
- **Contract Standard**: ERC-4626 Tokenized Vaults for Social Signal Copy-Trading

### Architecture Overview
1. **Frontend App**: Interactive dashboard displaying Morpho Lending Vaults, APY analytics, Risk scores, and Copy-Trading Signal Vaults.
2. **Web3 Provider Layer**: Custom Viem client configured for Robinhood Chain RPCs (`https://rpc.robinhood.com` / Alchemy RPC).
3. **Vault Integration Layer**: Interacts with Morpho Blue Core & MetaMorpho contracts for lending metrics and OpenZeppelin ERC-4626 for social copy-trading vaults.

---

## Design Artifacts Summary

- 🔍 **[`research.md`](./research.md)** — Architectural decisions & tech stack rationale
- 📊 **[`data-model.md`](./data-model.md)** — Data structures, entities, and state transition rules
- 🚀 **[`quickstart.md`](./quickstart.md)** — Developer setup and end-to-end testing scenarios

---

## Proposed Changes

### Component 1: Web3 Infrastructure & Robinhood Chain Config
- Define Robinhood Chain network configuration (`id: 4663`, RPC endpoints, Block Explorer).
- Initialize Viem public client and Wagmi provider hooks.

### Component 2: Yield Explorer Dashboard
- Build `VaultCard.svelte` and `YieldTable.svelte` to display Morpho markets (Collateral, Loan Asset, Supply APY, Net Rewards, TVL).
- Implement dynamic filtering by asset type (RWAs, Treasuries, Stablecoins, ETH).
- Build `YieldCalculator.svelte` for simulating interest earnings based on deposit amount and lock period.

### Component 3: Social Copy-Trading Vaults (ERC-4626)
- Build `SignalVaultCard.svelte` showing strategist profiles, historical performance, AUM, and performance fee (%).
- Provide `DepositModal.svelte` allowing users to mint vault shares in 1-click.

---

## Verification Plan

### Automated Tests
- Unit tests for yield calculation logic (`calcSupplyApy`, `simulatedReturn`).
- Integration tests for RPC connection resilience to Robinhood Chain.

### Manual Verification
1. Launch local dev server (`npm run dev`).
2. Verify Morpho vault list loads and renders live APY data.
3. Test yield return simulator with sample inputs ($1,000 USDC deposit over 12 months).
4. Verify wallet connection modal detects Robinhood Chain network (Chain ID `4663`).
