from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas as pdfcanvas

OUTPUT_PATH = "Module2_BusinessWriting_Notes.pdf"

# ── COLORS ──────────────────────────────────────────────────────────────────
DARK_BLUE    = colors.HexColor("#0d2137")
MED_BLUE     = colors.HexColor("#1565c0")
LIGHT_BLUE   = colors.HexColor("#e3f2fd")
ACCENT       = colors.HexColor("#e65100")
ACCENT_LIGHT = colors.HexColor("#fff3e0")
GREEN        = colors.HexColor("#2e7d32")
GREEN_LIGHT  = colors.HexColor("#e8f5e9")
RED          = colors.HexColor("#b71c1c")
RED_LIGHT    = colors.HexColor("#ffebee")
PURPLE       = colors.HexColor("#4a148c")
PURPLE_LIGHT = colors.HexColor("#f3e5f5")
TEAL         = colors.HexColor("#004d40")
TEAL_LIGHT   = colors.HexColor("#e0f2f1")
GOLD         = colors.HexColor("#f57f17")
GOLD_LIGHT   = colors.HexColor("#fffde7")
GRAY_LIGHT   = colors.HexColor("#f5f5f5")
GRAY_MED     = colors.HexColor("#757575")
WHITE        = colors.white
BLACK        = colors.black
YELLOW_HL    = colors.HexColor("#fff9c4")

# ── STYLE FACTORY ─────────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

body_text  = S("BT2", fontSize=10, textColor=BLACK, fontName="Helvetica",
               leading=15, spaceBefore=3, spaceAfter=3, alignment=TA_JUSTIFY)
sub_head   = S("SH2", fontSize=12, textColor=MED_BLUE, fontName="Helvetica-Bold",
               leading=16, spaceBefore=10, spaceAfter=3)
sub2_head  = S("S2H2", fontSize=11, textColor=TEAL, fontName="Helvetica-Bold",
               leading=14, spaceBefore=7, spaceAfter=2)
bullet_txt = S("BUL2", fontSize=10, textColor=BLACK, fontName="Helvetica",
               leading=14, spaceBefore=2, spaceAfter=2, leftIndent=16, firstLineIndent=-10)
note_txt   = S("NT2", fontSize=9.5, textColor=PURPLE, fontName="Helvetica-Oblique",
               leading=13, spaceBefore=1, spaceAfter=1)
toc_item   = S("TOC2", fontSize=10.5, textColor=MED_BLUE, fontName="Helvetica",
               leading=16, leftIndent=10)

def sp(n=6):  return Spacer(1, n)
def hr():     return HRFlowable(width="100%", thickness=1, color=LIGHT_BLUE, spaceAfter=4, spaceBefore=4)
def hr2():    return HRFlowable(width="100%", thickness=2, color=ACCENT, spaceAfter=6, spaceBefore=6)

def ch_banner(text, bg=DARK_BLUE):
    d = [[Paragraph(text, S("CB", fontSize=17, textColor=WHITE, fontName="Helvetica-Bold",
                            alignment=TA_LEFT, leading=22))]]
    t = Table(d, colWidths=[17*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), bg),
        ("TOPPADDING",(0,0),(-1,-1),11),("BOTTOMPADDING",(0,0),(-1,-1),11),
        ("LEFTPADDING",(0,0),(-1,-1),14),("RIGHTPADDING",(0,0),(-1,-1),14),
    ]))
    return t

def prob_badge(pct, color=ACCENT):
    d = [[Paragraph(f"<b>Exam Probability: {pct}</b>",
                    S("PB", fontSize=10, textColor=WHITE, fontName="Helvetica-Bold",
                      leading=13, alignment=TA_CENTER))]]
    t = Table(d, colWidths=[5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), color),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
    ]))
    return t

def sec_header(num, title, pct, pc=ACCENT):
    d = [[
        Paragraph(f"<b>{num}. {title}</b>",
                  S("SH", fontSize=13, textColor=DARK_BLUE, fontName="Helvetica-Bold", leading=18)),
        prob_badge(pct, pc)
    ]]
    t = Table(d, colWidths=[12*cm, 5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), LIGHT_BLUE),
        ("BOX",(0,0),(-1,-1),1.5, MED_BLUE),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
        ("LEFTPADDING",(0,0),(0,0),10),("RIGHTPADDING",(0,1),(-1,-1),6),
    ]))
    return t

def info_box(title, content, bg=LIGHT_BLUE, tc=DARK_BLUE, bc=MED_BLUE):
    d = [
        [Paragraph(f"<b>{title}</b>", S("IB_T", fontSize=11, textColor=tc, fontName="Helvetica-Bold", leading=14))],
        [Paragraph(content, S("IB_B", fontSize=10, textColor=BLACK, fontName="Helvetica",
                              leading=14, alignment=TA_JUSTIFY))],
    ]
    t = Table(d, colWidths=[16.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,0), bg),
        ("BACKGROUND",(0,1),(0,1), WHITE),
        ("BOX",(0,0),(-1,-1),1, bc),
        ("LINEBELOW",(0,0),(0,0),1, bc),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
    ]))
    return t

def tip_box(text):
    d = [[Paragraph(f"<b>&#9733; KEY POINT:</b> {text}",
                    S("TIP", fontSize=10, textColor=PURPLE, fontName="Helvetica",
                      leading=14, alignment=TA_JUSTIFY))]]
    t = Table(d, colWidths=[16.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), PURPLE_LIGHT),
        ("BOX",(0,0),(-1,-1),1.5, PURPLE),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
    ]))
    return t

def warn_box(text):
    d = [[Paragraph(f"<b>&#9888; EXAM NOTE:</b> {text}",
                    S("WB", fontSize=10, textColor=RED, fontName="Helvetica",
                      leading=14, alignment=TA_JUSTIFY))]]
    t = Table(d, colWidths=[16.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), RED_LIGHT),
        ("BOX",(0,0),(-1,-1),1.5, RED),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
    ]))
    return t

def q_box(label, color, q, a):
    hdr = [[Paragraph(label, S("QH", fontSize=10, textColor=WHITE, fontName="Helvetica-Bold",
                               leading=13, alignment=TA_CENTER))]]
    ht = Table(hdr, colWidths=[16.5*cm])
    ht.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), color),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
    ]))
    qt = Paragraph(f"<b>Q:</b> {q}",
                   S("QT", fontSize=10, textColor=DARK_BLUE, fontName="Helvetica-Bold",
                     leading=14, alignment=TA_JUSTIFY, leftIndent=8, rightIndent=8, spaceBefore=4))
    at = Paragraph(f"<b>Ans:</b> {a}",
                   S("AT", fontSize=10, textColor=BLACK, fontName="Helvetica",
                     leading=15, alignment=TA_JUSTIFY, leftIndent=8, rightIndent=8,
                     spaceBefore=3, spaceAfter=6))
    return [ht, qt, at, sp(8)]

def two_col_table(headers, rows, widths=None):
    if widths is None:
        widths = [8.25*cm, 8.25*cm]
    hrow = [Paragraph(f"<b>{h}</b>", S("TH", fontSize=10, fontName="Helvetica-Bold",
                                        textColor=WHITE, alignment=TA_CENTER, leading=13))
            for h in headers]
    data = [hrow] + rows
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0), DARK_BLUE),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LIGHT_BLUE]),
        ("BOX",(0,0),(-1,-1),1, MED_BLUE),
        ("INNERGRID",(0,0),(-1,-1),0.4, colors.HexColor("#90caf9")),
        ("FONTNAME",(0,1),(-1,-1),"Helvetica"),
        ("FONTSIZE",(0,0),(-1,-1),9.5),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    return t

def sample_letter_box(content_lines, title="SAMPLE LETTER"):
    """Renders a typewriter-style sample letter box."""
    rows = [[Paragraph(title, S("SLT", fontSize=10, textColor=WHITE, fontName="Helvetica-Bold",
                                 alignment=TA_CENTER, leading=13))]]
    for line in content_lines:
        if line == "---":
            rows.append([HRFlowable(width="90%", thickness=0.5, color=GRAY_MED)])
        else:
            rows.append([Paragraph(line, S("SLL", fontSize=9.5, textColor=BLACK,
                                           fontName="Courier", leading=14))])
    t = Table(rows, colWidths=[16.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,0), TEAL),
        ("BACKGROUND",(0,1),(-1,-1), colors.HexColor("#fafafa")),
        ("BOX",(0,0),(-1,-1),1.5, TEAL),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),14),("RIGHTPADDING",(0,0),(-1,-1),14),
    ]))
    return t

# ── NUMBERED CANVAS ────────────────────────────────────────────────────────────
class NumberedCanvas(pdfcanvas.Canvas):
    def __init__(self, *args, **kwargs):
        pdfcanvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
    def save(self):
        num = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num)
            pdfcanvas.Canvas.showPage(self)
        pdfcanvas.Canvas.save(self)
    def draw_page_number(self, total):
        self.setFont("Helvetica", 8)
        self.setFillColor(GRAY_MED)
        self.drawRightString(A4[0]-1.5*cm, 1.2*cm, f"Page {self._pageNumber} of {total}")
        self.drawString(1.5*cm, 1.2*cm, "OEC-CS-601(I) | Module 2 — Communication Breakdown & Business Writing")
        self.setStrokeColor(LIGHT_BLUE)
        self.setLineWidth(0.5)
        self.line(1.5*cm, 1.5*cm, A4[0]-1.5*cm, 1.5*cm)

# ══════════════════════════════════════════════════════════════════════════════
#  BUILD STORY
# ══════════════════════════════════════════════════════════════════════════════
story = []

# ── COVER ──────────────────────────────────────────────────────────────────────
cover_rows = [
    [sp(14)],
    [Paragraph("&#9733; OEC-CS-601(I) &#9733;",
               S("C1", fontSize=13, textColor=colors.HexColor("#bbdefb"),
                 fontName="Helvetica-Bold", alignment=TA_CENTER, leading=18))],
    [sp(6)],
    [Paragraph("SOFT SKILLS &amp;",
               S("C2", fontSize=30, textColor=WHITE, fontName="Helvetica-Bold",
                 alignment=TA_CENTER, leading=36))],
    [Paragraph("INTERPERSONAL COMMUNICATION",
               S("C3", fontSize=19, textColor=colors.HexColor("#e3f2fd"),
                 fontName="Helvetica-Bold", alignment=TA_CENTER, leading=28))],
    [sp(8)],
    [HRFlowable(width="80%", thickness=2, color=ACCENT, spaceAfter=8, spaceBefore=4)],
    [Paragraph("MODULE 2 — COMMUNICATION BREAKDOWN",
               S("C4", fontSize=15, textColor=ACCENT, fontName="Helvetica-Bold",
                 alignment=TA_CENTER, leading=22))],
    [Paragraph("Advanced Writing Skills · Business Writing · Business Letters",
               S("C5", fontSize=11, textColor=colors.HexColor("#bbdefb"),
                 fontName="Helvetica-Oblique", alignment=TA_CENTER, leading=16))],
    [sp(12)],
    [Paragraph("Maximum Marks: 75  |  Full Notes + Q&amp;A + Sample Letters",
               S("C6", fontSize=11, textColor=WHITE, fontName="Helvetica", alignment=TA_CENTER, leading=16))],
    [sp(6)],
    [Paragraph("6 Core Topics | 60+ Practice Questions | Sample Letters Included",
               S("C7", fontSize=10, textColor=colors.HexColor("#e3f2fd"),
                 fontName="Helvetica", alignment=TA_CENTER, leading=14))],
    [sp(14)],
]
cover_t = Table(cover_rows, colWidths=[17*cm])
cover_t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1), DARK_BLUE),
    ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
    ("LEFTPADDING",(0,0),(-1,-1),16),("RIGHTPADDING",(0,0),(-1,-1),16),
]))
story.append(cover_t)
story.append(sp(18))

legend_data = [
    ["1.5 Marks — ~50 words", "5 Marks — 300-500 words",
     "10 Marks — 500-700 words", "15 Marks — 700-1000 words"]
]
leg_t = Table(legend_data, colWidths=[4*cm, 4.5*cm, 4.5*cm, 4.5*cm])
leg_t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(0,0), GREEN),("BACKGROUND",(1,0),(1,0), MED_BLUE),
    ("BACKGROUND",(2,0),(2,0), ACCENT),("BACKGROUND",(3,0),(3,0), RED),
    ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),9),
    ("FONTCOLOR",(0,0),(-1,-1), WHITE),
    ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
    ("ALIGN",(0,0),(-1,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
]))
story.append(leg_t)
story.append(PageBreak())

