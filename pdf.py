from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas as pdfcanvas

OUTPUT_PATH = "Week12_Resume_Interview_EI_Grammar_Notes.pdf"

# ── PALETTE ────────────────────────────────────────────────────────────────────
DARK        = colors.HexColor("#0a1628")
NAVY        = colors.HexColor("#1a3a5c")
BLUE        = colors.HexColor("#1565c0")
BLUE_L      = colors.HexColor("#e3f2fd")
SKY         = colors.HexColor("#bbdefb")
TEAL        = colors.HexColor("#00695c")
TEAL_L      = colors.HexColor("#e0f2f1")
TEAL_M      = colors.HexColor("#004d40")
GREEN       = colors.HexColor("#1b5e20")
GREEN_M     = colors.HexColor("#2e7d32")
GREEN_L     = colors.HexColor("#e8f5e9")
PURPLE      = colors.HexColor("#4a148c")
PURPLE_M    = colors.HexColor("#6a1b9a")
PURPLE_L    = colors.HexColor("#f3e5f5")
CRIMSON     = colors.HexColor("#b71c1c")
CRIMSON_L   = colors.HexColor("#ffebee")
AMBER       = colors.HexColor("#e65100")
AMBER_L     = colors.HexColor("#fff3e0")
GOLD        = colors.HexColor("#f57f17")
GOLD_L      = colors.HexColor("#fffde7")
INDIGO      = colors.HexColor("#1a237e")
INDIGO_L    = colors.HexColor("#e8eaf6")
MAROON      = colors.HexColor("#880e4f")
MAROON_L    = colors.HexColor("#fce4ec")
BROWN       = colors.HexColor("#4e342e")
GRAY_M      = colors.HexColor("#757575")
GRAY_L      = colors.HexColor("#f5f5f5")
YELLOW_HL   = colors.HexColor("#fff9c4")
WHITE       = colors.white
BLACK       = colors.black
DEEP_GREEN  = colors.HexColor("#33691e")
DEEP_GR_L   = colors.HexColor("#f1f8e9")
ROSE        = colors.HexColor("#c62828")
ROSE_L      = colors.HexColor("#ffebee")
SLATE       = colors.HexColor("#37474f")
SLATE_L     = colors.HexColor("#eceff1")

def S(n, **kw): return ParagraphStyle(n, **kw)

body  = S("B", fontSize=10, textColor=BLACK, fontName="Helvetica",
          leading=15, spaceBefore=3, spaceAfter=3, alignment=TA_JUSTIFY)
sub1  = S("H1", fontSize=12, textColor=BLUE, fontName="Helvetica-Bold",
          leading=16, spaceBefore=10, spaceAfter=3)
sub2  = S("H2", fontSize=11, textColor=TEAL, fontName="Helvetica-Bold",
          leading=14, spaceBefore=7, spaceAfter=2)
sub3  = S("H3", fontSize=10.5, textColor=PURPLE_M, fontName="Helvetica-Bold",
          leading=13, spaceBefore=5, spaceAfter=2)
bul   = S("BU", fontSize=10, textColor=BLACK, fontName="Helvetica",
          leading=14, spaceBefore=2, spaceAfter=2, leftIndent=16, firstLineIndent=-10)
note  = S("NT", fontSize=9.5, textColor=PURPLE, fontName="Helvetica-Oblique",
          leading=13, spaceBefore=1, spaceAfter=1)
mono  = S("MN", fontSize=9.5, textColor=BLACK, fontName="Courier",
          leading=13, spaceBefore=2, spaceAfter=2)
toc_i = S("TC", fontSize=10.5, textColor=BLUE, fontName="Helvetica",
          leading=16, leftIndent=12)
gram_wrong = S("GW", fontSize=10, textColor=CRIMSON, fontName="Helvetica",
               leading=14, leftIndent=12)
gram_right = S("GR", fontSize=10, textColor=GREEN_M, fontName="Helvetica-Bold",
               leading=14, leftIndent=12)

def sp(n=6): return Spacer(1, n)
def hr():    return HRFlowable(width="100%", thickness=1,
                               color=BLUE_L, spaceAfter=4, spaceBefore=4)

# ── BUILDERS ────────────────────────────────────────────────────────────────────
def banner(text, bg=DARK, fs=16):
    d = [[Paragraph(text, S("BN", fontSize=fs, textColor=WHITE,
                            fontName="Helvetica-Bold", alignment=TA_LEFT, leading=fs+6))]]
    t = Table(d, colWidths=[17*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), bg),
        ("TOPPADDING",(0,0),(-1,-1),11),("BOTTOMPADDING",(0,0),(-1,-1),11),
        ("LEFTPADDING",(0,0),(-1,-1),14),("RIGHTPADDING",(0,0),(-1,-1),14),
    ]))
    return t

def badge(pct, color=AMBER):
    d = [[Paragraph(f"<b>Exam Probability: {pct}</b>",
                    S("PB", fontSize=10, textColor=WHITE,
                      fontName="Helvetica-Bold", leading=13, alignment=TA_CENTER))]]
    t = Table(d, colWidths=[5.2*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), color),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
    ]))
    return t

def sec_hdr(num, title, pct, pc=AMBER):
    d = [[Paragraph(f"<b>{num}. {title}</b>",
                    S("SH", fontSize=13, textColor=DARK, fontName="Helvetica-Bold", leading=18)),
          badge(pct, pc)]]
    t = Table(d, colWidths=[11.8*cm, 5.2*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), BLUE_L),
        ("BOX",(0,0),(-1,-1),1.5, BLUE),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
        ("LEFTPADDING",(0,0),(0,0),10),("RIGHTPADDING",(0,1),(-1,-1),6),
    ]))
    return t

def ibox(title, content, bg=BLUE_L, tc=DARK, bc=BLUE):
    d = [[Paragraph(f"<b>{title}</b>",
                    S("IH", fontSize=11, textColor=tc, fontName="Helvetica-Bold", leading=14))],
         [Paragraph(content, S("IB", fontSize=10, textColor=BLACK, fontName="Helvetica",
                               leading=14, alignment=TA_JUSTIFY))]]
    t = Table(d, colWidths=[16.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,0), bg),("BACKGROUND",(0,1),(0,1), WHITE),
        ("BOX",(0,0),(-1,-1),1, bc),("LINEBELOW",(0,0),(0,0),1, bc),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
    ]))
    return t

def tip(text, bg=PURPLE_L, border=PURPLE_M, tc=PURPLE):
    d = [[Paragraph(f"<b>&#9733; KEY POINT:</b> {text}",
                    S("TIP", fontSize=10, textColor=tc,
                      fontName="Helvetica", leading=14, alignment=TA_JUSTIFY))]]
    t = Table(d, colWidths=[16.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), bg),("BOX",(0,0),(-1,-1),1.5, border),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
    ]))
    return t

def warn(text):
    d = [[Paragraph(f"<b>&#9888; EXAM NOTE:</b> {text}",
                    S("WB", fontSize=10, textColor=CRIMSON,
                      fontName="Helvetica", leading=14, alignment=TA_JUSTIFY))]]
    t = Table(d, colWidths=[16.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), CRIMSON_L),("BOX",(0,0),(-1,-1),1.5, CRIMSON),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
    ]))
    return t

def q_box(label, color, q, a):
    hdr = [[Paragraph(label, S("QH", fontSize=10, textColor=WHITE,
                               fontName="Helvetica-Bold", leading=13, alignment=TA_CENTER))]]
    ht  = Table(hdr, colWidths=[16.5*cm])
    ht.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), color),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
    ]))
    qt = Paragraph(f"<b>Q:</b> {q}",
                   S("QT", fontSize=10, textColor=DARK, fontName="Helvetica-Bold",
                     leading=14, alignment=TA_JUSTIFY, leftIndent=8, rightIndent=8, spaceBefore=4))
    at = Paragraph(f"<b>Ans:</b> {a}",
                   S("AT", fontSize=10, textColor=BLACK, fontName="Helvetica",
                     leading=15, alignment=TA_JUSTIFY, leftIndent=8, rightIndent=8,
                     spaceBefore=3, spaceAfter=6))
    return [ht, qt, at, sp(8)]

def q_hdr(title, color):
    d = [[Paragraph(title, S("QSH", fontSize=11, textColor=WHITE,
                             fontName="Helvetica-Bold", alignment=TA_CENTER, leading=15))]]
    t = Table(d, colWidths=[17*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), color),
        ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),
    ]))
    return t

def grid(headers, rows, widths=None, hc=DARK):
    if not widths:
        widths = [16.5*cm/len(headers)]*len(headers)
    hrow = [Paragraph(f"<b>{h}</b>", S("GH", fontSize=10, fontName="Helvetica-Bold",
                                        textColor=WHITE, alignment=TA_CENTER, leading=13))
            for h in headers]
    data = [hrow]+rows
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0), hc),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, BLUE_L]),
        ("BOX",(0,0),(-1,-1),1, BLUE),("INNERGRID",(0,0),(-1,-1),0.4, SKY),
        ("FONTNAME",(0,1),(-1,-1),"Helvetica"),("FONTSIZE",(0,0),(-1,-1),9.5),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    return t

def correct_wrong(wrong, right, explanation=""):
    d = [
        [Paragraph(f"&#10008; WRONG: <i>{wrong}</i>",
                   S("GW2", fontSize=10, textColor=CRIMSON, fontName="Helvetica",
                     leading=14, alignment=TA_JUSTIFY))],
        [Paragraph(f"&#10004; CORRECT: <b>{right}</b>",
                   S("GR2", fontSize=10, textColor=GREEN_M, fontName="Helvetica-Bold",
                     leading=14, alignment=TA_JUSTIFY))],
    ]
    if explanation:
        d.append([Paragraph(f"Rule: {explanation}",
                            S("EXP", fontSize=9.5, textColor=NAVY, fontName="Helvetica-Oblique",
                              leading=13, alignment=TA_JUSTIFY))])
    t = Table(d, colWidths=[16.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,0), CRIMSON_L),
        ("BACKGROUND",(0,1),(0,1), GREEN_L),
        ("BACKGROUND",(0,2),(0,-1), INDIGO_L) if explanation else ("TOPPADDING",(0,0),(0,0),0),
        ("BOX",(0,0),(-1,-1),1, BLUE),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
    ]))
    return t

def resume_sample(lines, title="SAMPLE"):
    rows = [[Paragraph(title, S("RST", fontSize=10, textColor=WHITE, fontName="Helvetica-Bold",
                                 alignment=TA_CENTER, leading=13))]]
    for line in lines:
        if line == "---":
            rows.append([HRFlowable(width="95%", thickness=0.5, color=GRAY_M)])
        elif line.startswith("##"):
            rows.append([Paragraph(line[2:], S("RSH", fontSize=11, textColor=DARK,
                                               fontName="Helvetica-Bold", leading=14))])
        elif line.startswith("#"):
            rows.append([Paragraph(line[1:], S("RSS", fontSize=10, textColor=TEAL,
                                               fontName="Helvetica-Bold", leading=13))])
        else:
            rows.append([Paragraph(line, S("RSL", fontSize=9.5, textColor=BLACK,
                                          fontName="Courier", leading=13))])
    t = Table(rows, colWidths=[16.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,0), TEAL_M),
        ("BACKGROUND",(0,1),(-1,-1), GRAY_L),
        ("BOX",(0,0),(-1,-1),1.5, TEAL_M),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),14),("RIGHTPADDING",(0,0),(-1,-1),14),
    ]))
    return t

# ── NUMBERED CANVAS ─────────────────────────────────────────────────────────────
class NC(pdfcanvas.Canvas):
    def __init__(self, *a, **kw):
        pdfcanvas.Canvas.__init__(self, *a, **kw)
        self._s = []
    def showPage(self):
        self._s.append(dict(self.__dict__)); self._startPage()
    def save(self):
        n = len(self._s)
        for st in self._s:
            self.__dict__.update(st); self._fn(n); pdfcanvas.Canvas.showPage(self)
        pdfcanvas.Canvas.save(self)
    def _fn(self, total):
        self.setFont("Helvetica", 8); self.setFillColor(GRAY_M)
        self.drawRightString(A4[0]-1.5*cm, 1.2*cm, f"Page {self._pageNumber} of {total}")
        self.drawString(1.5*cm, 1.2*cm,
                        "OEC-CS-601(I) | Week 12 — Résumé · Interviews · EI & Critical Thinking · Applied Grammar")
        self.setStrokeColor(BLUE_L); self.setLineWidth(0.5)
        self.line(1.5*cm, 1.5*cm, A4[0]-1.5*cm, 1.5*cm)

# ══════════════════════════════════════════════════════════════════════════════
story = []

