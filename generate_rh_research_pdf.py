#!/usr/bin/env python3
"""Generate a detailed Robinhood Chain research PDF."""

from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUT = Path(__file__).resolve().parent / "Robinhood_Chain_Research_Report.pdf"

# Brand-ish palette
HOOD_GREEN = colors.HexColor("#00C805")
DARK = colors.HexColor("#0D0D0D")
SLATE = colors.HexColor("#1A1A1A")
GRAY = colors.HexColor("#4A4A4A")
LIGHT_GRAY = colors.HexColor("#F4F5F7")
MID_GRAY = colors.HexColor("#E5E7EB")
ACCENT = colors.HexColor("#0B5FFF")
WHITE = colors.white


def make_styles():
    base = getSampleStyleSheet()
    styles = {
        "cover_title": ParagraphStyle(
            "cover_title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=28,
            leading=34,
            textColor=WHITE,
            alignment=TA_CENTER,
            spaceAfter=12,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=12,
            leading=16,
            textColor=colors.HexColor("#D1D5DB"),
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
        "cover_meta": ParagraphStyle(
            "cover_meta",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#9CA3AF"),
            alignment=TA_CENTER,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=DARK,
            spaceBefore=16,
            spaceAfter=10,
            borderPadding=3,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=17,
            textColor=SLATE,
            spaceBefore=12,
            spaceAfter=6,
        ),
        "h3": ParagraphStyle(
            "h3",
            parent=base["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=GRAY,
            spaceBefore=8,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13.5,
            textColor=DARK,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        ),
        "body_left": ParagraphStyle(
            "body_left",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13.5,
            textColor=DARK,
            alignment=TA_LEFT,
            spaceAfter=6,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13,
            textColor=DARK,
            leftIndent=12,
            spaceAfter=3,
        ),
        "cell": ParagraphStyle(
            "cell",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=10.5,
            textColor=DARK,
        ),
        "cell_bold": ParagraphStyle(
            "cell_bold",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10.5,
            textColor=DARK,
        ),
        "caption": ParagraphStyle(
            "caption",
            parent=base["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=8,
            leading=10,
            textColor=GRAY,
            spaceBefore=2,
            spaceAfter=8,
        ),
        "callout": ParagraphStyle(
            "callout",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13,
            textColor=DARK,
            leftIndent=8,
            rightIndent=8,
            spaceBefore=4,
            spaceAfter=4,
        ),
        "toc": ParagraphStyle(
            "toc",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=16,
            textColor=DARK,
            leftIndent=8,
        ),
        "footer": ParagraphStyle(
            "footer",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            textColor=GRAY,
            alignment=TA_CENTER,
        ),
        "quote": ParagraphStyle(
            "quote",
            parent=base["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=10,
            leading=14,
            textColor=SLATE,
            leftIndent=16,
            rightIndent=16,
            spaceBefore=8,
            spaceAfter=8,
            alignment=TA_CENTER,
        ),
        "mono": ParagraphStyle(
            "mono",
            parent=base["Code"],
            fontName="Courier",
            fontSize=7.5,
            leading=10,
            textColor=DARK,
            backColor=LIGHT_GRAY,
            leftIndent=4,
            rightIndent=4,
            spaceBefore=4,
            spaceAfter=8,
        ),
        "tier_title": ParagraphStyle(
            "tier_title",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=13,
            textColor=DARK,
            spaceBefore=6,
            spaceAfter=4,
        ),
    }
    return styles


def hr():
    return HRFlowable(
        width="100%", thickness=0.8, color=MID_GRAY, spaceBefore=4, spaceAfter=10
    )


def green_hr():
    return HRFlowable(
        width="100%", thickness=2, color=HOOD_GREEN, spaceBefore=2, spaceAfter=12
    )


def p(text, style):
    return Paragraph(text, style)


def bullet_list(items, styles):
    flow = []
    for item in items:
        flow.append(p(f"•  {item}", styles["bullet"]))
    return flow


def make_table(headers, rows, col_widths=None):
    """Build a styled table with Paragraph cells for wrapping."""
    s_h = ParagraphStyle(
        "th",
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=WHITE,
    )
    s_c = ParagraphStyle(
        "td",
        fontName="Helvetica",
        fontSize=7.5,
        leading=10,
        textColor=DARK,
    )
    s_cb = ParagraphStyle(
        "tdb",
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=10,
        textColor=DARK,
    )

    data = [[Paragraph(str(h), s_h) for h in headers]]
    for i, row in enumerate(rows):
        cells = []
        for j, cell in enumerate(row):
            st = s_cb if j == 0 else s_c
            cells.append(Paragraph(str(cell), st))
        data.append(cells)

    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), DARK),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("ALIGN", (0, 0), (-1, 0), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.4, MID_GRAY),
        ("BOX", (0, 0), (-1, -1), 0.8, DARK),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), LIGHT_GRAY))
        else:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), WHITE))
    t.setStyle(TableStyle(style_cmds))
    return t


def add_header_footer(canvas, doc):
    canvas.saveState()
    # top line
    canvas.setStrokeColor(HOOD_GREEN)
    canvas.setLineWidth(2)
    canvas.line(0.7 * inch, letter[1] - 0.45 * inch, letter[0] - 0.7 * inch, letter[1] - 0.45 * inch)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GRAY)
    canvas.drawString(0.7 * inch, letter[1] - 0.38 * inch, "Robinhood Chain — Deep Research Report")
    canvas.drawRightString(letter[0] - 0.7 * inch, letter[1] - 0.38 * inch, "Confidential research synthesis")

    # footer
    canvas.setStrokeColor(MID_GRAY)
    canvas.setLineWidth(0.5)
    canvas.line(0.7 * inch, 0.55 * inch, letter[0] - 0.7 * inch, 0.55 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GRAY)
    canvas.drawCentredString(letter[0] / 2, 0.35 * inch, f"Page {doc.page}")
    canvas.drawString(0.7 * inch, 0.35 * inch, "Research compiled July 2026")
    canvas.drawRightString(letter[0] - 0.7 * inch, 0.35 * inch, "For builders & founders")
    canvas.restoreState()


