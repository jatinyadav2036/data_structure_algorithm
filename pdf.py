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

OUTPUT_PATH = "PYQ_Master_Answers_OEC_CS_601.pdf"

# ── COLORS ─────────────────────────────────────────────────────────────────────
DARK        = colors.HexColor("#0a1628")
NAVY        = colors.HexColor("#1a3a5c")
BLUE        = colors.HexColor("#1565c0")
BLUE_L      = colors.HexColor("#e3f2fd")
SKY         = colors.HexColor("#bbdefb")
TEAL        = colors.HexColor("#00695c")
TEAL_L      = colors.HexColor("#e0f2f1")
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
GRAY_M      = colors.HexColor("#757575")
GRAY_L      = colors.HexColor("#f5f5f5")
WHITE       = colors.white
BLACK       = colors.black
DEEP_GREEN  = colors.HexColor("#33691e")
ROSE        = colors.HexColor("#c62828")
SLATE       = colors.HexColor("#37474f")
OLIVE       = colors.HexColor("#558b2f")

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

def sp(n=6): return Spacer(1, n)

def banner(text, bg=DARK, fs=15):
    d = [[Paragraph(text, S("BN", fontSize=fs, textColor=WHITE,
                            fontName="Helvetica-Bold", alignment=TA_LEFT, leading=fs+5))]]
    t = Table(d, colWidths=[17*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), bg),
        ("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10),
        ("LEFTPADDING",(0,0),(-1,-1),14),("RIGHTPADDING",(0,0),(-1,-1),14),
    ]))
    return t

def paper_banner(text, year, marks_info):
    d = [[
        Paragraph(f"<b>{text}</b>",
                  S("PB1", fontSize=13, textColor=WHITE, fontName="Helvetica-Bold", leading=18)),
        Paragraph(f"<b>{year}</b><br/>{marks_info}",
                  S("PB2", fontSize=10, textColor=colors.HexColor("#ffe0b2"),
                    fontName="Helvetica", leading=14, alignment=TA_RIGHT))
    ]]
    t = Table(d, colWidths=[12*cm, 5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), AMBER),
        ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),12),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    return t

def q_block_a(q_num, question, answer, appears_in=""):
    # Part A question block - 1.5 marks
    hdr_data = [[
        Paragraph(f"<b>Q{q_num}. {question}</b>",
                  S("QAH", fontSize=10.5, textColor=WHITE, fontName="Helvetica-Bold", leading=14)),
        Paragraph(f"1.5 Marks | ~50 words",
                  S("QAM", fontSize=9, textColor=colors.HexColor("#ffe082"),
                    fontName="Helvetica", alignment=TA_RIGHT, leading=12))
    ]]
    ht = Table(hdr_data, colWidths=[13*cm, 4*cm])
    ht.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), NAVY),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    if appears_in:
        app = Paragraph(f"<i>&#128197; Asked in: {appears_in}</i>",
                        S("APP", fontSize=8.5, textColor=GRAY_M, fontName="Helvetica-Oblique",
                          leading=12, leftIndent=10, spaceBefore=2))
    ans_para = Paragraph(answer,
                         S("ANS_A", fontSize=10, textColor=BLACK, fontName="Helvetica",
                           leading=14, alignment=TA_JUSTIFY, leftIndent=10, rightIndent=10,
                           spaceBefore=5, spaceAfter=5))
    result = [ht]
    if appears_in:
        result.append(app)
    result.append(ans_para)
    result.append(sp(6))
    return result

def q_block_b(q_num, question, topic_bg, full_answer, marks, color=BLUE, appears_in=""):
    # Part B question block
    hdr_data = [[
        Paragraph(f"<b>Q{q_num}.</b> {question}",
                  S("QBH", fontSize=11, textColor=WHITE, fontName="Helvetica-Bold", leading=15)),
        Paragraph(f"<b>{marks} Marks</b>",
                  S("QBM", fontSize=10, textColor=WHITE, fontName="Helvetica-Bold",
                    alignment=TA_RIGHT, leading=13))
    ]]
    ht = Table(hdr_data, colWidths=[13.5*cm, 3*cm])
    ht.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), color),
        ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    if appears_in:
        app = Paragraph(f"<i>&#128197; Asked in: {appears_in}</i>",
                        S("APP2", fontSize=8.5, textColor=GRAY_M, fontName="Helvetica-Oblique",
                          leading=12, leftIndent=10, spaceBefore=2))
    # Topic background box
    bg_data = [[Paragraph(f"<b>&#128218; Topic Background:</b> {topic_bg}",
                          S("TBG", fontSize=10, textColor=INDIGO, fontName="Helvetica",
                            leading=14, alignment=TA_JUSTIFY))]]
    bg_t = Table(bg_data, colWidths=[16.5*cm])
    bg_t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), INDIGO_L),
        ("BOX",(0,0),(-1,-1),1, INDIGO),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
    ]))
    # Answer
    ans_para = Paragraph(full_answer,
                         S("ANS_B", fontSize=10, textColor=BLACK, fontName="Helvetica",
                           leading=15, alignment=TA_JUSTIFY,
                           leftIndent=10, rightIndent=10, spaceBefore=5, spaceAfter=5))
    result = [ht]
    if appears_in:
        result.append(app)
    result += [sp(4), bg_t, sp(4), ans_para, sp(8)]
    return result

def tip_box(text):
    d = [[Paragraph(f"<b>&#9733; EXAM TIP:</b> {text}",
                    S("TIP", fontSize=10, textColor=PURPLE, fontName="Helvetica",
                      leading=14, alignment=TA_JUSTIFY))]]
    t = Table(d, colWidths=[16.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), PURPLE_L),
        ("BOX",(0,0),(-1,-1),1.5, PURPLE_M),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
    ]))
    return t

def sample_box(lines, title="SAMPLE"):
    rows = [[Paragraph(title, S("SBT", fontSize=10, textColor=WHITE,
                                fontName="Helvetica-Bold", alignment=TA_CENTER, leading=13))]]
    for line in lines:
        if line == "---":
            rows.append([HRFlowable(width="95%", thickness=0.5, color=GRAY_M)])
        elif line.startswith("##"):
            rows.append([Paragraph(line[2:], S("SBH", fontSize=11, textColor=DARK,
                                               fontName="Helvetica-Bold", leading=14))])
        elif line.startswith("#"):
            rows.append([Paragraph(line[1:], S("SBS", fontSize=10, textColor=TEAL,
                                               fontName="Helvetica-Bold", leading=13))])
        else:
            rows.append([Paragraph(line, S("SBL", fontSize=9.5, textColor=BLACK,
                                          fontName="Courier", leading=13))])
    t = Table(rows, colWidths=[16.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,0), TEAL),
        ("BACKGROUND",(0,1),(-1,-1), GRAY_L),
        ("BOX",(0,0),(-1,-1),1.5, TEAL),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),14),("RIGHTPADDING",(0,0),(-1,-1),14),
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
        self.drawString(1.5*cm, 1.2*cm, "OEC-CS-601(I) | PYQ Master Answers — All Papers (2022–2025)")
        self.setStrokeColor(BLUE_L); self.setLineWidth(0.5)
        self.line(1.5*cm, 1.5*cm, A4[0]-1.5*cm, 1.5*cm)

# ══════════════════════════════════════════════════════════════════════════════
story = []

# ── COVER ────────────────────────────────────────────────────────────────────
cover_rows = [
    [sp(10)],
    [Paragraph("&#9733; OEC-CS-601(I) | B.Tech. VI Semester &#9733;",
               S("CV1", fontSize=12, textColor=SKY, fontName="Helvetica-Bold",
                 alignment=TA_CENTER, leading=18))],
    [sp(6)],
    [Paragraph("SOFT SKILLS &amp;", S("CV2", fontSize=32, textColor=WHITE,
               fontName="Helvetica-Bold", alignment=TA_CENTER, leading=38))],
    [Paragraph("INTERPERSONAL COMMUNICATION",
               S("CV3", fontSize=17, textColor=colors.HexColor("#ffe0b2"),
                 fontName="Helvetica-Bold", alignment=TA_CENTER, leading=24))],
    [sp(8)],
    [HRFlowable(width="70%", thickness=2.5, color=GOLD, spaceAfter=8, spaceBefore=4)],
    [Paragraph("PREVIOUS YEAR QUESTION PAPERS",
               S("CV4", fontSize=15, textColor=GOLD, fontName="Helvetica-Bold",
                 alignment=TA_CENTER, leading=20))],
    [Paragraph("COMPLETE ANSWERS + TOPIC EXPLANATIONS",
               S("CV5", fontSize=13, textColor=GOLD, fontName="Helvetica-Bold",
                 alignment=TA_CENTER, leading=18))],
    [sp(10)],
    [Paragraph("May 2025  |  May 2024  |  May 2023  |  Aug/Sep 2022",
               S("CV6", fontSize=12, textColor=WHITE, fontName="Helvetica",
                 alignment=TA_CENTER, leading=16))],
    [sp(6)],
    [Paragraph("Every Question Answered · Topic Background · Mark-Limit Compliant",
               S("CV7", fontSize=11, textColor=colors.HexColor("#ffe0b2"),
                 fontName="Helvetica", alignment=TA_CENTER, leading=16))],
    [sp(6)],
    [Paragraph("Max Marks: 75 | Time: 3 Hours | Part A: 10×1.5=15 | Part B: 4×15=60",
               S("CV8", fontSize=10, textColor=WHITE, fontName="Helvetica",
                 alignment=TA_CENTER, leading=14))],
    [sp(12)],
]
cov = Table(cover_rows, colWidths=[17*cm])
cov.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1), DARK),
    ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
    ("LEFTPADDING",(0,0),(-1,-1),16),("RIGHTPADDING",(0,0),(-1,-1),16),
]))
story.append(cov)
story.append(sp(16))

# Exam pattern box
ep_data = [
    [Paragraph("<b>EXAM PATTERN ANALYSIS</b>",
               S("EP0", fontSize=12, textColor=DARK, fontName="Helvetica-Bold",
                 alignment=TA_CENTER, leading=16))],
    [Paragraph(
        "<b>Part A:</b> 10 questions × 1.5 marks = 15 marks (ALL COMPULSORY, ~50 words each)<br/>"
        "<b>Part B:</b> Answer ANY 4 questions from 6 (Marks vary: 5+10, 5+5+5, 15, 10+5 etc.) = 60 marks<br/>"
        "<b>Total: 75 marks | Time: 3 Hours</b><br/><br/>"
        "<b>Most Repeated Topics:</b> Business Letters · Report Writing · Presentation · "
        "Resume + Cover Letter · 7 C's · Listening · Leadership · EQ · Negotiation · Meta-Communication",
        S("EP1", fontSize=10, textColor=BLACK, fontName="Helvetica",
          leading=15, alignment=TA_JUSTIFY))],
]
ep_t = Table(ep_data, colWidths=[17*cm])
ep_t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(0,0), BLUE_L),("BACKGROUND",(0,1),(0,1), WHITE),
    ("BOX",(0,0),(-1,-1),2, BLUE),("LINEBELOW",(0,0),(0,0),1.5, BLUE),
    ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),
    ("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),12),
]))
story.append(ep_t)
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# PART A — ALL 1.5-MARK QUESTIONS
# ══════════════════════════════════════════════════════════════════════════════
story.append(banner("PART A — ALL 1.5-MARK SHORT ANSWER QUESTIONS", DARK))
story.append(sp(6))
story.append(Paragraph(
    "Each answer below is approximately 50 words — the exact requirement for 1.5-mark Part A questions. "
    "Every unique Part A question from all 4 papers is covered here.",
    S("NOTE", fontSize=10, textColor=GRAY_M, fontName="Helvetica-Oblique",
      leading=14, spaceBefore=4, spaceAfter=8)))

# ── NEGOTIATION SKILLS ─────────────────────────────────────────────────────
for x in q_block_a("1", "What is Negotiation Skill?",
    "Negotiation skill is the ability to communicate, discuss, and reach a mutually acceptable agreement "
    "between two or more parties with different interests or needs. It involves active listening, empathy, "
    "persuasion, and problem-solving. Key concepts include BATNA (Best Alternative To a Negotiated Agreement), "
    "ZOPA (Zone of Possible Agreement), and the principle of focusing on interests rather than positions.",
    "May 2025, Aug/Sep 2022, May 2024"): story.append(x)

# ── COMPLEX PROBLEM SOLVING ───────────────────────────────────────────────
for x in q_block_a("2", "What is Complex Problem Solving?",
    "Complex problem solving is the ability to identify, analyse, and resolve multifaceted problems that "
    "cannot be solved by simple, routine methods. It requires critical thinking, creativity, logical reasoning, "
    "data analysis, and decision-making under uncertainty. Steps include: Define problem → Gather data → "
    "Generate solutions → Evaluate → Implement → Review. It is ranked among the top future workplace skills by the WEF.",
    "May 2025"): story.append(x)

# ── INTERVIEWER VS INTERVIEWEE ─────────────────────────────────────────────
for x in q_block_a("3", "How is an Interviewer Different from an Interviewee?",
    "The <b>interviewer</b> is the person who conducts the interview — asks questions, evaluates responses, "
    "and represents the organisation. The <b>interviewee</b> is the candidate who answers questions and seeks "
    "the position. The interviewer has power and control over the process; the interviewee must prepare "
    "answers, demonstrate competence, and persuade the interviewer of their suitability for the role.",
    "May 2025, Aug/Sep 2022"): story.append(x)

# ── EMOTIONAL INTELLIGENCE ────────────────────────────────────────────────
for x in q_block_a("4", "What is Emotional Intelligence?",
    "Emotional Intelligence (EQ) is the ability to identify, understand, manage, and use emotions effectively "
    "in oneself and others. Defined by Daniel Goleman (1995), it has 5 components: Self-Awareness, "
    "Self-Regulation, Internal Motivation, Empathy, and Social Skills. Goleman argues EQ matters more than "
    "IQ for professional and leadership success, accounting for 67% of leadership performance.",
    "May 2025, Aug/Sep 2022, May 2023, May 2024"): story.append(x)

# ── WORK ETHICS ───────────────────────────────────────────────────────────
for x in q_block_a("5", "What do you understand by Work Ethics?",
    "Work ethics are the moral principles and values that guide professional behaviour in a workplace. "
    "They include integrity (honesty and alignment of words and actions), reliability (meeting deadlines, "
    "punctuality), diligence (persistent effort), accountability (owning outcomes), professionalism "
    "(appropriate conduct), and confidentiality. Strong work ethics build professional reputation, "
    "trust, and long-term career success.",
    "May 2025, Aug/Sep 2022"): story.append(x)

# ── ORAL PRESENTATION ─────────────────────────────────────────────────────
for x in q_block_a("6", "What is Oral Presentation?",
    "An oral presentation is a formal, structured communication activity in which a speaker delivers "
    "information to an audience using spoken words, supported by visual aids (slides, demonstrations). "
    "It combines content organisation, verbal delivery (vocal variety, clarity), and non-verbal communication "
    "(eye contact, gestures, posture). Its structure follows: Opening (hook + preview) → Body (3-5 points) "
    "→ Conclusion (summary + call to action).",
    "May 2025, May 2024"): story.append(x)

# ── GROUP DISCUSSION ──────────────────────────────────────────────────────
for x in q_block_a("7", "Explain the Process of Group Discussion.",
    "A Group Discussion (GD) is a structured activity where 6-12 participants discuss a topic without a "
    "formal leader, while evaluators assess communication, knowledge, leadership, and teamwork. "
    "Process: Topic announced → Thinking time (1-2 min) → Discussion (15-20 min) → Conclusion/Summary. "
    "Evaluators assess: initiation, content quality, listening, leadership, conflict management, "
    "analytical thinking, and non-verbal communication.",
    "May 2025, May 2024"): story.append(x)

# ── CRITICAL THINKING ────────────────────────────────────────────────────
for x in q_block_a("8", "Define Critical Thinking.",
    "Critical thinking is the disciplined, systematic process of actively analysing, evaluating, and "
    "synthesising information to form well-reasoned judgements and decisions. It involves identifying "
    "assumptions, recognising biases, evaluating evidence quality, considering multiple perspectives, "
    "and drawing logical conclusions. It opposes passive acceptance of information. Key barriers include "
    "confirmation bias, groupthink, emotional reasoning, and hasty generalisation.",
    "May 2025, Aug/Sep 2022"): story.append(x)

