from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas as pdfcanvas

OUTPUT_PATH = "Module4_Presentation_Interview_Notes.pdf"

# ── COLORS ─────────────────────────────────────────────────────────────────────
DARK_NAVY    = colors.HexColor("#0d1b2a")
ROYAL_BLUE   = colors.HexColor("#1565c0")
LIGHT_BLUE   = colors.HexColor("#e3f2fd")
SKY          = colors.HexColor("#bbdefb")
CRIMSON      = colors.HexColor("#b71c1c")
CRIMSON_L    = colors.HexColor("#ffebee")
EMERALD      = colors.HexColor("#1b5e20")
EMERALD_L    = colors.HexColor("#e8f5e9")
EMERALD_M    = colors.HexColor("#2e7d32")
AMBER        = colors.HexColor("#e65100")
AMBER_L      = colors.HexColor("#fff3e0")
PURPLE       = colors.HexColor("#4a148c")
PURPLE_L     = colors.HexColor("#f3e5f5")
TEAL         = colors.HexColor("#004d40")
TEAL_L       = colors.HexColor("#e0f2f1")
TEAL_M       = colors.HexColor("#00695c")
INDIGO       = colors.HexColor("#1a237e")
INDIGO_L     = colors.HexColor("#e8eaf6")
GOLD         = colors.HexColor("#f57f17")
GOLD_L       = colors.HexColor("#fffde7")
BROWN        = colors.HexColor("#4e342e")
GRAY_M       = colors.HexColor("#757575")
GRAY_L       = colors.HexColor("#f5f5f5")
YELLOW_HL    = colors.HexColor("#fff9c4")
WHITE        = colors.white
BLACK        = colors.black
MAROON       = colors.HexColor("#880e4f")
MAROON_L     = colors.HexColor("#fce4ec")
DEEP_TEAL    = colors.HexColor("#006064")
DEEP_TEAL_L  = colors.HexColor("#e0f7fa")

def S(name, **kw):
    return ParagraphStyle(name, **kw)

body  = S("B4",  fontSize=10, textColor=BLACK, fontName="Helvetica",
          leading=15, spaceBefore=3, spaceAfter=3, alignment=TA_JUSTIFY)
sub1  = S("S1_4", fontSize=12, textColor=ROYAL_BLUE, fontName="Helvetica-Bold",
          leading=16, spaceBefore=10, spaceAfter=3)
sub2  = S("S2_4", fontSize=11, textColor=TEAL_M, fontName="Helvetica-Bold",
          leading=14, spaceBefore=7, spaceAfter=2)
sub3  = S("S3_4", fontSize=10.5, textColor=INDIGO, fontName="Helvetica-Bold",
          leading=13, spaceBefore=5, spaceAfter=2)
bul   = S("BU4",  fontSize=10, textColor=BLACK, fontName="Helvetica",
          leading=14, spaceBefore=2, spaceAfter=2, leftIndent=16, firstLineIndent=-10)
note  = S("NT4",  fontSize=9.5, textColor=PURPLE, fontName="Helvetica-Oblique",
          leading=13, spaceBefore=1, spaceAfter=1)
toc_i = S("TC4",  fontSize=10.5, textColor=ROYAL_BLUE, fontName="Helvetica",
          leading=16, leftIndent=10)
cv_mono = S("CVM", fontSize=9.5, textColor=BLACK, fontName="Courier",
             leading=14, spaceBefore=1, spaceAfter=1)

def sp(n=6):  return Spacer(1, n)
def hr():     return HRFlowable(width="100%", thickness=1,
                                color=LIGHT_BLUE, spaceAfter=4, spaceBefore=4)
def hr2():    return HRFlowable(width="100%", thickness=2,
                                color=AMBER, spaceAfter=6, spaceBefore=6)

def ch_banner(text, bg=DARK_NAVY):
    d = [[Paragraph(text, S("CB4", fontSize=16, textColor=WHITE,
                            fontName="Helvetica-Bold", alignment=TA_LEFT, leading=22))]]
    t = Table(d, colWidths=[17*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), bg),
        ("TOPPADDING",(0,0),(-1,-1),11),("BOTTOMPADDING",(0,0),(-1,-1),11),
        ("LEFTPADDING",(0,0),(-1,-1),14),("RIGHTPADDING",(0,0),(-1,-1),14),
    ]))
    return t

def prob_badge(pct, color=AMBER):
    d = [[Paragraph(f"<b>Exam Probability: {pct}</b>",
                    S("PB4", fontSize=10, textColor=WHITE,
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
                    S("SH4", fontSize=13, textColor=DARK_NAVY,
                      fontName="Helvetica-Bold", leading=18)),
          prob_badge(pct, pc)]]
    t = Table(d, colWidths=[11.8*cm, 5.2*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), LIGHT_BLUE),
        ("BOX",(0,0),(-1,-1),1.5, ROYAL_BLUE),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
        ("LEFTPADDING",(0,0),(0,0),10),("RIGHTPADDING",(0,1),(-1,-1),6),
    ]))
    return t

def info_box(title, content, bg=LIGHT_BLUE, tc=DARK_NAVY, bc=ROYAL_BLUE):
    d = [
        [Paragraph(f"<b>{title}</b>",
                   S("IB_T4", fontSize=11, textColor=tc,
                     fontName="Helvetica-Bold", leading=14))],
        [Paragraph(content,
                   S("IB_B4", fontSize=10, textColor=BLACK,
                     fontName="Helvetica", leading=14, alignment=TA_JUSTIFY))],
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

def tip_box(text, bg=PURPLE_L, border=PURPLE, tc=PURPLE):
    d = [[Paragraph(f"<b>&#9733; KEY POINT:</b> {text}",
                    S("TIP4", fontSize=10, textColor=tc,
                      fontName="Helvetica", leading=14, alignment=TA_JUSTIFY))]]
    t = Table(d, colWidths=[16.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), bg),
        ("BOX",(0,0),(-1,-1),1.5, border),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
    ]))
    return t

def warn_box(text):
    d = [[Paragraph(f"<b>&#9888; EXAM NOTE:</b> {text}",
                    S("WB4", fontSize=10, textColor=CRIMSON,
                      fontName="Helvetica", leading=14, alignment=TA_JUSTIFY))]]
    t = Table(d, colWidths=[16.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), CRIMSON_L),
        ("BOX",(0,0),(-1,-1),1.5, CRIMSON),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
    ]))
    return t

def q_box(label, color, q, a):
    hdr = [[Paragraph(label, S("QH4", fontSize=10, textColor=WHITE,
                               fontName="Helvetica-Bold", leading=13,
                               alignment=TA_CENTER))]]
    ht  = Table(hdr, colWidths=[16.5*cm])
    ht.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), color),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
    ]))
    qt = Paragraph(f"<b>Q:</b> {q}",
                   S("QT4", fontSize=10, textColor=DARK_NAVY,
                     fontName="Helvetica-Bold", leading=14,
                     alignment=TA_JUSTIFY, leftIndent=8, rightIndent=8, spaceBefore=4))
    at = Paragraph(f"<b>Ans:</b> {a}",
                   S("AT4", fontSize=10, textColor=BLACK,
                     fontName="Helvetica", leading=15,
                     alignment=TA_JUSTIFY, leftIndent=8, rightIndent=8,
                     spaceBefore=3, spaceAfter=6))
    return [ht, qt, at, sp(8)]

def q_sec_hdr(title, color):
    d = [[Paragraph(title, S("QSH4", fontSize=11, textColor=WHITE,
                             fontName="Helvetica-Bold",
                             alignment=TA_CENTER, leading=15))]]
    t = Table(d, colWidths=[17*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), color),
        ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),
    ]))
    return t

def grid_table(headers, rows, widths=None, hdr_color=DARK_NAVY):
    if widths is None:
        widths = [16.5*cm/len(headers)]*len(headers)
    hrow = [Paragraph(f"<b>{h}</b>",
                      S("GTH", fontSize=10, fontName="Helvetica-Bold",
                        textColor=WHITE, alignment=TA_CENTER, leading=13))
            for h in headers]
    data = [hrow]+rows
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0), hdr_color),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LIGHT_BLUE]),
        ("BOX",(0,0),(-1,-1),1, ROYAL_BLUE),
        ("INNERGRID",(0,0),(-1,-1),0.4, SKY),
        ("FONTNAME",(0,1),(-1,-1),"Helvetica"),
        ("FONTSIZE",(0,0),(-1,-1),9.5),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    return t

def resume_box(lines, title="SAMPLE RÉSUMÉ SECTION"):
    rows = [[Paragraph(title,
                       S("RBT", fontSize=10, textColor=WHITE,
                         fontName="Helvetica-Bold", alignment=TA_CENTER, leading=13))]]
    for line in lines:
        if line == "---":
            rows.append([HRFlowable(width="95%", thickness=0.5,
                                    color=GRAY_M, spaceAfter=2, spaceBefore=2)])
        elif line.startswith("##"):
            rows.append([Paragraph(line[2:],
                                   S("RBH", fontSize=11, textColor=DARK_NAVY,
                                     fontName="Helvetica-Bold", leading=14))])
        elif line.startswith("#"):
            rows.append([Paragraph(line[1:],
                                   S("RBS", fontSize=10, textColor=TEAL_M,
                                     fontName="Helvetica-Bold", leading=13))])
        else:
            rows.append([Paragraph(line,
                                   S("RBL", fontSize=9.5, textColor=BLACK,
                                     fontName="Courier", leading=13))])
    t = Table(rows, colWidths=[16.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,0), TEAL_M),
        ("BACKGROUND",(0,1),(-1,-1), colors.HexColor("#fafafa")),
        ("BOX",(0,0),(-1,-1),1.5, TEAL_M),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),14),("RIGHTPADDING",(0,0),(-1,-1),14),
    ]))
    return t

class NumberedCanvas(pdfcanvas.Canvas):
    def __init__(self, *args, **kwargs):
        pdfcanvas.Canvas.__init__(self, *args, **kwargs)
        self._saved = []
    def showPage(self):
        self._saved.append(dict(self.__dict__))
        self._startPage()
    def save(self):
        total = len(self._saved)
        for state in self._saved:
            self.__dict__.update(state)
            self._draw_footer(total)
            pdfcanvas.Canvas.showPage(self)
        pdfcanvas.Canvas.save(self)
    def _draw_footer(self, total):
        self.setFont("Helvetica", 8)
        self.setFillColor(GRAY_M)
        self.drawRightString(A4[0]-1.5*cm, 1.2*cm,
                             f"Page {self._pageNumber} of {total}")
        self.drawString(1.5*cm, 1.2*cm,
                        "OEC-CS-601(I) | Module 4 — Presentations, Interviews & Résumé Writing")
        self.setStrokeColor(LIGHT_BLUE)
        self.setLineWidth(0.5)
        self.line(1.5*cm, 1.5*cm, A4[0]-1.5*cm, 1.5*cm)

# ══════════════════════════════════════════════════════════════════════════════
story = []

# ── COVER ──────────────────────────────────────────────────────────────────────
cover_rows = [
    [sp(14)],
    [Paragraph("&#9733; OEC-CS-601(I) | Soft Skills &amp; Interpersonal Communication &#9733;",
               S("C1_4", fontSize=12, textColor=SKY,
                 fontName="Helvetica-Bold", alignment=TA_CENTER, leading=18))],
    [sp(8)],
    [Paragraph("MODULE 4",
               S("C2_4", fontSize=40, textColor=WHITE,
                 fontName="Helvetica-Bold", alignment=TA_CENTER, leading=46))],
    [Paragraph("PRESENTATION & INTERVIEW",
               S("C3_4", fontSize=20, textColor=colors.HexColor("#ffe0b2"),
                 fontName="Helvetica-Bold", alignment=TA_CENTER, leading=26))],
    [sp(8)],
    [HRFlowable(width="75%", thickness=2.5, color=AMBER,
                spaceAfter=8, spaceBefore=4)],
    [Paragraph("Effective Presentations  ·  Speeches for All Occasions",
               S("C4_4", fontSize=12, textColor=AMBER,
                 fontName="Helvetica-Bold", alignment=TA_CENTER, leading=18))],
    [Paragraph("Interviews  ·  Résumé Writing  ·  Career Communication",
               S("C5_4", fontSize=12, textColor=AMBER,
                 fontName="Helvetica-Bold", alignment=TA_CENTER, leading=18))],
    [sp(12)],
    [Paragraph("Max Marks: 75  |  5 Major Topics  |  80+ Q&amp;A  |  Sample Résumé &amp; Interview Q's Included",
               S("C6_4", fontSize=11, textColor=WHITE,
                 fontName="Helvetica", alignment=TA_CENTER, leading=16))],
    [sp(14)],
]
ct = Table(cover_rows, colWidths=[17*cm])
ct.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1), DARK_NAVY),
    ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
    ("LEFTPADDING",(0,0),(-1,-1),16),("RIGHTPADDING",(0,0),(-1,-1),16),
]))
story.append(ct)
story.append(sp(18))