def cover_page(styles, story):
    # Green bar table as cover block
    cover_data = [[""]]
    cover = Table(cover_data, colWidths=[7.1 * inch], rowHeights=[9.2 * inch])
    cover.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), DARK),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 40),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 40),
                ("LEFTPADDING", (0, 0), (-1, -1), 30),
                ("RIGHTPADDING", (0, 0), (-1, -1), 30),
            ]
        )
    )

    inner = []
    inner.append(Spacer(1, 1.2 * inch))
    inner.append(
        Paragraph(
            '<font color="#00C805">●</font>  BLOCKCHAIN ECOSYSTEM RESEARCH',
            ParagraphStyle(
                "badge",
                fontName="Helvetica-Bold",
                fontSize=9,
                textColor=HOOD_GREEN,
                alignment=TA_CENTER,
                spaceAfter=18,
            ),
        )
    )
    inner.append(
        Paragraph(
            "Robinhood Chain",
            ParagraphStyle(
                "ct",
                fontName="Helvetica-Bold",
                fontSize=32,
                leading=38,
                textColor=WHITE,
                alignment=TA_CENTER,
                spaceAfter=8,
            ),
        )
    )
    inner.append(
        Paragraph(
            "Deep Research Report",
            ParagraphStyle(
                "ct2",
                fontName="Helvetica",
                fontSize=18,
                leading=22,
                textColor=colors.HexColor("#E5E7EB"),
                alignment=TA_CENTER,
                spaceAfter=20,
            ),
        )
    )
    inner.append(
        HRFlowable(
            width="40%",
            thickness=2,
            color=HOOD_GREEN,
            spaceBefore=4,
            spaceAfter=20,
            hAlign="CENTER",
        )
    )
    inner.append(
        Paragraph(
            "Apps, SocialFi Landscape, Competitor Comparison,<br/>Grant Funding &amp; Cashflow-Positive Build Recommendations",
            ParagraphStyle(
                "cs",
                fontName="Helvetica",
                fontSize=11,
                leading=16,
                textColor=colors.HexColor("#D1D5DB"),
                alignment=TA_CENTER,
                spaceAfter=28,
            ),
        )
    )
    meta = """
    <b>Sources:</b> Official Robinhood docs &amp; newsroom · Arbitrum blog · Ecosystem partners · X/Twitter crypto activity · Public SocialFi research<br/><br/>
    <b>Compiled:</b> July 2026 &nbsp;&nbsp;|&nbsp;&nbsp; <b>Audience:</b> Founders evaluating Robinhood Chain<br/><br/>
    <b>Scope:</b> Technical overview · Live ecosystem · Social apps · Friend.tech / Lens / Farcaster comparison · Grants · Product strategy
    """
    inner.append(
        Paragraph(
            meta,
            ParagraphStyle(
                "cm",
                fontName="Helvetica",
                fontSize=8.5,
                leading=12,
                textColor=colors.HexColor("#9CA3AF"),
                alignment=TA_CENTER,
            ),
        )
    )
    inner.append(Spacer(1, 1.4 * inch))
    inner.append(
        Paragraph(
            "NOT financial, legal, or investment advice. Ecosystem is early and changes rapidly.",
            ParagraphStyle(
                "disc",
                fontName="Helvetica-Oblique",
                fontSize=7.5,
                textColor=colors.HexColor("#6B7280"),
                alignment=TA_CENTER,
            ),
        )
    )

    # Use a nested approach - simpler cover without nested table complexity
    story.append(Spacer(1, 0.8 * inch))
    for el in inner:
        story.append(el)
    story.append(PageBreak())