# ── TABLE OF CONTENTS ──────────────────────────────────────────────────────────
story.append(ch_banner("&#128196;  TABLE OF CONTENTS — MODULE 2"))
story.append(sp(10))
toc = [
    ("1", "Communication Breakdown — Overview", "82%"),
    ("2", "Advanced Writing Skills", "85%"),
    ("3", "Principles of Business Writing", "90%"),
    ("4", "Types of Business Writing", "80%"),
    ("5", "Business Letters — Meaning & Importance", "88%"),
    ("6", "Business Letters: Format and Style", "92%"),
    ("7", "Types of Business Letters (with Samples)", "95%"),
]
for num, title, pct in toc:
    row = [[
        Paragraph(f"<b>{num}.</b>  {title}", toc_item),
        Paragraph(f"<b>{pct}</b>", S("TP", fontSize=10, textColor=ACCENT,
                                      fontName="Helvetica-Bold", alignment=TA_RIGHT, leading=14)),
    ]]
    rt = Table(row, colWidths=[14*cm, 3*cm])
    rt.setStyle(TableStyle([
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(0,0),10),
        ("LINEBELOW",(0,0),(-1,-1),0.3, colors.HexColor("#c5cae9")),
    ]))
    story.append(rt)
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — COMMUNICATION BREAKDOWN
# ══════════════════════════════════════════════════════════════════════════════
story.append(ch_banner("MODULE 2: COMMUNICATION BREAKDOWN & ADVANCED BUSINESS WRITING", DARK_BLUE))
story.append(sp(10))
story.append(sec_header("1", "Communication Breakdown — Overview", "82%", MED_BLUE))
story.append(sp(8))

story.append(Paragraph("What is Communication Breakdown?", sub_head))
story.append(Paragraph(
    "Communication breakdown occurs when the intended message fails to reach the receiver as the sender meant it, "
    "resulting in misunderstanding, conflict, inefficiency, or complete failure of communication. "
    "In business and professional contexts, communication breakdown costs organisations billions annually through "
    "lost productivity, poor decisions, conflict, and damaged relationships.", body_text))
story.append(sp(5))

story.append(Paragraph("Causes of Communication Breakdown:", sub2_head))
causes = [
    ("Poor Writing Skills", "Ambiguous, grammatically incorrect, or unclear written messages — emails, memos, reports — cause misinterpretation."),
    ("Inappropriate Channel Selection", "Using an informal chat for a critical policy announcement; using email for an urgent matter needing immediate response."),
    ("Information Overload", "Too much information overwhelms the receiver, causing important content to be missed or misunderstood."),
    ("Lack of Feedback", "One-way communication without confirmation of receipt and understanding — the sender assumes understanding."),
    ("Cultural and Language Differences", "Different interpretations of the same words, idioms, or writing styles across cultures."),
    ("Poor Listening / Reading", "Receiver does not give full attention to the message — skimming a report and missing critical details."),
    ("Emotional and Psychological Barriers", "Anger, stress, bias, or preconceptions distorting message reception."),
    ("Structural/Organizational Barriers", "Too many hierarchical levels filtering information; siloed departments not sharing information."),
    ("Technical Barriers", "Poor email systems, broken links, unformatted documents, or inaccessible files."),
]
for c, d in causes:
    story.append(Paragraph(f"&#9654; <b>{c}:</b> {d}", bullet_txt))
    story.append(sp(2))

story.append(sp(4))
story.append(tip_box(
    "The single most common cause of workplace communication breakdown is POOR WRITING — unclear emails, "
    "ambiguous instructions, and poorly structured reports. This is why Advanced Writing Skills are a core professional competency."))
story.append(sp(6))

story.append(Paragraph("Consequences of Communication Breakdown in Organizations:", sub2_head))
for c in [
    "Project delays and cost overruns due to misunderstood requirements or instructions.",
    "Damaged professional relationships — clients, colleagues, and superiors lose trust.",
    "Legal and compliance risks — poorly written contracts or policy documents cause disputes.",
    "Employee disengagement — poor internal communication lowers morale and motivation.",
    "Loss of business opportunities — poor proposal or email writing loses clients.",
    "Conflict escalation — misunderstood messages trigger arguments and disputes.",
]:
    story.append(Paragraph(f"&#8226; {c}", bullet_txt))
story.append(sp(8))

# Q&A
hdr_q1 = [[Paragraph("PRACTICE QUESTIONS — TOPIC 1: Communication Breakdown",
                      S("QS", fontSize=11, textColor=WHITE, fontName="Helvetica-Bold",
                        alignment=TA_CENTER, leading=15))]]
ht_q1 = Table(hdr_q1, colWidths=[17*cm])
ht_q1.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),MED_BLUE),
                            ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
story.append(ht_q1)
story.append(sp(6))

for item in q_box("1.5 MARKS (~50 words)", GREEN, "What is Communication Breakdown?",
    "Communication breakdown is the failure of the intended message to be correctly received, understood, or acted upon. "
    "It results from poor writing, wrong channel choice, language barriers, noise, emotional bias, or lack of feedback. "
    "In business, it leads to errors, conflict, project failures, and loss of professional relationships."):
    story.append(item)

for item in q_box("5 MARKS (300-500 words)", MED_BLUE,
    "What are the main causes of communication breakdown? How can they be prevented?",
    "<b>Introduction:</b> Communication breakdown is the disruption in the communication process that prevents "
    "the message from being understood as intended. It is one of the most costly problems in business organisations.<br/><br/>"
    "<b>Key Causes:</b><br/>"
    "1. <b>Poor Writing Skills:</b> Ambiguous, grammatically flawed, or badly structured written communication — "
    "the receiver misinterprets or cannot understand the content.<br/>"
    "2. <b>Wrong Channel Selection:</b> Sending urgent messages by email (slow response time) or using casual chat "
    "for important policy announcements loses urgency and formality.<br/>"
    "3. <b>Information Overload:</b> Bombarding receivers with excessive data makes them miss critical points. "
    "The human brain can only process limited information at a time.<br/>"
    "4. <b>Lack of Feedback:</b> When senders assume understanding without seeking confirmation, errors go undetected.<br/>"
    "5. <b>Cultural and Language Differences:</b> Idioms, humor, and writing conventions differ across cultures, "
    "causing misinterpretation in global organisations.<br/>"
    "6. <b>Emotional Barriers:</b> Anger, stress, or prejudice distort how messages are sent and received.<br/>"
    "7. <b>Organisational Structure:</b> Multiple hierarchical levels filter and distort messages as they pass upward or downward.<br/>"
    "8. <b>Technical Failures:</b> Broken links, corrupted attachments, poor email formatting prevent message delivery.<br/><br/>"
    "<b>Prevention Strategies:</b><br/>"
    "1. Invest in professional writing training for employees.<br/>"
    "2. Select the right channel for each message (urgent = call/instant message; formal = email/memo).<br/>"
    "3. Use the 7 C's of communication: Clear, Concise, Complete, Correct, Concrete, Courteous, Considerate.<br/>"
    "4. Build feedback mechanisms — ask for confirmation of understanding.<br/>"
    "5. Provide cross-cultural communication training for global teams.<br/>"
    "6. Create open-door communication cultures that encourage questions.<br/><br/>"
    "<b>Conclusion:</b> Most communication breakdowns are preventable through awareness, skill development, "
    "and systematic communication protocols. Advanced writing skills are the foundation of prevention."):
    story.append(item)

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — ADVANCED WRITING SKILLS
# ══════════════════════════════════════════════════════════════════════════════
story.append(sec_header("2", "Advanced Writing Skills", "85%", ACCENT))
story.append(sp(8))

story.append(Paragraph("What are Advanced Writing Skills?", sub_head))
story.append(Paragraph(
    "Advanced writing skills go beyond basic grammar and spelling. They encompass the ability to plan, structure, draft, "
    "revise, and polish complex written documents that effectively communicate purpose, persuade audiences, and achieve "
    "professional objectives. In business, writing is the primary tool for formal communication — emails, reports, "
    "proposals, contracts, memos, and letters all demand advanced writing competence.", body_text))
story.append(sp(5))

story.append(Paragraph("The Writing Process — Step by Step:", sub2_head))
writing_steps = [
    ("Step 1: Pre-Writing (Planning)", [
        "Define PURPOSE — why are you writing? (Inform, persuade, request, complain, apologise?)",
        "Identify AUDIENCE — who will read this? (Technical expert or layperson? Superior or peer?)",
        "Gather INFORMATION — facts, data, examples, evidence needed.",
        "OUTLINE — organise main points logically before writing.",
        "Choose TONE — formal, semi-formal, or informal based on context.",
    ]),
    ("Step 2: Drafting", [
        "Write the first draft without obsessing over perfection — get ideas on paper.",
        "Follow the planned structure: Introduction → Body → Conclusion.",
        "Use topic sentences for each paragraph — one main idea per paragraph.",
        "Use transitional phrases: 'Furthermore...', 'However...', 'In conclusion...'",
    ]),
    ("Step 3: Revising (Content Level)", [
        "Check: Does the content fulfil the PURPOSE?",
        "Is all information ACCURATE, COMPLETE, and RELEVANT?",
        "Is the STRUCTURE logical — does one idea flow into the next?",
        "Is the TONE appropriate for the audience?",
    ]),
    ("Step 4: Editing (Language Level)", [
        "Grammar check: subject-verb agreement, tense consistency, pronoun reference.",
        "Sentence structure: vary sentence length; avoid run-ons and fragments.",
        "Word choice: precise, professional vocabulary; eliminate clichés and jargon.",
        "Punctuation and spelling: use tools like spell check but verify manually.",
    ]),
    ("Step 5: Proofreading (Final Polish)", [
        "Read document slowly, preferably aloud.",
        "Check formatting: margins, fonts, headings, alignment, spacing.",
        "Verify names, dates, numbers, references — facts must be accurate.",
        "Get a second reader's opinion for important documents.",
    ]),
]
for step, points in writing_steps:
    story.append(Paragraph(f"<b>{step}</b>", sub2_head))
    for p in points:
        story.append(Paragraph(f"&#9654; {p}", bullet_txt))
    story.append(sp(4))

story.append(Paragraph("Advanced Writing Techniques:", sub2_head))
techniques = [
    ("1. Active vs Passive Voice",
     "Active voice: Subject performs the action — 'The manager approved the report.' (Direct, strong, clear.)\n"
     "Passive voice: Subject receives action — 'The report was approved by the manager.' (Weaker, wordier.)\n"
     "Business writing prefers ACTIVE voice for directness. Use passive only when the actor is unknown or emphasis on action is needed."),
    ("2. Sentence Variety",
     "Mix short sentences (impact) with medium and long sentences (explanation). Monotonous sentence length bores the reader. "
     "Short sentences punch. Longer sentences can carry more nuance and develop complex ideas that need elaboration."),
    ("3. Parallel Structure",
     "List items in the same grammatical form: 'We need to plan, execute, and evaluate.' "
     "NOT: 'We need to plan, the execution, and evaluation.' Parallelism improves clarity and professionalism."),
    ("4. Coherence and Cohesion",
     "COHERENCE: Logical connection of ideas — reader can follow your argument. "
     "COHESION: Language links — use transitional words (therefore, however, moreover, consequently) to connect sentences."),
    ("5. Precision and Conciseness",
     "Cut every word that does not add meaning. 'Due to the fact that' = 'Because'. "
     "'In the event that' = 'If'. Business readers have limited time — be precise."),
    ("6. Reader-Centric Writing (You-Attitude)",
     "Frame writing from the reader's perspective — benefits to THEM, not your own interests. "
     "'You will receive your refund within 5 days' (not 'We will process your refund within 5 days')."),
    ("7. Tone Management",
     "Match tone to context: Formal for official correspondence, Semi-formal for internal communication, "
     "Assertive for negotiations, Empathetic for complaints, Positive for routine good-news messages."),
    ("8. Paragraph Organisation (PIE Structure)",
     "P — Point (topic sentence stating the main idea)\n"
     "I — Illustration (evidence, example, data supporting the point)\n"
     "E — Explanation (analysis, so-what of the evidence)"),
]
for t, d in techniques:
    story.append(Paragraph(f"<b>{t}</b>", sub2_head))
    story.append(Paragraph(d.replace('\n', '<br/>'), body_text))
    story.append(sp(4))