# ── PARALANGUAGE ─────────────────────────────────────────────────────────
for x in q_block_a("9", "Describe Paralanguage with Suitable Example.",
    "Paralanguage (vocalics) refers to the non-verbal vocal elements that accompany spoken words and modify "
    "their meaning — HOW something is said, not WHAT is said. Components: pitch, volume, rate/speed, tone, "
    "pause, rhythm, and vocal quality. Example: 'Really?' said in a high-pitched, rising tone = genuine "
    "curiosity. Same word in flat sarcastic tone = disbelief or mockery. Mehrabian found paralanguage "
    "accounts for 38% of emotional communication impact.",
    "May 2025, Aug/Sep 2022, May 2024"): story.append(x)

# ── META-COMMUNICATION ────────────────────────────────────────────────────
for x in q_block_a("10", "Explain Meta-Communication.",
    "Meta-communication is communication ABOUT communication — it provides context, tone, and relational "
    "framing that tells the receiver HOW to interpret a message. Coined by Gregory Bateson; expanded by "
    "Watzlawick. Every message has two levels: Content (what is said) and Relationship/Meta level "
    "(how it should be understood). Example: 'I was just joking!' reframes a harsh statement. "
    "Winking while speaking = non-verbal meta-communication signalling sarcasm.",
    "May 2025, Aug/Sep 2022, May 2024"): story.append(x)

# ── PROXEMICS ─────────────────────────────────────────────────────────────
for x in q_block_a("11", "What is Proxemics / Proximity?",
    "Proxemics is the study of how humans use physical space as a form of communication, coined by "
    "Edward T. Hall (1966). Hall identified 4 spatial zones: Intimate (0-18 inches — for closest "
    "relationships), Personal (18 inches-4 feet — friends), Social (4-12 feet — professional "
    "interactions), and Public (12 feet+ — speeches/presentations). Cultural differences significantly "
    "affect acceptable spatial distances.",
    "Aug/Sep 2022, May 2023, May 2024"): story.append(x)

# ── POSITIVE THINKING ────────────────────────────────────────────────────
for x in q_block_a("12", "What is Positive Thinking?",
    "Positive thinking is a mental attitude that focuses on constructive, optimistic, and hopeful thoughts, "
    "approaching challenges with a 'can-do' mindset. Popularised by Norman Vincent Peale ('The Power of "
    "Positive Thinking', 1952). Benefits: reduced stress, greater resilience, better health, improved "
    "relationships, and higher productivity. Techniques: affirmations, visualisation, gratitude journaling, "
    "cognitive restructuring, and mindfulness.",
    "Aug/Sep 2022"): story.append(x)

# ── HAPTICS ──────────────────────────────────────────────────────────────
for x in q_block_a("13", "What is Haptics?",
    "Haptics is the study of communication through touch — from Greek 'haptikos' (able to grasp). Touch "
    "is the first sense humans develop and communicates warmth, support, dominance, intimacy, and cultural "
    "identity. Heslin's classification: Functional/Professional (doctor-patient), Social/Polite (handshake), "
    "Friendship/Warmth (friendly hug), Love/Intimacy (romantic touch). In professional settings, "
    "a firm handshake communicates confidence.",
    "May 2023"): story.append(x)

# ── GROUPTHINK ────────────────────────────────────────────────────────────
for x in q_block_a("14", "What is Groupthink?",
    "Groupthink is a psychological phenomenon where a group's desire for harmony, conformity, and consensus "
    "suppresses individual critical thinking, dissent, and realistic evaluation of alternatives. "
    "Coined by Irving Janis (1972). Symptoms: illusion of invulnerability, collective rationalisation, "
    "pressure on dissenters. Famous examples: NASA Challenger disaster, Bay of Pigs. Prevention: "
    "appoint devil's advocate, encourage open dissent, use structured decision-making.",
    "May 2023"): story.append(x)

# ── ETHICS ────────────────────────────────────────────────────────────────
for x in q_block_a("15", "What is Ethics (in a Professional Context)?",
    "Ethics refers to the moral principles and values that govern individual and organisational behaviour — "
    "distinguishing right from wrong in professional contexts. Professional ethics include integrity "
    "(honesty), confidentiality (protecting sensitive information), fairness, accountability, and "
    "respect for others. Business ethics involves ethical decision-making in areas like advertising, "
    "data privacy, employee treatment, and environmental responsibility.",
    "May 2023"): story.append(x)

# ── EMPATHY ──────────────────────────────────────────────────────────────
for x in q_block_a("16", "What is Empathy?",
    "Empathy is the ability to understand and share the feelings, perspectives, and experiences of another "
    "person. It is a core component of Goleman's Emotional Intelligence model. Three types: Cognitive "
    "empathy (intellectually understanding another's perspective), Emotional empathy (feeling what another "
    "feels), and Compassionate empathy (understanding + feeling + taking helpful action). High empathy "
    "is essential for leadership, conflict resolution, and customer relationships.",
    "May 2023"): story.append(x)

# ── ADAPTABILITY ─────────────────────────────────────────────────────────
for x in q_block_a("17", "What is Adaptability?",
    "Adaptability is the ability to adjust thoughts, behaviours, and approaches in response to changing "
    "circumstances, environments, and challenges. In the VUCA (Volatile, Uncertain, Complex, Ambiguous) "
    "workplace, adaptability is a critical survival skill. Types: Cognitive (flexible thinking), "
    "Emotional (resilience), Behavioural (new methods), Interpersonal (diverse relationships). "
    "Based on Carol Dweck's 'Growth Mindset' — viewing change as opportunity.",
    "May 2023"): story.append(x)

# ── SEMANTIC BARRIERS ─────────────────────────────────────────────────────
for x in q_block_a("18", "What are Semantic Barriers?",
    "Semantic barriers are communication obstacles arising from different interpretations or meanings "
    "of words, symbols, and language. They occur when the sender and receiver attach different meanings "
    "to the same word. Causes: jargon and technical language, ambiguous words, cultural differences in "
    "language, slang, and idioms. Example: 'Let's table the discussion' means 'postpone' in American "
    "English but 'discuss now' in British English.",
    "May 2023"): story.append(x)

# ── ACTIVE LISTENING ─────────────────────────────────────────────────────
for x in q_block_a("19", "What is Active Listening?",
    "Active listening is the intentional, focused process of fully attending to a speaker — understanding "
    "not just words but meaning, emotions, and intent — and responding in ways that confirm understanding. "
    "Carl Rogers championed it as essential for therapeutic communication. Components (RASA model): "
    "Receive (full attention), Appreciate (affirm), Summarise ('So what you mean is...'), "
    "Ask (clarifying questions). Contrasts with passive hearing.",
    "May 2024"): story.append(x)

# ── VERBAL COMMUNICATION ─────────────────────────────────────────────────
for x in q_block_a("20", "What is Verbal Communication?",
    "Verbal communication is the use of words — spoken or written — to exchange information, ideas, "
    "and feelings. It includes oral communication (face-to-face, telephone, speeches, meetings) and "
    "written communication (emails, reports, letters, memos). Verbal communication carries the logical "
    "content of a message. According to Mehrabian, words alone account for only 7% of emotional "
    "communication impact — tone and body language carry the rest.",
    "May 2024"): story.append(x)

# ── PROCESS OF COMMUNICATION ─────────────────────────────────────────────
for x in q_block_a("21", "What is the Process of Communication?",
    "The communication process is a sequential exchange of information involving 8 elements: Sender "
    "(encodes message) → Message (content) → Encoding (converting idea into symbols) → Channel/Medium "
    "(path: speech, email, letter) → Receiver (decodes message) → Decoding (interpreting meaning) → "
    "Feedback (receiver's response confirming understanding) → Noise (any interference: physical, "
    "semantic, psychological). Shannon-Weaver Model (1949) first formalised this process.",
    "May 2024"): story.append(x)

# ── SPEECHES VS DEBATES ───────────────────────────────────────────────────
for x in q_block_a("22", "Differentiate between Speech and Debate.",
    "A <b>speech</b> is a formal, one-sided oral address delivered by a single speaker to an audience — "
    "informative, persuasive, motivational, or commemorative. A <b>debate</b> is a structured argument between "
    "two opposing sides on a specific proposition (motion) — one side argues FOR (affirmative) and one "
    "AGAINST (opposition). Speech has no opponent; debate has direct opposition. "
    "Speech = monologue; Debate = structured adversarial dialogue.",
    "Aug/Sep 2022, May 2024"): story.append(x)

# ── SOFT SKILLS ──────────────────────────────────────────────────────────
for x in q_block_a("23", "What are Soft Skills?",
    "Soft skills are non-technical, interpersonal and social competencies that determine how a person "
    "communicates, collaborates, and behaves in professional and personal environments. Unlike hard skills "
    "(technical knowledge), soft skills include communication, emotional intelligence, leadership, "
    "teamwork, adaptability, problem-solving, and time management. According to LinkedIn (2019), 92% of "
    "talent professionals say soft skills matter as much or more than hard skills.",
    "May 2024"): story.append(x)

# ── ASSUMPTIONS ──────────────────────────────────────────────────────────
for x in q_block_a("24", "What are Assumptions in Communication?",
    "Assumptions in communication are unstated beliefs, presuppositions, or conclusions we take for "
    "granted without verifying them. They lead to misunderstandings, conflict, and communication breakdown "
    "because the sender assumes the receiver shares the same knowledge, context, or interpretation. "
    "Example: assuming a colleague understands technical jargon. Good communicators verify assumptions "
    "by seeking feedback, asking clarifying questions, and confirming shared understanding.",
    "May 2023"): story.append(x)

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# PART B — ALL LONG ANSWER QUESTIONS
# ══════════════════════════════════════════════════════════════════════════════
story.append(banner("PART B — ALL LONG ANSWER QUESTIONS", DARK))
story.append(sp(8))
story.append(Paragraph(
    "Every Part B question from all papers is answered below with: (1) Topic Background, "
    "(2) Full Answer within the correct word limit, (3) Exam tips where relevant.",
    S("NOTE2", fontSize=10, textColor=GRAY_M, fontName="Helvetica-Oblique", leading=14, spaceAfter=8)))

# ── TOPIC: SOFT SKILLS ────────────────────────────────────────────────────
story.append(banner("TOPIC 1: SOFT SKILLS", NAVY, 13))
story.append(sp(6))

for x in q_block_b("B1",
    "What are Soft Skills? What are its important types? How can soft skills enhance employability? (10 marks)",
    "Soft skills are the non-technical, personality-driven competencies that determine how a person "
    "interacts with others. They are critical for career success and are increasingly prioritised by "
    "employers over technical skills alone.",
    "<b>Introduction:</b><br/>Soft skills are a combination of interpersonal skills, social skills, "
    "communication abilities, character traits, attitudes, and emotional intelligence that enable people "
    "to work effectively with others and succeed professionally. The term 'soft' contrasts with 'hard' "
    "(technical) skills. Hard skills get you the interview; soft skills get you the job and help you grow.<br/><br/>"
    "<b>Definition:</b> Klaus and Bailey (2007): 'Soft skills are a combination of interpersonal skills, "
    "social skills, communication skills, character traits, attitudes, and emotional intelligence.' "
    "They are personality-based and harder to measure than technical competencies.<br/><br/>"
    "<b>Important Types of Soft Skills:</b><br/>"
    "1. <b>Communication Skills:</b> Verbal fluency, written clarity, active listening, non-verbal awareness. "
    "Example: A manager who gives clear project briefings reduces errors and misunderstandings.<br/>"
    "2. <b>Emotional Intelligence (EQ):</b> Self-awareness, self-regulation, motivation, empathy, social skills. "
    "High EQ professionals make better leaders and handle workplace pressure effectively.<br/>"
    "3. <b>Teamwork and Collaboration:</b> Working cooperatively toward shared goals, respecting diversity, "
    "compromising, and contributing fairly. Example: cross-functional project teams.<br/>"
    "4. <b>Problem-Solving and Critical Thinking:</b> Analysing situations logically, generating creative "
    "solutions, and making sound decisions. Ranked top-10 future skill by WEF.<br/>"
    "5. <b>Leadership:</b> Influencing, inspiring, and guiding others — even without formal authority.<br/>"
    "6. <b>Adaptability:</b> Embracing change, learning new skills, resilience during uncertainty.<br/>"
    "7. <b>Time Management:</b> Prioritising tasks, meeting deadlines, avoiding procrastination.<br/>"
    "8. <b>Negotiation:</b> Reaching mutually acceptable agreements through constructive dialogue.<br/><br/>"
    "<b>How Soft Skills Enhance Employability:</b><br/>"
    "1. <b>Hiring Decisions:</b> LinkedIn's 2019 Global Talent Trends survey found 92% of recruiters say "
    "soft skills matter as much or more than technical skills. Employers screen soft skills in every interview.<br/>"
    "2. <b>Career Advancement:</b> Technical skills secure entry-level roles; soft skills drive promotion. "
    "The most senior roles require leadership, communication, and interpersonal mastery — not technical expertise.<br/>"
    "3. <b>Team Performance:</b> Employees with strong soft skills improve entire team dynamics, communication "
    "quality, and collective output.<br/>"
    "4. <b>Client Relationships:</b> Empathy, listening, and persuasion skills build lasting client loyalty.<br/>"
    "5. <b>Adaptability to Change:</b> Professionals who can communicate across cultures, manage conflict, "
    "and navigate uncertainty are invaluable in global, rapidly changing organisations.<br/>"
    "6. <b>Automation Resistance:</b> While technical tasks can be automated, soft skills (empathy, creativity, "
    "leadership) cannot be replicated by machines — making them the most future-proof career assets.<br/><br/>"
    "<b>Conclusion:</b><br/>Soft skills are not optional additions to technical competence — they are "
    "multipliers. A technically skilled professional without soft skills hits a ceiling; one with both "
    "technical mastery and strong soft skills has no career ceiling. In 21st-century knowledge economies, "
    "soft skills are the differentiator between good employees and exceptional leaders.",
    "10", BLUE, "May 2023"): story.append(x)

for x in q_block_b("B2",
    "What are the three important Soft Skills? Explain with example. (10 marks)",
    "While all soft skills matter, certain ones are universally recognised as most critical for professional "
    "success. Communication, Emotional Intelligence, and Teamwork form the foundational triad.",
    "<b>Introduction:</b><br/>While soft skills encompass a broad range of interpersonal competencies, "
    "research consistently identifies three as the most critical: Communication, Emotional Intelligence, "
    "and Teamwork/Collaboration. These three underpin virtually every other soft skill.<br/><br/>"
    "<b>1. COMMUNICATION SKILLS:</b><br/>"
    "Communication is the process of transmitting information and meaning between people through "
    "verbal (spoken/written), non-verbal (body language, gestures), and paralinguistic (tone, pitch, pace) channels.<br/>"
    "Sub-skills: Active listening, verbal fluency, written precision, non-verbal awareness, and feedback.<br/>"
    "Why it matters: Every professional interaction — meetings, emails, presentations, negotiations, "
    "client calls — requires communication. Poor communication is the leading cause of workplace conflict, "
    "project failures, and missed opportunities.<br/>"
    "Example: A project manager who communicates requirements clearly to the development team avoids "
    "rework, reduces delays, and builds team trust. One who communicates poorly causes confusion, "
    "missed deadlines, and team frustration.<br/><br/>"
    "<b>2. EMOTIONAL INTELLIGENCE (EQ):</b><br/>"
    "Daniel Goleman's model identifies five components: Self-Awareness (knowing your emotions), "
    "Self-Regulation (managing impulses), Internal Motivation (intrinsic drive), Empathy "
    "(understanding others' emotions), and Social Skills (managing relationships).<br/>"
    "Why it matters: Goleman's research found EQ accounts for 67% of the abilities most important for "
    "leadership performance — more than IQ or technical skills. Low EQ professionals struggle with "
    "conflict, relationships, and stress management.<br/>"
    "Example: A team leader who remains calm during a crisis, listens to team members' concerns, "
    "and motivates them through uncertainty demonstrates high EQ — keeping team performance stable "
    "while lower-EQ leaders' teams collapse under pressure.<br/><br/>"
    "<b>3. TEAMWORK AND COLLABORATION:</b><br/>"
    "The ability to work cooperatively with diverse groups toward shared goals. Involves: active "
    "participation, respecting different viewpoints, constructive conflict resolution, role clarity, "
    "and shared accountability for outcomes.<br/>"
    "Tuckman's stages: Forming → Storming → Norming → Performing → Adjourning. "
    "Understanding these stages helps professionals navigate team dynamics.<br/>"
    "Why it matters: Modern work is team-based. No significant professional achievement happens alone. "
    "Cross-functional teams, remote collaboration, and global projects all demand strong teamwork skills.<br/>"
    "Example: A software team that communicates openly, respects each member's expertise, addresses "
    "conflicts quickly, and shares credit consistently outperforms equally skilled teams with poor "
    "collaboration skills.<br/><br/>"
    "<b>Conclusion:</b><br/>Communication, EQ, and Teamwork are the three most universally critical soft "
    "skills because they directly enable every other professional interaction. Developing these three "
    "creates a foundation from which all other soft skills naturally grow.",
    "10", BLUE, "May 2025"): story.append(x)

