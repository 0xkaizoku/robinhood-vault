# Quickstart & Verification Guide: Morpho Yield Explorer

**Feature**: Morpho Yield Explorer & Signal Vaults  
**Target Chain**: Robinhood Chain (Chain ID `4663`)  

---

## 1. Local Development Setup

### Prerequisites
- Node.js v18+ and `npm`
- Installed dependencies: `viem`, `@morpho-org/blue-sdk`, `svelte`

### Running the App
```bash
npm install
npm run dev
```

The application will be served at `http://localhost:5173`.

---

## 2. Verification Scenarios

### Scenario 1: Verify Robinhood Chain RPC Connection
1. Open developer console in browser.
2. Check network requests to `https://rpc.robinhood.com` (or configured Alchemy RPC).
3. Confirm chain ID returns `4663`.

### Scenario 2: Test Morpho Yield Explorer Table
1. Navigate to the Explorer tab.
2. Verify that Morpho vaults are listed with APY, TVL, and risk ratings.
3. Apply filter `RWAs` — verify only Treasury / RWA collateral vaults are displayed.

### Scenario 3: Test Yield Calculator Simulation
1. Input deposit amount: `$5,000`.
2. Select lock duration: `12 Months`.
3. Verify calculated projected yield updates dynamically without page reload.