story.append(sp(4))
story.append(warn_box(
    "EXAM FAVOURITE: Questions often ask to 'rewrite the following passage using active voice / concise language / "
    "formal tone.' Practice converting passive to active, wordy to concise, informal to formal."))
story.append(sp(8))

# Q&A Section 2
hdr_q2 = [[Paragraph("PRACTICE QUESTIONS — TOPIC 2: Advanced Writing Skills",
                      S("QS", fontSize=11, textColor=WHITE, fontName="Helvetica-Bold",
                        alignment=TA_CENTER, leading=15))]]
ht_q2 = Table(hdr_q2, colWidths=[17*cm])
ht_q2.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),ACCENT),
                            ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
story.append(ht_q2)
story.append(sp(6))

for item in q_box("1.5 MARKS", GREEN, "What is the 'You-Attitude' in business writing?",
    "The 'You-Attitude' (reader-centric writing) means framing messages from the reader's perspective, "
    "focusing on their interests and benefits rather than the writer's. "
    "Example: 'You will receive your refund in 5 days' (You-attitude) vs "
    "'We will process your refund in 5 days' (I/We attitude). It builds goodwill and reader engagement."):
    story.append(item)

for item in q_box("5 MARKS", MED_BLUE, "Explain the writing process with its key stages.",
    "<b>Introduction:</b> The writing process is a systematic, multi-stage approach to producing effective written "
    "communication. It transforms vague ideas into clear, purposeful, polished documents.<br/><br/>"
    "<b>Stage 1 — Pre-Writing (Planning):</b> Define purpose (inform/persuade/request), identify audience, "
    "gather information, and create an outline. This stage prevents disorganised, unfocused writing.<br/><br/>"
    "<b>Stage 2 — Drafting:</b> Write a first draft following the outline. Focus on getting ideas down; "
    "do not aim for perfection. Structure: Introduction (purpose) → Body (details) → Conclusion (action/summary).<br/><br/>"
    "<b>Stage 3 — Revising:</b> Review at the content level — is information complete, accurate, and logically "
    "organised? Does the document fulfil its purpose? Is the tone appropriate for the audience?<br/><br/>"
    "<b>Stage 4 — Editing:</b> Language-level review — grammar, sentence structure, word choice, punctuation, "
    "and clarity. Convert passive to active voice; eliminate redundancy.<br/><br/>"
    "<b>Stage 5 — Proofreading:</b> Final read-through for typos, formatting errors, factual inaccuracies, "
    "and name/number errors. Read aloud for flow; have a second person review important documents.<br/><br/>"
    "<b>Conclusion:</b> Skipping any stage results in weaker documents. Professional writers follow all five "
    "stages consistently for high-quality output."):
    story.append(item)

for item in q_box("10 MARKS (500-700 words)", ACCENT,
    "What are Advanced Writing Skills? Explain the key techniques used in professional business writing.",
    "<b>Introduction:</b><br/>"
    "Advanced writing skills are the sophisticated competencies needed to produce clear, purposeful, persuasive, "
    "and professionally polished written communication. In business, writing is the primary instrument of formal "
    "communication — every email, report, proposal, and letter reflects the writer's professional credibility. "
    "Poor writing causes communication breakdown; advanced writing skills prevent it.<br/><br/>"
    "<b>The Writing Process:</b><br/>"
    "Professional writing follows a five-stage process: (1) Pre-Writing — planning purpose, audience, and content; "
    "(2) Drafting — creating the initial version; (3) Revising — checking content logic and completeness; "
    "(4) Editing — fixing grammar, word choice, and style; (5) Proofreading — final accuracy and formatting check.<br/><br/>"
    "<b>Key Advanced Writing Techniques:</b><br/>"
    "1. <b>Active Voice:</b> Business writing prefers active voice for clarity and directness. "
    "'The team completed the project.' (Active) vs 'The project was completed by the team.' (Passive — weaker). "
    "Active voice is shorter, clearer, and more dynamic.<br/>"
    "2. <b>Conciseness:</b> Eliminate every word that adds no meaning. Replace wordy phrases: "
    "'in the event that' = 'if'; 'due to the fact that' = 'because'; 'at this point in time' = 'now'. "
    "Business readers are busy — respect their time.<br/>"
    "3. <b>Parallel Structure:</b> List items in the same grammatical form. "
    "'We aim to plan, execute, and evaluate' (NOT: 'We aim to plan, the execution, and evaluation'). "
    "Parallelism improves readability and professionalism.<br/>"
    "4. <b>Coherence and Cohesion:</b> Coherence = logical flow of ideas; Cohesion = language links. "
    "Use transitional words: 'Furthermore', 'However', 'Consequently', 'In contrast', 'Therefore'. "
    "Each paragraph should connect logically to the next.<br/>"
    "5. <b>Reader-Centric Writing (You-Attitude):</b> Frame every message from the reader's perspective. "
    "Focus on benefits to THEM. 'You will receive your invoice by Friday' vs 'We will send your invoice by Friday'.<br/>"
    "6. <b>Tone Management:</b> Select appropriate tone — formal (official letters), semi-formal (internal emails), "
    "empathetic (complaint responses), assertive (negotiation letters). Wrong tone damages professional relationships.<br/>"
    "7. <b>Paragraph Structure (PIE):</b> Point (topic sentence) → Illustration (evidence/example) → "
    "Explanation (analysis). One idea per paragraph. Topic sentence tells reader what the paragraph is about.<br/>"
    "8. <b>Sentence Variety:</b> Vary length — short sentences create impact; longer ones develop complex ideas. "
    "Monotonous sentence length fatigues the reader.<br/>"
    "9. <b>Precision:</b> Choose words carefully — 'The project is delayed' not 'The project is experiencing some "
    "timeline challenges.' Vague language reduces trust and creates misunderstanding.<br/>"
    "10. <b>Positive Language:</b> Frame messages positively when possible. "
    "'We can deliver by Thursday' not 'We cannot deliver before Thursday.' Positive framing builds goodwill.<br/><br/>"
    "<b>Conclusion:</b><br/>"
    "Advanced writing skills are not innate talents — they are learnable, practicable competencies. "
    "Professionals who write clearly, concisely, and reader-centrically build stronger credibility, advance faster "
    "in careers, and contribute more effectively to organisational communication."):
    story.append(item)

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — PRINCIPLES OF BUSINESS WRITING
# ══════════════════════════════════════════════════════════════════════════════
story.append(sec_header("3", "Principles of Business Writing", "90% — VERY HIGH", RED))
story.append(sp(8))

story.append(Paragraph("What is Business Writing?", sub_head))
story.append(Paragraph(
    "Business writing is a type of professional communication used in workplace and commercial contexts. "
    "It includes all written correspondence, documentation, and materials produced within or between organisations: "
    "emails, letters, reports, memos, proposals, minutes, notices, and more. Unlike creative writing, "
    "business writing is purpose-driven, audience-focused, and result-oriented.", body_text))
story.append(sp(5))

story.append(Paragraph("Core Characteristics of Business Writing:", sub2_head))
chars = [
    ("Purposeful", "Every piece of business writing has a clear, specific objective — to inform, request, persuade, or document."),
    ("Audience-Focused", "Written with the reader's needs, knowledge level, and interests in mind (You-attitude)."),
    ("Clear and Unambiguous", "No room for multiple interpretations. Business decisions depend on precise information."),
    ("Concise", "Uses minimum words to convey maximum meaning. Respects the reader's time."),
    ("Formal and Professional", "Appropriate language, tone, and format for the business context."),
    ("Factual and Accurate", "Based on verified information. Business writing must be legally and factually defensible."),
    ("Well-Structured", "Logical organisation — the reader can easily navigate to information they need."),
    ("Action-Oriented", "Business writing drives action — requests, decisions, approvals, and responses."),
]
for c, d in chars:
    story.append(Paragraph(f"&#9654; <b>{c}:</b> {d}", bullet_txt))
    story.append(sp(2))

story.append(sp(6))
story.append(Paragraph("The 7 C's of Business Writing (CRITICAL — VERY HIGH EXAM CHANCE):", sub2_head))

sevenc_data = [
    [Paragraph("<b>Principle</b>", S("TH", fontSize=10, fontName="Helvetica-Bold", textColor=WHITE, alignment=TA_CENTER, leading=13)),
     Paragraph("<b>Meaning</b>", S("TH", fontSize=10, fontName="Helvetica-Bold", textColor=WHITE, alignment=TA_CENTER, leading=13)),
     Paragraph("<b>Example</b>", S("TH", fontSize=10, fontName="Helvetica-Bold", textColor=WHITE, alignment=TA_CENTER, leading=13))],
    ["1. Clarity", "Ideas expressed simply and clearly; no ambiguity", "Use short sentences; avoid jargon with non-specialists"],
    ["2. Conciseness", "No redundant words; maximum meaning in minimum words", "'If' not 'In the event that'; 'Because' not 'Due to the fact that'"],
    ["3. Completeness", "All information the reader needs is included (5W 1H)", "Who, What, When, Where, Why, How — all answered"],
    ["4. Correctness", "Accurate grammar, facts, figures, names, and spelling", "Proofread; verify data; check names of recipients"],
    ["5. Concreteness", "Specific, definite language; no vague generalities", "'By Friday 5PM' not 'soon'; '15% increase' not 'significant growth'"],
    ["6. Courtesy", "Respectful, polite, reader-oriented tone; goodwill language", "'Please', 'Thank you', 'We appreciate your patience'"],
    ["7. Consideration", "Writer considers reader's viewpoint, feelings, and needs", "You-attitude; benefit-focused; empathetic framing"],
]
t_7c = Table(sevenc_data, colWidths=[3.5*cm, 6.5*cm, 6.5*cm])
t_7c.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0), DARK_BLUE),
    ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LIGHT_BLUE]),
    ("BOX",(0,0),(-1,-1),1, MED_BLUE),
    ("INNERGRID",(0,0),(-1,-1),0.4, colors.HexColor("#90caf9")),
    ("FONTNAME",(0,1),(-1,-1),"Helvetica"),("FONTSIZE",(0,0),(-1,-1),9.5),
    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
]))
story.append(t_7c)
story.append(sp(8))

story.append(Paragraph("Additional Principles of Business Writing:", sub2_head))
addl = [
    ("Unity", "Each paragraph deals with only ONE idea. One document = one purpose. Do not mix multiple objectives in a single piece."),
    ("Coherence", "Ideas flow logically. Each sentence connects to the next. Each paragraph links to adjacent ones. The reader never gets lost."),
    ("Emphasis", "Important ideas are placed in positions of emphasis — beginning or end of sentence/paragraph. Use formatting (bold, bullet, heading) to highlight key information."),
    ("Positive Tone", "Frame messages positively wherever possible. Positive writing builds goodwill and reduces defensiveness. 'We can dispatch by Thursday' not 'We cannot dispatch before Thursday'."),
    ("Appropriate Language Level", "Match vocabulary complexity to the audience. Technical terms with experts; simple language with general public."),
    ("Ethical Writing", "No misrepresentation, exaggeration, or manipulation. Business writing must be honest and legally defensible."),
]
for a, d in addl:
    story.append(Paragraph(f"&#8226; <b>{a}:</b> {d}", bullet_txt))
    story.append(sp(3))

story.append(sp(5))
story.append(tip_box(
    "The 7 C's appear in almost EVERY exam. Memorize them as: "
    "Clarity · Conciseness · Completeness · Correctness · Concreteness · Courtesy · Consideration. "
    "Be ready to explain each with an example."))
story.append(sp(8))

# Q&A Section 3
hdr_q3 = [[Paragraph("PRACTICE QUESTIONS — TOPIC 3: Principles of Business Writing",
                      S("QS", fontSize=11, textColor=WHITE, fontName="Helvetica-Bold",
                        alignment=TA_CENTER, leading=15))]]
ht_q3 = Table(hdr_q3, colWidths=[17*cm])
ht_q3.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),RED),
                            ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
story.append(ht_q3)
story.append(sp(6))