for x in q_block_b("B3",
    "How to remain positive and handle conflict in the workplace? (5 marks)",
    "Workplace conflict and negativity are inevitable. The ability to maintain positivity and resolve "
    "conflicts constructively is a high-value professional skill that preserves relationships and productivity.",
    "<b>Introduction:</b><br/>Conflict is a natural part of any workplace — diverse personalities, "
    "competing priorities, and resource constraints make disagreement inevitable. What differentiates "
    "high-performing professionals is not the absence of conflict but the ability to handle it constructively "
    "while maintaining a positive mindset.<br/><br/>"
    "<b>Strategies for Remaining Positive:</b><br/>"
    "1. <b>Growth Mindset (Carol Dweck):</b> View challenges as learning opportunities, not personal failures. "
    "Reframe setbacks: 'This is not failure — this is feedback.'<br/>"
    "2. <b>Focus on What You Can Control:</b> Identify what is within your sphere of influence "
    "and invest energy there. Release anxiety about uncontrollable factors.<br/>"
    "3. <b>Gratitude Practice:</b> Reflecting daily on 3 things that went well shifts focus from "
    "problems to progress — backed by positive psychology research.<br/>"
    "4. <b>Self-Regulation (EQ):</b> Pause before reacting to frustrating situations — "
    "the 90-second rule: acknowledge the emotion, breathe, respond thoughtfully.<br/>"
    "5. <b>Build Positive Relationships:</b> Invest in supportive professional relationships that "
    "provide perspective, encouragement, and collaborative problem-solving.<br/><br/>"
    "<b>Strategies for Handling Conflict:</b><br/>"
    "1. <b>Address Early:</b> Small conflicts escalate when ignored. Address issues promptly and privately.<br/>"
    "2. <b>Separate People from Problems:</b> Attack the issue, not the person. Harvard's Fisher and Ury: "
    "'Be hard on the problem, soft on the person.'<br/>"
    "3. <b>Listen First:</b> Give the other party full opportunity to express their perspective without "
    "interruption. Reflective listening ('What I hear you saying is...') builds trust.<br/>"
    "4. <b>Find Common Ground:</b> Identify shared interests and goals — most conflicts have more common "
    "ground than apparent at first.<br/>"
    "5. <b>Use 'I' Statements:</b> 'I feel frustrated when...' rather than 'You always...' "
    "reduces defensiveness and opens dialogue.<br/>"
    "6. <b>Involve Neutral Parties:</b> When direct resolution fails, mediation by a neutral manager "
    "or HR professional provides structured resolution.<br/><br/>"
    "<b>Conclusion:</b> Positivity is not naive optimism — it is a disciplined mental strategy. "
    "Conflict handled constructively strengthens relationships. Both skills together create the "
    "resilient, collaborative professional every organisation values.",
    "5", TEAL, "May 2025"): story.append(x)

story.append(PageBreak())

# ── TOPIC: COMMUNICATION ─────────────────────────────────────────────────
story.append(banner("TOPIC 2: COMMUNICATION — TYPES, 7 C's, SOCIO-ECONOMIC ROLE", TEAL_L, 13))
story.append(sp(6))

for x in q_block_b("B4",
    "Define Communication and its types. Do you think communication plays an important role in socio-economic development of country? (10-15 marks)",
    "Communication is the fundamental process through which information, ideas, and meaning are exchanged "
    "between individuals and groups. Its role in national development is profound — from education to commerce "
    "to governance, all progress depends on effective communication.",
    "<b>Definition of Communication:</b><br/>"
    "Communication is the process of transmitting information, ideas, feelings, and thoughts from one "
    "person (sender) to another (receiver) through a medium, with the objective of creating shared "
    "understanding. The word derives from Latin 'communis' — to make common. Keith Davis: 'Communication "
    "is the process of passing information and understanding from one person to another.'<br/><br/>"
    "<b>The Communication Process (8 Elements):</b><br/>"
    "Sender → Encoding → Message → Channel → Receiver → Decoding → Feedback → Noise (barrier).<br/><br/>"
    "<b>Types of Communication:</b><br/>"
    "<b>A. Based on Channel/Mode:</b><br/>"
    "1. <b>Verbal:</b> Uses words — Oral (face-to-face, phone, speeches — immediate, rich in feedback) and "
    "Written (emails, reports, letters — documented, permanent). According to Mehrabian, words carry "
    "only 7% of emotional impact; tone carries 38% and body language 55%.<br/>"
    "2. <b>Non-Verbal:</b> Body language, facial expressions, gestures, eye contact, posture, proxemics, "
    "haptics — often more powerful than words for conveying emotions and attitudes.<br/>"
    "3. <b>Visual:</b> Charts, graphs, infographics, videos — highly effective for complex data and across "
    "language barriers.<br/><br/>"
    "<b>B. Based on Direction (Organisational):</b><br/>"
    "1. <b>Downward:</b> Management to employees — instructions, policies, feedback.<br/>"
    "2. <b>Upward:</b> Employees to management — reports, suggestions, complaints.<br/>"
    "3. <b>Horizontal/Lateral:</b> Between peers — coordination, teamwork.<br/>"
    "4. <b>Diagonal:</b> Cross-department and cross-level — modern matrix organisations.<br/><br/>"
    "<b>C. Based on Formality:</b><br/>"
    "1. <b>Formal:</b> Official channels — board meetings, policy circulars, annual reports.<br/>"
    "2. <b>Informal (Grapevine):</b> Unofficial, spontaneous — fast but prone to distortion.<br/><br/>"
    "<b>Role of Communication in Socio-Economic Development:</b><br/>"
    "Yes — communication plays an absolutely critical, foundational role in a nation's development.<br/>"
    "1. <b>Economic Development:</b> Commerce, trade, and industry function entirely through communication. "
    "Business negotiations, contract formation, marketing, banking, and international trade all depend on "
    "effective formal and digital communication infrastructure.<br/>"
    "2. <b>Education and Skill Development:</b> Knowledge is transmitted through communication. "
    "Quality education — from classrooms to MOOCs — depends on clear, effective communication between "
    "teachers, students, policymakers, and employers.<br/>"
    "3. <b>Governance and Policy:</b> Democratic governance requires communication between citizens and "
    "government — political speeches, public consultations, right to information, and transparency. "
    "Corruption thrives where communication is suppressed.<br/>"
    "4. <b>Healthcare:</b> Public health campaigns (vaccination, hygiene, disease prevention) save millions "
    "of lives through effective mass communication. Doctor-patient communication directly impacts treatment outcomes.<br/>"
    "5. <b>Social Cohesion:</b> Communication bridges cultural, linguistic, and geographic divides — "
    "building national identity, tolerance, and collective action.<br/>"
    "6. <b>Technology and Innovation:</b> Scientific research, technological innovation, and entrepreneurship "
    "depend on communication — research publication, knowledge sharing, mentorship, and collaborative work.<br/>"
    "7. <b>Digital Economy:</b> India's digital revolution (UPI, Aadhaar, Digital India) depends on "
    "communication infrastructure — internet access, digital literacy, and data exchange protocols.<br/><br/>"
    "<b>Conclusion:</b><br/>Communication is the nervous system of society and the economy. A nation with "
    "poor communication infrastructure, low literacy, or suppressed information flows cannot achieve "
    "its development potential. Every rupee invested in communication — education, media, digital "
    "infrastructure — generates multiplied returns in economic and social progress.",
    "15", BLUE, "May 2025, Aug/Sep 2022"): story.append(x)

for x in q_block_b("B5",
    "Enumerate the 7 C's of Effective Communication. (5 marks)",
    "The 7 C's are the gold-standard framework for professional written and spoken communication, "
    "ensuring every message achieves its purpose without ambiguity, inefficiency, or offence.",
    "<b>Introduction:</b><br/>The 7 C's of communication are universally recognised principles that "
    "ensure every piece of professional communication — letter, email, report, presentation, or "
    "conversation — is effective, professional, and achieves its intended purpose.<br/><br/>"
    "<b>The 7 C's:</b><br/>"
    "1. <b>CLARITY:</b> The message must be immediately and unambiguously understood. Use simple, "
    "direct language. Avoid jargon with non-specialist audiences. Short sentences (15-20 words). "
    "Example: 'Please submit the report by Monday 5 PM.' (Clear) vs 'Kindly ensure the report is "
    "forwarded at the earliest.' (Unclear — when exactly?)<br/><br/>"
    "2. <b>CONCISENESS:</b> Use minimum words to convey maximum meaning. Eliminate redundancies: "
    "'Due to the fact that' = 'Because'. 'At this point in time' = 'Now'. "
    "Concise communication respects the reader's time and improves retention.<br/><br/>"
    "3. <b>COMPLETENESS:</b> Include ALL information the reader needs. Apply 5W1H test: "
    "Who? What? When? Where? Why? How? Incomplete messages require follow-up — wasting time.<br/><br/>"
    "4. <b>CORRECTNESS:</b> Verify all facts, names, figures, and grammar. One factual error "
    "or typo damages professional credibility. Proofread all formal communications.<br/><br/>"
    "5. <b>CONCRETENESS:</b> Use specific, definite, measurable language. "
    "'Sales improved significantly' = vague. 'Sales grew by 34% in Q3 2025' = concrete. "
    "Concrete language builds trust and enables action.<br/><br/>"
    "6. <b>COURTESY:</b> Maintain a respectful, empathetic, reader-oriented tone. "
    "Use 'please', 'thank you', and acknowledge inconvenience. "
    "Courtesy transforms transactional communication into relationship-building.<br/><br/>"
    "7. <b>CONSIDERATION:</b> Write from the READER's perspective — focus on their needs, "
    "interests, and benefits (You-Attitude). 'You will receive your refund by Friday' vs "
    "'We will process your refund by Friday' — same information; first is reader-centred.<br/><br/>"
    "<b>Conclusion:</b> The 7 C's are not bureaucratic rules — they are the architecture of effective "
    "professional communication. Applying all seven consistently builds credibility, clarity, and "
    "lasting professional relationships.",
    "5", TEAL, "May 2023, May 2024"): story.append(x)

for x in q_block_b("B6",
    "Discuss some modes of Non-Verbal Communication and their significance. (10 marks)",
    "Non-verbal communication encompasses all communication that does not use words. Mehrabian's research "
    "showed 55% of emotional impact comes from body language — making it the dominant communication channel. "
    "Understanding non-verbal modes is essential for professional effectiveness.",
    "<b>Introduction:</b><br/>Non-verbal communication (NVC) is all communication that occurs without words. "
    "Albert Mehrabian's famous 7-38-55 rule: 7% of emotional message impact comes from WORDS, "
    "38% from TONE OF VOICE (paralanguage), and 55% from BODY LANGUAGE. This makes NVC the dominant "
    "form of communication in face-to-face interaction.<br/><br/>"
    "<b>Modes of Non-Verbal Communication:</b><br/>"
    "1. <b>Kinesics (Body Language):</b> Study of body movements — gestures, facial expressions, eye "
    "contact, posture, and gait. Coined by Ray Birdwhistell. Nodding = agreement; Crossed arms = "
    "defensiveness; Upright posture = confidence; Slouching = disinterest.<br/>"
    "Significance: Reveals true emotions that words conceal. Liars show inconsistent kinesic signals.<br/><br/>"
    "2. <b>Facial Expressions:</b> Paul Ekman identified 6 universal micro-expressions: Happiness, Sadness, "
    "Anger, Fear, Disgust, Surprise. Micro-expressions (lasting 1/25 second) are involuntary — hard to fake. "
    "A genuine Duchenne smile involves both mouth muscles AND eye crinkles.<br/><br/>"
    "3. <b>Proxemics:</b> Edward T. Hall's study of space as communication (1966). Four zones: "
    "Intimate (0-18 inches), Personal (18in-4ft), Social (4-12ft), Public (12ft+). "
    "Entering intimate zone uninvited triggers stress and defensiveness.<br/><br/>"
    "4. <b>Paralanguage (Vocalics):</b> Non-verbal vocal elements — pitch, volume, rate, tone, pause, "
    "and vocal quality. HOW you say something, not WHAT you say. Accounts for 38% of emotional impact. "
    "Example: 'Really?' in rising tone = curiosity; flat tone = sarcasm.<br/><br/>"
    "5. <b>Haptics:</b> Communication through touch — handshakes, hugs, pats. Communicates warmth, "
    "support, dominance, and intimacy. Cultural variations are significant (contact vs non-contact cultures).<br/><br/>"
    "6. <b>Chronemics:</b> Use of time as communication. Punctuality signals respect and professionalism; "
    "constant lateness signals disrespect or power assertion.<br/><br/>"
    "7. <b>Oculesics:</b> Specifically the study of eye behaviour — gaze, blink rate, pupil dilation. "
    "Direct eye contact = confidence and honesty; avoidance = dishonesty or shyness; "
    "pupil dilation = interest or attraction.<br/><br/>"
    "8. <b>Appearance and Artifacts:</b> Clothing, grooming, and accessories communicate status, "
    "profession, culture, and personality. A formal suit projects authority; casual dress signals "
    "accessibility. First impressions are formed within 7 seconds — almost entirely non-verbally.<br/><br/>"
    "9. <b>Silence:</b> Silence communicates thoughtfulness, respect, disapproval, or tension. "
    "A strategic pause after a key statement in a presentation gives the audience time to absorb it.<br/><br/>"
    "<b>Significance of Non-Verbal Communication:</b><br/>"
    "1. Reveals TRUE emotions — liars show inconsistent non-verbal signals (micro-expressions).<br/>"
    "2. First impressions (within 7 seconds) are formed entirely through non-verbal cues.<br/>"
    "3. Reinforces or contradicts verbal messages — when they conflict, body language is believed.<br/>"
    "4. Regulates conversations — eye contact, nods, and gestures signal speaking turns.<br/>"
    "5. Establishes relationship dynamics — warmth, trust, and power communicated non-verbally.<br/><br/>"
    "<b>Conclusion:</b> Non-verbal communication is the unspoken language that often speaks louder than "
    "words. Mastery of non-verbal awareness enhances credibility, interpersonal connection, and the "
    "ability to read — and respond appropriately to — every communication situation.",
    "10", BLUE, "May 2023"): story.append(x)

