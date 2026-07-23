#!/usr/bin/env python3
"""Generate PDF: Grants & funding guide for Earn/Morpho yield explorer on RH Chain."""

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

OUT = Path(__file__).resolve().parent / "Earn_Morpho_Grants_Funding_Guide.pdf"

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


def ghr():
    return HRFlowable(width="100%", thickness=2, color=HOOD, spaceBefore=2, spaceAfter=9)


def hr():
    return HRFlowable(width="100%", thickness=0.6, color=MID, spaceBefore=3, spaceAfter=7)


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
    canvas.drawString(0.65 * inch, letter[1] - 0.35 * inch, "Earn / Morpho Product — Grants & Funding Guide")
    canvas.drawRightString(letter[0] - 0.65 * inch, letter[1] - 0.35 * inch, "Arbitrum · Open House · Morpho · RH")
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
            "●  FUNDING STRATEGY",
            ParagraphStyle(
                "badge", fontName="Helvetica-Bold", fontSize=9,
                textColor=HOOD, alignment=TA_CENTER, spaceAfter=14,
            ),
        )
    )
    story.append(
        P(
            "Grants &amp; Funding Guide",
            ParagraphStyle(
                "t", fontName="Helvetica-Bold", fontSize=24, leading=30,
                textColor=DARK, alignment=TA_CENTER, spaceAfter=6,
            ),
        )
    )
    story.append(
        P(
            "Earn / Morpho Yield &amp; Risk Intelligence SaaS<br/>on Robinhood Chain",
            ParagraphStyle(
                "st", fontName="Helvetica", fontSize=12, leading=16,
                textColor=GRAY, alignment=TA_CENTER, spaceAfter=14,
            ),
        )
    )
    story.append(ghr())
    story.append(
        P(
            "Can you get a grant? Where to apply · Odds · Pitch angles · Application outline · Action order",
            ParagraphStyle(
                "p", fontName="Helvetica", fontSize=9.5, leading=13,
                textColor=SLATE, alignment=TA_CENTER, spaceAfter=16,
            ),
        )
    )
    story.append(
        box(
            "Short answer",
            "Yes — you can chase funding for this product. Best fits: <b>Arbitrum Foundation grants</b> "
            "(Infrastructure &amp; Tools / dApps) and <b>Arbitrum Open House</b> prizes (Robinhood committed $1M "
            "toward RH Chain builder support). Morpho DAO/ecosystem grants when rounds are open. "
            "There is <b>no public Robinhood Chain grant form</b> — use BD email instead. "
            "Ship MVP first; grants fund shipping teams, not slides.",
        )
    )
    story.append(Spacer(1, 0.2 * inch))
    story.append(
        P(
            "<b>Product:</b> Morpho vault explorer · Robinhood Earn risk/APY intelligence · portfolio · alerts<br/>"
            "<b>Compiled:</b> July 2026 &nbsp;·&nbsp; <b>Disclaimer:</b> Not financial, legal, or fundraising advice. "
            "Programs change; verify links and open rounds before applying.",
            s["small"],
        )
    )
    story.append(PageBreak())

    # TOC
    story.append(P("Table of Contents", s["h1"]))
    story.append(ghr())
    for item in [
        "1. Executive Answer",
        "2. Why This Product Is Fundable",
        "3. Funding Sources (Ranked Best → Weaker)",
        "4. Honest Odds Matrix",
        "5. How to Maximize Chances (Action Order)",
        "6. Grant Application Outline (Copy Framework)",
        "7. Pitch Angles by Funder",
        "8. What Not to Expect",
        "9. Practical Recommendation",
        "10. Checklist Before You Apply",
        "11. Links &amp; Contacts",
        "12. Closing Summary",
    ]:
        story.append(P(item, s["toc"]))
    story.append(PageBreak())

    # 1
    story.append(P("1. Executive Answer", s["h1"]))
    story.append(ghr())
    story.append(
        P(
            "Your product (Morpho / Earn yield explorer + risk intelligence + portfolio tracker on Robinhood Chain) "
            "is a <b>good grant fit</b>: DeFi tooling, retail UX, Morpho surface area, Arbitrum Orbit / Dedicated "
            "blockchain narrative. It is <b>not</b> a guaranteed grant.",
            s["body"],
        )
    )
    story.append(
        tbl(
            ["Question", "Answer"],
            [
                ["Can I get grant/funding?", "Yes — eligible and aligned; competitive, not automatic"],
                ["Best cash/prize path?", "Arbitrum Foundation grants + Open House (RH-backed)"],
                ["Robinhood open grant form?", "No public portal found — BD email only"],
                ["Morpho grants?", "Logical fit; check forum for open DAO rounds"],
                ["Wait for grant before building?", "No — ship MVP with URL + metrics first"],
                ["Replace SaaS revenue with grants?", "No — grants are bonus; charge Pro in parallel"],
            ],
            [2.4 * inch, 4.4 * inch],
        )
    )
    story.append(P("Table: Executive Q&amp;A.", s["caption"]))

    # 2
    story.append(P("2. Why This Product Is Fundable", s["h1"]))
    story.append(ghr())
    story.append(
        tbl(
            ["What funders like", "Why your app matches"],
            [
                ["Retail DeFi education / transparency", "Earn “7%” clarity — base APY vs incentives vs risk"],
                ["Morpho ecosystem tooling", "Vault explorer, positions, net APY, allocations"],
                ["Arbitrum / Orbit growth", "Built on Robinhood Chain (Arbitrum stack)"],
                ["Public goods / infra &amp; tools", "Read-only explorer; not a memecoin casino"],
                ["Live product + metrics", "Stronger than idea-only decks"],
            ],
            [2.6 * inch, 4.2 * inch],
        )
    )
    story.append(P("Table: Fundability fit factors.", s["caption"]))
    story.append(
        P(
            "<b>Weak alone:</b> “We’ll raise a VC seed for a dashboard with no users.”<br/>"
            "<b>Strong path:</b> Ship MVP → apply with metrics → Open House / Foundation grant → angel/VC only if growth warrants.",
            s["body"],
        )
    )

    # 3
    story.append(P("3. Funding Sources (Ranked Best → Weaker)", s["h1"]))
    story.append(ghr())

    story.append(P("3.1 Arbitrum Foundation Grants — best formal fit", s["h2"]))
    for b in [
        "<b>Status:</b> Applications open on a rolling basis (verify current phase on site)",
        "<b>Categories:</b> Decentralized Applications (dApps) + <b>Infrastructure &amp; Tools</b> — your product is tooling",
        "<b>Typical size (public ranges):</b> often cited ~$20,000–$150,000 in ARB; milestone-based disbursement",
        "<b>Why you fit:</b> RH Chain is Arbitrum Dedicated/Orbit-style; DeFi tooling increases usage and retail onboarding",
        "<b>Apply:</b> https://arbitrum.foundation/grants (Notion application form linked from page)",
    ]:
        story.append(P(f"•  {b}", s["bullet"]))
    story.append(
        box(
            "Pitch angle (Arbitrum Foundation)",
            "“Retail transparency layer for Morpho vaults and Robinhood Earn on Robinhood Chain — "
            "net APY vs incentives, portfolio tracking, and alerts — reducing confusion and increasing "
            "safe DeFi adoption on the Arbitrum stack.”",
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    story.append(P("3.2 Arbitrum Open House 2026 — prizes + exposure (RH-backed)", s["h2"]))
    for b in [
        "Robinhood committed <b>$1 million USD</b> toward Open House support for builders on <b>Robinhood Chain</b>",
        "Program: online Buildathons + in-person Founder Houses (NYC, London, Dubai, Singapore, and related events)",
        "City prize pools have been substantial (e.g. London Founder House materials cited ~$300k prizes/grants; NYC and others also awarded large pools)",
        "This is <b>prize/program funding</b>, not a multi-year grant — highly aligned if you demo a live explorer on RH Chain",
        "<b>Hub:</b> https://openhouse.arbitrum.io/",
    ]:
        story.append(P(f"•  {b}", s["bullet"]))

    story.append(P("3.3 Robinhood Chain direct BD — soft support, not a grant form", s["h2"]))
    for b in [
        "<b>No</b> public dedicated Robinhood Chain grant application portal found as of this research",
        "Contact: <b>chain-developers-group@robinhood.com</b>",
        "Ask for: ecosystem page listing, product feedback, partner intros, possible infra credits",
        "Pitch: live product + users + how you help Earn / Wallet users understand Morpho risk",
        "Treat as <b>distribution and relationships</b>, not day-one cash",
    ]:
        story.append(P(f"•  {b}", s["bullet"]))

    story.append(P("3.4 Morpho ecosystem / DAO grants — logical, check current round", s["h2"]))
    for b in [
        "Morpho ran a grants pilot (e.g. MIP 93): pool on the order of <b>200k MORPHO</b>, DAO-voted, milestone payouts (portion upfront, portion on completion, remainder on metrics)",
        "Later DAO activity includes larger Association multi-year budgets; external builder rounds come and go",
        "Action: monitor https://forum.morpho.org for open “Call for Grants” / Questbook rounds before applying",
        "If no open round: ship live tool and engage Morpho ecosystem / curator community (partnership can beat a closed grant round)",
    ]:
        story.append(P(f"•  {b}", s["bullet"]))
    story.append(
        box(
            "Pitch angle (Morpho)",
            "“Best Morpho UX for Robinhood Chain / Earn users — vault registry, positions, risk breakdown "
            "driving Morpho literacy and usage on a high-distribution L2.”",
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    story.append(P("3.5 Credits &amp; non-cash (easy wins)", s["h2"]))
    story.append(
        tbl(
            ["Source", "What you might get", "Notes"],
            [
                ["Alchemy", "RPC / compute credits", "RH recommends Alchemy; historical grant programs existed — ask partnerships"],
                ["Hosting (Railway / Vercel)", "Startup credits", "Low effort, reduces opex"],
                ["Paxos / USDG / Global Dollar Network", "Partner economics more than micro-grants", "Relevant if you become a real USDG surface, not pure dashboard alone"],
            ],
            [2.0 * inch, 2.2 * inch, 2.6 * inch],
        )
    )
    story.append(P("Table: Non-cash support.", s["caption"]))

    story.append(P("3.6 Outside pure grants", s["h2"]))
    story.append(
        tbl(
            ["Type", "Realistic for you?", "When"],
            [
                ["Angels / micro-seed", "Possible", "After MVP + early MRR or strong usage"],
                ["Crypto accelerators", "Possible", "Live product + clear chain thesis"],
                ["Gitcoin / quadratic", "Sporadic", "If a round matches DeFi tooling"],
                ["VC seed", "Low early", "Unless growth is sharp; dashboard alone is hard"],
            ],
            [1.8 * inch, 1.5 * inch, 3.5 * inch],
        )
    )
    story.append(P("Table: Non-grant capital paths.", s["caption"]))
    story.append(PageBreak())

    # 4
    story.append(P("4. Honest Odds Matrix", s["h1"]))
    story.append(ghr())
    story.append(
        tbl(
            ["Path", "Odds of some money", "Expected amount", "Effort"],
            [
                ["Open House prize", "Medium if you ship + demo", "$5k–50k+ (highly competitive)", "High (event + demo)"],
                ["Arbitrum Foundation grant", "Medium with live product + milestones", "$20k–80k typical tooling ask band", "High (app + milestones)"],
                ["Morpho grant (if open)", "Low–medium", "Variable (pilot was modest MORPHO)", "Medium"],
                ["RH cash grant", "Low (no portal)", "Unclear", "Low effort email"],
                ["Alchemy credits", "Medium", "Credits, not cash", "Low"],
                ["VC without traction", "Low", "—", "High waste if premature"],
            ],
            [1.7 * inch, 1.7 * inch, 2.0 * inch, 1.4 * inch],
        )
    )
    story.append(P("Table: Rough probability and size — directional only.", s["caption"]))
    story.append(
        P(
            "<b>Bottom line:</b> Funding is available and your idea is eligible — mainly Arbitrum (Foundation + Open House) "
            "and possibly Morpho when rounds are open. Do not wait for a grant to start building.",
            s["body"],
        )
    )

    # 5
    story.append(P("5. How to Maximize Chances (Action Order)", s["h1"]))
    story.append(ghr())
    for i, b in enumerate(
        [
            "<b>Ship a public MVP</b> on RH Chain (even 1–3 vaults + Earn spotlight + wallet positions).",
            "<b>Metrics pack:</b> weekly users, wallets connected, vaults tracked, alert signups, retention if any.",
            "<b>Apply Arbitrum Foundation</b> under Infrastructure &amp; Tools / dApp with milestones.",
            "<b>Register Open House</b> and prepare a live demo on Robinhood Chain.",
            "<b>Email</b> chain-developers-group@robinhood.com with link + metrics + one-pager.",
            "<b>Watch Morpho forum</b> for next grants call; engage Discord/community if active.",
            "<b>Ask Alchemy</b> for credits once you are on their Robinhood Chain stack.",
            "<b>Charge Pro</b> ($10–20/mo) in parallel — revenue de-risks every application.",
        ],
        1,
    ):
        story.append(P(f"<b>{i}.</b>  {b}", s["bullet"]))

    # 6
    story.append(P("6. Grant Application Outline (Copy Framework)", s["h1"]))
    story.append(ghr())
    story.append(
        tbl(
            ["Section", "What to write"],
            [
                ["Problem", "Earn users don’t understand variable APY, incentives, withdraw/liquidity risk, or curator role"],
                ["Solution", "Euler-like Morpho vault explorer + risk split + portfolio + alerts on Robinhood Chain"],
                ["Why Arbitrum / RH", "Orbit/Dedicated L2; Morpho already powers Earn; retail distribution funnel"],
                ["Traction", "Public URL, users, wallets connected (even small numbers beat zero)"],
                ["Milestones", "M1 live Explore · M2 Portfolio · M3 Alerts · M4 history/multi-vault polish"],
                ["Ask", "e.g. $40k ARB over 4 milestones — or Open House prize track"],
                ["Budget", "Hosting, RPC, design, part-time help — not founder lifestyle salary"],
                ["Open source?", "Optional public APIs / risk formulas help “public goods” narrative"],
                ["Impact metrics", "MAU, wallets, vaults listed, alert fires, open-source stars, docs used"],
            ],
            [1.5 * inch, 5.3 * inch],
        )
    )
    story.append(P("Table: Application skeleton for Arbitrum / similar programs.", s["caption"]))

    # 7
    story.append(P("7. Pitch Angles by Funder", s["h1"]))
    story.append(ghr())
    story.append(
        tbl(
            ["Funder", "Lead with", "Avoid"],
            [
                ["Arbitrum Foundation", "Orbit growth, tooling, onchain activity, milestones", "Vague “AI DeFi” with no demo"],
                ["Open House judges", "Live demo on RH Chain in 3 minutes, clear retail problem", "Long tokenomics pitch"],
                ["Robinhood BD email", "Help Earn users; safety/clarity; ecosystem listing readiness", "Asking for cash in first line"],
                ["Morpho community", "Morpho usage, vault UX, positions API, open tooling", "Ignoring Morpho brand guidelines"],
                ["Alchemy", "Usage of RPC/AA on RH Chain; growth plan", "Demanding cash grants only"],
            ],
            [1.5 * inch, 3.0 * inch, 2.3 * inch],
        )
    )
    story.append(P("Table: Customize the same product story per audience.", s["caption"]))
    story.append(PageBreak())

    # 8
    story.append(P("8. What Not to Expect", s["h1"]))
    story.append(ghr())
    for b in [
        "Instant cash for an idea deck with no live product",
        "Robinhood writing a personal check from a public grant form (none found)",
        "Grants fully replacing the need for users or SaaS revenue",
        "Morpho funding you only because you mention “Earn” without a live integration",
        "VC seed solely on “dashboard for vaults” with zero traction",
        "Open House prizes without showing up and demoing",
    ]:
        story.append(P(f"•  {b}", s["bullet"]))

    # 9
    story.append(P("9. Practical Recommendation", s["h1"]))
    story.append(ghr())
    story.append(
        tbl(
            ["Goal", "Do this"],
            [
                ["Fastest path to “funded”", "Build 4–6 week MVP → Open House + Arbitrum grant the same month"],
                ["Cash independence", "Charge Pro ($10–20/mo) in parallel — grants are bonus"],
                ["Best narrative line", "“Transparency layer for Robinhood Earn / Morpho on RH Chain”"],
                ["If grant rejected", "Keep shipping; reapply next phase with better metrics"],
                ["If prize won", "Use funds for RPC, design, alerts infra — publish milestones publicly"],
            ],
            [2.0 * inch, 4.8 * inch],
        )
    )
    story.append(P("Table: Decision defaults.", s["caption"]))
    story.append(
        box(
            "Default 90-day funding plan",
            "Days 1–30: Public MVP on chain 4663. Days 31–45: Metrics dashboard + one-pager. "
            "Days 45–60: Submit Arbitrum Foundation application + Open House registration. "
            "Days 60–90: RH BD email, Morpho forum check, Stripe Pro live, re-apply or report milestones.",
        )
    )

    # 10
    story.append(P("10. Checklist Before You Apply", s["h1"]))
    story.append(ghr())
    for b in [
        "Live HTTPS URL on mainnet data (not localhost)",
        "At least Explore + one vault detail + connect wallet or clear portfolio path",
        "Disclaimer: not financial advice; yields variable; not FDIC/SIPC",
        "One-page PDF or Notion: problem, solution, screenshots, milestones, ask, team",
        "GitHub or public repo optional but helpful for tooling grants",
        "Wallet addresses / multisig ready if they pay in ARB/MORPHO",
        "Legal entity optional early; some programs prefer one for larger amounts",
        "No misleading Robinhood / Morpho affiliation claims",
    ]:
        story.append(P(f"•  {b}", s["bullet"]))

    # 11
    story.append(P("11. Links &amp; Contacts", s["h1"]))
    story.append(ghr())
    story.append(
        tbl(
            ["Resource", "URL / contact"],
            [
                ["Arbitrum Foundation Grants", "https://arbitrum.foundation/grants"],
                ["Arbitrum Open House", "https://openhouse.arbitrum.io/"],
                ["Arbitrum RH Chain testnet blog (Open House $1M)", "https://blog.arbitrum.io/robinhood-chain-testnet/"],
                ["Robinhood Chain docs", "https://docs.robinhood.com/chain/"],
                ["Robinhood Chain homepage", "https://robinhood.com/us/en/chain/"],
                ["Robinhood ecosystem", "https://robinhood.com/us/en/chain/ecosystem/"],
                ["RH developer email", "chain-developers-group@robinhood.com"],
                ["Morpho governance forum", "https://forum.morpho.org"],
                ["Morpho docs / API", "https://docs.morpho.org"],
                ["Alchemy (RPC partner)", "https://www.alchemy.com"],
            ],
            [2.4 * inch, 4.4 * inch],
        )
    )
    story.append(P("Table: Primary links — re-verify before use.", s["caption"]))

    # 12
    story.append(P("12. Closing Summary", s["h1"]))
    story.append(ghr())
    story.append(
        P(
            "Yes, you can get grant- and prize-style funding for an Earn/Morpho yield &amp; risk intelligence product "
            "on Robinhood Chain. The strongest formal paths are the <b>Arbitrum Foundation</b> and "
            "<b>Arbitrum Open House</b> (with Robinhood’s $1M builder support narrative). "
            "<b>Morpho</b> is a natural second track when DAO grants are open. "
            "Robinhood itself is best approached via <b>ecosystem BD email</b>, not a public grant form. "
            "Credits (Alchemy, hosting) reduce burn cheaply.",
            s["body"],
        )
    )
    story.append(
        P(
            "Ship first. Apply with a URL and metrics. Charge users in parallel. "
            "Grants accelerate a real product — they do not create one.",
            s["quote"],
        )
    )
    story.append(
        tbl(
            ["Priority", "Action", "Outcome sought"],
            [
                ["1", "MVP live on RH Chain", "Fundable artifact"],
                ["2", "Arbitrum Foundation apply", "Milestone cash/ARB"],
                ["3", "Open House demo", "Prize + network"],
                ["4", "RH BD email", "Listing / intros"],
                ["5", "Morpho forum / community", "Grant or partnership"],
                ["6", "Pro SaaS revenue", "Independence"],
            ],
            [0.8 * inch, 2.5 * inch, 3.5 * inch],
        )
    )
    story.append(P("Table: Priority stack.", s["caption"]))

    story.append(Spacer(1, 0.15 * inch))
    story.append(ghr())
    story.append(
        P(
            "— End of grants &amp; funding guide —",
            ParagraphStyle(
                "end", fontName="Helvetica-Oblique", fontSize=9,
                textColor=GRAY, alignment=TA_CENTER, spaceBefore=12,
            ),
        )
    )
    story.append(
        P(
            "Research synthesis for planning only. Grant programs, prize pools, and eligibility change. "
            "Always confirm current application windows and terms on official sites before submitting.",
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
        title="Earn Morpho Grants and Funding Guide",
        author="Funding Strategy Research",
        subject="Grants and funding for Morpho Earn yield explorer on Robinhood Chain",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Wrote: {OUT}")
    return OUT


if __name__ == "__main__":
    build()