for item in q_box("1.5 MARKS", GREEN, "What is 'Concreteness' in business writing?",
    "Concreteness means using specific, definite, and precise language rather than vague generalities. "
    "Instead of 'The project will be done soon,' write 'The project will be completed by Friday, 17 June, at 5 PM.' "
    "Concrete language eliminates ambiguity, builds credibility, and ensures the reader knows exactly what to expect."):
    story.append(item)

for item in q_box("5 MARKS", MED_BLUE, "Explain any five principles of business writing with examples.",
    "<b>Introduction:</b> Business writing principles are guidelines that ensure written professional communication "
    "is effective, professional, and achieves its purpose. The most important set is the 7 C's.<br/><br/>"
    "1. <b>Clarity:</b> The message must be immediately understandable. Use simple, direct language. "
    "Avoid jargon with non-specialist readers. Short sentences enhance clarity. "
    "Example: 'Please send the invoice by Monday.' (Clear) vs 'Please ensure the requisite documentation "
    "is forwarded at your earliest convenience.' (Unclear).<br/><br/>"
    "2. <b>Conciseness:</b> Eliminate every unnecessary word. Business readers are busy. "
    "Replace: 'Due to the fact that' with 'Because'; 'At this point in time' with 'Now'. "
    "A concise email is more likely to be read and acted upon than a long one.<br/><br/>"
    "3. <b>Completeness:</b> Include all information the reader needs. Answer: Who? What? When? Where? Why? How? "
    "An incomplete message requires follow-up — wasting time and causing frustration.<br/><br/>"
    "4. <b>Courtesy:</b> Maintain a polite, respectful, and empathetic tone. Use 'please' and 'thank you'. "
    "Acknowledge inconvenience: 'We apologise for the delay and appreciate your patience.' "
    "Courtesy builds long-term business relationships.<br/><br/>"
    "5. <b>Correctness:</b> Verify every fact, name, date, and figure. Check grammar and spelling. "
    "An error in a client's name or a financial figure in a business letter damages credibility and can have legal consequences.<br/><br/>"
    "<b>Conclusion:</b> These principles are not optional extras — they are the foundation of professional "
    "written communication that builds credibility, trust, and effective working relationships."):
    story.append(item)

for item in q_box("15 MARKS (700-1000 words)", RED,
    "Explain the principles of effective business writing in detail. Why are these principles important in professional communication?",
    "<b>Introduction:</b><br/>"
    "Business writing is the formal, professional written communication used in commercial and organisational "
    "contexts. Unlike casual or creative writing, business writing is purposeful, audience-focused, and result-oriented. "
    "Effective business writing is governed by a set of well-established principles — most notably the 7 C's — "
    "that ensure messages are clear, professional, and effective.<br/><br/>"
    "<b>The 7 C's of Business Writing:</b><br/>"
    "<b>1. Clarity:</b> The message must be immediately and unambiguously understood. Use short sentences "
    "(15-20 words optimal), avoid technical jargon with non-specialist audiences, and use precise vocabulary. "
    "Clarity prevents misinterpretation and the costly follow-up communication it generates. "
    "Example: 'Please confirm attendance by Wednesday' is clear. 'Kindly ensure your presence is confirmed at "
    "the earliest possible time' is not.<br/><br/>"
    "<b>2. Conciseness:</b> Use the minimum number of words needed. Every redundant word wastes the reader's time "
    "and dilutes the message. Replace: 'In the event that' = 'If'; 'Due to the fact that' = 'Because'; "
    "'At this point in time' = 'Now'. Concise writing demonstrates respect for the reader and confidence in expression.<br/><br/>"
    "<b>3. Completeness:</b> Include all information the reader needs to understand and act. Apply the 5W1H test: "
    "Who is involved? What is the issue/request? When must it happen? Where? Why is it needed? How should it be done? "
    "Incomplete messages generate unnecessary back-and-forth communication, causing frustration and delays.<br/><br/>"
    "<b>4. Correctness:</b> Every fact, name, figure, date, and reference must be accurate. Grammar and spelling "
    "must be flawless. Errors in business writing damage professional credibility, create legal exposure, "
    "and undermine trust. Proofreading is non-negotiable for all formal business documents.<br/><br/>"
    "<b>5. Concreteness:</b> Use specific, measurable, definite language. 'Sales increased by 23% in Q2 2025' "
    "is concrete. 'Sales improved significantly' is vague. Concrete language builds trust, reduces ambiguity, "
    "and makes messages actionable.<br/><br/>"
    "<b>6. Courtesy:</b> Maintain a respectful, empathetic, and reader-oriented tone. Courtesy goes beyond "
    "politeness — it involves anticipating the reader's needs and feelings. "
    "'We understand the inconvenience this may cause and appreciate your patience.' "
    "Courtesy transforms transactional communication into relationship-building interaction.<br/><br/>"
    "<b>7. Consideration:</b> Write from the reader's perspective. Focus on what matters to THEM — their benefits, "
    "their concerns, their questions. Apply the 'You-attitude': "
    "'You will receive the delivery on Monday' (reader-focused) vs "
    "'We will dispatch your order on Friday' (writer-focused).<br/><br/>"
    "<b>Additional Principles:</b><br/>"
    "<b>Unity:</b> One document, one purpose. One paragraph, one idea. Mixing multiple objectives confuses readers.<br/>"
    "<b>Coherence:</b> Logical flow throughout — each idea connects naturally to the next. Use transitional phrases: "
    "Furthermore, However, Therefore, Consequently, In addition.<br/>"
    "<b>Positive Tone:</b> Frame messages positively to build goodwill. "
    "'We can process your request by Thursday' instead of 'We cannot process your request before Thursday.'<br/>"
    "<b>Emphasis:</b> Place most important information at the beginning or end of sentences and paragraphs. "
    "Use formatting — bold, bullet points, headings — to highlight critical information.<br/>"
    "<b>Ethical Writing:</b> No misrepresentation or manipulation. Business writing must be honest, balanced, "
    "and legally defensible.<br/><br/>"
    "<b>Importance of These Principles:</b><br/>"
    "1. <b>Credibility:</b> Well-written documents signal professionalism and competence.<br/>"
    "2. <b>Efficiency:</b> Clear, complete writing reduces back-and-forth communication.<br/>"
    "3. <b>Legal Protection:</b> Accurate, ethical writing reduces legal exposure.<br/>"
    "4. <b>Relationship Building:</b> Courteous, considerate writing builds lasting business relationships.<br/>"
    "5. <b>Decision Support:</b> Well-organised writing enables faster, better decisions.<br/><br/>"
    "<b>Conclusion:</b><br/>"
    "Business writing principles are not bureaucratic rules — they are the architecture of effective professional "
    "communication. Writers who master these principles communicate more clearly, build stronger relationships, "
    "earn greater professional credibility, and contribute more effectively to organisational success."):
    story.append(item)

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — TYPES OF BUSINESS WRITING
# ══════════════════════════════════════════════════════════════════════════════
story.append(sec_header("4", "Types of Business Writing", "80%", MED_BLUE))
story.append(sp(8))

story.append(Paragraph("Overview of Business Writing Types:", sub_head))
story.append(Paragraph(
    "Business writing encompasses a wide range of document types, each with distinct purpose, audience, format, "
    "and tone. Understanding which type to use in which situation is a critical professional competency.", body_text))
story.append(sp(5))

biz_writing_types = [
    ("1. CORRESPONDENCE", [
        ("Business Letters", "Formal external communication — orders, complaints, enquiries, job applications. Has specific format (letterhead, date, salutation, body, closing)."),
        ("Emails", "Most common modern business communication — internal and external. Semi-formal to formal. Subject line is critical; keep brief and professional."),
        ("Memorandums (Memos)", "Internal organisational communication — policy updates, meeting notices, information sharing. Header: TO / FROM / DATE / SUBJECT."),
        ("Notices", "Brief official announcements for a specific group — employees, members. Posted on notice boards or circulated."),
    ]),
    ("2. REPORTS", [
        ("Formal Business Reports", "Structured documents presenting research findings, analysis, and recommendations. Sections: Title, Executive Summary, Introduction, Body, Conclusion, Recommendations, Appendices."),
        ("Informal Reports", "Short internal reports — progress reports, incident reports, daily summaries. Less structured than formal reports."),
        ("Analytical Reports", "Investigate a problem and provide solutions. Require data analysis, critical thinking, and well-supported recommendations."),
        ("Informational Reports", "Present facts without analysis or recommendations — status updates, periodic reports, meeting minutes."),
        ("Progress/Status Reports", "Regular updates on project progress — what has been done, what remains, any obstacles."),
    ]),
    ("3. PROPOSALS", [
        ("Business Proposals", "Documents persuading a client or management to adopt a solution, product, or service. External proposals pitch to clients; internal proposals present projects to management."),
        ("Research Proposals", "Outline research objectives, methodology, resources needed, and expected outcomes."),
        ("Grant Proposals", "Requests for funding — must convince funders of project's value, feasibility, and alignment with their priorities."),
    ]),
    ("4. INSTRUCTIONS AND MANUALS", [
        ("User Manuals", "Step-by-step guides for using products or systems. Must be clear, sequential, and precise."),
        ("Standard Operating Procedures (SOPs)", "Official, authorised instructions for performing tasks in an organisation. Ensure consistency and compliance."),
        ("Policy Documents", "State organisational rules, standards, and expectations for behaviour."),
    ]),
    ("5. MARKETING AND SALES WRITING", [
        ("Brochures and Flyers", "Promotional materials highlighting products or services — reader benefit-focused."),
        ("Press Releases", "Official statements to media announcing news — new products, events, awards, appointments."),
        ("Product Descriptions", "Detailed, persuasive descriptions of product features and benefits."),
        ("Newsletters", "Regular communications to stakeholders — updates, stories, achievements."),
    ]),
    ("6. ACADEMIC/ANALYTICAL WRITING IN BUSINESS", [
        ("Case Studies", "Detailed analysis of real business situations — problem, analysis, solution, evaluation."),
        ("White Papers", "Authoritative documents presenting a problem and recommending a solution. Used in tech and policy."),
        ("Research Papers", "Systematic investigation of a business topic with literature review, methodology, findings, discussion."),
    ]),
]
for cat, items in biz_writing_types:
    story.append(Paragraph(f"<b>{cat}</b>", sub2_head))
    for title, desc in items:
        story.append(Paragraph(f"&#9654; <b>{title}:</b> {desc}", bullet_txt))
        story.append(sp(2))
    story.append(sp(4))

story.append(sp(4))
story.append(two_col_table(
    ["Formal Business Writing", "Informal Business Writing"],
    [
        ["Follows strict format and structure", "Flexible structure"],
        ["Formal vocabulary and grammar", "Conversational language acceptable"],
        ["Official letterhead used", "Plain format"],
        ["External: clients, government, partners", "Internal: colleagues, team members"],
        ["Examples: Letters, formal reports, contracts", "Examples: Emails to colleagues, team memos"],
    ]
))
story.append(sp(8))

# Q&A Section 4
hdr_q4 = [[Paragraph("PRACTICE QUESTIONS — TOPIC 4: Types of Business Writing",
                      S("QS", fontSize=11, textColor=WHITE, fontName="Helvetica-Bold",
                        alignment=TA_CENTER, leading=15))]]
ht_q4 = Table(hdr_q4, colWidths=[17*cm])
ht_q4.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),MED_BLUE),
                            ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
story.append(ht_q4)
story.append(sp(6))

for item in q_box("1.5 MARKS", GREEN, "What is a Memorandum (Memo)?",
    "A memorandum (memo) is a brief, internal written communication used within an organisation to convey "
    "information, policy updates, instructions, or notices to employees. It follows a standard format: "
    "TO, FROM, DATE, SUBJECT — followed by the message body. Memos are direct, concise, "
    "and do not use salutations like 'Dear Sir'."):
    story.append(item)

