export interface MorphoVault {
  id: string;
  name: string;
  asset: string;
  collateralAsset: string;
  category: 'RWA' | 'Treasury' | 'Stablecoin' | 'Crypto';
  supplyApy: number;
  borrowApy: number;
  tvlUsd: number;
  lltv: number; // Liquidation Loan-to-Value in %
  riskRating: 'Low' | 'Medium' | 'High';
  contractAddress: string;
}

export interface YieldSimulation {
  depositAmount: number;
  durationMonths: number;
  projectedEarnedUsd: number;
  effectiveApy: number;
}
