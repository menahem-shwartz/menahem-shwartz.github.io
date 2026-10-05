"""Generate the ATS-friendly CV linked from the GitHub Pages site.

Run:  python3 generate_cv.py
Needs: pip install reportlab
Fonts: Inter (SIL Open Font License), bundled in cv-fonts/ so the PDF looks
the same on any machine.
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent
OUTPUT_PATH = ROOT / "assets" / "menahem-shwartz-cv.pdf"
FONT_DIR = ROOT / "cv-fonts"

# ---------------------------------------------------------------- content ---

NAME = "Menahem Shwartz"
TITLE = "QA Automation Engineer"
EMAIL = "menahemshvartz@gmail.com"
PHONE_DISPLAY, PHONE_LINK = "058-408-0770", "+972584080770"
LOCATION = "Israel"
LINKEDIN = ("linkedin.com/in/menahem-shwartz",
            "https://www.linkedin.com/in/menahem-shwartz-659342243/")
GITHUB = ("github.com/menahem-shwartz", "https://github.com/menahem-shwartz")
WEBSITE = ("menahem-shwartz.github.io", "https://menahem-shwartz.github.io")

SUMMARY = (
    "QA Automation Engineer with 6+ years of manual and automated testing "
    "experience at Redis Cloud and in the IDF. Specialized in Playwright and "
    "TypeScript automation, REST API and microservices testing, CI/CD quality "
    "gates, framework architecture, flaky-test stabilization, and "
    "observability-driven debugging."
)

ACHIEVEMENTS = [
    "<b>Billing-platform migration:</b> designed the E2E automation strategy, "
    "closed coverage gaps, and created a three-phase mitigation plan; supported "
    "a successful launch with no known revenue-impacting regressions at release.",
    "<b>CI stability:</b> built a GitHub Actions workflow that automatically "
    "reruns failed critical-path tests, reducing manual intervention and "
    "false-negative CI noise.",
    "<b>Microservice quality gates:</b> drove CI/CD quality gates and critical "
    "E2E coverage for a new billing microservice, creating a reusable reference "
    "model for additional services.",
    "<b>Ownership:</b> owned automation decisions and quality strategy for "
    "critical revenue-related product flows in the Billing scrum.",
]

JOBS = [
    {
        "title": "QA Automation Engineer",
        "org": "Redis Cloud",
        "dates": "Aug 2022 – Present",
        "bullets": [
            "Own automation and quality coverage for Redis Cloud billing, "
            "subscriptions, databases, and service-management journeys.",
            "Build and maintain Playwright and TypeScript frameworks for E2E and "
            "REST API coverage with production-like flows, CI evidence, traces, "
            "and focused reruns.",
            "Partner with developers and product managers on high-priority "
            "billing and subscription releases.",
            "Stabilize flaky tests and investigate failures across logs, traces, "
            "deploy context, and CI artifacts to separate product regressions "
            "from infrastructure noise.",
        ],
    },
    {
        "title": "QA Automation Engineer",
        "org": "IDF – Shachar Unit, Lotem",
        "dates": "Nov 2019 – Jul 2022",
        "bullets": [
            "Contributed to the unit's first end-to-end automation "
            "infrastructure using Python and Selenium.",
            "Supported migration from legacy testing libraries, trained "
            "developers, reviewed code, and performed automated and manual "
            "testing across multiple deployment environments.",
            "Worked with product managers on Agile test specifications, bug "
            "management, and test planning for new products and features.",
        ],
    },
]

SKILLS = [
    ("Automation", "Playwright, TypeScript, Selenium, Python, test framework "
                   "architecture, E2E testing, manual testing"),
    ("API &amp; Cloud", "REST API testing, Postman, microservices testing, "
                        "billing systems, SQL, Kafka, Kubernetes"),
    ("CI &amp; Debugging", "GitHub Actions, Jenkins, GitLab, CI/CD quality "
                           "gates, ReportPortal, observability, root-cause "
                           "analysis, flaky-test stabilization"),
    ("Engineering", "Java, Git, code review, Nx, pnpm, Jira, Agile, "
                    "AI-assisted QA"),
    ("Languages", "Hebrew, English"),
]

EDUCATION = [
    ("Basmach QA Certificate", "Basmach, Mamram, Ramat Gan",
     "May 2020 – Jul 2020"),
    ("Advanced Automation", "INT College", "Oct 2020"),
]

# ----------------------------------------------------------------- design ---

INK = colors.HexColor("#111827")
BODY = colors.HexColor("#1F2937")
MUTED = colors.HexColor("#6B7280")
ACCENT = colors.HexColor("#0F766E")
RULE = colors.HexColor("#D1D5DB")

PAGE_W, PAGE_H = A4
MARGIN_X = 17 * mm
CONTENT_W = PAGE_W - 2 * MARGIN_X - 12  # frame has 6pt inner padding


def register_fonts() -> dict:
    files = {w: FONT_DIR / f"Inter-{w}.ttf"
             for w in ("Regular", "Medium", "SemiBold", "Bold")}
    if all(p.exists() for p in files.values()):
        for w, p in files.items():
            pdfmetrics.registerFont(TTFont(f"Inter-{w}", str(p)))
        pdfmetrics.registerFontFamily(
            "Inter-Regular", normal="Inter-Regular", bold="Inter-SemiBold",
            italic="Inter-Regular", boldItalic="Inter-SemiBold")
        return {"reg": "Inter-Regular", "med": "Inter-Medium",
                "semi": "Inter-SemiBold", "bold": "Inter-Bold"}
    return {"reg": "Helvetica", "med": "Helvetica",
            "semi": "Helvetica-Bold", "bold": "Helvetica-Bold"}


F = register_fonts()


def style(name, **kw) -> ParagraphStyle:
    base = dict(fontName=F["reg"], fontSize=9.5, leading=12.6,
                textColor=BODY)
    base.update(kw)
    return ParagraphStyle(name, **base)


S = {
    "name": style("name", fontName=F["bold"], fontSize=25, leading=29,
                  textColor=INK),
    "title": style("title", fontName=F["semi"], fontSize=12, leading=16,
                   textColor=ACCENT),
    "contact": style("contact", fontSize=9, leading=13, textColor=MUTED),
    "section": style("section", fontName=F["bold"], fontSize=9.5, leading=12,
                     textColor=ACCENT),
    "body": style("body"),
    "bullet": style("bullet", leftIndent=11, bulletIndent=1,
                    bulletFontName=F["bold"], bulletColor=ACCENT,
                    spaceAfter=1.3),
    "job": style("job", fontName=F["semi"], fontSize=10.6, leading=14,
                 textColor=INK),
    "date": style("date", fontName=F["med"], fontSize=9, leading=14,
                  textColor=MUTED, alignment=2),
    "label": style("label", fontName=F["semi"], textColor=INK),
}


def link(text: str, url: str) -> str:
    return f'<link href="{url}" color="{BODY.hexval().replace("0x", "#")}">{text}</link>'


def section(title: str) -> list:
    return [
        Spacer(1, 3.4 * mm),
        Paragraph(title.upper().replace("&", "&amp;"), S["section"]),
        HRFlowable(width="100%", thickness=0.6, color=RULE,
                   spaceBefore=1.4 * mm, spaceAfter=2.2 * mm),
    ]


def two_col(left, right, right_w=42 * mm) -> Table:
    t = Table([[left, right]], colWidths=[CONTENT_W - right_w, right_w])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def bullets(items) -> list:
    return [Paragraph(i, S["bullet"], bulletText="•") for i in items]


def header() -> list:
    sep = '&nbsp;&nbsp;<font color="#D1D5DB">|</font>&nbsp;&nbsp;'
    line1 = sep.join([
        link(EMAIL, f"mailto:{EMAIL}"),
        link(PHONE_DISPLAY, f"tel:{PHONE_LINK}"),
        LOCATION,
    ])
    line2 = sep.join([link(*LINKEDIN), link(*GITHUB), link(*WEBSITE)])
    return [
        Paragraph(NAME, S["name"]),
        Spacer(1, 1 * mm),
        Paragraph(TITLE, S["title"]),
        Spacer(1, 2 * mm),
        Paragraph(f"{line1}<br/>{line2}", S["contact"]),
        Spacer(1, 1 * mm),
        HRFlowable(width="100%", thickness=2, color=ACCENT,
                   spaceBefore=2.5 * mm, spaceAfter=0),
    ]


def build_cv() -> None:
    doc = SimpleDocTemplate(
        str(OUTPUT_PATH), pagesize=A4,
        leftMargin=MARGIN_X, rightMargin=MARGIN_X,
        topMargin=12 * mm, bottomMargin=10 * mm,
        title=f"{NAME} – {TITLE}", author=NAME, subject="CV",
    )

    story = header()

    story += section("Professional Summary")
    story.append(Paragraph(SUMMARY, S["body"]))

    story += section("Selected Achievements")
    story += bullets(ACHIEVEMENTS)

    story += section("Experience")
    for n, job in enumerate(JOBS):
        head = two_col(
            Paragraph(f'{job["title"]} <font name="{F["reg"]}" color="#6B7280">'
                      f'&nbsp;·&nbsp; {job["org"]}</font>', S["job"]),
            Paragraph(job["dates"], S["date"]),
        )
        block = [head, Spacer(1, 1.6 * mm)] + bullets(job["bullets"])
        if n < len(JOBS) - 1:
            block.append(Spacer(1, 2.6 * mm))
        story.append(KeepTogether(block))

    story += section("Core Skills")
    rows = [[Paragraph(label, S["label"]), Paragraph(value, S["body"])]
            for label, value in SKILLS]
    skills = Table(rows, colWidths=[33 * mm, CONTENT_W - 33 * mm])
    skills.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
    ]))
    story.append(skills)

    story += section("Education & Courses")
    for name, place, dates in EDUCATION:
        story.append(two_col(
            Paragraph(f'<font name="{F["semi"]}" color="#111827">{name}</font>'
                      f'<font color="#6B7280">&nbsp;&nbsp;·&nbsp; {place}</font>',
                      S["body"]),
            Paragraph(dates, S["date"]),
        ))
        story.append(Spacer(1, 1.2 * mm))
    story.pop()  # no trailing gap after the last entry

    doc.build(story)


if __name__ == "__main__":
    build_cv()
