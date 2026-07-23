import { defineChain } from 'viem';

export const robinhoodChain = defineChain({
  id: 4663,
  name: 'Robinhood Chain',
  nativeCurrency: {
    decimals: 18,
    name: 'Ether',
    symbol: 'ETH',
  },
  rpcUrls: {
    default: {
      http: ['https://rpc.robinhood.com'],
    },
    public: {
      http: ['https://rpc.robinhood.com'],
    },
  },
  blockExplorers: {
    default: {
      name: 'Robinhood Explorer',
      url: 'https://explorer.robinhood.com',
    },
  },
});

export const robinhoodTestnet = defineChain({
  id: 46630,
  name: 'Robinhood Chain Testnet',
  nativeCurrency: {
    decimals: 18,
    name: 'Testnet Ether',
    symbol: 'tETH',
  },
  rpcUrls: {
    default: {
      http: ['https://testnet-rpc.robinhood.com'],
    },
    public: {
      http: ['https://testnet-rpc.robinhood.com'],
    },
  },
  blockExplorers: {
    default: {
      name: 'Robinhood Testnet Explorer',
      url: 'https://testnet-explorer.robinhood.com',
    },
  },
});
