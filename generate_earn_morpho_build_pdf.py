#!/usr/bin/env python3
"""Generate PDF: How to build Earn/Morpho Yield Explorer + Portfolio SaaS."""

from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUT = Path(__file__).resolve().parent / "Earn_Morpho_Yield_Explorer_Build_Guide.pdf"

HOOD = colors.HexColor("#00C805")
DARK = colors.HexColor("#0D0D0D")
SLATE = colors.HexColor("#1A1A1A")
GRAY = colors.HexColor("#4A4A4A")
LIGHT = colors.HexColor("#F4F5F7")
MID = colors.HexColor("#E5E7EB")
WHITE = colors.white


def S():
    return {
        "h1": ParagraphStyle(
            "h1", fontName="Helvetica-Bold", fontSize=14, leading=18,
            textColor=DARK, spaceBefore=12, spaceAfter=7,
        ),
        "h2": ParagraphStyle(
            "h2", fontName="Helvetica-Bold", fontSize=11.5, leading=14,
            textColor=SLATE, spaceBefore=9, spaceAfter=4,
        ),
        "h3": ParagraphStyle(
            "h3", fontName="Helvetica-Bold", fontSize=10, leading=12,
            textColor=DARK, spaceBefore=7, spaceAfter=3,
        ),
        "body": ParagraphStyle(
            "body", fontName="Helvetica", fontSize=9, leading=12.5,
            textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=5,
        ),
        "bullet": ParagraphStyle(
            "bullet", fontName="Helvetica", fontSize=8.5, leading=11.5,
            textColor=DARK, leftIndent=10, spaceAfter=2,
        ),
        "caption": ParagraphStyle(
            "caption", fontName="Helvetica-Oblique", fontSize=7.5,
            leading=9.5, textColor=GRAY, spaceBefore=2, spaceAfter=7,
        ),
        "code": ParagraphStyle(
            "code", fontName="Courier", fontSize=7, leading=9.5,
            textColor=DARK, backColor=LIGHT, leftIndent=4, rightIndent=4,
            spaceBefore=4, spaceAfter=6,
        ),
        "toc": ParagraphStyle(
            "toc", fontName="Helvetica", fontSize=9.5, leading=14,
            textColor=DARK, leftIndent=4,
        ),
        "quote": ParagraphStyle(
            "quote", fontName="Helvetica-Oblique", fontSize=9, leading=12,
            textColor=SLATE, leftIndent=10, rightIndent=10,
            alignment=TA_CENTER, spaceBefore=6, spaceAfter=8,
        ),
        "small": ParagraphStyle(
            "small", fontName="Helvetica", fontSize=8, leading=10.5,
            textColor=DARK, spaceAfter=3,
        ),
    }


def hr():
    return HRFlowable(width="100%", thickness=0.6, color=MID, spaceBefore=3, spaceAfter=7)


def ghr():
    return HRFlowable(width="100%", thickness=2, color=HOOD, spaceBefore=2, spaceAfter=9)


def P(t, st):
    return Paragraph(t, st)


def tbl(headers, rows, widths=None):
    sh = ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=7.5, leading=9.5, textColor=WHITE)
    sc = ParagraphStyle("td", fontName="Helvetica", fontSize=7, leading=9.5, textColor=DARK)
    sb = ParagraphStyle("tdb", fontName="Helvetica-Bold", fontSize=7, leading=9.5, textColor=DARK)
    data = [[Paragraph(str(h), sh) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), sb if j == 0 else sc) for j, c in enumerate(row)])
    t = Table(data, colWidths=widths, repeatRows=1)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), DARK),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.35, MID),
        ("BOX", (0, 0), (-1, -1), 0.7, DARK),
    ]
    for i in range(1, len(data)):
        cmds.append(("BACKGROUND", (0, i), (-1, i), LIGHT if i % 2 == 0 else WHITE))
    t.setStyle(TableStyle(cmds))
    return t