for x in q_block_b("B7",
    "What is Meta-Communication? Is non-verbal language always supportive of verbal language? (10 marks)",
    "Meta-communication is one of the most sophisticated concepts in communication theory — it explains "
    "why the same words can mean completely different things in different contexts. Understanding whether "
    "verbal and non-verbal always align is critical for accurate message interpretation.",
    "<b>Meta-Communication — Definition:</b><br/>"
    "Meta-communication is 'communication about communication' — messages that define, clarify, or modify "
    "the meaning of other messages. From Greek 'meta' (about/beyond). Developed by Gregory Bateson "
    "and Paul Watzlawick (1967). Watzlawick's principle: Every message has two levels — "
    "CONTENT level (what is said) and RELATIONSHIP level (how it should be interpreted). "
    "The relationship level IS the meta-communication.<br/><br/>"
    "<b>Examples of Meta-Communication:</b><br/>"
    "1. 'I was just joking!' — verbal meta-communication that reframes a harsh statement as humour.<br/>"
    "2. Winking while saying something serious — non-verbal meta-communication: 'don't take this literally'.<br/>"
    "3. 'Let's have a serious talk' — relational meta-message about the conversation's importance.<br/>"
    "4. Email subject line 'URGENT' — meta-message about priority.<br/>"
    "5. Cold tone when saying 'Fine' — contradicts the word; reveals displeasure.<br/><br/>"
    "<b>Is Non-Verbal Language Always Supportive of Verbal Language?</b><br/>"
    "<b>NO — Non-verbal language is NOT always supportive of verbal language.</b><br/><br/>"
    "<b>When Non-Verbal SUPPORTS Verbal (Congruence):</b><br/>"
    "1. <b>Complementing:</b> Nodding while saying 'Yes I agree.' — reinforces the verbal message.<br/>"
    "2. <b>Accenting:</b> Slamming the table while saying 'This must stop!' — emphasises the verbal message.<br/>"
    "3. <b>Repeating:</b> Pointing to the door while saying 'Please leave' — repeats the message in another channel.<br/>"
    "4. <b>Substituting:</b> Thumbs up instead of saying 'Good job.' — replaces verbal entirely.<br/><br/>"
    "<b>When Non-Verbal CONTRADICTS Verbal (Incongruence):</b><br/>"
    "1. <b>Deception:</b> A person says 'I'm not nervous' while visibly trembling, sweating, and avoiding "
    "eye contact. Body language betrays the verbal denial — and body language is believed.<br/>"
    "2. <b>Sarcasm:</b> Saying 'That's a GREAT idea!' with an eye-roll and flat tone. "
    "The non-verbal completely inverts the verbal meaning.<br/>"
    "3. <b>Suppressed Emotion:</b> A person says 'I'm fine' while displaying sadness micro-expressions. "
    "The non-verbal tells the true story.<br/>"
    "4. <b>Cultural Conflict:</b> In some cultures, nodding means 'I'm listening' (not 'I agree'). "
    "A South Asian nodding 'yes' may be saying 'I understand' not 'I consent' — creating misunderstanding.<br/><br/>"
    "<b>The Golden Rule — When They Conflict:</b><br/>"
    "When verbal and non-verbal messages contradict each other, research consistently shows that "
    "people believe the NON-VERBAL message. The body does not lie as easily as words do. "
    "This is why interviewers, negotiators, and therapists pay close attention to body language "
    "even when spoken words sound confident and agreeable.<br/><br/>"
    "<b>Conclusion:</b><br/>Non-verbal language serves communication in four ways: complementing, "
    "accenting, repeating, and substituting. But it also regularly contradicts verbal language — "
    "particularly in deception, sarcasm, and suppressed emotion. Effective communicators develop "
    "awareness of both channels to understand the complete message being sent.",
    "10", TEAL, "May 2023"): story.append(x)

story.append(PageBreak())

# ── TOPIC: LISTENING & GROUP DISCUSSION ──────────────────────────────────
story.append(banner("TOPIC 3: LISTENING, GROUP DISCUSSION & LEADERSHIP", GREEN_M, 13))
story.append(sp(6))

for x in q_block_b("B8",
    "Discuss Listening as an Art. / Explain the role of Listening in Group Discussion. (5 marks)",
    "Listening is described as an art because it requires conscious, deliberate practice to move from "
    "passive hearing to active, empathetic engagement. In group discussions, listening quality directly "
    "determines the contribution quality.",
    "<b>Listening as an Art:</b><br/>"
    "Hearing is a passive physiological process — sound waves hitting the eardrum. "
    "Listening is an active cognitive and emotional process requiring attention, interpretation, "
    "evaluation, and response. Research shows we spend 45% of communication time listening — yet "
    "retain only 25% of what we hear. This gap is why listening is called an art that must be practised.<br/><br/>"
    "<b>Key Principles of Effective Listening:</b><br/>"
    "1. <b>Stop Talking:</b> You cannot listen and talk simultaneously. Silence is the first requirement.<br/>"
    "2. <b>Full Attention:</b> Put away distractions. Face the speaker. Stop mental planning of responses.<br/>"
    "3. <b>Empathise:</b> Try to understand the speaker's perspective, feelings, and context.<br/>"
    "4. <b>Avoid Prejudging:</b> Form conclusions only after the speaker finishes.<br/>"
    "5. <b>Give Feedback:</b> Verbal ('I see...') and non-verbal (nodding) signals that confirm attention.<br/>"
    "6. <b>Paraphrase:</b> 'So what you mean is...' confirms accurate understanding.<br/><br/>"
    "<b>Role of Listening in Group Discussion:</b><br/>"
    "1. <b>Building on Ideas:</b> You can only build on others' points if you have truly listened. "
    "'Adding to what Priya said...' signals active engagement and collaborative thinking.<br/>"
    "2. <b>Avoiding Repetition:</b> Active listeners don't repeat points already made — showing "
    "respect and awareness of the discussion's progress.<br/>"
    "3. <b>Leadership:</b> In GDs, evaluators specifically assess whether candidates listen — "
    "a listener who synthesises the group's discussion and summarises it demonstrates leadership.<br/>"
    "4. <b>Conflict Prevention:</b> Most GD conflicts arise from participants not truly hearing each other. "
    "Good listening reduces friction and increases productive dialogue.<br/>"
    "5. <b>Quality of Contribution:</b> The best GD contributions are responses to what was actually said — "
    "only possible through attentive listening.<br/><br/>"
    "<b>Tips for Becoming a Good Listener:</b><br/>"
    "Maintain eye contact · Use verbal affirmations · Take mental notes · Ask clarifying questions · "
    "Resist the urge to form responses mid-sentence · Practise mindful presence.<br/><br/>"
    "<b>Conclusion:</b> Listening is the most underrated communication skill. In group discussions, "
    "a skilled listener who builds on others' ideas, prevents repetition, and synthesises perspectives "
    "consistently outscores louder but less attentive participants.",
    "5", GREEN_M, "May 2023, Aug/Sep 2022"): story.append(x)

for x in q_block_b("B9",
    "Write in brief about ALL types of Listening. (5 marks)",
    "Listening is not a single, uniform activity. Context, purpose, and mindset determine the type "
    "of listening engaged. There are 10 recognised types, each serving a distinct communicative function.",
    "<b>Types of Listening:</b><br/>"
    "1. <b>Active Listening:</b> Full, intentional engagement — attending to words, tone, and emotions. "
    "Provides verbal/non-verbal feedback. Highest quality. Used in counselling, management, conflict resolution.<br/><br/>"
    "2. <b>Passive Listening:</b> Receiving information without active feedback — one-way absorption. "
    "Appropriate for radio, podcasts, lectures. Not suitable for interpersonal communication.<br/><br/>"
    "3. <b>Empathetic Listening:</b> Listening to understand the speaker's emotional state — "
    "suspending personal judgment to enter their emotional world. Essential for counsellors and empathetic leaders.<br/><br/>"
    "4. <b>Critical / Evaluative Listening:</b> Analysing content for logic, accuracy, and validity. "
    "Used when evaluating arguments, speeches, and proposals. Requires high cognitive engagement.<br/><br/>"
    "5. <b>Appreciative Listening:</b> Listening for pleasure and aesthetic enjoyment — music, poetry, "
    "comedy. Information retention is not the goal.<br/><br/>"
    "6. <b>Informational Listening:</b> Focus on understanding and retaining factual content. "
    "Used in academic lectures and training sessions. Note-taking accompanies this.<br/><br/>"
    "7. <b>Discriminative Listening:</b> Detecting subtle differences in sounds — tone, pitch, accent. "
    "Foundation of all listening. Allows recognition of sarcasm, emotional subtext, and cultural cues.<br/><br/>"
    "8. <b>Selective Listening:</b> Paying attention only to parts that confirm existing beliefs or interests. "
    "Unconscious bias. Dangerous in professional settings — causes serious misunderstandings.<br/><br/>"
    "9. <b>Pseudo-Listening (False Listening):</b> Appearing to listen (nodding, eye contact) while "
    "mentally absent. Severely damages relationships when discovered. Common in low-engagement meetings.<br/><br/>"
    "10. <b>Deep/Mindful Listening:</b> Complete presence — no mental chatter, no planning responses. "
    "Associated with mindfulness and high EQ. Produces profound understanding.<br/><br/>"
    "<b>Conclusion:</b> Consciously choosing the right type of listening for each situation transforms "
    "communication quality. Moving from selective or pseudo-listening to active or empathetic listening "
    "is one of the most impactful professional development investments.",
    "5", TEAL, "May 2024"): story.append(x)

for x in q_block_b("B10",
    "Can leadership be learnt? Can we train ourselves to be leaders? (5 marks)",
    "Leadership development is one of the most debated topics in management theory. The question "
    "of whether leaders are born or made has significant implications for professional development, "
    "education, and organisational training programmes.",
    "<b>Introduction:</b><br/>The debate: Are leaders born (nature) or made (nurture)? Modern research "
    "strongly supports that while some personality traits provide a natural advantage, "
    "leadership is fundamentally a learnable set of skills and behaviours.<br/><br/>"
    "<b>Arguments Supporting 'Leadership Can Be Learnt':</b><br/>"
    "1. <b>Behavioural Theories:</b> Ohio State and Michigan University studies (1940s-50s) found "
    "that effective leadership behaviours — task orientation and people orientation — can be taught "
    "and practised. Leadership is WHAT leaders DO, not WHO they are.<br/>"
    "2. <b>Situational Leadership (Hersey and Blanchard):</b> Effective leaders adapt their style "
    "(Telling → Selling → Participating → Delegating) based on follower maturity — "
    "this contextual intelligence is learnable through training and experience.<br/>"
    "3. <b>Emotional Intelligence (Goleman):</b> EQ — the core of great leadership — is 'highly "
    "developable' according to Goleman's research. Unlike IQ, EQ grows significantly with self-awareness "
    "practices, feedback, and deliberate effort.<br/>"
    "4. <b>Global Leadership Development Industry:</b> Organisations invest billions in leadership "
    "programmes annually (ILM, CCL, Kellogg) — with measurable results in performance improvement.<br/>"
    "5. <b>Historical Examples:</b> Many great leaders developed through experience, mentorship, "
    "and deliberate practice — not innate genius. Winston Churchill was mocked as a poor speaker; "
    "he trained himself into one of history's greatest orators.<br/><br/>"
    "<b>How to Train Ourselves to Be Leaders:</b><br/>"
    "1. <b>Develop Self-Awareness:</b> Regular reflection, journaling, 360-degree feedback.<br/>"
    "2. <b>Build EQ:</b> Mindfulness, empathy practice, managing emotional reactions.<br/>"
    "3. <b>Study Leadership Models:</b> Read widely — biographies, leadership theory, case studies.<br/>"
    "4. <b>Seek Leadership Opportunities:</b> Volunteer for projects, team roles, community work.<br/>"
    "5. <b>Find a Mentor:</b> Learn from experienced leaders through observation and guided reflection.<br/>"
    "6. <b>Develop Communication:</b> Public speaking, active listening, negotiation — all learnable skills.<br/><br/>"
    "<b>Conclusion:</b><br/>While natural personality traits may provide a head start, leadership is "
    "fundamentally a learnable craft. The most effective leaders are those who combine whatever natural "
    "disposition they possess with deliberate, sustained self-development. The question is not "
    "'Can I be a leader?' but 'Am I willing to do the work?'",
    "5", GREEN_M, "May 2025, Aug/Sep 2022, May 2024"): story.append(x)

for x in q_block_b("B11",
    "Write in brief the essential attributes of a good leader. (10 marks)",
    "Leadership effectiveness is determined by a consistent set of attributes that enable a person "
    "to inspire, guide, and develop others toward shared goals. These attributes span cognitive, "
    "emotional, and behavioural dimensions.",
    "<b>Introduction:</b><br/>A good leader is one who inspires voluntary action — people follow them "
    "not because they must but because they want to. Warren Bennis: 'Leadership is the capacity to "
    "translate vision into reality.' The essential attributes of a good leader span intellectual, "
    "emotional, and behavioural dimensions.<br/><br/>"
    "<b>Essential Attributes of a Good Leader:</b><br/>"
    "1. <b>Vision:</b> The ability to see beyond the present — to define a compelling picture of "
    "a desired future and communicate it powerfully. Great leaders give people a destination that "
    "is both inspiring and achievable. Example: Steve Jobs' vision for 'a computer in every hand.'<br/><br/>"
    "2. <b>Integrity:</b> Absolute alignment between words and actions. 'Walk the talk.' "
    "Trust is built slowly and destroyed instantly — integrity is its foundation. "
    "Warren Bennis: 'Leadership without integrity is just manipulation.'<br/><br/>"
    "3. <b>Emotional Intelligence (EQ):</b> Self-awareness, self-regulation, empathy, motivation, "
    "and social skills. Goleman found EQ accounts for 67% of leadership performance — more than "
    "IQ or technical competence. Leaders with high EQ handle pressure, conflict, and change with composure.<br/><br/>"
    "4. <b>Communication Excellence:</b> Clarity in setting direction, active listening to understand "
    "team concerns, persuasion through storytelling and evidence, and feedback that develops people. "
    "Great leaders make complex ideas simple and compelling.<br/><br/>"
    "5. <b>Decisiveness:</b> The courage to make decisions under uncertainty and own their consequences. "
    "Indecisive leaders create organisational paralysis. Good leaders gather adequate data, "
    "consult where appropriate, decide confidently, and adapt when new information emerges.<br/><br/>"
    "6. <b>Empathy:</b> Understanding team members' perspectives, feelings, and circumstances. "
    "Empathetic leaders create psychological safety — environments where people feel safe to "
    "take risks, share ideas, and admit mistakes.<br/><br/>"
    "7. <b>Adaptability:</b> Remaining effective through change. The most valuable leaders thrive "
    "in uncertainty — they see change as opportunity and help their teams navigate it with confidence.<br/><br/>"
    "8. <b>Accountability:</b> Taking ownership of outcomes — both successes and failures. "
    "Leaders who blame others for failures and take credit for others' successes destroy team morale "
    "and lose their most talented members.<br/><br/>"
    "9. <b>Ability to Develop Others:</b> The best leaders make themselves unnecessary by developing "
    "their team members' capabilities. They invest in coaching, mentoring, and delegating growth opportunities.<br/><br/>"
    "10. <b>Courage:</b> The willingness to make unpopular decisions, challenge the status quo, "
    "give honest feedback, and advocate for what is right — even under pressure.<br/><br/>"
    "<b>Conclusion:</b><br/>Great leadership is not a single attribute — it is a dynamic combination "
    "of vision, character, emotional intelligence, and communication skills. These attributes can all "
    "be developed through deliberate practice, reflection, and continuous learning. The most effective "
    "leaders are not those with the most talent — they are those who work hardest on themselves.",
    "10", TEAL, "May 2024"): story.append(x)

story.append(PageBreak())

# ── TOPIC: PERSONALITY DEVELOPMENT ───────────────────────────────────────
story.append(banner("TOPIC 4: PERSONALITY DEVELOPMENT & TELEPHONIC COMMUNICATION", PURPLE_M, 13))
story.append(sp(6))

