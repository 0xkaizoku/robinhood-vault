#!/usr/bin/env python3
"""Generate comprehensive Robinhood Chain viable products PDF."""

from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
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

OUT = Path(__file__).resolve().parent / "Robinhood_Chain_Viable_Products_Guide.pdf"

HOOD_GREEN = colors.HexColor("#00C805")
DARK = colors.HexColor("#0D0D0D")
SLATE = colors.HexColor("#1A1A1A")
GRAY = colors.HexColor("#4A4A4A")
LIGHT_GRAY = colors.HexColor("#F4F5F7")
MID_GRAY = colors.HexColor("#E5E7EB")
WHITE = colors.white
EASY = colors.HexColor("#059669")
MED = colors.HexColor("#D97706")
HARD = colors.HexColor("#DC2626")
BLUE = colors.HexColor("#2563EB")


def styles():
    base = getSampleStyleSheet()
    return {
        "h1": ParagraphStyle(
            "h1", fontName="Helvetica-Bold", fontSize=15, leading=19,
            textColor=DARK, spaceBefore=14, spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "h2", fontName="Helvetica-Bold", fontSize=12, leading=15,
            textColor=SLATE, spaceBefore=10, spaceAfter=5,
        ),
        "h3": ParagraphStyle(
            "h3", fontName="Helvetica-Bold", fontSize=10.5, leading=13,
            textColor=DARK, spaceBefore=8, spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body", fontName="Helvetica", fontSize=9, leading=12.5,
            textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=5,
        ),
        "bullet": ParagraphStyle(
            "bullet", fontName="Helvetica", fontSize=9, leading=12,
            textColor=DARK, leftIndent=10, spaceAfter=2,
        ),
        "caption": ParagraphStyle(
            "caption", fontName="Helvetica-Oblique", fontSize=7.5,
            leading=9.5, textColor=GRAY, spaceBefore=2, spaceAfter=8,
        ),
        "quote": ParagraphStyle(
            "quote", fontName="Helvetica-Oblique", fontSize=9.5, leading=13,
            textColor=SLATE, leftIndent=12, rightIndent=12,
            spaceBefore=6, spaceAfter=8, alignment=TA_CENTER,
        ),
        "toc": ParagraphStyle(
            "toc", fontName="Helvetica", fontSize=9.5, leading=15,
            textColor=DARK, leftIndent=6,
        ),
        "small": ParagraphStyle(
            "small", fontName="Helvetica", fontSize=8, leading=10.5,
            textColor=DARK, spaceAfter=3,
        ),
        "badge": ParagraphStyle(
            "badge", fontName="Helvetica-Bold", fontSize=8, leading=10,
            textColor=HOOD_GREEN, alignment=TA_CENTER, spaceAfter=12,
        ),
        "title": ParagraphStyle(
            "title", fontName="Helvetica-Bold", fontSize=26, leading=32,
            textColor=DARK, alignment=TA_CENTER, spaceAfter=6,
        ),
        "subtitle": ParagraphStyle(
            "subtitle", fontName="Helvetica", fontSize=12, leading=16,
            textColor=GRAY, alignment=TA_CENTER, spaceAfter=14,
        ),
        "rank": ParagraphStyle(
            "rank", fontName="Helvetica-Bold", fontSize=11, leading=14,
            textColor=DARK, spaceBefore=6, spaceAfter=4,
        ),
    }


def green_hr():
    return HRFlowable(
        width="100%", thickness=2, color=HOOD_GREEN, spaceBefore=2, spaceAfter=10
    )


def hr():
    return HRFlowable(
        width="100%", thickness=0.6, color=MID_GRAY, spaceBefore=4, spaceAfter=8
    )


def p(text, style):
    return Paragraph(text, style)


def make_table(headers, rows, col_widths=None):
    s_h = ParagraphStyle(
        "th", fontName="Helvetica-Bold", fontSize=7.5, leading=9.5, textColor=WHITE
    )
    s_c = ParagraphStyle(
        "td", fontName="Helvetica", fontSize=7, leading=9.5, textColor=DARK
    )
    s_cb = ParagraphStyle(
        "tdb", fontName="Helvetica-Bold", fontSize=7, leading=9.5, textColor=DARK
    )
    data = [[Paragraph(str(h), s_h) for h in headers]]
    for row in rows:
        cells = []
        for j, cell in enumerate(row):
            cells.append(Paragraph(str(cell), s_cb if j == 0 else s_c))
        data.append(cells)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), DARK),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.35, MID_GRAY),
        ("BOX", (0, 0), (-1, -1), 0.7, DARK),
    ]
    for i in range(1, len(data)):
        cmds.append(
            ("BACKGROUND", (0, i), (-1, i), LIGHT_GRAY if i % 2 == 0 else WHITE)
        )
    t.setStyle(TableStyle(cmds))
    return t


def callout_box(title, body_text, s):
    cell = Paragraph(
        f"<b>{title}</b><br/><br/>{body_text}",
        ParagraphStyle(
            "callout", fontName="Helvetica", fontSize=8.5, leading=11.5, textColor=DARK
        ),
    )
    t = Table([[cell]], colWidths=[6.8 * inch])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
                ("BOX", (0, 0), (-1, -1), 1.2, HOOD_GREEN),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    return t