# ── COVER ────────────────────────────────────────────────────────────────────
rows = [
    [sp(12)],
    [Paragraph("&#9733; OEC-CS-601(I) | Soft Skills &amp; Interpersonal Communication &#9733;",
               S("CV1", fontSize=12, textColor=SKY, fontName="Helvetica-Bold",
                 alignment=TA_CENTER, leading=18))],
    [sp(8)],
    [Paragraph("WEEK 12",
               S("CV2", fontSize=44, textColor=WHITE, fontName="Helvetica-Bold",
                 alignment=TA_CENTER, leading=50))],
    [Paragraph("COMPLETE STUDY NOTES",
               S("CV3", fontSize=18, textColor=colors.HexColor("#ffe0b2"),
                 fontName="Helvetica-Bold", alignment=TA_CENTER, leading=24))],
    [sp(8)],
    [HRFlowable(width="70%", thickness=2.5, color=GOLD, spaceAfter=8, spaceBefore=4)],
    [Paragraph("Drafting an Effective Résumé",
               S("T1", fontSize=13, textColor=GOLD, fontName="Helvetica-Bold",
                 alignment=TA_CENTER, leading=18))],
    [Paragraph("Facing Job Interviews",
               S("T2", fontSize=13, textColor=GOLD, fontName="Helvetica-Bold",
                 alignment=TA_CENTER, leading=18))],
    [Paragraph("Emotional Intelligence &amp; Critical Thinking",
               S("T3", fontSize=13, textColor=GOLD, fontName="Helvetica-Bold",
                 alignment=TA_CENTER, leading=18))],
    [Paragraph("Applied Grammar",
               S("T4", fontSize=13, textColor=GOLD, fontName="Helvetica-Bold",
                 alignment=TA_CENTER, leading=18))],
    [sp(12)],
    [Paragraph("Max Marks: 75 | Exam Probability Rated | All Q&amp;A Types | 200+ Grammar Examples",
               S("CV6", fontSize=11, textColor=WHITE, fontName="Helvetica",
                 alignment=TA_CENTER, leading=16))],
    [sp(14)],
]
cov = Table(rows, colWidths=[17*cm])
cov.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1), DARK),
    ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
    ("LEFTPADDING",(0,0),(-1,-1),16),("RIGHTPADDING",(0,0),(-1,-1),16),
]))
story.append(cov)
story.append(sp(18))

leg = [["1.5 Marks (~50 words)", "5 Marks (300-500 words)",
        "10 Marks (500-700 words)", "15 Marks (700-1000 words)"]]
lt = Table(leg, colWidths=[4*cm, 4.5*cm, 4.5*cm, 4.5*cm])
lt.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(0,0), GREEN_M),("BACKGROUND",(1,0),(1,0), BLUE),
    ("BACKGROUND",(2,0),(2,0), AMBER),("BACKGROUND",(3,0),(3,0), CRIMSON),
    ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),9),
    ("FONTCOLOR",(0,0),(-1,-1), WHITE),("ALIGN",(0,0),(-1,-1),"CENTER"),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
]))
story.append(lt)
story.append(PageBreak())

# ── TOC ──────────────────────────────────────────────────────────────────────
story.append(banner("&#128196;  TABLE OF CONTENTS — WEEK 12"))
story.append(sp(10))
toc = [
    ("1","Drafting an Effective Résumé","95%"),
    ("","  1.1  Résumé vs CV — Differences & Uses",""),
    ("","  1.2  Types of Résumé Formats",""),
    ("","  1.3  All 9 Components in Detail",""),
    ("","  1.4  10 Golden Rules of Résumé Writing",""),
    ("","  1.5  Action Verbs Master List (100+)",""),
    ("","  1.6  Common Mistakes & Corrections",""),
    ("","  1.7  Complete Sample Résumé (Fresher & Experienced)",""),
    ("2","Facing Job Interviews","92%"),
    ("","  2.1  Before, During & After Interview Strategy",""),
    ("","  2.2  Body Language in Interviews",""),
    ("","  2.3  STAR Method — Full Guide with Examples",""),
    ("","  2.4  50 Common Interview Questions & Model Answers",""),
    ("","  2.5  Salary Negotiation Basics",""),
    ("","  2.6  Thank-You Email Template",""),
    ("3","Emotional Intelligence & Critical Thinking","88%"),
    ("","  3.1  EQ — Goleman's 5 Components (Full Detail)",""),
    ("","  3.2  EQ in the Workplace",""),
    ("","  3.3  Critical Thinking — Definition & Process",""),
    ("","  3.4  Barriers to Critical Thinking",""),
    ("","  3.5  EQ vs IQ vs CQ",""),
    ("4","Applied Grammar","90%"),
    ("","  4.1  Parts of Speech — Full Review",""),
    ("","  4.2  Tenses — All 12 with Examples",""),
    ("","  4.3  Active vs Passive Voice",""),
    ("","  4.4  Common Grammatical Errors (50+ Corrections)",""),
    ("","  4.5  Subject-Verb Agreement Rules",""),
    ("","  4.6  Articles, Prepositions & Conjunctions",""),
    ("","  4.7  Punctuation Rules",""),
]
for num, title, pct in toc:
    is_main = bool(num)
    if is_main:
        row = [[Paragraph(f"<b>{num}.</b>  {title}", toc_i),
                Paragraph(f"<b>{pct}</b>",
                          S("TP", fontSize=10, textColor=AMBER, fontName="Helvetica-Bold",
                            alignment=TA_RIGHT, leading=14))]]
        rt = Table(row, colWidths=[14*cm, 3*cm])
        rt.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1), BLUE_L),
            ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
            ("LEFTPADDING",(0,0),(0,0),10),("LINEBELOW",(0,0),(-1,-1),0.5, SKY),
        ]))
    else:
        row = [[Paragraph(title, S("TS", fontSize=9.5, textColor=GRAY_M, fontName="Helvetica",
                                   leading=14, leftIndent=20))]]
        rt = Table(row, colWidths=[17*cm])
        rt.setStyle(TableStyle([
            ("TOPPADDING",(0,0),(-1,-1),2),("BOTTOMPADDING",(0,0),(-1,-1),2),
            ("LEFTPADDING",(0,0),(-1,-1),10),
            ("LINEBELOW",(0,0),(-1,-1),0.2, colors.HexColor("#e0e0e0")),
        ]))
    story.append(rt)
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# TOPIC 1 — DRAFTING AN EFFECTIVE RÉSUMÉ
# ══════════════════════════════════════════════════════════════════════════════
story.append(banner("TOPIC 1: DRAFTING AN EFFECTIVE RÉSUMÉ", DARK))
story.append(sp(10))
story.append(sec_hdr("1","Drafting an Effective Résumé","95%", TEAL_M))
story.append(sp(8))

story.append(Paragraph("1.1 Résumé vs CV", sub1))
story.append(grid(
    ["Dimension","Résumé","Curriculum Vitae (CV)"],
    [
        ["Meaning","French: 'summary'","Latin: 'course of life'"],
        ["Length","1–2 pages","2–10+ pages"],
        ["Purpose","Private-sector job applications","Academic, research, government roles"],
        ["Content","Targeted to specific job","Complete academic & professional history"],
        ["Customisation","Yes — different per application","Updated; not tailored per application"],
        ["Used in","USA, Canada, private sector globally","UK, Europe, academia, government"],
        ["Photo?","Generally excluded","Sometimes required (varies by country)"],
        ["References","'Available on request'","Often listed in full"],
    ],
    [3.5*cm, 6.5*cm, 6.5*cm]
))
story.append(sp(8))

story.append(Paragraph("1.2 Types of Résumé Formats:", sub1))
resume_format_data = [
    ("CHRONOLOGICAL", TEAL_M,
     "Lists work experience in REVERSE chronological order (latest first). "
     "Most widely used and preferred by employers. Shows career progression clearly. "
     "Best for: professionals with consistent, relevant work history in the same field. "
     "ATS-friendly. Easy to read. "
     "Weakness: Exposes employment gaps; not ideal for career changers."),
    ("FUNCTIONAL (Skills-Based)", BLUE,
     "Organises content around skills and competencies rather than chronological jobs. "
     "Skills sections come before work history. "
     "Best for: career changers, people with employment gaps, fresh graduates with limited work experience. "
     "Weakness: Employers may view it with suspicion; ATS-unfriendly."),
    ("COMBINATION (Hybrid)", PURPLE_M,
     "Opens with a prominent skills/competencies summary, followed by chronological work history. "
     "Best of both worlds. Best for: experienced professionals making strategic career changes. "
     "Weakness: Can exceed 2 pages if not carefully edited."),
    ("TARGETED", CRIMSON,
     "Every line of the résumé is customised specifically for ONE job at ONE company. "
     "Uses exact language and keywords from the job description. "
     "Highest success rate but most time-intensive. Requires a different version for each application."),
    ("INFOGRAPHIC / VISUAL", AMBER,
     "Uses visual design elements — timelines, icons, charts, colour bars. "
     "Best for: creative/design/marketing roles where visual communication is valued. "
     "NOT for: corporate, legal, technical, or any ATS-screened applications."),
]
for fmt, color, desc in resume_format_data:
    hd = [[Paragraph(f"<b>{fmt}</b>", S("FH", fontSize=11, textColor=WHITE,
                                         fontName="Helvetica-Bold", leading=14))]]
    ht = Table(hd, colWidths=[16.5*cm])
    ht.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), color),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),12),
    ]))
    story.append(ht)
    story.append(Paragraph(desc, S("FD", fontSize=10, textColor=BLACK, fontName="Helvetica",
                                   leading=14, alignment=TA_JUSTIFY,
                                   leftIndent=12, rightIndent=12, spaceBefore=4, spaceAfter=6)))
    story.append(sp(4))

story.append(sp(4))
story.append(Paragraph("1.3 All 9 Components of a Résumé — In Full Detail:", sub1))
story.append(sp(5))

components = [
    ("COMPONENT 1: HEADER / CONTACT INFORMATION", DARK,
     "The very top of your résumé. The first thing a recruiter sees.<br/><br/>"
     "<b>Must Include:</b><br/>"
     "&#9654; Full Name — largest text on the page (14-18pt bold)<br/>"
     "&#9654; Professional Email — firstname.lastname@gmail.com (NOT coolguy99@hotmail.com)<br/>"
     "&#9654; Phone Number — with country code for international applications<br/>"
     "&#9654; City and State/Country (not full street address — privacy risk)<br/>"
     "&#9654; LinkedIn Profile URL — shortened: linkedin.com/in/yourname<br/>"
     "&#9654; Portfolio / GitHub / Website — if relevant to the role<br/><br/>"
     "<b>DO NOT Include:</b><br/>"
     "&#9888; Date of Birth &#9888; Religion / Caste &#9888; Marital Status<br/>"
     "&#9888; Photo (unless specifically required — rare in India's private sector)<br/>"
     "&#9888; National ID / Aadhaar / PAN number<br/><br/>"
     "<b>Example Header:</b><br/>"
     "PRIYA SHARMA<br/>"
     "priya.sharma@gmail.com | +91-98765-43210 | Bengaluru, KA<br/>"
     "linkedin.com/in/priyasharma | github.com/priyasharma"),
    ("COMPONENT 2: PROFESSIONAL SUMMARY", TEAL_M,
     "A 3-4 line targeted paragraph immediately after the header. "
     "REPLACES the old-fashioned 'Career Objective.' Should be: specific, achievement-referenced, "
     "and aligned to the target role.<br/><br/>"
     "<b>Formula:</b> [Role/Title] with [X years] of [key expertise]. "
     "[Best achievement with number]. Seeking to [career goal aligned to role].<br/><br/>"
     "<b>WEAK Example (Generic — Avoid):</b><br/>"
     "<i>'Motivated individual seeking a challenging position in a reputed organisation where I can "
     "utilise my skills and grow professionally.'</i> — Says nothing. Gets you rejected.<br/><br/>"
     "<b>STRONG Example (Specific — Use This Style):</b><br/>"
     "<i>'Data-driven Marketing Manager with 5 years building B2B SaaS brands. Led content strategy "
     "that grew qualified pipeline by 67% in FY2024. Seeking a senior marketing leadership role "
     "to drive product-led growth at a Series B+ organisation.'</i>"),
    ("COMPONENT 3: WORK EXPERIENCE", BLUE,
     "The most critical section for experienced professionals. Presented in REVERSE CHRONOLOGICAL order.<br/><br/>"
     "<b>Format for each role:</b><br/>"
     "[Job Title] | [Company Name] | [City, Country] | [Month Year – Month Year or Present]<br/>"
     "&#9654; 3-5 bullet points per role<br/>"
     "&#9654; Every bullet starts with a STRONG ACTION VERB<br/>"
     "&#9654; Every bullet is an ACHIEVEMENT, not a duty<br/>"
     "&#9654; Every achievement has a NUMBER (%, Rs., count, time saved)<br/><br/>"
     "<b>WEAK (Duty-based — Never write this):</b><br/>"
     "<i>• Was responsible for managing the company's social media accounts</i><br/>"
     "<i>• Handled customer service queries and complaints</i><br/><br/>"
     "<b>STRONG (Achievement-based — Always write this):</b><br/>"
     "<i>• Grew Instagram engagement rate from 1.2% to 4.8% in 4 months by launching "
     "daily Reels strategy, adding 28,000 followers</i><br/>"
     "<i>• Reduced customer complaint resolution time by 42% by implementing AI-powered "
     "ticketing system, improving CSAT score from 3.2 to 4.6/5.0</i>"),
    ("COMPONENT 4: EDUCATION", PURPLE_M,
     "Reverse chronological. Format:<br/>"
     "[Degree Name] | [Institution Name] | [City] | [Year] | [CGPA or %]<br/><br/>"
     "<b>For Fresh Graduates/Students (add these sub-elements):</b><br/>"
     "&#9654; Relevant Coursework: Machine Learning, Data Structures, DBMS<br/>"
     "&#9654; Final Year Project: Brief description + tech stack<br/>"
     "&#9654; Academic Achievements: Rank, scholarships, awards<br/><br/>"
     "<b>For Experienced Professionals:</b><br/>"
     "Keep education brief — 2-3 lines. Recruiters focus on work experience.<br/><br/>"
     "<b>Example:</b><br/>"
     "B.Tech, Computer Science Engineering | IIT Bombay | Mumbai | 2022 | CGPA: 8.7/10"),
    ("COMPONENT 5: SKILLS", CRIMSON,
     "Divide into TWO clear categories:<br/><br/>"
     "<b>Technical / Hard Skills:</b> Specific tools, languages, platforms, certifications.<br/>"
     "Examples: Python, SQL, React.js, Tableau, AutoCAD, Tally, Adobe Premiere Pro<br/><br/>"
     "<b>Professional / Soft Skills:</b> Interpersonal and cognitive competencies.<br/>"
     "Examples: Project Management, Cross-functional Leadership, Public Speaking, Data Storytelling<br/><br/>"
     "<b>CRITICAL — ATS Optimisation:</b><br/>"
     "Read the job description carefully. Extract all required skills. "
     "Use their EXACT language in your skills section. "
     "ATS software matches keywords — if you write 'MS Excel' but they want 'Microsoft Excel', you may not match."),
    ("COMPONENT 6: PROJECTS", TEAL_M,
     "Essential for fresh graduates. Very useful for career changers.<br/><br/>"
     "<b>Format:</b><br/>"
     "[Project Name] | [Role] | [Link if available]<br/>"
     "&#9654; What it does (1 line)<br/>"
     "&#9654; Technologies / tools used<br/>"
     "&#9654; Your specific contribution<br/>"
     "&#9654; Outcome or impact (even if estimated)<br/><br/>"
     "<b>Example:</b><br/>"
     "HealthTrack — AI-Powered Symptom Checker | github.com/user/healthtrack<br/>"
     "<i>• Built NLP-based symptom analysis API using Python and BERT, achieving 89% accuracy<br/>"
     "• Deployed on Heroku; 500+ users in 2-week beta test</i>"),
    ("COMPONENT 7: CERTIFICATIONS & ACHIEVEMENTS", AMBER,
     "List professional certifications, online courses, competition wins, publications, scholarships.<br/><br/>"
     "<b>Format:</b> [Certification Name] | [Issuing Organisation] | [Year]<br/><br/>"
     "<b>Examples:</b><br/>"
     "&#9654; AWS Certified Solutions Architect – Associate | Amazon | 2024<br/>"
     "&#9654; Google Data Analytics Professional Certificate | Google | 2023<br/>"
     "&#9654; Winner — Smart India Hackathon 2022 (National Level, 12,000 participants)<br/>"
     "&#9654; Published: 'Optimising Transformer Models for Low-Resource Languages' — ACL 2024<br/><br/>"
     "<b>AVOID:</b> Listing courses you haven't completed, outdated certifications (10+ years old), "
     "or irrelevant achievements."),
    ("COMPONENT 8: EXTRACURRICULARS / LEADERSHIP", BLUE,
     "ONLY include if they demonstrate transferable professional skills or leadership.<br/><br/>"
     "<b>Good Examples:</b><br/>"
     "&#9654; President, Entrepreneurship Cell | IIT Madras | 2021-22<br/>"
     "    — Scaled annual membership 3x (150 to 450 members); organised 15 speaker events<br/>"
     "&#9654; National Basketball Player — India Under-19 Squad, 2020-21<br/><br/>"
     "<b>Avoid Including:</b><br/>"
     "&#9888; 'Hobbies: Cooking, watching Netflix, sleeping' — says nothing professional<br/>"
     "&#9888; School-level achievements for professionals with 5+ years experience"),
    ("COMPONENT 9: REFERENCES", DARK,
     "'References available upon request.'<br/><br/>"
     "This is the ONLY content needed for references on a résumé. "
     "NEVER list actual reference names, phone numbers, or emails on the résumé itself.<br/><br/>"
     "<b>Why:</b> You need to brief your references before a recruiter calls them. "
     "Listing them without warning is unprofessional.<br/><br/>"
     "Prepare a separate 'References Sheet' (3 professional references with name, designation, "
     "company, email, phone) to provide only when specifically requested."),
]
for comp, color, desc in components:
    hd = [[Paragraph(comp, S("CH", fontSize=11, textColor=WHITE,
                             fontName="Helvetica-Bold", leading=14))]]
    ht = Table(hd, colWidths=[16.5*cm])
    ht.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), color),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
        ("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),12),
    ]))
    story.append(ht)
    story.append(Paragraph(desc, S("CD", fontSize=10, textColor=BLACK, fontName="Helvetica",
                                   leading=14, alignment=TA_JUSTIFY,
                                   leftIndent=12, rightIndent=12, spaceBefore=5, spaceAfter=7)))
    story.append(sp(4))

