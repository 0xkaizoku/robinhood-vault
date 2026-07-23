import type { MorphoVault, YieldSimulation } from '../types/morpho.ts';

export const MOCK_MORPHO_VAULTS: MorphoVault[] = [
  {
    id: '0x1111111111111111111111111111111111111111',
    name: 'Robinhood US Treasury 3-Month Yield Vault',
    asset: 'USDC',
    collateralAsset: 'rT-BILL (Tokenized US Treasury)',
    category: 'Treasury',
    supplyApy: 5.45,
    borrowApy: 6.80,
    tvlUsd: 14250000,
    lltv: 86.5,
    riskRating: 'Low',
    contractAddress: '0x1111111111111111111111111111111111111111',
  },
  {
    id: '0x2222222222222222222222222222222222222222',
    name: 'Tokenized Equities Index Collateralized USDC',
    asset: 'USDC',
    collateralAsset: 'rSPY (S&P 500 Token)',
    category: 'RWA',
    supplyApy: 6.12,
    borrowApy: 7.45,
    tvlUsd: 8900000,
    lltv: 80.0,
    riskRating: 'Low',
    contractAddress: '0x2222222222222222222222222222222222222222',
  },
  {
    id: '0x3333333333333333333333333333333333333333',
    name: 'Robinhood Staked ETH Yield Multiplier',
    asset: 'WETH',
    collateralAsset: 'wstETH',
    category: 'Crypto',
    supplyApy: 4.85,
    borrowApy: 5.90,
    tvlUsd: 22100000,
    lltv: 91.5,
    riskRating: 'Low',
    contractAddress: '0x3333333333333333333333333333333333333333',
  },
  {
    id: '0x4444444444444444444444444444444444444444',
    name: 'High-Yield RWA Real Estate Cashflow Vault',
    asset: 'USDT',
    collateralAsset: 'rREIT (Real Estate Vault Token)',
    category: 'RWA',
    supplyApy: 8.75,
    borrowApy: 10.20,
    tvlUsd: 3800000,
    lltv: 75.0,
    riskRating: 'Medium',
    contractAddress: '0x4444444444444444444444444444444444444444',
  },
];

export async function fetchMorphoVaults(categoryFilter?: string): Promise<MorphoVault[]> {
  // Simulating sub-250ms RPC response latency on Robinhood Chain
  await new Promise((resolve) => setTimeout(resolve, 80));
  
  if (!categoryFilter || categoryFilter === 'All') {
    return MOCK_MORPHO_VAULTS;
  }
  return MOCK_MORPHO_VAULTS.filter((v) => v.category === categoryFilter);
}

export function calculateProjectedYield(depositAmount: number, durationMonths: number, apy: number): YieldSimulation {
  const annualRate = apy / 100;
  const years = durationMonths / 12;
  // Compound monthly
  const totalAmount = depositAmount * Math.pow(1 + annualRate / 12, 12 * years);
  const earnedUsd = totalAmount - depositAmount;

  return {
    depositAmount,
    durationMonths,
    projectedEarnedUsd: Number(earnedUsd.toFixed(2)),
    effectiveApy: apy,
  };
}