legend = [["1.5 Marks (~50 words)", "5 Marks (300-500 words)",
           "10 Marks (500-700 words)", "15 Marks (700-1000 words)"]]
lt = Table(legend, colWidths=[4*cm, 4.5*cm, 4.5*cm, 4.5*cm])
lt.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(0,0), EMERALD_M),
    ("BACKGROUND",(1,0),(1,0), ROYAL_BLUE),
    ("BACKGROUND",(2,0),(2,0), AMBER),
    ("BACKGROUND",(3,0),(3,0), CRIMSON),
    ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),9),
    ("FONTCOLOR",(0,0),(-1,-1), WHITE),("ALIGN",(0,0),(-1,-1),"CENTER"),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
]))
story.append(lt)
story.append(PageBreak())

# ── TABLE OF CONTENTS ──────────────────────────────────────────────────────────
story.append(ch_banner("&#128196;  TABLE OF CONTENTS — MODULE 4: PRESENTATION & INTERVIEW"))
story.append(sp(10))
toc_data = [
    ("1",  "Making Effective Presentations",              "90%"),
    ("",   "  ↳ Elements of Effective Presentations",    ""),
    ("",   "  ↳ Presentation Tools & Visual Aids",       ""),
    ("",   "  ↳ Audience Engagement Techniques",         ""),
    ("",   "  ↳ Delivering with Impact",                 ""),
    ("2",  "Speeches for Various Occasions",              "88%"),
    ("",   "  ↳ Formal & Informal Speeches",             ""),
    ("",   "  ↳ Welcome, Vote of Thanks, Farewell",      ""),
    ("",   "  ↳ Toasts, Eulogies, Award Speeches",       ""),
    ("",   "  ↳ Sample Speeches for Each Occasion",      ""),
    ("3",  "Interviews — Types & Techniques",             "92%"),
    ("",   "  ↳ Types of Interviews",                    ""),
    ("",   "  ↳ Interview Preparation Strategies",       ""),
    ("",   "  ↳ Common Interview Questions & Answers",   ""),
    ("",   "  ↳ Dos and Don'ts of Interviews",           ""),
    ("4",  "Planning & Preparing (Part I): Résumé",       "95%"),
    ("",   "  ↳ What is a Résumé / CV?",                ""),
    ("",   "  ↳ Types of Résumé",                       ""),
    ("",   "  ↳ Components of a Résumé",                ""),
    ("",   "  ↳ Résumé Writing Principles",             ""),
    ("5",  "Planning & Preparing (Part II): Résumé",      "95%"),
    ("",   "  ↳ Cover Letter Writing",                  ""),
    ("",   "  ↳ Sample Résumé (Full Template)",         ""),
    ("",   "  ↳ Sample Cover Letter",                   ""),
    ("",   "  ↳ Common Résumé Mistakes to Avoid",       ""),
]
for num, title, pct in toc_data:
    is_main = bool(num)
    if is_main:
        row = [[
            Paragraph(f"<b>{num}.</b>  {title}", toc_i),
            Paragraph(f"<b>{pct}</b>",
                      S("TP4", fontSize=10, textColor=AMBER,
                        fontName="Helvetica-Bold", alignment=TA_RIGHT, leading=14)),
        ]]
        rt = Table(row, colWidths=[14*cm, 3*cm])
        rt.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1), LIGHT_BLUE),
            ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
            ("LEFTPADDING",(0,0),(0,0),10),
            ("LINEBELOW",(0,0),(-1,-1),0.5, SKY),
        ]))
    else:
        row = [[Paragraph(title,
                          S("TC_SUB", fontSize=9.5, textColor=GRAY_M,
                            fontName="Helvetica", leading=14, leftIndent=20))]]
        rt = Table(row, colWidths=[17*cm])
        rt.setStyle(TableStyle([
            ("TOPPADDING",(0,0),(-1,-1),2),("BOTTOMPADDING",(0,0),(-1,-1),2),
            ("LEFTPADDING",(0,0),(-1,-1),10),
            ("LINEBELOW",(0,0),(-1,-1),0.2, colors.HexColor("#e0e0e0")),
        ]))
    story.append(rt)
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — MAKING EFFECTIVE PRESENTATIONS
# ══════════════════════════════════════════════════════════════════════════════
story.append(ch_banner("MODULE 4: PRESENTATION & INTERVIEW", DARK_NAVY))
story.append(sp(10))
story.append(sec_hdr("1","Making Effective Presentations","90%", ROYAL_BLUE))
story.append(sp(8))

story.append(Paragraph("Overview — What Makes a Presentation 'Effective'?", sub1))
story.append(Paragraph(
    "An effective presentation is one that achieves its intended purpose — informing, persuading, motivating, "
    "or entertaining — while keeping the audience fully engaged from start to finish. Effectiveness is not "
    "about perfection; it is about communication impact. A presentation succeeds when the audience "
    "understands the message, remembers the key points, and is moved to think or act differently. "
    "The three pillars are: <b>Content</b> (what you say), <b>Structure</b> (how you organise it), "
    "and <b>Delivery</b> (how you communicate it).", body))
story.append(sp(6))

story.append(Paragraph("A. The 10 Elements of an Effective Presentation:", sub2))
elements = [
    ("1. Clear Purpose", "Every presentation must have a single, crystal-clear objective. "
     "Write it as one sentence: 'By the end, the audience will understand / be able to / decide to...' "
     "A presentation without clear purpose wastes everyone's time."),
    ("2. Deep Audience Understanding", "Analyse your audience before designing content: "
     "their knowledge level, expectations, interests, cultural background, and what they need from you. "
     "Audience analysis drives every decision — vocabulary, examples, depth, and tone."),
    ("3. Compelling Opening", "The first 60 seconds determine whether the audience is with you or not. "
     "Hook options: Shocking statistic | Thought-provoking question | Powerful quote | "
     "Brief story | Bold statement | Short video/demo. NEVER start with 'Good morning, my name is...'"),
    ("4. Logical, Clear Structure", "Three-part structure: Opening (15%) → Body (70%) → Close (15%). "
     "Maximum 3-5 main points. Use signposting: 'My first point is...' 'Before I move on...' 'Finally...' "
     "Tell them → Tell them → Tell them (Preview → Deliver → Summarise)."),
    ("5. Evidence-Based Content", "Every claim must be supported: statistics, case studies, expert quotes, "
     "research findings, real-world examples. Unsupported claims are opinions; supported claims are evidence."),
    ("6. Storytelling", "Stories activate 7 regions of the brain versus 2 for pure data. "
     "Embed key messages in stories — personal experiences, client case studies, historical examples. "
     "The audience will forget your slides; they will remember your stories."),
    ("7. High-Quality Visual Aids", "Slides support — they do not replace — the speaker. "
     "Apply: 6x6 Rule (max 6 bullets × 6 words), high contrast, readable fonts (24pt min), "
     "one idea per slide, visuals over text. Test all technology in advance."),
    ("8. Dynamic Delivery", "Vocal variety (pitch, pace, volume, pause), purposeful movement, "
     "genuine eye contact (3-5 seconds per person), open gestures, and authentic enthusiasm. "
     "Delivery is what the audience experiences — content is what they receive."),
    ("9. Active Audience Engagement", "Engagement techniques: rhetorical questions, think-pair-share, "
     "polls, demonstrations, humour, interactive exercises. An engaged audience is a receptive audience."),
    ("10. Powerful Close", "The close is the last thing the audience hears — make it memorable. "
     "Summarise → Call to Action → Callback to opening or inspiring quote. "
     "NEVER end with 'That's all I have' or trail off lamely."),
]
for title, desc in elements:
    story.append(Paragraph(f"<b>{title}:</b> {desc}", bul))
    story.append(sp(3))
story.append(sp(5))

story.append(Paragraph("B. Advanced Audience Engagement Techniques:", sub2))
engage_techs = [
    ("Rhetorical Questions", "Pose questions that provoke thought without requiring verbal answers: "
     "'How many of you have ever lost important data?' Creates mental engagement immediately."),
    ("Think-Pair-Share", "Give audience 60 seconds to think about a question, discuss with neighbour, "
     "then share with the group. Increases participation and retention."),
    ("Live Polling", "Use tools like Mentimeter, Slido, or show of hands for instant audience input. "
     "Shows responses affect the presentation's direction."),
    ("Demonstrations", "Show rather than tell. Live demos are more memorable and credible than slides."),
    ("Storytelling and Analogies", "Relatable stories and comparisons make abstract concepts concrete and memorable."),
    ("Humour (Used Carefully)", "Appropriate, inclusive humour relaxes the room and builds rapport. "
     "Never use: political, religious, gender-based, or ethnicity-related humour."),
    ("Strategic Pauses", "Silence after a key point lets it sink in. Counted pause of 3-5 seconds "
     "after a significant statement is far more powerful than rushing on."),
    ("Name Dropping (Audience)", "Use audience members' names (where known) or reference their industry/context. "
     "Personalises the presentation and shows you did your homework."),
]
for t, d in engage_techs:
    story.append(Paragraph(f"&#9654; <b>{t}:</b> {d}", bul))
    story.append(sp(2))
story.append(sp(5))

story.append(Paragraph("C. Visual Aid Best Practices:", sub2))
story.append(grid_table(
    ["Principle", "Best Practice", "Common Mistake to Avoid"],
    [
        ["Text Amount", "6x6: max 6 bullets × 6 words each", "Writing full paragraphs on slides"],
        ["Font Size", "Heading: 36pt+; Body: 24pt minimum", "Font below 20pt — unreadable from distance"],
        ["Colour Contrast", "Dark text on light; light on dark", "Similar colours that blend together"],
        ["Images vs Text", "Use images, charts, diagrams over text", "Clipart and irrelevant stock images"],
        ["Slide Count", "1 slide per ~2 minutes of speaking", "50 slides for a 10-minute talk"],
        ["Consistency", "Same theme, fonts, colours throughout", "Mixing 5 different fonts and themes"],
        ["Animation", "Sparingly; only where it adds clarity", "Flashy transitions on every element"],
        ["Data Visuals", "Label all charts; show only needed data", "Cluttered charts with too many data sets"],
    ],
    [3.5*cm, 6.5*cm, 6.5*cm]
))
story.append(sp(5))

story.append(Paragraph("D. The PPPF Framework for Presentation Success:", sub2))
story.append(Paragraph(
    "<b>P — Purpose:</b> Define exactly what you want to achieve.<br/>"
    "<b>P — Preparation:</b> Research, outline, design, practice — deeply and thoroughly.<br/>"
    "<b>P — Practice:</b> Full out-loud rehearsals; timed; recorded; with feedback.<br/>"
    "<b>F — Feedback:</b> Incorporate feedback from every presentation to continuously improve.", body))
story.append(sp(6))
story.append(tip_box(
    "The 10-20-30 Rule (Guy Kawasaki): No more than 10 SLIDES, no longer than 20 MINUTES, "
    "no smaller than 30pt FONT. A brilliantly simple framework for business pitches and presentations."))
story.append(sp(8))

story.append(q_sec_hdr("PRACTICE QUESTIONS — TOPIC 1: Making Effective Presentations", ROYAL_BLUE))
story.append(sp(6))
for item in q_box("1.5 MARKS (~50 words)", EMERALD_M,
    "What is the 6x6 Rule in presentations?",
    "The 6x6 Rule is a slide design guideline stating that each slide should contain no more than "
    "6 bullet points and each bullet point should be no longer than 6 words. This prevents information "
    "overload, keeps slides clean and readable, and ensures the audience listens to the speaker "
    "rather than reading dense text."):
    story.append(item)