story.append(sp(4))
story.append(Paragraph("1.4  The 10 Golden Rules of Résumé Writing:", sub1))
rules = [
    ("Rule 1: Achievement-Not-Duty", "Every bullet = achievement + number. Never list duties. "
     "Duty: 'Managed project timelines.' Achievement: 'Delivered 6 projects on time, reducing deadline "
     "overruns by 80% vs company average.'"),
    ("Rule 2: Start Every Bullet with a Power Verb", "Achieved · Accelerated · Built · Championed · Created · "
     "Delivered · Designed · Drove · Enhanced · Executed · Generated · Grew · Implemented · Increased · "
     "Launched · Led · Mentored · Negotiated · Optimised · Produced · Reduced · Saved · Scaled · Spearheaded · "
     "Streamlined · Transformed · Won. NEVER start with 'Was responsible for' or 'Helped to.'"),
    ("Rule 3: Quantify Everything", "If you can attach a number — do it. %, Rs., count, time, rank, ratio. "
     "'Improved sales' → 'Grew sales by 42% QoQ.'"),
    ("Rule 4: Tailor to Every Application", "No generic résumés. Read the JD. Identify top 10 keywords. "
     "Ensure your résumé addresses each one using their language."),
    ("Rule 5: ATS Optimisation", "Use exact keywords from the JD. Standard headings only. "
     "No tables/columns/graphics/text boxes. Submit as PDF (unless ATS says Word)."),
    ("Rule 6: 1-2 Pages Maximum", "Under 5 years = 1 page. 5-15 years = 2 pages. "
     "Senior (15+ years) = 2-3 pages max. A longer résumé is not more impressive."),
    ("Rule 7: Professional Formatting", "Fonts: Calibri, Garamond, or Arial. Body: 10-11pt. "
     "Headings: 12-14pt. Margins: 1.5-2.5cm. Consistent spacing. Clean white space."),
    ("Rule 8: Zero Tolerance for Errors", "ONE typo = instant rejection signal. "
     "Proofread 3 times. Use Grammarly. Have someone else review. Read aloud."),
    ("Rule 9: Reverse Chronological Always", "Most recent = first. Recruiters read top-to-bottom. "
     "Put your strongest, most relevant experience at the top."),
    ("Rule 10: Absolute Honesty", "Inflating titles, fabricating degrees, exaggerating achievements — "
     "background checks and reference calls expose all lies. Career-ending and legally actionable."),
]
for r, d in rules:
    story.append(Paragraph(f"<b>{r}:</b> {d}", bul))
    story.append(sp(3))
story.append(sp(6))

story.append(Paragraph("1.5  Power Action Verbs Master List (by category):", sub1))
verb_data = [
    ["LEADERSHIP", "ANALYSIS", "ACHIEVEMENT", "COMMUNICATION", "INNOVATION"],
    ["Led / Directed", "Analysed / Evaluated", "Achieved / Exceeded", "Presented / Delivered", "Designed / Created"],
    ["Managed / Supervised", "Assessed / Audited", "Generated / Produced", "Negotiated / Persuaded", "Developed / Built"],
    ["Mentored / Coached", "Forecasted / Modelled", "Won / Ranked", "Advocated / Promoted", "Launched / Piloted"],
    ["Delegated / Coordinated", "Investigated / Researched", "Surpassed / Outperformed", "Authored / Published", "Engineered / Architected"],
    ["Spearheaded / Championed", "Identified / Diagnosed", "Saved / Reduced", "Collaborated / Partnered", "Transformed / Revamped"],
    ["Established / Founded", "Optimised / Improved", "Grew / Expanded", "Consulted / Advised", "Pioneered / Innovated"],
    ["Executed / Implemented", "Reviewed / Reported", "Doubled / Tripled", "Trained / Educated", "Automated / Streamlined"],
]
vt = Table(verb_data, colWidths=[3.3*cm, 3.3*cm, 3.3*cm, 3.3*cm, 3.3*cm])
vt.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0), DARK),
    ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, BLUE_L]),
    ("BOX",(0,0),(-1,-1),1, BLUE),("INNERGRID",(0,0),(-1,-1),0.4, SKY),
    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
    ("FONTNAME",(0,1),(-1,-1),"Helvetica"),
    ("FONTCOLOR",(0,0),(-1,0), WHITE),
    ("FONTSIZE",(0,0),(-1,-1),9),
    ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),
    ("ALIGN",(0,0),(-1,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
]))
story.append(vt)
story.append(sp(8))

story.append(Paragraph("1.6  20 Most Common Résumé Mistakes:", sub1))
mistakes = [
    "Using generic objective: 'Seeking a challenging position...' — means nothing.",
    "Writing duties not achievements: 'Managed social media' not 'Grew followers by 340%'.",
    "No quantification: 'Improved sales' without saying by HOW MUCH.",
    "Submitting the same résumé for every job without tailoring.",
    "Spelling errors, grammar mistakes, or inconsistent formatting.",
    "Wrong email address: coolguy99 or a childish handle.",
    "Including photo, age, marital status unnecessarily.",
    "Using tables and columns — ATS cannot parse them.",
    "Exceeding 2 pages for under 5 years of experience.",
    "Including every job back to high school — only last 10 years matter.",
    "Using passive voice: 'Was responsible for' instead of 'Led'.",
    "Inconsistent dates or unexplained gaps without a brief note.",
    "Listing skills you cannot demonstrate — immediate red flag in interviews.",
    "No LinkedIn profile or LinkedIn inconsistent with résumé.",
    "Using a functional format when you have good work experience.",
    "Placing education before experience (unless you are a fresh graduate).",
    "Long paragraphs instead of concise bullet points.",
    "No professional summary — leaving the top of the résumé empty.",
    "Generic skill lists: 'Good communication skills' — prove it with achievements.",
    "Not saving as PDF — Word documents look different on every device.",
]
for i, m in enumerate(mistakes, 1):
    story.append(Paragraph(f"&#9888; {i}. {m}", bul))
story.append(sp(6))

story.append(Paragraph("1.7  Complete Sample Résumé (Fresh Graduate):", sub1))
story.append(sp(4))
story.append(resume_sample([
    "## ANIKA SHARMA",
    "# anika.sharma@gmail.com | +91-97865-23410 | Mumbai, MH",
    "# linkedin.com/in/anikasharma | github.com/anikasharma",
    "---",
    "# PROFESSIONAL SUMMARY",
    "Computer Science graduate (CGPA 9.1/10, NIT Surat, 2025) with hands-on",
    "experience in full-stack development and machine learning. Built a live",
    "EdTech platform serving 3,000+ users. AWS Certified Cloud Practitioner.",
    "Seeking a Software Engineer role at a product-driven organisation.",
    "---",
    "# WORK EXPERIENCE",
    "Software Development Intern | FinFlow Technologies | Mumbai | Jan–Jul 2025",
    "  • Built REST APIs handling 120,000+ daily transactions using Node.js + PostgreSQL",
    "  • Reduced page load time by 55% through lazy loading and CDN optimisation",
    "  • Automated monthly invoicing system, eliminating 20 hrs of manual work/month",
    "",
    "Web Development Intern | StartupNest | Pune | Jun–Aug 2024",
    "  • Redesigned company website using React, improving bounce rate from 72% to 41%",
    "  • Implemented SEO best practices, growing organic traffic by 180% in 8 weeks",
    "---",
    "# EDUCATION",
    "B.Tech, Computer Science Engineering",
    "  NIT Surat | 2025 | CGPA: 9.1/10 | Rank: 3 of 180",
    "  Relevant Coursework: ML, DSA, DBMS, Cloud Computing, NLP",
    "---",
    "# TECHNICAL SKILLS",
    "Languages : Python, JavaScript, TypeScript, SQL, HTML/CSS",
    "Frameworks : React, Node.js, Express, Django, FastAPI",
    "Tools/Cloud: AWS (EC2, S3, Lambda), Docker, Git, MongoDB",
    "---",
    "# KEY PROJECTS",
    "EduAdapt — AI Personalised Learning Platform | github.com/anika/eduadapt",
    "  • NLP-based adaptive quiz engine (Python, BERT); 89% accuracy on 5,000 test cases",
    "  • Onboarded 3,000 users in 2-month beta; rated 4.7/5.0 by users",
    "",
    "CarbonTrack — Real-Time Emissions Dashboard | github.com/anika/carbontrack",
    "  • Real-time IoT data pipeline (MQTT + Node.js) processing 10,000 readings/min",
    "---",
    "# CERTIFICATIONS & ACHIEVEMENTS",
    "  • AWS Certified Cloud Practitioner | Amazon | 2024",
    "  • Google UX Design Certificate | Google | 2024",
    "  • 1st Prize — NIT Hackathon 2023 (500 participants)",
    "  • Merit Scholarship, NIT Surat (Top 5% of cohort, 3 consecutive years)",
    "---",
    "  References available upon request.",
], "COMPLETE SAMPLE RÉSUMÉ — FRESH GRADUATE (1 Page Template)"))
story.append(sp(8))