for x in q_block_b("B12",
    "What do you mean by Personality Development? Explain the effective ways to develop a sound personality. (5 marks)",
    "Personality development is the systematic process of enhancing one's attributes, behaviours, "
    "and attitudes to become more effective personally and professionally. It is based on the premise "
    "that personality — while partly genetic — is substantially shaped by environment and conscious effort.",
    "<b>Definition:</b><br/>Personality is the unique, consistent pattern of thoughts, emotions, and "
    "behaviours that characterises an individual. Personality development is the process of enhancing "
    "these patterns through deliberate effort — building on strengths, addressing weaknesses, and "
    "developing new competencies.<br/><br/>"
    "<b>Determinants of Personality:</b><br/>"
    "1. Heredity — genetic temperament and predispositions<br/>"
    "2. Environment — family, culture, education, social circle<br/>"
    "3. Situation — context and significant life experiences shape character<br/><br/>"
    "<b>Effective Ways to Develop a Sound Personality:</b><br/>"
    "1. <b>Build Self-Awareness:</b> Know your strengths, limitations, values, and emotional triggers. "
    "Use tools: personality assessments (MBTI, Big Five), journaling, 360° feedback.<br/><br/>"
    "2. <b>Develop Communication Skills:</b> Speak clearly, listen actively, write precisely, "
    "and communicate non-verbally with confidence. Communication shapes every first impression.<br/><br/>"
    "3. <b>Cultivate Emotional Intelligence:</b> Manage your emotional responses, develop empathy, "
    "and build meaningful professional relationships.<br/><br/>"
    "4. <b>Set SMART Goals:</b> Direction and structured progress fuel personality growth. "
    "People with clear goals project greater confidence and purpose.<br/><br/>"
    "5. <b>Read and Learn Continuously:</b> Wide reading expands perspective, vocabulary, "
    "knowledge base, and empathy — all of which contribute to a richer personality.<br/><br/>"
    "6. <b>Practise Positive Thinking:</b> Replace self-critical inner dialogue with affirmations "
    "and constructive self-talk. Confidence is built from the inside out.<br/><br/>"
    "7. <b>Develop Social Skills:</b> Networking, teamwork, public speaking, and conflict resolution "
    "build interpersonal confidence and professional presence.<br/><br/>"
    "8. <b>Manage Time and Stress:</b> Punctuality, discipline, and stress management "
    "communicate reliability and self-control — both key personality attributes.<br/><br/>"
    "<b>Conclusion:</b> Personality is not fixed destiny — it is shaped by daily choices, "
    "habits, and environments. A commitment to continuous self-improvement is itself the most "
    "powerful personality attribute of all.",
    "5", PURPLE_M, "May 2025, Aug/Sep 2022"): story.append(x)

for x in q_block_b("B13",
    "How should we deal with difficult callers in a telephonic conversation? (5 marks)",
    "Telephonic communication lacks visual cues, making voice management and emotional regulation "
    "even more critical. Difficult callers — angry customers, unreasonable complainants, or confused "
    "clients — test professional composure and problem-solving skills simultaneously.",
    "<b>Introduction:</b><br/>Difficult callers are an inevitable reality in any professional role "
    "involving telephonic communication — customer service, helpdesks, sales, or management. "
    "How you handle them determines the professional relationship outcome and represents the "
    "organisation's reputation in that moment.<br/><br/>"
    "<b>Types of Difficult Callers:</b><br/>"
    "1. Angry/Aggressive callers — frustrated with a product, service, or experience.<br/>"
    "2. Confused callers — don't understand the issue or process.<br/>"
    "3. Talkative callers — don't allow responses; monologise.<br/>"
    "4. Demanding callers — unreasonable expectations; want immediate resolutions.<br/>"
    "5. Rude callers — disrespectful language and tone.<br/><br/>"
    "<b>Strategies for Handling Difficult Callers:</b><br/>"
    "1. <b>Stay Calm — Always:</b> Never match the caller's emotional intensity. "
    "'Emotional contagion' works both ways — your calm voice can de-escalate their anger. "
    "Take a breath before responding. Lower your voice slightly — it calms the conversation.<br/><br/>"
    "2. <b>Listen Without Interrupting:</b> Let the caller fully express their frustration. "
    "Interrupting an angry caller escalates the situation. Being heard is what most upset "
    "callers need first — before solutions.<br/><br/>"
    "3. <b>Empathise Genuinely:</b> 'I completely understand how frustrating this must be for you.' "
    "Empathy validates the caller's feelings without accepting blame. It is the fastest "
    "path to de-escalation.<br/><br/>"
    "4. <b>Apologise for the Experience (Not Necessarily the Company):</b> "
    "'I'm so sorry you've had this experience' acknowledges their frustration professionally. "
    "Avoid: 'That's not our policy' or 'You should have...' — both escalate further.<br/><br/>"
    "5. <b>Focus on Solutions:</b> After acknowledging the issue, move to: "
    "'Here is what I can do for you right now...' Give clear, specific next steps.<br/><br/>"
    "6. <b>Set Polite Limits on Abuse:</b> If a caller becomes verbally abusive: "
    "'I want to help you, but I need us to have a respectful conversation to do that effectively. "
    "If you continue in this manner, I will need to end the call.' Then follow through if necessary.<br/><br/>"
    "7. <b>Document and Follow Up:</b> Note the caller's concern, what was promised, and follow up "
    "within the committed timeframe. Breaking a promise to an already difficult caller "
    "creates a permanent relationship breakdown.<br/><br/>"
    "<b>Conclusion:</b> Every difficult call handled professionally converts a frustrated contact "
    "into a satisfied one — often the most loyal customers are those whose complaints were "
    "resolved exceptionally. Composure, empathy, and solution-focus are the three pillars of "
    "difficult-caller management.",
    "5", TEAL, "Aug/Sep 2022"): story.append(x)

story.append(PageBreak())

# ── TOPIC: REPORT WRITING ─────────────────────────────────────────────────
story.append(banner("TOPIC 5: REPORT WRITING — TYPES, STRUCTURE & STRATEGIES", CRIMSON, 13))
story.append(sp(6))

for x in q_block_b("B14",
    "What is Report Writing? Explain in detail the important elements of a Long Report. (15 marks)",
    "A report is one of the most important formal documents in any organisation. Long (formal) reports "
    "are comprehensive documents used for major investigations, feasibility studies, annual reviews, "
    "and research presentations. Understanding their complete structure is ESSENTIAL — this question "
    "appears in almost every paper.",
    "<b>What is Report Writing?</b><br/>"
    "Report writing is the process of documenting, organising, and presenting factual information, "
    "findings, analysis, and recommendations in a structured format for a defined audience and purpose. "
    "Lesikar and Pettit: 'A report is any written communication about something done, observed, or "
    "investigated.' Reports are the backbone of organisational decision-making, accountability, "
    "and institutional memory.<br/><br/>"
    "<b>Characteristics of a Good Report:</b><br/>"
    "Accurate · Objective · Clear · Complete · Concise · Logically organised · Reader-focused · Timely<br/><br/>"
    "<b>Types of Reports (Brief):</b><br/>"
    "Formal/Informal · Informational/Analytical · Periodic/Special · Internal/External · "
    "Progress/Feasibility/Audit/Incident<br/><br/>"
    "<b>IMPORTANT ELEMENTS OF A LONG (FORMAL) REPORT:</b><br/><br/>"
    "<b>1. TITLE PAGE:</b><br/>"
    "The first page. Contains: Complete report title (specific and descriptive), Author's full name "
    "and designation, Department and organisation, Date of submission, Submitted to (recipient's "
    "name and designation), and Report reference number. The title must answer 'What is this report "
    "about?' Example: 'Market Feasibility Report for Entry into the South Asian E-Commerce Market (2025).'<br/><br/>"
    "<b>2. LETTER OF TRANSMITTAL / PREFACE:</b><br/>"
    "A formal covering memo/letter that officially presents the report to the recipient. Contains: "
    "Formal greeting, purpose of the report, brief summary of scope and key findings, "
    "acknowledgements, and formal closing. Think of it as a formal 'handover' document.<br/><br/>"
    "<b>3. TABLE OF CONTENTS (ToC):</b><br/>"
    "Lists all major sections, subsections, and appendices with accurate page numbers. Enables "
    "readers to navigate directly to needed information. All headings must match the body exactly. "
    "Required in reports exceeding 5 pages.<br/><br/>"
    "<b>4. LIST OF FIGURES / LIST OF TABLES:</b><br/>"
    "Separate lists of all visual elements — tables, charts, graphs, diagrams — with their "
    "titles and page numbers. Required when reports contain multiple visuals.<br/><br/>"
    "<b>5. EXECUTIVE SUMMARY / ABSTRACT:</b><br/>"
    "A condensed, standalone summary of the entire report — purpose, methodology, key findings, "
    "conclusions, and recommendations — in 1-2 pages. Written LAST but placed first. "
    "A busy executive must be able to understand the complete report from this section alone. "
    "It is the most-read section of any formal report.<br/><br/>"
    "<b>6. INTRODUCTION:</b><br/>"
    "Opens the report body. Contains: Background context, Purpose/Objective (why the report was written), "
    "Scope (what is covered and excluded), Methodology overview (how information was gathered), "
    "Limitations (constraints on the research), and Organisation of the report (overview of subsequent sections).<br/><br/>"
    "<b>7. METHODOLOGY / RESEARCH METHOD:</b><br/>"
    "Describes HOW the research was conducted: Data collection methods (surveys, interviews, "
    "observation, secondary research), Sample size and selection criteria, Research instruments used, "
    "and Data analysis techniques. Must be detailed enough for another researcher to replicate the study.<br/><br/>"
    "<b>8. FINDINGS / RESULTS:</b><br/>"
    "The core section — presents collected data objectively. No interpretation yet — only facts. "
    "Organised with headings, subheadings, tables, and charts. Rule: Every visual must be titled, "
    "numbered, and referenced in the text.<br/><br/>"
    "<b>9. DISCUSSION / ANALYSIS:</b><br/>"
    "Interprets the findings: What do they mean? What patterns emerge? How do findings relate to "
    "the original purpose? Comparison with existing literature or benchmarks. This is where "
    "analytical thinking is demonstrated — not just WHAT happened but WHY.<br/><br/>"
    "<b>10. CONCLUSIONS:</b><br/>"
    "Reasoned judgements drawn directly from the analysis. No new information introduced. "
    "Directly answers the questions posed in the Introduction. Numbered for clarity. "
    "Conclusion is evidence-based judgement — not personal opinion.<br/><br/>"
    "<b>11. RECOMMENDATIONS:</b><br/>"
    "Specific, actionable proposals based on the conclusions: WHO should do WHAT by WHEN. "
    "Numbered for reference. May include cost estimates and responsible parties. "
    "Not all reports have recommendations — informational reports end at conclusions.<br/><br/>"
    "<b>12. REFERENCES / BIBLIOGRAPHY:</b><br/>"
    "Complete list of all sources cited. Formatted consistently (APA, MLA, or Harvard style). "
    "Demonstrates intellectual honesty and allows readers to verify sources.<br/><br/>"
    "<b>13. APPENDICES:</b><br/>"
    "Supplementary material too detailed for the main body: Raw data, questionnaires, interview "
    "transcripts, detailed calculations, maps, photographs, legal documents. "
    "Labelled: Appendix A, Appendix B, etc.<br/><br/>"
    "<b>Conclusion:</b><br/>A long report is a systematic, comprehensive communication instrument. "
    "Each section serves a distinct and non-substitutable role. The quality of a formal report "
    "reflects directly on the professional credibility of its author and the organisation it represents. "
    "Writing excellent reports is one of the highest-value skills any professional can develop.",
    "15", CRIMSON, "May 2025, May 2024, Aug/Sep 2022"): story.append(x)

for x in q_block_b("B15",
    "Describe various types of Reports. Discuss the important elements of a formal report. (10 marks)",
    "Reports vary enormously in purpose, audience, format, and length. Understanding the classification "
    "system helps writers choose the right format and readers understand what to expect.",
    "<b>Introduction:</b><br/>A report is a structured document presenting factual information for a "
    "specific audience and purpose. Reports are classified on multiple bases.<br/><br/>"
    "<b>Classification of Reports:</b><br/>"
    "<b>A. Based on Formality:</b><br/>"
    "1. <b>Formal Reports:</b> Long, structured, official — title page, executive summary, ToC, "
    "findings, conclusions, recommendations, appendices. Used for external or senior management "
    "audiences. Example: Annual reports, feasibility studies, audit reports.<br/>"
    "2. <b>Informal Reports:</b> Short, internal, memo/letter format. Less rigid structure. "
    "Example: Progress updates, incident reports, daily summaries.<br/><br/>"
    "<b>B. Based on Purpose:</b><br/>"
    "1. <b>Informational Reports:</b> Present facts without analysis — attendance records, sales figures.<br/>"
    "2. <b>Analytical Reports:</b> Analyse problems and provide recommendations — feasibility studies, "
    "market analysis. Most complex and demanding type.<br/>"
    "3. <b>Research Reports:</b> Systematic investigation — defined methodology, literature review, "
    "data analysis. Academic and scientific contexts.<br/><br/>"
    "<b>C. Based on Frequency:</b><br/>"
    "1. <b>Periodic/Routine Reports:</b> Fixed intervals — weekly sales, quarterly financial, annual review.<br/>"
    "2. <b>Special Reports:</b> One-time — accident investigation, new market entry study.<br/><br/>"
    "<b>D. Based on Audience:</b><br/>"
    "Internal (within organisation) vs External (to clients, government, investors).<br/><br/>"
    "<b>E. Special Types:</b><br/>"
    "Progress Reports · Feasibility Reports · Audit Reports · Incident Reports · Minutes of Meeting<br/><br/>"
    "<b>Important Elements of a Formal Report (Summary):</b><br/>"
    "1. Title Page — identification details<br/>"
    "2. Letter of Transmittal — formal handover<br/>"
    "3. Table of Contents — navigation<br/>"
    "4. Executive Summary — standalone overview (written last, placed first)<br/>"
    "5. Introduction — background, purpose, scope, limitations<br/>"
    "6. Methodology — how research was conducted<br/>"
    "7. Findings — objective data presentation<br/>"
    "8. Discussion/Analysis — interpretation and meaning<br/>"
    "9. Conclusions — evidence-based judgements<br/>"
    "10. Recommendations — specific actionable proposals<br/>"
    "11. References — cited sources<br/>"
    "12. Appendices — supplementary material<br/><br/>"
    "<b>Conclusion:</b> Knowing which report type to use — and correctly structuring it — demonstrates "
    "professional competence and ensures the report achieves its communication purpose.",
    "10", AMBER, "Aug/Sep 2022, May 2023"): story.append(x)

story.append(PageBreak())

# ── TOPIC: BUSINESS LETTERS ───────────────────────────────────────────────
story.append(banner("TOPIC 6: BUSINESS LETTERS — TYPES, FORMATS & SAMPLES", TEAL_L, 13))
story.append(sp(6))

