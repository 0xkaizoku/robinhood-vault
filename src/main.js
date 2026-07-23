import { MOCK_MORPHO_VAULTS, calculateProjectedYield } from './lib/services/morphoService.ts';
import { getLiveChainMetrics } from './lib/web3/client.ts';

const STRATEGIES = [
  {
    id: 's1',
    name: 'RWA Delta-Neutral Treasury Carry',
    category: 'RWA',
    tokens: 'USDC / rT-BILL',
    risk: 'Low (2/10)',
    tvl: '$18.40M',
    apy: '5.85%',
    link: 'https://app.morpho.org',
  },
  {
    id: 's2',
    name: 'Morpho ETH/wstETH 3.2x Staking Loop',
    category: 'Leveraged',
    tokens: 'WETH / wstETH',
    risk: 'Med (5/10)',
    tvl: '$12.10M',
    apy: '12.40%',
    link: 'https://app.morpho.org',
  },
  {
    id: 's3',
    name: 'Robinhood Tokenized Stock (rSPY) Covered Call',
    category: 'Yield Boost',
    tokens: 'rSPY / USDC',
    risk: 'Med (6/10)',
    tvl: '$6.80M',
    apy: '16.20%',
    link: 'https://app.morpho.org',
  },
  {
    id: 's4',
    name: 'Arbitrum Orbit Gas Subsidy Booster',
    category: 'Subsidized',
    tokens: 'USDC / ARB',
    risk: 'Low (4/10)',
    tvl: '$4.20M',
    apy: '18.50%',
    link: 'https://app.morpho.org',
  },
  {
    id: 's5',
    name: 'Fixed-Income Corporate Bond Ladder (rBOND)',
    category: 'RWA',
    tokens: 'USDC / rBOND',
    risk: 'Low (3/10)',
    tvl: '$9.30M',
    apy: '7.10%',
    link: 'https://app.morpho.org',
  },
  {
    id: 's6',
    name: 'Automated Morpho Flashloan Rebalancer',
    category: 'Algorithmic',
    tokens: 'Multi-Asset',
    risk: 'Med (5/10)',
    tvl: '$5.10M',
    apy: '11.80%',
    link: 'https://app.morpho.org',
  },
];

const ACTIVITIES = [
  { action: 'DEPOSIT', vault: 'RWA Delta-Neutral Treasury Carry', tokens: 'USDC ➔ rT-BILL', amount: '$25,400.00', account: '0x71C...39F2', time: '12s ago', hash: '0x3a8f...9b1c' },
  { action: 'SWAP', vault: 'Morpho ETH/wstETH 3.2x Staking', tokens: 'WETH ➔ wstETH', amount: '$14,200.50', account: '0x94B...81E4', time: '35s ago', hash: '0x7b2e...41a9' },
  { action: 'REBALANCE', vault: 'Automated Morpho Flashloan Rebalancer', tokens: 'USDC Vault ➔ rSPY', amount: '$89,500.00', account: '0xVaultCore_RBH', time: '1m ago', hash: '0x1c9d...66f2' },
  { action: 'CREATE', vault: 'Tokenized Stock Covered Call', tokens: 'rSPY Options Vault', amount: '$50,000.00', account: '0xA4F...1209', time: '2m ago', hash: '0x88f1...33d4' },
  { action: 'DEPOSIT', vault: 'rhALPHA Social Copy-Trading Vault', tokens: 'USDC ➔ rhALPHA', amount: '$5,200.00', account: '0x31E...99D0', time: '3m ago', hash: '0x55a2...11b8' },
];

// Live Chain Header Bar Polling
async function pollLiveMetrics() {
  const badge = document.querySelector('.brand-badge');
  const metrics = await getLiveChainMetrics();
  if (badge) {
    badge.textContent = `L2 BLOCK #${metrics.blockNumber} (${metrics.gasPriceGwei} GWEI)`;
  }
}