for item in q_box("5 MARKS (300-500 words)", ROYAL_BLUE,
    "What are the key elements that make a presentation effective?",
    "<b>Introduction:</b> An effective presentation achieves its purpose — informing, persuading, or "
    "motivating — while keeping the audience fully engaged. Effectiveness depends on content, "
    "structure, and delivery working together seamlessly.<br/><br/>"
    "<b>Key Elements:</b><br/>"
    "1. <b>Clear Purpose:</b> One-sentence objective — 'By the end, the audience will...' "
    "A purposeless presentation wastes everyone's time.<br/>"
    "2. <b>Audience Analysis:</b> Understanding knowledge level, expectations, and needs determines "
    "vocabulary, depth, examples, and tone.<br/>"
    "3. <b>Compelling Opening:</b> First 60 seconds must hook attention — shocking statistic, "
    "powerful question, brief story. Never start with 'Good morning, my name is...'<br/>"
    "4. <b>Logical Structure:</b> Opening (15%) → Body with 3-5 main points (70%) → "
    "Strong Conclusion (15%). Preview → Deliver → Summarise.<br/>"
    "5. <b>Evidence-Based Content:</b> Statistics, case studies, expert quotes supporting every claim.<br/>"
    "6. <b>Storytelling:</b> Stories activate 7 brain regions; data activates 2. Stories are remembered.<br/>"
    "7. <b>Quality Visual Aids:</b> 6x6 rule; one idea per slide; visuals over text; 24pt minimum font.<br/>"
    "8. <b>Dynamic Delivery:</b> Vocal variety, eye contact, open gestures, controlled movement.<br/>"
    "9. <b>Audience Engagement:</b> Rhetorical questions, polls, demos, strategic humour.<br/>"
    "10. <b>Memorable Close:</b> Summarise → Call to Action → Powerful final statement.<br/><br/>"
    "<b>Conclusion:</b> The best presentations make complex ideas simple, make information personal "
    "through stories, and leave the audience moved to think or act differently."):
    story.append(item)

for item in q_box("15 MARKS (700-1000 words)", CRIMSON,
    "Discuss in detail the techniques for making an effective presentation. Include structure, delivery, visual aids, and audience engagement.",
    "<b>Introduction:</b><br/>"
    "A presentation is the most visible test of professional communication skills. Unlike written reports "
    "or emails, presentations unfold in real time before a live audience — every choice of word, pause, "
    "gesture, and slide is immediately evaluated. Making presentations effective requires mastery of four "
    "interconnected domains: content, structure, visual design, and live delivery.<br/><br/>"
    "<b>1. PRE-PRESENTATION PREPARATION:</b><br/>"
    "Effective presentations begin long before the speaker stands up. Purpose definition — writing a "
    "single-sentence objective — anchors all subsequent decisions. Audience analysis determines vocabulary, "
    "depth, tone, and example selection. A presentation for data scientists requires different language "
    "and examples than the same content for business executives.<br/>"
    "Content research must be thorough — gather more than needed, then select the most relevant, "
    "accurate, and compelling evidence. Every claim must be supported: statistics, case studies, "
    "expert quotes, or demonstrations.<br/><br/>"
    "<b>2. STRUCTURE — The Three-Part Framework:</b><br/>"
    "<b>Opening (15% of time):</b> The first 60 seconds determine audience engagement. "
    "Use a hook: shocking statistic, thought-provoking question, brief story, bold claim, or powerful quote. "
    "Then establish credibility ('As a 10-year practitioner in this field...'), state relevance "
    "('This affects every one of you...'), and preview the structure ('Today I will cover three key areas...').<br/>"
    "<b>Body (70% of time):</b> Maximum 3-5 main points. More than 5 exceeds audience retention capacity. "
    "Each point follows: State it → Explain it → Support with evidence/example → Transition. "
    "Use clear signposting between points: 'My first point...', 'Building on this...', 'Finally...' "
    "Embed at least one story or relatable analogy — stories are remembered when statistics are forgotten.<br/>"
    "<b>Conclusion (15% of time):</b> Signal closure ('In summary...'), restate the 3-5 main points, "
    "deliver a clear call to action, and close with a memorable final statement — callback to opening, "
    "inspiring quote, or challenge to the audience. The close is the last impression — make it count.<br/><br/>"
    "<b>3. VISUAL AIDS — Support, Not Substitute:</b><br/>"
    "Slides support the speaker; they do not replace the speaker. Key design principles: "
    "6x6 Rule (max 6 bullets × 6 words); 24pt minimum font; high colour contrast; one idea per slide; "
    "visuals (images, charts, diagrams) over dense text. Use the 10-20-30 Rule: max 10 slides, "
    "20 minutes, 30pt font. Test all technology before the event — always have a printed backup. "
    "Label every chart and graph; reference all visuals in spoken content.<br/><br/>"
    "<b>4. DELIVERY SKILLS:</b><br/>"
    "<b>Vocal Variety:</b> Vary pitch (high for excitement, low for authority), volume (loud for emphasis, "
    "soft for intimacy), and pace (slow for importance, faster for energy). Eliminate filler words "
    "('um', 'uh', 'like', 'you know') through recording and practice.<br/>"
    "<b>Eye Contact:</b> Hold gaze with each audience member for 3-5 seconds. "
    "Creates personal connection even in large rooms. Avoid reading from screen or notes.<br/>"
    "<b>Gestures:</b> Open, natural hand gestures reinforce points and signal confidence. "
    "Avoid: touching face, crossing arms, hands in pockets, pen clicking.<br/>"
    "<b>Movement:</b> Move purposefully. Step forward for emphasis; step to the side for a new point; "
    "face the audience always — never turn your back to read slides.<br/>"
    "<b>Pauses:</b> Strategic silence after key points allows information to land. "
    "3-5 second pauses are far more powerful than rushing nervously forward.<br/><br/>"
    "<b>5. AUDIENCE ENGAGEMENT TECHNIQUES:</b><br/>"
    "Rhetorical questions maintain mental engagement without requiring verbal response. "
    "Think-Pair-Share activities increase participation. Live polling (Mentimeter, Slido) creates "
    "interactivity. Demonstrations show rather than tell — far more credible and memorable. "
    "Appropriate, inclusive humour relaxes the audience and builds rapport. "
    "Using audience members' names or referencing their context personalises the presentation.<br/><br/>"
    "<b>6. POST-PRESENTATION:</b><br/>"
    "Invite and manage questions professionally. Listen fully before answering. "
    "If unsure: 'I'll verify that and get back to you.' Never bluff. "
    "Collect feedback for improvement. Follow up with promised information.<br/><br/>"
    "<b>Conclusion:</b><br/>"
    "Making an effective presentation is a learnable skill, not a natural talent. "
    "The difference between a good and a great presenter is systematic preparation, "
    "deliberate practice, honest self-evaluation, and continuous improvement. "
    "Every presentation — regardless of outcome — is an opportunity to grow as a communicator."):
    story.append(item)
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — SPEECHES FOR VARIOUS OCCASIONS
# ══════════════════════════════════════════════════════════════════════════════
story.append(sec_hdr("2","Speeches for Various Occasions","88%", TEAL_M))
story.append(sp(8))

story.append(Paragraph("What are Occasional Speeches?", sub1))
story.append(Paragraph(
    "Occasional speeches are speeches delivered for specific social, professional, or ceremonial occasions. "
    "They differ from formal presentations in that they are often shorter, more personal, more emotional, "
    "and more audience-connecting. They mark transitions, honour people, celebrate achievements, "
    "and build community. Every professional must be able to deliver occasional speeches confidently.", body))
story.append(sp(5))

story.append(Paragraph("1. WELCOME SPEECH:", sub2))
story.append(Paragraph(
    "<b>Purpose:</b> To greet and introduce guests/participants at an event — conference, seminar, "
    "cultural programme, academic function.<br/>"
    "<b>Key Elements:</b><br/>"
    "&#9654; Warm greeting addressing the audience and distinguished guests<br/>"
    "&#9654; Introduction of the occasion/event and its significance<br/>"
    "&#9654; Brief introduction of distinguished guests (in order of seniority)<br/>"
    "&#9654; Overview of the programme/agenda<br/>"
    "&#9654; Expression of gratitude to organisers and participants<br/>"
    "&#9654; Wish that the event/occasion proves fruitful and enjoyable<br/>"
    "<b>Tone:</b> Warm, inclusive, formal but friendly. Usually 2-3 minutes.<br/>"
    "<b>Language:</b> 'It is my honour and privilege...', 'We are delighted to welcome...', "
    "'On behalf of...'", body))
story.append(sp(4))

story.append(resume_box([
    "## SAMPLE WELCOME SPEECH",
    "---",
    "Respected Chief Guest, Mr. Rajesh Sharma, Director of Innovation, TechCorp Ltd.,",
    "Distinguished faculty members, honoured guests,",
    "and my dear fellow students —",
    "",
    "A very warm good morning to each and every one of you.",
    "",
    "It is my immense honour and privilege to welcome you all to the",
    "Annual Technical Symposium 2025 of the Department of Computer Science,",
    "hosted by our esteemed institution.",
    "",
    "This symposium represents a platform where brilliant minds converge",
    "to share knowledge, spark innovation, and forge connections that",
    "transcend the boundaries of classrooms.",
    "",
    "We are especially privileged today to have Mr. Rajesh Sharma with us,",
    "whose pioneering work in Artificial Intelligence has inspired a generation",
    "of technology professionals. Sir, your presence honours us greatly.",
    "",
    "The day promises to be intellectually stimulating, with paper presentations,",
    "panel discussions, and a keynote address that I am confident will",
    "leave us all with fresh perspectives.",
    "",
    "On behalf of the organising committee and the entire department,",
    "I extend the warmest welcome to each of you. We hope this day",
    "proves enriching, inspiring, and thoroughly enjoyable.",
    "",
    "Thank you.",
], "SAMPLE — WELCOME SPEECH"))
story.append(sp(8))

story.append(Paragraph("2. VOTE OF THANKS:", sub2))
story.append(Paragraph(
    "<b>Purpose:</b> To formally thank all contributors and participants at the conclusion of an event.<br/>"
    "<b>Key Elements:</b><br/>"
    "&#9654; Thank the chief guest / keynote speaker (most prominently)<br/>"
    "&#9654; Thank other speakers, resource persons, and dignitaries<br/>"
    "&#9654; Thank the organising team, sponsors, and supporting staff<br/>"
    "&#9654; Thank the audience for their time and participation<br/>"
    "&#9654; Brief note on the value of the event<br/>"
    "&#9654; Close with hope to meet again / invitation to future events<br/>"
    "<b>Important:</b> Name people specifically — generic thanks are hollow. "
    "Keep it concise (2-3 mins max). Do NOT summarise the event — that is the anchor's job.<br/>"
    "<b>Language:</b> 'We are profoundly grateful to...', 'Words fall short of expressing...'", body))
story.append(sp(4))

story.append(resume_box([
    "## SAMPLE VOTE OF THANKS",
    "---",
    "Respected dignitaries on the dais, distinguished guests,",
    "faculty members, and dear participants —",
    "",
    "As we draw the curtains on today's Annual Technical Symposium 2025,",
    "I have the privilege and pleasure of expressing our heartfelt gratitude",
    "to all who made this event the grand success it has been.",
    "",
    "We begin by extending our deepest thanks to our Chief Guest,",
    "Mr. Rajesh Sharma, whose keynote address on 'AI and the Future of Work'",
    "was nothing short of transformative. Your insights have left a lasting",
    "impression on every mind in this auditorium. Thank you, Sir.",
    "",
    "Our sincere gratitude to our Principal, Dr. Anita Verma, whose vision",
    "and unwavering support made this event possible.",
    "",
    "We thank our faculty coordinators — especially Prof. S. Menon and",
    "Prof. R. Iyer — whose tireless efforts behind the scenes ensured",
    "seamless execution.",
    "",
    "A heartfelt thank you to our sponsors, the student volunteer team,",
    "the technical crew, and every participant whose enthusiasm gave this",
    "event its energy.",
    "",
    "And finally, to you — our wonderful audience — thank you for your",
    "time, your questions, and your engagement. You are what made today matter.",
    "",
    "We hope to see you again at future events. Thank you.",
], "SAMPLE — VOTE OF THANKS"))
story.append(sp(8))

story.append(Paragraph("3. FAREWELL SPEECH:", sub2))
story.append(Paragraph(
    "<b>Purpose:</b> To bid goodbye to a colleague, teacher, student, or group leaving an organisation.<br/>"
    "<b>Key Elements:</b><br/>"
    "&#9654; Personal and warm acknowledgement of the person/group leaving<br/>"
    "&#9654; Recall of shared memories, achievements, and contributions<br/>"
    "&#9654; Expression of what they meant to the organisation/group<br/>"
    "&#9654; Wishes for their future — new chapter, success ahead<br/>"
    "&#9654; Assurance that they will always be remembered and welcomed<br/>"
    "<b>Tone:</b> Warm, nostalgic, personal, and hopeful. Often emotional but professional.<br/>"
    "<b>Avoid:</b> Being overly sad or making the departing person feel they are dying. "
    "Celebrate the next chapter!", body))