def build():
    styles = make_styles()
    story = []

    # ========== COVER ==========
    story.append(Spacer(1, 1.5 * inch))
    story.append(
        Paragraph(
            '<font color="#00C805">●</font>  BLOCKCHAIN ECOSYSTEM RESEARCH',
            ParagraphStyle(
                "badge",
                fontName="Helvetica-Bold",
                fontSize=10,
                textColor=HOOD_GREEN,
                alignment=TA_CENTER,
                spaceAfter=20,
            ),
        )
    )
    story.append(
        Paragraph(
            "Robinhood Chain",
            ParagraphStyle(
                "ct",
                fontName="Helvetica-Bold",
                fontSize=34,
                leading=40,
                textColor=DARK,
                alignment=TA_CENTER,
                spaceAfter=6,
            ),
        )
    )
    story.append(
        Paragraph(
            "Deep Research Report",
            ParagraphStyle(
                "ct2",
                fontName="Helvetica",
                fontSize=18,
                leading=22,
                textColor=GRAY,
                alignment=TA_CENTER,
                spaceAfter=16,
            ),
        )
    )
    story.append(green_hr())
    story.append(
        Paragraph(
            "Apps &amp; Projects · SocialFi Landscape · Competitor Comparison<br/>Grant Funding · Cashflow-Positive Build Recommendations",
            ParagraphStyle(
                "cs",
                fontName="Helvetica",
                fontSize=11,
                leading=16,
                textColor=SLATE,
                alignment=TA_CENTER,
                spaceAfter=30,
            ),
        )
    )

    meta_box = [
        [
            Paragraph(
                "<b>Sources</b><br/>Robinhood official docs &amp; newsroom, Arbitrum blog, "
                "ecosystem partner pages, X/Twitter crypto activity, public SocialFi analyses",
                styles["cell"],
            )
        ],
        [
            Paragraph(
                "<b>Compiled</b> July 2026 &nbsp;&nbsp;·&nbsp;&nbsp; <b>Audience</b> Founders evaluating Robinhood Chain "
                "&nbsp;&nbsp;·&nbsp;&nbsp; <b>Mainnet age</b> ~3 weeks (as of late July 2026)",
                styles["cell"],
            )
        ],
        [
            Paragraph(
                "<b>Disclaimer:</b> Not financial, legal, or investment advice. Stock Tokens and products are geo-restricted. "
                "Ecosystem data changes rapidly; verify on official sources before building or investing.",
                styles["cell"],
            )
        ],
    ]
    mt = Table(meta_box, colWidths=[6.8 * inch])
    mt.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
                ("BOX", (0, 0), (-1, -1), 1, HOOD_GREEN),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.append(mt)
    story.append(Spacer(1, 0.5 * inch))
    story.append(
        Paragraph(
            "<b>Executive thesis in one line</b>",
            styles["h2"],
        )
    )
    story.append(
        Paragraph(
            "Build the social layer for <b>capital markets</b> on Robinhood Chain — rooms, copy desks, and agents "
            "around Stock Tokens and yield — monetized by trading/subscription fees, not by posts.",
            styles["quote"],
        )
    )
    story.append(PageBreak())

    # ========== TOC ==========
    story.append(p("Table of Contents", styles["h1"]))
    story.append(green_hr())
    toc_items = [
        "1. What Robinhood Chain Actually Is",
        "2. Official Ecosystem &amp; Day-One Partners",
        "3. Grassroots / Early Community Projects (from X)",
        "4. Social Apps Building on Robinhood Chain",
        "5. Crypto Social Platforms Comparison (Friend.tech, Farcaster, Lens/Hey.xyz)",
        "6. Grant &amp; Funding Reality",
        "7. What Not to Build",
        "8. What You Should Build (Tier A / B / C)",
        "9. Recommended Product Thesis &amp; Competitive Map",
        "10. Go-to-Market for Grants + Users",
        "11. Network Configuration &amp; Developer Resources",
        "12. Honest Summary Matrix",
        "13. Sources &amp; Further Links",
    ]
    for item in toc_items:
        story.append(p(item, styles["toc"]))
    story.append(PageBreak())

    # ========== SECTION 1 ==========
    story.append(p("1. What Robinhood Chain Actually Is", styles["h1"]))
    story.append(green_hr())
    story.append(
        p(
            "Robinhood Chain is a <b>permissionless, Ethereum-compatible Layer-2 blockchain</b> built to support "
            "onchain financial infrastructure — bringing traditional markets, crypto, and real-world assets (RWAs) "
            "together on a fast, open network. It is part of Robinhood’s broader mission to democratize access to "
            "global financial markets and empower developers with modern blockchain tools.",
            styles["body"],
        )
    )
    story.append(
        p(
            "The chain is <b>not</b> primarily positioned as a memecoin or general consumer social L2. Official "
            "messaging emphasizes <b>tokenized stocks, DeFi (trade / earn / borrow), and AI agents</b> that can "
            "transact with RWAs onchain.",
            styles["body"],
        )
    )

    story.append(p("1.1 Core Facts", styles["h2"]))
    story.append(
        make_table(
            ["Fact", "Detail"],
            [
                ["Type", "Permissionless EVM Layer-2 on Arbitrum Dedicated Blockchains"],
                ["Mainnet launch", "Public mainnet ~July 1–2, 2026"],
                ["Testnet", "Public testnet from ~February 2026"],
                ["Native gas token", "ETH (no official Robinhood Chain gas token announced)"],
                ["Mainnet Chain ID", "4663"],
                ["Testnet Chain ID", "46630"],
                ["Design goal", "Onchain finance + tokenized RWAs (Stock Tokens, ETFs, private assets)"],
                ["Positioning", "“AI-native” L2 — ERC-4337 account abstraction, gas sponsorship, agentic trading"],
                ["Sequencing model", "First-come-first-served by arrival at sequencer (not pure priority-gas auction)"],
                ["Data availability", "Ethereum blobs"],
                ["Security model", "Inherits Ethereum security via Arbitrum L2 stack"],
                ["Distribution edge", "~28M Robinhood customers claimed; chain conversion still tiny"],
                ["Ecosystem signal (CT)", "~500k cumulative addresses; &lt;0.1% of Robinhood app users"],
            ],
            col_widths=[1.8 * inch, 5.0 * inch],
        )
    )
    story.append(
        p(
            "Table: Technical and market facts as of research compilation (July 2026).",
            styles["caption"],
        )
    )

    story.append(p("1.2 Why Robinhood Built Its Own L2", styles["h2"]))
    story.append(
        p(
            "Building a dedicated chain (rather than only using Arbitrum One forever) gives Robinhood more control "
            "over performance, cost structure, partnerships, and product UX while staying EVM-compatible and "
            "Ethereum-secured. Stock Tokens were first explored on shared infrastructure (Arbitrum One), then "
            "migrated toward purpose-built rails (Robinhood Chain) as a phased roadmap.",
            styles["body"],
        )
    )
    for item in [
        "<b>Ethereum security without a new L1</b> — focus engineering on product experience, not consensus reinvention.",
        "<b>Interoperability with Ethereum</b> — avoid fragmented liquidity and unfamiliar developer standards.",
        "<b>Shared → dedicated path</b> — validate demand on Arbitrum One, then run a tailored environment.",
        "<b>Consumer-grade UX</b> — low cost, fast blocks (marketing cites ~100ms block times), crypto in the background.",
    ]:
        story.append(p(f"•  {item}", styles["bullet"]))

    story.append(p("1.3 Built for Real-World Assets", styles["h2"]))
    story.append(
        p(
            "At its core, Robinhood Chain is optimized for <b>tokenized real-world assets</b> — equities, ETFs, "
            "private assets, and other financial instruments — so they can be represented, transferred, and composed "
            "in DeFi (trading, lending collateral, productivity) 24/7. Robinhood’s Stock Tokens provide economic "
            "exposure to underlying securities but are typically structured as tokenized debt securities and "
            "<b>do not grant legal ownership of the underlying shares</b>.",
            styles["body"],
        )
    )
    story.append(
        p(
            "<b>Critical compliance note:</b> Stock Tokens are <b>not available in the US</b> (or to US persons) and "
            "are restricted in many other jurisdictions (including, per disclosures, UK, Canada, Switzerland, UAE, "
            "and sanctioned regions). Any product you build must respect geo eligibility — do not design as if all "
            "Robinhood app users can freely hold Stock Tokens.",
            styles["body"],
        )
    )

    story.append(p("1.4 Developer &amp; Platform Properties", styles["h2"]))
    for item in [
        "<b>Permissionless:</b> Anyone can interact, deploy contracts, and build apps without platform lock-in.",
        "<b>EVM compatible:</b> Solidity/Vyper contracts deploy without modification; Hardhat, Foundry, ethers.js, viem, Wagmi work out of the box.",
        "<b>Account abstraction (ERC-4337):</b> Gas sponsorship, batching, session keys, programmable wallets.",
        "<b>AI-native narrative:</b> Agents intended to trade, swap, lend, and transact with tokenized RWAs under human guardrails.",
        "<b>Official products tied to chain:</b> Stock Tokens in Robinhood Wallet (eligible regions), Robinhood Earn (Morpho/USDG lending for eligible US users), perps integrations (e.g. Lighter) in wallet for eligible jurisdictions.",
    ]:
        story.append(p(f"•  {item}", styles["bullet"]))

    story.append(PageBreak())

    # ========== SECTION 2 ==========
    story.append(p("2. Official Ecosystem &amp; Day-One Partners", styles["h1"]))
    story.append(green_hr())
    story.append(
        p(
            "Robinhood’s official ecosystem page and documentation emphasize <b>infrastructure, trading, and lending</b> — "
            "not social media. Day-one and documented partners include:",
            styles["body"],
        )
    )

    story.append(p("2.1 Partner Matrix (from docs / newsroom / ecosystem page)", styles["h2"]))
    story.append(
        make_table(
            ["Category", "Partner", "Role / Notes"],
            [
                ["Public DEX / AMM", "Uniswap", "Primary public liquidity protocol (v2/v3/v4, Uniswap X cited in coverage)"],
                ["Prop AMM / RWA venue", "Pleiades / Rialto", "Proprietary AMM / prop trading venue for RWA-style flow"],
                ["Perps DEX", "Lighter", "Perps in Robinhood Wallet; $11M $LIT community commitment reported"],
                ["Perps / spot DEX", "Arcus", "Spot &amp; perps across equity, commodity, crypto markets"],
                ["Lending", "Morpho", "Powers Robinhood Earn (USDG lending, ~7% APY narrative for eligible US users)"],
                ["Oracles", "Chainlink", "Price feeds &amp; data for tokenization / DeFi"],
                ["Bridge / messaging", "LayerZero", "Omnichain messaging and asset bridging"],
                ["Canonical bridge", "Arbitrum Bridge", "ETH and assets onto Robinhood Chain"],
                ["RPC / AA / gasless", "Alchemy", "Recommended RPC, Data API, gasless / AA infrastructure"],
                ["Custody", "BitGo, Fireblocks", "Institutional digital asset operations"],
                ["Analytics", "Allium", "Onchain data and analytics"],
                ["Token tracking", "CoinGecko", "Price and volume tracking"],
                ["Wallet data", "Zerion", "Enterprise-grade wallet data API"],
                ["Compliance / risk", "TRM Labs", "Analytics and risk management"],
                ["Stablecoin", "Paxos (USDG)", "Dollar-backed stablecoin infrastructure"],
                ["Exchange / onramp", "Bitstamp by Robinhood", "Institutional crypto exchange &amp; prime services"],
                ["Base tech", "Arbitrum / Offchain Labs", "Dedicated blockchain / rollup stack"],
            ],
            col_widths=[1.5 * inch, 1.5 * inch, 3.8 * inch],
        )
    )
    story.append(p("Table: Official / documented ecosystem partners.", styles["caption"]))

    story.append(p("2.2 Robinhood Product Launches Alongside Chain (July 2026)", styles["h2"]))
    for item in [
        "<b>Stock Tokens (new generation)</b> — 24/7 trading onchain for eligible users in 120+ countries (availability varies); composable into DeFi (lending, collateral).",
        "<b>Classic Stock Tokens</b> — continue in Robinhood Europe app as derivative-style products.",
        "<b>Robinhood Earn</b> — decentralized lending of USDG via Morpho in self-custody wallet; insurance narrative via Lloyd’s / RELM for certain covered losses.",
        "<b>Perps in Wallet</b> — Lighter integration; points multipliers for trading via Robinhood Wallet.",
        "<b>Agentic trading expansion</b> — AI agents for equities/options already; crypto agentic accounts planned with human capital/guardrail control.",
        "<b>Global expansion</b> — Canada crypto launch (WonderFi), UK crypto planned, Singapore CMS licence step, EU perps expansion (commodities, ETF, FX).",
    ]:
        story.append(p(f"•  {item}", styles["bullet"]))

    story.append(p("2.3 Early Chain Metrics (public / CT, approximate)", styles["h2"]))
    story.append(
        p(
            "Testnet reportedly processed ~<b>4 million transactions in the first week</b> (Vlad Tenev, Feb 2026). "
            "Mainnet (~3 weeks old in late July 2026) is still early: community analyses cite on the order of "
            "<b>~500k cumulative addresses</b> and very low penetration of Robinhood’s ~28M funded accounts. "
            "One CT analysis framed chain gross revenue early on as hundreds of thousands of dollars with "
            "Arbitrum middleware / Ethereum settlement fee splits — treat all third-party metrics as unverified snapshots.",
            styles["body"],
        )
    )
    story.append(
        p(
            "<b>Important:</b> Robinhood has <b>not announced a native RH Chain token</b>. Gas is ETH. Be wary of "
            "unofficial “Robinhood coins” marketed as official.",
            styles["body"],
        )
    )

    story.append(PageBreak())

    # ========== SECTION 3 ==========
    story.append(p("3. Grassroots / Early Community Projects (from X)", styles["h1"]))
    story.append(green_hr())
    story.append(
        p(
            "Outside the official partner list, Twitter/X activity (the main crypto discovery surface) shows a "
            "typical new-L2 pattern: <b>memecoins, launchpads, SocialFi clones, GameFi experiments, and thin DeFi</b>. "
            "Quality is uneven; many posts are hype or shill. Below are projects that appeared as product-shaped "
            "efforts rather than pure tickers.",
            styles["body"],
        )
    )

    story.append(
        make_table(
            ["Project", "Category", "Description (as claimed on X / web)"],
            [
                [
                    "GreenTown Social",
                    "SocialFi",
                    "Claims first SocialFi on RH Chain: creator keys, GreenSwap, launchpad, referrals, lifetime trading-fee earnings. Friend.tech-style model.",
                ],
                [
                    "The Arena",
                    "SocialFi / launchpad",
                    "Creator coins &amp; trading tools with prior Avalanche experience; expanding with Robinhood Chain launchpad.",
                ],
                [
                    "HoodFrens",
                    "SocialFi / fantasy",
                    "Creator cards, series, tournaments — fantasy/social card model on RH Chain.",
                ],
                [
                    "Nicehood",
                    "Launchpad",
                    "Permissionless memecoin launches, AI creation tools, creator-first rewards; team reportedly pivoted from prior SocialFi.",
                ],
                [
                    "Bowline",
                    "Lending / credit",
                    "Lending for tokenized stocks + crypto collateral; onchain wallet credit score (300–850); AI agent borrow API / x402-style pay-per-call narrative.",
                ],
                [
                    "SendrPrivacy",
                    "Privacy payments",
                    "Privacy-first payments (hide sender wallet from recipient by default); roadmap for private RWA trading / payouts.",
                ],
                [
                    "Cardena",
                    "GameFi",
                    "Collectible card battles / GameFi ecosystem native to Robinhood Chain.",
                ],
                [
                    "Sherwood",
                    "Onchain game / fair launch",
                    "Provably fair archery mini-game / fair-launch sport; no house narrative; LP burn claims.",
                ],
                [
                    "HOOD//LAUNCH &amp; token launchers",
                    "Tooling",
                    "Community bounties to build token launcher factories (e.g. mandatory pairing with community tokens like $HOODIE).",
                ],
                [
                    "Misc memecoins",
                    "Memes",
                    "Many tickers ($HMM, $NOXA, $YIELDFY, $r/DOG, $RWOG, etc.) with high volume claims — high noise, high scam risk.",
                ],
            ],
            col_widths=[1.4 * inch, 1.2 * inch, 4.2 * inch],
        )
    )
    story.append(p("Table: Grassroots projects observed in July 2026 research (not endorsements).", styles["caption"]))

    story.append(
        p(
            "<b>Honest read of X:</b> Most activity is memecoins + SocialFi clones + launchpads. Official partners "
            "are DEX, perps, lending, custody. <b>Social is underserved at quality, overserved at copycats.</b>",
            styles["body"],
        )
    )

    story.append(PageBreak())

    # ========== SECTION 4 ==========
    story.append(p("4. Social Apps Building on Robinhood Chain", styles["h1"]))
    story.append(green_hr())
    story.append(
        p(
            "<b>Yes — but immature.</b> There is no official Robinhood social graph product. Early SocialFi is bottom-up.",
            styles["body"],
        )
    )

    story.append(p("4.1 What Exists Today", styles["h2"]))
    for item in [
        "<b>Keys / creator coins</b> — GreenTown ≈ Friend.tech model (buy access / speculation on people).",
        "<b>Launchpad + social feed</b> — Nicehood, Arena-style creator launch flows.",
        "<b>Creator cards / fantasy SocialFi</b> — HoodFrens tournaments and collectible creator cards.",
        "<b>Community builders groups</b> — informal “Robinhood Builders” media/podcast/launchpad communities on X (not official).",
    ]:
        story.append(p(f"•  {item}", styles["bullet"]))

    story.append(p("4.2 Quality &amp; Retention Reality", styles["h2"]))
    story.append(
        p(
            "Quality bar is low. Retention models resemble 2023–24 Base SocialFi cycles: <b>spike → fee harvest → decay</b>. "
            "If you only build “another Friend.tech on RH,” you are <b>late to a crowded free-for-all</b>, not early to a unique wedge. "
            "GreenTown reportedly claimed rapid user/volume spikes in early days (e.g. multi-thousand users, ETH TVL swings) — "
            "typical of speculative SocialFi, not proof of durable PMF.",
            styles["body"],
        )
    )

    story.append(p("4.3 Why Social Still Matters on This Chain", styles["h2"]))
    story.append(
        p(
            "Even though HQ focuses on RWA/DeFi, every new L2 needs attention loops. The winning social products on "
            "Robinhood Chain will likely be <b>social finance</b> (trading, rooms around assets, copy desks) rather than "
            "generic posting — because Robinhood users already think in portfolios and prices, not timelines.",
            styles["body"],
        )
    )

    story.append(PageBreak())

    # ========== SECTION 5 ==========
    story.append(p("5. Crypto Social Platforms Comparison", styles["h1"]))
    story.append(green_hr())
    story.append(
        p(
            "Understanding Friend.tech, Farcaster, Lens/Hey.xyz (and discovery-style SocialFi) is essential before "
            "copying any model onto Robinhood Chain.",
            styles["body"],
        )
    )

    story.append(p("5.1 Platform Comparison Table", styles["h2"]))
    story.append(
        make_table(
            ["Platform", "Core model", "How money works", "Strength", "Failure mode"],
            [
                [
                    "Friend.tech",
                    "Buy <b>keys</b> on a bonding curve for chat access to a person (often X-linked)",
                    "~10% fee on key trades, split protocol + creator → strong revenue in hype",
                    "Cashflow when speculative demand is hot; simple UX for CT",
                    "Retention dies when key prices dump; “chat for whales,” not durable social network",
                ],
                [
                    "Farcaster / Warpcast",
                    "Decentralized <b>protocol + clients</b>; identity onchain, content mostly offchain hubs; Frames for interactive posts",
                    "Storage/hosting fees, developer fees on Frames, low per-post costs",
                    "Real social UX, portable graph, developer ecosystem",
                    "Harder protocol-level cashflow; growth is product-led over years",
                ],
                [
                    "Lens / Hey.xyz",
                    "Onchain <b>social graph</b> (profiles, follows, publications as NFT/modules)",
                    "Account fees, module fees, royalties, protocol take on modules",
                    "Composable social primitives; multi-client ecosystem",
                    "UX/gas/complexity; monetization more fragmented",
                ],
                [
                    "Discovery SocialFi",
                    "Feed + ranking of people/tokens/rooms; often wraps trading",
                    "Trading fees, boosts, ads, tips",
                    "Attention → trade conversion",
                    "Without unique content/graph, becomes a pure pump channel",
                ],
            ],
            col_widths=[1.0 * inch, 1.6 * inch, 1.5 * inch, 1.3 * inch, 1.4 * inch],
        )
    )
    story.append(p("Table: SocialFi / DeSoc models relevant to builders.", styles["caption"]))

    story.append(p("5.2 How Friend.tech Works (detail)", styles["h2"]))
    for item in [
        "User links social identity (historically X) and uses an app-generated wallet funded with ETH (on Base historically).",
        "Users buy and sell <b>keys</b> (formerly “shares”) for a subject; price set by a <b>bonding curve</b> (more keys → higher price).",
        "Holding keys unlocks private group chat / access to that person.",
        "Each trade typically incurs a ~<b>10% fee</b> split between protocol and the subject — this is the core revenue engine.",
        "Historically generated very high protocol revenue during 2023–24 hype (tens of millions USD equivalent reported in analyses) but suffered sharp engagement and price collapses.",
        "V2 experiments (clubs, token models) tried to extend lifecycle; sustainability of pure key speculation remains the open question.",
    ]:
        story.append(p(f"•  {item}", styles["bullet"]))

    story.append(p("5.3 How Farcaster Works (detail)", styles["h2"]))
    for item in [
        "Shared protocol; multiple clients (e.g. Warpcast) can read/write the same social graph.",
        "Onchain identity / registry pieces; content distributed via hubs (hybrid architecture).",
        "<b>Frames</b>: interactive mini-apps inside posts (vote, mint, transact) — social becomes a surface for software.",
        "Monetization leans on storage, hosting, developer Frame fees — less “casino,” more “network.”",
        "Stronger stickiness narrative than Friend.tech in many comparisons; weaker short-term protocol profit printing.",
    ]:
        story.append(p(f"•  {item}", styles["bullet"]))

    story.append(p("5.4 How Lens / Hey.xyz Works (detail)", styles["h2"]))
    for item in [
        "Profiles and social actions as onchain (or module-driven) primitives — ownable graph.",
        "Developers build clients (Hey.xyz is a major client historically) on shared protocol data.",
        "Revenue via account creation fees, collect/module economics, royalties on secondary activity.",
        "Philosophy: portability and composability over single-app lock-in.",
        "Tradeoff: more blockchain complexity for users vs pure Web2 social UX.",
    ]:
        story.append(p(f"•  {item}", styles["bullet"]))

    story.append(p("5.5 Mental Model for Builders", styles["h2"]))
    story.append(
        make_table(
            ["Dimension", "Speculative SocialFi (Friend.tech-like)", "Protocol Social (Farcaster / Lens)"],
            [
                ["Revenue", "High, bursty (trading fees on keys/coins)", "Slower, stickier (storage, modules, Frames)"],
                ["Primary users", "Traders + KOLs", "Posters + communities + builders"],
                ["Moat", "Liquidity + creator FOMO", "Graph + clients + habits"],
                ["Risk", "Dies with market cycles", "Never reaches escape velocity / cold start"],
                ["Build cost of copy", "Low (bonding curve + chat)", "High (graph, clients, moderation, hubs)"],
                ["Fit on RH Chain", "Crowded already (GreenTown etc.)", "Underserved but needs unfair distribution"],
            ],
            col_widths=[1.4 * inch, 2.7 * inch, 2.7 * inch],
        )
    )
    story.append(p("Table: Builder mental model — pick deliberately, don’t hybridize accidentally.", styles["caption"]))

    story.append(
        p(
            "<b>Cashflow truth:</b> Friend.tech-type products can print money during hype. Farcaster/Lens win more on "
            "retention and brand but need years and distribution. Pure “Twitter clone onchain” almost never becomes "
            "cashflow-positive without a <b>financial primitive</b> (keys, tips, trading, launches, paid access).",
            styles["body"],
        )
    )

    story.append(PageBreak())

    # ========== SECTION 6 ==========
    story.append(p("6. Grant &amp; Funding Reality", styles["h1"]))
    story.append(green_hr())

    story.append(p("6.1 Robinhood-Specific Funding", styles["h2"]))
    story.append(
        make_table(
            ["Source", "Status / Detail"],
            [
                [
                    "Dedicated “Robinhood Chain Grants” portal",
                    "<b>Not publicly launched</b> as a standing open grant program (as of this research).",
                ],
                [
                    "Arbitrum Open House 2026",
                    "Robinhood committed <b>$1M in prizes</b> for builders on RH Chain testnet/mainnet. "
                    "Buildathons: New York, Dubai, London, Singapore + founder houses. Sign up: openhouse.arbitrum.io",
                ],
                [
                    "Direct developer contact",
                    "Docs list <b>chain-developers-group@robinhood.com</b> — BD / ecosystem path, not a formal grant form.",
                ],
                [
                    "Robin Hood Foundation (NYC charity)",
                    "<b>Unrelated</b> to the blockchain. Do not apply there for chain grants (poverty-fighting NYC nonprofits).",
                ],
                [
                    "Ecosystem listing",
                    "robinhood.com/chain/ecosystem — inclusion is not endorsement; still useful distribution if listed.",
                ],
            ],
            col_widths=[2.2 * inch, 4.6 * inch],
        )
    )
    story.append(p("Table: Robinhood-adjacent funding and support channels.", styles["caption"]))

    story.append(p("6.2 Adjacent Funding That Fits RH Builders", styles["h2"]))
    story.append(
        make_table(
            ["Program", "Why it matters", "Notes"],
            [
                [
                    "Arbitrum Foundation Grants",
                    "RH Chain is Arbitrum tech — strong narrative fit",
                    "Rolling applications; milestone-based. Typical public ranges often cited ~$20k–$150k ARB for dApps. arbitrum.foundation/grants",
                ],
                [
                    "Arbitrum Audit Subsidy",
                    "Offsets security costs for real contracts",
                    "Apply if shipping production DeFi/social contracts",
                ],
                [
                    "Alchemy / infra partners",
                    "Credits, RPC, AA, co-marketing",
                    "Useful if you drive gasless UX and active users",
                ],
                [
                    "Chainlink community grants",
                    "If you hard-depend on oracles for RWA pricing",
                    "Fits tokenization / advanced DeFi use cases",
                ],
                [
                    "Circle developer grants",
                    "USDC / real-world payment flows",
                    "Less native than USDG on RH narrative, still relevant for payments",
                ],
            ],
            col_widths=[1.8 * inch, 2.2 * inch, 2.8 * inch],
        )
    )
    story.append(p("Table: Non-Robinhood grant programs relevant to RH Chain builders.", styles["caption"]))

    story.append(p("6.3 Funding Strategy Bottom Line", styles["h2"]))
    story.append(
        p(
            "There is <b>no rich, easy “Robinhood grant form”</b> today. There <b>is</b> a <b>$1M Open House prize narrative</b>, "
            "<b>Arbitrum grants</b>, and a <b>BD email</b>. Design the product so Robinhood <i>wants</i> to showcase it "
            "(RWA utility, Earn, Wallet, agents) — that beats waiting for a grant portal.",
            styles["body"],
        )
    )

    story.append(PageBreak())

    # ========== SECTION 7 ==========
    story.append(p("7. What Not to Build", styles["h1"]))
    story.append(green_hr())
    story.append(
        p(
            "If the goal is <b>cashflow + grants + real traction</b>, avoid these traps:",
            styles["body"],
        )
    )
    story.append(
        make_table(
            ["#", "Avoid", "Why"],
            [
                ["1", "Generic Twitter clone", "No graph, no distribution, no sticky fees"],
                ["2", "Plain Friend.tech fork", "GreenTown / Arena already racing that lane"],
                ["3", "Random memecoin as “the business”", "Volume ≠ durable business; reputation risk next to Robinhood brand"],
                ["4", "US Stock Token products for US users", "Stock Tokens are geo-restricted; compliance risk"],
                ["5", "Empty “AI wrapper”", "“AI agent” is marketing unless it executes safe, paid workflows with guardrails"],
                ["6", "Token-first no product", "Harder to get grants/BD; easier to look like a scam in a retail-branded ecosystem"],
            ],
            col_widths=[0.4 * inch, 2.0 * inch, 4.4 * inch],
        )
    )
    story.append(p("Table: Anti-patterns for RH Chain founders.", styles["caption"]))

    # ========== SECTION 8 ==========
    story.append(p("8. What You Should Build", styles["h1"]))
    story.append(green_hr())
    story.append(
        p(
            "Guiding principle: <b>Robinhood users think in portfolios and prices, not posts.</b> "
            "Social only works here if it is <b>social finance</b>, not social media cosplay.",
            styles["body"],
        )
    )

    story.append(p("Tier A — Best Fit (Cashflow + Ecosystem Love + Grant Angle)", styles["h2"]))

    story.append(p("A1. Social trading / copy desks for Stock Tokens + perps", styles["tier_title"]))
    for item in [
        "<b>What:</b> Follow wallets/creators; mirror trades (or sell “signal packs”) on Stock Tokens / Lighter–Arcus style markets; creator earns fee on copy volume.",
        "<b>Why RH:</b> Matches RWA + 24/7 trading thesis; Wallet-native habit.",
        "<b>Revenue:</b> 10–30% of performance or copy fees; Pro desk subscriptions; API for agents.",
        "<b>Grant story:</b> “Brings Robinhood retail into onchain RWA with social proof and safer defaults.”",
        "<b>Lessons:</b> eToro-style copy UX + crypto transparency; avoid pure key speculation.",
    ]:
        story.append(p(f"•  {item}", styles["bullet"]))

    story.append(p("A2. Portfolio rooms / “House” for RWA communities", styles["tier_title"]))
    for item in [
        "<b>What:</b> Rooms tied to <b>assets</b> (e.g. $NVDA room), not only people. Chat + shared watchlists + optional paid tiers + tip rails in USDG/ETH.",
        "<b>Why RH:</b> Differentiates from GreenTown (people-keys) and Farcaster (general social).",
        "<b>Revenue:</b> Room subscriptions, boosts, take-rate on tips/swaps inside room, premium analytics.",
        "<b>Stickiness:</b> Asset identity &gt; influencer identity when prices move 24/7.",
        "<b>Hybrid model:</b> Lens-like community UX + Friend.tech-like monetization only where it fits (paid access), not pure bonding-curve casino.",
    ]:
        story.append(p(f"•  {item}", styles["bullet"]))

    story.append(p("A3. Agent marketplace for trading policies (AI-native)", styles["tier_title"]))
    for item in [
        "<b>What:</b> Users rent/run guardrailed agents (DCA Stock Tokens, rebalance, lend idle USDG on Morpho, stop-loss). Humans set caps.",
        "<b>Why RH:</b> They market “AI-native” + agentic trading explicitly.",
        "<b>Revenue:</b> SaaS monthly + % of AUM or per-execution fee.",
        "<b>Grant story:</b> Showcases account abstraction, gas sponsorship, safe agent UX for retail.",
    ]:
        story.append(p(f"•  {item}", styles["bullet"]))

    story.append(p("A4. RWA-aware launchpad / vault factory", styles["tier_title"]))
    for item in [
        "<b>What:</b> Not pure memes — tokenized strategies (index baskets where legal, yield wrappers on Morpho, structured products).",
        "<b>Revenue:</b> Launch fee + swap fee + vault performance fee.",
        "<b>Compete carefully:</b> Nicehood owns meme mindshare; win on compliance-aware UX and RWA, not another pump.fun.",
    ]:
        story.append(p(f"•  {item}", styles["bullet"]))

    story.append(p("Tier B — Solid Cashflow Tools (Faster to Ship)", styles["h2"]))
    story.append(
        make_table(
            ["Idea", "Revenue model", "Why it works on RH"],
            [
                [
                    "Stock Token + DeFi portfolio tracker (tax/PnL, basis, 24/7 marks)",
                    "Freemium + Pro subscription + B2B API",
                    "Retail needs this day one",
                ],
                [
                    "Smart routing UI across Uniswap / Rialto / aggregators",
                    "Swap fee share",
                    "Volume = cash; ST + stables path",
                ],
                [
                    "Credit score / undercollateralized UX on lending (Bowline-like)",
                    "Referral + premium features",
                    "Lending is core RH Earn narrative",
                ],
                [
                    "Compliance-friendly onboarding for non-US creators (ST eligibility)",
                    "Lead-gen + paid checklists / B2B tools",
                    "Trust product Robinhood can list",
                ],
            ],
            col_widths=[2.6 * inch, 2.0 * inch, 2.2 * inch],
        )
    )
    story.append(p("Table: Tier B product ideas.", styles["caption"]))

    story.append(p("Tier C — Social Only If You Have Unfair Distribution", styles["h2"]))
    for item in [
        "Friend.tech clone with keys",
        "Fantasy SocialFi cards",
        "Generic creator-coin launchpad",
    ]:
        story.append(p(f"•  {item}", styles["bullet"]))
    story.append(
        p(
            "Only pursue Tier C if you already have a <b>large X audience</b> or exclusive KOL pipeline. "
            "Otherwise fees go to zero after week two.",
            styles["body"],
        )
    )

    story.append(PageBreak())

    # ========== SECTION 9 ==========
    story.append(p("9. Recommended Product Thesis &amp; Competitive Map", styles["h1"]))
    story.append(green_hr())

    story.append(p("9.1 One-Sentence Thesis", styles["h2"]))
    story.append(
        p(
            "Build the social layer for <b>capital markets</b> on Robinhood Chain — rooms, copy desks, and agents "
            "around Stock Tokens and yield — monetized by trading/subscription fees, not by posts.",
            styles["quote"],
        )
    )
    story.append(
        p(
            "This aligns with: (1) official chain purpose (RWA + DeFi + AI), (2) cashflow (fees on capital movement), "
            "(3) traction (Robinhood mental model = money), (4) grants/BD (fill the empty middle of the funnel between Wallet and Uniswap).",
            styles["body"],
        )
    )

    story.append(p("9.2 Single Recommended MVP: “Copy Desk + Asset Rooms”", styles["h2"]))
    for item in [
        "Rooms per ticker/theme (asset-native social).",
        "Creators publish trade ideas with optional auto-copy.",
        "Protocol takes fee on copy/execution.",
        "Optional AI agent that only executes inside user-set risk rails.",
        "Pitch to Robinhood: the social layer that makes Stock Tokens and onchain Earn understandable for retail.",
        "Fundable, defensible vs pure SocialFi clones, aligned with how this chain wants to grow.",
    ]:
        story.append(p(f"•  {item}", styles["bullet"]))

    story.append(p("9.3 Competitive Map (Social / Finance on RH)", styles["h2"]))
    story.append(
        make_table(
            ["Quadrant", "Examples", "Notes"],
            [
                [
                    "High speculation",
                    "Nicehood / meme launchpads, GreenTown keys",
                    "Crowded; fee revenue possible but fragile",
                ],
                [
                    "Mid speculation social",
                    "HoodFrens cards, Arena creator coins",
                    "Entertainment + trading hybrid; retention TBD",
                ],
                [
                    "★ Empty high-value wedge",
                    "Social trading + RWA rooms + agents",
                    "Utility social finance — best cashflow + BD fit",
                ],
                [
                    "Low speculation / high utility",
                    "Portfolio tools, Morpho frontends, Bowline credit",
                    "Solid SaaS; less viral, more durable",
                ],
            ],
            col_widths=[1.8 * inch, 2.4 * inch, 2.6 * inch],
        )
    )
    story.append(p("Table: Where to position on the RH social/finance map.", styles["caption"]))

    # ========== SECTION 10 ==========
    story.append(p("10. Go-to-Market for Grants + Users", styles["h1"]))
    story.append(green_hr())
    steps = [
        "<b>Ship a thin MVP in 4–6 weeks</b> on mainnet: one asset room + portfolio view + one paid action (copy trade or subscription).",
        "<b>Apply in parallel</b> to Arbitrum Open House / Foundation grants with a RH-specific pitch (problem, metric, demo, milestones).",
        "<b>Email</b> chain-developers-group@robinhood.com with live metrics (users, volume, retention); ask for ecosystem page consideration and Wallet deep-link discussion.",
        "<b>Geo-design</b>: Non-US Stock Token flows + global crypto/USDG flows. Never pretend US users can hold Stock Tokens if they cannot.",
        "<b>Pick one monetization metric day one</b>: fee revenue per week — not “followers.”",
        "<b>Avoid token first.</b> Product + fees first; token only if you need liquidity bootstrapping later.",
        "<b>Use AA + gas sponsorship</b> (Alchemy) so retail onboarding feels app-like, matching Robinhood UX standards.",
        "<b>Compliance posture</b>: clear disclaimers, no investment advice framing, jurisdiction gates for RWA features.",
    ]
    for i, step in enumerate(steps, 1):
        story.append(p(f"<b>{i}.</b>  {step}", styles["bullet"]))

    story.append(PageBreak())

    # ========== SECTION 11 ==========
    story.append(p("11. Network Configuration &amp; Developer Resources", styles["h1"]))
    story.append(green_hr())

    story.append(p("11.1 Network Parameters", styles["h2"]))
    story.append(
        make_table(
            ["Property", "Mainnet", "Testnet"],
            [
                ["Chain ID", "4663", "46630"],
                ["Currency", "ETH", "ETH"],
                [
                    "Block explorer",
                    "robinhoodchain.blockscout.com",
                    "explorer.testnet.chain.robinhood.com",
                ],
                [
                    "Public RPC (rate-limited)",
                    "https://rpc.mainnet.chain.robinhood.com",
                    "https://rpc.testnet.chain.robinhood.com",
                ],
                [
                    "Recommended RPC",
                    "Alchemy robinhood-mainnet",
                    "Alchemy robinhood-testnet",
                ],
            ],
            col_widths=[1.8 * inch, 2.5 * inch, 2.5 * inch],
        )
    )
    story.append(p("Table: Network config from official docs.", styles["caption"]))

    story.append(p("11.2 Key Links", styles["h2"]))
    links = [
        ("Chain homepage", "https://robinhood.com/us/en/chain/"),
        ("Ecosystem", "https://robinhood.com/us/en/chain/ecosystem/"),
        ("Documentation", "https://docs.robinhood.com/chain/"),
        ("Connecting / RPC", "https://docs.robinhood.com/chain/connecting/"),
        ("Newsroom mainnet announcement", "https://robinhood.com/us/en/newsroom/robinhood-accelerates-global-expansion-robinhood-chain-mainnet-stock-tokens-agentic-trading/"),
        ("Arbitrum Open House", "https://openhouse.arbitrum.io/"),
        ("Arbitrum Foundation Grants", "https://arbitrum.foundation/grants"),
        ("Arbitrum RH Chain testnet blog", "https://blog.arbitrum.io/robinhood-chain-testnet/"),
        ("Developer email", "chain-developers-group@robinhood.com"),
        ("Bridge (Arbitrum portal)", "https://portal.arbitrum.io/bridge"),
    ]
    for name, url in links:
        story.append(p(f"•  <b>{name}:</b> {url}", styles["bullet"]))

    story.append(p("11.3 Stack Recommendations for Builders", styles["h2"]))
    for item in [
        "Solidity + Foundry/Hardhat (EVM standard).",
        "Frontend: Next.js / Wagmi / viem + WalletConnect / Robinhood Wallet deep links where available.",
        "AA / gasless: Alchemy gasless transaction infrastructure.",
        "Oracles for prices: Chainlink where available on chain.",
        "Liquidity integrations: Uniswap first; be aware of prop venues (Rialto/Pleiades).",
        "Yield rails: Morpho / USDG where product scope allows.",
        "Indexing: Alchemy Data API, Allium, or custom indexers for social/trading feeds.",
    ]:
        story.append(p(f"•  {item}", styles["bullet"]))

    # ========== SECTION 12 ==========
    story.append(p("12. Honest Summary Matrix", styles["h1"]))
    story.append(green_hr())
    story.append(
        make_table(
            ["Question", "Answer"],
            [
                ["Is RH Chain real?", "Yes — live L2, serious partners, RWA focus."],
                ["Is social “the” opportunity?", "Social media: no. Social finance: yes."],
                [
                    "Who’s building social now?",
                    "GreenTown, Arena, HoodFrens, Nicehood — early and thin quality.",
                ],
                [
                    "Official grants from Robinhood?",
                    "No clear open grant portal; $1M Open House + BD email.",
                ],
                [
                    "Best adjacent funding?",
                    "Arbitrum Foundation grants + Open House prizes.",
                ],
                [
                    "Path to cashflow?",
                    "Fees on trades, copies, vaults, subscriptions — not ads on a feed.",
                ],
                [
                    "Path to traction?",
                    "Ride Stock Tokens + Earn + Wallet distribution, not CT memecoins alone.",
                ],
                [
                    "Native chain token?",
                    "Not announced; gas is ETH. Distrust “official” fake tokens.",
                ],
                [
                    "US users &amp; Stock Tokens?",
                    "Stock Tokens not available in US / to US persons.",
                ],
                [
                    "Best single product bet",
                    "Copy Desk + Asset Rooms with optional guardrailed agents.",
                ],
            ],
            col_widths=[2.2 * inch, 4.6 * inch],
        )
    )
    story.append(p("Table: Executive answers at a glance.", styles["caption"]))

    story.append(PageBreak())

    # ========== SECTION 13 ==========
    story.append(p("13. Sources &amp; Further Links", styles["h1"]))
    story.append(green_hr())
    story.append(
        p(
            "Primary sources used in this synthesis (verify latest state before decisions):",
            styles["body"],
        )
    )
    sources = [
        "Robinhood Chain docs — About, Connecting, Bridging, Deploy contracts (docs.robinhood.com/chain)",
        "Robinhood Chain product page (robinhood.com/us/en/chain/)",
        "Robinhood Chain ecosystem directory (robinhood.com/us/en/chain/ecosystem/)",
        "Robinhood newsroom — “Accelerates Global Expansion…” July 1, 2026",
        "Arbitrum blog — Robinhood Chain testnet &amp; $1M Open House commitment (Feb 2026)",
        "CoinDesk, Forbes, The Block, Yahoo Finance coverage of mainnet / testnet",
        "X posts from @RobinhoodApp, @vladtenev, ecosystem projects, CT analysts",
        "Public SocialFi research comparing Friend.tech, Farcaster, Lens (Dune-cited analyses, industry writeups)",
        "Arbitrum Foundation grants pages (arbitrum.foundation/grants)",
    ]
    for s in sources:
        story.append(p(f"•  {s}", styles["bullet"]))

    story.append(Spacer(1, 0.3 * inch))
    story.append(green_hr())
    story.append(p("Closing Recommendation", styles["h2"]))
    story.append(
        p(
            "Robinhood Chain is a <b>finance-first L2 with retail distribution potential</b>, not a social protocol. "
            "The open opportunity is the missing middle: products that make Stock Tokens, Earn, and perps socially "
            "legible and monetized through real capital movement. Ship fees early, respect geo rules, apply to "
            "Arbitrum funding paths, and pitch Robinhood ecosystem BD with metrics — not memes.",
            styles["body"],
        )
    )
    story.append(Spacer(1, 0.25 * inch))
    story.append(
        p(
            "— End of report —",
            ParagraphStyle(
                "end",
                fontName="Helvetica-Oblique",
                fontSize=9,
                textColor=GRAY,
                alignment=TA_CENTER,
                spaceBefore=12,
            ),
        )
    )
    story.append(
        p(
            "This document is a research synthesis for educational and product-planning purposes only. "
            "It is not an offer, solicitation, or recommendation to buy or sell any asset or to build any unlicensed financial product.",
            ParagraphStyle(
                "end2",
                fontName="Helvetica",
                fontSize=7.5,
                leading=10,
                textColor=GRAY,
                alignment=TA_CENTER,
                spaceBefore=8,
            ),
        )
    )

    # Build PDF
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.7 * inch,
        title="Robinhood Chain Deep Research Report",
        author="Research Synthesis",
        subject="Robinhood Chain ecosystem, SocialFi, grants, product recommendations",
    )
    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    print(f"Wrote: {OUT}")
    return OUT


if __name__ == "__main__":
    build()
