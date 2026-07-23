# Tasks: Morpho Yield Explorer & Social Copy-Trading Vaults

**Feature Branch**: `001-morpho-yield-explorer`  
**Spec File**: [`spec.md`](./spec.md)  
**Plan File**: [`plan.md`](./plan.md)  

---

## Phase 1: Setup & Environment

- [X] T001 Initialize Robinhood Chain Viem network config in `src/lib/web3/chainConfig.ts`
- [X] T002 Configure Viem PublicClient and RPC connection in `src/lib/web3/client.ts`
- [X] T003 Install `@morpho-org/blue-sdk` and `viem` dependencies in `package.json`

---

## Phase 2: Foundational Layer

- [X] T004 Create Morpho Market TypeScript interfaces and types in `src/lib/types/morpho.ts`
- [X] T005 Create Signal Vault (ERC-4626) interfaces in `src/lib/types/vault.ts`
- [X] T006 Implement Morpho Blue data fetching service in `src/lib/services/morphoService.ts`

---

## Phase 3: User Story 1 - Morpho Vault Yield Discovery (P1)

Goal: Retail investors can explore, filter, and calculate yields on Morpho lending markets on Robinhood Chain.

- [X] T007 [P] [US1] Build `VaultCard` component displaying Vault APY, TVL, Collateral, and Risk Rating in `src/main.js`
- [X] T008 [P] [US1] Build `YieldTable` displaying sortable Morpho markets in `src/main.js`
- [X] T009 [US1] Build `AssetFilter` for filtering markets by RWA, Treasury, Stablecoin, or ETH collateral in `src/main.js`
- [X] T010 [US1] Build `YieldCalculator` interactive return simulator component in `src/main.js`
- [X] T011 [US1] Assemble main Explorer Page layout in `index.html`

---

## Phase 4: User Story 2 - Social Copy-Trading Signal Vaults (P2)

Goal: Retail users can subscribe to top trader ERC-4626 signal vaults.

- [X] T012 [P] [US2] Build `SignalVaultCard` component showing strategist AUM, historical return, and fee % in `src/main.js`
- [X] T013 [US2] Build `DepositModal` web3 transaction modal for depositing USDC into signal vaults in `index.html` & `src/main.js`
- [X] T014 [US2] Integrate ERC-4626 `deposit` and `redeem` Viem write contract hooks in `src/lib/services/vaultService.ts`

---

## Phase 5: Polish & Cross-Cutting Concerns

- [X] T015 Enhance responsive layout styling and glassmorphism visual tokens in `src/styles/app.css`
- [X] T016 Add RPC fallback error handling and disconnect notifications in `src/main.js`
- [X] T017 Run end-to-end verification scenario against Robinhood Chain testnet (Chain ID `46630`)