story.append(sp(5))

story.append(Paragraph("4. TOAST SPEECH:", sub2))
story.append(Paragraph(
    "<b>Purpose:</b> A short speech at a dinner, celebration, or social gathering honouring a person or occasion.<br/>"
    "<b>Key Elements:</b> Very brief (30-90 seconds); personal; celebratory; ends with raising a glass/cheers.<br/>"
    "<b>Structure:</b> Acknowledge the occasion → Personal tribute or memory → Wish or compliment → "
    "Invite audience to raise their glasses → 'Please join me in raising a toast to [Name/Occasion]!'<br/>"
    "<b>Tone:</b> Celebratory, warm, sometimes humorous (appropriately).", body))
story.append(sp(5))

story.append(Paragraph("5. EULOGY:", sub2))
story.append(Paragraph(
    "<b>Purpose:</b> A speech delivered at a funeral or memorial service honouring the life of a deceased person.<br/>"
    "<b>Key Elements:</b><br/>"
    "&#9654; Introduce yourself and your relationship to the deceased<br/>"
    "&#9654; Share specific memories, qualities, and achievements<br/>"
    "&#9654; Talk about their impact on others and the community<br/>"
    "&#9654; Offer comfort to those grieving<br/>"
    "&#9654; Close with a final tribute — their values, legacy, or favourite quote<br/>"
    "<b>Tone:</b> Dignified, heartfelt, and hopeful. Balance grief with celebration of life.<br/>"
    "<b>Length:</b> 3-5 minutes. Prepare fully in writing and practice delivery.", body))
story.append(sp(5))

story.append(Paragraph("6. ACCEPTANCE/AWARD SPEECH:", sub2))
story.append(Paragraph(
    "<b>Purpose:</b> Delivered when receiving an award, honour, or recognition.<br/>"
    "<b>Key Elements:</b><br/>"
    "&#9654; Express genuine gratitude — not false modesty<br/>"
    "&#9654; Thank specific people who contributed to the achievement<br/>"
    "&#9654; Share what the award means to you and what it represents<br/>"
    "&#9654; Inspire others — acknowledge the community/team effort<br/>"
    "&#9654; Brief, humble, and heartfelt<br/>"
    "<b>Classic Mistake:</b> Forgetting to thank key people. Prepare a list in advance.", body))
story.append(sp(5))

story.append(Paragraph("7. MOTIVATIONAL / COMMENCEMENT SPEECH:", sub2))
story.append(Paragraph(
    "<b>Purpose:</b> To inspire and motivate an audience at a milestone occasion — graduation, convocation, "
    "new employee orientation, team launch.<br/>"
    "<b>Key Elements:</b><br/>"
    "&#9654; Acknowledge the occasion's significance<br/>"
    "&#9654; Share a personal story or universal truth<br/>"
    "&#9654; Present a central message/theme — one big idea to carry forward<br/>"
    "&#9654; Challenge the audience to greatness<br/>"
    "&#9654; Close with a powerful, memorable call to action<br/>"
    "<b>Tone:</b> Inspiring, energetic, authentic. Famous examples: Steve Jobs Stanford Commencement (2005), "
    "Oprah Winfrey Harvard Commencement (2013).", body))
story.append(sp(6))

story.append(Paragraph("Comparison of Occasional Speeches:", sub2))
story.append(grid_table(
    ["Speech Type", "Occasion", "Tone", "Length"],
    [
        ["Welcome Speech", "Event opening", "Warm, formal-friendly", "2-3 minutes"],
        ["Vote of Thanks", "Event closing", "Grateful, sincere", "2-3 minutes"],
        ["Farewell Speech", "Someone leaving", "Nostalgic, hopeful", "3-5 minutes"],
        ["Toast", "Celebration/dinner", "Celebratory, light", "30-90 seconds"],
        ["Eulogy", "Funeral/memorial", "Dignified, heartfelt", "3-5 minutes"],
        ["Award Speech", "Receiving honour", "Humble, grateful", "1-3 minutes"],
        ["Motivational", "Graduation/launch", "Inspiring, energetic", "5-20 minutes"],
    ],
    [4*cm, 4*cm, 4.5*cm, 4*cm]
))
story.append(sp(8))

story.append(q_sec_hdr("PRACTICE QUESTIONS — TOPIC 2: Speeches for Various Occasions", TEAL_M))
story.append(sp(6))
for item in q_box("1.5 MARKS", EMERALD_M, "What is a Vote of Thanks?",
    "A Vote of Thanks is a formal speech delivered at the conclusion of an event to thank all contributors — "
    "chief guest, speakers, organisers, sponsors, and audience. It names people specifically, "
    "acknowledges their contributions, and expresses genuine gratitude. It closes with an "
    "invitation to future events and should be concise (2-3 minutes maximum)."):
    story.append(item)

for item in q_box("5 MARKS (300-500 words)", ROYAL_BLUE,
    "What is a Welcome Speech? Write a sample welcome speech for a college annual day function.",
    "<b>Definition and Purpose:</b> A welcome speech is delivered at the opening of an event to greet "
    "guests, introduce the occasion, and set a positive tone. It introduces distinguished guests, "
    "outlines the programme, and expresses gratitude to all for attending.<br/><br/>"
    "<b>Key Elements:</b> Formal greeting addressing guests in order of seniority; introduction of the "
    "event's significance; brief introduction of chief guest; programme overview; expression of "
    "gratitude; warm closing wish.<br/><br/>"
    "<b>SAMPLE WELCOME SPEECH — Annual Day Function:</b><br/><br/>"
    "Respected Chief Guest, Dr. Priya Menon, Director of Education, Maharashtra;<br/>"
    "Respected Principal, Dr. Ramesh Iyer; distinguished faculty members;<br/>"
    "proud parents; and my dear students —<br/><br/>"
    "A very warm good evening to each and every one of you.<br/><br/>"
    "It is with immense pride and joy that I welcome you to the 25th Annual Day of "
    "St. Xavier's College of Arts and Science — a golden milestone in our institution's journey.<br/><br/>"
    "Tonight, we gather not merely to celebrate achievements but to honour the spirit "
    "of excellence, creativity, and hard work that defines every student of this institution.<br/><br/>"
    "We are truly honoured to have with us Dr. Priya Menon, whose contributions to "
    "educational policy have transformed thousands of young lives. Dr. Menon, your "
    "presence tonight elevates this occasion immeasurably.<br/><br/>"
    "The evening promises cultural performances, prize distributions, and inspiring words "
    "that will stay in our hearts long after tonight concludes.<br/><br/>"
    "On behalf of the entire St. Xavier's family, I extend our warmest welcome. "
    "We hope this evening brings you as much joy as it does us. Thank you."):
    story.append(item)

for item in q_box("10 MARKS (500-700 words)", AMBER,
    "Explain the different types of speeches for various occasions. Write sample outlines for any three.",
    "<b>Introduction:</b><br/>Occasional speeches are tailored to specific social, professional, or "
    "ceremonial contexts. Each type has a distinct purpose, tone, and structure. "
    "The ability to speak appropriately for different occasions is a mark of true communication maturity.<br/><br/>"
    "<b>Types of Occasional Speeches:</b><br/>"
    "<b>1. Welcome Speech:</b> Opens an event. Greets audience and dignitaries; introduces occasion "
    "and programme; sets a positive tone. Tone: Warm, formal-friendly. Length: 2-3 minutes.<br/>"
    "Outline: Formal greeting → Introduce occasion → Acknowledge distinguished guests → "
    "Programme overview → Gratitude → Warm welcome.<br/><br/>"
    "<b>2. Vote of Thanks:</b> Closes an event. Thanks all contributors by name. Tone: Sincere, grateful. "
    "Length: 2-3 minutes. KEY RULE: Name people specifically — generic thanks are empty.<br/>"
    "Outline: Open graciously → Thank chief guest → Thank speakers → Thank organisers/sponsors → "
    "Thank audience → Closing hope to meet again.<br/><br/>"
    "<b>3. Farewell Speech:</b> Bids goodbye to a departing colleague/student. Recalls shared memories "
    "and contributions. Wishes for the future. Tone: Warm, nostalgic, hopeful. Length: 3-5 minutes.<br/>"
    "Outline: Personal acknowledgement → Shared memories → Their contributions/impact → "
    "What they meant to us → Warm wishes for the future → Assurance of being remembered.<br/><br/>"
    "<b>4. Toast:</b> Short (30-90 secs) celebration speech at dinner/event. "
    "Ends with raising glasses. Tone: Celebratory. Outline: Occasion → Personal tribute → "
    "Wish → 'Please raise your glasses to [Name/Occasion]!'<br/><br/>"
    "<b>5. Eulogy:</b> Honours a deceased person at a memorial. Tone: Dignified, heartfelt. "
    "Length: 3-5 minutes. Outline: Self-introduction & relationship → Specific memories & qualities → "
    "Impact on others → Comfort to grieving → Final tribute/legacy statement.<br/><br/>"
    "<b>6. Award/Acceptance Speech:</b> When receiving recognition. Tone: Humble, grateful. "
    "Length: 1-3 minutes. Outline: Express gratitude → Thank specific contributors → "
    "Meaning of award → Inspire others.<br/><br/>"
    "<b>7. Motivational/Commencement:</b> Inspires at milestone occasions. Tone: Inspiring, authentic. "
    "Length: 5-20 minutes. Outline: Acknowledge occasion → Personal story/universal truth → "
    "Central theme/message → Challenge audience → Powerful call to action.<br/><br/>"
    "<b>Conclusion:</b><br/>The most effective occasional speeches are those that feel personal, "
    "authentic, and prepared — not read verbatim from a paper but delivered from the heart "
    "with careful preparation. Every occasion deserves a speech that honours its significance."):
    story.append(item)
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — INTERVIEWS
# ══════════════════════════════════════════════════════════════════════════════
story.append(sec_hdr("3","Interviews — Types, Preparation & Techniques","92%", CRIMSON))
story.append(sp(8))

story.append(Paragraph("What is an Interview?", sub1))
story.append(Paragraph(
    "An interview is a structured, formal conversation between two or more people where one party "
    "(the interviewer/s) asks questions to assess the other party (the interviewee) for a specific "
    "purpose — employment, admission, research, journalism, or appraisal. "
    "Interviews are among the most consequential communication events in a professional's life — "
    "a 30-minute interview can determine a career trajectory.", body))
story.append(sp(5))

story.append(Paragraph("A. Types of Interviews:", sub2))
interview_types = [
    ("1. Selection/Employment Interview", "Most common — conducted by employers to select candidates for a job. "
     "Assesses: qualifications, experience, personality, communication, cultural fit, and motivation."),
    ("2. Structured Interview", "All candidates are asked the same predetermined questions in the same order. "
     "Ensures fairness, comparability, and reduced bias. Most reliable type for selection."),
    ("3. Unstructured Interview", "Free-flowing, conversational. Interviewer follows the candidate's responses. "
     "More flexible but less reliable and harder to compare candidates."),
    ("4. Semi-Structured Interview", "Predetermined core questions with flexibility to explore responses. "
     "Most common in practice — combines structure with conversational depth."),
    ("5. Panel Interview", "Multiple interviewers simultaneously question one candidate. "
     "Tests composure under pressure, ability to address diverse stakeholders, and consistency of answers."),
    ("6. Group Interview", "Multiple candidates assessed simultaneously. Tests: teamwork, leadership, "
     "communication, competitive performance, and problem-solving in a group setting."),
    ("7. Telephonic / Video Interview", "Conducted via phone or video call (Zoom, Teams, Skype). "
     "Screening stage for shortlisting. Voice quality, clarity, and background (video) are critical."),
    ("8. Stress Interview", "Interviewer deliberately creates pressure — challenging questions, long silences, "
     "contradictions. Tests emotional control, composure, and performance under pressure."),
    ("9. Behavioural Interview", "Questions based on past behaviour: 'Tell me about a time when...' "
     "Based on the principle that past behaviour predicts future performance. "
     "Answer with the STAR method."),
    ("10. Case Interview", "Candidate is given a business problem to analyse and solve on the spot. "
     "Common in consulting (McKinsey, BCG, Deloitte). Tests analytical, logical, and communication skills."),
    ("11. HR Interview", "Focuses on personality, values, salary expectations, availability, "
     "and organisational fit rather than technical competence."),
    ("12. Technical Interview", "Tests domain-specific knowledge, skills, and problem-solving ability. "
     "Common in IT, engineering, finance, law, and medicine."),
]
for t, d in interview_types:
    story.append(Paragraph(f"&#9654; <b>{t}:</b> {d}", bul))
    story.append(sp(2))