def box(title, body):
    cell = Paragraph(
        f"<b>{title}</b><br/><br/>{body}",
        ParagraphStyle("bx", fontName="Helvetica", fontSize=8.5, leading=11.5, textColor=DARK),
    )
    t = Table([[cell]], colWidths=[6.8 * inch])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                ("BOX", (0, 0), (-1, -1), 1.2, HOOD),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    return t


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(HOOD)
    canvas.setLineWidth(2)
    canvas.line(0.65 * inch, letter[1] - 0.42 * inch, letter[0] - 0.65 * inch, letter[1] - 0.42 * inch)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(GRAY)
    canvas.drawString(0.65 * inch, letter[1] - 0.35 * inch, "Earn / Morpho Yield Explorer — Build Guide")
    canvas.drawRightString(letter[0] - 0.65 * inch, letter[1] - 0.35 * inch, "Vaults · Portfolio · Real-time data")
    canvas.setStrokeColor(MID)
    canvas.setLineWidth(0.5)
    canvas.line(0.65 * inch, 0.5 * inch, letter[0] - 0.65 * inch, 0.5 * inch)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawCentredString(letter[0] / 2, 0.32 * inch, f"Page {doc.page}")
    canvas.drawString(0.65 * inch, 0.32 * inch, "July 2026")
    canvas.drawRightString(letter[0] - 0.65 * inch, 0.32 * inch, "Not financial/legal advice")
    canvas.restoreState()