story.append(q_hdr("PRACTICE QUESTIONS — TOPIC 1: Drafting an Effective Résumé", TEAL_M))
story.append(sp(6))
for item in q_box("1.5 MARKS", GREEN_M, "What is an ATS and why does it matter for résumé writing?",
    "ATS (Applicant Tracking System) is software used by most large companies to automatically scan, "
    "filter, and rank résumés before a human recruiter sees them. It searches for keywords from the "
    "job description. Résumés must use exact keywords from the JD, standard section headings, and "
    "simple formatting (no tables or graphics) to pass ATS screening."):
    story.append(item)
for item in q_box("10 MARKS (500-700 words)", AMBER,
    "What is a résumé? Explain its key components and the principles of effective résumé writing.",
    "<b>Introduction:</b><br/>A résumé is a concise, targeted, professional document summarising a "
    "candidate's qualifications, experience, skills, and achievements for a specific job application. "
    "Its sole purpose is to earn an interview. Research shows recruiters spend 6-7 seconds on initial "
    "résumé review — every design and content decision must serve the goal of passing that 7-second test.<br/><br/>"
    "<b>Components of a Résumé:</b><br/>"
    "1. <b>Header:</b> Name, professional email, phone, city, LinkedIn. No photo, birthdate, or religion.<br/>"
    "2. <b>Professional Summary:</b> 3-4 targeted lines: identity + key achievement + career goal aligned to role. "
    "NOT a generic objective statement.<br/>"
    "3. <b>Work Experience:</b> Reverse chronological. Each role: title | company | dates + 3-5 achievement "
    "bullets. Every bullet: strong action verb + achievement + number.<br/>"
    "4. <b>Education:</b> Degree | Institution | Year | CGPA. Freshers add projects and relevant coursework.<br/>"
    "5. <b>Skills:</b> Technical (Python, SQL) and Professional (Leadership, Communication). "
    "Mirror JD keywords exactly for ATS.<br/>"
    "6. <b>Projects:</b> Name | Role | Tech | Outcome. Essential for freshers. Include links if available.<br/>"
    "7. <b>Certifications & Achievements:</b> With issuing body and year.<br/>"
    "8. <b>Extracurriculars:</b> Only if showing transferable professional skills.<br/>"
    "9. <b>References:</b> 'Available upon request' — never list names on résumé.<br/><br/>"
    "<b>10 Golden Principles:</b><br/>"
    "1. Achievement-not-duty (quantify everything with numbers)<br/>"
    "2. Power action verbs to start every bullet<br/>"
    "3. Tailor to every application using JD keywords<br/>"
    "4. ATS-optimised (standard headings, no graphics/tables)<br/>"
    "5. 1-2 pages maximum<br/>"
    "6. Professional formatting (Calibri/Arial, 10-11pt, PDF format)<br/>"
    "7. Zero spelling or grammar errors<br/>"
    "8. Reverse chronological order throughout<br/>"
    "9. Specific not generic (data, not adjectives)<br/>"
    "10. Absolute honesty<br/><br/>"
    "<b>Conclusion:</b> A résumé is not a historical record — it is a targeted persuasion document. "
    "Every line must justify its presence by communicating specific, measurable value to the specific employer."):
    story.append(item)
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# TOPIC 2 — FACING JOB INTERVIEWS
# ══════════════════════════════════════════════════════════════════════════════
story.append(banner("TOPIC 2: FACING JOB INTERVIEWS", NAVY))
story.append(sp(10))
story.append(sec_hdr("2","Facing Job Interviews","92%", BLUE))
story.append(sp(8))

story.append(Paragraph("2.1  The 3-Phase Interview Strategy:", sub1))
story.append(sp(4))

phases = [
    ("PHASE 1: BEFORE THE INTERVIEW", DARK, [
        ("Research the Company (3-4 hours minimum)",
         "History, founding story, products/services, revenue, key customers, competitors, "
         "recent news (last 6 months), culture/values (Glassdoor, company blog), leadership team."),
        ("Analyse the Job Description",
         "Underline every requirement. Map each to your experience. "
         "Identify the top 5 most critical skills they need. "
         "Prepare at least one STAR story for each."),
        ("Know Your Résumé Inside Out",
         "Be ready to elaborate on every single line. "
         "Prepare your 'career story' — connect your past to this role to your future."),
        ("Prepare 8-10 STAR Stories",
         "Cover: leadership, teamwork, conflict, failure (with learning), achievement, "
         "initiative, creativity, pressure handling, client management, learning agility."),
        ("Prepare Intelligent Questions to Ask",
         "'What does success look like in this role at 6 months?' "
         "'What are the biggest challenges the team currently faces?' "
         "'How does the company support professional development?' "
         "AVOID: 'What is the salary?' as first question."),
        ("Logistics: Plan Everything",
         "Route and travel time. Arrive 10-15 minutes early. "
         "Appropriate professional attire (when in doubt: more formal). "
         "Documents: 3 copies of résumé, certificates, ID, notepad, pen. "
         "Silence phone. Get 8 hours sleep. Eat a light meal."),
    ]),
    ("PHASE 2: DURING THE INTERVIEW", TEAL_M, [
        ("First Impression (First 30 seconds)",
         "Firm, confident handshake. Direct eye contact. Genuine smile. "
         "Walk in with purpose — confident posture, shoulders back. "
         "Wait to be offered a seat. Place documents neatly on the table."),
        ("Active Listening",
         "Listen to the COMPLETE question before formulating an answer. "
         "Do NOT interrupt. If you did not understand, ask for clarification: "
         "'Could you please elaborate on what you mean by...?'"),
        ("Answering Technique",
         "Conversational, natural pace — not rushed or robotic. "
         "STAR method for all behavioural questions. "
         "Target 1.5-2 minutes per answer. Not 30 seconds (too brief) or 5 minutes (rambling). "
         "Pause and think before complex questions — 3 seconds is acceptable."),
        ("Stay Positive Always",
         "Never criticise previous employers, colleagues, or managers — even if true. "
         "Frame all 'negative' experiences positively: 'That experience taught me...'"),
        ("Ask Your Questions Strategically",
         "Usually at end. Ask 2-3 prepared questions. "
         "Shows genuine interest and preparation. Elevates you above candidates who ask nothing."),
        ("Close Confidently",
         "Express enthusiasm clearly: 'I am very excited about this opportunity. "
         "Based on our conversation, I am confident I could make a strong contribution to the team.' "
         "Ask about next steps: 'What are the next steps in your selection process?'"),
    ]),
    ("PHASE 3: AFTER THE INTERVIEW", PURPLE_M, [
        ("Send Thank-You Email Within 24 Hours",
         "Address the main interviewer (and CC others if known). "
         "Reference a specific topic from your conversation. "
         "Reiterate your enthusiasm and fit. Keep it to 3-4 short paragraphs."),
        ("Self-Debrief",
         "What questions caught you off-guard? Research better answers. "
         "What did you do well? Reinforce. What would you change? Adjust."),
        ("Follow Up Professionally",
         "If no response after the stated timeline, send ONE polite follow-up. "
         "Do NOT call multiple times or email daily — signals desperation."),
        ("Multiple Applications",
         "Never put all eggs in one basket. Keep applying and interviewing "
         "until you have a written offer in hand."),
    ]),
]
for phase, color, points in phases:
    hd = [[Paragraph(phase, S("PH", fontSize=12, textColor=WHITE,
                              fontName="Helvetica-Bold", leading=16))]]
    ht = Table(hd, colWidths=[16.5*cm])
    ht.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), color),
        ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),12),
    ]))
    story.append(ht)
    for pt, desc in points:
        story.append(Paragraph(f"<b>&#9654; {pt}:</b> {desc}", bul))
        story.append(sp(2))
    story.append(sp(6))

story.append(Paragraph("2.2  Body Language in Interviews:", sub2))
story.append(grid(
    ["Non-Verbal Signal", "DO THIS", "AVOID THIS"],
    [
        ["Handshake", "Firm, 2-pump, direct eye contact", "Limp/crushing/sweaty; no eye contact"],
        ["Eye Contact", "Steady 3-5 sec per contact; natural breaks", "Staring unblinking or constantly avoiding"],
        ["Posture", "Upright, slight forward lean, open chest", "Slouching, crossed arms, leaning back"],
        ["Hands", "Resting on table; natural open gestures", "Fidgeting, touching face/hair, drumming"],
        ["Facial Expression", "Engaged, nodding, genuine smiling", "Blank face, frowning, nervous laughing"],
        ["Legs", "Both feet on floor; parallel", "Crossing, bouncing, wrapping around chair"],
        ["Voice", "Confident, moderate pace, varied tone", "Rushing, monotone, too soft, vocal fry"],
        ["Entry/Exit", "Confident stride, knock, wait for invite", "Rushing in, slouching, quick exit"],
    ],
    [3*cm, 6.5*cm, 7*cm], DARK
))
story.append(sp(6))

story.append(Paragraph("2.3  The STAR Method — Complete Guide:", sub2))
story.append(ibox(
    "STAR = Situation → Task → Action → Result",
    "<b>S — Situation:</b> Set the specific scene. When? Where? Who was involved? What was the context? "
    "Keep brief — 1-2 sentences. 'In my second year at company X, our largest client threatened to leave...'<br/><br/>"
    "<b>T — Task:</b> What was YOUR specific responsibility in this situation? "
    "What were you asked to do or what did you realise needed to be done? "
    "KEY: Use 'I', not 'we' — they are evaluating YOU specifically.<br/><br/>"
    "<b>A — Action:</b> The heart of your answer. What specific steps did YOU take? "
    "HOW did you approach it? Why did you make those specific choices? "
    "This is where you demonstrate competence, creativity, and judgement.<br/><br/>"
    "<b>R — Result:</b> What was the measurable outcome? Quantify wherever possible. "
    "What did you learn? What would you do differently?",
    GOLD_L, BROWN, GOLD
))
story.append(sp(5))

story.append(Paragraph("STAR Example — 'Tell me about a time you led a difficult team project':", sub2))
star_ex = [
    ["S — Situation",
     "During my third year at TechCorp, our flagship mobile app had 0 reviews after 3 months of launch "
     "and management was considering discontinuing it."],
    ["T — Task",
     "I was assigned as project lead to identify the root causes of low adoption and propose "
     "a turnaround strategy within 30 days."],
    ["A — Action",
     "I conducted 50 user interviews in 2 weeks, synthesised findings into 3 core problems: "
     "poor onboarding, slow performance, and missing key features. I held daily 15-minute standups, "
     "reallocated developer resources from 3 other projects (with management approval), "
     "and personally managed the redesigned onboarding flow."],
    ["R — Result",
     "Within 6 weeks, app ratings reached 4.2/5.0 with 1,200 new reviews. "
     "DAU (Daily Active Users) grew 280%. Management not only continued the app "
     "but allocated an additional budget of Rs. 50 lakhs for further development."],
]
star_t = Table(star_ex, colWidths=[3.5*cm, 13*cm])
star_bg = [TEAL_M, BLUE, PURPLE_M, GREEN_M]
star_style = [
    ("BOX",(0,0),(-1,-1),1, BLUE),("INNERGRID",(0,0),(-1,-1),0.4, SKY),
    ("FONTNAME",(0,0),(-1,-1),"Helvetica"),("FONTSIZE",(0,0),(-1,-1),9.5),
    ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
    ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),
    ("FONTCOLOR",(0,0),(0,-1), WHITE),
]
for i, bg in enumerate(star_bg):
    star_style.append(("BACKGROUND",(0,i),(0,i), bg))
    star_style.append(("BACKGROUND",(1,i),(1,i), BLUE_L if i%2==0 else WHITE))
star_t.setStyle(TableStyle(star_style))
story.append(star_t)
story.append(sp(6))