story.append(sp(5))

story.append(Paragraph("B. Interview Preparation — The 5-Phase Strategy:", sub2))
prep_phases = [
    ("Phase 1: Research (Company & Role)", [
        "Study the company: history, products/services, revenue, culture, competitors, recent news.",
        "Understand the job description: every word is a clue to what they value.",
        "Research the industry: trends, challenges, key players, regulatory environment.",
        "Know your interviewer: LinkedIn profile of the interviewer if possible.",
        "Prepare intelligent questions to ask — shows genuine interest and preparation.",
    ]),
    ("Phase 2: Know Yourself (Self-Analysis)", [
        "Review your entire résumé — be ready to elaborate on every line.",
        "Identify your top 5 strengths with specific evidence for each.",
        "Identify 2-3 genuine weaknesses with your mitigation plan (not fake weaknesses like 'I work too hard').",
        "Prepare your career story: where have you been, where are you, where are you going, and why this role?",
        "Know your salary expectations based on market research.",
    ]),
    ("Phase 3: Prepare Answers — STAR Method", [
        "STAR = Situation → Task → Action → Result.",
        "For behavioural questions ('Tell me about a time...'), use STAR to structure answers.",
        "Prepare 8-10 STAR stories covering: leadership, teamwork, conflict, failure, achievement, initiative.",
        "Each story should be 1.5-2 minutes — not a 5-minute monologue.",
    ]),
    ("Phase 4: Practice Delivery", [
        "Mock interviews with a friend or mentor — record and review.",
        "Practice in front of a mirror for non-verbal awareness.",
        "Time your answers: 1.5-2 minutes for most questions; 3 minutes maximum for complex ones.",
        "Practise firm handshake, confident posture, and interview room entry.",
    ]),
    ("Phase 5: Logistics Preparation", [
        "Plan route to venue — arrive 10-15 minutes early (not 30+ minutes).",
        "Prepare professional attire (ironed, clean, appropriate for company culture).",
        "Bring: copies of résumé, certificates, ID, pen, notepad.",
        "Silence phone completely before entering the building.",
        "Get adequate sleep the night before; eat a light meal before.",
    ]),
]
for phase, points in prep_phases:
    story.append(Paragraph(f"<b>{phase}</b>", sub3))
    for p in points:
        story.append(Paragraph(f"&#9654; {p}", bul))
    story.append(sp(4))

story.append(Paragraph("C. The STAR Method for Behavioural Questions:", sub2))
story.append(info_box(
    "STAR Method — The Gold Standard for Behavioural Interview Answers",
    "<b>S — Situation:</b> Describe the context/background. When? Where? Who was involved?<br/>"
    "<b>T — Task:</b> What was YOUR specific responsibility in this situation?<br/>"
    "<b>A — Action:</b> What specific steps did YOU take? Use 'I' not 'we' — the interviewer is assessing YOU.<br/>"
    "<b>R — Result:</b> What was the outcome? Quantify wherever possible — '20% improvement', 'team met deadline 3 days early'.<br/><br/>"
    "<b>Example Q:</b> 'Tell me about a time you managed a difficult team conflict.'<br/>"
    "<b>S:</b> During my final year project, two team members had a significant disagreement over technical approach...<br/>"
    "<b>T:</b> As team leader, it was my responsibility to resolve the conflict before the submission deadline...<br/>"
    "<b>A:</b> I scheduled a structured meeting, asked each person to present their approach objectively, "
    "facilitated a vote, and ensured the losing side's concerns were formally documented...<br/>"
    "<b>R:</b> The team reached consensus within two days, maintained productive relationships, and submitted "
    "the project on time, receiving the highest grade in the class.",
    GOLD_L, BROWN, GOLD))
story.append(sp(6))

story.append(Paragraph("D. 20 Most Common Interview Questions with Model Answers:", sub2))
common_qs = [
    ("1. Tell me about yourself.",
     "Model: Start with present (current role/status), go to past (relevant background), "
     "end with future (why this role). Keep to 90 seconds. It's a professional summary — not a biography."),
    ("2. Why do you want to work here?",
     "Model: Mention specific company qualities (culture, products, mission, growth trajectory) + "
     "how your skills align + what you can contribute. Show research."),
    ("3. What are your strengths?",
     "Model: Choose 2-3 strengths directly relevant to the role. Support each with a specific example. "
     "Avoid generic answers like 'I'm a hard worker.'"),
    ("4. What are your weaknesses?",
     "Model: Choose a genuine, non-critical weakness. Show self-awareness and the steps you are taking to improve. "
     "'I used to struggle with public speaking, but I joined Toastmasters 6 months ago and have presented at 8 events.'"),
    ("5. Where do you see yourself in 5 years?",
     "Model: Show ambition aligned with realistic career progression. Connect your goal to this role and company. "
     "Avoid: 'In your position' or 'Running my own business.'"),
    ("6. Why should we hire you?",
     "Model: Summarise your unique value — the intersection of what they need and what you offer. "
     "Reference specific skills and experiences that match the job description."),
    ("7. Tell me about a challenge you overcame.",
     "Model: Use STAR method. Choose a significant professional challenge. "
     "Emphasise YOUR actions and a measurable positive result."),
    ("8. How do you handle pressure and deadlines?",
     "Model: Describe your system (prioritisation, planning, communication). "
     "Give a specific STAR example of successful delivery under pressure."),
    ("9. Describe your leadership style.",
     "Model: Identify your primary style (democratic, coaching, transformational). "
     "Give one STAR example demonstrating it. Acknowledge situational adaptability."),
    ("10. Do you have any questions for us?",
     "Model: ALWAYS have 3-5 prepared questions. Ask about: team culture, success metrics for the role, "
     "growth opportunities, current challenges, next steps. NEVER ask about salary first."),
]
for q, ans in common_qs:
    story.append(Paragraph(f"<b>{q}</b>", sub3))
    story.append(Paragraph(ans, body))
    story.append(sp(3))
story.append(sp(5))

story.append(Paragraph("E. Dos and Don'ts of Job Interviews:", sub2))
story.append(grid_table(
    ["&#10003; DOs", "&#9888; DON'Ts"],
    [
        ["Arrive 10-15 minutes early", "Arrive late (even by 5 minutes)"],
        ["Research company thoroughly", "Know nothing about the company"],
        ["Dress appropriately (slightly formal)", "Dress casually or inappropriately"],
        ["Maintain confident eye contact", "Avoid eye contact or stare rudely"],
        ["Listen fully before answering", "Interrupt the interviewer"],
        ["Use STAR method for behavioural questions", "Give vague, unstructured answers"],
        ["Ask intelligent, prepared questions", "Ask 'What does your company do?'"],
        ["Be positive about past employers", "Criticise previous employers"],
        ["Quantify achievements where possible", "Use only vague generalities"],
        ["Send a thank-you email within 24 hours", "Disappear without follow-up"],
        ["Speak at moderate, confident pace", "Rush, mumble, or speak too softly"],
        ["Turn off phone completely", "Have phone ring during interview"],
    ],
    [8.25*cm, 8.25*cm],
    DARK_NAVY
))
story.append(sp(8))

story.append(q_sec_hdr("PRACTICE QUESTIONS — TOPIC 3: Interviews", CRIMSON))
story.append(sp(6))
for item in q_box("1.5 MARKS", EMERALD_M, "What is the STAR method in interview preparation?",
    "STAR is a structured method for answering behavioural interview questions: "
    "S — Situation (the context), T — Task (your specific responsibility), "
    "A — Action (what YOU specifically did), R — Result (the measurable outcome). "
    "It provides complete, evidence-based answers that demonstrate competencies clearly and concisely."):
    story.append(item)

for item in q_box("5 MARKS (300-500 words)", ROYAL_BLUE,
    "What is a Panel Interview? How should a candidate prepare and perform in a panel interview?",
    "<b>Definition:</b> A panel interview involves multiple interviewers (usually 3-7) simultaneously "
    "questioning a single candidate. Panel members may include: HR manager, department head, "
    "technical lead, and a senior executive. This format is common for senior positions, academic "
    "admissions, government roles, and positions where multiple stakeholders must agree on the hire.<br/><br/>"
    "<b>Why Organisations Use Panel Interviews:</b><br/>"
    "1. Multiple perspectives reduce individual bias.<br/>"
    "2. Efficiency — everyone meets the candidate at once.<br/>"
    "3. Tests candidate's ability to manage multiple relationships simultaneously.<br/>  "
    "4. Different panellists evaluate different dimensions — HR evaluates culture fit, "
    "technical lead evaluates skills, manager evaluates leadership potential.<br/><br/>"
    "<b>How to Perform in a Panel Interview:</b><br/>"
    "1. <b>Begin with eye contact for all:</b> When entering, greet every panellist individually. "
    "Learn each name from introductions and use them during answers.<br/>"
    "2. <b>Address the questioner first, then the group:</b> Start your answer looking at the person "
    "who asked, then include all panellists with eye contact during the answer.<br/>"
    "3. <b>Do not favour one panellist:</b> Give equal attention to all — neglecting any panellist "
    "creates a negative impression with that person who may veto your selection.<br/>"
    "4. <b>Manage different question styles:</b> Technical questions get technical answers; "
    "behavioural questions get STAR answers; HR questions get personal/values-based answers.<br/>"
    "5. <b>Maintain composure:</b> Panel settings can feel intimidating. Use slow breathing to remain calm.<br/>"
    "6. <b>Ask questions to the full panel:</b> Direct your closing questions to the group — "
    "'I'd love to hear each of your perspectives on what success looks like in this role.'<br/><br/>"
    "<b>Conclusion:</b> Panel interviews reward poise, preparation, and the ability to connect "
    "with diverse personalities simultaneously — skills that are directly relevant to every "
    "high-level professional role."):
    story.append(item)

for item in q_box("10 MARKS (500-700 words)", AMBER,
    "Classify the types of interviews. Explain the preparation strategies and key techniques for interview success.",
    "<b>Introduction:</b><br/>An interview is a structured formal conversation designed to assess a candidate's "
    "suitability for a specific role or purpose. Interviews are among the most consequential communication events "
    "in a professional's life. Preparation, technique, and performance together determine outcomes.<br/><br/>"
    "<b>Types of Interviews:</b><br/>"
    "1. <b>Structured:</b> Same questions for all; standardised; most reliable and fair.<br/>"
    "2. <b>Unstructured:</b> Conversational; flexible; less comparable.<br/>"
    "3. <b>Semi-Structured:</b> Core questions with flexibility; most common.<br/>"
    "4. <b>Panel:</b> Multiple interviewers; tests composure and multi-stakeholder communication.<br/>"
    "5. <b>Group:</b> Multiple candidates; tests teamwork, leadership, and competitive performance.<br/>"
    "6. <b>Behavioural:</b> 'Tell me about a time...'; past behaviour predicts future performance; "
    "answered with STAR method.<br/>"
    "7. <b>Stress:</b> Deliberate pressure; tests emotional control.<br/>"
    "8. <b>Technical:</b> Domain-specific knowledge assessment.<br/>"
    "9. <b>Case:</b> Business problem analysis on the spot (consulting).<br/>"
    "10. <b>Telephonic/Video:</b> Screening stage; voice clarity and background critical.<br/><br/>"
    "<b>Preparation Strategy — 5 Phases:</b><br/>"
    "<b>Phase 1 — Research:</b> Company (history, products, culture, recent news), role (job description analysis), "
    "industry (trends, challenges), and interviewer (LinkedIn).<br/>"
    "<b>Phase 2 — Self-Analysis:</b> Review résumé fully; identify top 5 strengths with evidence; "
    "prepare 2-3 genuine weaknesses with improvement steps; craft your career narrative.<br/>"
    "<b>Phase 3 — STAR Stories:</b> Prepare 8-10 specific STAR examples covering "
    "leadership, teamwork, conflict, failure, achievement, initiative, and creativity.<br/>"
    "<b>Phase 4 — Practice:</b> Mock interviews; record video; time answers (1.5-2 min each); "
    "practice non-verbals — handshake, posture, eye contact.<br/>"
    "<b>Phase 5 — Logistics:</b> Plan route; arrive 10-15 minutes early; appropriate attire; "
    "bring documents; sleep well; silence phone.<br/><br/>"
    "<b>During the Interview:</b><br/>"
    "Listen fully before answering. Use STAR for behavioural questions. "
    "Speak at moderate pace with clear articulation. Maintain confident eye contact. "
    "Keep answers 1.5-2 minutes. Ask intelligent prepared questions. "
    "Stay positive about past employers. Quantify achievements.<br/><br/>"
    "<b>After the Interview:</b><br/>"
    "Send a professional thank-you email within 24 hours. "
    "Reflect on questions that caught you off-guard — prepare better answers. "
    "Follow up on promised timelines professionally.<br/><br/>"
    "<b>Conclusion:</b><br/>Interview success is 80% preparation and 20% performance under pressure. "
    "Candidates who research thoroughly, prepare specific STAR examples, practise delivery, "
    "and present professionally differentiate themselves from equally qualified competitors."):
    story.append(item)
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — PLANNING & PREPARING PART I: EFFECTIVE RÉSUMÉ
# ══════════════════════════════════════════════════════════════════════════════
story.append(sec_hdr("4","Planning & Preparing (Part I): Effective Résumé","95% — HIGHEST", MAROON))
story.append(sp(8))