def build():
    s = S()
    story = []

    # COVER
    story.append(Spacer(1, 1.0 * inch))
    story.append(
        P(
            "●  PRODUCT #1 BUILD GUIDE",
            ParagraphStyle(
                "badge", fontName="Helvetica-Bold", fontSize=9,
                textColor=HOOD, alignment=TA_CENTER, spaceAfter=14,
            ),
        )
    )
    story.append(
        P(
            "Earn / Morpho Yield &amp; Risk Intelligence",
            ParagraphStyle(
                "t", fontName="Helvetica-Bold", fontSize=22, leading=27,
                textColor=DARK, alignment=TA_CENTER, spaceAfter=6,
            ),
        )
    )
    story.append(
        P(
            "Vault Explorer · DeFi Pools Repo · Portfolio Tracker<br/>How to Build It &amp; Keep Data Live",
            ParagraphStyle(
                "st", fontName="Helvetica", fontSize=11, leading=15,
                textColor=GRAY, alignment=TA_CENTER, spaceAfter=14,
            ),
        )
    )
    story.append(ghr())
    story.append(
        P(
            "Euler Explore–style registry for Morpho vaults, Robinhood Earn, LPs &amp; pools<br/>"
            "on Robinhood Chain — with architecture, real-time updates, costs, and roadmap",
            ParagraphStyle(
                "p", fontName="Helvetica", fontSize=9.5, leading=13,
                textColor=SLATE, alignment=TA_CENTER, spaceAfter=16,
            ),
        )
    )
    story.append(
        box(
            "What you are building",
            "A SaaS app that (1) explores Morpho vaults and yield pools like Euler Finance Explore, "
            "(2) explains Robinhood Earn risk and APY truth (base vs incentives), "
            "(3) tracks wallet portfolio positions, and (4) later expands to Uniswap LPs and other adapters — "
            "without custody and without requiring a full DeFiLlama rebuild on day one.",
        )
    )
    story.append(Spacer(1, 0.2 * inch))
    story.append(
        P(
            "<b>Reference UX:</b> https://app.euler.finance/explore?network=1<br/>"
            "<b>Chain focus:</b> Robinhood Chain (chain ID 4663) · Morpho · USDG Earn<br/>"
            "<b>Disclaimer:</b> Not financial, legal, or investment advice. Yields are variable. Geo restrictions apply.",
            s["small"],
        )
    )
    story.append(PageBreak())

    # TOC
    story.append(P("Table of Contents", s["h1"]))
    story.append(ghr())
    for item in [
        "1. Product Vision &amp; Positioning",
        "2. Scope Phases (MVP → Full Repo)",
        "3. How Euler-Style Apps Get Data",
        "4. How Real-Time Updates Work",
        "5. System Architecture",
        "6. Recommended Tech Stack",
        "7. Data Model",
        "8. Explore UX (Euler-like)",
        "9. Portfolio Tracker Design",
        "10. Risk Intelligence Features (Your Edge)",
        "11. Week-by-Week Build Plan",
        "12. Real-Time Levels (Complexity Ladder)",
        "13. Expanding Beyond Morpho (Adapters)",
        "14. Costs",
        "15. What Not to Do",
        "16. Definition of Done (v1)",
        "17. Monetization",
        "18. Distribution",
        "19. Sources &amp; Links",
        "20. Closing Checklist",
    ]:
        story.append(P(item, s["toc"]))
    story.append(PageBreak())

    # 1
    story.append(P("1. Product Vision &amp; Positioning", s["h1"]))
    story.append(ghr())
    story.append(
        P(
            "Robinhood Chain’s Earn product routes USDG into a Morpho vault (curated by Steakhouse). "
            "Retail users see a simple “~7% APY” story; underneath, rates are variable, partly incentives, "
            "with smart-contract, liquidity, curator, and stablecoin risks. Your product is the "
            "<b>intelligence and explore layer</b> — not a bank, not a new lending protocol.",
            s["body"],
        )
    )
    story.append(
        tbl(
            ["Layer", "Euler-like", "Your version"],
            [
                ["Explore", "Browse vaults/markets", "Morpho vaults, USDG Earn, later Uniswap LPs"],
                ["Detail", "One vault APY/TVL/risk", "Net APY vs incentives, utilization, curator, liquidity"],
                ["Portfolio", "Your positions", "Wallet balances, earned yield, alerts"],
            ],
            [1.3 * inch, 2.5 * inch, 3.0 * inch],
        )
    )
    story.append(P("Table: Three layers of the product shell.", s["caption"]))
    story.append(
        P(
            "You do <b>not</b> need to re-index all of DeFi on day one. Start narrow (Morpho + Robinhood Earn on RH Chain), "
            "then widen with adapters. Euler wins because it is deep on Euler vaults — not because it lists every farm on earth.",
            s["body"],
        )
    )

    # 2
    story.append(P("2. Scope Phases (MVP → Full Repo)", s["h1"]))
    story.append(ghr())
    story.append(P("Phase 1 — MVP (4–6 weeks): Robinhood Chain + Morpho only", s["h2"]))
    for b in [
        "Explore table: vault name, asset (USDG…), TVL, supply APY, net APY, rewards APY, curator, chain",
        "Vault detail: market allocations, historical APY chart, utilization / withdraw liquidity, fees, risk notes",
        "<b>Robinhood Earn spotlight</b> card (Steakhouse-curated vault users actually use)",
        "Connect wallet → my deposits in those vaults",
        "Simple alerts (APY drop, high utilization)",
    ]:
        story.append(P(f"•  {b}", s["bullet"]))

    story.append(P("Phase 2 — Portfolio tracker", s["h2"]))
    for b in [
        "All positions across vaults",
        "Cost basis / earned yield estimate",
        "CSV export",
        "Multi-wallet later",
    ]:
        story.append(P(f"•  {b}", s["bullet"]))

    story.append(P("Phase 3 — “Repo of everything”", s["h2"]))
    for b in [
        "Uniswap V3/V4 LP positions on Robinhood Chain",
        "Other lending markets as they appear on RH Chain",
        "Optional: Ethereum/Base Morpho for comparison (multi-network like Euler)",
    ]:
        story.append(P(f"•  {b}", s["bullet"]))

    story.append(
        box(
            "Scope rule",
            "Do not try to be DefiLlama + Euler + Zapper in month one. Depth on Morpho + Earn clarity is the wedge. "
            "Breadth (every LP) is a later growth feature.",
        )
    )
    story.append(PageBreak())

    # 3
    story.append(P("3. How Euler-Style Apps Get Data", s["h1"]))
    story.append(ghr())
    story.append(
        P(
            "Apps like Euler Explore do not scrape their own frontend. They combine onchain truth with hosted indexes:",
            s["body"],
        )
    )
    story.append(
        P(
            "Onchain contracts  →  Indexer / Hosted API  →  Your backend cache  →  Frontend\n"
            "     (truth)            (Morpho API / subgraph)      (Postgres)         (Explore table)",
            s["code"],
        )
    )
    story.append(
        tbl(
            ["Source", "Role", "Freshness"],
            [
                [
                    "Protocol GraphQL API (Morpho public API)",
                    "Vault lists, APY, net APY, rewards, TVL, allocations, positions",
                    "Seconds–minutes (pre-indexed)",
                ],
                [
                    "Subgraph (The Graph / Goldsky)",
                    "Events: deposits, withdraws, factory deploys",
                    "Near real-time on new blocks",
                ],
                [
                    "RPC + viem readContract",
                    "Live balances, share price, allowance for connected wallet",
                    "Live per request or poll",
                ],
                [
                    "Your database",
                    "History, favorites, alerts, curated labels (“Robinhood Earn”)",
                    "You control",
                ],
                [
                    "WebSocket / new block heads",
                    "Optional push when a new block lands",
                    "True near real-time",
                ],
            ],
            [2.2 * inch, 2.8 * inch, 1.8 * inch],
        )
    )
    story.append(P("Table: Data source stack for yield explorers.", s["caption"]))
    story.append(
        P(
            "<b>Morpho specifically</b> publishes a public Morpho API (GraphQL) so you can skip building a full indexer "
            "at first: vaults, APYs (native + rewards), positions, markets. Same idea as using Euler’s API/subgraph "
            "instead of reading every storage slot yourself. Prefer API first; add custom indexing only when RH Chain "
            "coverage is incomplete or you need custom history.",
            s["body"],
        )
    )

    # 4
    story.append(P("4. How Real-Time Updates Work", s["h1"]))
    story.append(ghr())
    story.append(
        P(
            "Nothing in retail DeFi UIs is literally continuous streaming for every table row. You combine three loops:",
            s["body"],
        )
    )

    story.append(P("A. Server refresh (catalog of vaults)", s["h2"]))
    story.append(
        P(
            "Cron or worker every <b>15–60 seconds</b>:",
            s["body"],
        )
    )
    for b in [
        "Query Morpho API: vaults on chainId <b>4663</b> (Robinhood Chain); optional Ethereum for comparison",
        "Normalize fields: address, symbol, asset, tvlUsd, apy, netApy, netApyExcludingRewards, rewards[], curator, fees",
        "Upsert into Postgres",
        "Frontend reads <b>your</b> API (fast, stable, cacheable — browsers never hammer Morpho directly)",
    ]:
        story.append(P(f"•  {b}", s["bullet"]))
    story.append(
        P(
            "This is how Explore stays “live” without rate-limit meltdown.",
            s["body"],
        )
    )

    story.append(P("B. User portfolio (more live)", s["h2"]))
    story.append(P("When a wallet is connected:", s["body"]))
    for b in [
        "<b>On page load:</b> balanceOf, vault convertToAssets, market positions via API or contracts",
        "<b>Poll every 10–30s</b> while tab is open (SWR / React Query refetchInterval)",
        "<b>On new block (optional):</b> Alchemy/WebSocket newHeads → invalidate queries",
        "<b>On user tx:</b> after deposit/withdraw receipt → immediate refetch",
    ]:
        story.append(P(f"•  {b}", s["bullet"]))

    story.append(P("C. What is never real-time without extra work", s["h2"]))
    for b in [
        "Historical charts → stored snapshots (cron writes APY/TVL every 5–15 min)",
        "Incentives / Merkl-style rewards → Morpho rewards fields and/or reward APIs",
        "Labels (“Robinhood Earn”, “deprecated”, “verified”) → your curated tables (like Euler known-vault metadata)",
    ]:
        story.append(P(f"•  {b}", s["bullet"]))

    story.append(P("Update interval cheat sheet", s["h2"]))
    story.append(
        tbl(
            ["Data", "Update method", "Interval"],
            [
                ["Vault list + TVL + APY", "Backend poll Morpho API", "30–60s"],
                ["Wallet shares / positions", "Frontend + RPC (and/or Morpho positions API)", "10–15s or on block"],
                ["Charts / history", "DB snapshots", "5–15 min"],
                ["Alerts", "Backend compare new APY vs threshold", "Same as catalog poll"],
                ["Prices (ETH, USDG)", "Chainlink / price API", "15–60s"],
            ],
            [2.2 * inch, 2.8 * inch, 1.8 * inch],
        )
    )
    story.append(P("Table: Practical freshness targets for MVP.", s["caption"]))
    story.append(PageBreak())

    # 5
    story.append(P("5. System Architecture", s["h1"]))
    story.append(ghr())
    story.append(
        P(
            "┌─────────────────────────────────────────────────────────┐\n"
            "│  Next.js App (Explore | Vault | Portfolio | Alerts)     │\n"
            "│  wagmi/viem + wallet connect + SWR/React Query            │\n"
            "└──────────────────────────┬──────────────────────────────┘\n"
            "                           │ REST / tRPC\n"
            "┌──────────────────────────▼──────────────────────────────┐\n"
            "│  API (Node / Next route handlers)                         │\n"
            "│  GET /vaults?chain=4663  ·  GET /vaults/:address           │\n"
            "│  GET /portfolio/:wallet  ·  POST /alerts                   │\n"
            "└───────────┬───────────────────────────┬─────────────────┘\n"
            "            │                           │\n"
            "            ▼                           ▼\n"
            "     Postgres + Redis              Morpho GraphQL API\n"
            "     (cache, history, labels)      + RH RPC (Alchemy)\n"
            "            ▲\n"
            "            │\n"
            "     Worker (every 30s)\n"
            "     morpho sync → upsert vaults → evaluate alerts",
            s["code"],
        )
    )
    story.append(
        P(
            "Browsers talk only to your API. Workers own external protocol APIs. RPC is used for wallet-specific "
            "truth and write previews — not for scanning all vaults every second from the client.",
            s["body"],
        )
    )

    # 6
    story.append(P("6. Recommended Tech Stack", s["h1"]))
    story.append(ghr())
    story.append(
        tbl(
            ["Piece", "Choice", "Why"],
            [
                ["Frontend", "Next.js App Router + Tailwind", "Fast ship; Euler-like tables/filters"],
                ["Chain reads", "viem", "Modern, typed; RH Chain EVM"],
                ["Wallet", "wagmi or Privy", "wagmi simple; Privy if social login later"],
                ["Catalog data", "Morpho public GraphQL API first", "Skip full indexer initially"],
                ["RPC", "Alchemy Robinhood mainnet", "Recommended by RH docs; AA later"],
                ["DB", "Postgres (Supabase / Neon)", "Vaults, snapshots, alerts"],
                ["Cache", "Redis (optional early)", "Portfolio keys, rate-limit protection"],
                ["Jobs", "node-cron, Inngest, or Railway worker", "30s vault sync"],
                ["Auth (optional)", "Privy / Clerk / NextAuth", "Only for saved alerts &amp; Pro"],
                ["Payments", "Stripe", "Pro tier $10–20/mo"],
                ["Hosting", "Vercel (FE) + Railway (worker/API)", "Common indie pattern"],
            ],
            [1.3 * inch, 2.3 * inch, 3.2 * inch],
        )
    )
    story.append(P("Table: Stack choices aligned with RH Chain and solo/small-team speed.", s["caption"]))

    # 7
    story.append(P("7. Data Model", s["h1"]))
    story.append(ghr())
    story.append(
        P(
            "chains(id, name, chain_id)\n\n"
            "vaults(\n"
            "  address, chain_id, name, symbol, asset_address, asset_symbol,\n"
            "  curator, tvl_usd, apy, net_apy, net_apy_ex_rewards,\n"
            "  rewards_apy, performance_fee, management_fee,\n"
            "  is_verified, tags[], updated_at\n"
            ")\n\n"
            "vault_snapshots(vault_id, tvl_usd, net_apy, ts)  -- charts\n"
            "vault_labels(vault_id, label)  -- robinhood-earn, steakhouse\n"
            "user_watchlists(user_id, vault_id)\n"
            "alerts(user_id, vault_id, type, threshold, channel, active)",
            s["code"],
        )
    )
    story.append(P("Curated seed (critical for positioning)", s["h2"]))
    story.append(
        P(
            "Tag the official <b>Robinhood Earn / Steakhouse Morpho vault</b> as <font face='Courier'>robinhood-earn</font>. "
            "Show incentive vs base APY clearly. That split is your product edge over a raw Morpho UI or a generic yield list.",
            s["body"],
        )
    )
    story.append(PageBreak())

    # 8
    story.append(P("8. Explore UX (Euler-like)", s["h1"]))
    story.append(ghr())
    story.append(
        P(
            "Copy the <b>interaction pattern</b> of Euler Explore, not the brand. Reference: "
            "https://app.euler.finance/explore?network=1",
            s["body"],
        )
    )
    for b in [
        "<b>Network selector</b> — start with Robinhood Chain (4663); optional Ethereum later",
        "<b>Filters</b> — asset (USDG), curator, min TVL, has rewards, verified only",
        "<b>Sort</b> — net APY, TVL, name, recently updated",
        "<b>Columns</b> — Asset | Vault | TVL | Base APY | Rewards | Net APY | Curator | Risk tag",
        "<b>Row click</b> → vault detail page",
        "<b>Connect wallet</b> → “Your deposits” column and/or Portfolio tab",
    ]:
        story.append(P(f"•  {b}", s["bullet"]))
    story.append(
        P(
            "Mobile: sticky filters collapsed; horizontal scroll on table or card list. "
            "Empty states when RH Morpho listing is thin — show “verified Earn vault” first.",
            s["body"],
        )
    )

    # 9
    story.append(P("9. Portfolio Tracker Design", s["h1"]))
    story.append(ghr())
    story.append(
        P(
            "User connects wallet\n"
            "  → API: Morpho positions-by-user (if available for chain)\n"
            "  → OR loop known vault addresses: convertToAssets(balanceOf(user))\n"
            "  → Cache ~15s in Redis keyed by wallet+chain\n"
            "  → UI polls every 15s + refetch on window focus + refetch after tx",
            s["code"],
        )
    )
    story.append(P("PnL (good enough v1)", s["h2"]))
    for b in [
        "Earned ≈ current assets − net deposits (from Deposit/Withdraw events or share delta over time)",
        "Store first-seen balance snapshot when user links wallet",
        "Do not promise tax-grade accuracy until full historical indexing exists",
        "CSV export of positions + timestamps for accountants (Pro feature)",
    ]:
        story.append(P(f"•  {b}", s["bullet"]))

    # 10
    story.append(P("10. Risk Intelligence Features (Your Edge)", s["h1"]))
    story.append(ghr())
    story.append(
        P(
            "A plain vault table is a commodity. Your SaaS sells <b>clarity</b>:",
            s["body"],
        )
    )
    story.append(
        tbl(
            ["Feature", "What user learns", "Data source"],
            [
                ["Base vs rewards APY", "How much of 7% is temporary incentives", "netApy vs netApyExcludingRewards"],
                ["Utilization / liquidity", "Can I withdraw right now?", "Morpho market/vault state"],
                ["Fee drag", "What curator/protocol takes", "performanceFee, managementFee"],
                ["Curator label", "Who sets risk parameters (e.g. Steakhouse)", "API + your labels"],
                ["Incentive end scenarios", "What if rewards go to zero?", "Computed from fields above"],
                ["Plain-language risks", "Smart contract, peg, liquidity, curator", "Your content + RH disclosures"],
                ["Alerts", "Notify when APY drops or util spikes", "Your worker + user settings"],
            ],
            [1.7 * inch, 2.6 * inch, 2.5 * inch],
        )
    )
    story.append(P("Table: Differentiated risk intelligence features.", s["caption"]))
    story.append(
        P(
            "Never market yields as guaranteed. Never imply FDIC/SIPC. Robinhood’s insurance (Lloyd’s/RELM) is not a "
            "personal user policy and does not cover market/lending losses — reflect that honestly.",
            s["body"],
        )
    )

    # 11
    story.append(P("11. Week-by-Week Build Plan", s["h1"]))
    story.append(ghr())
    story.append(
        tbl(
            ["Week", "Ship"],
            [
                [
                    "1",
                    "Next.js shell, RH Chain wallet connect, hardcode 1–3 vault addresses (Earn vault), "
                    "live APY/TVL via Morpho API or contracts",
                ],
                [
                    "2",
                    "Explore table from API sync worker + Postgres; vault detail page; charts from snapshots",
                ],
                [
                    "3",
                    "Portfolio: wallet positions; deep-link deposit/withdraw to Morpho or Robinhood; no custody",
                ],
                [
                    "4",
                    "Alerts (email/Telegram); Robinhood Earn explainer module; Pro feature flag",
                ],
                [
                    "5–6",
                    "Polish filters, mobile, SEO landing; optional Uniswap LP positions; Stripe $10–15/mo",
                ],
            ],
            [0.8 * inch, 6.0 * inch],
        )
    )
    story.append(P("Table: 4–6 week path to a chargeable MVP.", s["caption"]))
    story.append(PageBreak())

    # 12
    story.append(P("12. Real-Time Levels (Complexity Ladder)", s["h1"]))
    story.append(ghr())
    story.append(
        tbl(
            ["Level", "What users feel", "How", "When"],
            [
                ["1 — Good enough", "Updates every ~30s", "Cron + SWR poll", "<b>Start here</b>"],
                ["2 — Snappy", "Wallet updates every block", "WebSocket newHeads + invalidate", "After MVP"],
                ["3 — Pro", "Live activity feed", "Index Deposit/Withdraw events + WS to clients", "Growth"],
                ["4 — Full Zapper", "Every protocol", "Multi-protocol adapters + heavy indexing", "Funded / late"],
            ],
            [1.2 * inch, 1.6 * inch, 2.4 * inch, 1.6 * inch],
        )
    )
    story.append(
        P(
            "For MVP, Levels 1–2 match “feels live” like Euler without insane infra cost.",
            s["caption"],
        )
    )

    # 13
    story.append(P("13. Expanding Beyond Morpho (Adapters)", s["h1"]))
    story.append(ghr())
    story.append(
        P(
            "Keep Explore clean with a protocol adapter interface:",
            s["body"],
        )
    )
    story.append(
        P(
            "interface YieldAdapter {\n"
            "  protocol: 'morpho' | 'uniswap' | 'euler' | ...\n"
            "  listPools(chainId: number): Promise&lt;PoolRow[]&gt;\n"
            "  getUserPositions(chainId: number, user: Address): Promise&lt;Position[]&gt;\n"
            "}",
            s["code"],
        )
    )
    story.append(
        tbl(
            ["Adapter", "Data source", "Phase"],
            [
                ["Morpho", "Morpho GraphQL API + contracts", "Phase 1"],
                ["Uniswap LP", "Subgraph / position NFTs + pool state", "Phase 3"],
                ["Generic ERC-4626", "Factory events + totalAssets / convertToAssets", "Phase 3"],
                ["Euler (optional multi-chain)", "Euler API / subgraphs", "Only if multi-network"],
            ],
            [1.5 * inch, 3.3 * inch, 2.0 * inch],
        )
    )
    story.append(P("Table: Adapter roadmap — Morpho first.", s["caption"]))

    # 14
    story.append(P("14. Costs", s["h1"]))
    story.append(ghr())
    story.append(
        tbl(
            ["Item", "MVP", "Growing", "Notes"],
            [
                ["Hosting + DB", "$20–80/mo", "$100–400/mo", "Vercel/Railway/Supabase"],
                ["Alchemy RPC", "$0–50/mo", "$200+/mo", "Scales with portfolio polls"],
                ["Morpho API", "Free public", "Free (cache!)", "Respect rate limits via backend"],
                ["Telegram / email", "$0–20/mo", "$50+/mo", "Alerts"],
                ["Stripe fees", "2.9% + fixed", "Same", "On subscriptions"],
                ["Domain / email", "$20–50/yr", "—", "One-time-ish"],
                ["Legal ToS/disclaimer", "$0–1k", "$2–5k", "Templates then lawyer"],
                ["Smart contract audit", "$0", "Only if you add deposit contracts", "Stay read-only first"],
                ["Cash to launch (you code)", "$500–3k", "—", "No salaries included"],
                ["12-month opex (indie)", "$1–5k", "$5–15k", "Before paid ads"],
            ],
            [1.7 * inch, 1.2 * inch, 1.5 * inch, 2.4 * inch],
        )
    )
    story.append(P("Table: Cost ranges for this product specifically.", s["caption"]))

    # 15
    story.append(P("15. What Not to Do", s["h1"]))
    story.append(ghr())
    for b in [
        "Do not build a full custom subgraph before trying Morpho’s public API",
        "Do not promise “7% guaranteed” — always show base vs rewards",
        "Do not custody user funds or keys",
        "Do not list 500 random farms day one — curation is a feature",
        "Do not fire 50 parallel RPC calls from the browser for the Explore table",
        "Do not imply affiliation with Robinhood, Morpho, or Steakhouse without permission",
        "Do not skip geo/eligibility disclaimers (Earn and products vary by region)",
        "Do not add a custom fee-routing contract until revenue justifies a $15–40k audit",
    ]:
        story.append(P(f"•  {b}", s["bullet"]))

    # 16
    story.append(P("16. Definition of Done (v1)", s["h1"]))
    story.append(ghr())
    story.append(
        P(
            "You are live when all of the following are true:",
            s["body"],
        )
    )
    for i, b in enumerate(
        [
            "Explore lists Morpho vaults on RH Chain (or at least Earn + top vaults) with APY/TVL refreshing ≤ 1 minute",
            "Vault page explains risk + incentive split better than Robinhood’s simple Earn screen",
            "Connected wallet shows my position updating within ~15 seconds",
            "At least one alert type works (e.g. net APY below threshold)",
            "Public URL + Stripe Pro ($10–15/mo) for alerts and history",
            "Clear disclaimers: not advice, yields variable, not FDIC/SIPC",
        ],
        1,
    ):
        story.append(P(f"<b>{i}.</b>  {b}", s["bullet"]))
    story.append(PageBreak())

    # 17
    story.append(P("17. Monetization", s["h1"]))
    story.append(ghr())
    story.append(
        tbl(
            ["Tier", "Price (example)", "Includes"],
            [
                ["Free", "$0", "Explore, basic vault detail, 1 wallet snapshot"],
                ["Pro", "$10–20/mo", "Alerts, history charts, multi-wallet, CSV export"],
                ["API (later)", "$49–499/mo", "Vault snapshots API for bots/creators"],
                ["Affiliate (optional)", "Revshare", "Deep-links to venues — disclose clearly"],
            ],
            [1.3 * inch, 1.5 * inch, 4.0 * inch],
        )
    )
    story.append(
        P(
            "Example: 200 Pro users × $12 = $2,400 MRR. Monetize insight and alerts — never “guaranteed yield.”",
            s["caption"],
        )
    )

    # 18
    story.append(P("18. Distribution", s["h1"]))
    story.append(ghr())
    story.append(
        tbl(
            ["Channel", "Tactic"],
            [
                ["SEO", "“How Robinhood Earn APY works”, “Morpho vault risks”, “USDG lend explained”"],
                ["X / CT", "Live APY breakdown posts when rates move; dashboards not memecoins"],
                ["YouTube", "Walkthrough: Earn under the hood + your dashboard"],
                ["Reddit", "Answer Earn risk questions carefully (no spam)"],
                ["RH ecosystem", "Email chain-developers-group@robinhood.com with live metrics"],
                ["Arbitrum", "Open House prizes + Foundation grants for retail transparency tooling"],
                ["In-product", "Shareable “vault health” cards"],
            ],
            [1.4 * inch, 5.4 * inch],
        )
    )
    story.append(P("Table: Distribution map for this product.", s["caption"]))

    # 19
    story.append(P("19. Sources &amp; Links", s["h1"]))
    story.append(ghr())
    for b in [
        "Euler Explore (UX reference): https://app.euler.finance/explore?network=1",
        "Euler data docs (subgraphs, APIs, patterns): docs.euler.finance developers data-querying",
        "Morpho API / vaults GraphQL: docs.morpho.org (developers API, earn get-data tutorials)",
        "Morpho: “Skip Indexing, Start Building” API blog — vault APY, positions, TVL queries",
        "Robinhood Chain docs: https://docs.robinhood.com/chain/",
        "Robinhood Earn support / disclosures: robinhood.com support crypto-earn",
        "Network: Robinhood Chain mainnet chain ID 4663; Alchemy recommended RPC",
        "Developer contact: chain-developers-group@robinhood.com",
        "Arbitrum Open House: openhouse.arbitrum.io · Grants: arbitrum.foundation/grants",
    ]:
        story.append(P(f"•  {b}", s["bullet"]))

    # 20
    story.append(P("20. Closing Checklist", s["h1"]))
    story.append(ghr())
    story.append(
        tbl(
            ["Question", "Answer"],
            [
                ["Is this like Euler Explore?", "Yes — vault registry + filters + portfolio"],
                ["How do pools stay updated?", "Backend poll Morpho API → DB every 30–60s; wallet via RPC poll / new block"],
                ["Is it real-time?", "Near real-time (seconds–minute), not millisecond trading"],
                ["Where to start?", "Morpho + Robinhood Earn on chain 4663 only"],
                ["Portfolio?", "Same app, tab 2 — positions from API + balanceOf"],
                ["Custody?", "None — read-only intelligence + optional deep-links"],
                ["Audit needed for v1?", "No, if you stay read-only"],
                ["First revenue?", "Pro alerts + history via Stripe"],
            ],
            [2.2 * inch, 4.6 * inch],
        )
    )
    story.append(P("Table: One-page summary answers.", s["caption"]))

    story.append(Spacer(1, 0.15 * inch))
    story.append(ghr())
    story.append(
        P(
            "Build the Morpho + Earn intelligence layer first. Make Explore feel as clear as Euler. "
            "Keep data fresh with a simple worker + wallet polling. Charge for alerts and portfolio history. "
            "Expand to LPs and multi-protocol only after users pay for the core job.",
            s["quote"],
        )
    )
    story.append(
        P(
            "— End of build guide —",
            ParagraphStyle(
                "end", fontName="Helvetica-Oblique", fontSize=9,
                textColor=GRAY, alignment=TA_CENTER, spaceBefore=12,
            ),
        )
    )
    story.append(
        P(
            "For product planning only. Yields, APIs, and chain integrations change. "
            "Re-verify Morpho API fields and Robinhood Earn vault addresses before production.",
            ParagraphStyle(
                "end2", fontName="Helvetica", fontSize=7.5, leading=10,
                textColor=GRAY, alignment=TA_CENTER, spaceBefore=6,
            ),
        )
    )

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        leftMargin=0.65 * inch,
        rightMargin=0.65 * inch,
        topMargin=0.58 * inch,
        bottomMargin=0.62 * inch,
        title="Earn Morpho Yield Explorer Build Guide",
        author="Product Build Guide",
        subject="How to build vault explorer portfolio tracker with real-time updates",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Wrote: {OUT}")
    return OUT


if __name__ == "__main__":
    build()