def product_card(story, s, num, name, difficulty, rev, dist, effort, cash, opex, one_liner, what, why, pays, build, costs_rows, rev_detail, dist_detail, risks, score):
    story.append(p(f"{num}. {name}", s["h2"]))
    story.append(
        make_table(
            ["Difficulty", "Revenue potential", "Distribution", "Build effort", "Cash to launch", "12-mo opex"],
            [[difficulty, rev, dist, effort, cash, opex]],
            col_widths=[1.05 * inch, 1.15 * inch, 1.1 * inch, 1.0 * inch, 1.2 * inch, 1.1 * inch],
        )
    )
    story.append(p(f"<b>Composite score:</b> {score} &nbsp;|&nbsp; <i>{one_liner}</i>", s["caption"]))
    story.append(p("<b>What to build</b>", s["h3"]))
    story.append(p(what, s["body"]))
    story.append(p("<b>Why it fits Robinhood Chain</b>", s["h3"]))
    story.append(p(why, s["body"]))
    story.append(p("<b>Who pays / revenue model</b>", s["h3"]))
    story.append(p(pays, s["body"]))
    story.append(p(rev_detail, s["small"]))
    story.append(p("<b>Distribution strategy</b>", s["h3"]))
    story.append(p(dist_detail, s["body"]))
    story.append(p("<b>Build shape</b>", s["h3"]))
    story.append(p(build, s["body"]))
    story.append(p("<b>Cost breakdown</b>", s["h3"]))
    story.append(
        make_table(
            ["Item", "Low / MVP", "Solid v1"],
            costs_rows,
            col_widths=[2.4 * inch, 2.2 * inch, 2.2 * inch],
        )
    )
    story.append(p("<b>Main risks</b>", s["h3"]))
    story.append(p(risks, s["body"]))
    story.append(hr())


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(HOOD_GREEN)
    canvas.setLineWidth(2)
    canvas.line(0.65 * inch, letter[1] - 0.42 * inch, letter[0] - 0.65 * inch, letter[1] - 0.42 * inch)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(GRAY)
    canvas.drawString(0.65 * inch, letter[1] - 0.35 * inch, "Robinhood Chain — Viable Products Guide")
    canvas.drawRightString(letter[0] - 0.65 * inch, letter[1] - 0.35 * inch, "Easy → Hard · Revenue · Dist · Costs")
    canvas.setStrokeColor(MID_GRAY)
    canvas.setLineWidth(0.5)
    canvas.line(0.65 * inch, 0.52 * inch, letter[0] - 0.65 * inch, 0.52 * inch)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawCentredString(letter[0] / 2, 0.32 * inch, f"Page {doc.page}")
    canvas.drawString(0.65 * inch, 0.32 * inch, "July 2026 · Research synthesis")
    canvas.drawRightString(letter[0] - 0.65 * inch, 0.32 * inch, "Not financial/legal advice")
    canvas.restoreState()