story.append(Paragraph("What is a Résumé / CV?", sub1))
story.append(Paragraph(
    "A résumé (French: summary) is a concise, targeted, professional document summarising a candidate's "
    "qualifications, work experience, skills, and achievements for a specific job application. "
    "A Curriculum Vitae (CV — Latin: 'course of life') is a comprehensive academic document listing "
    "all educational qualifications, research, publications, and professional achievements — "
    "typically used for academic, research, and senior government positions.", body))
story.append(sp(5))

story.append(Paragraph("Résumé vs CV — Key Differences:", sub2))
story.append(grid_table(
    ["Feature", "Résumé", "Curriculum Vitae (CV)"],
    [
        ["Length", "1-2 pages (concise)", "2-10+ pages (comprehensive)"],
        ["Purpose", "Job application (private sector)", "Academic/research/government positions"],
        ["Content", "Targeted to specific job", "Complete academic/professional history"],
        ["Customisation", "Customised per application", "Updated but not tailored per application"],
        ["Photos", "Generally excluded (Western norms)", "Sometimes included (varies by country)"],
        ["Used in", "USA, Canada, Australia, private sector globally", "UK, Europe, Academia, Research"],
    ],
    [3.5*cm, 6.5*cm, 6.5*cm]
))
story.append(sp(6))

story.append(Paragraph("Types of Résumé Formats:", sub2))
resume_types = [
    ("1. Chronological Résumé (Most Common)", "Lists work experience in REVERSE chronological order "
     "(most recent first). Best for candidates with strong, consistent, relevant work history. "
     "Preferred by most employers — easy to follow career progression."),
    ("2. Functional / Skills-Based Résumé", "Emphasises SKILLS and competencies rather than chronological "
     "employment history. Best for: career changers, those with employment gaps, or fresh graduates "
     "with limited experience but strong skills. Employers may view it suspiciously if hiding gaps."),
    ("3. Combination / Hybrid Résumé", "Combines chronological and functional formats. "
     "Opens with a prominent skills summary, followed by chronological work history. "
     "Best for: experienced professionals making strategic career changes."),
    ("4. Targeted Résumé", "Customised specifically for ONE job at ONE company. "
     "Every line speaks directly to the job description's requirements. "
     "Most effective but most time-consuming to prepare. Highest success rate."),
    ("5. Infographic / Visual Résumé", "Uses visual design elements — timelines, icons, charts. "
     "Appropriate for creative roles (design, marketing, media). "
     "Avoid for corporate, legal, or technical roles where formality is valued."),
]
for t, d in resume_types:
    story.append(Paragraph(f"&#9654; <b>{t}:</b> {d}", bul))
    story.append(sp(2))
story.append(sp(5))

story.append(Paragraph("Core Components of an Effective Résumé:", sub2))
components = [
    ("1. HEADER / CONTACT INFORMATION",
     "Name (prominent — largest text on page), Professional Email, Phone Number, City/Location, "
     "LinkedIn Profile URL, Portfolio/GitHub (if relevant). "
     "Do NOT include: Date of birth, religion, caste, marital status, or photo (unless required locally)."),
    ("2. PROFESSIONAL SUMMARY / OBJECTIVE",
     "3-4 line paragraph at the top summarising who you are, your key strengths, and your career goal. "
     "Replaces the old-fashioned 'Objective' statement. Should be specific, not generic. "
     "Example: 'Results-driven Data Analyst with 3 years of experience in Python, SQL, and Tableau. "
     "Proven track record of reducing reporting time by 40%. Seeking to leverage analytical expertise "
     "at a growth-stage fintech organisation.'"),
    ("3. WORK EXPERIENCE",
     "Reverse chronological order. For each role include: Job title, Company name, Location, "
     "Dates (Month Year – Month Year), 3-5 bullet points of achievements (not duties). "
     "CRITICAL: Write ACHIEVEMENTS, not job descriptions. "
     "Weak: 'Responsible for managing social media accounts.' "
     "Strong: 'Grew Instagram following by 340% in 6 months, increasing lead generation by 28%.'"),
    ("4. EDUCATION",
     "Reverse chronological. Include: Degree, Institution, Year of completion, Percentage/CGPA. "
     "For recent graduates: can also include relevant coursework, projects, and academic achievements. "
     "For experienced professionals: keep brief — 2-3 lines."),
    ("5. SKILLS",
     "Categorise: Technical Skills (programming languages, tools, software) and "
     "Professional/Soft Skills (project management, communication, leadership). "
     "Match skills directly to the job description — ATS (Applicant Tracking Systems) scan for keywords."),
    ("6. PROJECTS (especially for freshers/students)",
     "Project name, brief description, technologies used, your specific role, and outcomes. "
     "Include a link if the project is online. 3-5 bullet points max per project."),
    ("7. CERTIFICATIONS & ACHIEVEMENTS",
     "Professional certifications (AWS, Google, PMP, CFA), online courses, academic awards, "
     "scholarships, publications, competitions won. Include year and issuing organisation."),
    ("8. EXTRACURRICULAR ACTIVITIES & LEADERSHIP",
     "Club roles, volunteer work, sports achievements at significant levels, cultural activities. "
     "Only include if they demonstrate transferable skills or leadership."),
    ("9. REFERENCES",
     "'References available upon request' — standard closing. Do not list reference names "
     "on the résumé itself; provide when specifically asked."),
]
for title, desc in components:
    story.append(Paragraph(f"<b>{title}</b>", sub3))
    story.append(Paragraph(desc, body))
    story.append(sp(4))

story.append(sp(4))
story.append(tip_box(
    "ATS (Applicant Tracking System) Alert: Most large companies use software to scan résumés "
    "before a human sees them. Use keywords from the job description. Use standard section headings. "
    "Avoid tables, graphics, and columns in ATS-submitted résumés — they confuse the software.", MAROON_L, MAROON, MAROON))
story.append(sp(8))

story.append(q_sec_hdr("PRACTICE QUESTIONS — TOPIC 4: Effective Résumé (Part I)", MAROON))
story.append(sp(6))
for item in q_box("1.5 MARKS", EMERALD_M, "What is the difference between a Résumé and a CV?",
    "A résumé is a concise (1-2 pages) targeted document summarising qualifications and experience "
    "for a specific private-sector job. A CV (Curriculum Vitae) is comprehensive (2-10+ pages), "
    "lists all academic and professional achievements, and is used for academic, research, or government positions. "
    "Résumés are customised per application; CVs are comprehensive historical documents."):
    story.append(item)

for item in q_box("5 MARKS (300-500 words)", ROYAL_BLUE,
    "Explain the types of résumé formats with their advantages and disadvantages.",
    "<b>Introduction:</b> A résumé format determines how information is organised and presented. "
    "Choosing the right format for your career stage and situation significantly impacts success.<br/><br/>"
    "1. <b>Chronological:</b> Most common. Work experience in reverse date order. "
    "Pros: Easy to follow; preferred by employers; shows career progression clearly. "
    "Cons: Exposes employment gaps; may not favour career changers.<br/><br/>"
    "2. <b>Functional / Skills-Based:</b> Leads with skills sections; downplays chronology. "
    "Pros: Hides gaps; highlights competencies; good for career changers. "
    "Cons: Employers may be suspicious; harder to read; not ATS-friendly.<br/><br/>"
    "3. <b>Combination / Hybrid:</b> Opens with skills summary + chronological history. "
    "Pros: Best of both worlds; shows both competencies and timeline. "
    "Cons: Can become long (risk of exceeding 2 pages).<br/><br/>"
    "4. <b>Targeted:</b> Customised specifically for one job/company. Every line matches the job description. "
    "Pros: Highest success rate; directly speaks to employer's needs. "
    "Cons: Time-intensive; different version needed for each application.<br/><br/>"
    "5. <b>Infographic/Visual:</b> Design-forward with timelines, icons, charts. "
    "Pros: Stands out; great for creative roles. "
    "Cons: ATS-unfriendly; inappropriate for formal/corporate roles.<br/><br/>"
    "<b>Recommendation:</b> For most job seekers — Chronological for experienced professionals; "
    "Combination for career changers; Targeted for any role you really want."):
    story.append(item)

for item in q_box("10 MARKS (500-700 words)", AMBER,
    "What is a Résumé? Explain its components in detail with examples.",
    "<b>Introduction:</b><br/>A résumé is a concise, professional marketing document that summarises a "
    "candidate's qualifications, experience, skills, and achievements to persuade an employer to "
    "invite them for an interview. It is the first impression — employers spend an average of "
    "6-7 seconds scanning a résumé before deciding to read further or discard it.<br/><br/>"
    "<b>Components of an Effective Résumé:</b><br/>"
    "<b>1. Header:</b> Full name (prominently displayed), professional email, phone, city, LinkedIn URL. "
    "Avoid: birthdate, photo, religion, marital status.<br/>"
    "<b>2. Professional Summary:</b> 3-4 targeted lines: who you are + key strengths + career goal aligned to the role. "
    "'Results-driven software engineer with 4 years in full-stack development, specialising in React "
    "and Node.js, seeking to leverage expertise in building scalable products at a growth-stage fintech.'<br/>"
    "<b>3. Work Experience:</b> Reverse chronological. Each role: Title | Company | Dates. "
    "3-5 achievement-based bullet points. NEVER list duties — list ACHIEVEMENTS with numbers. "
    "'Reduced API response time by 60% through query optimisation, improving user experience for 50,000+ users.'<br/>"
    "<b>4. Education:</b> Degree | Institution | Year | CGPA/%. Freshers can add projects and relevant coursework. "
    "Experienced professionals keep this brief.<br/>"
    "<b>5. Skills:</b> Technical (Python, SQL, Tableau) and Professional (Project Management, Team Leadership). "
    "Mirror keywords from job description — critical for ATS screening.<br/>"
    "<b>6. Projects:</b> Name | Brief description | Tech used | Your role | Outcome. "
    "Include links where available. Essential for fresh graduates.<br/>"
    "<b>7. Certifications:</b> AWS Certified, Google Analytics, PMP, etc. Include year and issuing body.<br/>"
    "<b>8. Extracurriculars/Leadership:</b> Only if demonstrating transferable skills or leadership. "
    "'President, Entrepreneurship Cell — grew annual membership by 200% and organised 12 speaker events.'<br/>"
    "<b>9. References:</b> 'Available upon request' — never list names on the résumé itself.<br/><br/>"
    "<b>Key Résumé Principles:</b><br/>"
    "1. Length: 1 page for under 5 years experience; 2 pages for 5-15 years; never exceed 2 pages.<br/>"
    "2. Achievement-oriented: Replace all duty statements with measurable achievements.<br/>"
    "3. ATS-optimised: Use keywords from job description; standard section headings; no tables/graphics.<br/>"
    "4. Tailored: Customise for each application — highlight most relevant experience first.<br/>"
    "5. Proofread: Zero spelling, grammar, or formatting errors. One typo = bin.<br/><br/>"
    "<b>Conclusion:</b><br/>A résumé is not a biography — it is a targeted marketing document. "
    "Its only job is to get you an interview. Every line must justify its presence by "
    "communicating your value to the specific employer you are targeting."):
    story.append(item)
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — PLANNING & PREPARING PART II: RÉSUMÉ + COVER LETTER + SAMPLES
# ══════════════════════════════════════════════════════════════════════════════
story.append(sec_hdr("5","Planning & Preparing (Part II): Résumé & Cover Letter","95% — HIGHEST", DEEP_TEAL))
story.append(sp(8))