for x in q_block_b("B16",
    "Define Business Letter. Explain the types, principles and formats of Business Letters. (15 marks)",
    "The business letter is the most formal and legally significant form of written professional "
    "communication. This question appears in EVERY paper — master it completely.",
    "<b>DEFINITION OF BUSINESS LETTER:</b><br/>"
    "A business letter is a formal written document sent by an individual or organisation to another "
    "for a specific professional purpose — to inform, request, order, complain, apply, or build goodwill. "
    "Business letters are official, legal records of communication carrying higher authority and "
    "permanence than emails. They represent the organisation's professional image to the outside world.<br/><br/>"
    "<b>PARTS OF A BUSINESS LETTER (12 Essential Parts):</b><br/>"
    "1. <b>Letterhead:</b> Organisation's name, logo, address, phone, email.<br/>"
    "2. <b>Date:</b> Full date: 15 May 2025 OR 15th May 2025.<br/>"
    "3. <b>Reference Number:</b> Optional internal tracking (Ref: HR/2025/041).<br/>"
    "4. <b>Inside Address:</b> Recipient's full name, title, and address.<br/>"
    "5. <b>Subject Line:</b> 'Sub: [Concise statement of purpose].'<br/>"
    "6. <b>Salutation:</b> Formal greeting — 'Dear Mr./Ms. [Surname],' or 'Dear Sir/Madam,'<br/>"
    "7. <b>Body:</b> Three paragraphs — Introduction (purpose), Details, Conclusion (action).<br/>"
    "8. <b>Complimentary Close:</b> 'Yours sincerely,' or 'Yours faithfully,'<br/>"
    "9. <b>Signature:</b> Handwritten signature.<br/>"
    "10. <b>Name and Designation:</b> Printed below signature.<br/>"
    "11. <b>Enclosures (Enc.):</b> List of attached documents.<br/>"
    "12. <b>CC (Copy To):</b> Others receiving copies.<br/><br/>"
    "<b>GOLDEN RULE — Salutation/Close Pairing:</b><br/>"
    "'Dear Sir/Madam' (unknown) → <b>Yours faithfully</b><br/>"
    "'Dear Mr./Ms. [Name]' (named) → <b>Yours sincerely</b><br/><br/>"
    "<b>TYPES OF BUSINESS LETTERS:</b><br/>"
    "1. <b>Enquiry Letter:</b> Requests information about products, services, prices, or terms. "
    "Must be specific with clear questions. Close: 'Yours faithfully.'<br/><br/>"
    "2. <b>Reply to Enquiry:</b> Responds with requested information, quotation, or catalogue. "
    "Should be prompt, complete, and highlight competitive advantages.<br/><br/>"
    "3. <b>Order Letter:</b> Formally places an order — specifies product, quantity, price, "
    "delivery terms, and payment. References previous quotation. Table format for itemised orders.<br/><br/>"
    "4. <b>Complaint Letter:</b> Registers formal dissatisfaction — specific problem, evidence, "
    "exact remedy required, deadline for response. Professional, firm, never rude.<br/><br/>"
    "5. <b>Adjustment Letter:</b> Response to complaint — acknowledge, apologise, propose resolution.<br/><br/>"
    "6. <b>Circular Letter:</b> Same information to multiple recipients — product announcements, "
    "price changes, new branch openings. Generic salutation.<br/><br/>"
    "7. <b>Sales Letter:</b> AIDA structure: Attention → Interest → Desire → Action. Persuasive, benefit-focused.<br/><br/>"
    "8. <b>Job Application Letter:</b> Sent with resume — specific post, qualifications matched to "
    "JD, key strengths, availability, enclosures list.<br/><br/>"
    "9. <b>Goodwill Letters:</b> Thank-you, congratulations, sympathy — builds long-term relationships.<br/><br/>"
    "<b>FORMATS OF BUSINESS LETTERS:</b><br/>"
    "1. <b>Full Block Style:</b> ALL parts aligned to LEFT margin. No indentation. "
    "Most modern, professional format. Preferred in USA and corporate globally.<br/><br/>"
    "2. <b>Modified Block Style:</b> Date, complimentary close, and signature are CENTRED or RIGHT. "
    "All other parts left-aligned. Body not indented. Traditional and widely used.<br/><br/>"
    "3. <b>Semi-Block (Indented) Style:</b> Like Modified Block but each body paragraph's first line "
    "is indented. Traditional British style.<br/><br/>"
    "<b>PRINCIPLES OF BUSINESS LETTER WRITING (The 7 C's Applied):</b><br/>"
    "1. Clarity — simple, direct language; no ambiguity.<br/>"
    "2. Conciseness — no redundant words; respect reader's time.<br/>"
    "3. Completeness — all information the reader needs; 5W1H.<br/>"
    "4. Correctness — verify all facts, names, figures, grammar.<br/>"
    "5. Concreteness — specific data and dates, not vague language.<br/>"
    "6. Courtesy — respectful, empathetic, polite tone throughout.<br/>"
    "7. Consideration — You-attitude; reader-centred framing.<br/><br/>"
    "<b>Conclusion:</b><br/>Business letters remain the gold standard of formal external communication. "
    "They carry legal weight, represent organisational credibility, and build lasting professional "
    "relationships. Every professional must master the art of writing clear, complete, correctly "
    "formatted business letters across all types.",
    "15", TEAL_L, "May 2025, Aug/Sep 2022, May 2023, May 2024"): story.append(x)

for x in q_block_b("B17",
    "Write a business letter ordering furniture for your office (with reference to earlier quotation/terms). (5 marks)",
    "An order letter formally places a request for goods. It must specify exact items, quantities, "
    "agreed prices, delivery terms, and reference the previous quotation. Full Block Style recommended.",
    "The following is a complete, exam-ready sample order letter:<br/><br/>",
    "5", AMBER, "May 2023"): story.append(x)

story.append(sample_box([
    "## SUNRISE TECHNOLOGIES PVT. LTD.",
    "# 45 Innovation Park, Koramangala, Bengaluru — 560 034",
    "# Tel: +91-80-4567-8900 | Email: procurement@sunrisetech.in",
    "---",
    "Ref: STP/PROC/2025/109",
    "22nd May 2025",
    "",
    "The Sales Manager",
    "Royal Office Furnishings Ltd.",
    "78 Industrial Estate, Peenya, Bengaluru — 560 058",
    "",
    "Sub: Order for Office Furniture — With reference to Quotation No. ROF/Q/2025/456 dated 15 May 2025",
    "",
    "Dear Sir/Madam,",
    "",
    "With reference to your quotation cited above and subsequent discussions with your",
    "representative, Mr. Anil Kumar, we are pleased to place the following order:",
    "",
    "  S.No | Item Description            | Qty | Unit Price | Total",
    "  1.   | Executive Office Chair      | 10  | Rs. 8,500  | Rs. 85,000",
    "  2.   | Conference Table (12-seater)| 1   | Rs. 45,000 | Rs. 45,000",
    "  3.   | Workstation Desk (standard) | 20  | Rs. 12,000 | Rs. 2,40,000",
    "  4.   | 4-Drawer Filing Cabinet     | 5   | Rs. 6,500  | Rs. 32,500",
    "                                           TOTAL: Rs. 4,02,500",
    "",
    "Please deliver the above items to our Koramangala address by 5th June 2025.",
    "Payment will be made within 15 days of delivery as per agreed terms.",
    "Kindly ensure GST invoice and delivery challan accompany the consignment.",
    "",
    "Please confirm receipt of this order at your earliest convenience.",
    "",
    "Yours faithfully,",
    "",
    "[Signature]",
    "Ms. Divya Menon",
    "Procurement Manager",
    "Sunrise Technologies Pvt. Ltd.",
], "SAMPLE ORDER LETTER — Full Block Style"))
story.append(sp(8))

for x in q_block_b("B18",
    "You are Rohan/Rohini, President of Resident Welfare Association. Write a letter to the Municipal Commissioner about increase in road accidents in your locality. (10 marks)",
    "This is a formal complaint letter to a government official. It requires: formal address, "
    "factual description of the problem, impact on residents, and specific requests for action. "
    "Full Block Style with a persuasive but respectful tone.",
    "Complete sample letter follows below:",
    "10", BLUE, "May 2024"): story.append(x)

story.append(sample_box([
    "## ROHINI SHARMA",
    "# President, Vasudev Nagar Residents Welfare Association",
    "# B-12, Vasudev Nagar, Sector 14, Faridabad — 121 007",
    "---",
    "25th May 2025",
    "",
    "The Municipal Commissioner",
    "Faridabad Municipal Corporation",
    "MCF Headquarters, NIT, Faridabad — 121 001",
    "",
    "Sub: Urgent Request for Safety Measures to Address Rise in Road Accidents",
    "       — Vasudev Nagar, Sector 14, Faridabad",
    "",
    "Dear Sir/Madam,",
    "",
    "I write on behalf of the 450 resident families of Vasudev Nagar, Sector 14,",
    "to bring to your urgent attention a deeply concerning rise in road accidents",
    "on our locality's main thoroughfare — Sector 14 Main Road.",
    "",
    "Over the past six months, we have recorded 14 accidents on this 1.2-km stretch,",
    "resulting in 3 fatalities and 11 serious injuries. The primary causes, as",
    "observed by residents, include:",
    "  1. Complete absence of speed breakers or traffic calming measures",
    "  2. Non-functional street lights creating dangerous conditions after 8 PM",
    "  3. No pedestrian crossing or zebra markings near the school and market",
    "  4. Potholes and uneven road surface causing vehicles to swerve unpredictably",
    "",
    "The situation has made our residents, particularly elderly members, schoolchildren,",
    "and morning walkers, genuinely fearful for their safety. Despite verbal complaints",
    "to the local ward office on 3 occasions, no action has been taken.",
    "",
    "We respectfully request that the Municipal Corporation take the following actions",
    "on an urgent basis:",
    "  1. Install 3 speed breakers at designated high-risk points within 2 weeks",
    "  2. Repair/replace all non-functional street lights within 1 week",
    "  3. Create a marked pedestrian crossing near Sunrise Public School",
    "  4. Repair the road surface and fill all potholes",
    "  5. Deploy a traffic constable at the main intersection during peak hours",
    "",
    "We are confident that these measures will significantly reduce accidents and",
    "restore the safety and confidence of our community. We are available to meet",
    "your office at any convenient time and can provide photographic documentation",
    "of the issues described above.",
    "",
    "We look forward to your urgent response and corrective action.",
    "",
    "Yours faithfully,",
    "",
    "[Signature]",
    "Rohini Sharma",
    "President, Vasudev Nagar Residents Welfare Association",
    "Contact: +91-98765-11223",
], "SAMPLE COMPLAINT LETTER TO MUNICIPAL COMMISSIONER"))
story.append(sp(8))

story.append(PageBreak())

# ── TOPIC: PRESENTATIONS ─────────────────────────────────────────────────
story.append(banner("TOPIC 7: PRESENTATIONS, INTERVIEWS & RESUME", INDIGO, 13))
story.append(sp(6))

for x in q_block_b("B19",
    "What is Presentation? Explain the tips for making the Presentation effective. (5/10 marks)",
    "Oral presentations combine content, structure, and delivery into a live communication experience. "
    "Making them effective requires systematic planning across all three dimensions.",
    "<b>Definition:</b><br/>An oral presentation is a formal, structured delivery of information to "
    "an audience using spoken words, supported by visual aids. It is the most visible test of "
    "professional communication skills — combining research, organisation, visual design, and "
    "live performance simultaneously.<br/><br/>"
    "<b>Structure of a Presentation:</b><br/>"
    "1. <b>Opening (15% of time):</b> Hook (shocking statistic / question / story / bold statement) → "
    "Credibility statement → Relevance (WIIFM) → Preview ('Today I will cover...')<br/>"
    "2. <b>Body (70% of time):</b> 3-5 main points maximum. Each point: State → Explain → "
    "Evidence/Example → Transition. Use signposting throughout.<br/>"
    "3. <b>Conclusion (15% of time):</b> Signal close → Summarise → Call to Action → Memorable final statement.<br/><br/>"
    "<b>Tips for Making a Presentation Effective:</b><br/>"
    "1. <b>Define Clear Purpose:</b> One-sentence objective: 'By the end, the audience will...' "
    "Everything serves this purpose.<br/><br/>"
    "2. <b>Analyse Your Audience:</b> Knowledge level, expectations, and needs determine "
    "vocabulary, depth, examples, and tone. A CEO needs summary + recommendations; "
    "engineers need methodology + data.<br/><br/>"
    "3. <b>Compelling Opening:</b> First 60 seconds determine engagement. Never start with "
    "'Good morning, my name is...' Use a hook that immediately creates interest.<br/><br/>"
    "4. <b>Apply the 6x6 Rule for Slides:</b> Maximum 6 bullet points per slide; "
    "maximum 6 words per bullet. One idea per slide. 24pt minimum font. Visuals over text.<br/><br/>"
    "5. <b>Dynamic Vocal Delivery:</b> Vary pitch, volume, and pace. Strategic pauses after "
    "key points. Eliminate filler words ('um', 'uh', 'like'). Enthusiasm is contagious.<br/><br/>"
    "6. <b>Eye Contact:</b> Hold gaze with individual audience members for 3-5 seconds. "
    "Creates personal connection even in large audiences.<br/><br/>"
    "7. <b>Storytelling:</b> Stories activate 7 brain regions vs 2 for pure data. "
    "Embed key messages in relatable stories — audiences remember stories long after facts are forgotten.<br/><br/>"
    "8. <b>Audience Engagement:</b> Rhetorical questions, polls, think-pair-share, demonstrations. "
    "An engaged audience is a receptive audience.<br/><br/>"
    "9. <b>Evidence-Based Content:</b> Support every claim with statistics, case studies, or expert quotes.<br/><br/>"
    "10. <b>Practice Extensively:</b> Full out-loud rehearsals, timed. Record yourself. "
    "Practise with visual aids. Final dress rehearsal in actual venue if possible.<br/><br/>"
    "11. <b>Technology Backup:</b> Test all equipment before presenting. "
    "Always have a printed backup of key content.<br/><br/>"
    "12. <b>Powerful Close:</b> Summarise → Call to Action → Memorable final statement. "
    "The close is the last thing the audience hears — make it count.<br/><br/>"
    "<b>Conclusion:</b> An effective presentation is 80% preparation and 20% live performance. "
    "Systematic planning, thorough practice, and audience-centred delivery transform ordinary "
    "presentations into compelling, memorable communication experiences.",
    "10", INDIGO, "May 2025, Aug/Sep 2022, May 2024, May 2023"): story.append(x)

for x in q_block_b("B20",
    "Discuss the importance of body language while participating in an interview. (5 marks)",
    "In interviews, non-verbal communication is assessed alongside verbal responses. "
    "Research shows 55% of communication impact comes from body language — making non-verbal "
    "management a critical interview skill.",
    "<b>Introduction:</b><br/>An interview is one of the highest-stakes communication events in a "
    "professional's life. Beyond what you say, HOW you present yourself physically creates an "
    "indelible impression. Research shows interviewers form initial impressions within 7 seconds "
    "— entirely through non-verbal cues — and often use the rest of the interview to confirm "
    "that first impression.<br/><br/>"
    "<b>Why Body Language Matters in Interviews:</b><br/>"
    "1. Interviewers consciously and unconsciously assess confidence, composure, and cultural fit "
    "through non-verbal signals.<br/>"
    "2. Verbal claims of confidence are contradicted by shaky hands, averted eyes, or nervous fidgeting.<br/>"
    "3. Positive body language makes interviewers feel comfortable and receptive — improving their "
    "evaluation of your verbal responses.<br/><br/>"
    "<b>Key Body Language Dos and Don'ts:</b><br/>"
    "1. <b>Entry:</b> Walk in with purpose — confident stride, shoulders back, upright posture. "
    "Knock and wait to be invited. Greet with a genuine smile.<br/>"
    "2. <b>Handshake:</b> Firm, 2-pump, with direct eye contact. Not limp (suggests weakness) "
    "or crushing (suggests aggression). The handshake creates the first tactile impression.<br/>"
    "3. <b>Posture:</b> Sit upright with a slight forward lean — signals interest and confidence. "
    "Avoid: slouching (disinterest), crossing arms (defensiveness), leaning back (arrogance).<br/>"
    "4. <b>Eye Contact:</b> Maintain steady, natural eye contact — 3-5 seconds per contact point. "
    "In panel interviews: distribute eye contact equally across all panellists. "
    "Avoid: staring (intimidating) or constant avoidance (suggests dishonesty).<br/>"
    "5. <b>Hand Gestures:</b> Natural, open hand movements reinforce key points. "
    "Avoid: fidgeting, touching face/hair, pen clicking, drumming fingers — all signal nervousness.<br/>"
    "6. <b>Facial Expressions:</b> Engaged, nodding, genuinely smiling when appropriate. "
    "A blank expression makes you seem disinterested or robotic.<br/>"
    "7. <b>Feet:</b> Both feet flat on the floor. Avoid bouncing legs — creates distraction.<br/>"
    "8. <b>Voice (Paralanguage):</b> Speak at a moderate, confident pace. Avoid rushing "
    "(nervousness signal) or speaking too softly (lack of conviction).<br/><br/>"
    "<b>Conclusion:</b> In interviews, body language is your silent CV. It either confirms or "
    "contradicts everything you say verbally. Master the physical performance of confidence, "
    "interest, and professionalism — even while managing nerves — and your interview scores "
    "will consistently improve.",
    "5", PURPLE_M, "May 2024"): story.append(x)