story.append(Paragraph("2.4  50 Common Interview Questions with Model Answers:", sub2))
interview_qs = [
    ("OPENING QUESTIONS", DARK, [
        ("Tell me about yourself.",
         "Present (current role/study) → Past (key relevant experience) → Future (why this role). "
         "90-second maximum. Professional, not personal. End by connecting to THIS job."),
        ("Why are you interested in this position?",
         "Specific role + specific company knowledge + specific alignment of your skills to their needs. "
         "Show research. Show fit. Never say: 'For career growth' or 'It's a good company.'"),
        ("Why should we hire you?",
         "Summarise your unique value in 3 points directly mapped to their top 3 job requirements. "
         "End with: 'I'm confident I'll contribute meaningfully from day one.'"),
        ("Where do you see yourself in 5 years?",
         "Show ambition aligned to this role's natural progression. "
         "Connect your 5-year goal to what this company can offer. "
         "Avoid: 'In your job' or 'Starting my own business.'"),
    ]),
    ("STRENGTHS & WEAKNESSES", BLUE, [
        ("What are your strengths?",
         "Choose 2-3 directly relevant to the role. Support EACH with a specific achievement. "
         "Not: 'I'm a hard worker.' Say: 'One strength is analytical problem-solving — "
         "at my last role, I identified a data anomaly that saved Rs. 18 lakh in quarterly losses.'"),
        ("What are your weaknesses?",
         "Choose a GENUINE but non-fatal weakness. Show what you are ACTIVELY doing to improve. "
         "Not: 'I work too hard' or 'I'm a perfectionist.' "
         "Say: 'I sometimes over-communicate details in written reports. I've been practising executive "
         "summary writing specifically to lead with insights, not data.'"),
        ("Describe yourself in 3 words.",
         "Choose words that align to the role. Back each with one-line evidence. "
         "'Systematic: I document all processes so the team doesn't depend on institutional memory. "
         "Collaborative: I've been called out in 3 performance reviews for peer support. "
         "Delivery-focused: I've met 100% of deadlines in my last 2 years at current company.'"),
    ]),
    ("BEHAVIOURAL QUESTIONS (Use STAR)", TEAL_M, [
        ("Tell me about a time you failed.",
         "Use STAR. Choose a real failure. Show specific steps you took to recover. "
         "Show what you learned and how it changed your behaviour. "
         "End on a learning/growth note — not dwelling on the failure."),
        ("Describe a situation where you had to handle conflict.",
         "Use STAR. Show empathy, listening, and constructive resolution. "
         "Emphasise: addressed the issue privately; listened first; found common ground; "
         "maintained professional relationship throughout."),
        ("Tell me about a time you showed leadership.",
         "Use STAR. Can be formal or informal leadership. "
         "Focus on what specifically you did, how you influenced others, and the measurable outcome."),
        ("Describe your greatest professional achievement.",
         "Use STAR. Choose your most impressive, quantified achievement relevant to this role. "
         "Walk through what made it challenging, your specific actions, and the concrete result."),
        ("How do you handle pressure and tight deadlines?",
         "Describe your specific system: prioritisation matrix, breaking into sub-tasks, "
         "proactive communication. Then give one STAR example of successful delivery under extreme pressure."),
    ]),
    ("SITUATIONAL QUESTIONS", PURPLE_M, [
        ("What would you do if you disagreed with your manager?",
         "Never say you'd just comply. Show confidence with diplomacy: "
         "'I'd seek a private conversation, present my perspective with supporting data, "
         "listen to understand their reasoning, and if still not aligned, respect the decision "
         "while documenting my concerns professionally.'"),
        ("How would you handle a difficult client?",
         "Listen first without interrupting. Acknowledge their frustration empathetically. "
         "Apologise for their experience (not the company's fault necessarily). "
         "Present a solution. Follow up to confirm resolution. STAR example preferred."),
        ("You're given a task with insufficient instructions. What do you do?",
         "Clarify before starting — ask specific questions to understand deliverables, timeline, "
         "and quality standards. If the manager is unavailable, make reasonable assumptions, "
         "document them, and confirm as soon as possible."),
    ]),
    ("CLOSING QUESTIONS", GREEN_M, [
        ("Do you have any questions for us?",
         "ALWAYS have 3-4 prepared. Recommended questions: "
         "'What does success look like in this role at 90 days?' "
         "'What are the biggest challenges the person in this role will face?' "
         "'How would you describe the team culture?' "
         "'What are the growth paths from this position?'"),
        ("What are your salary expectations?",
         "Research market rate (LinkedIn Salary, Glassdoor, Naukri). Give a range, not a single number. "
         "'Based on my research and experience, I'm targeting between Rs. X and Rs. Y. "
         "I'm open to discussion based on the full compensation package and growth opportunity.'"),
        ("When can you start?",
         "Give your actual notice period. If you can negotiate it down, mention that. "
         "Never promise something you cannot deliver — it starts the relationship with dishonesty."),
    ]),
]
for section, color, qs in interview_qs:
    sh = [[Paragraph(section, S("IQH", fontSize=11, textColor=WHITE,
                                fontName="Helvetica-Bold", alignment=TA_CENTER, leading=14))]]
    ht = Table(sh, colWidths=[16.5*cm])
    ht.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), color),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
    ]))
    story.append(ht)
    for q, a in qs:
        story.append(Paragraph(f"<b>Q: {q}</b>",
                               S("IQQ", fontSize=10, textColor=DARK, fontName="Helvetica-Bold",
                                 leading=14, leftIndent=8, spaceBefore=4)))
        story.append(Paragraph(f"&#9654; {a}",
                               S("IQA", fontSize=10, textColor=BLACK, fontName="Helvetica",
                                 leading=14, leftIndent=16, rightIndent=8, spaceAfter=4,
                                 alignment=TA_JUSTIFY)))
    story.append(sp(6))

story.append(Paragraph("2.5  Thank-You Email Template:", sub2))
story.append(resume_sample([
    "## THANK-YOU EMAIL — SEND WITHIN 24 HOURS",
    "---",
    "To: divya.krishnan@company.com",
    "Subject: Thank You — Software Engineer Interview (22 May 2025)",
    "",
    "Dear Ms. Krishnan,",
    "",
    "Thank you for the opportunity to interview for the Software Engineer role at",
    "FinEdge Technologies yesterday. I thoroughly enjoyed our conversation,",
    "particularly the discussion about your plans to scale the payments infrastructure",
    "to handle 10x transaction volume — a challenge I find genuinely exciting.",
    "",
    "Our conversation reinforced my enthusiasm for this role. My experience building",
    "high-throughput APIs at InnoTech (handling 120,000+ daily transactions) directly",
    "aligns with the challenges you described, and I am confident I could make an",
    "immediate and meaningful contribution to your engineering team.",
    "",
    "Please do not hesitate to reach out if you need any additional information.",
    "I look forward to hearing about the next steps.",
    "",
    "With warm regards,",
    "Anika Sharma",
    "+91-97865-23410 | anika.sharma@gmail.com",
], "THANK-YOU EMAIL TEMPLATE"))
story.append(sp(8))

story.append(q_hdr("PRACTICE QUESTIONS — TOPIC 2: Facing Job Interviews", BLUE))
story.append(sp(6))
for item in q_box("1.5 MARKS", GREEN_M, "What is a Stress Interview?",
    "A stress interview is a type of job interview where the interviewer deliberately creates "
    "pressure — through challenging questions, long uncomfortable silences, contradicting the candidate's "
    "statements, or creating an adversarial atmosphere. Its purpose is to test the candidate's "
    "emotional control, composure under pressure, and ability to think clearly in difficult situations."):
    story.append(item)
for item in q_box("5 MARKS", BLUE,
    "How should a candidate prepare for and face a job interview? Explain the STAR method.",
    "<b>Preparation Strategy:</b><br/>"
    "1. Research company — products, culture, recent news, competition, leadership<br/>"
    "2. Analyse JD — map every requirement to your experience<br/>"
    "3. Prepare 8-10 STAR stories covering key competencies<br/>"
    "4. Practice answering out loud and recording yourself<br/>"
    "5. Prepare 3-4 intelligent questions to ask the interviewer<br/>"
    "6. Plan logistics — route, attire, documents, 10 minutes early<br/><br/>"
    "<b>During the Interview:</b><br/>"
    "Listen fully. Use STAR for behavioural questions. Maintain confident eye contact. "
    "Moderate, clear pace. Stay positive about past employers. Ask your prepared questions.<br/><br/>"
    "<b>STAR Method:</b><br/>"
    "<b>S — Situation:</b> Brief context — when, where, who, what was happening.<br/>"
    "<b>T — Task:</b> Your specific responsibility in that situation.<br/>"
    "<b>A — Action:</b> Exact steps YOU took — HOW and WHY (most important part).<br/>"
    "<b>R — Result:</b> Measurable outcome + learning + what you'd do differently.<br/><br/>"
    "Example: 'Tell me about a time you handled a failing project.' [S] 'In Q2 2024, our app launch "
    "was 6 weeks behind schedule...' [T] 'As PM, my task was to recover the timeline...' "
    "[A] 'I ran a 2-day scope-reduction workshop...' [R] 'We launched 4 weeks later, "
    "within budget, with 96% of planned features...'<br/><br/>"
    "<b>After the Interview:</b> Send thank-you email within 24 hours. Self-debrief. Follow up professionally.<br/><br/>"
    "<b>Conclusion:</b> Interview success is preparation made visible. Practice is the bridge "
    "between preparation and performance."):
    story.append(item)
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# TOPIC 3 — EMOTIONAL INTELLIGENCE & CRITICAL THINKING
# ══════════════════════════════════════════════════════════════════════════════
story.append(banner("TOPIC 3: EMOTIONAL INTELLIGENCE & CRITICAL THINKING", PURPLE_M))
story.append(sp(10))
story.append(sec_hdr("3","Emotional Intelligence & Critical Thinking","88%", PURPLE_M))
story.append(sp(8))

story.append(Paragraph("3.1  Emotional Intelligence (EQ) — Full Concept:", sub1))
story.append(Paragraph(
    "Emotional Intelligence (EQ or EI) is the ability to identify, understand, manage, and "
    "effectively use one's own emotions and the emotions of others in thinking, communication, "
    "and behaviour. The concept was formally developed by psychologists Peter Salovey and "
    "John D. Mayer (1990) and popularised globally by Daniel Goleman's landmark 1995 book "
    "<i>Emotional Intelligence: Why It Can Matter More Than IQ.</i>", body))
story.append(sp(5))

story.append(ibox(
    "Goleman's Definition",
    "'Emotional intelligence refers to the capacity for recognising our own feelings and those "
    "of others, for motivating ourselves, and for managing emotions well in ourselves and in our relationships.' "
    "— Daniel Goleman, 1995",
    PURPLE_L, PURPLE, PURPLE_M
))
story.append(sp(6))

story.append(Paragraph("3.2  Goleman's 5-Component Model of EQ (EXAM CRITICAL):", sub2))
eq_components = [
    ("1. SELF-AWARENESS", PURPLE_M,
     "The ability to recognise and understand your own emotions, strengths, weaknesses, "
     "values, and the impact your behaviour has on others.<br/><br/>"
     "<b>Signs of High Self-Awareness:</b><br/>"
     "&#9654; Know what triggers your anger, anxiety, or excitement<br/>"
     "&#9654; Can accurately assess your own strengths and limitations<br/>"
     "&#9654; Actively seek and act on feedback<br/>"
     "&#9654; Have a clear sense of personal values and purpose<br/>"
     "&#9654; Not surprised by your own emotional reactions<br/><br/>"
     "<b>Development:</b> Journaling, meditation, 360-degree feedback, therapy.<br/>"
     "<b>Workplace Example:</b> 'I notice I feel defensive when my ideas are challenged in meetings — "
     "I am going to pause and listen more carefully before responding.'"),
    ("2. SELF-REGULATION (Self-Management)", TEAL_M,
     "The ability to control disruptive emotions and impulses — to think before acting, "
     "to adapt to changing circumstances, and to maintain trustworthiness and integrity.<br/><br/>"
     "<b>Signs of High Self-Regulation:</b><br/>"
     "&#9654; Stay calm and composed under pressure<br/>"
     "&#9654; Respond thoughtfully rather than react impulsively<br/>"
     "&#9654; Manage stress without projecting it onto others<br/>"
     "&#9654; Are trustworthy and consistent in all situations<br/>"
     "&#9654; Adapt well to change<br/><br/>"
     "<b>Development:</b> Mindfulness practice, breathing techniques, reflective pause before responding.<br/>"
     "<b>Workplace Example:</b> After receiving harsh public criticism from a client, "
     "the professional thanks them for their feedback, privately processes the frustration, "
     "and responds constructively rather than defensively."),
    ("3. INTERNAL MOTIVATION", BLUE,
     "The drive to pursue goals with energy and persistence for INTERNAL reasons "
     "(interest, personal growth, satisfaction) rather than external incentives (money, status).<br/><br/>"
     "<b>Signs of High Internal Motivation:</b><br/>"
     "&#9654; Passionate and enthusiastic even without external rewards<br/>"
     "&#9654; Resilient in the face of failure — view setbacks as data<br/>"
     "&#9654; Optimistic and solution-focused<br/>"
     "&#9654; Committed to continuous improvement and learning<br/>"
     "&#9654; Raise performance standards proactively<br/><br/>"
     "<b>Development:</b> Connect work to personal values; set intrinsic goals; "
     "track progress; celebrate effort not just outcomes.<br/>"
     "<b>Workplace Example:</b> An employee continues improving a product feature "
     "beyond the minimum required because they genuinely care about the user experience."),
    ("4. EMPATHY", GREEN_M,
     "The ability to understand and sense the feelings, perspectives, and concerns of others — "
     "and to use that understanding to guide how you interact with them.<br/><br/>"
     "<b>Three Types of Empathy:</b><br/>"
     "&#9654; <b>Cognitive Empathy:</b> Understanding someone's perspective intellectually<br/>"
     "&#9654; <b>Emotional Empathy:</b> Feeling what another person feels<br/>"
     "&#9654; <b>Compassionate Empathy:</b> Understanding + feeling + taking action to help<br/><br/>"
     "<b>Signs of High Empathy:</b><br/>"
     "&#9654; Listen without immediately offering solutions or judgement<br/>"
     "&#9654; Pick up on unspoken emotional cues (non-verbal signals)<br/>"
     "&#9654; Understand diverse cultural perspectives<br/>"
     "&#9654; Create psychological safety for others to share honestly<br/><br/>"
     "<b>Workplace Example:</b> A manager notices a high-performing employee is unusually quiet "
     "and disconnected in meetings. Instead of assuming attitude issues, they schedule a 1:1, "
     "listen fully, and discover the employee is dealing with a family health crisis — "
     "then adjusts workload accordingly."),
    ("5. SOCIAL SKILLS", AMBER,
     "The ability to manage relationships, build networks, find common ground, "
     "resolve conflicts, and move people in desired directions through communication and leadership.<br/><br/>"
     "<b>Key Social Skills in EQ:</b><br/>"
     "&#9654; Building and maintaining professional relationships (networking)<br/>"
     "&#9654; Influencing and persuading without manipulation<br/>"
     "&#9654; Inspiring and leading team members<br/>"
     "&#9654; Managing conflict constructively<br/>"
     "&#9654; Clear, compelling communication<br/>"
     "&#9654; Team building and collaboration<br/>"
     "&#9654; Political awareness — reading organisational dynamics<br/><br/>"
     "<b>Workplace Example:</b> A project manager with high social skills navigates competing "
     "priorities between the engineering and sales teams by clearly communicating tradeoffs, "
     "acknowledging both teams' concerns, and building consensus around a phased delivery plan."),
]
for comp, color, desc in eq_components:
    hd = [[Paragraph(comp, S("EQH", fontSize=11, textColor=WHITE,
                             fontName="Helvetica-Bold", leading=14))]]
    ht = Table(hd, colWidths=[16.5*cm])
    ht.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), color),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
        ("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),12),
    ]))
    story.append(ht)
    story.append(Paragraph(desc, S("EQD", fontSize=10, textColor=BLACK, fontName="Helvetica",
                                   leading=14, alignment=TA_JUSTIFY,
                                   leftIndent=12, rightIndent=12, spaceBefore=5, spaceAfter=7)))
    story.append(sp(4))