story.append(Paragraph("A. Résumé Writing Principles (The 10 Golden Rules):", sub2))
resume_rules = [
    ("1. Achieve-Not-Describe", "Every bullet point must be an achievement with a number, not a duty. "
     "Weak: 'Was responsible for sales activities.' "
     "Strong: 'Exceeded quarterly sales target by 34%, generating Rs. 2.1 crore in new revenue.'"),
    ("2. Reverse Chronological Order", "Always list the most recent experience FIRST. "
     "This is what recruiters look for immediately — your current/most recent role."),
    ("3. Use Strong Action Verbs", "Start every bullet with a powerful action verb: "
     "Achieved · Implemented · Developed · Led · Designed · Optimised · Generated · "
     "Streamlined · Launched · Mentored · Negotiated · Increased · Reduced. "
     "Never start with 'Responsible for' or 'Was tasked with.'"),
    ("4. Quantify Everything Possible", "Numbers tell the truth. "
     "'Improved user retention' → 'Improved user retention by 28% in 6 months.' "
     "'Managed a team' → 'Managed a cross-functional team of 12 developers across 3 time zones.'"),
    ("5. Keep it Concise — 1-2 Pages Maximum", "1 page for under 5 years experience. "
     "2 pages for 5+ years. NEVER submit a 3-page résumé for private sector roles. "
     "If you cannot edit it down, you have not thought hard enough about what matters."),
    ("6. Customise for Every Application", "Read the job description carefully. "
     "Identify the top 10 keywords and requirements. Ensure your résumé addresses each one. "
     "A generic résumé is a less effective résumé."),
    ("7. ATS Optimisation", "Use keywords from the job description verbatim. "
     "Use standard section headings (Work Experience, not 'My Journey'). "
     "Use simple formatting — no tables, columns, text boxes, headers/footers, or images for ATS submissions."),
    ("8. Zero Errors Policy", "One spelling mistake or grammatical error in a résumé signals "
     "carelessness, lack of attention to detail, and poor communication skills simultaneously. "
     "Proofread manually; use grammar tools; have a second person review."),
    ("9. Professional Formatting", "Consistent font (Calibri, Garamond, or Arial); 10-12pt body text; "
     "subtle use of bold for headings; clean white space; 1-inch margins. "
     "PDF format for submission (preserves formatting across devices)."),
    ("10. Be Honest", "Never lie on your résumé — exaggeration of qualifications, "
     "fake degrees, or inflated job titles are grounds for immediate termination and legal action if discovered."),
]
for t, d in resume_rules:
    story.append(Paragraph(f"<b>{t}:</b> {d}", bul))
    story.append(sp(3))
story.append(sp(5))

story.append(Paragraph("Common Résumé Mistakes to Avoid:", sub2))
mistakes = [
    "Using a generic objective statement ('To obtain a challenging position that utilises my skills') — says nothing.",
    "Listing duties instead of achievements — tells employers WHAT you did, not HOW WELL you did it.",
    "Including irrelevant personal information (hobbies like 'watching TV', 'cooking').",
    "Using fancy templates with headers, footers, columns, and graphics — ATS cannot read them.",
    "Submitting the same résumé for every job without customising.",
    "Spelling errors, grammar mistakes, and inconsistent formatting.",
    "Using passive voice ('Was responsible for') instead of active verbs ('Led', 'Generated').",
    "Including outdated technology or skills (software not used in 10 years).",
    "Overly long (3+ pages for entry-level) or too short (half-page hiding experience).",
    "Not including a LinkedIn profile URL or keeping LinkedIn profile inconsistent with résumé.",
    "Using unprofessional email address (e.g., coolguy99@gmail.com).",
    "Including references on the résumé itself.",
]
for m in mistakes:
    story.append(Paragraph(f"&#9888; {m}", bul))
story.append(sp(6))

story.append(Paragraph("B. COVER LETTER — The Essential Companion:", sub2))
story.append(Paragraph(
    "A cover letter is a 1-page formal letter submitted with a résumé, introducing the candidate and "
    "making a personalised case for their candidacy. While the résumé lists WHAT you have done, "
    "the cover letter explains WHY you want this role and HOW your experience directly serves "
    "the employer's needs. A strong cover letter can get a résumé read; "
    "a weak one can get both rejected.", body))
story.append(sp(5))

story.append(Paragraph("Cover Letter Structure:", sub2))
cl_structure = [
    ("Paragraph 1 — Opening Hook", "State the specific role you are applying for (and source), "
     "and immediately give the most compelling reason they should continue reading. "
     "Do NOT start with 'I am writing to apply for...'. "
     "Example: 'When I increased customer retention by 47% using data-driven personalisation at TechStartup, "
     "I realised my skills were built for a company like yours — one that uses analytics to create "
     "genuinely customer-centric products.'"),
    ("Paragraph 2 — Your Value Proposition", "Connect your 2-3 most relevant achievements directly to "
     "the job requirements. This is where you customise most heavily. "
     "Mirror the language of the job description. Show them you have done your research."),
    ("Paragraph 3 — Why THIS Company", "Demonstrate company-specific knowledge — mention their products, "
     "mission, culture, recent news, or specific team. Show this is not a generic application. "
     "'Having followed your product roadmap since Series B, I particularly admire your approach to...'"),
    ("Paragraph 4 — Confident Close", "Reiterate your enthusiasm. Express confidence in your fit. "
     "Request an interview specifically. Provide contact details. "
     "'I would welcome the opportunity to discuss how my background in [X] could contribute to [specific goal]. "
     "I am available for an interview at your convenience and can be reached at [phone] or [email].'"),
]
for t, d in cl_structure:
    story.append(Paragraph(f"<b>{t}:</b> {d}", bul))
    story.append(sp(3))
story.append(sp(6))

story.append(Paragraph("C. SAMPLE FULL RÉSUMÉ:", sub2))
story.append(sp(4))
story.append(resume_box([
    "## ARJUN MEHTA",
    "# +91-98765-43210 | arjun.mehta@email.com | linkedin.com/in/arjunmehta | Bengaluru, Karnataka",
    "---",
    "# PROFESSIONAL SUMMARY",
    "Results-driven Software Engineer with 3+ years building scalable web applications",
    "using React, Node.js, and PostgreSQL. Reduced API latency by 60% at current role.",
    "Seeking to leverage full-stack expertise at a growth-stage product company.",
    "---",
    "# WORK EXPERIENCE",
    "Software Engineer | InnoTech Solutions Pvt. Ltd. | Bengaluru | Aug 2022 – Present",
    "  • Reduced API response time by 60% through database query optimisation,",
    "    improving UX for 80,000+ active users",
    "  • Led migration of legacy monolith to microservices architecture, cutting",
    "    deployment time from 4 hours to 12 minutes",
    "  • Mentored 3 junior developers, reducing their onboarding time by 50%",
    "  • Developed real-time notification system handling 500,000+ daily events",
    "",
    "Junior Developer (Internship) | StartupX | Mumbai | Jan 2022 – Jul 2022",
    "  • Built and deployed 4 REST APIs using Node.js and Express",
    "  • Automated monthly reporting, saving 15 hours of manual work per month",
    "---",
    "# EDUCATION",
    "B.Tech in Computer Science Engineering",
    "National Institute of Technology, Surathkal | 2022 | CGPA: 8.9/10",
    "---",
    "# TECHNICAL SKILLS",
    "Languages: JavaScript, Python, SQL, TypeScript",
    "Frameworks: React, Node.js, Express, Django",
    "Databases: PostgreSQL, MongoDB, Redis",
    "Tools: Docker, Git, AWS (EC2, S3, Lambda), Figma",
    "---",
    "# KEY PROJECTS",
    "EduTrack — AI-Powered Learning Platform (github.com/arjun/edutrack)",
    "  • Built adaptive learning recommendation engine using Python + ML",
    "  • Deployed on AWS, served 2,000+ beta users, 92% positive feedback",
    "---",
    "# CERTIFICATIONS",
    "AWS Certified Solutions Architect – Associate | Amazon | 2024",
    "Google Professional Data Engineer | Google | 2023",
    "---",
    "# ACHIEVEMENTS",
    "  • Winner, Smart India Hackathon 2022 (National Level, 10,000+ participants)",
    "  • Published: 'Optimising React Performance' – Dev.to (12,000+ reads)",
    "",
    "References available upon request.",
], "SAMPLE — COMPLETE CHRONOLOGICAL RÉSUMÉ (1 Page)"))
story.append(sp(8))

story.append(Paragraph("D. SAMPLE COVER LETTER:", sub2))
story.append(sp(4))
story.append(resume_box([
    "## ARJUN MEHTA",
    "# +91-98765-43210 | arjun.mehta@email.com | Bengaluru, Karnataka",
    "---",
    "22 May 2025",
    "",
    "Ms. Divya Krishnan",
    "Head of Engineering",
    "FinEdge Technologies Pvt. Ltd.",
    "14th Floor, Embassy Tech Village, Bengaluru - 560 103",
    "",
    "Subject: Application for Software Engineer (Product) — Ref: FE/ENG/2025/47",
    "",
    "Dear Ms. Krishnan,",
    "",
    "When I led the migration of InnoTech's entire backend from a monolith to",
    "microservices — cutting deployment time from 4 hours to 12 minutes — I",
    "understood viscerally what it means to build systems that scale. That same",
    "challenge is exactly what drives FinEdge's mission, and it is why I am",
    "writing to you today.",
    "",
    "Over the past 3 years at InnoTech Solutions, I have built production-grade",
    "systems serving 80,000+ users, reduced API latency by 60% through strategic",
    "query optimisation, and developed a real-time event pipeline processing",
    "500,000+ daily notifications. My experience directly maps to the core",
    "requirements in your job description: distributed systems, API design,",
    "and full-stack React/Node.js development.",
    "",
    "What draws me specifically to FinEdge is your commitment to financial",
    "inclusion for Tier 2 and 3 India — a mission I find deeply meaningful.",
    "Your recent Series B funding news and the product roadmap shared at the",
    "Delhi FinTech Summit suggest an exciting growth phase, and I am eager",
    "to contribute during this critical scaling period.",
    "",
    "I would welcome the opportunity to discuss how my background could",
    "strengthen your engineering team. I am available for an interview at",
    "your convenience and can be reached at +91-98765-43210.",
    "",
    "Thank you for your time and consideration.",
    "",
    "Yours sincerely,",
    "",
    "[Signature]",
    "Arjun Mehta",
    "",
    "Enc: 1. Résumé  2. AWS Certification  3. Google Cloud Certification",
], "SAMPLE — COVER LETTER (Full Block Style)"))
story.append(sp(8))

story.append(q_sec_hdr("PRACTICE QUESTIONS — TOPIC 5: Résumé Part II & Cover Letter", DEEP_TEAL))
story.append(sp(6))
for item in q_box("1.5 MARKS", EMERALD_M, "What is a Cover Letter?",
    "A cover letter is a 1-page formal letter submitted alongside a résumé, introducing the applicant "
    "and making a personalised case for their candidacy. While the résumé lists achievements, "
    "the cover letter explains WHY the candidate wants this specific role and HOW their experience "
    "serves the employer's specific needs. A strong cover letter significantly improves interview chances."):
    story.append(item)

