export interface SignalVault {
  address: string;
  name: string;
  symbol: string;
  managerAddress: string;
  managerName: string;
  avatarUrl?: string;
  strategyDescription: string;
  performanceFeePercent: number;
  aumUsd: number;
  historicalReturn30d: number;
  subscribersCount: number;
  riskScore: number; // 1 to 10
}

export interface UserPortfolioPosition {
  vaultAddress: string;
  vaultName: string;
  sharesBalance: bigint;
  underlyingBalanceUsd: number;
  earnedYieldUsd: number;
}
