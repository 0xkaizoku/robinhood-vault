import type { SignalVault } from '../types/vault.ts';

export const MOCK_SIGNAL_VAULTS: SignalVault[] = [
  {
    address: '0xVaultAlpha111111111111111111111111111111',
    name: 'Robinhood Alpha RWA Yield Aggregator',
    symbol: 'rhALPHA',
    managerAddress: '0x8888888888888888888888888888888888888888',
    managerName: 'SatoshiRetail_Cap',
    strategyDescription: 'Automated 70/30 allocation between US T-Bills and Morpho ETH lending pools.',
    performanceFeePercent: 10,
    aumUsd: 4150000,
    historicalReturn30d: 14.8,
    subscribersCount: 842,
    riskScore: 3,
  },
  {
    address: '0xVaultBeta222222222222222222222222222222',
    name: 'DeFi Max Yield Arbitrage Vault',
    symbol: 'rhARBIT',
    managerAddress: '0x9999999999999999999999999999999999999999',
    managerName: 'QuantOrbit_Vaults',
    strategyDescription: 'High-frequency interest rate arbitrage across Morpho Blue markets on Robinhood Chain.',
    performanceFeePercent: 15,
    aumUsd: 1890000,
    historicalReturn30d: 22.4,
    subscribersCount: 419,
    riskScore: 6,
  },
];

export async function fetchSignalVaults(): Promise<SignalVault[]> {
  await new Promise((resolve) => setTimeout(resolve, 80));
  return MOCK_SIGNAL_VAULTS;
}

export async function depositToSignalVault(vaultAddress: string, amountUsdc: number): Promise<{ txHash: string; status: 'success' }> {
  // Simulating sub-250ms Robinhood Chain transaction execution
  await new Promise((resolve) => setTimeout(resolve, 400));
  const mockTxHash = `0x${Array.from({ length: 64 }, () => Math.floor(Math.random() * 16).toString(16)).join('')}`;
  return { txHash: mockTxHash, status: 'success' };
}