for item in q_box("5 MARKS (300-500 words)", ROYAL_BLUE,
    "Explain the principles of effective résumé writing.",
    "<b>Introduction:</b> A résumé is a professional marketing document whose only purpose is to earn "
    "an interview. Effective résumé writing follows 10 golden principles that maximise impact.<br/><br/>"
    "1. <b>Achievement Over Description:</b> Every bullet point must be an achievement, not a duty. "
    "Use numbers to prove impact: '34% sales increase', 'managed 12-person team'.<br/>"
    "2. <b>Strong Action Verbs:</b> Start every bullet with power verbs: Led, Developed, "
    "Generated, Optimised, Launched. Never 'Responsible for.'<br/>"
    "3. <b>Quantify Everything:</b> Numbers make achievements concrete and credible. "
    "'Improved performance' vs 'Improved query performance by 60%.'<br/>"
    "4. <b>Customise Per Application:</b> Tailor every résumé to match the job description. "
    "Use their keywords. Address their specific requirements.<br/>"
    "5. <b>ATS Optimisation:</b> Use standard headings; no tables or graphics; "
    "include job description keywords verbatim.<br/>"
    "6. <b>Conciseness:</b> 1 page under 5 years; 2 pages for more. Ruthlessly edit.<br/>"
    "7. <b>Professional Formatting:</b> Clean font (Calibri/Arial); 10-12pt; "
    "consistent spacing; white space; PDF format.<br/>"
    "8. <b>Zero Errors:</b> One typo signals carelessness. Proofread 3 times; "
    "use grammar tools; have someone else review.<br/>"
    "9. <b>Reverse Chronological:</b> Most recent experience always first.<br/>"
    "10. <b>Honesty:</b> Never fabricate — dishonesty discovered in background checks "
    "ends careers.<br/><br/>"
    "<b>Conclusion:</b> A résumé is not a historical document — it is a strategic persuasion tool. "
    "Every line must justify its presence by communicating specific value to the specific employer."):
    story.append(item)

for item in q_box("15 MARKS (700-1000 words)", CRIMSON,
    "Discuss comprehensively the planning and preparation of an effective résumé and cover letter. Include sample content.",
    "<b>Introduction:</b><br/>"
    "The résumé and cover letter together form the most critical documents in any professional's career. "
    "They are the gatekeepers — every opportunity begins with them. Research shows recruiters spend "
    "an average of 6-7 seconds on initial résumé review. The goal: make those seconds count by "
    "immediately communicating your most relevant value.<br/><br/>"
    "<b>PART 1 — EFFECTIVE RÉSUMÉ:</b><br/>"
    "<b>Definition:</b> A résumé is a concise (1-2 page), targeted professional document summarising "
    "qualifications, experience, skills, and achievements for a specific job application.<br/><br/>"
    "<b>Types:</b> Chronological (most common; reverse date order), Functional (skills-focused; "
    "good for gaps/career change), Combination (hybrid; skills + chronology), and Targeted "
    "(customised for one specific job — highest effectiveness).<br/><br/>"
    "<b>Essential Components:</b><br/>"
    "1. <b>Header:</b> Name, email, phone, LinkedIn, city. No photo, birthdate, or religion.<br/>"
    "2. <b>Professional Summary:</b> 3-4 lines: who you are + key quantified achievement + goal "
    "aligned to role. Example: 'Marketing Manager with 7 years building B2B SaaS brands. "
    "Led campaigns generating $3.2M pipeline. Seeking VP Marketing role at Series B+ company.'<br/>"
    "3. <b>Work Experience:</b> Reverse chronological. Achievement bullets with numbers. "
    "Action verb starts. Example: 'Grew LinkedIn following from 2K to 45K in 8 months, "
    "driving 38% increase in inbound leads.'<br/>"
    "4. <b>Education:</b> Degree, institution, year, CGPA. Fresh graduates: add projects.<br/>"
    "5. <b>Skills:</b> Technical and professional. Mirror job description keywords for ATS.<br/>"
    "6. <b>Projects/Certifications/Achievements:</b> Relevant, quantified, recent.<br/><br/>"
    "<b>10 Golden Principles:</b><br/>"
    "1. Achievements, not duties. 2. Action verbs every bullet. 3. Quantify everything. "
    "4. Customise per application. 5. ATS-optimised (keywords, standard headings). "
    "6. 1-2 pages maximum. 7. Professional formatting (Calibri/Arial, 10-12pt, PDF). "
    "8. Zero errors policy. 9. Reverse chronological. 10. Absolute honesty.<br/><br/>"
    "<b>PART 2 — EFFECTIVE COVER LETTER:</b><br/>"
    "<b>Definition:</b> A 1-page formal letter that introduces you, explains why you want this "
    "specific role, and connects your experience directly to the employer's needs. "
    "The résumé shows WHAT you've done; the cover letter shows WHY you're the right person for this role.<br/><br/>"
    "<b>Structure (4 Paragraphs):</b><br/>"
    "1. <b>Opening Hook:</b> Start with your most compelling achievement relevant to the role. "
    "NOT 'I am writing to apply for...' Instead: 'When I generated Rs. 3.5 crore in new business "
    "within 6 months using consultative selling, I discovered my strength lies in complex B2B sales — "
    "exactly what your Regional Sales Manager role demands.'<br/>"
    "2. <b>Value Proposition:</b> Connect 2-3 achievements directly to the job description "
    "requirements. Use the employer's language. Mirror their keywords.<br/>"
    "3. <b>Company-Specific Passion:</b> Mention their products, mission, culture, or recent news. "
    "Show this is not a generic copy-paste application.<br/>"
    "4. <b>Confident Close:</b> Request an interview. Provide contact. Express enthusiasm.<br/><br/>"
    "<b>Cover Letter Principles:</b><br/>"
    "1. One page maximum — ideally 3-4 paragraphs.<br/>"
    "2. Never repeat the résumé — add context and personality to achievements.<br/>"
    "3. Research the company; show it.<br/>"
    "4. Use the interviewer's name ('Dear Ms. Sharma') not 'Dear Sir/Madam'.<br/>"
    "5. Professional business letter format (Full Block or Modified Block).<br/><br/>"
    "<b>Common Mistakes in Both Documents:</b><br/>"
    "Using duties not achievements; generic content; typos; wrong company name (critical error); "
    "unprofessional email address; no quantification; inconsistency between résumé and LinkedIn.<br/><br/>"
    "<b>Conclusion:</b><br/>"
    "The résumé and cover letter are the most edited, most strategic, and most consequential documents "
    "a professional will write. They deserve proportionally more time and effort than they typically "
    "receive. The investment is simple: a great résumé and cover letter open doors; "
    "weak ones keep doors permanently closed. Write them as if your career depends on them — because it does."):
    story.append(item)
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# QUICK REVISION PAGE
# ══════════════════════════════════════════════════════════════════════════════
story.append(ch_banner("&#9733;  QUICK REVISION: MODULE 4 AT A GLANCE  &#9733;", DARK_NAVY))
story.append(sp(10))

rev = [
    [Paragraph("<b>Topic</b>", S("TH_R4", fontSize=9.5, fontName="Helvetica-Bold",
                                  textColor=WHITE, alignment=TA_CENTER, leading=13)),
     Paragraph("<b>Key Must-Know Points</b>",
               S("TH_R4B", fontSize=9.5, fontName="Helvetica-Bold",
                 textColor=WHITE, alignment=TA_CENTER, leading=13)),
     Paragraph("<b>%</b>", S("TH_R4C", fontSize=9.5, fontName="Helvetica-Bold",
                               textColor=WHITE, alignment=TA_CENTER, leading=13))],

    ["Effective Presentations",
     "PPPF Framework. 10 Elements. 6x6 Rule. 10-20-30 Rule. 3-Part Structure (15-70-15%)",
     "90%"],
    ["Audience Engagement",
     "Rhetorical questions, think-pair-share, polls, demos, storytelling, strategic pause",
     "88%"],
    ["Visual Aid Design",
     "6x6. 24pt min. 1 idea/slide. Visuals>text. Test tech. Label all charts. PDF not PPT",
     "85%"],
    ["Welcome Speech",
     "Greet→Introduce occasion→Acknowledge guests→Programme→Gratitude→Welcome. 2-3 min",
     "88%"],
    ["Vote of Thanks",
     "Thank chief guest→speakers→organisers→sponsors→audience. Name specifically. 2-3 min",
     "88%"],
    ["Farewell Speech",
     "Memory→Contributions→Impact→Wishes→Assurance of being remembered. Warm+hopeful",
     "82%"],
    ["Toast / Eulogy / Award",
     "Toast: 30-90 secs, raise glasses. Eulogy: dignified, 3-5 min. Award: humble, thank specifically",
     "80%"],
    ["Interview Types",
     "Structured/Unstructured/Panel/Group/Behavioural/Stress/Case/Technical/Video",
     "92%"],
    ["STAR Method",
     "Situation→Task→Action→Result. Use for ALL behavioural ('Tell me about a time...') questions",
     "95%"],
    ["Interview Dos",
     "Research company. STAR answers. Arrive early. Ask questions. Thank-you email within 24 hrs",
     "90%"],
    ["Interview Don'ts",
     "Criticise past employers. Ask salary first. Arrive late. Phone rings. Generic answers",
     "88%"],
    ["Résumé vs CV",
     "Résumé: 1-2 pg, targeted, private sector. CV: comprehensive, academic/government/research",
     "90%"],
    ["Résumé Types",
     "Chronological (most common). Functional (career change/gaps). Combination. Targeted (best)",
     "88%"],
    ["Résumé Components",
     "Header→Summary→Experience→Education→Skills→Projects→Certifications→References",
     "95%"],
    ["Résumé Golden Rules",
     "Achievements not duties. Quantify. Action verbs. ATS-optimised. 1-2 pages. Zero errors",
     "95%"],
    ["Cover Letter Structure",
     "Hook→Value Proposition→Why this company→Confident close. 1 page. Name-specific. No repeat",
     "92%"],
]
rev_t = Table(rev, colWidths=[4*cm, 10.5*cm, 2*cm])
rev_t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0), DARK_NAVY),
    ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LIGHT_BLUE]),
    ("BOX",(0,0),(-1,-1),1.5, ROYAL_BLUE),
    ("INNERGRID",(0,0),(-1,-1),0.4, SKY),
    ("FONTNAME",(0,1),(-1,-1),"Helvetica"),("FONTSIZE",(0,0),(-1,-1),8.5),
    ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("ALIGN",(2,0),(2,-1),"CENTER"),
]))
story.append(rev_t)
story.append(sp(12))

closing_d = [[Paragraph(
    "<b>FINAL EXAM STRATEGY — MODULE 4 &#9733;</b><br/>"
    "&#9654; <b>Résumé Question:</b> Always describe ALL components (9 sections) + write sample content. "
    "Use achievement bullets with numbers. Differentiate from CV.<br/>"
    "&#9654; <b>Interview Question:</b> Classify types (10+) + explain STAR method with example + "
    "write Dos &amp; Don'ts as a table for structured answers.<br/>"
    "&#9654; <b>Speeches:</b> Know all 7 types with purpose, tone, length, and key elements. "
    "Be ready to write a sample welcome speech or vote of thanks in full.<br/>"
    "&#9654; <b>Effective Presentations:</b> 10 elements + 6x6 Rule + 10-20-30 Rule + "
    "3-part structure (15%-70%-15%) = complete answer.<br/>"
    "&#9654; <b>Cover Letter:</b> 4-paragraph structure + hook opening + company-specific para = full marks.",
    S("CLO4", fontSize=10.5, textColor=DARK_NAVY, fontName="Helvetica",
      alignment=TA_LEFT, leading=17))]]
closing_t = Table(closing_d, colWidths=[17*cm])
closing_t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1), GOLD_L),
    ("BOX",(0,0),(-1,-1),2, GOLD),
    ("TOPPADDING",(0,0),(-1,-1),14),("BOTTOMPADDING",(0,0),(-1,-1),14),
    ("LEFTPADDING",(0,0),(-1,-1),16),("RIGHTPADDING",(0,0),(-1,-1),16),
]))
story.append(closing_t)
story.append(sp(10))

final_wish = [[Paragraph(
    "&#9733; ALL THE VERY BEST FOR YOUR OEC-CS-601(I) FINAL EXAM! &#9733;<br/>"
    "You've got this — Study Smart, Revise Often, Write Confidently!",
    S("FW", fontSize=14, textColor=WHITE, fontName="Helvetica-Bold",
      alignment=TA_CENTER, leading=22))]]
fw_t = Table(final_wish, colWidths=[17*cm])
fw_t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1), DARK_NAVY),
    ("TOPPADDING",(0,0),(-1,-1),16),("BOTTOMPADDING",(0,0),(-1,-1),16),
    ("LEFTPADDING",(0,0),(-1,-1),16),("RIGHTPADDING",(0,0),(-1,-1),16),
]))
story.append(fw_t)

# ── BUILD ──────────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT_PATH,
    pagesize=A4,
    leftMargin=1.8*cm, rightMargin=1.8*cm,
    topMargin=2*cm, bottomMargin=2.2*cm,
    title="Soft Skills Module 4 — Presentations, Interviews & Résumé",
    author="OEC-CS-601(I)",
)
doc.build(story, canvasmaker=NumberedCanvas)
print(f"PDF created: {OUTPUT_PATH}")