story.append(Paragraph("3.3  EQ vs IQ vs CQ — Comparison:", sub2))
story.append(grid(
    ["Dimension","EQ (Emotional Intelligence)","IQ (Intelligence Quotient)","CQ (Cultural Intelligence)"],
    [
        ["Measures","Emotional & social skills","Cognitive & analytical ability","Cross-cultural effectiveness"],
        ["Fixed?","Highly developable","Relatively fixed after adulthood","Developable through exposure"],
        ["Predicts","Leadership success, teamwork","Academic success, technical role entry","Global/diverse team success"],
        ["Key theorist","Daniel Goleman","Alfred Binet","Christopher Earley & Soon Ang"],
        ["In workplace","Collaboration, conflict resolution","Technical problem-solving","International business, diverse teams"],
        ["Can it be learnt?","Yes — primary EQ skill","Partially (cognitive training)","Yes — through travel, exposure, study"],
    ],
    [3*cm, 4.5*cm, 4.5*cm, 5.5*cm]
))
story.append(sp(6))

story.append(Paragraph("3.4  EQ in the Workplace:", sub2))
eq_workplace = [
    "Higher EQ employees perform significantly better as leaders — Goleman found EQ accounts for "
    "67% of the abilities deemed most important for leader performance.",
    "EQ drives conflict resolution — high-EQ professionals de-escalate disputes, find win-wins, "
    "and maintain positive relationships post-conflict.",
    "EQ improves customer relationships — empathetic service professionals create more loyal customers.",
    "EQ enables change management — self-aware, regulated leaders help teams navigate uncertainty without panic.",
    "High-EQ teams have better psychological safety — members feel safe to contribute, disagree, and take risks.",
    "Low EQ is the #1 reason technically brilliant professionals fail in leadership roles.",
]
for e in eq_workplace:
    story.append(Paragraph(f"&#10003; {e}", bul))
story.append(sp(6))

story.append(Paragraph("3.5  Critical Thinking — Definition, Process & Barriers:", sub1))
story.append(Paragraph(
    "Critical thinking is the disciplined, intellectual process of actively and skilfully "
    "conceptualising, applying, analysing, synthesising, and evaluating information gathered "
    "from or generated by observation, experience, reflection, or reasoning — as a guide to "
    "belief and action. It is the opposite of accepting information passively and uncritically.", body))
story.append(sp(5))

story.append(Paragraph("The Critical Thinking Process:", sub2))
ct_process = [
    ("1. Identify the Problem/Question", "What exactly is being asked? What is the core issue? "
     "Poorly defined problems produce poor thinking."),
    ("2. Gather Information", "Collect relevant data, evidence, expert opinions, and perspectives. "
     "Apply the RAVEN test: Relevance, Authority, Viewpoint/Bias, Evidence, Newness."),
    ("3. Analyse and Evaluate", "Break the problem into components. Identify assumptions. "
     "Assess the quality of evidence. Look for logical fallacies."),
    ("4. Identify Multiple Perspectives", "Actively seek viewpoints that differ from your own. "
     "Consider: Who benefits from this position? Whose voice is missing?"),
    ("5. Draw Conclusions", "Based on evidence and reasoning, form a justified conclusion. "
     "Be prepared to state your confidence level — not all conclusions are certain."),
    ("6. Communicate & Apply", "Articulate your reasoning clearly. Apply conclusions to decisions. "
     "Be open to revising your conclusion when new evidence emerges."),
]
for t, d in ct_process:
    story.append(Paragraph(f"&#9654; <b>{t}:</b> {d}", bul))
    story.append(sp(2))
story.append(sp(5))

story.append(Paragraph("Common Barriers to Critical Thinking:", sub2))
barriers = [
    ("Cognitive Biases", "Confirmation bias (seeking info that confirms existing beliefs), "
     "availability heuristic, anchoring bias, survivorship bias."),
    ("Emotional Reasoning", "'I feel it's true, therefore it is true.' "
     "Emotions provide important data but cannot substitute for evidence."),
    ("Groupthink", "Desire for group harmony suppresses individual dissent and critical evaluation."),
    ("Overconfidence", "Assuming you understand something better than you do. "
     "The Dunning-Kruger effect: incompetent people tend to overestimate their competence."),
    ("False Dichotomy", "Presenting only two options when more exist: "
     "'You're either with us or against us.'"),
    ("Ad Hominem", "Attacking the person making an argument instead of the argument itself."),
    ("Appeal to Authority", "Accepting something as true simply because an authority said so, "
     "without evaluating the evidence."),
    ("Hasty Generalisation", "Drawing broad conclusions from insufficient data."),
]
for b, d in barriers:
    story.append(Paragraph(f"&#9888; <b>{b}:</b> {d}", bul))
    story.append(sp(2))
story.append(sp(5))
story.append(tip("EQ and Critical Thinking are COMPLEMENTARY. EQ gives you self-awareness to "
                 "recognise when emotions are biasing your thinking. Critical thinking gives "
                 "you the tools to evaluate information objectively. Together they create "
                 "the most effective professional thinker and decision-maker."))
story.append(sp(8))

story.append(q_hdr("PRACTICE QUESTIONS — TOPIC 3: EQ & Critical Thinking", PURPLE_M))
story.append(sp(6))
for item in q_box("1.5 MARKS", GREEN_M, "Define Emotional Intelligence according to Goleman.",
    "According to Daniel Goleman (1995), Emotional Intelligence (EQ) is 'the capacity for recognising "
    "our own feelings and those of others, for motivating ourselves, and for managing emotions well "
    "in ourselves and in our relationships.' It comprises five components: Self-Awareness, "
    "Self-Regulation, Internal Motivation, Empathy, and Social Skills."):
    story.append(item)
for item in q_box("10 MARKS (500-700 words)", AMBER,
    "Explain Goleman's model of Emotional Intelligence. How does EQ influence professional success?",
    "<b>Introduction:</b><br/>Emotional Intelligence (EQ) is the capacity to identify, understand, "
    "manage, and effectively use emotions in oneself and others. Peter Salovey and John Mayer coined "
    "the term in 1990; Daniel Goleman's 1995 book brought it to global prominence. "
    "Goleman argued that EQ matters more than IQ for professional and leadership success — "
    "it accounts for 67% of leadership performance according to his research.<br/><br/>"
    "<b>Goleman's 5 Components:</b><br/>"
    "<b>1. Self-Awareness:</b> Knowing your own emotions, strengths, limitations, values, and impact "
    "on others. Self-aware professionals seek feedback, recognise their triggers, and make better "
    "decisions by factoring in their emotional state.<br/>"
    "<b>2. Self-Regulation:</b> Controlling disruptive impulses and emotions. Thinking before acting. "
    "Self-regulated professionals stay composed under pressure, adapt to change smoothly, and are "
    "trusted for consistency and integrity.<br/>"
    "<b>3. Internal Motivation:</b> Pursuing goals for internal satisfaction rather than external reward. "
    "Highly motivated professionals are resilient, optimistic, and raise performance standards proactively. "
    "They stay committed when external motivators (salary, recognition) fluctuate.<br/>"
    "<b>4. Empathy:</b> Understanding others' emotional states and perspectives. Three types: "
    "Cognitive empathy (understanding), Emotional empathy (feeling with), and Compassionate empathy "
    "(understanding + acting). Empathetic leaders build loyal teams, resolve conflicts better, and "
    "create psychologically safe environments where innovation flourishes.<br/>"
    "<b>5. Social Skills:</b> Managing relationships, influencing, communicating, and collaborating "
    "effectively. Professionals with high social skills build large, diverse networks; resolve conflicts "
    "diplomatically; and inspire others toward shared goals.<br/><br/>"
    "<b>EQ and Professional Success:</b><br/>"
    "1. <b>Leadership:</b> EQ is the defining competency that differentiates average managers from "
    "exceptional leaders. Technically brilliant professionals without EQ consistently fail in "
    "leadership — they cannot inspire, empathise, or manage relationships.<br/>"
    "2. <b>Teamwork:</b> High-EQ professionals collaborate, share credit, resolve conflicts, and "
    "create psychological safety where team members contribute fearlessly.<br/>"
    "3. <b>Conflict Resolution:</b> EQ enables professionals to de-escalate disputes, find common "
    "ground, and maintain positive relationships after disagreements.<br/>"
    "4. <b>Customer Relations:</b> Empathy creates loyal customers. Emotionally intelligent service "
    "professionals read customer emotional states and respond in ways that build trust.<br/>"
    "5. <b>Change Management:</b> Self-regulated, internally motivated leaders help teams navigate "
    "organisational change without anxiety or resistance.<br/><br/>"
    "<b>Critical Thinking Connection:</b><br/>"
    "EQ and critical thinking are complementary. EQ provides self-awareness to recognise emotional "
    "biases in reasoning; critical thinking provides the framework to evaluate evidence objectively.<br/><br/>"
    "<b>Conclusion:</b><br/>"
    "Unlike IQ, which is largely fixed, EQ is highly developable through self-reflection, mindfulness, "
    "feedback, and practice. The most impactful professionals in any field continuously develop both "
    "their EQ and their critical thinking — these are the two intellectual superpowers of modern leadership."):
    story.append(item)
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# TOPIC 4 — APPLIED GRAMMAR
# ══════════════════════════════════════════════════════════════════════════════
story.append(banner("TOPIC 4: APPLIED GRAMMAR", SLATE))
story.append(sp(10))
story.append(sec_hdr("4","Applied Grammar","90%", SLATE))
story.append(sp(8))

story.append(Paragraph("4.1  Parts of Speech — Quick Reference:", sub1))
story.append(grid(
    ["Part of Speech","Definition","Example Words","Example Sentence"],
    [
        ["Noun","Person, place, thing, or idea","book, city, love, Priya","Priya loves this city."],
        ["Pronoun","Replaces a noun","he, she, it, they, we","She gave it to them."],
        ["Verb","Action or state of being","run, think, is, become","He runs every day."],
        ["Adjective","Describes a noun","beautiful, quick, three","The quick fox jumped."],
        ["Adverb","Describes verb/adjective/adverb","quickly, very, always","She runs very quickly."],
        ["Preposition","Shows relationship","in, on, at, between, with","The book is on the table."],
        ["Conjunction","Connects words/clauses","and, but, or, because, although","I studied, but I failed."],
        ["Interjection","Expresses emotion","Oh! Wow! Ouch! Hurray!","Wow! That was incredible!"],
        ["Article","Specifies nouns","a, an, the","A dog bit the man."],
    ],
    [2.5*cm, 3.5*cm, 3.5*cm, 7*cm]
))
story.append(sp(6))

story.append(Paragraph("4.2  All 12 Tenses — Complete Guide with Examples:", sub1))
story.append(sp(4))
tense_data = [
    ["SIMPLE TENSES", "", "", ""],
    ["Simple Present","Habitual/general truth","I work every day.","She works every day."],
    ["Simple Past","Completed action in past","I worked yesterday.","She worked yesterday."],
    ["Simple Future","Action in future","I will work tomorrow.","She will work tomorrow."],
    ["CONTINUOUS / PROGRESSIVE TENSES", "", "", ""],
    ["Present Continuous","Action happening right now","I am working now.","She is working now."],
    ["Past Continuous","Action in progress in past","I was working at 9 PM.","She was working then."],
    ["Future Continuous","Action in progress at future time","I will be working at noon.","She will be working then."],
    ["PERFECT TENSES", "", "", ""],
    ["Present Perfect","Past action with present relevance","I have worked here 3 years.","She has worked here."],
    ["Past Perfect","Action completed before another past action","I had worked before she arrived.","She had worked."],
    ["Future Perfect","Action completed before a future point","I will have worked 5 years by May.","She will have worked."],
    ["PERFECT CONTINUOUS TENSES", "", "", ""],
    ["Present Perf. Continuous","Ongoing action from past to now","I have been working since 8 AM.","She has been working."],
    ["Past Perf. Continuous","Ongoing action before a past point","I had been working for 2 hrs.","She had been working."],
    ["Future Perf. Continuous","Ongoing action up to a future time","I will have been working 10 yrs.","She will have been working."],
]
section_rows = {0, 3, 6, 9}
tense_style = [
    ("BOX",(0,0),(-1,-1),1, BLUE),("INNERGRID",(0,0),(-1,-1),0.4, SKY),
    ("FONTNAME",(0,0),(-1,-1),"Helvetica"),("FONTSIZE",(0,0),(-1,-1),9.5),
    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
]
for i in section_rows:
    tense_style.append(("BACKGROUND",(0,i),(-1,i), NAVY))
    tense_style.append(("FONTNAME",(0,i),(-1,i),"Helvetica-Bold"))
    tense_style.append(("FONTCOLOR",(0,i),(-1,i), WHITE))
    tense_style.append(("SPAN",(0,i),(-1,i)))
