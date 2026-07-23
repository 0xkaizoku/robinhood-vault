# Data Model: Morpho Yield Explorer & Signal Vaults

**Feature**: Morpho Yield Explorer  
**Date**: 2026-07-23  

---

## Entities

### 1. `MorphoVault`
Represents an active lending market / vault on Robinhood Chain.

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | `string` | Unique vault address (0x...) |
| `name` | `string` | Human-readable vault name (e.g. "USDC Treasury Yield Vault") |
| `asset` | `string` | Primary underlying asset symbol (USDC, rT-BILL, ETH) |
| `collateralAsset` | `string` | Collateral asset symbol |
| `supplyApy` | `number` | Net annual percentage yield (e.g. 5.45) |
| `borrowApy` | `number` | Borrow rate (if applicable) |
| `tvlUsd` | `number` | Total value locked in USD |
| `lltv` | `number` | Liquidation Loan-to-Value ratio (%) |
| `riskRating` | `'Low' | 'Medium' | 'High'` | Calculated risk score based on LLTV and collateral liquidity |

---

### 2. `SignalVault`
Represents a social copy-trading vault managed by a top trader.

| Field | Type | Description |
| :--- | :--- | :--- |
| `address` | `string` | ERC-4626 vault contract address |
| `managerAddress` | `string` | Strategist wallet address |
| `managerName` | `string` | Display name / ENS / handle |
| `performanceFeeBps` | `number` | Performance fee in basis points (e.g. 1000 = 10%) |
| `aumUsd` | `number` | Assets under management in USD |
| `historicalReturn30d` | `number` | 30-day percentage return |
| `subscribersCount` | `number` | Total retail depositors |

---

### 3. `PortfolioPosition`
Represents a connected user's active holdings across vaults.

| Field | Type | Description |
| :--- | :--- | :--- |
| `userAddress` | `string` | Connected wallet address |
| `vaultAddress` | `string` | Target vault address |
| `sharesOwned` | `bigint` | ERC-4626 vault shares |
| `underlyingBalanceUsd` | `number` | Current USD value of shares |
| `accruedInterestUsd` | `number` | Lifetime interest earned |

---

## State Transition Rules

1. **Deposit into Vault**:
   - `User` approves underlying token (e.g. USDC) -> calls `vault.deposit(amount, receiver)` -> `SignalVault` updates `aumUsd` and mints `sharesOwned` to `User`.
2. **Withdraw from Vault**:
   - `User` calls `vault.redeem(shares, receiver, owner)` -> `SignalVault` burns `sharesOwned` -> transfers underlying + accrued yield to `User`.