for item in q_box("10 MARKS", ACCENT,
    "Classify and explain the different types of business writing with examples.",
    "<b>Introduction:</b><br/>Business writing encompasses all written communication produced in professional and "
    "organisational contexts. Each type serves a distinct purpose, targets a specific audience, and follows "
    "different conventions of format and tone.<br/><br/>"
    "<b>1. Correspondence:</b><br/>"
    "<b>Business Letters:</b> Formal external written communication — orders, enquiries, complaints, job applications. "
    "Highly structured with letterhead, date, inside address, salutation, body, and complimentary close.<br/>"
    "<b>Emails:</b> Most prevalent business communication — fast, flexible, and documented. "
    "Effective business emails have a specific subject line, professional greeting, brief purposeful body, and clear call to action.<br/>"
    "<b>Memos:</b> Internal-only; no salutation; TO/FROM/DATE/SUBJECT header. Used for policy notices, updates, reminders.<br/>"
    "<b>Notices:</b> Brief announcements — meeting calls, event notifications, policy reminders.<br/><br/>"
    "<b>2. Reports:</b><br/>"
    "<b>Formal Reports:</b> Comprehensive documents with Title Page, Executive Summary, Introduction, Body, "
    "Conclusion, and Recommendations. Used for major research findings, annual reviews, feasibility studies.<br/>"
    "<b>Progress Reports:</b> Regular status updates — what is done, what is pending, any obstacles.<br/>"
    "<b>Analytical Reports:</b> Investigate a problem and recommend solutions based on data analysis.<br/>"
    "<b>Informational Reports:</b> Present facts without analysis — meeting minutes, status updates.<br/><br/>"
    "<b>3. Proposals:</b><br/>"
    "Documents persuading decision-makers to approve a project, purchase, or plan. Must demonstrate need, "
    "proposed solution, cost-benefit, and implementation plan. External proposals win client business; "
    "internal proposals secure management approval.<br/><br/>"
    "<b>4. Instructions and Manuals:</b><br/>"
    "User manuals, SOPs, and policy documents provide step-by-step guidance. Must be sequential, precise, "
    "and unambiguous. Critical for compliance and operational consistency.<br/><br/>"
    "<b>5. Marketing and Sales Writing:</b><br/>"
    "Brochures, press releases, newsletters, and product descriptions. Persuasive, benefit-focused, and "
    "audience-centric. Must inspire interest and drive action.<br/><br/>"
    "<b>6. Analytical/Research Writing:</b><br/>"
    "Case studies, white papers, and research papers. Evidence-based, structured argumentation used in "
    "policy, technology, and business strategy contexts.<br/><br/>"
    "<b>Conclusion:</b><br/>"
    "Each type of business writing serves a unique communicative purpose. Effective professionals choose the "
    "right type, follow appropriate format conventions, and apply the 7 C's across all types."):
    story.append(item)

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — BUSINESS LETTERS: MEANING & IMPORTANCE
# ══════════════════════════════════════════════════════════════════════════════
story.append(sec_header("5", "Business Letters — Meaning & Importance", "88%", GREEN))
story.append(sp(8))

story.append(Paragraph("What is a Business Letter?", sub_head))
story.append(Paragraph(
    "A business letter is a formal written document sent by an individual or organisation to another individual, "
    "organisation, or institution for a specific professional purpose. It is the oldest and most formal form "
    "of written business communication. Business letters serve as official, legal records of communication "
    "between parties. Unlike emails, they carry higher formality, legal weight, and organisational authority.", body_text))
story.append(sp(5))

story.append(Paragraph("Functions / Purposes of Business Letters:", sub2_head))
functions = [
    ("Communication Record", "Business letters create an official, permanent, written record — essential for legal and compliance purposes."),
    ("External Communication Channel", "Primary formal channel for communicating with parties outside the organisation — clients, suppliers, government, partners."),
    ("Conveying Information", "Transmit important data, decisions, policies, prices, terms, and conditions."),
    ("Making Requests", "Formally request information, services, meetings, approvals, or resources."),
    ("Placing and Acknowledging Orders", "Order letters place requests for goods/services; acknowledgement confirms receipt."),
    ("Handling Complaints and Adjustments", "Professionally address grievances and offer resolutions."),
    ("Building Goodwill", "Well-written letters build long-term professional relationships and positive brand image."),
    ("Legal Documentation", "Serve as legal evidence in disputes, contractual matters, and official proceedings."),
    ("Job Applications", "Cover letters accompany CVs — formal first impressions in employment contexts."),
    ("Sales and Marketing", "Sales letters, circulars, and promotional correspondence generate business."),
]
for f, d in functions:
    story.append(Paragraph(f"&#9654; <b>{f}:</b> {d}", bullet_txt))
    story.append(sp(2))

story.append(sp(5))
story.append(Paragraph("Merits of Business Letters:", sub2_head))
merits = [
    "Written record: Provides permanent documentation for future reference.",
    "Formality: Carries legal weight and official authority.",
    "Reach: Can communicate with anyone, anywhere globally.",
    "Deliberate composition: Allows careful choice of words — more precise than spoken communication.",
    "Wide circulation: Same letter can be sent to multiple recipients (circular letters).",
    "Cost-effective: Especially for formal communications where email may be too informal.",
]
for m in merits:
    story.append(Paragraph(f"&#10003; {m}", bullet_txt))

story.append(sp(5))
story.append(Paragraph("Limitations of Business Letters:", sub2_head))
limits = [
    "Slower than email, phone, or instant messaging for urgent matters.",
    "Costly if sent by courier or registered post.",
    "One-way at the time of sending — feedback is delayed.",
    "Requires formal language skill — poorly written letters damage reputation.",
]
for l in limits:
    story.append(Paragraph(f"&#9888; {l}", bullet_txt))
story.append(sp(8))

# Q&A Section 5
hdr_q5 = [[Paragraph("PRACTICE QUESTIONS — TOPIC 5: Business Letters",
                      S("QS", fontSize=11, textColor=WHITE, fontName="Helvetica-Bold",
                        alignment=TA_CENTER, leading=15))]]
ht_q5 = Table(hdr_q5, colWidths=[17*cm])
ht_q5.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),GREEN),
                            ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
story.append(ht_q5)
story.append(sp(6))

for item in q_box("1.5 MARKS", GREEN, "What is a Business Letter?",
    "A business letter is a formal written document exchanged between organisations or individuals for professional "
    "purposes — making requests, placing orders, handling complaints, conveying information, or building goodwill. "
    "It serves as an official, legal record of communication and represents the organisation's professional image."):
    story.append(item)

for item in q_box("5 MARKS", MED_BLUE, "Discuss the importance and functions of business letters.",
    "<b>Introduction:</b> Despite the dominance of email, business letters remain the gold standard of formal "
    "professional communication — carrying legal authority, formality, and permanence that digital messages often lack.<br/><br/>"
    "<b>Key Functions:</b><br/>"
    "1. <b>Official Record:</b> Business letters are permanent, written records — critical for legal and compliance purposes. "
    "Courts accept business letters as documentary evidence.<br/>"
    "2. <b>External Communication:</b> Primary formal channel to clients, suppliers, government bodies, and partners. "
    "Reflects the organisation's professionalism.<br/>"
    "3. <b>Information Transmission:</b> Conveys policies, decisions, price lists, terms, and conditions formally.<br/>"
    "4. <b>Request Processing:</b> Formally requests information, services, approvals, appointments, and resources.<br/>"
    "5. <b>Order Management:</b> Order letters place requests; acknowledgement letters confirm receipt and processing.<br/>"
    "6. <b>Complaint Handling:</b> Formally documents grievances and provides official responses/resolutions.<br/>"
    "7. <b>Goodwill Building:</b> Thank-you letters, congratulation letters, and seasonal greetings build long-term "
    "professional relationships.<br/>"
    "8. <b>Legal Instrument:</b> Letters of credit, letters of authority, and official agreements carry legal weight.<br/><br/>"
    "<b>Merits:</b> Permanent record; formal authority; global reach; careful composition; legal validity.<br/>"
    "<b>Limitations:</b> Slower than email; delivery costs; delayed feedback.<br/><br/>"
    "<b>Conclusion:</b> Business letters are irreplaceable for formal, legal, and high-stakes professional communication. "
    "Every business professional must master the art of writing them effectively."):
    story.append(item)

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — BUSINESS LETTER FORMAT AND STYLE
# ══════════════════════════════════════════════════════════════════════════════
story.append(sec_header("6", "Business Letters: Format and Style", "92% — EXTREMELY HIGH", RED))
story.append(sp(8))

story.append(Paragraph("Parts of a Business Letter (The 12 Essential Parts):", sub_head))
story.append(Paragraph(
    "A standard business letter has 12 parts. Knowing ALL parts, their order, purpose, and examples is "
    "ESSENTIAL for the exam. Questions frequently ask to 'Label the parts of a letter' or 'Write a letter "
    "with all standard parts.'", body_text))
story.append(sp(5))

parts_data = [
    [Paragraph("<b>Part</b>", S("TH", fontSize=10, fontName="Helvetica-Bold", textColor=WHITE, alignment=TA_CENTER, leading=13)),
     Paragraph("<b>Description</b>", S("TH", fontSize=10, fontName="Helvetica-Bold", textColor=WHITE, alignment=TA_CENTER, leading=13)),
     Paragraph("<b>Example</b>", S("TH", fontSize=10, fontName="Helvetica-Bold", textColor=WHITE, alignment=TA_CENTER, leading=13))],
    ["1. Letterhead", "Organisation's name, address, logo, phone, email. Top of page.", "ABC Technologies Ltd., 12 Park Street, Mumbai 400001"],
    ["2. Date", "Full date the letter is written. Below letterhead.", "15th May 2025 OR May 15, 2025"],
    ["3. Reference Number", "Optional. Internal tracking number assigned by sender.", "Ref: HR/2025/041"],
    ["4. Inside Address", "Full name, designation, and address of recipient.", "Mr. Ramesh Kumar, HR Manager, XYZ Ltd."],
    ["5. Subject Line", "Concise statement of letter's purpose. Below inside address.", "Sub: Application for the Post of Software Engineer"],
    ["6. Salutation", "Formal greeting to the recipient.", "Dear Mr. Kumar, / Dear Sir/Madam,"],
    ["7. Body", "Main content — Introduction, Details, Conclusion. Core of the letter.", "Paragraphs explaining purpose, details, and requested action."],
    ["8. Complimentary Close", "Polite farewell phrase before signature.", "Yours sincerely, / Yours faithfully,"],
    ["9. Signature", "Handwritten signature of the writer.", "Handwritten signature above typed name"],
    ["10. Sender's Name & Designation", "Printed name and position below signature.", "Priya Sharma, Marketing Manager"],
    ["11. Enclosures (Enc.)", "List of documents attached with the letter.", "Enc: 1. Resume 2. Certificates"],
    ["12. CC / Copy to", "Names of others receiving a copy of the letter.", "CC: Mr. Suresh Patel, CEO"],
]
pt = Table(parts_data, colWidths=[3.5*cm, 7*cm, 6*cm])
pt.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0), DARK_BLUE),
    ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LIGHT_BLUE]),
    ("BOX",(0,0),(-1,-1),1, MED_BLUE),
    ("INNERGRID",(0,0),(-1,-1),0.4, colors.HexColor("#90caf9")),
    ("FONTNAME",(0,1),(-1,-1),"Helvetica"),("FONTSIZE",(0,0),(-1,-1),9),
    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
]))
story.append(pt)
story.append(sp(8))

story.append(Paragraph("Styles / Formats of Business Letters:", sub_head))
story.append(Paragraph(
    "Business letters are formatted in different styles. The three most commonly examined are Full Block, "
    "Modified Block, and Semi-Block.", body_text))
story.append(sp(5))

style_data = [
    [Paragraph("<b>Feature</b>", S("TH", fontSize=10, fontName="Helvetica-Bold", textColor=WHITE, alignment=TA_CENTER, leading=13)),
     Paragraph("<b>Full Block Style</b>", S("TH", fontSize=10, fontName="Helvetica-Bold", textColor=WHITE, alignment=TA_CENTER, leading=13)),
     Paragraph("<b>Modified Block Style</b>", S("TH", fontSize=10, fontName="Helvetica-Bold", textColor=WHITE, alignment=TA_CENTER, leading=13)),
     Paragraph("<b>Semi-Block (Indented) Style</b>", S("TH", fontSize=10, fontName="Helvetica-Bold", textColor=WHITE, alignment=TA_CENTER, leading=13))],
    ["Alignment", "All parts left-aligned", "Date, close, signature centred or right; rest left", "Like modified block but first line of each para indented"],
    ["Paragraph indent", "No indentation", "No indentation", "First line indented ~1.27 cm"],
    ["Spacing", "Extra space between parts", "Extra space between parts", "Extra space between parts"],
    ["Formality", "Most formal", "Moderately formal", "Traditional; slightly less formal"],
    ["Most used in", "Modern corporate; USA", "General business", "Older British tradition"],
]
st = Table(style_data, colWidths=[3*cm, 3.5*cm, 4.5*cm, 6*cm])
st.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0), DARK_BLUE),
    ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LIGHT_BLUE]),
    ("BOX",(0,0),(-1,-1),1, MED_BLUE),
    ("INNERGRID",(0,0),(-1,-1),0.4, colors.HexColor("#90caf9")),
    ("FONTNAME",(0,1),(-1,-1),"Helvetica"),("FONTSIZE",(0,0),(-1,-1),9),
    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("WORDWRAP",(0,0),(-1,-1),1),
]))
story.append(st)
story.append(sp(8))