for i in range(len(tense_data)):
    if i not in section_rows:
        if i % 2 == 0:
            tense_style.append(("BACKGROUND",(0,i),(-1,i), BLUE_L))
        else:
            tense_style.append(("BACKGROUND",(0,i),(-1,i), WHITE))
        tense_style.append(("FONTNAME",(0,i),(0,i),"Helvetica-Bold"))
tense_t = Table(tense_data, colWidths=[4.5*cm, 4*cm, 4.5*cm, 3.5*cm])
tense_t.setStyle(TableStyle(tense_style))
story.append(tense_t)
story.append(sp(8))

story.append(Paragraph("4.3  Active vs Passive Voice:", sub1))
story.append(Paragraph(
    "<b>Active Voice:</b> Subject performs the action. Direct, clear, strong.<br/>"
    "<b>Passive Voice:</b> Subject receives the action. Indirect, formal, sometimes necessary.", body))
story.append(sp(4))

apv_data = [
    [Paragraph("<b>Tense</b>", S("TH", fontSize=10, fontName="Helvetica-Bold", textColor=WHITE,
                                  alignment=TA_CENTER, leading=13)),
     Paragraph("<b>Active Voice</b>", S("TH", fontSize=10, fontName="Helvetica-Bold", textColor=WHITE,
                                         alignment=TA_CENTER, leading=13)),
     Paragraph("<b>Passive Voice</b>", S("TH", fontSize=10, fontName="Helvetica-Bold", textColor=WHITE,
                                          alignment=TA_CENTER, leading=13))],
    ["Simple Present", "She writes the report.", "The report is written by her."],
    ["Simple Past", "She wrote the report.", "The report was written by her."],
    ["Simple Future", "She will write the report.", "The report will be written by her."],
    ["Present Continuous", "She is writing the report.", "The report is being written by her."],
    ["Past Continuous", "She was writing the report.", "The report was being written by her."],
    ["Present Perfect", "She has written the report.", "The report has been written by her."],
    ["Past Perfect", "She had written the report.", "The report had been written by her."],
    ["Future Perfect", "She will have written the report.", "The report will have been written by her."],
]
apvt = Table(apv_data, colWidths=[4*cm, 6.25*cm, 6.25*cm])
apvt.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0), DARK),
    ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, BLUE_L]),
    ("BOX",(0,0),(-1,-1),1, BLUE),("INNERGRID",(0,0),(-1,-1),0.4, SKY),
    ("FONTNAME",(0,1),(-1,-1),"Helvetica"),("FONTSIZE",(0,0),(-1,-1),9.5),
    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
]))
story.append(apvt)
story.append(sp(5))
story.append(tip("Business writing prefers ACTIVE voice (direct, clear, shorter). "
                 "Use passive when: the actor is unknown ('The files were deleted.'), "
                 "when the action is more important than the actor, or in formal/scientific reports."))
story.append(sp(6))

story.append(Paragraph("4.4  Subject-Verb Agreement — Rules with Examples:", sub1))
sva_rules = [
    ("Rule 1: Singular subject = singular verb",
     "WRONG: 'The team are playing well.'",
     "CORRECT: 'The team is playing well.'",
     "Collective nouns (team, jury, committee) take singular verbs in American English."),
    ("Rule 2: Plural subject = plural verb",
     "WRONG: 'The children was excited.'",
     "CORRECT: 'The children were excited.'",
     "Plural subjects always take plural verbs."),
    ("Rule 3: Compound subjects with 'and' = plural",
     "WRONG: 'Rahul and Priya is coming.'",
     "CORRECT: 'Rahul and Priya are coming.'",
     "Two subjects joined by 'and' form a compound plural subject."),
    ("Rule 4: 'Or' / 'Nor' — verb agrees with nearer subject",
     "WRONG: 'Neither the manager nor the employees was informed.'",
     "CORRECT: 'Neither the manager nor the employees were informed.'",
     "With 'or/nor', the verb agrees with the subject closest to it."),
    ("Rule 5: Indefinite pronouns — mostly singular",
     "WRONG: 'Everyone have submitted their assignments.'",
     "CORRECT: 'Everyone has submitted their assignment.'",
     "Each, every, everyone, somebody, nobody, anyone, no one = singular verbs."),
    ("Rule 6: Titles and proper nouns = singular",
     "WRONG: 'The United States are a large country.'",
     "CORRECT: 'The United States is a large country.'",
     "Names of countries, organisations, and book/film titles take singular verbs."),
    ("Rule 7: 'A number of' = plural; 'The number of' = singular",
     "WRONG: 'A number of students was absent.'",
     "CORRECT: 'A number of students were absent.'",
     "'A number of' implies 'many' (plural). 'The number of' refers to a single count (singular)."),
    ("Rule 8: Relative pronouns — verb agrees with antecedent",
     "WRONG: 'She is one of the employees who works overtime.'",
     "CORRECT: 'She is one of the employees who work overtime.'",
     "The verb in the relative clause agrees with the noun the relative pronoun refers to (employees, not 'one')."),
]
for rule, wrong, correct, explanation in sva_rules:
    story.append(Paragraph(f"<b>{rule}</b>", sub3))
    story.append(correct_wrong(wrong.replace("WRONG: ",""), correct.replace("CORRECT: ",""), explanation))
    story.append(sp(4))

story.append(Paragraph("4.5  Articles — A / An / The:", sub2))
story.append(grid(
    ["Article","When to Use","Examples","Common Errors"],
    [
        ["A","Before consonant sounds; indefinite singular","a book, a university, a one-way street",
         "'a apple' (wrong — use 'an apple')"],
        ["An","Before vowel sounds; indefinite singular","an apple, an hour, an MBA, an heir",
         "'an university' (wrong — 'u' sounds like 'yoo' = consonant sound)"],
        ["The","Definite; specific; previously mentioned; unique","the sun, the President, the book I gave you",
         "'the India' (wrong for country names usually)"],
        ["No article","Plural/uncountable in general; proper nouns; abstract nouns in general","Dogs are loyal. Love is powerful. India is vast.",
         "'The love is...' when speaking generally"],
    ],
    [1.5*cm, 4.5*cm, 5*cm, 5.5*cm]
))
story.append(sp(6))

story.append(Paragraph("4.6  Prepositions — Common Rules & Errors:", sub2))
prep_rules = [
    ("In / On / At — Time",
     "IN: months, years, seasons, centuries (in May, in 2025, in winter)<br/>"
     "ON: days, dates (on Monday, on 5th June)<br/>"
     "AT: specific times, festivals (at 9 AM, at noon, at Diwali)"),
    ("In / On / At — Place",
     "IN: enclosed spaces, countries, cities (in the room, in India, in Delhi)<br/>"
     "ON: surfaces, floors, streets (on the table, on the 3rd floor, on MG Road)<br/>"
     "AT: specific points, addresses (at the bus stop, at No. 12 Park Street)"),
    ("Common Preposition Errors",
     "WRONG: 'Married with' → CORRECT: 'Married to'<br/>"
     "WRONG: 'Discuss about' → CORRECT: 'Discuss' (no preposition needed)<br/>"
     "WRONG: 'Cope up with' → CORRECT: 'Cope with'<br/>"
     "WRONG: 'Reach to Mumbai' → CORRECT: 'Reach Mumbai'<br/>"
     "WRONG: 'Return back' → CORRECT: 'Return'<br/>"
     "WRONG: 'Since 2 hours' → CORRECT: 'For 2 hours'"),
]
for t, d in prep_rules:
    story.append(Paragraph(f"<b>{t}:</b>", sub3))
    story.append(Paragraph(d, body))
    story.append(sp(3))
story.append(sp(6))

story.append(Paragraph("4.7  Punctuation Rules — The Essential Set:", sub2))
punct_rules = [
    ("FULL STOP ( . )", "Ends a declarative or imperative sentence. 'She left at noon.'"),
    ("COMMA ( , )", "Separates list items; after introductory phrases; before conjunctions in compound sentences. "
     "'I bought milk, bread, and eggs.' | 'After the meeting, she left.' | 'I was tired, but I stayed.'"),
    ("SEMICOLON ( ; )", "Connects closely related independent clauses; separates complex list items. "
     "'She worked hard; she deserved the promotion.'"),
    ("COLON ( : )", "Introduces a list, explanation, or quotation. "
     "'Three things are needed: patience, practice, and persistence.'"),
    ("APOSTROPHE ( ' )", "Possession: 'Priya's book.' Contraction: 'It's (it is) raining.' "
     "COMMON ERROR: 'its' (possessive) vs 'it's' (it is). 'The dog hurt its paw.' NOT 'it's paw.'"),
    ("QUOTATION MARKS ( '' )", "Enclose direct speech and titles of short works. "
     "'She said, \"I will attend the meeting.\"'"),
    ("QUESTION MARK ( ? )", "Ends a direct question. 'Are you coming?' "
     "NOT used after indirect questions: 'She asked whether I was coming.'"),
    ("EXCLAMATION MARK ( ! )", "Expresses strong emotion. Use sparingly in professional writing. "
     "'What a brilliant idea!' Overuse reduces impact and sounds unprofessional."),
    ("HYPHEN ( - )", "Joins compound modifiers before nouns: 'well-known author', 'five-year plan'. "
     "Joins compound nouns: 'mother-in-law'. Joins prefixes: 'self-aware', 'co-worker'."),
    ("DASH ( — )", "Sets off emphatic statements or additional information — like this — within a sentence."),
]
for p, d in punct_rules:
    story.append(Paragraph(f"<b>{p}:</b> {d}", bul))
    story.append(sp(2))
story.append(sp(6))

story.append(Paragraph("4.8  50 Common Grammar Errors — Corrections & Rules:", sub1))
story.append(sp(4))

grammar_errors = [
    # (wrong, correct, rule)
    ("I am knowing the answer.", "I know the answer.",
     "Stative verbs (know, believe, love, understand, see, hear) do not use continuous tense."),
    ("She has went to the market.", "She has gone to the market.",
     "Present Perfect uses past participle (gone), not simple past (went)."),
    ("He gave me an useful advice.", "He gave me useful advice.",
     "'Advice' is uncountable — no article 'an'. 'An' is used before vowel sounds; 'useful' starts with 'yoo' sound."),
    ("I am having a car.", "I have a car.",
     "Possession verbs (have, own) do not take continuous form."),
    ("He is more taller than her.", "He is taller than her.",
     "Never use 'more' with comparative adjectives that already end in '-er'."),
    ("She did not came yesterday.", "She did not come yesterday.",
     "After auxiliaries (did, does, do, will, etc.), use the base form of the verb, not past tense."),
    ("The informations are useful.", "The information is useful.",
     "'Information' is an uncountable noun — no plural form; takes singular verb."),
    ("I have seen him since three days.", "I have seen him for three days. / I have not seen him for three days.",
     "'Since' is used with a specific point in time (since Monday). 'For' is used with a period of time (for three days)."),
    ("She is my cousin sister.", "She is my cousin.",
     "'Cousin' already implies a sibling relationship within the family — 'sister' is redundant."),
    ("He passed out from college in 2022.", "He graduated from college in 2022.",
     "'Pass out' means to faint/lose consciousness. Use 'graduate' for completing education."),
    ("I am agree with you.", "I agree with you.",
     "'Agree' is not an adjective — do not use 'am/is/are' with it."),
    ("She is a 5-foot tall girl.", "She is a 5-foot-tall girl.", "Use hyphens in compound modifiers before nouns."),
    ("Can I borrow you a pen?", "Can you lend me a pen? / Can I borrow a pen from you?",
     "'Borrow' = take temporarily. 'Lend' = give temporarily. They are not interchangeable."),
    ("I am fed up from this job.", "I am fed up with this job.",
     "The correct collocation is 'fed up with', not 'fed up from'."),
    ("Inspite of raining, she went.", "Despite the rain, she went. / In spite of the rain, she went.",
     "'In spite of' is three separate words. 'Despite' does not take 'of'. Both are followed by a noun/gerund."),
    ("He is a coward man.", "He is a cowardly man. / He is a coward.",
     "'Coward' is a noun, not an adjective. Use 'cowardly' as the adjective form."),
    ("I look forward to meet you.", "I look forward to meeting you.",
     "After 'look forward to', use a gerund (-ing form), not infinitive (to + base verb)."),
    ("She knows to swim.", "She knows how to swim.",
     "'Know' is followed by 'how to' before an infinitive."),
    ("The police has arrested the thief.", "The police have arrested the thief.",
     "'Police' is always plural — takes plural verb."),
    ("Either of the boys are responsible.", "Either of the boys is responsible.",
     "'Either' and 'neither' as subjects take singular verbs."),
]
story.append(Paragraph("<b>FORMAT: ✗ Wrong → ✓ Correct | Rule Explained</b>",
                       S("GEH", fontSize=11, textColor=DARK, fontName="Helvetica-Bold",
                         leading=14, spaceBefore=4, spaceAfter=6)))
for wrong, correct, rule in grammar_errors:
    story.append(correct_wrong(wrong, correct, rule))
    story.append(sp(3))