for x in q_block_b("B21",
    "How would you plan for conducting the interview? What necessary preparations should be made before conducting the interview? (10 marks)",
    "Interview planning is relevant from BOTH sides — the interviewer preparing to conduct, and the "
    "interviewee preparing to perform. This question is typically from the interviewee's perspective "
    "but may address both. A 5-phase preparation strategy covers all aspects.",
    "<b>Introduction:</b><br/>Interview success is 80% preparation. The difference between candidates "
    "who perform well and those who do not is almost always rooted in preparation quality, "
    "not raw talent. A systematic 5-phase preparation strategy covers every dimension.<br/><br/>"
    "<b>PHASE 1 — RESEARCH (Company, Role, Industry):</b><br/>"
    "&#9654; Company: history, products/services, mission, culture (Glassdoor), recent news, financials.<br/>"
    "&#9654; Role: analyse every word in the job description; map each requirement to your experience.<br/>"
    "&#9654; Industry: trends, challenges, key players — shows strategic awareness.<br/>"
    "&#9654; Interviewer: LinkedIn profile — their background, areas of expertise, career path.<br/>"
    "Time investment: 3-4 hours minimum for any significant role.<br/><br/>"
    "<b>PHASE 2 — KNOW YOURSELF (Self-Analysis):</b><br/>"
    "&#9654; Review your entire résumé line by line — be ready to elaborate on every item.<br/>"
    "&#9654; Identify your top 5 strengths with specific, quantified examples for each.<br/>"
    "&#9654; Identify 2-3 genuine weaknesses with active improvement strategies.<br/>"
    "&#9654; Craft your career narrative: where have you been → where are you → where are you going → "
    "why this specific role at this specific company?<br/>"
    "&#9654; Research salary market rate: LinkedIn Salary, Glassdoor, Naukri — prepare a range.<br/><br/>"
    "<b>PHASE 3 — PREPARE STAR STORIES:</b><br/>"
    "Prepare 8-10 STAR (Situation-Task-Action-Result) stories covering: leadership, teamwork, "
    "conflict resolution, failure + learning, achievement, initiative, creative problem-solving, "
    "handling pressure, client management, and learning agility. Each story: 1.5-2 minutes maximum.<br/><br/>"
    "<b>PHASE 4 — PRACTICE DELIVERY:</b><br/>"
    "&#9654; Mock interviews with a friend, mentor, or recorded alone.<br/>"
    "&#9654; Time your answers — 1.5-2 minutes per question; identify which need tightening.<br/>"
    "&#9654; Practise non-verbals: firm handshake, confident posture, eye contact — in front of a mirror.<br/>"
    "&#9654; Record video of yourself — identify and eliminate filler words ('um', 'uh', 'like').<br/>"
    "&#9654; Prepare 3-4 intelligent questions to ask the interviewer.<br/><br/>"
    "<b>PHASE 5 — LOGISTICS PREPARATION:</b><br/>"
    "&#9654; Plan route to venue — test journey if possible; allow extra time.<br/>"
    "&#9654; Arrive 10-15 minutes early (not 30+ minutes — awkward and pressuring to staff).<br/>"
    "&#9654; Professional attire: ironed, clean, appropriate for company culture (when in doubt, more formal).<br/>"
    "&#9654; Documents: 3 copies of résumé, original certificates, ID proof, notepad, pen.<br/>"
    "&#9654; Silence phone completely before entering the building. Charge it fully the night before.<br/>"
    "&#9654; Get 8 hours sleep. Eat a light, nutritious meal before. Avoid alcohol the evening before.<br/><br/>"
    "<b>During the Interview (Brief):</b><br/>"
    "Listen fully before answering. Use STAR method. Moderate, clear speech. Confident body language. "
    "Stay positive about past employers. Ask your prepared questions. Express enthusiasm clearly.<br/><br/>"
    "<b>After the Interview:</b><br/>"
    "Send professional thank-you email within 24 hours. Reference a specific topic discussed. "
    "Reiterate enthusiasm and fit. Follow up professionally on the stated timeline.<br/><br/>"
    "<b>Conclusion:</b><br/>Interview preparation is not a checklist — it is a mindset of thorough, "
    "disciplined readiness. The candidate who has researched the company, prepared specific "
    "evidence-based stories, and practised delivery will almost always outperform the equally "
    "talented candidate who 'just wings it.'",
    "10", BLUE, "May 2025, Aug/Sep 2022"): story.append(x)

story.append(PageBreak())

# ── TOPIC: RESUME & COVER LETTER ─────────────────────────────────────────
story.append(banner("TOPIC 8: DRAFT A RÉSUMÉ AND COVERING LETTER — COMPLETE SAMPLE", MAROON, 13))
story.append(sp(6))

story.append(Paragraph("<b>Q: Draft a resume and covering letter for your desired job profile in your dream company. (15 marks)</b>",
                       S("QB_RES", fontSize=11, textColor=WHITE, fontName="Helvetica-Bold",
                         leading=14, spaceBefore=0, spaceAfter=0)))
story.append(Paragraph("&#128197; Asked in: May 2025, Aug/Sep 2022, May 2024 — EVERY PAPER",
                       S("APP_R", fontSize=9, textColor=colors.HexColor("#ffe082"),
                         fontName="Helvetica-Oblique", leading=12, spaceBefore=4, spaceAfter=6)))

hdr_r = [[Paragraph("<b>Q: Draft a resume and covering letter for your desired job profile in your dream company. (15 marks)</b>",
                    S("QR_H", fontSize=11, textColor=WHITE, fontName="Helvetica-Bold", leading=15))]]
htr = Table(hdr_r, colWidths=[16.5*cm])
htr.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1), MAROON),
    ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),
    ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
]))
story.append(htr)
story.append(sp(4))

bg_r = [[Paragraph("<b>&#128218; Topic Background:</b> A résumé is a concise, targeted professional document "
                   "summarising qualifications and achievements for a specific job. A cover letter introduces "
                   "the applicant and makes a personalised case for candidacy. Together they form the most "
                   "consequential career documents you will ever write. Key principles: Achievement bullets "
                   "with numbers, ATS-optimised keywords, You-attitude in cover letter, specific not generic.",
                   S("TBG_R", fontSize=10, textColor=INDIGO, fontName="Helvetica",
                     leading=14, alignment=TA_JUSTIFY))]]
bgt = Table(bg_r, colWidths=[16.5*cm])
bgt.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1), INDIGO_L),("BOX",(0,0),(-1,-1),1, INDIGO),
    ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
    ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
]))
story.append(bgt)
story.append(sp(6))
story.append(sample_box([
    "## VIKRAM PATEL",
    "# vikram.patel@gmail.com  |  +91-98123-45678  |  Hyderabad, TS",
    "# linkedin.com/in/vikrampatel  |  github.com/vikrampatel",
    "---",
    "# PROFESSIONAL SUMMARY",
    "Data Science Engineer with B.Tech CSE (9.2 CGPA, NIT Warangal, 2025)",
    "specialising in ML, Python, and SQL. Built predictive model reducing customer",
    "churn by 31% during internship. AWS Certified. Seeking Data Scientist role",
    "at a product-driven analytics organisation.",
    "---",
    "# WORK EXPERIENCE",
    "Data Science Intern | InfoAnalytics Pvt. Ltd. | Hyderabad | Jan–Jul 2025",
    "  • Developed XGBoost customer churn prediction model (91% accuracy), reducing",
    "    churn by 31% and saving estimated Rs. 1.2 crore in annual revenue",
    "  • Automated weekly reporting pipeline using Python + SQL, saving 18 hrs/month",
    "  • Built Tableau dashboard adopted by 3 business teams for real-time KPI tracking",
    "",
    "ML Research Intern | IIT Hyderabad | May–Jul 2024",
    "  • Fine-tuned BERT model for sentiment analysis on regional languages (Telugu/Hindi)",
    "  • Achieved 88% F1-score on 50,000-sample test set; presented findings at lab seminar",
    "---",
    "# EDUCATION",
    "B.Tech, Computer Science Engineering",
    "  NIT Warangal  |  2025  |  CGPA: 9.2/10  |  Rank: 2 of 160",
    "---",
    "# TECHNICAL SKILLS",
    "Languages : Python, SQL, R, JavaScript",
    "ML/AI     : scikit-learn, XGBoost, TensorFlow, BERT, LangChain",
    "Tools     : Tableau, Power BI, Apache Spark, Git, Docker",
    "Cloud     : AWS (S3, EC2, SageMaker), Google BigQuery",
    "---",
    "# KEY PROJECTS",
    "FraudShield — Real-Time Payment Fraud Detection | github.com/vikram/fraudshield",
    "  • Ensemble model (RF + XGBoost) flagging 97.3% of fraudulent transactions",
    "  • Processes 10,000 transactions/sec on AWS Lambda; 0.2% false positive rate",
    "---",
    "# CERTIFICATIONS",
    "  • AWS Certified Machine Learning Specialty | Amazon | 2025",
    "  • Google Professional Data Engineer | Google | 2024",
    "  • Deep Learning Specialisation | deeplearning.ai / Coursera | 2024",
    "---",
    "# ACHIEVEMENTS",
    "  • 1st Prize — Smart India Hackathon 2024 (AI/ML Track, 15,000 participants)",
    "  • Published: 'Low-Resource NLP for Telugu Sentiment Analysis' — EMNLP 2024",
    "",
    "References available upon request.",
], "SAMPLE RÉSUMÉ — DATA SCIENTIST (Fresh Graduate, 1 Page)"))
story.append(sp(8))
story.append(sample_box([
    "## VIKRAM PATEL",
    "# vikram.patel@gmail.com  |  +91-98123-45678  |  Hyderabad, TS",
    "---",
    "25th May 2025",
    "",
    "Ms. Ananya Krishnan",
    "Head of Data Science",
    "Flipkart Internet Pvt. Ltd.",
    "Embassy Tech Village, Outer Ring Road, Bengaluru — 560 103",
    "",
    "Sub: Application for Data Scientist (L4) — Ref: FK/DS/2025/178",
    "",
    "Dear Ms. Krishnan,",
    "",
    "When my customer churn prediction model at InfoAnalytics identified a segment",
    "of 12,000 at-risk users that had been completely invisible to the business team,",
    "the subsequent targeted retention campaign saved Rs. 1.2 crore in annual revenue",
    "within three months. That experience of turning data into measurable business",
    "value is exactly what drew me to Flipkart's data science mandate.",
    "",
    "Your job description calls for expertise in XGBoost, Python, SQL, and Spark —",
    "tools I use daily. In my 7 months at InfoAnalytics, I built end-to-end ML",
    "pipelines processing 10,000+ transactions per second, automated reporting saving",
    "18 hours monthly, and delivered dashboards adopted by 3 business teams. My NIT",
    "Warangal research internship at IIT Hyderabad, where I published in EMNLP 2024,",
    "demonstrates the academic rigour your senior research problems require.",
    "",
    "What excites me most about Flipkart is the scale: 400 million products, 100+",
    "million customers, and recommendation systems that must perform under extreme",
    "concurrency. I have been following your engineering blog for two years —",
    "particularly the 2024 series on real-time fraud detection at scale, which",
    "directly inspired my own FraudShield project.",
    "",
    "I would welcome the opportunity to discuss how my skills could contribute to",
    "Flipkart's data science roadmap. I am available for interview at your",
    "convenience and can join within 30 days of offer.",
    "",
    "Yours sincerely,",
    "",
    "[Signature]",
    "Vikram Patel",
    "",
    "Enc: 1. Résumé   2. AWS ML Certification   3. EMNLP 2024 Publication",
], "SAMPLE COVER LETTER — DATA SCIENTIST APPLICATION"))
story.append(sp(8))

story.append(PageBreak())

# ── TOPIC: CRITICAL THINKING & EQ ────────────────────────────────────────
story.append(banner("TOPIC 9: CRITICAL THINKING, EQ & SPECIAL QUESTIONS", PURPLE_M, 13))
story.append(sp(6))

for x in q_block_b("B22",
    "Discuss some important techniques of Critical Thinking and Problem Solving. (15 marks)",
    "Critical thinking and problem solving are the two most sought-after cognitive skills in the "
    "21st century workforce. They enable professionals to navigate complexity, make sound decisions, "
    "and create innovative solutions.",
    "<b>PART A — CRITICAL THINKING:</b><br/><br/>"
    "<b>Definition:</b> Critical thinking is the disciplined, systematic process of actively analysing, "
    "evaluating, and synthesising information gathered through observation, experience, or reasoning "
    "to form well-justified conclusions and decisions. It opposes passive, uncritical acceptance of information.<br/><br/>"
    "<b>The Critical Thinking Process:</b><br/>"
    "1. Identify and define the problem/question precisely.<br/>"
    "2. Gather relevant, credible information (RAVEN test: Relevance, Authority, View, Evidence, Newness).<br/>"
    "3. Analyse and evaluate — identify assumptions, logical fallacies, biases in the data.<br/>"
    "4. Consider multiple perspectives — actively seek views that contradict your own.<br/>"
    "5. Draw well-reasoned conclusions — state confidence level.<br/>"
    "6. Communicate and apply — articulate reasoning; remain open to revision.<br/><br/>"
    "<b>Key Techniques of Critical Thinking:</b><br/>"
    "1. <b>Socratic Questioning:</b> Systematic questioning to probe assumptions, uncover evidence, "
    "and expose logical weaknesses. 'What is the evidence for this claim?' 'What assumptions am I making?' "
    "'What are alternative explanations?' 'What are the implications if I'm wrong?'<br/><br/>"
    "2. <b>Root Cause Analysis (5 Whys):</b> Ask 'Why?' five times to get past symptoms to underlying "
    "causes. Example: Sales declined → Why? Team morale dropped → Why? Manager resigned → "
    "Why? Company culture issues → Why? No feedback culture → Why? No management training.<br/><br/>"
    "3. <b>SWOT Analysis:</b> Strengths, Weaknesses, Opportunities, Threats. Provides structured "
    "evaluation framework for decisions and strategic situations.<br/><br/>"
    "4. <b>Devil's Advocate:</b> Deliberately argue against the dominant view to expose weaknesses "
    "and assumptions. Prevents groupthink and overconfidence.<br/><br/>"
    "5. <b>Six Thinking Hats (Edward de Bono):</b> Examines a problem from 6 perspectives: "
    "White (facts), Red (emotions), Black (caution), Yellow (optimism), Green (creativity), "
    "Blue (process). Ensures balanced, multi-dimensional analysis.<br/><br/>"
    "6. <b>Logical Fallacy Recognition:</b> Identifying flawed reasoning: Ad hominem (attacking "
    "person not argument), False dichotomy (only two options), Hasty generalisation (too few "
    "data points), Straw man (misrepresenting opponent's position).<br/><br/>"
    "7. <b>Evidence Triangulation:</b> Verify claims through multiple independent sources before "
    "accepting them. If three credible sources agree, confidence increases significantly.<br/><br/>"
    "<b>PART B — PROBLEM SOLVING:</b><br/><br/>"
    "<b>Definition:</b> Problem solving is the process of identifying, analysing, and resolving "
    "situations or challenges that stand between the current state and a desired goal.<br/><br/>"
    "<b>The Problem-Solving Process (7 Steps):</b><br/>"
    "1. <b>Define the Problem:</b> State precisely what is wrong and what 'solved' looks like. "
    "Most failed problem-solving efforts fail here — solving the wrong problem.<br/>"
    "2. <b>Gather Information:</b> Collect relevant data, stakeholder perspectives, and constraints.<br/>"
    "3. <b>Identify Root Causes:</b> Use 5 Whys, fishbone diagram, or process mapping to find the "
    "actual cause — not just symptoms.<br/>"
    "4. <b>Generate Solutions (Divergent Thinking):</b> Brainstorm without judgment — quantity before "
    "quality. Defer evaluation. Combine and build on ideas.<br/>"
    "5. <b>Evaluate Solutions (Convergent Thinking):</b> Assess each option against: feasibility, "
    "cost, time, risk, and alignment with the goal. Decision matrix or cost-benefit analysis.<br/>"
    "6. <b>Implement:</b> Develop an action plan with clear responsibilities and timelines.<br/>"
    "7. <b>Review and Learn:</b> Measure the outcome. What worked? What would you do differently?<br/><br/>"
    "<b>Problem-Solving Techniques:</b><br/>"
    "1. <b>Brainstorming:</b> Group idea generation — no criticism allowed during generation phase.<br/>"
    "2. <b>Design Thinking:</b> Empathise → Define → Ideate → Prototype → Test. Human-centred approach.<br/>"
    "3. <b>Fishbone Diagram (Ishikawa):</b> Visual tool mapping causes of a problem into categories: "
    "People, Process, Technology, Environment, Materials.<br/>"
    "4. <b>Mind Mapping:</b> Visual brainstorming that shows relationships between ideas.<br/>"
    "5. <b>Decision Matrix:</b> Weighted scoring of options against criteria — reduces subjectivity.<br/>"
    "6. <b>Lateral Thinking (de Bono):</b> Approaching problems from unexpected angles; "
    "challenging assumptions about how things must be done.<br/><br/>"
    "<b>Barriers to Critical Thinking and Problem Solving:</b><br/>"
    "Confirmation bias · Groupthink · Overconfidence (Dunning-Kruger effect) · "
    "Emotional reasoning · Analysis paralysis · False dichotomy · Cognitive rigidity<br/><br/>"
    "<b>Conclusion:</b><br/>Critical thinking and problem solving are the cognitive foundation of "
    "professional effectiveness. In a world of information overload, algorithmic bias, and rapid "
    "change, the professional who can think clearly, question assumptions, evaluate evidence, "
    "and generate innovative solutions is invaluable to any organisation. These are learnable "
    "skills — they develop through deliberate practice, intellectual humility, and the courage "
    "to challenge comfortable assumptions.",
    "15", PURPLE_M, "May 2023"): story.append(x)