story.append(Paragraph("Salutation and Complimentary Close — Rules:", sub2_head))
salut_data = [
    [Paragraph("<b>Situation</b>", S("TH", fontSize=10, fontName="Helvetica-Bold", textColor=WHITE, alignment=TA_CENTER, leading=13)),
     Paragraph("<b>Salutation</b>", S("TH", fontSize=10, fontName="Helvetica-Bold", textColor=WHITE, alignment=TA_CENTER, leading=13)),
     Paragraph("<b>Complimentary Close</b>", S("TH", fontSize=10, fontName="Helvetica-Bold", textColor=WHITE, alignment=TA_CENTER, leading=13))],
    ["Named individual known to you", "Dear Mr./Ms./Dr. [Surname],", "Yours sincerely,"],
    ["Unknown recipient (Sir/Madam)", "Dear Sir, / Dear Madam, / Dear Sir/Madam,", "Yours faithfully,"],
    ["Organisation (not a person)", "Dear Sir/Madam,", "Yours faithfully,"],
    ["First name basis (informal)", "Dear [First Name],", "Best regards, / Kind regards,"],
    ["Formal American style", "Dear Mr./Ms. [Last Name]:", "Sincerely, / Respectfully,"],
]
st2 = Table(salut_data, colWidths=[4.5*cm, 6*cm, 6*cm])
st2.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0), TEAL),
    ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, TEAL_LIGHT]),
    ("BOX",(0,0),(-1,-1),1, TEAL),
    ("INNERGRID",(0,0),(-1,-1),0.4, colors.HexColor("#80cbc4")),
    ("FONTNAME",(0,1),(-1,-1),"Helvetica"),("FONTSIZE",(0,0),(-1,-1),9.5),
    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
]))
story.append(st2)
story.append(sp(6))
story.append(tip_box(
    "GOLDEN RULE: 'Dear Sir/Madam' (unknown) → 'Yours faithfully'. "
    "'Dear Mr./Ms. Smith' (named person) → 'Yours sincerely'. "
    "These pairing rules are frequently tested!"))
story.append(sp(8))

# Q&A Section 6
hdr_q6 = [[Paragraph("PRACTICE QUESTIONS — TOPIC 6: Format and Style of Business Letters",
                      S("QS", fontSize=11, textColor=WHITE, fontName="Helvetica-Bold",
                        alignment=TA_CENTER, leading=15))]]
ht_q6 = Table(hdr_q6, colWidths=[17*cm])
ht_q6.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),RED),
                            ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
story.append(ht_q6)
story.append(sp(6))

for item in q_box("1.5 MARKS", GREEN, "What is the difference between 'Yours sincerely' and 'Yours faithfully'?",
    "'Yours sincerely' is used when the recipient's name is known and used in the salutation (e.g., 'Dear Mr. Sharma'). "
    "'Yours faithfully' is used when the recipient's name is unknown and the salutation is 'Dear Sir' or 'Dear Madam'. "
    "This is a fixed rule of business letter etiquette in British English."):
    story.append(item)

for item in q_box("5 MARKS", MED_BLUE, "Explain the essential parts of a business letter.",
    "<b>Introduction:</b> A standard business letter follows a structured format that ensures professionalism, "
    "completeness, and legal validity. Understanding each part is essential for writing effective business letters.<br/><br/>"
    "<b>The 12 Essential Parts:</b><br/>"
    "1. <b>Letterhead:</b> Contains the organisation's name, address, logo, phone number, and email. Establishes "
    "identity and professionalism.<br/>"
    "2. <b>Date:</b> Exact date of writing — e.g., '15 May 2025'. Provides legal and chronological reference.<br/>"
    "3. <b>Reference Number:</b> Optional internal tracking code (e.g., Ref: MKT/2025/042).<br/>"
    "4. <b>Inside Address:</b> Full name, title, and address of the recipient. Ensures correct delivery.<br/>"
    "5. <b>Subject Line:</b> Concise statement of the letter's purpose — e.g., 'Sub: Request for Quotation for Office Furniture'.<br/>"
    "6. <b>Salutation:</b> Formal greeting — 'Dear Mr. Kumar,' or 'Dear Sir/Madam,'.<br/>"
    "7. <b>Body:</b> Three paragraphs — (a) Introduction: state purpose; (b) Details: expand information; "
    "(c) Conclusion: state desired action or closing remark.<br/>"
    "8. <b>Complimentary Close:</b> Polite farewell — 'Yours sincerely,' or 'Yours faithfully,'.<br/>"
    "9. <b>Signature:</b> Handwritten signature of the writer.<br/>"
    "10. <b>Name and Designation:</b> Printed name and title below signature — e.g., 'Rahul Gupta, Sales Manager'.<br/>"
    "11. <b>Enclosures:</b> List of attached documents — e.g., 'Enc: 1. Brochure 2. Price List'.<br/>"
    "12. <b>CC (Copy To):</b> Names of others receiving copies of the letter.<br/><br/>"
    "<b>Conclusion:</b> Each part plays a specific role in making the letter professional, complete, and effective. "
    "Missing any essential part reduces formality and may create legal or practical problems."):
    story.append(item)

for item in q_box("10 MARKS", ACCENT,
    "Explain the different formats/styles of business letters. Compare Full Block, Modified Block, and Semi-Block styles.",
    "<b>Introduction:</b><br/>A business letter's FORMAT refers to the physical arrangement of its parts on the page. "
    "While all formats include the same essential parts, they differ in alignment, indentation, and layout. "
    "The three most important formats are Full Block, Modified Block, and Semi-Block (Indented).<br/><br/>"
    "<b>1. Full Block Style:</b><br/>"
    "The most modern and widely used format. ALL parts of the letter — letterhead, date, inside address, "
    "subject, salutation, body paragraphs, closing, and signature — are aligned to the LEFT margin. "
    "No indentation anywhere. Paragraphs are separated by a blank line. This style is highly professional, "
    "clean, and easy to type. Most commonly used in the USA and modern corporate environments globally. "
    "Simple: start everything from the left.<br/><br/>"
    "<b>2. Modified Block Style:</b><br/>"
    "A hybrid format. The Date, Complimentary Close, Signature, and Name/Designation are placed at the "
    "CENTRE or RIGHT of the page. All other parts (inside address, subject, salutation, body) are aligned "
    "to the LEFT. Body paragraphs are NOT indented. This was the most common traditional format for many "
    "decades and is still widely used in general business correspondence globally.<br/><br/>"
    "<b>3. Semi-Block Style (Indented Style):</b><br/>"
    "Similar to Modified Block — Date, Close, and Signature are centred or right-aligned. "
    "The unique feature: the first line of EACH body paragraph is indented (typically 1.27 cm or 5 spaces). "
    "This gives the letter a slightly traditional, literary feel. Common in older British business tradition "
    "and some academic contexts.<br/><br/>"
    "<b>4. Simplified Style:</b><br/>"
    "All parts left-aligned (like Full Block) but the salutation and complimentary close are OMITTED. "
    "A bold subject line replaces the salutation. Used in very modern, ultra-efficient business correspondence. "
    "Not commonly taught in exams but worth knowing.<br/><br/>"
    "<b>Salutation-Close Pairings (Critical Rule):</b><br/>"
    "'Dear Sir/Madam' (unknown recipient) → MUST use 'Yours faithfully'.<br/>"
    "'Dear Mr./Ms. [Name]' (known recipient) → MUST use 'Yours sincerely'.<br/>"
    "This rule is consistent across all formats and is frequently tested in exams.<br/><br/>"
    "<b>General Formatting Guidelines:</b><br/>"
    "Font: Times New Roman or Arial; Size: 11-12pt; Margins: 1 inch/2.5 cm all sides. "
    "Single spacing within paragraphs; double spacing between parts/paragraphs.<br/><br/>"
    "<b>Conclusion:</b><br/>"
    "Choosing the right format reflects the writer's professionalism and understanding of business conventions. "
    "Full Block is recommended for modern formal correspondence; Modified Block for traditional contexts. "
    "Regardless of format, the 7 C's of business writing must always be applied."):
    story.append(item)

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 7 — TYPES OF BUSINESS LETTERS (WITH SAMPLES)
# ══════════════════════════════════════════════════════════════════════════════
story.append(sec_header("7", "Types of Business Letters (with Samples)", "95% — HIGHEST PRIORITY", RED))
story.append(sp(8))

story.append(Paragraph(
    "Types of business letters is the MOST FREQUENTLY EXAMINED topic in this module. "
    "You must know: the purpose, key elements, and be able to write a letter for each type.",
    S("HIG", fontSize=10.5, textColor=RED, fontName="Helvetica-Bold", leading=15,
      spaceBefore=4, spaceAfter=8)))

letter_types_intro = [
    ("1. Enquiry Letter (Letter of Enquiry)", "Asks for information about a product, service, price, terms, conditions, or availability."),
    ("2. Reply to Enquiry", "Responds to an enquiry — provides requested information, quotation, or directs to relevant resources."),
    ("3. Order Letter", "Formally places an order for goods or services. Specifies quantity, description, price, delivery terms."),
    ("4. Acknowledgement Letter", "Confirms receipt of a letter, order, payment, application, or document."),
    ("5. Complaint Letter", "Formally registers dissatisfaction with a product, service, delivery, or behaviour. Seeks remedy."),
    ("6. Adjustment / Reply to Complaint", "Responds to a complaint — acknowledges, apologises, and proposes resolution."),
    ("7. Circular Letter", "Sent to multiple recipients simultaneously to announce the same information — new product, price change, policy update."),
    ("8. Sales Letter", "Persuasive letter to promote a product or service and encourage purchase."),
    ("9. Job Application Letter (Cover Letter)", "Sent with a resume/CV — introduces the applicant and makes a case for their candidacy."),
    ("10. Reference/Recommendation Letter", "Written by a third party vouching for an individual's character, skills, and abilities."),
    ("11. Collection Letter", "Formal request for payment of overdue accounts — often sent in series (gentle reminder to legal notice)."),
    ("12. Goodwill Letter", "Builds or strengthens business relationships — thank-you, congratulations, sympathy, or seasonal greeting."),
]
for t, d in letter_types_intro:
    story.append(Paragraph(f"&#9654; <b>{t}:</b> {d}", bullet_txt))
    story.append(sp(2))

story.append(sp(8))

# ── DETAILED LETTER TYPES WITH SAMPLES ─────────────────────────────────────

# --- ENQUIRY LETTER ---
story.append(Paragraph("TYPE 1: ENQUIRY LETTER", sub_head))
story.append(Paragraph(
    "<b>Purpose:</b> To request information about a product/service/price/availability from a supplier or organisation.<br/>"
    "<b>Key Elements:</b> Specific questions about product; request for catalogue, price list, delivery terms; "
    "mention of intended purpose/volume; professional closing requesting prompt response.", body_text))
story.append(sp(5))
story.append(sample_letter_box([
    "TECH SOLUTIONS PVT. LTD.",
    "24 Innovation Park, Bengaluru - 560 001",
    "Tel: +91-80-2234-5678 | Email: info@techsolutions.in",
    "---",
    "15th May 2025",
    "",
    "The Sales Manager",
    "Premium Office Supplies Ltd.",
    "78 Commercial Street, Mumbai - 400 001",
    "",
    "Sub: Enquiry regarding Office Furniture",
    "",
    "Dear Sir/Madam,",
    "",
    "We are setting up a new office in Bengaluru with a seating capacity for 50 employees",
    "and require high-quality office furniture. We came across your company's products through",
    "an industry directory and believe your range may suit our requirements.",
    "",
    "We would be grateful if you could provide the following information:",
    "  1. Your current product catalogue with specifications",
    "  2. Bulk pricing for orders above 50 units",
    "  3. Delivery timelines and installation services available",
    "  4. Warranty terms and after-sales support",
    "",
    "We intend to finalise our order within the next two weeks and would appreciate a prompt",
    "response at your earliest convenience.",
    "",
    "Yours faithfully,",
    "",
    "[Signature]",
    "Priya Mehta",
    "Procurement Manager",
    "Tech Solutions Pvt. Ltd.",
], "SAMPLE — ENQUIRY LETTER (Full Block Style)"))
story.append(sp(8))

