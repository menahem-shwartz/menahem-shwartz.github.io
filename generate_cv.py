"""Generate the ATS-friendly CV linked from the GitHub Pages site."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


ROOT = Path(__file__).resolve().parent
OUTPUT_PATH = ROOT / "assets" / "menahem-shwartz-cv.pdf"

INK = colors.HexColor("#172033")
MUTED = colors.HexColor("#566174")
ACCENT = colors.HexColor("#0F766E")
LINE = colors.HexColor("#D6DCE5")


def register_fonts() -> tuple[str, str]:
    regular = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
    bold = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("CVSans", regular))
        pdfmetrics.registerFont(TTFont("CVSans-Bold", bold))
        return "CVSans", "CVSans-Bold"
    return "Helvetica", "Helvetica-Bold"


FONT, FONT_BOLD = register_fonts()


def page_footer(canvas, document) -> None:
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(document.leftMargin, 13 * mm, A4[0] - document.rightMargin, 13 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont(FONT, 8)
    canvas.drawString(
        document.leftMargin,
        8.5 * mm,
        "Menahem Shwartz | QA Automation Engineer",
    )
    canvas.drawRightString(
        A4[0] - document.rightMargin,
        8.5 * mm,
        f"Page {document.page}",
    )
    canvas.restoreState()


def build_cv() -> None:
    styles = getSampleStyleSheet()
    name_style = ParagraphStyle(
        "Name",
        parent=styles["Title"],
        fontName=FONT_BOLD,
        fontSize=22,
        leading=25,
        textColor=INK,
        alignment=TA_CENTER,
        spaceAfter=3,
    )
    role_style = ParagraphStyle(
        "Role",
        parent=styles["Normal"],
        fontName=FONT_BOLD,
        fontSize=11,
        leading=13,
        textColor=ACCENT,
        alignment=TA_CENTER,
        spaceAfter=3,
    )
    contact_style = ParagraphStyle(
        "Contact",
        parent=styles["Normal"],
        fontName=FONT,
        fontSize=9.5,
        leading=13,
        textColor=MUTED,
        alignment=TA_CENTER,
        spaceAfter=5,
    )
    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontName=FONT_BOLD,
        fontSize=11.8,
        leading=14,
        textColor=ACCENT,
        spaceBefore=5,
        spaceAfter=2.5,
        borderColor=LINE,
        borderWidth=0,
        borderPadding=0,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName=FONT,
        fontSize=10,
        leading=12.4,
        textColor=INK,
        spaceAfter=4,
    )
    job_style = ParagraphStyle(
        "Job",
        parent=styles["Heading3"],
        fontName=FONT_BOLD,
        fontSize=10.8,
        leading=13,
        textColor=INK,
        spaceBefore=2,
        spaceAfter=1,
    )
    date_style = ParagraphStyle(
        "Date",
        parent=body_style,
        fontSize=9.5,
        leading=11.5,
        textColor=MUTED,
        spaceAfter=3,
    )
    bullet_style = ParagraphStyle(
        "Bullet",
        parent=body_style,
        fontSize=10,
        leading=12.2,
        leftIndent=13,
        firstLineIndent=-8,
        bulletIndent=0,
        spaceAfter=1.5,
    )
    skills_style = ParagraphStyle(
        "Skills",
        parent=body_style,
        fontSize=10,
        leading=12.4,
        spaceAfter=2,
    )

    document = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=10 * mm,
        bottomMargin=17 * mm,
        title="Menahem Shwartz - QA Automation Engineer",
        author="Menahem Shwartz",
        subject="Professional CV",
    )

    story = [
        Paragraph("MENAHEM SHWARTZ", name_style),
        Paragraph("QA AUTOMATION ENGINEER", role_style),
        Paragraph(
            '<link href="mailto:menahemshvartz@gmail.com" color="#0F766E">'
            "menahemshvartz@gmail.com</link>"
            " &nbsp;|&nbsp; "
            '<link href="tel:+972584080770" color="#0F766E">'
            "058-408-0770</link>"
            " &nbsp;|&nbsp; Israel<br/>"
            '<link href="https://www.linkedin.com/in/menahem-shwartz-659342243/" '
            'color="#0F766E">linkedin.com/in/menahem-shwartz</link>'
            " &nbsp;|&nbsp; "
            '<link href="https://github.com/menahem-shwartz" color="#0F766E">'
            "github.com/menahem-shwartz</link>",
            contact_style,
        ),
        Paragraph("PROFESSIONAL SUMMARY", section_style),
        Paragraph(
            "QA Automation Engineer with 6+ years of manual and automated "
            "testing experience at Redis Cloud and in the IDF. Specialized in "
            "Playwright and TypeScript automation, REST API and microservices "
            "testing, CI/CD quality gates, framework architecture, flaky-test "
            "stabilization, and observability-driven debugging.",
            body_style,
        ),
        Paragraph("SELECTED ACHIEVEMENTS", section_style),
    ]

    achievements = [
        "Designed the E2E automation strategy for a critical billing-platform "
        "migration, closed coverage gaps, and created a three-phase mitigation "
        "plan; supported a successful launch with no known revenue-impacting "
        "regressions at release.",
        "Built a GitHub Actions workflow that automatically reruns failed "
        "critical-path tests, reducing manual intervention and false-negative CI noise.",
        "Drove CI/CD quality gates and critical E2E coverage for a new billing "
        "microservice, creating a reusable reference model for additional services.",
        "Owned automation decisions and quality strategy for critical "
        "revenue-related product flows in the Billing scrum.",
    ]
    story.extend(
        Paragraph(item, bullet_style, bulletText="-") for item in achievements
    )

    story.append(Paragraph("EMPLOYMENT HISTORY", section_style))
    redis_section = [
        Paragraph("QA Automation Engineer - Redis Cloud", job_style),
        Paragraph("Aug 2022 - Present", date_style),
    ]
    redis_bullets = [
        "Own automation and quality coverage for Redis Cloud billing, subscriptions, "
        "databases, and service-management journeys.",
        "Build and maintain Playwright and TypeScript frameworks for E2E and REST API "
        "coverage with production-like flows, CI evidence, traces, and focused reruns.",
        "Partner with developers and product managers on high-priority billing and "
        "subscription releases.",
        "Stabilize flaky tests and investigate failures across logs, traces, deploy "
        "context, and CI artifacts to separate product regressions from infrastructure noise.",
    ]
    redis_section.extend(
        Paragraph(item, bullet_style, bulletText="-") for item in redis_bullets
    )
    story.append(KeepTogether(redis_section[:3]))
    story.extend(redis_section[3:])

    idf_section = [
        Paragraph("QA Automation Engineer - IDF, Shachar Unit, Lotem", job_style),
        Paragraph("Nov 2019 - Jul 2022", date_style),
    ]
    idf_bullets = [
        "Contributed to the unit's first end-to-end automation infrastructure using "
        "Python and Selenium.",
        "Supported migration from legacy testing libraries, trained developers, "
        "reviewed code, and performed automated and manual testing across multiple "
        "deployment environments.",
        "Worked with product managers on Agile test specifications, bug management, "
        "and test planning for new products and application features.",
    ]
    idf_section.extend(
        Paragraph(item, bullet_style, bulletText="-") for item in idf_bullets
    )
    story.append(KeepTogether(idf_section[:3]))
    story.extend(idf_section[3:])

    story.extend(
        [
            Paragraph("CORE SKILLS", section_style),
            Paragraph(
                "<b>Automation:</b> Playwright, TypeScript, Selenium, Python, "
                "test framework architecture, E2E testing, manual testing",
                skills_style,
            ),
            Paragraph(
                "<b>API and cloud:</b> REST API testing, Postman, microservices "
                "testing, billing systems, SQL, Kafka, Kubernetes",
                skills_style,
            ),
            Paragraph(
                "<b>CI and debugging:</b> GitHub Actions, Jenkins, GitLab, CI/CD quality gates, "
                "ReportPortal, observability, root-cause analysis, flaky-test stabilization",
                skills_style,
            ),
            Paragraph(
                "<b>Engineering:</b> Java, Git, code review, Nx, pnpm, Jira, Agile, "
                "AI-assisted QA",
                skills_style,
            ),
            Paragraph("<b>Languages:</b> Hebrew, English", skills_style),
            Paragraph("EDUCATION", section_style),
            Paragraph(
                "<b>Basmach QA Certificate</b> - Basmach, Mamram, Ramat Gan "
                "(May 2020 - Jul 2020)",
                body_style,
            ),
            Paragraph(
                "<b>Advanced Automation</b> - INT College (Oct 2020)",
                body_style,
            ),
            Spacer(1, 2 * mm),
        ]
    )

    document.build(story, onFirstPage=page_footer, onLaterPages=page_footer)


if __name__ == "__main__":
    build_cv()