for x in q_block_b("B23",
    "Draft a speech in favour of democratic values upheld in the Constitution of India. (5 marks)",
    "This is a persuasive speech on a civic/social topic. It requires: formal speech structure "
    "(hook → thesis → arguments → conclusion), patriotic but balanced tone, and specific reference "
    "to constitutional provisions. Approximately 300-350 words for 5 marks.",
    "The following is a complete, exam-ready speech draft:<br/><br/>",
    "5", GREEN_M, "May 2023"): story.append(x)

story.append(sample_box([
    "## SPEECH IN FAVOUR OF DEMOCRATIC VALUES IN THE CONSTITUTION OF INDIA",
    "---",
    "'The Constitution is not a mere lawyers' document; it is a vehicle of life,",
    "and its spirit is always the spirit of an age.' — Dr. B.R. Ambedkar",
    "",
    "Respected faculty members, honoured judges, and my dear fellow students —",
    "",
    "Namaste.",
    "",
    "Seventy-five years ago, on the 26th of January 1950, a remarkable document",
    "came into force — not merely a set of rules, but a solemn promise to 340",
    "million people that they would be free, equal, and empowered. That document",
    "was the Constitution of India.",
    "",
    "I stand before you today to affirm my conviction that the democratic values",
    "enshrined in our Constitution are not just relevant — they are irreplaceable",
    "pillars of our nation's identity and future.",
    "",
    "Our Constitution begins with the word 'WE' — not the government, not the",
    "powerful, not any religion or caste — but WE, THE PEOPLE. In those two words",
    "lies the entire philosophy of Indian democracy: sovereignty belongs to the",
    "citizens.",
    "",
    "Consider the values our founders enshrined:",
    "  JUSTICE — social, economic, and political. No citizen left behind.",
    "  LIBERTY — of thought, expression, faith, and conscience. The right to think",
    "  differently is the engine of all progress.",
    "  EQUALITY — before the law. Rich or poor, powerful or marginalised,",
    "  the law treats every Indian the same.",
    "  FRATERNITY — the constitutional demand that we see each other as family,",
    "  as fellow citizens, beyond religion, caste, and region.",
    "",
    "These are not merely ideals. They are the architecture of a nation that has",
    "held together in diversity that would have fractured any lesser vision.",
    "",
    "Yes — our democracy is imperfect. Yes — our institutions sometimes fail us.",
    "But the answer to an imperfect democracy is never less democracy — it is",
    "more democracy. It is deeper engagement, louder voices, and stronger demands",
    "that our Constitution's promise be fulfilled.",
    "",
    "Dr. Ambedkar warned us: 'Constitutional morality is not a natural sentiment.",
    "It has to be cultivated.' Let us be the generation that cultivates it —",
    "that defends freedom of the press, upholds the independence of the judiciary,",
    "participates actively in elections, and refuses to let any voice be silenced.",
    "",
    "India's Constitution is our most powerful inheritance and our most",
    "important responsibility. Let us honour it — not just on Republic Day,",
    "but in every choice we make as citizens.",
    "",
    "Jai Hind. Jai Bharat.",
    "Thank you.",
], "SAMPLE SPEECH — DEMOCRATIC VALUES IN THE CONSTITUTION"))
story.append(sp(8))

for x in q_block_b("B24",
    "Write a descriptive/analytical report on the Impact of ChatGPT on Academia and Industry. (15 marks)",
    "Proposal and analytical reports demonstrate formal report writing skills. This question tests "
    "knowledge of both the content domain (AI/ChatGPT) and the formal report structure. "
    "Apply all elements: Title → Executive Summary → Introduction → Findings → Analysis → Conclusion → Recommendations.",
    "Below is a complete sample analytical report:<br/><br/>",
    "15", AMBER, "May 2023"): story.append(x)

story.append(sample_box([
    "## ANALYTICAL REPORT: IMPACT OF CHATGPT ON ACADEMIA AND INDUSTRY",
    "---",
    "# Report Title  : Impact of ChatGPT on Academia and Industry — Opportunities and Challenges",
    "# Prepared by   : [Your Name], [Department], [Institution/Organisation]",
    "# Date          : May 2025",
    "# Submitted to  : [Professor Name / Manager Name]",
    "---",
    "# EXECUTIVE SUMMARY",
    "This report analyses the impact of ChatGPT, OpenAI's large language model,",
    "on academic institutions and industries. Key findings indicate that ChatGPT",
    "offers significant productivity gains and educational support but raises",
    "serious concerns around academic integrity, job displacement, and information",
    "accuracy. Recommendations include policy development, AI literacy training,",
    "and hybrid human-AI workflows.",
    "---",
    "# 1. INTRODUCTION",
    "ChatGPT, launched by OpenAI in November 2022, reached 100 million users within",
    "60 days — the fastest-growing consumer application in history. It represents",
    "a qualitative leap in AI capability, capable of producing coherent text, code,",
    "analysis, and creative content across virtually every domain. Its rapid adoption",
    "in both academic and industrial contexts has made understanding its impact urgent.",
    "",
    "This report examines: (a) its benefits and applications in academia and industry,",
    "(b) the challenges and risks it creates, and (c) strategic recommendations for",
    "stakeholders.",
    "---",
    "# 2. IMPACT ON ACADEMIA",
    "",
    "2.1 BENEFITS:",
    "  • Personalised tutoring — explains complex concepts at the student's level 24/7",
    "  • Research assistance — literature summaries, bibliography suggestions",
    "  • Writing support — drafts, feedback, grammar correction for ESL students",
    "  • Accessibility — supports differently-abled learners with adapted content",
    "",
    "2.2 CHALLENGES:",
    "  • Academic dishonesty — students submitting AI-generated work as their own",
    "  • Assessment validity — traditional essays and assignments easily circumvented",
    "  • Hallucinations — ChatGPT produces confidently stated but factually incorrect",
    "    citations and statistics (documented error rate: ~30% for factual claims)",
    "  • Skill atrophy — over-reliance may impair critical thinking and writing development",
    "---",
    "# 3. IMPACT ON INDUSTRY",
    "",
    "3.1 BENEFITS:",
    "  • Productivity: McKinsey (2023) estimates AI could add $4.4 trillion annually",
    "    to global economy; software developers using Copilot (GitHub's AI tool) show",
    "    55% productivity increase",
    "  • Customer service: AI chatbots handle up to 80% of routine queries",
    "  • Content creation: marketing, documentation, legal drafting, code generation",
    "  • Data analysis: natural language querying of databases",
    "",
    "3.2 CHALLENGES:",
    "  • Job displacement: World Economic Forum estimates 85 million jobs may be",
    "    disrupted by 2025; copywriters, entry-level coders, data entry roles at risk",
    "  • Data privacy: corporate data input into ChatGPT may breach confidentiality",
    "  • Bias and misinformation: model trained on internet data inherits biases",
    "  • Over-reliance: decisions made on AI output without human verification",
    "---",
    "# 4. CONCLUSIONS",
    "  1. ChatGPT is transforming both academia and industry at unprecedented speed",
    "  2. Benefits (productivity, accessibility, personalisation) are substantial",
    "  3. Risks (dishonesty, displacement, inaccuracy) require active management",
    "  4. The technology itself is neutral — impact depends on governance frameworks",
    "---",
    "# 5. RECOMMENDATIONS",
    "  For Academia:",
    "  1. Develop and communicate clear AI use policies for assignments/assessments",
    "  2. Redesign assessments to test higher-order thinking that AI cannot replicate",
    "  3. Integrate AI literacy into curricula — teach students to use AI critically",
    "",
    "  For Industry:",
    "  1. Establish AI governance frameworks and data input policies",
    "  2. Invest in reskilling programmes for workers in AI-impacted roles",
    "  3. Mandate human verification for all AI-generated outputs in high-stakes domains",
    "---",
    "# REFERENCES",
    "  • McKinsey Global Institute (2023). The Economic Potential of Generative AI.",
    "  • World Economic Forum (2023). Future of Jobs Report.",
    "  • OpenAI (2023). GPT-4 Technical Report.",
], "SAMPLE ANALYTICAL REPORT — ChatGPT Impact on Academia and Industry"))
story.append(sp(8))

story.append(PageBreak())

# ── QUICK REVISION TABLE ──────────────────────────────────────────────────
story.append(banner("&#9733;  PYQ MASTER REVISION — ALL QUESTIONS & KEY ANSWERS AT A GLANCE  &#9733;", DARK))
story.append(sp(10))

rev_data = [
    [Paragraph("<b>Question / Topic</b>", S("TH1", fontSize=9.5, fontName="Helvetica-Bold",
                                             textColor=WHITE, alignment=TA_CENTER, leading=13)),
     Paragraph("<b>Key Answer Points (Memorise These)</b>",
               S("TH2", fontSize=9.5, fontName="Helvetica-Bold",
                 textColor=WHITE, alignment=TA_CENTER, leading=13)),
     Paragraph("<b>Papers</b>", S("TH3", fontSize=9, fontName="Helvetica-Bold",
                                   textColor=WHITE, alignment=TA_CENTER, leading=13))],
    ["Negotiation Skills","BATNA · ZOPA · Interests > Positions · Fisher & Ury · Win-Win","ALL 4"],
    ["Emotional Intelligence","Goleman's 5: Self-Aware → Self-Regulate → Motivate → Empathy → Social Skills","ALL 4"],
    ["Meta-Communication","Comm. about comm. · Content + Relationship levels · Bateson · Watzlawick","ALL 4"],
    ["Paralanguage","HOW not WHAT · Trager · Pitch/Volume/Rate/Tone/Pause · 38% impact (Mehrabian)","ALL 4"],
    ["7 C's of Comm.","Clarity·Concise·Complete·Correct·Concrete·Courtesy·Consideration + examples","2023,2024"],
    ["Report Writing (15)","13 parts: Title→Transmittal→ToC→ExecSumm→Intro→Method→Findings→Analysis→Concl→Rec→Ref→App","ALL 4"],
    ["Business Letters (15)","12 parts · 3 formats (Full/Modified/Semi-block) · 9 types · Golden rule: Faithfully/Sincerely","ALL 4"],
    ["Presentation","Purpose→Audience→Structure(15-70-15%) · 6x6 rule · Delivery skills · 10-20-30 rule","ALL 4"],
    ["Resume+Cover Letter","9 components · 10 golden rules · Achievement not duty · ATS · Hook opening in CL","ALL 4"],
    ["Leadership","Learnable · EQ=67% leadership performance · Trait/Behavioural/Situational theories · Attributes","ALL 4"],
    ["Soft Skills","Non-technical · Communication+EQ+Teamwork top 3 · Enhance employability · LinkedIn 92%","2023,2025"],
    ["Group Discussion","6-12 people · No leader · PREP format · Evaluators assess 8 criteria · Dos&Don'ts","ALL 4"],
    ["Personality Dev.","Heredity+Env+Situation · 8 development steps · SMART goals · Self-awareness","2022,2025"],
    ["Proxemics","Hall (1966) · 4 zones: Intimate(0-18in) Personal(4ft) Social(12ft) Public(12ft+)","ALL 4"],
    ["Critical Thinking","6-step process · Socratic Q · 5 Whys · Devil's Advocate · Six Hats (de Bono)","2022,2023"],
    ["Listening Types","10 types: Active/Passive/Empathetic/Critical/Appreciative/Info/Discriminative/Selective/Pseudo/Deep","2023,2024"],
    ["Non-Verbal Comm.","Mehrabian 55-38-7 rule · Kinesics · Proxemics · Haptics · Paralanguage · Chronemics","2023,2024"],
    ["Telephonic Comm.","Tone>Words · Professional greeting · Active listen · Difficult callers: Calm+Empathise+Solve","2022"],
    ["Interview Prep","5 phases: Research→Self-Analysis→STAR→Practice→Logistics · STAR method key","ALL 4"],
    ["Body Language Interview","Handshake · Eye contact(3-5s) · Upright posture · Open hands · Moderate voice","2024"],
    ["Communication & Dev.","7 components · Economic+Governance+Healthcare+Social+Digital roles explained","2022,2025"],
    ["Types of Reports","Formal/Informal · Info/Analytical/Research · Periodic/Special · Internal/External","2022,2023"],
    ["Org. Communication","Downward/Upward/Horizontal/Diagonal + Grapevine (4 chain types)","2024"],
    ["Speech vs Debate","Speech: monologue, no opponent · Debate: structured opposition, affirmative vs negative","2022,2024"],
    ["Work Ethics","Integrity·Reliability·Diligence·Accountability·Professionalism·Confidentiality","2022,2025"],
]
rev_t = Table(rev_data, colWidths=[4.5*cm, 9.5*cm, 2.5*cm])
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

# Final strategy box
strat_d = [[Paragraph(
    "<b>EXAM STRATEGY: HOW TO SCORE MAXIMUM MARKS &#9733;</b><br/>"
    "&#9654; <b>Part A (15 marks):</b> Write EXACTLY 50 words for each 1.5-mark question. "
    "Include: definition + key elements/components + one example/application. No padding needed.<br/>"
    "&#9654; <b>Part B — Choose wisely:</b> Always attempt: Q on Report Writing (15 marks), "
    "Q on Business Letters (15 marks), and Q on Resume+Cover Letter (15 marks) — "
    "these are the three most predictable high-mark questions.<br/>"
    "&#9654; <b>15-mark answers:</b> Minimum 7-8 headings/sub-sections, numbered points, "
    "2 examples, and a proper introduction + conclusion. Aim for 700-900 words.<br/>"
    "&#9654; <b>Sample letters/resume:</b> Always write a full sample even if not asked — "
    "it demonstrates mastery and earns bonus marks in practice.<br/>"
    "&#9654; <b>Presentation question:</b> Always include 6x6 rule, 3-part structure (15-70-15%), "
    "and at least 8-10 specific tips. Never write fewer than 6 tips.",
    S("STR", fontSize=10.5, textColor=DARK, fontName="Helvetica",
      alignment=TA_LEFT, leading=17))]]
st_t = Table(strat_d, colWidths=[17*cm])
st_t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1), GOLD_L),("BOX",(0,0),(-1,-1),2, GOLD),
    ("TOPPADDING",(0,0),(-1,-1),14),("BOTTOMPADDING",(0,0),(-1,-1),14),
    ("LEFTPADDING",(0,0),(-1,-1),16),("RIGHTPADDING",(0,0),(-1,-1),16),
]))
story.append(st_t)
story.append(sp(10))

final_d = [[Paragraph(
    "&#9733; YOU NOW HAVE EVERY QUESTION FROM EVERY PAPER — FULLY ANSWERED &#9733;<br/>"
    "Study Smart · Revise the Quick Table · Write Full Answers · ALL THE BEST!",
    S("FIN", fontSize=13, textColor=WHITE, fontName="Helvetica-Bold",
      alignment=TA_CENTER, leading=20))]]
fin_t = Table(final_d, colWidths=[17*cm])
fin_t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1), DARK),
    ("TOPPADDING",(0,0),(-1,-1),16),("BOTTOMPADDING",(0,0),(-1,-1),16),
    ("LEFTPADDING",(0,0),(-1,-1),16),("RIGHTPADDING",(0,0),(-1,-1),16),
]))
story.append(fin_t)

doc = SimpleDocTemplate(
    OUTPUT_PATH, pagesize=A4,
    leftMargin=1.8*cm, rightMargin=1.8*cm,
    topMargin=2*cm, bottomMargin=2.2*cm,
    title="PYQ Master Answers — OEC-CS-601(I)",
    author="OEC-CS-601(I) Soft Skills"
)
doc.build(story, canvasmaker=NC)
print(f"PDF created: {OUTPUT_PATH}")