def build():
    s = styles()
    story = []

    # COVER
    story.append(Spacer(1, 1.1 * inch))
    story.append(p("●  ROBINHOOD CHAIN PRODUCT STRATEGY", s["badge"]))
    story.append(p("Viable Products Guide", s["title"]))
    story.append(
        p(
            "Sorted Easy → Hard · Revenue Potential · Distribution · Full Costs",
            s["subtitle"],
        )
    )
    story.append(green_hr())
    story.append(
        p(
            "Stock Tokens / RWAs · Earn / Lending · Wallet Distribution · Trading · Agents",
            ParagraphStyle(
                "pillars", fontName="Helvetica", fontSize=10, leading=14,
                textColor=SLATE, alignment=TA_CENTER, spaceAfter=18,
            ),
        )
    )
    story.append(
        callout_box(
            "Thesis",
            "Robinhood Chain’s real opportunity is not generic social media. It is tokenized stocks and RWAs, "
            "USDG Earn via Morpho, Wallet distribution into ~28M brokerage users, trading venues (Uniswap, Lighter, Arcus), "
            "and AI agents (MCP + onchain AA). This guide ranks products by difficulty, revenue, distribution leverage, and cost.",
            s,
        )
    )
    story.append(Spacer(1, 0.25 * inch))
    story.append(
        p(
            "<b>Compiled:</b> July 2026 &nbsp;·&nbsp; <b>Audience:</b> Solo builders &amp; small teams &nbsp;·&nbsp; "
            "<b>Mainnet:</b> ~July 1, 2026 (early ecosystem)<br/>"
            "<b>Disclaimer:</b> Not financial, legal, or investment advice. Stock Tokens, Earn, and agents are geo-restricted. "
            "Costs are industry estimates. Verify on official docs before building.",
            s["small"],
        )
    )
    story.append(PageBreak())

    # TOC
    story.append(p("Table of Contents", s["h1"]))
    story.append(green_hr())
    for item in [
        "1. How to Read This Guide (Scoring System)",
        "2. Chain Thesis &amp; Market Context",
        "3. Master Ranking Matrix (Easy → Hard)",
        "4. Product Deep Dives (1–10)",
        "5. Cost Reference Tables (Infra, Audits, People, GTM)",
        "6. Distribution Playbook",
        "7. Recommended Paths by Budget &amp; Skills",
        "8. 90-Day Default Roadmap",
        "9. Regulatory &amp; Landmine Checklist",
        "10. Sources &amp; Further Links",
    ]:
        story.append(p(item, s["toc"]))
    story.append(PageBreak())

    # 1 SCORING
    story.append(p("1. How to Read This Guide (Scoring System)", s["h1"]))
    story.append(green_hr())
    story.append(
        p(
            "Products are ordered primarily by <b>difficulty (easy → hard)</b>. Within similar difficulty, higher "
            "<b>revenue potential</b> and better <b>distribution fit</b> rank higher. Composite scores are judgment "
            "scores for a small team (solo to 3 people), not market caps.",
            s["body"],
        )
    )
    story.append(
        make_table(
            ["Dimension", "Scale", "What it means"],
            [
                ["Difficulty", "1–5 (Easy→Hard)", "Tech complexity, contracts, oracles, ops, compliance load"],
                ["Revenue potential", "1–5", "Ability to charge (SaaS, fees, AUM share) at modest scale"],
                ["Distribution", "1–5", "Fit with RH Wallet, Earn, ST, CT, SEO, partnerships"],
                ["Cash to launch", "USD", "Out-of-pocket if founder codes; not full founder salary"],
                ["12-mo opex", "USD", "Hosting, RPC, tools, light marketing, basic legal"],
                ["Time to MVP", "Weeks", "Solo full-stack baseline"],
            ],
            col_widths=[1.5 * inch, 1.5 * inch, 3.8 * inch],
        )
    )
    story.append(p("Table: Scoring dimensions used throughout this guide.", s["caption"]))
    story.append(
        p(
            "<b>Rule of thumb:</b> Prefer products with Difficulty ≤ 2 and Revenue ≥ 3 for first revenue. "
            "Only take Difficulty ≥ 4 after revenue or funding covers audits ($40k–$150k+).",
            s["body"],
        )
    )

    # 2 CONTEXT
    story.append(p("2. Chain Thesis &amp; Market Context", s["h1"]))
    story.append(green_hr())
    story.append(
        make_table(
            ["Pillar", "What is live", "Builder open surface"],
            [
                [
                    "Stock Tokens / RWAs",
                    "Tokenized equity exposure (Jersey debt securities); 24/7 onchain for eligible non-US; US persons excluded",
                    "Portfolio, tax/PnL, routing, collateral UX, analytics, eligibility UX",
                ],
                [
                    "Earn / lending",
                    "USDG → self-custody (Privy TEE) → Morpho vault (Steakhouse); ~7% est. APY = base + incentives; not FDIC/SIPC",
                    "Risk dashboards, APY truth, alerts, power Morpho UI, borrow UX",
                ],
                [
                    "Wallet distribution",
                    "~28M brokerage funnel; Wallet + in-app self-custody; AA (ERC-4337); early gas sponsorship narrative",
                    "Gasless onboarding, deep links, first DeFi action products",
                ],
                [
                    "Trading",
                    "Uniswap, Pleiades/Rialto, Lighter perps, Arcus, 1inch-style routing",
                    "Best-execution UI, ST-specific tools, alerts, copy desks",
                ],
                [
                    "Agents",
                    "Brokerage Agentic Trading via MCP; chain marketed AI-native for onchain ST/lend/swap",
                    "Strategy packs, risk wrappers, onchain AA agents with caps",
                ],
            ],
            col_widths=[1.3 * inch, 2.9 * inch, 2.6 * inch],
        )
    )
    story.append(p("Table: Official thesis pillars and where third-party builders still fit.", s["caption"]))

    story.append(p("Critical geo split", s["h2"]))
    story.append(
        p(
            "<b>US users:</b> Earn / USDG / Morpho path is the hot wedge; Stock Tokens generally unavailable. "
            "<b>Non-US eligible users:</b> Stock Tokens + DeFi composability is the hot wedge. "
            "Design products with jurisdiction gates; do not assume one UX for everyone.",
            s["body"],
        )
    )
    story.append(
        p(
            "Official Earn mechanics: users buy USDG, move to self-custody wallet, lend via Morpho curated by Steakhouse. "
            "APY is variable; community analysis has split headline ~7% into protocol APR + Merkl-style incentives. "
            "Insurance (Lloyd’s/RELM) covers Robinhood for certain technical events — not a personal user policy, not market risk.",
            s["body"],
        )
    )
    story.append(PageBreak())

    # 3 MASTER MATRIX
    story.append(p("3. Master Ranking Matrix (Easy → Hard)", s["h1"]))
    story.append(green_hr())
    story.append(
        p(
            "Sorted by difficulty ascending. Revenue and distribution scored 1–5. "
            "“Best first bet” products are highlighted in the deep dives.",
            s["body"],
        )
    )
    story.append(
        make_table(
            ["#", "Product", "Diff", "Rev", "Dist", "MVP cash", "MVP time", "Contracts?", "Best for"],
            [
                ["1", "Earn / Morpho yield &amp; risk intelligence SaaS", "1", "4", "5", "$0.5–3k", "3–6 wks", "No", "US / Earn"],
                ["2", "Stock Token portfolio + tax/PnL tracker", "2", "4", "4", "$0.5–5k", "4–8 wks", "No", "Non-US ST"],
                ["3", "ST + USDG swap / best-execution UI", "2", "4", "4", "$0.5–8k", "3–6 wks", "Optional", "Volume fees"],
                ["4", "Alerts, watchlists, ST/Earn notifier", "1", "3", "4", "$0.3–2k", "2–4 wks", "No", "Quick ship"],
                ["5", "Agent strategy packs + risk monitor (MCP)", "2–3", "3", "4", "$1–10k", "4–8 wks", "No (ph1)", "AI narrative"],
                ["6", "Morpho power-user frontend", "3", "3", "3", "$3–15k", "6–10 wks", "No", "DeFi natives"],
                ["7", "Copy desk / social trading (not keys)", "3–4", "4", "3", "$5–25k+", "8–14 wks", "Optional", "Trading brand"],
                ["8", "Onchain AA agent executor", "4", "4", "3", "$40–120k", "3–6 mo", "Yes + audit", "Funded team"],
                ["9", "Morpho curator / own vault brand", "4–5", "5", "3", "$50k–200k+", "6–12 mo", "Risk ops", "Risk firm"],
                ["10", "Own lending / ST collateral protocol", "5", "5", "2", "$150k–500k+", "9–18 mo", "Yes heavy", "Raise first"],
            ],
            col_widths=[0.35 * inch, 2.0 * inch, 0.45 * inch, 0.4 * inch, 0.45 * inch, 0.75 * inch, 0.7 * inch, 0.75 * inch, 0.95 * inch],
        )
    )
    story.append(p("Table: Master ranking — Difficulty 1=easiest, Revenue/Dist 5=highest.", s["caption"]))

    story.append(p("Revenue potential ranked (independent of difficulty)", s["h2"]))
    story.append(
        make_table(
            ["Rev rank", "Product", "Primary monetization", "Ceiling note"],
            [
                ["Highest", "Own lending / curator at scale", "Interest margin, curator fees 5–15% of yield", "Needs AUM + trust"],
                ["High", "Swap UI with fee / referral", "5–30 bps or partner revshare", "Scales with volume"],
                ["High", "Copy trading with take-rate", "Volume bps or profit share", "Regulatory drag"],
                ["High", "Earn + ST SaaS at scale", "$8–50/mo × users + API", "Steady, not explosive"],
                ["Medium", "Agent packs / LLM tools", "Sub + usage", "Commoditizes fast"],
                ["Lower short-term", "Pure free tools", "Indirect / grants", "Use as wedge only"],
            ],
            col_widths=[1.0 * inch, 1.8 * inch, 2.2 * inch, 1.8 * inch],
        )
    )
    story.append(p("Table: Revenue ceiling order — higher ceiling often means harder compliance/capital.", s["caption"]))

    story.append(p("Distribution potential ranked", s["h2"]))
    story.append(
        make_table(
            ["Dist rank", "Channel", "Why it works on RH Chain", "Best products"],
            [
                ["1", "Robinhood Earn users (US)", "In-app DeFi, confused about 7% &amp; risk", "#1 Earn intelligence"],
                ["2", "Robinhood Wallet ST holders (non-US)", "New asset class, poor portfolio tools", "#2 Portfolio, #3 Swap"],
                ["3", "Agentic Trading curiosity", "MCP is new; safety content goes viral", "#5 Agent packs"],
                ["4", "Crypto Twitter / X", "Fast feedback; noisy memecoins", "All — carefully"],
                ["5", "SEO / YouTube education", "“How does Robinhood Earn work?”", "#1, #2"],
                ["6", "Ecosystem BD / grants", "Email + Arbitrum Open House $1M prizes", "Tooling products"],
                ["7", "KOL / affiliate", "Paid distribution", "#3 swap, #7 copy"],
            ],
            col_widths=[0.7 * inch, 1.8 * inch, 2.5 * inch, 1.8 * inch],
        )
    )
    story.append(p("Table: Where users actually come from — match product to channel.", s["caption"]))
    story.append(PageBreak())

    # 4 DEEP DIVES
    story.append(p("4. Product Deep Dives (Easy → Hard)", s["h1"]))
    story.append(green_hr())

    # 1
    product_card(
        story, s,
        "1", "Earn / Morpho Yield &amp; Risk Intelligence (SaaS)",
        "Easy (1/5)", "High (4/5)", "Excellent (5/5)", "3–6 weeks", "$500–3,000", "$1–15k/yr",
        "Best first bet for US-focused builders — zero contracts, clear pain, subscription revenue.",
        "Dashboard for Robinhood Earn / Morpho vaults on Robinhood Chain: split real APY (protocol interest vs incentives), "
        "utilization, withdraw liquidity, curator parameter change feed, historical rates, “what if incentives end” scenarios, "
        "Telegram/email alerts on rate drops or high utilization.",
        "Earn is the US distribution wedge. Official app is simple; disclosures and Reddit already show confusion about "
        "variable ~7%, incentives, smart contract risk, and insurance limits. You provide clarity without custody.",
        "Pro retail $8–20/mo; power users; later B2B/API for creators and tools. Affiliate optional.",
        "Read-only indexer + Next.js app + wallet optional. No custom smart contracts. Morpho/public RPC + indexer.",
        [
            ["Dev time (solo)", "3–6 weeks", "2–3 months"],
            ["Hosting + DB + jobs", "$20–80/mo", "$100–400/mo"],
            ["RPC / Alchemy", "$0– freemium", "$200–500/mo"],
            ["Custom contracts", "$0", "$0"],
            ["Audit", "$0", "$0"],
            ["Legal (ToS/disclaimer)", "$0–1k templates", "$2–5k review"],
            ["Cash to launch", "$200–1,500", "$3–10k"],
            ["12-month opex", "~$1–4k", "~$5–15k"],
        ],
        "<b>Revenue detail:</b> 200 × $12 = $2.4k MRR. Freemium free tier for growth. API $49–499/mo later. "
        "Do not promise yields. Monetize insight and alerts.",
        "<b>Distribution:</b> SEO “Robinhood Earn explained”; X threads on APY breakdown; Reddit r/RobinhoodApp (value, not spam); "
        "YouTube explainers; share vault health when rates change; email chain-developers-group@robinhood.com as ecosystem tool; "
        "Arbitrum grants angle: transparency tooling for retail DeFi.",
        "Low technical risk. Reputation risk if you overstate safety. Keep educational tone. Rates/incentives change — refresh data quality.",
        "Diff 1 · Rev 4 · Dist 5 · <b>Overall: TOP PICK (US)</b>",
    )

    # 2
    product_card(
        story, s,
        "2", "Stock Token Portfolio + Tax / PnL Tracker",
        "Easy–Med (2/5)", "High (4/5)", "Strong (4/5)", "4–8 weeks", "$500–5,000", "$5–20k/yr",
        "Best first bet for non-US / Stock Token builders — portfolio job is unsolved.",
        "Connect wallet → list Stock Token positions, cost basis, 24/7 marks vs traditional close (where useful), "
        "unrealized/realized PnL, multi-venue trade history (e.g. Uniswap), CSV export for accountants, eligibility banners.",
        "ST is a new asset class on RH Chain. Brokerage-quality portfolio tracking is missing. Users buy NVDA/AAPL-linked tokens "
        "and lack “what do I hold and what did I make?” tools. Aligns with RWA thesis without competing with Uniswap itself.",
        "Subscription $10–30/mo Pro; accountant seats later; B2B white-label for wallets.",
        "Wallet connect (viem/wagmi), indexer for transfers/swaps, price feeds (Chainlink + ST metadata), Next.js UI. No custody.",
        [
            ["Dev time", "4–8 weeks", "3–4 months"],
            ["Indexer (subgraph/custom)", "$50–150/mo", "$200–800/mo"],
            ["Price / data", "Mostly public", "$0–300/mo"],
            ["Hosting", "$20–100/mo", "$100–400/mo"],
            ["Contracts / audit", "$0", "$0"],
            ["Legal disclaimers", "$500–3k", "$3–8k"],
            ["Cash to launch", "$500–3k", "$5–15k"],
        ],
        "<b>Revenue detail:</b> 300 × $15 = $4.5k MRR. Annual plans. Export-only free tier. "
        "Partnerships with tax tools. High willingness to pay among active traders.",
        "<b>Distribution:</b> Non-US crypto Twitter; Wallet user communities; content “Stock Tokens tax tracking”; "
        "list on RH ecosystem page when ready; DEXs refer for post-trade; SEO on ticker + tokenized stock.",
        "Data accuracy liability → heavy disclaimers. Geo: never market ST tools to US persons. Oracle/mark discrepancies.",
        "Diff 2 · Rev 4 · Dist 4 · <b>Overall: TOP PICK (Non-US)</b>",
    )

    # 3
    product_card(
        story, s,
        "3", "Stock Token + USDG Best-Execution / Swap UI",
        "Easy–Med (2/5)", "High (4/5)", "Strong (4/5)", "3–6 weeks (UI)", "$500–8,000 UI / $20–55k with router", "Varies",
        "Volume-native revenue; ship UI-first without custom router.",
        "One screen: buy $X of a Stock Token with USDG/ETH; compare Uniswap vs other venues; show price impact, fees, gas; "
        "eligibility warning; optional gas sponsorship via Alchemy AA.",
        "Trading is core thesis. Retail cannot compare venues. Official stack has multiple AMMs/routers — clarity wins.",
        "Swap fee share 5–30 bps; or free + Pro charts; partner referrals from DEXs.",
        "Phase 1: pure frontend deep-linking / quoting Uniswap (no custody). Phase 2: fee-taking router contract + audit.",
        [
            ["UI-only build", "3–6 weeks / $0.5–2k cash", "Polished 2–3 mo"],
            ["Fee router contract", "$2–8k dev", "—"],
            ["Audit if routing value", "$0 (UI-only)", "$15–40k"],
            ["Infra", "$50–200/mo", "$100–400/mo"],
            ["Cash to launch", "$500–2k (UI)", "$20–55k (with audit)"],
        ],
        "<b>Revenue detail:</b> At $2M monthly volume and 10 bps = $2k/mo. Scales linearly. "
        "UI-only can use affiliate until volume justifies audit.",
        "<b>Distribution:</b> Default landing after “I want ST”; Twitter quote tools; embed widgets; "
        "Wallet deep links; compete on UX not liquidity ownership.",
        "Medium if custom router (MEV, routing bugs). Low if pure UI. Compliance if you look like a broker — counsel before fees.",
        "Diff 2 · Rev 4 · Dist 4 · <b>Overall: BEST FEE PATH (start UI-only)</b>",
    )

    # 4
    product_card(
        story, s,
        "4", "Alerts, Watchlists &amp; Notifier (ST / Earn / Perps)",
        "Easy (1/5)", "Medium (3/5)", "Strong (4/5)", "2–4 weeks", "$300–2,000", "$1–8k/yr",
        "Fastest ship; often a feature of #1/#2 — can also be standalone wedge.",
        "Price alerts on Stock Tokens, Earn APY threshold alerts, Morpho utilization alerts, large trade / whale alerts, "
        "Telegram bot + email + web push.",
        "24/7 markets need 24/7 attention tools. Robinhood app won’t cover every onchain condition early.",
        "Freemium: free limited alerts; Pro $5–12/mo unlimited + SMS optional.",
        "Workers + webhooks + simple DB. Can share backend with product #1 or #2.",
        [
            ["Dev", "2–4 weeks", "6–8 weeks"],
            ["Messaging (Telegram free; SMS $)", "$0–50/mo", "$50–300/mo"],
            ["Infra", "$20–80/mo", "$100–250/mo"],
            ["Audit", "$0", "$0"],
            ["Cash to launch", "$300–1k", "$2–5k"],
        ],
        "<b>Revenue detail:</b> Lower ARPU than full SaaS; high conversion from free. Good upsell into #1/#2.",
        "<b>Distribution:</b> Viral “set this alert” posts; bot invite links; embed in content creator workflows.",
        "Spam regulations for SMS. Alert fatigue. Don’t spam X users.",
        "Diff 1 · Rev 3 · Dist 4 · <b>Overall: FAST WEDGE / FEATURE</b>",
    )
    story.append(PageBreak())

    # 5
    product_card(
        story, s,
        "5", "Agent Strategy Packs + Risk Monitor (MCP Phase 1)",
        "Med (2–3/5)", "Med–High (3/5)", "Strong (4/5)", "4–8 weeks", "$1–10,000", "$15–40k/yr w/ LLM",
        "Ride the agent narrative without building a full onchain agent (yet).",
        "Productized strategies and guardrail templates for Robinhood Agentic Trading (brokerage MCP): "
        "DCA packs, rebalance rules, max daily loss language, checklist UX, monitoring dashboard. "
        "User connects their own agent (Claude/ChatGPT/etc.) via official MCP; you sell templates + monitoring — not custody.",
        "RH heavily markets agentic trading (MCP endpoint agent.robinhood.com/mcp/trading). Users fear runaway bots. "
        "Safety and templates are the product. Phase 2 can move onchain later.",
        "$15–50/mo; usage-based LLM if you host runners (higher reg risk — prefer user-hosted agent).",
        "Content + SaaS app. No chain contracts in phase 1. Optional LLM API for strategy generation.",
        [
            ["Phase 1 SaaS", "$1–8k cash", "2–3 months polish"],
            ["LLM API opex", "$50–500/mo", "$500–2k/mo at scale"],
            ["Phase 2 onchain AA agent", "—", "$40–120k + audit"],
            ["Legal (advice boundaries)", "$1–5k", "$5–15k"],
        ],
        "<b>Revenue detail:</b> Content-led growth; subscriptions. Avoid AUM fees without licenses. "
        "Never guarantee returns. Tools/templates framing only.",
        "<b>Distribution:</b> YouTube “safe agentic setup”; X demos; SEO; partnership with agent platforms; "
        "RH agent narrative content.",
        "High regulatory risk if personalized advice or managing money. Stay software tools. Liability if templates lose money — disclaimers.",
        "Diff 2–3 · Rev 3 · Dist 4 · <b>Overall: STRONG NARRATIVE FIT</b>",
    )

    # 6
    product_card(
        story, s,
        "6", "Morpho Power-User Frontend (Beyond Earn)",
        "Med (3/5)", "Med (3/5)", "Med (3/5)", "6–10 weeks", "$3–15,000", "$5–25k/yr",
        "For DeFi-native users who export wallets or want more than one vault.",
        "Full Morpho markets UI on RH Chain: supply USDG, explore collateral markets, health factors, "
        "liquidation awareness, multi-market view. Complements — does not replace — Robinhood Earn’s one-tap vault.",
        "Earn is one curated vault. Power users and exported-wallet users need a home. Morpho is official lending primitive.",
        "Referral fees; later optional curator partnership; Pro analytics.",
        "Frontend on Morpho SDK/contracts; wallet connect; read+write to existing protocol — no new lending math if pure frontend.",
        [
            ["Frontend build", "$3–10k time/cash", "$10–20k polished"],
            ["Audit", "$0 pure frontend", "If wrappers: $40k+"],
            ["Infra", "$50–200/mo", "$200–500/mo"],
        ],
        "<b>Revenue detail:</b> Moderate until AUM referrals. Curator path is separate (see #9).",
        "<b>Distribution:</b> DeFi Twitter; Morpho community; “export wallet then manage here” content; "
        "power users from Earn who outgrow simple UI.",
        "Competing with official simplicity. UX must be excellent. Don’t imply affiliation with Robinhood/Morpho.",
        "Diff 3 · Rev 3 · Dist 3 · <b>Overall: SOLID IF YOU KNOW DEFI</b>",
    )

    # 7
    product_card(
        story, s,
        "7", "Copy Desk / Social Trading (Not Friend.tech Keys)",
        "Med–Hard (3–4/5)", "High (4/5)", "Med (3/5)", "8–14 weeks", "$5–25,000+", "Higher legal opex",
        "Trading thesis + social distribution — different from GreenTown key casino.",
        "Follow wallets with transparent PnL; optional auto-copy with max allocation and kill switch; "
        "fee on copy volume. Asset rooms optional later. Not bonding-curve keys.",
        "Users want “who to follow” for ST/perps without pure speculation social. Aligns with trading + wallet habits.",
        "10–20% profit share or volume bps; Pro leaderboards.",
        "Phase 1: signal feed + manual follow (no auto-exec). Phase 2: onchain/copy vault + audit + legal.",
        [
            ["Signals UI only", "$5–15k", "—"],
            ["Onchain copy + audit", "—", "$50–150k+"],
            ["Legal / compliance", "$5–25k", "Ongoing counsel"],
            ["Infra", "$100–400/mo", "$300–1k/mo"],
        ],
        "<b>Revenue detail:</b> High if volume works. Friend.tech-like hype is wrong model; durable PnL trust is right.",
        "<b>Distribution:</b> Trader KOLs; X leaderboards; perps communities (Lighter); careful paid KOL tests.",
        "Regulatory: copy trading may be treated as advisory/brokerage by jurisdiction. Budget counsel. Scam leaders — need filtering.",
        "Diff 3–4 · Rev 4 · Dist 3 · <b>Overall: HIGH CEILING, LEGAL FIRST</b>",
    )

    # 8
    product_card(
        story, s,
        "8", "Onchain AA Agent Executor (Guarded Agents on RH Chain)",
        "Hard (4/5)", "High (4/5)", "Med (3/5)", "3–6 months", "$40–120,000", "$30–100k/yr",
        "Only after phase-1 agent demand or funding — contracts + audit required.",
        "Session keys / ERC-4337 account abstraction agents that can swap, lend USDG, rebalance ST within hard caps "
        "set by user. Kill switch. Human remains in control of limits.",
        "Chain is marketed AI-native; AA is first-class. Fills gap between brokerage MCP and onchain ST/Earn automation.",
        "SaaS + per-execution fee or % of AUM (careful: regs). Gas sponsorship margin.",
        "Solidity AA modules, policy engine, frontend, monitoring, formal audit, bug bounty.",
        [
            ["Contracts + frontend", "$20–50k", "Team cost higher"],
            ["Audit", "$40–100k", "Remediation extra"],
            ["Bug bounty", "$5–25k", "—"],
            ["Infra + AA gas", "$200–2k/mo", "Scales with users"],
            ["Cash to launch", "$40–120k", "—"],
        ],
        "<b>Revenue detail:</b> Strong if sticky automation. High trust bar. Enterprise later.",
        "<b>Distribution:</b> Agent Twitter; showcase on RH AI narrative; Open House demos; security-first marketing.",
        "Smart contract risk, agent misbehavior, regulatory classification. Do not skip audit.",
        "Diff 4 · Rev 4 · Dist 3 · <b>Overall: FUNDED / POST-REVENUE</b>",
    )
    story.append(PageBreak())

    # 9
    product_card(
        story, s,
        "9", "Morpho Vault Curator Brand (Compete/Complement Earn)",
        "Hard (4–5/5)", "Very High (5/5)", "Med (3/5)", "6–12 months", "$50–200,000+", "Ops-heavy",
        "Risk firm business — not a weekend app. Steakhouse-style curation.",
        "Curate Morpho vaults with own risk parameters, allocations, documentation, and fee model "
        "(management and/or performance fees, often ~5–15% of yield in industry practice). "
        "Possibly differentiate on ST collateral markets or non-US strategies where legal.",
        "Curators are the silent winners of Morpho: fees on AUM without building full lending primitive. "
        "Earn already uses Steakhouse — room for specialized vaults, not easy “clone Earn.”",
        "Curator fees on deposits; distributor revshare with frontends.",
        "Risk team, monitoring, governance/timelocks, legal, reputation, liquidity relationships. "
        "Steakhouse reached large AUM with lean team but deep expertise — not beginner path.",
        [
            ["Risk + ops team", "Ongoing salaries", "Main cost"],
            ["Monitoring infra", "$500–5k/mo", "—"],
            ["Legal / entity", "$10–50k+", "—"],
            ["Audit / reviews", "$20–80k", "Ongoing"],
            ["Cash / runway", "$50–200k+ year 1", "Until fee AUM"],
        ],
        "<b>Revenue detail:</b> Example industry narrative: meaningful ARR at large AUM. "
        "At $50M AUM and 1% effective fee ≈ $500k/yr — hard to reach. Start only with risk credibility.",
        "<b>Distribution:</b> Institutional + DeFi-native; integrations with frontends; not CT memes.",
        "Curation risk is real (disclosed in Robinhood Earn). Bad parameters → user losses → brand death. Capital intensive.",
        "Diff 4–5 · Rev 5 · Dist 3 · <b>Overall: ONLY WITH RISK EXPERTISE</b>",
    )

    # 10
    product_card(
        story, s,
        "10", "Own Lending Protocol / ST Collateral Market",
        "Hardest (5/5)", "Very High (5/5)", "Low–Med (2/5)", "9–18 months", "$150–500,000+", "$300k–1M+",
        "Protocol ambition — raise first. Do not start here.",
        "New borrow/lend markets specialized for Stock Tokens: oracles, LTVs, liquidations, risk engines, "
        "insurance narratives, multi-asset collateral.",
        "Official story says ST can be collateral in DeFi — building the full protocol captures interest margin "
        "but fights Morpho/Aave-style gravity and needs deep liquidity + security.",
        "Interest spread, liquidation fees, token incentives (optional, dangerous).",
        "Full protocol engineering, multiple audits, bug bounties, market makers, legal, liquidity mining budget.",
        [
            ["Engineering team", "$200k+/yr", "—"],
            ["Audits (multi)", "$100–250k+", "—"],
            ["Liquidity / incentives", "$50–500k+", "—"],
            ["Legal", "$50–250k+", "Securities issues"],
            ["Total year-1", "$150k–500k+ lean", "$1M+ serious"],
        ],
        "<b>Revenue detail:</b> Highest ceiling if successful; most projects fail or never get TVL.",
        "<b>Distribution:</b> Needs RH/ecosystem partnership or massive incentives. Cold start is brutal.",
        "Smart contract exploits, oracle failure, regulatory (RWA collateral), liquidity death spiral.",
        "Diff 5 · Rev 5 · Dist 2 · <b>Overall: RAISE OR SKIP</b>",
    )

    # 5 COSTS
    story.append(p("5. Cost Reference Tables", s["h1"]))
    story.append(green_hr())
    story.append(p("5.1 Infrastructure (monthly)", s["h2"]))
    story.append(
        make_table(
            ["Item", "Indie", "Growth", "Notes"],
            [
                ["Hosting (Railway/Vercel)", "$20–50", "$100–400", "FE + API split like GreenTown pattern"],
                ["Postgres / Redis", "$15–50", "$50–200", "Supabase, Neon, Railway"],
                ["RPC / Alchemy", "$0–50", "$200–500+", "RH recommends Alchemy; AA gas extra"],
                ["Indexer workers", "$20–100", "$200–800", "Critical for portfolio products"],
                ["Sentry / analytics", "$0–30", "$50–200", "GA4 free tier ok early"],
                ["LLM APIs", "$50–200", "$500–2,000+", "Agents only"],
                ["Domain + email", "$5–15", "$20–50", "Google Workspace etc."],
                ["Total typical", "$50–400", "$500–2,500+", "Before salaries"],
            ],
            col_widths=[1.8 * inch, 1.2 * inch, 1.3 * inch, 2.5 * inch],
        )
    )
    story.append(p("Table: Monthly infra ranges.", s["caption"]))

    story.append(p("5.2 Smart contract audits (2026 market)", s["h2"]))
    story.append(
        make_table(
            ["Scope", "Typical audit cost", "When needed"],
            [
                ["Simple ERC-20 / minimal", "$5–20k", "Rarely your MVP"],
                ["Fee router / simple vault wrapper", "$15–40k", "If you take fees onchain"],
                ["Mid DeFi protocol", "$40–100k", "Vaults, leverage, complex money flow"],
                ["Complex lending / AMM", "$50–150k+", "New protocol"],
                ["Full pre-launch package", "$60–120k common", "Audit + remediation pass"],
                ["Bug bounty pool", "$5–50k", "After audit"],
            ],
            col_widths=[2.2 * inch, 1.8 * inch, 2.8 * inch],
        )
    )
    story.append(
        p(
            "Sources: 2026 audit market references (Sherlock, industry blogs). "
            "Arbitrum audit subsidy may offset later — do not depend on it for launch.",
            s["caption"],
        )
    )

    story.append(p("5.3 People (if not solo)", s["h2"]))
    story.append(
        make_table(
            ["Role", "Monthly (rough)", "Notes"],
            [
                ["Full-stack contractor", "$6–15k", "US/EU rates; lower offshore"],
                ["Solidity part-time", "$4–10k", "Only when contracts needed"],
                ["Designer", "$2–6k", "Or one-time $2–8k"],
                ["Part-time counsel", "$2–8k retainer", "Before trading/agent fees"],
                ["Risk analyst (curator)", "$8–20k", "For vault curation only"],
            ],
            col_widths=[2.0 * inch, 1.8 * inch, 3.0 * inch],
        )
    )
    story.append(p("Table: People costs — largest budget item after audits for funded teams.", s["caption"]))

    story.append(p("5.4 True total by ambition", s["h2"]))
    story.append(
        make_table(
            ["Ambition", "90-day cash", "12-month cash", "Products"],
            [
                ["Read-only SaaS", "$500–5k", "$5–20k", "#1, #2, #4"],
                ["Trading UI no custom router", "$1–8k", "$8–25k", "#3 phase 1"],
                ["Agent templates", "$2–10k", "$15–40k", "#5 phase 1"],
                ["Custom DeFi + audit", "$40–120k", "$100–300k", "#3 phase 2, #8"],
                ["New lending / curator serious", "$150k+", "$300k–1M+", "#9, #10"],
            ],
            col_widths=[1.9 * inch, 1.3 * inch, 1.4 * inch, 2.2 * inch],
        )
    )
    story.append(p("Table: All-in cash if founder codes; add salary if not.", s["caption"]))
    story.append(PageBreak())

    # 6 DISTRIBUTION
    story.append(p("6. Distribution Playbook", s["h1"]))
    story.append(green_hr())
    story.append(
        p(
            "Robinhood Chain distribution is <b>not</b> “post a memecoin.” It is a mix of brokerage funnel leakage, "
            "Wallet users, Earn curiosity, and crypto-native Twitter. Match channel to product.",
            s["body"],
        )
    )
    story.append(
        make_table(
            ["Channel", "Cost", "Best products", "Tactics"],
            [
                ["SEO / content", "Time / $0–1k", "#1 #2 #5", "Earn explainers, ST tax guides, agent safety"],
                ["X / CT", "Time / $0–2k", "All", "Data posts, dashboards, not shill coins"],
                ["YouTube", "Time / $100–500", "#1 #5", "Walkthroughs of Earn + agents"],
                ["Reddit (careful)", "Time", "#1", "Answer risk questions; no spam"],
                ["RH ecosystem BD", "Time", "Tooling", "chain-developers-group@robinhood.com + metrics"],
                ["Arbitrum Open House", "Time", "Any shipping", "$1M prize narrative for RH builders"],
                ["Arbitrum Foundation grants", "Time", "Public goods", "Rolling grants ~$20–150k ARB cited range"],
                ["KOL / affiliate", "$500–5k tests", "#3 #7", "Only with real product"],
                ["In-product viral", "Eng", "#4 #3", "Share PnL cards, alert links"],
            ],
            col_widths=[1.5 * inch, 1.1 * inch, 1.2 * inch, 3.0 * inch],
        )
    )
    story.append(p("Table: Distribution channels with cost and product fit.", s["caption"]))
    story.append(
        p(
            "<b>Wallet distribution reality:</b> ~28M customers are a funnel, not free users. Conversion to onchain "
            "is still tiny early. Design for the few who export, bridge, or open Earn/Wallet — make their first success "
            "obvious. Account abstraction + gas sponsorship (Alchemy) reduces drop-off.",
            s["body"],
        )
    )

    # 7 PATHS
    story.append(p("7. Recommended Paths by Budget &amp; Skills", s["h1"]))
    story.append(green_hr())
    story.append(
        make_table(
            ["Your situation", "Build this", "Avoid"],
            [
                ["Solo, &lt;$5k, can code FE/BE", "#1 or #2 (+ #4 features)", "Custom lending, SocialFi clone"],
                ["Solo, non-US focus", "#2 then #3 UI", "US-only Earn assumptions"],
                ["Solo, US focus", "#1 then #5 templates", "Stock Token primary product"],
                ["Want fees from volume", "#3 UI → fee later", "Router without audit"],
                ["Love AI, hate Solidity", "#5 phase 1", "Onchain agent day one"],
                ["Have $50k+ and Solidity", "#6 + small fee contracts", "Jumping to #10"],
                ["Risk/TradFi background", "Explore #9 carefully", "CT growth hacks as core"],
                ["Raising a fundraise", "#8 or #10 narrative + MVP #1/#2", "Token-only no product"],
            ],
            col_widths=[2.0 * inch, 2.5 * inch, 2.3 * inch],
        )
    )
    story.append(p("Table: Decision matrix by founder situation.", s["caption"]))

    # 8 ROADMAP
    story.append(p("8. 90-Day Default Roadmap", s["h1"]))
    story.append(green_hr())
    story.append(
        callout_box(
            "Default path for most solo builders",
            "Days 1–30: Ship product #1 (US) or #2 (non-US) read-only MVP. Landing page, waitlist, first 20 users. "
            "Days 31–60: Paid tier live; add alerts (#4). Apply Arbitrum Open House / grants. Email RH ecosystem with metrics. "
            "Days 61–90: Add #3 swap deep-links; first revenue target $500–2k MRR. Only then plan contracts.",
            s,
        )
    )
    story.append(Spacer(1, 0.1 * inch))
    for item in [
        "<b>Week 1–2:</b> Pick geo (US Earn vs non-US ST). Validate 10 interviews. Sketch data sources (Morpho, RPC, ST list).",
        "<b>Week 3–4:</b> MVP dashboard live on mainnet data. Public URL. Discord/Telegram support.",
        "<b>Week 5–6:</b> Pricing page. Stripe. First paid user. Iterate on clarity of risk copy.",
        "<b>Week 7–8:</b> Alerts + shareable report cards. Content engine (2 posts/week).",
        "<b>Week 9–10:</b> Swap quotes / Uniswap links for ST. Measure conversion.",
        "<b>Week 11–12:</b> Grant deck. Ecosystem email. Decide if agent pack is worth phase-2.",
    ]:
        story.append(p(f"•  {item}", s["bullet"]))

    story.append(PageBreak())

    # 9 REGULATORY
    story.append(p("9. Regulatory &amp; Landmine Checklist", s["h1"]))
    story.append(green_hr())
    story.append(
        make_table(
            ["Topic", "Rule of thumb", "Product impact"],
            [
                ["Stock Tokens", "Not for US persons; debt exposure ≠ share ownership", "Geo gates mandatory on #2 #3 #7"],
                ["Earn / USDG", "Not a bank; variable APY; incentives can end", "#1 must show risk + incentive split"],
                ["Insurance", "RH policy ≠ user personal claim; not FDIC", "Never market “insured yield” carelessly"],
                ["Agents", "User-controlled; no guaranteed alpha", "#5 #8 = tools not advisors"],
                ["Advice language", "Education/tools ≠ personalized advice", "All SaaS products"],
                ["Swap fees", "May trigger broker/MSB issues by country", "Counsel before #3 fees scale"],
                ["Copy trading", "Often regulated as advice/brokerage", "Legal budget for #7"],
                ["Custody", "Avoid holding user keys/funds", "Prefer non-custodial always"],
                ["Tokens", "Token-first raises scam + legal risk on RH brand", "Product + fees first"],
            ],
            col_widths=[1.3 * inch, 2.8 * inch, 2.7 * inch],
        )
    )
    story.append(
        p(
            "Budget $2–10k legal review before meaningful trading/agent fees; more if targeting US retail at scale. "
            "This guide is not legal advice.",
            s["caption"],
        )
    )

    # 10 SOURCES
    story.append(p("10. Sources &amp; Further Links", s["h1"]))
    story.append(green_hr())
    for item in [
        "Robinhood Chain: https://robinhood.com/us/en/chain/ · docs: https://docs.robinhood.com/chain/",
        "Ecosystem: https://robinhood.com/us/en/chain/ecosystem/",
        "Mainnet newsroom (July 1, 2026): Stock Tokens, Earn, agents, DeFi partners",
        "Robinhood Earn support: https://robinhood.com/us/en/support/articles/crypto-earn/",
        "Agentic Trading: https://robinhood.com/us/en/agentic-trading/ · MCP trading endpoint documentation in support articles",
        "Morpho / Steakhouse curation model (public Morpho + Steakhouse materials)",
        "Arbitrum Open House: https://openhouse.arbitrum.io/ · Grants: https://arbitrum.foundation/grants",
        "Developer contact: chain-developers-group@robinhood.com",
        "Audit cost landscape 2026: industry references (e.g. Sherlock market notes, audit firm guides)",
        "Network: Chain ID 4663 mainnet · RPC via Alchemy / public rpc.mainnet.chain.robinhood.com",
    ]:
        story.append(p(f"•  {item}", s["bullet"]))

    story.append(Spacer(1, 0.2 * inch))
    story.append(green_hr())
    story.append(p("Closing Recommendation", s["h2"]))
    story.append(
        p(
            "Sort products by <b>easy → hard</b>, but choose by <b>revenue × distribution ÷ difficulty</b>. "
            "For most builders that formula peaks at <b>#1 Earn intelligence (US)</b> or "
            "<b>#2 Stock Token portfolio (non-US)</b>, then <b>#3 UI-only swap</b>. "
            "Hard products (#8–#10) have higher ceilings and higher death rates — fund them with revenue or capital, not hope.",
            s["body"],
        )
    )
    story.append(
        p(
            "You provide value when you make Earn understandable, Stock Tokens operable, trades clearer, or agents safer — "
            "and charge for that job. You do not need to beat SocialFi clones or rebuild Morpho on day one.",
            s["quote"],
        )
    )
    story.append(
        p(
            "— End of guide —",
            ParagraphStyle(
                "end", fontName="Helvetica-Oblique", fontSize=9,
                textColor=GRAY, alignment=TA_CENTER, spaceBefore=14,
            ),
        )
    )
    story.append(
        p(
            "Research synthesis for product planning only. Not an offer or solicitation. "
            "Costs and ecosystem details change rapidly — re-verify before spending money or shipping financial features.",
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
        topMargin=0.6 * inch,
        bottomMargin=0.65 * inch,
        title="Robinhood Chain Viable Products Guide",
        author="Product Strategy Research",
        subject="Easy to hard product ranking with revenue, distribution, and costs",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"Wrote: {OUT}")
    return OUT


if __name__ == "__main__":
    build()