// Render Data Tables
function renderMarketsTable() {
  const tbody = document.getElementById('marketsTableBody');
  if (!tbody) return;

  tbody.innerHTML = MOCK_MORPHO_VAULTS.map(m => `
    <tr>
      <td style="font-weight: 600; color: #fff;">${m.name}</td>
      <td style="font-family: var(--font-mono); color: var(--blue);">${m.asset}</td>
      <td style="font-family: var(--font-mono); color: var(--text-secondary);">${m.collateralAsset}</td>
      <td style="font-family: var(--font-mono);">${m.lltv}%</td>
      <td style="font-family: var(--font-mono); font-weight: 700; color: var(--green);">${m.supplyApy.toFixed(2)}%</td>
      <td style="font-family: var(--font-mono); color: var(--text-muted);">${m.borrowApy.toFixed(2)}%</td>
      <td style="font-family: var(--font-mono);">$${(m.tvlUsd / 1e6).toFixed(2)}M</td>
      <td><span class="brand-badge" style="background: rgba(0,230,118,0.1); color: var(--green);">${m.riskRating}</span></td>
      <td style="text-align: right;">
        <a href="https://app.morpho.org" target="_blank" class="btn-action" style="text-decoration: none; display: inline-block;">View Pool ↗</a>
      </td>
    </tr>
  `).join('');
}

function renderStrategiesTable() {
  const tbody = document.getElementById('strategiesTableBody');
  if (!tbody) return;

  tbody.innerHTML = STRATEGIES.map(s => `
    <tr>
      <td style="font-weight: 600; color: #fff;">${s.name}</td>
      <td><span class="brand-badge">${s.category}</span></td>
      <td style="font-family: var(--font-mono); color: var(--text-secondary);">${s.tokens}</td>
      <td style="color: var(--text-secondary);">${s.risk}</td>
      <td style="font-family: var(--font-mono);">${s.tvl}</td>
      <td style="font-family: var(--font-mono); font-weight: 700; color: var(--green);">${s.apy}</td>
      <td style="text-align: right;">
        <a href="https://app.morpho.org" target="_blank" class="btn-action" style="text-decoration: none; display: inline-block;">Official App ↗</a>
      </td>
    </tr>
  `).join('');
}

function renderActivityTable() {
  const tbody = document.getElementById('activityTableBody');
  if (!tbody) return;

  tbody.innerHTML = ACTIVITIES.map(a => `
    <tr>
      <td>
        <span style="font-family: var(--font-mono); font-size: 0.75rem; padding: 2px 6px; border-radius: 4px; background: rgba(0,230,118,0.1); color: var(--green); border: 1px solid rgba(0,230,118,0.2);">${a.action}</span>
      </td>
      <td style="font-weight: 600; color: #fff;">${a.vault}</td>
      <td style="color: var(--text-secondary); font-family: var(--font-mono);">${a.tokens}</td>
      <td style="font-family: var(--font-mono); font-weight: 700; color: var(--green);">${a.amount}</td>
      <td style="font-family: var(--font-mono); color: var(--text-muted);">${a.account}</td>
      <td style="color: var(--text-muted); font-size: 0.8rem;">${a.time}</td>
      <td style="text-align: right;">
        <a href="https://explorer.robinhood.com" target="_blank" style="color: var(--blue); font-family: var(--font-mono); text-decoration: none;">${a.hash} ↗</a>
      </td>
    </tr>
  `).join('');
}

function initTabs() {
  const tabs = document.querySelectorAll('.tab-btn');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

      tab.classList.add('active');
      const target = tab.getAttribute('data-tab');
      const targetPane = document.getElementById(`tab-${target}`);
      if (targetPane) targetPane.classList.add('active');
    });
  });
}

function initYieldCalculator() {
  const amountInput = document.getElementById('calcAmount');
  const durationSelect = document.getElementById('calcDuration');
  const apySelect = document.getElementById('calcApy');
  const resultDiv = document.getElementById('calcResult');

  function update() {
    const amount = parseFloat(amountInput.value) || 0;
    const months = parseInt(durationSelect.value, 10);
    const apy = parseFloat(apySelect.value);

    const res = calculateProjectedYield(amount, months, apy);
    if (resultDiv) resultDiv.textContent = `$${res.projectedEarnedUsd.toLocaleString()}`;
  }

  amountInput?.addEventListener('input', update);
  durationSelect?.addEventListener('change', update);
  apySelect?.addEventListener('change', update);
}

document.addEventListener('DOMContentLoaded', () => {
  renderMarketsTable();
  renderStrategiesTable();
  renderActivityTable();
  initTabs();
  initYieldCalculator();
  pollLiveMetrics();

  setInterval(pollLiveMetrics, 6000);
});