story.append(sp(6))
story.append(Paragraph("4.9  Conjunctions — Types and Usage:", sub2))
conj_data = [
    ["Coordinating", "FANBOYS: For, And, Nor, But, Or, Yet, So",
     "I was tired, but I kept working."],
    ["Subordinating", "because, although, since, unless, when, while, after, before, if, though",
     "Although she studied hard, she failed."],
    ["Correlative", "either...or, neither...nor, both...and, not only...but also, whether...or",
     "Not only did she win, but she also broke the record."],
]
story.append(grid(
    ["Type","Key Words","Example"],
    conj_data,
    [3*cm, 7*cm, 6.5*cm]
))
story.append(sp(8))

story.append(q_hdr("PRACTICE QUESTIONS — TOPIC 4: Applied Grammar", SLATE))
story.append(sp(6))
for item in q_box("1.5 MARKS", GREEN_M, "What is the difference between 'since' and 'for' in English grammar?",
    "'Since' is used to indicate a specific point of time from which something began: "
    "'I have worked here since 2022.' (since + point in time) "
    "'For' is used to indicate a duration/period of time: "
    "'I have worked here for 3 years.' (for + duration) "
    "Both are used with Perfect tenses to describe ongoing situations."):
    story.append(item)
for item in q_box("5 MARKS (300-500 words)", BLUE,
    "Explain Subject-Verb Agreement rules with examples.",
    "<b>Introduction:</b> Subject-Verb Agreement (SVA) is the grammatical rule that the verb in a sentence "
    "must agree with its subject in number (singular/plural) and person (first/second/third). "
    "Errors in SVA are among the most common in written and spoken English.<br/><br/>"
    "<b>Key Rules:</b><br/>"
    "1. <b>Singular subject → Singular verb:</b> 'The report is ready.' NOT 'The report are ready.'<br/>"
    "2. <b>Plural subject → Plural verb:</b> 'The students are present.' NOT 'The students is present.'<br/>"
    "3. <b>Compound subject with 'and' → Plural:</b> 'Ravi and Priya are here.' (two separate subjects)<br/>"
    "4. <b>'Or/Nor' → Verb agrees with nearer subject:</b> 'Neither the teacher nor the students were present.' "
    "(students = plural → were)<br/>"
    "5. <b>Collective nouns → Singular (AmE):</b> 'The committee has decided.' 'The team is ready.'<br/>"
    "6. <b>Indefinite pronouns → Singular:</b> 'Everyone has submitted.' 'Nobody knows.'<br/>"
    "7. <b>'A number of' → Plural; 'The number of' → Singular:</b> "
    "'A number of students were absent.' vs 'The number of students is increasing.'<br/>"
    "8. <b>Relative pronouns → Agree with antecedent:</b> 'She is one of those leaders who inspire (not inspires) others.'<br/>"
    "9. <b>Titles/proper nouns → Singular:</b> 'The United States is...' 'Mathematics is my favourite subject.'<br/>"
    "10. <b>Uncountable nouns → Singular:</b> 'Information is...' 'Advice is...' 'News is...'<br/><br/>"
    "<b>Conclusion:</b> SVA errors signal poor grammatical control, especially in formal writing. "
    "Mastering these rules significantly improves résumé, report, and email writing quality."):
    story.append(item)
for item in q_box("10 MARKS (500-700 words)", AMBER,
    "Write a detailed note on Applied Grammar. Include: Tenses, Active/Passive Voice, Subject-Verb Agreement, and Common Errors.",
    "<b>Introduction:</b><br/>Applied Grammar refers to the practical use of grammatical rules in real "
    "communication — writing, speaking, and professional documentation. Mastery of applied grammar is "
    "essential for effective résumés, formal reports, business letters, and all professional communication.<br/><br/>"
    "<b>1. TENSES:</b><br/>English has 12 tenses across 4 groups: Simple (Present/Past/Future), "
    "Continuous (Present/Past/Future), Perfect (Present/Past/Future), and Perfect Continuous.<br/>"
    "Key uses: Simple Present for habits/facts ('She writes reports daily'). Simple Past for completed "
    "actions ('She submitted the report'). Present Perfect for past actions with present relevance "
    "('She has submitted the report'). Past Perfect for actions completed before another past action "
    "('She had submitted it before the deadline passed').<br/><br/>"
    "<b>2. ACTIVE VS PASSIVE VOICE:</b><br/>"
    "Active: 'The team completed the project.' (Subject does the action — direct, clear, strong)<br/>"
    "Passive: 'The project was completed by the team.' (Subject receives action — formal, indirect)<br/>"
    "Formula: Passive = Object + to be (conjugated) + Past Participle + by + Agent (optional)<br/>"
    "Use active for business writing. Use passive when actor is unknown, unimportant, or when "
    "formality requires it.<br/><br/>"
    "<b>3. SUBJECT-VERB AGREEMENT:</b><br/>"
    "Core rule: Singular subject = singular verb; Plural subject = plural verb.<br/>"
    "Tricky cases: Compound subjects with 'and' = plural. With 'or/nor' = agrees with nearer subject. "
    "Collective nouns = singular (AmE). Indefinite pronouns (everyone, anyone, nobody) = singular. "
    "Uncountable nouns (information, advice, news) = singular always.<br/><br/>"
    "<b>4. ARTICLES (a/an/the):</b><br/>"
    "'A' before consonant sounds; 'An' before vowel sounds; 'The' for specific/unique references. "
    "No article for general plurals/uncountables/proper nouns.<br/>"
    "Error: 'She is an useful employee.' → Correct: 'She is a useful employee.' ('useful' = 'yoo' = consonant sound)<br/><br/>"
    "<b>5. PREPOSITIONS:</b><br/>"
    "Time: In (months/years), On (days/dates), At (specific times/points).<br/>"
    "Common errors: 'Discuss about' → 'Discuss'; 'Married with' → 'Married to'; "
    "'Reach to Mumbai' → 'Reach Mumbai'; 'Since 2 hours' → 'For 2 hours'<br/><br/>"
    "<b>6. COMMON GRAMMAR ERRORS:</b><br/>"
    "'I am knowing' → 'I know' (stative verbs). 'More taller' → 'Taller'. "
    "'Did not came' → 'Did not come' (base form after auxiliary). "
    "'Informations' → 'Information' (uncountable). 'I am agree' → 'I agree'.<br/><br/>"
    "<b>7. PUNCTUATION:</b><br/>"
    "Comma: list items, introductory phrases, before conjunctions in compound sentences. "
    "Apostrophe: 'it's' = it is; 'its' = possessive. Semicolon: connects related independent clauses. "
    "Colon: introduces list/explanation. Hyphen: compound modifiers ('well-known author').<br/><br/>"
    "<b>Conclusion:</b><br/>"
    "Applied grammar is the foundation of professional credibility. In résumés, one grammatical error "
    "signals carelessness. In business reports, incorrect tense usage confuses timelines. "
    "In interviews, poor grammar undermines the impression of education and communication competence. "
    "Regular reading, writing practice, and deliberate error-correction build grammatical mastery over time."):
    story.append(item)
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# QUICK REVISION SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
story.append(banner("&#9733;  WEEK 12 — QUICK REVISION MASTER TABLE  &#9733;", DARK))
story.append(sp(10))

rev = [
    [Paragraph("<b>Topic</b>", S("TH_W", fontSize=9.5, fontName="Helvetica-Bold",
                                  textColor=WHITE, alignment=TA_CENTER, leading=13)),
     Paragraph("<b>Key Formulas / Must-Know Points</b>",
               S("TH_W2", fontSize=9.5, fontName="Helvetica-Bold",
                 textColor=WHITE, alignment=TA_CENTER, leading=13)),
     Paragraph("<b>%</b>", S("TH_W3", fontSize=9.5, fontName="Helvetica-Bold",
                               textColor=WHITE, alignment=TA_CENTER, leading=13))],
    ["Résumé vs CV","Résumé: 1-2 pg, targeted. CV: comprehensive, academic/government","90%"],
    ["Résumé Formats","Chronological (best) · Functional (gaps/change) · Combination · Targeted (most effective)","88%"],
    ["Résumé Components","9 parts: Header→Summary→Experience→Education→Skills→Projects→Certs→Extra→Refs","95%"],
    ["Résumé Golden Rules","Achieve not describe · Quantify · Action verbs · ATS keywords · 1-2 pages · Zero errors","95%"],
    ["Action Verbs","Led·Grew·Built·Reduced·Launched·Generated·Optimised·Delivered·Spearheaded·Mentored","90%"],
    ["Interview Phases","Before: Research+STAR prep · During: Listen+STAR+confident · After: Thank-you+debrief","92%"],
    ["STAR Method","S=Situation (brief) T=Task (YOUR role) A=Action (YOUR steps) R=Result (numbers!)","95%"],
    ["Interview Types","Structured·Unstructured·Panel·Group·Behavioural·Stress·Technical·Case·Video","88%"],
    ["Body Language","Firm handshake·Eye contact 3-5s·Upright posture·Open hands·Moderate pace","85%"],
    ["Interview Don'ts","Criticise past employers·Ask salary first·Arrive late·Vague answers·No research","90%"],
    ["EQ Definition","Goleman: Recognise+manage own emotions+understand others' emotions to build relationships","88%"],
    ["EQ 5 Components","Self-Awareness→Self-Regulation→Internal Motivation→Empathy→Social Skills","95%"],
    ["Critical Thinking","Identify→Gather→Analyse→Multiple perspectives→Conclude→Apply+Communicate","85%"],
    ["CT Barriers","Confirmation bias·Emotional reasoning·Groupthink·Overconfidence·Hasty generalisation","82%"],
    ["Tenses","12 tenses: Simple(3)+Continuous(3)+Perfect(3)+PerfContinuous(3). Know all with examples","90%"],
    ["Active vs Passive","Active: Subject does action (preferred). Passive: Subject receives action (formal)","90%"],
    ["SVA Rules","Singular=singular verb · Compound+and=plural · Or/nor=nearer subject · Everyone=singular","88%"],
    ["Articles","A=consonant sound · An=vowel sound · The=specific/unique · No article=general","85%"],
    ["Prepositions","In(months/years) On(days) At(time/point) · Common errors: discuss about→discuss","85%"],
    ["Common Errors","'I am knowing'→I know · 'More taller'→taller · 'Did not came'→did not come","90%"],
]
rev_t = Table(rev, colWidths=[4*cm, 10.5*cm, 2*cm])
rev_t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0), DARK),
    ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, BLUE_L]),
    ("BOX",(0,0),(-1,-1),1.5, BLUE),("INNERGRID",(0,0),(-1,-1),0.4, SKY),
    ("FONTNAME",(0,1),(-1,-1),"Helvetica"),("FONTSIZE",(0,0),(-1,-1),8.5),
    ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("ALIGN",(2,0),(2,-1),"CENTER"),
]))
story.append(rev_t)
story.append(sp(12))

closing = [[Paragraph(
    "<b>FINAL EXAM STRATEGY — WEEK 12 &#9733;</b><br/>"
    "&#9654; <b>Résumé:</b> Write ALL 9 components with examples. Use a fresh graduate sample if asked to write one. "
    "Mention ATS. Distinguish Résumé from CV.<br/>"
    "&#9654; <b>Interviews:</b> STAR method with a full worked example. Classify 10+ types. Write Dos/Don'ts as a table.<br/>"
    "&#9654; <b>EQ:</b> Name all 5 Goleman components with workplace examples. Compare EQ vs IQ vs CQ.<br/>"
    "&#9654; <b>Grammar:</b> Know all 12 tenses. Active-passive conversion table. SVA rules. 20+ error corrections. "
    "In/On/At rules. Articles.<br/>"
    "&#9654; <b>Max Marks Tip:</b> 15-mark grammar questions often ask to 'correct the sentences' — "
    "practise identifying the rule behind each error, not just guessing the correct form.",
    S("CLO_W", fontSize=10.5, textColor=DARK, fontName="Helvetica",
      alignment=TA_LEFT, leading=17))]]
ct_final = Table(closing, colWidths=[17*cm])
ct_final.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1), GOLD_L),("BOX",(0,0),(-1,-1),2, GOLD),
    ("TOPPADDING",(0,0),(-1,-1),14),("BOTTOMPADDING",(0,0),(-1,-1),14),
    ("LEFTPADDING",(0,0),(-1,-1),16),("RIGHTPADDING",(0,0),(-1,-1),16),
]))
story.append(ct_final)
story.append(sp(10))

final = [[Paragraph(
    "&#9733; ALL THE VERY BEST! YOU NOW HAVE EVERYTHING YOU NEED TO ACE OEC-CS-601(I) &#9733;",
    S("FW", fontSize=13, textColor=WHITE, fontName="Helvetica-Bold",
      alignment=TA_CENTER, leading=20))]]
ft = Table(final, colWidths=[17*cm])
ft.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1), DARK),
    ("TOPPADDING",(0,0),(-1,-1),16),("BOTTOMPADDING",(0,0),(-1,-1),16),
    ("LEFTPADDING",(0,0),(-1,-1),16),("RIGHTPADDING",(0,0),(-1,-1),16),
]))
story.append(ft)

# BUILD
doc = SimpleDocTemplate(
    OUTPUT_PATH, pagesize=A4,
    leftMargin=1.8*cm, rightMargin=1.8*cm,
    topMargin=2*cm, bottomMargin=2.2*cm,
    title="Week 12 — Résumé, Interviews, EI & Grammar",
    author="OEC-CS-601(I)",
)
doc.build(story, canvasmaker=NC)
print(f"PDF created: {OUTPUT_PATH}")