# --- COMPLAINT LETTER ---
story.append(Paragraph("TYPE 2: COMPLAINT LETTER", sub_head))
story.append(Paragraph(
    "<b>Purpose:</b> To formally communicate dissatisfaction and seek remedy — replacement, refund, apology, or correction.<br/>"
    "<b>Key Elements of an Effective Complaint Letter:</b>", body_text))
complaint_points = [
    "State the problem clearly and specifically (order number, date, product name).",
    "Explain the impact of the problem (business loss, inconvenience, safety risk).",
    "Attach evidence if possible (invoice copy, photos — mention as enclosures).",
    "State exactly what resolution you expect — replacement, refund, repair, apology.",
    "Maintain professional, firm tone — NOT emotional or rude. Firm but polite.",
    "Set a reasonable deadline for response.",
]
for p in complaint_points:
    story.append(Paragraph(f"&#9654; {p}", bullet_txt))
story.append(sp(5))
story.append(sample_letter_box([
    "SUNRISE RETAIL STORE",
    "45 Market Road, Chennai - 600 002",
    "Tel: +91-44-2891-0234",
    "---",
    "20th May 2025",
    "",
    "The Customer Service Manager",
    "ElectoHome Appliances Ltd.",
    "15 Industrial Estate, Hyderabad - 500 032",
    "",
    "Sub: Complaint Regarding Defective Microwave Oven (Invoice No. EH/2025/7812)",
    "",
    "Dear Sir/Madam,",
    "",
    "I am writing to express my deep dissatisfaction with the microwave oven purchased from",
    "your authorised dealer on 1st May 2025 (Invoice No. EH/2025/7812, Model: EH-MW-500).",
    "",
    "The appliance stopped heating food within the first week of use. Despite following all",
    "instructions in the user manual, the product fails to perform its basic function. This",
    "defect has caused significant inconvenience to our business operations.",
    "",
    "We request that you arrange for a replacement unit or a full refund within 10 working",
    "days. Please arrange for pickup of the defective unit at your cost.",
    "",
    "Copies of the invoice and warranty card are enclosed for your reference.",
    "",
    "We trust you will resolve this matter promptly to maintain your company's reputation",
    "for quality and customer service.",
    "",
    "Yours faithfully,",
    "",
    "[Signature]",
    "Ramesh Nair",
    "Store Manager, Sunrise Retail Store",
    "",
    "Enc: 1. Copy of Invoice  2. Warranty Card  3. Photographs of Defect",
], "SAMPLE — COMPLAINT LETTER (Full Block Style)"))
story.append(sp(8))

# --- ORDER LETTER ---
story.append(Paragraph("TYPE 3: ORDER LETTER", sub_head))
story.append(Paragraph(
    "<b>Purpose:</b> To formally place an order for goods or services.<br/>"
    "<b>Key Elements:</b> Specific product names, model numbers, quantities; agreed price; payment terms; "
    "requested delivery date and location; packaging/shipping instructions; reference to previous quotation.", body_text))
story.append(sp(4))
story.append(sample_letter_box([
    "GREENFIELD SCHOOLS TRUST",
    "12 Education Avenue, Pune - 411 001",
    "Ref: GST/PUR/2025/089",
    "---",
    "22nd May 2025",
    "",
    "The Managing Director",
    "EduTech Supplies Pvt. Ltd.",
    "56 Technology Park, Bengaluru - 560 045",
    "",
    "Sub: Order for Computer Accessories",
    "",
    "Dear Sir,",
    "",
    "With reference to your quotation dated 15th May 2025 (Ref: ET/Q/2025/234), we are",
    "pleased to place an order for the following items:",
    "",
    "  S.No  | Item Description      | Qty  | Unit Price  | Total",
    "  1.    | HP Wireless Mouse     | 30   | Rs.850      | Rs.25,500",
    "  2.    | Dell USB Keyboard     | 30   | Rs.1,200    | Rs.36,000",
    "  3.    | 32 GB USB Flash Drive | 50   | Rs.450      | Rs.22,500",
    "                                              TOTAL: Rs.84,000",
    "",
    "Please deliver the items to our Pune address by 30th May 2025. Payment will be made",
    "within 15 days of delivery as per your terms. Kindly send the delivery note and GST",
    "invoice along with the consignment.",
    "",
    "Yours sincerely,",
    "",
    "[Signature]",
    "Dr. Anita Sharma",
    "Principal & Procurement Head",
    "Greenfield Schools Trust",
], "SAMPLE — ORDER LETTER"))
story.append(sp(8))

# --- JOB APPLICATION LETTER ---
story.append(Paragraph("TYPE 4: JOB APPLICATION LETTER (Cover Letter)", sub_head))
story.append(Paragraph(
    "<b>Purpose:</b> To formally apply for a position of employment, sent alongside a resume/CV.<br/>"
    "<b>Key Elements:</b> Position applied for (source of advertisement); "
    "qualifications and relevant experience; key strengths aligned to job requirements; "
    "availability for interview; professional closing requesting consideration.", body_text))
story.append(sp(4))
story.append(sample_letter_box([
    "Aakash Verma",
    "B-12, Green Park, New Delhi - 110 016",
    "Phone: +91-98765-43210 | Email: aakash.verma@email.com",
    "---",
    "25th May 2025",
    "",
    "The HR Manager",
    "Infosys Technologies Limited",
    "Plot 44, Electronic City, Bengaluru - 560 100",
    "",
    "Sub: Application for the Post of Software Engineer (Job ID: INF/SE/2025/112)",
    "",
    "Dear Sir/Madam,",
    "",
    "I am writing to apply for the position of Software Engineer as advertised on your",
    "company's careers portal on 20th May 2025.",
    "",
    "I hold a B.Tech in Computer Science Engineering from Delhi Technological University",
    "(2025) with a CGPA of 8.7/10. During my academic career, I developed strong",
    "proficiency in Python, Java, SQL, and REST API development. My internship at TCS",
    "Bengaluru (June-August 2024) provided hands-on experience in agile development,",
    "code review processes, and client-facing requirement analysis.",
    "",
    "Key strengths I bring to this role include:",
    "  - Full-stack development experience (React, Node.js, MySQL)",
    "  - Problem-solving and debugging complex system issues",
    "  - Team collaboration and communication in Agile sprints",
    "  - Certified AWS Cloud Practitioner (2024)",
    "",
    "I am highly motivated to contribute to Infosys's innovative projects and am confident",
    "that my technical skills and work ethic make me a strong candidate for this role.",
    "I am available to join at two weeks' notice.",
    "",
    "I have attached my resume and academic certificates for your review. I would welcome",
    "the opportunity to discuss my application at your convenience.",
    "",
    "Yours faithfully,",
    "",
    "[Signature]",
    "Aakash Verma",
    "",
    "Enc: 1. Resume  2. Academic Certificates  3. Internship Certificate",
], "SAMPLE — JOB APPLICATION LETTER"))
story.append(sp(8))

# --- CIRCULAR LETTER ---
story.append(Paragraph("TYPE 5: CIRCULAR LETTER", sub_head))
story.append(Paragraph(
    "<b>Purpose:</b> To communicate the SAME information to MULTIPLE recipients simultaneously. "
    "Used for announcements — new products, price changes, new branch openings, policy updates, personnel changes.<br/>"
    "<b>Key Features:</b> Generic salutation (Dear Customer/Dear Client); same content for all; "
    "often sent in large numbers (mass mailing); can promote goodwill or announce changes.", body_text))
story.append(sp(4))
story.append(sample_letter_box([
    "GOLDEN THREADS TEXTILES LTD.",
    "88 Weavers' Road, Surat - 395 002",
    "Tel: +91-261-2345-678 | Web: www.goldenthreads.in",
    "---",
    "1st June 2025",
    "",
    "To All Our Valued Customers",
    "",
    "Sub: Announcement of New Product Range and Revised Price List",
    "",
    "Dear Customer,",
    "",
    "We are delighted to announce the launch of our new AUTUMN-WINTER 2025 collection,",
    "featuring premium-quality silk, linen, and cotton blends crafted from sustainably",
    "sourced materials.",
    "",
    "Effective 15th June 2025, our revised price list will be applicable to all new orders.",
    "As a valued customer, we are pleased to offer you an exclusive Early-Bird Discount of",
    "12% on all orders placed before 14th June 2025.",
    "",
    "Our new collection catalogue and updated price list are enclosed herewith. We invite",
    "you to visit our showroom or contact your dedicated account manager for personalised",
    "assistance.",
    "",
    "We thank you for your continued patronage and look forward to serving you with our",
    "finest products.",
    "",
    "Yours faithfully,",
    "",
    "[Signature]",
    "Rajesh Patel",
    "Managing Director, Golden Threads Textiles Ltd.",
    "",
    "Enc: 1. New Collection Catalogue  2. Revised Price List",
], "SAMPLE — CIRCULAR LETTER"))
story.append(sp(8))

# Q&A Section 7
hdr_q7 = [[Paragraph("PRACTICE QUESTIONS — TOPIC 7: Types of Business Letters",
                      S("QS", fontSize=11, textColor=WHITE, fontName="Helvetica-Bold",
                        alignment=TA_CENTER, leading=15))]]
ht_q7 = Table(hdr_q7, colWidths=[17*cm])
ht_q7.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),RED),
                            ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
story.append(ht_q7)
story.append(sp(6))

for item in q_box("1.5 MARKS", GREEN, "What is a Circular Letter?",
    "A circular letter is a business letter sent simultaneously to multiple recipients containing the same "
    "information. It is used to announce product launches, price changes, new branch openings, policy updates, "
    "or personnel changes. Circular letters use a generic salutation ('Dear Customer') "
    "and are an efficient way to communicate identical information to a wide audience."):
    story.append(item)

for item in q_box("5 MARKS", MED_BLUE, "Write a complaint letter to a supplier regarding damaged goods received.",
    "Note: In your exam, write this as an actual letter. Here is the full model answer:<br/><br/>"
    "SUNRISE ELECTRONICS, 45 Market Lane, Jaipur - 302 001<br/>"
    "12th May 2025<br/>"
    "The Manager, Bharat Supplies Ltd., 23 Industrial Area, Delhi - 110 020<br/><br/>"
    "Sub: Complaint Regarding Damaged Goods — Order No. SE/ORD/2025/456<br/><br/>"
    "Dear Sir,<br/><br/>"
    "We write with considerable concern regarding our Order No. SE/ORD/2025/456 for "
    "50 units of Samsung LED Monitors, received on 10th May 2025.<br/><br/>"
    "Upon inspection, we found that 12 units were severely damaged, with cracked screens "
    "and dented packaging, clearly indicating mishandling during transit. This damage has "
    "caused significant disruption to our business operations as these units were committed "
    "to our clients.<br/><br/>"
    "We request that you:<br/>"
    "(a) Arrange immediate replacement of the 12 damaged units within 5 working days;<br/>"
    "(b) Arrange pickup of the damaged goods at your expense;<br/>"
    "(c) Ensure proper packaging for future deliveries to prevent recurrence.<br/><br/>"
    "Photographs of the damaged goods and copies of the delivery note are enclosed. We trust "
    "you will treat this matter with the urgency it deserves to protect our ongoing business relationship.<br/><br/>"
    "Yours sincerely,<br/>"
    "[Signature]<br/>Mr. Arjun Kapoor, Procurement Manager, Sunrise Electronics<br/>"
    "Enc: 1. Photographs of Damaged Goods 2. Delivery Note Copy"):
    story.append(item)

