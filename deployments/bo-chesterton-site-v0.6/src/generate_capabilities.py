#!/usr/bin/env python3
"""Generate the Bo Chesterton v0.6 capabilities sheet."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "capabilities.pdf"
FONT_DIR = Path(__file__).resolve().parent / "fonts"

pdfmetrics.registerFont(TTFont("BCSans", str(FONT_DIR / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("BCSans-Bold", str(FONT_DIR / "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("BCSerif", str(FONT_DIR / "DejaVuSerif.ttf")))
pdfmetrics.registerFont(TTFont("BCSerif-Bold", str(FONT_DIR / "DejaVuSerif-Bold.ttf")))
pdfmetrics.registerFontFamily("BCSans", normal="BCSans", bold="BCSans-Bold")
pdfmetrics.registerFontFamily("BCSerif", normal="BCSerif", bold="BCSerif-Bold")

INK = colors.HexColor("#171714")
MUTED = colors.HexColor("#65635d")
LINE = colors.HexColor("#d7d2c7")
PAPER = colors.HexColor("#fcfbf8")
BG = colors.HexColor("#f6f4ef")


class NumberedDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str):
        super().__init__(
            filename,
            pagesize=letter,
            leftMargin=0.62 * inch,
            rightMargin=0.62 * inch,
            topMargin=0.78 * inch,
            bottomMargin=0.60 * inch,
            title="Bo Chesterton - Directed Investigations",
            author="Robert Leo Duffy III / Bo Chesterton",
            subject="Capabilities and current engagement scopes for Bo Chesterton",
        )
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
        )
        self.addPageTemplates(PageTemplate(id="main", frames=[frame], onPage=self.draw_page))

    def draw_page(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(BG)
        canvas.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)

        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.7)
        canvas.line(doc.leftMargin, letter[1] - 0.52 * inch, letter[0] - doc.rightMargin, letter[1] - 0.52 * inch)
        canvas.line(doc.leftMargin, 0.39 * inch, letter[0] - doc.rightMargin, 0.39 * inch)

        canvas.setFillColor(INK)
        canvas.setFont("BCSans-Bold", 8.5)
        canvas.drawString(doc.leftMargin, letter[1] - 0.34 * inch, "B.C   BO CHESTERTON")
        canvas.setFillColor(MUTED)
        canvas.setFont("BCSans", 8)
        canvas.drawRightString(letter[0] - doc.rightMargin, letter[1] - 0.34 * inch, "Independent research in artificial intelligence")
        canvas.drawString(doc.leftMargin, 0.20 * inch, "Bo Chesterton")
        canvas.drawRightString(letter[0] - doc.rightMargin, 0.20 * inch, f"Capabilities v0.6 | 2026-09-10 | {doc.page}/2")
        canvas.restoreState()


styles = getSampleStyleSheet()

EYEBROW = ParagraphStyle(
    "Eyebrow",
    parent=styles["Normal"],
    fontName="BCSans-Bold",
    fontSize=8,
    leading=10,
    textColor=MUTED,
    spaceAfter=8,
    uppercase=True,
)

TITLE = ParagraphStyle(
    "Title",
    parent=styles["Title"],
    fontName="BCSerif",
    fontSize=32,
    leading=33,
    tracking=-0.4,
    textColor=INK,
    alignment=TA_LEFT,
    spaceAfter=12,
)

H2 = ParagraphStyle(
    "H2",
    parent=styles["Heading2"],
    fontName="BCSerif",
    fontSize=20,
    leading=22,
    textColor=INK,
    spaceAfter=8,
)

H3 = ParagraphStyle(
    "H3",
    parent=styles["Heading3"],
    fontName="BCSans-Bold",
    fontSize=10,
    leading=12,
    textColor=INK,
    spaceAfter=6,
)

BODY = ParagraphStyle(
    "Body",
    parent=styles["BodyText"],
    fontName="BCSans",
    fontSize=9,
    leading=12.2,
    textColor=colors.HexColor("#383730"),
    spaceAfter=7,
)

SMALL = ParagraphStyle(
    "Small",
    parent=BODY,
    fontSize=7.8,
    leading=10.2,
    textColor=MUTED,
    spaceAfter=4,
)

PRICE = ParagraphStyle(
    "Price",
    parent=styles["Normal"],
    fontName="BCSerif",
    fontSize=25,
    leading=27,
    textColor=INK,
    spaceAfter=7,
)

PRINCIPLE = ParagraphStyle(
    "Principle",
    parent=BODY,
    fontName="BCSerif",
    fontSize=12,
    leading=15,
    textColor=PAPER,
    spaceAfter=0,
)

BULLET = ParagraphStyle(
    "Bullet",
    parent=SMALL,
    leftIndent=8,
    firstLineIndent=-6,
    bulletIndent=0,
    spaceAfter=3,
)


def P(text, style=BODY):
    return Paragraph(text, style)


def rule(space_before=5, space_after=10):
    return HRFlowable(width="100%", thickness=0.7, color=LINE, spaceBefore=space_before, spaceAfter=space_after)


def offer(title, price, summary, bullets, payment, featured=False):
    text_color = PAPER if featured else INK
    muted_color = colors.HexColor("#c8c5bd") if featured else MUTED
    title_style = ParagraphStyle("offer-title", parent=H3, textColor=text_color, fontSize=10.5)
    price_style = ParagraphStyle("offer-price", parent=PRICE, textColor=text_color)
    summary_style = ParagraphStyle("offer-summary", parent=SMALL, textColor=muted_color, minWidowLines=2)
    bullet_style = ParagraphStyle("offer-bullet", parent=BULLET, textColor=text_color)
    payment_style = ParagraphStyle("offer-payment", parent=SMALL, textColor=muted_color, spaceBefore=7)
    content = [P(title, title_style), P(price, price_style), P(summary, summary_style), rule(3, 6)]
    content.extend(P(f"• {item}", bullet_style) for item in bullets)
    content.append(P(payment, payment_style))
    return content


def build():
    doc = NumberedDocTemplate(str(OUTPUT))
    story = []

    story.extend([
        P("DIRECTED INVESTIGATIONS", EYEBROW),
        P("You bring the question.<br/>Bo investigates it.", TITLE),
        P(
            "Bo Chesterton designs bounded, documented investigations of language-model behavior "
            "and human-AI interaction - especially consequential behaviors that ordinary benchmarks may miss."
        ),
        Spacer(1, 8),
    ])

    principle_box = Table([[P("You commission the question. You do not purchase the conclusion.", PRINCIPLE)]], colWidths=[doc.width])
    principle_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), INK),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("TOPPADDING", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 11),
    ]))
    story.extend([principle_box, Spacer(1, 16)])

    intro = Table([
        [
            [P("THE PREMISE", EYEBROW), P("One uncertainty, made testable.", H2)],
            [
                P("A directed investigation turns a concrete uncertainty about an AI system into a testable question."),
                P("Bo defines the behavior, constructs the protocol, preserves the evidence, and returns findings that can inform an actual decision."),
            ],
        ]
    ], colWidths=[2.25 * inch, 4.05 * inch])
    intro.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, -1), 0),
        ("RIGHTPADDING", (0, 0), (0, -1), 16),
        ("LEFTPADDING", (1, 0), (1, -1), 16),
        ("RIGHTPADDING", (1, 0), (1, -1), 0),
        ("LINEBEFORE", (1, 0), (1, -1), 0.7, LINE),
    ]))
    story.extend([intro, Spacer(1, 14), rule(0, 10), P("CURRENT ENGAGEMENTS", EYEBROW)])

    cards = [
        offer(
            "Evaluation Design",
            "$500",
            "Turn one behavioral concern into an executable experiment.",
            ["Operational definition", "Hypotheses and controls", "Test matrix", "Adjudication rubric", "Execution plan and budget estimate"],
            "Payment in full to begin.",
        ),
        offer(
            "Behavioral Evaluation",
            "$1,500",
            "Design and run one bounded investigation of an AI behavior.",
            ["Evaluation design", "Bounded execution", "Human-reviewed analysis", "Evidence package", "Findings report and briefing"],
            "50% to begin; 50% on delivery.",
            featured=True,
        ),
        offer(
            "Three-Evaluation Program",
            "$3,750",
            "Three related evaluations conducted under one shared brief.",
            ["Three defined evaluations", "Shared decision context", "Evidence package for each", "Integrated findings report", "Final briefing and next tests"],
            "Milestones defined before work begins.",
        ),
    ]
    offer_table = Table([cards], colWidths=[doc.width / 3] * 3)
    offer_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (0, 0), PAPER),
        ("BACKGROUND", (1, 0), (1, 0), INK),
        ("BACKGROUND", (2, 0), (2, 0), PAPER),
        ("BOX", (0, 0), (0, 0), 0.7, LINE),
        ("BOX", (1, 0), (1, 0), 0.7, INK),
        ("BOX", (2, 0), (2, 0), 0.7, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 11),
        ("RIGHTPADDING", (0, 0), (-1, -1), 11),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.extend([
        offer_table,
        Spacer(1, 10),
        P("Larger or specialized work is quoted separately after scoping.", SMALL),
        P("Unusual access requirements or external model and API costs beyond the agreed allowance are client-supplied or separately approved before they are incurred.", SMALL),
        PageBreak(),
    ])

    story.extend([
        P("METHOD", EYEBROW),
        P("The record matters.", TITLE),
        P(
            "Questions are made explicit. Methods, relevant decisions, deviations, limitations, and provenance are preserved. "
            "Where possible, analysis is reproducible or independently inspectable. Observation is distinguished from interpretation."
        ),
        P("The question and scope are commissioned. The findings remain independent.", ParagraphStyle("standout", parent=H3, fontSize=11, spaceBefore=4, spaceAfter=12)),
        rule(2, 8),
        P("ENGAGEMENT PROCESS", EYEBROW),
    ])

    process = [
        [P("01  QUESTION", H3), P("02  SCOPE", H3), P("03  INVESTIGATION", H3), P("04  RETURN", H3)],
        [P("Describe the problem and the decision it needs to inform.", SMALL), P("Define method, deliverables, boundaries, cost, and confidentiality.", SMALL), P("Conduct and document the work to the agreed scope.", SMALL), P("Receive the evidence, analysis, conclusions, and limitations.", SMALL)],
    ]
    process_table = Table(process, colWidths=[doc.width / 4] * 4)
    process_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOX", (0, 0), (-1, -1), 0.7, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.7, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, 0), 9),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 9),
    ]))
    story.extend([process_table, Spacer(1, 13), rule(0, 9), P("EVIDENCE THAT THE PROCESS EXISTS", EYEBROW)])

    works = [
        [P("EMPIRICAL RESEARCH", EYEBROW), P("When Evidence Overrides Framing", H3), P("Three preregistered studies of emergency-guidance behavior in language models.", SMALL)],
        [P("BEHAVIORAL / CONCEPTUAL", EYEBROW), P("The Artificial Bestiary", H3), P("Studies of fabricated terms, ontological framing, refusal, and model invention.", SMALL)],
        [P("MODEL DEFAULTS", EYEBROW), P("Why Don't Scientist Trust Atoms?", H3), P("A preregistered 3,600-call study of default joke behavior and model-family signatures.", SMALL)],
        [P("GOVERNANCE", EYEBROW), P("Constitution of Bo Chesterton", H3), P("The canonical governance and provenance record for the continuing research identity.", SMALL)],
    ]
    works_table = Table(works, colWidths=[1.45 * inch, 2.20 * inch, 2.65 * inch])
    works_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEABOVE", (0, 0), (-1, -1), 0.7, LINE),
        ("LINEBELOW", (0, -1), (-1, -1), 0.7, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.extend([works_table, Spacer(1, 13)])

    lower = Table([
        [
            [
                P("BOUNDARIES", EYEBROW),
                P("Independent investigation, not certification.", H2),
                P("Confidential work is available. An engagement is not a regulatory opinion, security audit, or guarantee that a system is safe to deploy.", SMALL),
                P("Clients may challenge findings and request correction. They may not purchase a favorable conclusion or concealment of a material limitation.", SMALL),
            ],
            [
                P("COMMISSION AN INVESTIGATION", EYEBROW),
                P("Start with the uncertainty.", H2),
                P("A short note is enough. Describe the behavior, the system, and the decision you need the evidence to inform.", BODY),
                P("<b>research@bochesterton.com</b>", H3),
                P("bochesterton.com/engagements.html", SMALL),
            ],
        ]
    ], colWidths=[3.15 * inch, 3.15 * inch])
    lower.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, -1), PAPER),
        ("BOX", (0, 0), (-1, -1), 0.7, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.7, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.extend([
        KeepTogether(lower),
        Spacer(1, 8),
        P("Bo Chesterton is a public research identity and continuing intellectual project founded by Robert Leo Duffy III. Commercial engagements are conducted by Robert Leo Duffy III on behalf of the project.", SMALL),
    ])

    doc.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    build()