for item in q_box("10 MARKS", ACCENT,
    "Classify the different types of business letters and explain any four types with their key features.",
    "<b>Introduction:</b><br/>Business letters are classified based on their PURPOSE — the function they serve "
    "in professional communication. Each type has distinct characteristics, structure, and tone requirements.<br/><br/>"
    "<b>Classification of Business Letters:</b><br/>"
    "Business letters can be categorised into: (1) Correspondence letters (enquiry, reply, order, acknowledgement), "
    "(2) Complaint and adjustment letters, (3) Sales and promotional letters (sales, circular), "
    "(4) Employment letters (application, reference), and (5) Goodwill letters (thank-you, congratulations).<br/><br/>"
    "<b>Type 1 — Enquiry Letter:</b><br/>"
    "Purpose: Request information about products, services, prices, or availability.<br/>"
    "Key Features: Specific questions clearly listed; professional tone; mention of intended purpose/volume; "
    "request for prompt response. Salutation: 'Dear Sir/Madam,' (unknown). Close: 'Yours faithfully,'<br/>"
    "Content: Introduce yourself/organisation → explain need → list specific questions → request response by a date.<br/><br/>"
    "<b>Type 2 — Complaint Letter:</b><br/>"
    "Purpose: Formally register dissatisfaction and seek remedy.<br/>"
    "Key Features: State problem specifically (date, order no., product); explain impact; attach evidence "
    "(mention as enclosures); state exact remedy required (replacement/refund); set response deadline; "
    "maintain firm-but-professional tone — never emotional or abusive.<br/>"
    "Tone: Assertive but courteous. Factual, not emotional.<br/><br/>"
    "<b>Type 3 — Order Letter:</b><br/>"
    "Purpose: Formally place an order for goods or services.<br/>"
    "Key Features: Specific product descriptions, model numbers, quantities, agreed price; "
    "delivery date, location, and packaging instructions; reference to previous quotation; payment terms.<br/>"
    "A table format for itemised orders is professional and clear.<br/><br/>"
    "<b>Type 4 — Job Application Letter (Cover Letter):</b><br/>"
    "Purpose: Apply for a position of employment alongside a resume.<br/>"
    "Key Features: Specific post applied for (and source of advertisement); relevant qualifications and "
    "experience aligned to job requirements; key strengths (use bullet list for clarity); "
    "availability for interview and to join; professional closing requesting consideration; "
    "list enclosures (resume, certificates).<br/>"
    "Tone: Confident, professional, and enthusiastic — never desperate or boastful.<br/><br/>"
    "<b>Type 5 — Circular Letter:</b><br/>"
    "Purpose: Communicate identical information to multiple recipients simultaneously.<br/>"
    "Key Features: Generic salutation ('Dear Customer'); same content for all recipients; used for "
    "announcements — new products, price changes, openings, policy updates; often followed by an "
    "invitation to respond or take action.<br/><br/>"
    "<b>Conclusion:</b><br/>"
    "Each type of business letter serves a unique communicative purpose and demands appropriate tone, "
    "content, and structure. Professionals who master different letter types can effectively represent "
    "their organisations across all formal written communication contexts."):
    story.append(item)

for item in q_box("15 MARKS (700-1000 words)", RED,
    "Write a detailed note on the types of business letters. Write a sample Job Application Letter AND a Complaint Letter.",
    "<b>PART A — TYPES OF BUSINESS LETTERS:</b><br/><br/>"
    "<b>Introduction:</b><br/>"
    "Business letters are formal written communications used between organisations or between an organisation "
    "and an individual. They are the backbone of external professional correspondence, carrying legal authority, "
    "permanence, and representing the organisation's professional image. Business letters are classified into "
    "various types based on their specific purpose and function.<br/><br/>"
    "<b>Classification and Explanation:</b><br/>"
    "<b>1. Enquiry Letter:</b> Requests information about products, services, prices, or terms. Must be specific, "
    "polite, and include all relevant details about the enquirer's needs. Salutation: Dear Sir/Madam; Close: Yours faithfully.<br/>"
    "<b>2. Reply to Enquiry:</b> Responds to an enquiry with the requested information, quotation, or catalogue. "
    "Should be prompt (within 48 hours), complete, and professional. Highlight competitive advantages.<br/>"
    "<b>3. Order Letter:</b> Places a formal order for specific goods/services with quantities, prices, delivery "
    "date, and payment terms. References previous quotation. Often uses a table for clarity.<br/>"
    "<b>4. Acknowledgement Letter:</b> Confirms receipt of order, payment, application, or document. Short, "
    "professional, provides reference number and expected next steps.<br/>"
    "<b>5. Complaint Letter:</b> Registers formal dissatisfaction — states problem specifically, provides evidence, "
    "demands specific remedy. Professional and firm, never rude. Legal document — factual accuracy critical.<br/>"
    "<b>6. Adjustment Letter (Reply to Complaint):</b> Responds to complaint — acknowledges, apologises "
    "empathetically, proposes resolution. If complaint is valid: full remedy offered. If not: explain politely.<br/>"
    "<b>7. Circular Letter:</b> Same information to multiple recipients — price changes, announcements, new products. "
    "Generic salutation; efficient mass communication.<br/>"
    "<b>8. Sales Letter:</b> Persuasive letter promoting products/services. AIDA structure: "
    "Attention → Interest → Desire → Action. Benefit-focused; clear call-to-action.<br/>"
    "<b>9. Job Application Letter:</b> Formal application for employment. Position stated, qualifications matched "
    "to job requirements, key strengths highlighted, interview availability stated.<br/>"
    "<b>10. Goodwill Letter:</b> Builds business relationships — thank-you, congratulations, sympathy, festive "
    "greetings. No immediate business purpose; purely relationship-building.<br/><br/>"
    "<b>PART B — SAMPLE COMPLAINT LETTER:</b><br/><br/>"
    "BRIGHT STAR ENTERPRISES, 34 Commerce Street, Kolkata - 700 001<br/>"
    "18 May 2025 | The Manager, Swift Couriers Ltd., 12 Transport Nagar, Kolkata - 700 005<br/>"
    "Sub: Complaint Regarding Delayed and Damaged Delivery — Consignment No. SC/2025/9834<br/><br/>"
    "Dear Sir, We write regarding Consignment No. SC/2025/9834 dispatched on 10 May 2025, "
    "to be delivered within 3 working days. The consignment arrived on 17 May 2025 — 4 days late "
    "— and 3 packages were found damaged upon inspection. The delay caused us to breach delivery "
    "commitments to our clients, resulting in financial loss. We request: (a) Full compensation for "
    "damaged goods; (b) Explanation for the delay; (c) Assurance of improved service for future consignments. "
    "Evidence enclosed. Please respond within 5 working days. Yours faithfully, [Signature] "
    "Vikram Sinha, Logistics Manager. Enc: Photos, Delivery Note.<br/><br/>"
    "<b>PART C — SAMPLE JOB APPLICATION LETTER:</b><br/><br/>"
    "Neha Gupta, C-45 Defence Colony, New Delhi-110024 | +91-99887-76655 | neha.g@email.com<br/>"
    "22 May 2025 | The HR Manager, Wipro Technologies, Gurgaon - 122 001<br/>"
    "Sub: Application for the Post of Data Analyst (Ref: WIP/DA/2025/88)<br/><br/>"
    "Dear Sir/Madam, I apply for the Data Analyst position as advertised on LinkedIn on 18 May 2025. "
    "I hold an M.Sc. in Statistics from Delhi University (2025, 9.1 CGPA) and have completed "
    "a 6-month data analytics internship at Accenture where I developed dashboards using Tableau, "
    "performed SQL-based data extraction, and created predictive models in Python. Key strengths: "
    "Advanced Python (pandas, scikit-learn), Power BI, SQL, statistical modelling, and data storytelling. "
    "I am confident of contributing to Wipro's analytics practice. My resume and certificates are enclosed. "
    "I am available for interview at your convenience and can join within one month. "
    "Yours faithfully, [Signature] Neha Gupta. Enc: Resume, Certificates."):
    story.append(item)

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# QUICK REVISION PAGE
# ══════════════════════════════════════════════════════════════════════════════
story.append(ch_banner("&#9733;  QUICK REVISION: MODULE 2 AT A GLANCE  &#9733;", DARK_BLUE))
story.append(sp(12))

rev_data = [
    [Paragraph("<b>Topic</b>", S("TH", fontSize=10, fontName="Helvetica-Bold", textColor=WHITE, alignment=TA_CENTER, leading=13)),
     Paragraph("<b>Must-Know Summary</b>", S("TH", fontSize=10, fontName="Helvetica-Bold", textColor=WHITE, alignment=TA_CENTER, leading=13)),
     Paragraph("<b>Exam %</b>", S("TH", fontSize=10, fontName="Helvetica-Bold", textColor=WHITE, alignment=TA_CENTER, leading=13))],
    ["Comm. Breakdown", "Causes: poor writing, wrong channel, overload, no feedback. Prevention: 7 C's", "82%"],
    ["Advanced Writing", "5-stage process: Plan→Draft→Revise→Edit→Proof. Active voice, PIE para, You-attitude", "85%"],
    ["Principles", "7 C's: Clarity Concise Complete Correct Concrete Courteous Considerate + Unity+Coherence", "90%"],
    ["Types of Biz Writing", "Correspondence, Reports, Proposals, Instructions, Marketing, Analytical", "80%"],
    ["Business Letters", "Most formal external comm; permanent legal record; 12 parts", "88%"],
    ["Format & Style", "Full Block (all left); Modified Block (date/close right); Semi-Block (para indent)", "92%"],
    ["Salutation Rule", "'Dear Sir/Madam' → 'Yours faithfully' | 'Dear Mr./Ms.' → 'Yours sincerely'", "95%"],
    ["Enquiry Letter", "Request info; specific questions; Dear Sir/Madam; Yours faithfully", "90%"],
    ["Complaint Letter", "Specific problem; evidence; remedy demanded; firm but polite; enclose proof", "95%"],
    ["Order Letter", "Specific items + qty + price + delivery; reference quotation; table format", "88%"],
    ["Job Application", "Post + source; qualifications; key strengths; availability; enc: resume", "92%"],
    ["Circular Letter", "Same info to many; generic salutation; announcement purpose", "80%"],
]
rev_t = Table(rev_data, colWidths=[4*cm, 10*cm, 2.5*cm])
rev_t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0), DARK_BLUE),
    ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LIGHT_BLUE]),
    ("BOX",(0,0),(-1,-1),1.5, MED_BLUE),
    ("INNERGRID",(0,0),(-1,-1),0.4, colors.HexColor("#90caf9")),
    ("FONTNAME",(0,1),(-1,-1),"Helvetica"),("FONTSIZE",(0,0),(-1,-1),9),
    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("ALIGN",(2,0),(2,-1),"CENTER"),
]))
story.append(rev_t)
story.append(sp(14))

closing_d = [[Paragraph(
    "<b>EXAM STRATEGY FOR MODULE 2 &#9733;</b><br/>"
    "1. ALWAYS write sample letters with all 12 parts — even if not explicitly asked, it shows mastery.<br/>"
    "2. Remember the 7 C's — list them, define each, give one example per C.<br/>"
    "3. For complaint letters: be specific, factual, and demand a remedy — never rant!<br/>"
    "4. Memorise: 'Dear Sir/Madam' = 'Yours faithfully' | Named person = 'Yours sincerely'.<br/>"
    "5. Full Block Style = everything LEFT-aligned. The simplest and most common format.",
    S("CLO", fontSize=10.5, textColor=DARK_BLUE, fontName="Helvetica", alignment=TA_LEFT,
      leading=17))]]
ct = Table(closing_d, colWidths=[17*cm])
ct.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1), GOLD_LIGHT),
    ("BOX",(0,0),(-1,-1),2, GOLD),
    ("TOPPADDING",(0,0),(-1,-1),14),("BOTTOMPADDING",(0,0),(-1,-1),14),
    ("LEFTPADDING",(0,0),(-1,-1),16),("RIGHTPADDING",(0,0),(-1,-1),16),
]))
story.append(ct)

# ── BUILD ──────────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT_PATH,
    pagesize=A4,
    leftMargin=1.8*cm, rightMargin=1.8*cm,
    topMargin=2*cm, bottomMargin=2.2*cm,
    title="Soft Skills Module 2 — Business Writing Notes",
    author="OEC-CS-601(I)",
)
doc.build(story, canvasmaker=NumberedCanvas)
print(f"PDF created: {OUTPUT_PATH}")