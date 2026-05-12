from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, HRFlowable)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

W, H = A4

# ── Colours ──────────────────────────────────────────────────────────────────
C = {
    'dark_navy' : HexColor('#0d1b2a'),
    'navy'      : HexColor('#1b2a4a'),
    'blue'      : HexColor('#1e3a5f'),
    'med_blue'  : HexColor('#2e5d9e'),
    'accent'    : HexColor('#e8edf5'),
    'teal'      : HexColor('#00695c'),
    'teal_bg'   : HexColor('#e0f2f1'),
    'purple'    : HexColor('#4a148c'),
    'purple_bg' : HexColor('#f3e5f5'),
    'orange'    : HexColor('#e65100'),
    'orange_bg' : HexColor('#fff3e0'),
    'green'     : HexColor('#1b5e20'),
    'green_bg'  : HexColor('#e8f5e9'),
    'red'       : HexColor('#b71c1c'),
    'red_bg'    : HexColor('#fce4ec'),
    'yellow_bg' : HexColor('#fffde7'),
    'grey_bg'   : HexColor('#f5f5f5'),
    'dark_text' : HexColor('#212121'),
    'med_text'  : HexColor('#424242'),
    'maroon'    : HexColor('#880e4f'),
    'maroon_bg' : HexColor('#fce4ec'),
    'indigo'    : HexColor('#283593'),
    'indigo_bg' : HexColor('#e8eaf6'),
    'brown'     : HexColor('#4e342e'),
    'brown_bg'  : HexColor('#efebe9'),
}

def S():
    """Build all paragraph styles."""
    s = {}
    def ps(name, **kw):
        defaults = dict(fontName='Helvetica', fontSize=10.5,
                        textColor=C['dark_text'], leading=16,
                        spaceAfter=5, alignment=TA_JUSTIFY)
        defaults.update(kw)
        s[name] = ParagraphStyle(name, **defaults)
    # cover
    ps('cov_title', fontName='Helvetica-Bold', fontSize=28, textColor=white,
       alignment=TA_CENTER, leading=36, spaceAfter=8)
    ps('cov_sub', fontName='Helvetica', fontSize=13, textColor=HexColor('#b0bec5'),
       alignment=TA_CENTER, leading=18, spaceAfter=6)
    ps('cov_mod', fontName='Helvetica-Bold', fontSize=20, textColor=white,
       alignment=TA_CENTER, leading=26, spaceAfter=4)
    # banners
    ps('banner', fontName='Helvetica-Bold', fontSize=15, textColor=white,
       alignment=TA_LEFT, leading=20, leftIndent=10)
    ps('section', fontName='Helvetica-Bold', fontSize=12, textColor=C['navy'],
       leading=16, spaceBefore=12, spaceAfter=5)
    ps('subsec', fontName='Helvetica-Bold', fontSize=10.5, textColor=C['med_blue'],
       leading=15, spaceBefore=8, spaceAfter=4)
    # body
    ps('body', fontName='Helvetica', fontSize=10.5, textColor=C['dark_text'],
       leading=16, spaceAfter=6, alignment=TA_JUSTIFY)
    ps('bullet', fontName='Helvetica', fontSize=10.5, textColor=C['dark_text'],
       leading=15, spaceAfter=4, leftIndent=14, bulletIndent=2, alignment=TA_JUSTIFY)
    ps('sub_bullet', fontName='Helvetica', fontSize=10, textColor=C['med_text'],
       leading=14, spaceAfter=3, leftIndent=28, bulletIndent=16)
    ps('note', fontName='Helvetica-Oblique', fontSize=10, textColor=C['purple'],
       leading=14, spaceAfter=5, leftIndent=8)
    ps('formula', fontName='Helvetica-Bold', fontSize=11, textColor=C['purple'],
       alignment=TA_CENTER, leading=18, spaceAfter=5, spaceBefore=4)
    ps('important', fontName='Helvetica-Bold', fontSize=10.5,
       textColor=C['red'], leading=15, spaceAfter=5, leftIndent=6)
    # question styles
    ps('q_mark', fontName='Helvetica-Bold', fontSize=10, textColor=white,
       alignment=TA_LEFT, leading=14, leftIndent=6)
    ps('q_num', fontName='Helvetica-Bold', fontSize=10.5, textColor=C['navy'],
       leading=14, spaceAfter=2)
    ps('q_ans_head', fontName='Helvetica-Bold', fontSize=10, textColor=C['teal'],
       leading=14, spaceAfter=3, leftIndent=4)
    ps('q_ans', fontName='Helvetica', fontSize=10, textColor=C['dark_text'],
       leading=15, spaceAfter=5, leftIndent=8, alignment=TA_JUSTIFY)
    ps('q_ans_bullet', fontName='Helvetica', fontSize=10, textColor=C['dark_text'],
       leading=14, spaceAfter=3, leftIndent=20, bulletIndent=8)
    ps('percent', fontName='Helvetica-Bold', fontSize=30, textColor=white,
       alignment=TA_CENTER, leading=36)
    ps('pct_lbl', fontName='Helvetica', fontSize=8, textColor=HexColor('#b0bec5'),
       alignment=TA_CENTER, leading=11)
    ps('pct_name', fontName='Helvetica-Bold', fontSize=9, textColor=white,
       alignment=TA_CENTER, leading=12)
    ps('toc', fontName='Helvetica', fontSize=11, textColor=C['navy'],
       leading=16, spaceAfter=5, leftIndent=12)
    return s

# ── Widget helpers ────────────────────────────────────────────────────────────
def banner(text, color, s_dict):
    t = Table([[Paragraph(text, s_dict['banner'])]], colWidths=[W-2.8*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),color),
        ('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10),
        ('LEFTPADDING',(0,0),(-1,-1),14),
    ]))
    return t

def sec_box(text, s_dict, bg=C['accent'], border=C['med_blue']):
    t = Table([[Paragraph(f"◆  {text}", s_dict['section'])]], colWidths=[W-2.8*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),bg),
        ('BOX',(0,0),(-1,-1),1.5,border),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),10),
    ]))
    return t

def formula_box(text, s_dict, bg=C['purple_bg'], border=C['purple']):
    t = Table([[Paragraph(text, s_dict['formula'])]], colWidths=[W-2.8*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),bg),
        ('BOX',(0,0),(-1,-1),1.5,border),
        ('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9),
    ]))
    return t

def info_box(text, s_dict, bg=C['orange_bg'], border=C['orange']):
    t = Table([[Paragraph(text, s_dict['body'])]], colWidths=[W-2.8*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),bg),
        ('BOX',(0,0),(-1,-1),1.2,border),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),
    ]))
    return t

def prob_badge(topic, pct, color):
    s_dict = S()
    data = [
        [Paragraph(f"{pct}%", s_dict['percent'])],
        [Paragraph("Exam Probability", s_dict['pct_lbl'])],
        [Paragraph(topic, s_dict['pct_name'])],
    ]
    t = Table(data, colWidths=[5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),color),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ]))
    return t

def badge_row(topic, pct, color, note_text, s_dict):
    data = [[prob_badge(topic, pct, color),
             Paragraph(note_text, s_dict['body'])]]
    t = Table(data, colWidths=[5.5*cm, W-8.3*cm])
    t.setStyle(TableStyle([
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('LEFTPADDING',(1,0),(1,0),14),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ]))
    return t

def two_col_table(data, col1_w=5*cm, header_color=C['navy'], s_dict=None):
    if s_dict is None: s_dict = S()
    th = ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=9.5,
                         textColor=white, alignment=TA_CENTER)
    rows = [[Paragraph(str(r[0]), th if i==0 else s_dict['body']),
             Paragraph(str(r[1]), th if i==0 else s_dict['body'])]
            for i,r in enumerate(data)]
    col2_w = W - 2.8*cm - col1_w
    t = Table(rows, colWidths=[col1_w, col2_w])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),header_color),
        ('FONTNAME',(0,1),(-1,-1),'Helvetica'),
        ('FONTSIZE',(0,0),(-1,-1),9.5),
        ('GRID',(0,0),(-1,-1),0.5,HexColor('#bdbdbd')),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),8),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ]))
    return t

def three_col_table(data, widths, header_color=C['navy']):
    th = ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=9.5,
                         textColor=white, alignment=TA_CENTER)
    sd = S()
    rows = [[Paragraph(str(c), th if i==0 else sd['body']) for c in r]
            for i,r in enumerate(data)]
    t = Table(rows, colWidths=widths)
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),header_color),
        ('FONTNAME',(0,1),(-1,-1),'Helvetica'),
        ('FONTSIZE',(0,0),(-1,-1),9.5),
        ('GRID',(0,0),(-1,-1),0.5,HexColor('#bdbdbd')),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),6),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('BACKGROUND',(0,1),(-1,1),C['accent']),
        ('BACKGROUND',(0,2),(-1,2),C['green_bg']),
        ('BACKGROUND',(0,3),(-1,3),C['orange_bg']),
        ('BACKGROUND',(0,4),(-1,4),C['purple_bg']),
        ('BACKGROUND',(0,5),(-1,5),C['accent']),
        ('BACKGROUND',(0,6),(-1,6),C['green_bg']),
        ('BACKGROUND',(0,7),(-1,7),C['orange_bg']),
        ('BACKGROUND',(0,8),(-1,8),C['purple_bg']),
    ]))
    return t

# ── Q&A block ────────────────────────────────────────────────────────────────
def qa_block(mark_label, color, qas, s_dict):
    """qas = list of (question_text, answer_text)"""
    items = []
    hdr = Table([[Paragraph(f"  ★  {mark_label}", s_dict['q_mark'])]],
                colWidths=[W-2.8*cm])
    hdr.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),color),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',(0,0),(-1,-1),10),
    ]))
    items.append(hdr)
    for i,(q,a) in enumerate(qas,1):
        bg = C['grey_bg'] if i%2==0 else white
        rows = [
            [Paragraph(f"Q{i}.", s_dict['q_num']),
             Paragraph(q, s_dict['q_num'])],
            [Paragraph("Ans:", s_dict['q_ans_head']),
             Paragraph(a, s_dict['q_ans'])],
        ]
        qt = Table(rows, colWidths=[1.1*cm, W-3.9*cm])
        qt.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,-1),bg),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
            ('LEFTPADDING',(0,0),(-1,-1),8),
            ('LINEBELOW',(0,-1),(-1,-1),0.5,HexColor('#e0e0e0')),
        ]))
        items.append(qt)
    return items

# ════════════════════════════════════════════════════════════════════════════
#                         ALL CONTENT
# ════════════════════════════════════════════════════════════════════════════
def build(s):

    story = []

    # ── COVER ────────────────────────────────────────────────────────────────
    cov = Table([
        [Paragraph("INTELLIGENT SYSTEMS", s['cov_title'])],
        [Paragraph("PCC-CS-601  |  B.Tech 6th Semester  |  YMCA University", s['cov_sub'])],
        [Spacer(1,0.3*cm)],
        [Paragraph("MODULE  2", s['cov_mod'])],
        [Paragraph("Biological Foundations to Intelligent Systems — II", s['cov_sub'])],
        [Spacer(1,0.4*cm)],
        [Paragraph("Fuzzy Logic  •  Knowledge Representation & Inference", s['cov_sub'])],
        [Paragraph("Genetic Algorithm  •  Fuzzy Neural Networks", s['cov_sub'])],
        [Spacer(1,0.8*cm)],
        [Paragraph("Complete Notes  |  All Questions  |  Full Model Answers", ParagraphStyle(
            'ci', fontName='Helvetica-Oblique', fontSize=11,
            textColor=HexColor('#78909c'), alignment=TA_CENTER, leading=16))],
    ], colWidths=[W-2*cm])
    cov.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),C['dark_navy']),
        ('TOPPADDING',(0,0),(-1,-1),18),('BOTTOMPADDING',(0,0),(-1,-1),18),
        ('BOX',(0,0),(-1,-1),3,HexColor('#546e7a')),
    ]))
    story += [Spacer(1,1.2*cm), cov, Spacer(1,0.8*cm)]

    # probability summary
    story.append(Paragraph("📊  TOPIC-WISE EXAM PROBABILITY", s['section']))
    prob_data = [
        ["TOPIC","PROBABILITY","MARKS EXPECTED","APPEARED IN"],
        ["Fuzzy Logic","90% ★★★","5–10 marks","2018, 2024, 2025"],
        ["Knowledge Representation & Inference","80% ★★★","5–15 marks","2018, 2024, 2025"],
        ["Genetic Algorithm","85% ★★★","5–10 marks","2018, 2024, 2025"],
        ["Fuzzy Neural Networks","45% ★","5 marks","Syllabus topic"],
    ]
    th_style = ParagraphStyle('th_s', fontName='Helvetica-Bold', fontSize=9.5,
                               textColor=white, alignment=TA_CENTER)
    td_style = ParagraphStyle('td_s', fontName='Helvetica', fontSize=9.5,
                               textColor=C['dark_text'], alignment=TA_CENTER)
    prob_rows = [[Paragraph(c, th_style) for c in prob_data[0]]]
    bgs = [C['accent'], C['green_bg'], C['orange_bg'], C['purple_bg']]
    for i, row in enumerate(prob_data[1:]):
        prob_rows.append([Paragraph(c, td_style) for c in row])
    pt = Table(prob_rows, colWidths=[6.5*cm,3*cm,3.5*cm,4.5*cm])
    pt.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),C['dark_navy']),
        ('BACKGROUND',(0,1),(-1,1),C['accent']),
        ('BACKGROUND',(0,2),(-1,2),C['green_bg']),
        ('BACKGROUND',(0,3),(-1,3),C['orange_bg']),
        ('BACKGROUND',(0,4),(-1,4),C['purple_bg']),
        ('GRID',(0,0),(-1,-1),0.5,HexColor('#bdbdbd')),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',(0,0),(-1,-1),8),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ]))
    story += [pt, PageBreak()]

    # ════════════════════════════════════════════════════════════════════════
    # TOPIC 1 ── FUZZY LOGIC
    # ════════════════════════════════════════════════════════════════════════
    story.append(banner("TOPIC 1 — FUZZY LOGIC", C['teal'], s))
    story.append(Spacer(1,0.3*cm))
    story.append(badge_row("Fuzzy Logic","90%",C['teal'],
        "<b>VERY HIGH probability!</b> Every year has at least one fuzzy question. "
        "2025 paper: fuzzy set core/height (1.5M), why fuzzy introduced + design for human age (5M). "
        "2024: crisp vs fuzzy (1.5M), probability vs fuzzy (5M). "
        "2018: fuzzy arithmetic operations (5M). Know crisp vs fuzzy, membership functions, "
        "operations, and how to design a fuzzy set.", s))
    story.append(Spacer(1,0.4*cm))

    # 1.1
    story.append(sec_box("1.1  Why Was Fuzzy Logic Introduced?", s, C['teal_bg'], C['teal']))
    story.append(Spacer(1,0.15*cm))
    story.append(Paragraph(
        "Classical (Crisp) logic deals only with <b>exact, binary values</b> — something is either TRUE (1) "
        "or FALSE (0). But the real world is full of vagueness and partial truths. "
        "Consider: 'Is this person tall?' A person of 5'9\" is somewhat tall — not perfectly tall, "
        "not perfectly short. Classical logic cannot model this in-between state.",s['body']))
    story.append(Paragraph(
        "<b>Fuzzy Logic</b> was introduced by <b>Lotfi A. Zadeh in 1965</b> to handle such vagueness and "
        "uncertainty. It allows truth values to be ANY number between 0 and 1, not just 0 or 1. "
        "This matches how humans think and communicate — we use words like 'somewhat', 'very', "
        "'mostly', 'a little' — all of which fuzzy logic can represent.",s['body']))
    reasons = [
        "Real-world problems are inherently vague and imprecise.",
        "Human language and reasoning is approximate, not exact.",
        "Classical Boolean logic fails for partial membership (e.g., 'lukewarm water').",
        "Fuzzy logic enables machines to reason like humans.",
        "Better control systems — smoother, more natural response.",
    ]
    for r in reasons:
        story.append(Paragraph(f"✓  {r}", s['bullet']))

    # 1.2
    story.append(sec_box("1.2  Crisp Set vs Fuzzy Set", s, C['teal_bg'], C['teal']))
    story.append(Spacer(1,0.15*cm))
    story.append(Paragraph(
        "A <b>Crisp Set</b> uses classical set theory — an element either belongs to a set (membership=1) "
        "or does not (membership=0). A <b>Fuzzy Set</b> allows <b>partial membership</b> — any value "
        "between 0 and 1.",s['body']))
    crisp_fuzzy = [
        ["Feature","Crisp (Classical) Logic","Fuzzy Logic"],
        ["Membership","Either 0 or 1 only","Any value between 0 and 1"],
        ["Truth values","Exactly TRUE or FALSE","Degree of truth (0.0 to 1.0)"],
        ["Boundary","Sharp, well-defined","Gradual, overlapping"],
        ["Example","Age > 18 is Adult (yes/no)","Age 17 is 0.8 adult, age 15 is 0.4 adult"],
        ["Handles vagueness","NO","YES"],
        ["Human reasoning match","Poor","Excellent"],
        ["Applications","Digital circuits, databases","Control systems, AI, NLP"],
    ]
    story.append(three_col_table(crisp_fuzzy,
        [4*cm,(W-2.8*cm-4*cm)/2,(W-2.8*cm-4*cm)/2], C['teal']))

    # 1.3
    story.append(sec_box("1.3  Fuzzy Set — Definition and Notation", s, C['teal_bg'], C['teal']))
    story.append(Spacer(1,0.15*cm))
    story.append(Paragraph(
        "A <b>Fuzzy Set A</b> defined on a universe of discourse X is characterized by a "
        "<b>Membership Function μ_A(x)</b> that assigns to each element x in X a degree of membership "
        "in A. This degree lies between 0 and 1.",s['body']))
    story.append(formula_box("A = { (x, μ_A(x)) | x ∈ X }     where  0 ≤ μ_A(x) ≤ 1", s))
    story.append(Paragraph(
        "<b>Example — Fuzzy set of 'TALL people':</b> Universe X = {heights from 4ft to 7ft}<br/>"
        "μ_TALL(5'0\") = 0.1  |  μ_TALL(5'6\") = 0.5  |  μ_TALL(6'0\") = 0.9  |  μ_TALL(7'0\") = 1.0",
        s['note']))

    # 1.4 — Key Terminology
    story.append(sec_box("1.4  Key Fuzzy Set Terminology (Very Important!)", s, C['teal_bg'], C['teal']))
    story.append(Spacer(1,0.15*cm))
    terms = [
        ("Support","The set of all elements x where membership μ_A(x) > 0 (strictly greater than zero).",
         "Support(A) = { x ∈ X | μ_A(x) > 0 }"),
        ("Core","The set of all elements x where membership μ_A(x) = 1 (full membership).",
         "Core(A) = { x ∈ X | μ_A(x) = 1 }"),
        ("Height","The maximum membership value of any element in the fuzzy set.",
         "Height(A) = max{ μ_A(x) | x ∈ X }"),
        ("Normal Fuzzy Set","A fuzzy set whose height = 1 (at least one element has full membership).",
         "Height(A) = 1  ⟹  Normal Fuzzy Set"),
        ("Subnormal Fuzzy Set","A fuzzy set whose height < 1 (no element has full membership).",
         "Height(A) < 1  ⟹  Subnormal"),
        ("α-cut (Alpha Cut)","The crisp set of all elements with membership ≥ α.",
         "A_α = { x ∈ X | μ_A(x) ≥ α }"),
        ("Crossover Point","The element x where μ_A(x) = 0.5 exactly.",
         "Crossover: μ_A(x) = 0.5"),
    ]
    for tname, tdesc, tformula in terms:
        story.append(Paragraph(f"<b>► {tname}:</b> {tdesc}", s['subsec']))
        story.append(formula_box(tformula, s))

    # 1.5 — Membership Functions
    story.append(sec_box("1.5  Types of Membership Functions", s, C['teal_bg'], C['teal']))
    story.append(Spacer(1,0.15*cm))
    story.append(Paragraph(
        "The membership function defines the shape of the fuzzy set. Common types:",s['body']))
    mf_types = [
        ("Triangular MF","Shape: /\\  (triangle). Defined by three points: a (start), b (peak=1), c (end).",
         "μ(x) = 0 if x≤a or x≥c  |  (x−a)/(b−a) if a≤x≤b  |  (c−x)/(c−b) if b≤x≤c"),
        ("Trapezoidal MF","Shape: /‾\\  (trapezoid). Flat top between b and c. Defined by four points a,b,c,d.",
         "μ(x) = 0 if x≤a or x≥d  |  (x−a)/(b−a) if a<x<b  |  1 if b≤x≤c  |  (d−x)/(d−c) if c<x<d"),
        ("Gaussian MF","Bell-shaped curve. Smooth and continuous. Defined by mean c and width σ.",
         "μ(x) = exp( −(x−c)² / (2σ²) )"),
        ("Sigmoid MF","S-shaped curve. Good for 'large' or 'small' type sets.",
         "μ(x) = 1 / (1 + exp(−a(x−c)))"),
    ]
    for mname, mdesc, mformula in mf_types:
        story.append(Paragraph(f"<b>{mname}:</b> {mdesc}", s['bullet']))
        story.append(formula_box(mformula, s))

    # 1.6 — Operations
    story.append(sec_box("1.6  Fuzzy Set Operations", s, C['teal_bg'], C['teal']))
    story.append(Spacer(1,0.15*cm))
    story.append(Paragraph("Three fundamental operations on fuzzy sets A and B:", s['body']))
    ops = [
        ("Union (OR)","The maximum of the two membership values. Like OR in crisp logic.",
         "μ_(A∪B)(x) = max( μ_A(x),  μ_B(x) )",
         "Example: μ_A(x)=0.6, μ_B(x)=0.8  →  μ_(A∪B)(x) = 0.8"),
        ("Intersection (AND)","The minimum of the two membership values. Like AND in crisp logic.",
         "μ_(A∩B)(x) = min( μ_A(x),  μ_B(x) )",
         "Example: μ_A(x)=0.6, μ_B(x)=0.8  →  μ_(A∩B)(x) = 0.6"),
        ("Complement (NOT)","One minus the membership value. Like NOT in crisp logic.",
         "μ_Ā(x) = 1 − μ_A(x)",
         "Example: μ_A(x)=0.6  →  μ_Ā(x) = 1 − 0.6 = 0.4"),
    ]
    for oname, odesc, oformula, oex in ops:
        story.append(Paragraph(f"<b>► {oname}:</b> {odesc}", s['subsec']))
        story.append(formula_box(oformula, s))
        story.append(Paragraph(oex, s['note']))

    # 1.7 — Fuzzy Arithmetic
    story.append(sec_box("1.7  Fuzzy Arithmetic Operations", s, C['teal_bg'], C['teal']))
    story.append(Spacer(1,0.15*cm))
    story.append(Paragraph(
        "Fuzzy arithmetic extends basic math operations to fuzzy numbers using the "
        "<b>Extension Principle</b>. For two fuzzy numbers A and B:",s['body']))
    arith = [
        ("Addition","μ_(A+B)(z) = max{ min(μ_A(x), μ_B(y)) | x + y = z }"),
        ("Subtraction","μ_(A−B)(z) = max{ min(μ_A(x), μ_B(y)) | x − y = z }"),
        ("Multiplication","μ_(A×B)(z) = max{ min(μ_A(x), μ_B(y)) | x × y = z }"),
        ("Division","μ_(A÷B)(z) = max{ min(μ_A(x), μ_B(y)) | x ÷ y = z,  y ≠ 0 }"),
    ]
    for aname, aformula in arith:
        story.append(Paragraph(f"<b>{aname}:</b>", s['bullet']))
        story.append(formula_box(aformula, s))
    story.append(info_box(
        "📌  EXAM TIP: For fuzzy arithmetic using interval arithmetic on α-cuts — "
        "find the α-cut of A and B, perform the operation on the intervals, then reconstruct the fuzzy result. "
        "Example: If A=[2,4] and B=[1,3] at α=1, then A+B=[3,7] at α=1.", s))

    # 1.8 — Fuzzy Inference System
    story.append(sec_box("1.8  Fuzzy Inference System (FIS) — How Fuzzy Logic Works", s, C['teal_bg'], C['teal']))
    story.append(Spacer(1,0.15*cm))
    story.append(Paragraph(
        "A Fuzzy Inference System converts crisp inputs into fuzzy outputs through a sequence of steps:",s['body']))
    fis_steps = [
        ("Step 1: Fuzzification","Convert crisp (exact) input values into fuzzy membership values using membership functions. "
         "Example: Input temperature = 45°C → μ_HOT(45)=0.7, μ_WARM(45)=0.3"),
        ("Step 2: Rule Evaluation","Apply fuzzy IF-THEN rules. "
         "Example: IF temperature is HOT AND humidity is HIGH THEN fan-speed is FAST. "
         "Use min(μ_HOT, μ_HIGH) to get the rule's firing strength."),
        ("Step 3: Aggregation","Combine the outputs of all rules into one fuzzy set "
         "using union (max) operation."),
        ("Step 4: Defuzzification","Convert the combined fuzzy output back to a crisp (single) value. "
         "Most common method: Centroid (Centre of Gravity) — "
         "x* = Σ(x · μ(x)) / Σ(μ(x))"),
    ]
    for sname, sdesc in fis_steps:
        story.append(Paragraph(f"<b>► {sname}:</b>", s['subsec']))
        story.append(Paragraph(sdesc, s['body']))

    # 1.9 — Designing fuzzy set for human age
    story.append(sec_box("1.9  Designing a Fuzzy Set for Human Age (Exam Example!)", s, C['teal_bg'], C['teal']))
    story.append(Spacer(1,0.15*cm))
    story.append(Paragraph(
        "This was directly asked in 2025 exam (5 marks). Universe of discourse X = [0, 100] years.",s['body']))
    age_sets = [
        ("YOUNG","μ=1 for age 0–20, gradually decreasing to 0 at age 40.",
         "Triangular: μ_YOUNG(x) = 1 if x≤20  |  (40−x)/20 if 20<x<40  |  0 if x≥40"),
        ("MIDDLE-AGED","μ rises from 0 at age 30 to 1 at age 45, stays at 1 till 55, drops to 0 at age 70.",
         "Trapezoidal: μ_MID(x) = 0 if x≤30 or x≥70  |  (x−30)/15 if 30<x<45  |  1 if 45≤x≤55  |  (70−x)/15 if 55<x<70"),
        ("OLD","μ starts rising from 0 at age 60, reaches 1 at age 80 and beyond.",
         "Triangular/sigmoid: μ_OLD(x) = 0 if x≤60  |  (x−60)/20 if 60<x<80  |  1 if x≥80"),
    ]
    for aname, adesc, aformula in age_sets:
        story.append(Paragraph(f"<b>Fuzzy set '{aname}':</b> {adesc}", s['bullet']))
        story.append(formula_box(aformula, s))
    story.append(Paragraph(
        "At age = 35:  μ_YOUNG(35) = 0.25,  μ_MIDDLE(35) = 0.33,  μ_OLD(35) = 0.0 — "
        "person is mostly young with some middle-aged characteristics.", s['note']))

    # 1.10 — Applications
    story.append(sec_box("1.10  Applications of Fuzzy Logic", s, C['teal_bg'], C['teal']))
    apps_fl = [
        "Washing machines — auto-adjusting wash cycle based on dirt level and load",
        "Air conditioners — smooth temperature control",
        "Camera auto-focus and image stabilization",
        "Medical diagnosis systems — handling imprecise symptoms",
        "Stock market prediction and financial forecasting",
        "Traffic control systems",
        "Robotics — smooth motion planning",
        "Natural Language Processing — handling vague words",
    ]
    for a in apps_fl:
        story.append(Paragraph(f"✓  {a}", s['bullet']))

    # ── FUZZY LOGIC QUESTIONS ─────────────────────────────────────────────
    story.append(Spacer(1,0.3*cm))
    story.append(banner("PRACTICE QUESTIONS & ANSWERS — TOPIC 1: FUZZY LOGIC", C['teal'], s))
    story.append(Spacer(1,0.2*cm))

    q15_fl = [
        (
            "What is fuzzy logic? How is it different from crisp logic?",
            "Fuzzy logic, introduced by Lotfi Zadeh in 1965, allows truth values between 0 and 1, not just 0 or 1. "
            "Crisp logic is binary — an element either belongs to a set (1) or doesn't (0). "
            "Fuzzy logic handles vagueness and partial truth, like 'somewhat hot' or 'fairly tall', making it suitable for real-world imprecision."
        ),
        (
            "Define: Core and Height of a fuzzy set. (Asked in 2025 paper)",
            "Core of a fuzzy set A is the set of all elements with membership value = 1: Core(A) = {x | μ_A(x) = 1}. "
            "Height of a fuzzy set is the maximum membership value: Height(A) = max{μ_A(x)}. "
            "A normal fuzzy set has height = 1. A subnormal fuzzy set has height < 1."
        ),
        (
            "Differentiate between crisp logic and fuzzy logic. (Asked in 2024 paper)",
            "Crisp logic: membership is strictly 0 or 1, boundaries are sharp, handles only exact true/false. "
            "Fuzzy logic: membership ranges from 0 to 1, boundaries are gradual/overlapping, handles vagueness and partial truth. "
            "Example: Crisp — 'temperature > 30°C is HOT' (binary). Fuzzy — '28°C is 0.7 HOT' (partial)."
        ),
        (
            "What is a membership function? Name its types.",
            "A membership function μ_A(x) defines the degree to which element x belongs to fuzzy set A, ranging from 0 to 1. "
            "Types: Triangular (three points, /\\ shape), Trapezoidal (flat top, /‾\\ shape), Gaussian (smooth bell curve), "
            "Sigmoid (S-shaped curve). Each type suits different kinds of vague concepts."
        ),
        (
            "What is defuzzification? Name one method.",
            "Defuzzification converts the fuzzy output of a fuzzy inference system back into a single crisp numerical value. "
            "It is the final step of fuzzy reasoning. Most common method: Centroid (Centre of Gravity) — "
            "x* = Σ(x · μ(x)) / Σ(μ(x)). Other methods: Mean of Maximum, Bisector method."
        ),
        (
            "State the fuzzy union, intersection, and complement operations.",
            "Union (OR): μ_(A∪B)(x) = max(μ_A(x), μ_B(x)). "
            "Intersection (AND): μ_(A∩B)(x) = min(μ_A(x), μ_B(x)). "
            "Complement (NOT): μ_Ā(x) = 1 − μ_A(x). "
            "Example: If μ_A=0.6 and μ_B=0.8: Union=0.8, Intersection=0.6, Complement of A=0.4."
        ),
    ]
    for item in qa_block("1.5 Marks Questions with Answers (~50 words each)",
                          HexColor('#00695c'), q15_fl, s):
        story.append(item)

    story.append(Spacer(1,0.25*cm))

    q5_fl = [
        (
            "What is fuzzy logic? Why was it introduced? Design a fuzzy set for human age. (Asked in 2025 — 5 marks)",
            "FUZZY LOGIC — INTRODUCTION AND DESIGN\n\n"
            "Fuzzy Logic is a mathematical framework introduced by Lotfi A. Zadeh in 1965 to handle "
            "vagueness and imprecision in real-world problems. Classical Boolean logic is binary — "
            "something is either TRUE (1) or FALSE (0). But natural language and human reasoning are "
            "rarely this absolute. Words like 'tall', 'hot', 'old', 'fast' do not have sharp boundaries. "
            "A person of 5'9\" is neither definitively 'tall' nor 'not tall' — they are SOMEWHAT tall. "
            "Crisp logic cannot represent this partial truth.\n\n"
            "WHY FUZZY LOGIC WAS INTRODUCED:\n"
            "1. Real-world problems involve vagueness and uncertainty that crisp logic cannot handle.\n"
            "2. Human language uses approximate terms — fuzzy logic formalizes this.\n"
            "3. Better control systems — gradual transitions instead of abrupt on/off switches.\n"
            "4. Models human reasoning more accurately.\n"
            "5. Bridges the gap between human thought and machine computation.\n\n"
            "DESIGNING A FUZZY SET FOR HUMAN AGE (Universe X = 0 to 100 years):\n\n"
            "We define three fuzzy sets: YOUNG, MIDDLE-AGED, and OLD.\n\n"
            "Fuzzy Set YOUNG (Triangular):\n"
            "μ_YOUNG(x) = 1 for x ≤ 20\n"
            "μ_YOUNG(x) = (40 − x)/20 for 20 < x < 40\n"
            "μ_YOUNG(x) = 0 for x ≥ 40\n"
            "→ A 25-year-old has μ_YOUNG = 0.75 (mostly young)\n\n"
            "Fuzzy Set MIDDLE-AGED (Trapezoidal):\n"
            "μ_MID(x) = 0 for x ≤ 30\n"
            "μ_MID(x) = (x−30)/15 for 30 < x < 45\n"
            "μ_MID(x) = 1 for 45 ≤ x ≤ 55\n"
            "μ_MID(x) = (70−x)/15 for 55 < x < 70\n"
            "μ_MID(x) = 0 for x ≥ 70\n\n"
            "Fuzzy Set OLD (Triangular/Ramp):\n"
            "μ_OLD(x) = 0 for x ≤ 60\n"
            "μ_OLD(x) = (x−60)/20 for 60 < x < 80\n"
            "μ_OLD(x) = 1 for x ≥ 80\n\n"
            "At age 35: μ_YOUNG=0.25, μ_MID=0.33, μ_OLD=0.0 — person is somewhat young and slightly middle-aged.\n"
            "This overlapping design reflects how people naturally transition between age categories."
        ),
        (
            "What is the main difference between probability and fuzzy logic? (Asked in 2024 — 5 marks)",
            "PROBABILITY VS FUZZY LOGIC — KEY DIFFERENCES\n\n"
            "Both probability and fuzzy logic deal with uncertainty, but they address DIFFERENT KINDS of uncertainty.\n\n"
            "PROBABILITY:\n"
            "• Deals with STATISTICAL uncertainty — events that may or may not occur.\n"
            "• P(A) = 0.7 means there is a 70% CHANCE that event A will occur.\n"
            "• Based on random experiments and frequency of occurrence.\n"
            "• P(A) + P(not A) = 1 always — mutually exclusive.\n"
            "• Example: 'There is a 70% probability it will rain tomorrow.' "
            "It either rains (1) or doesn't (0) — we are just uncertain which.\n"
            "• Based on classical set theory.\n\n"
            "FUZZY LOGIC:\n"
            "• Deals with LINGUISTIC uncertainty — vagueness in meaning of words.\n"
            "• μ_A(x) = 0.7 means element x BELONGS to set A with degree 0.7.\n"
            "• Based on partial membership — no statistical experiment needed.\n"
            "• μ_A(x) + μ_Ā(x) = 1, but both can be non-zero simultaneously.\n"
            "• Example: 'Temperature 35°C belongs to HOT with degree 0.7.' "
            "The temperature IS 35°C — we are not uncertain about its value, "
            "just about how 'hot' it is.\n"
            "• Based on fuzzy set theory.\n\n"
            "KEY DISTINCTION: Probability answers 'How likely is it to happen?' "
            "Fuzzy logic answers 'To what degree does it belong?' "
            "A glass of warm water is NOT probably hot — it is PARTIALLY hot (fuzzy). "
            "Probability is about random events; fuzzy logic is about imprecise concepts.\n\n"
            "COMPARISON TABLE:\n"
            "Probability: 0.7 = 70% chance of occurrence.\n"
            "Fuzzy: 0.7 = 70% degree of membership.\n"
            "Probability: Sum of complementary probabilities = 1.\n"
            "Fuzzy: Sum of complementary memberships = 1.\n"
            "Probability: Binary outcome (occurs or not).\n"
            "Fuzzy: Graded truth (partial belonging)."
        ),
        (
            "Explain fuzzy arithmetic operations with examples. (Asked in 2018 — 5 marks)",
            "FUZZY ARITHMETIC OPERATIONS\n\n"
            "Fuzzy arithmetic extends regular arithmetic to fuzzy numbers using the Extension Principle. "
            "A fuzzy number is a fuzzy set on the real number line with a unimodal, normal membership function.\n\n"
            "The most practical approach uses ALPHA-CUT ARITHMETIC:\n"
            "For α-cut level, get interval [a_L, a_R] for A and [b_L, b_R] for B, then operate on intervals.\n\n"
            "Let A = 'approximately 3' and B = 'approximately 5' be triangular fuzzy numbers:\n"
            "A = (2, 3, 4)  meaning: peak at 3, starts at 2, ends at 4\n"
            "B = (4, 5, 6)  meaning: peak at 5, starts at 4, ends at 6\n\n"
            "1. FUZZY ADDITION:\n"
            "A + B = (2+4, 3+5, 4+6) = (6, 8, 10)\n"
            "The result is a triangular fuzzy number peaking at 8, ranging from 6 to 10.\n"
            "Formula: μ_(A+B)(z) = max{min(μ_A(x), μ_B(y)) | x + y = z}\n\n"
            "2. FUZZY SUBTRACTION:\n"
            "A − B = (2−6, 3−5, 4−4) = (−4, −2, 0)\n"
            "Formula: μ_(A−B)(z) = max{min(μ_A(x), μ_B(y)) | x − y = z}\n\n"
            "3. FUZZY MULTIPLICATION:\n"
            "A × B ≈ (2×4, 3×5, 4×6) = (8, 15, 24)\n"
            "Formula: μ_(A×B)(z) = max{min(μ_A(x), μ_B(y)) | x × y = z}\n\n"
            "4. FUZZY DIVISION:\n"
            "A ÷ B ≈ (2/6, 3/5, 4/4) = (0.33, 0.6, 1.0)\n"
            "Formula: μ_(A÷B)(z) = max{min(μ_A(x), μ_B(y)) | x ÷ y = z, y ≠ 0}\n\n"
            "These operations are essential in fuzzy control systems where inputs are fuzzy "
            "and computations must preserve the fuzzy nature of the result."
        ),
    ]
    for item in qa_block("5 Marks Questions with Answers (300–500 words each)",
                          HexColor('#00897b'), q5_fl, s):
        story.append(item)

    story.append(Spacer(1,0.25*cm))

    q10_fl = [
        (
            "What is fuzzy logic? Why is it important? Explain fuzzy arithmetic operations in detail. "
            "(Asked in 2018 — 5+5 = 10 marks combined topic)",
            "FUZZY LOGIC — COMPLETE EXPLANATION\n\n"
            "INTRODUCTION:\n"
            "Fuzzy Logic is a form of multi-valued logic introduced by Lotfi A. Zadeh at UC Berkeley in 1965. "
            "Unlike classical binary logic where truth values are only 0 (False) or 1 (True), fuzzy logic allows "
            "DEGREES OF TRUTH — any value between 0 and 1. This makes it capable of representing the natural "
            "vagueness and imprecision found in human language and real-world situations.\n\n"
            "WHY FUZZY LOGIC IS IMPORTANT:\n"
            "1. Models Human Reasoning: Humans naturally think in approximate terms — 'somewhat fast', 'very cold', "
            "'nearly done'. Fuzzy logic mathematically formalizes these approximate concepts.\n"
            "2. Handles Uncertainty: Real-world systems involve noise, vagueness, and incomplete information. "
            "Fuzzy logic provides tools to reason under such conditions.\n"
            "3. Better Control Systems: Fuzzy controllers give smooth, gradual responses instead of abrupt on/off "
            "switching. Example: A fuzzy air conditioner gradually adjusts cooling, not just ON/OFF.\n"
            "4. Simple Rules, Complex Behavior: Complex systems can be described using simple IF-THEN fuzzy rules "
            "that non-experts can write.\n"
            "5. Works Without Mathematical Model: Unlike classical control theory, fuzzy systems don't need a "
            "precise mathematical model of the system.\n\n"
            "FUZZY SET DEFINITION:\n"
            "A fuzzy set A on universe X: A = {(x, μ_A(x)) | x ∈ X}, where 0 ≤ μ_A(x) ≤ 1.\n\n"
            "KEY TERMS:\n"
            "• Support: {x | μ_A(x) > 0}  |  Core: {x | μ_A(x) = 1}  |  Height: max{μ_A(x)}\n"
            "• α-cut: {x | μ_A(x) ≥ α}  |  Crossover Point: μ_A(x) = 0.5\n\n"
            "FUZZY OPERATIONS:\n"
            "Union: μ_(A∪B)(x) = max(μ_A(x), μ_B(x))\n"
            "Intersection: μ_(A∩B)(x) = min(μ_A(x), μ_B(x))\n"
            "Complement: μ_Ā(x) = 1 − μ_A(x)\n\n"
            "FUZZY ARITHMETIC (using Extension Principle):\n"
            "Given triangular fuzzy numbers A=(a1,a2,a3) and B=(b1,b2,b3):\n"
            "Addition: A+B = (a1+b1, a2+b2, a3+b3)\n"
            "Subtraction: A−B = (a1−b3, a2−b2, a3−b1)\n"
            "Multiplication: A×B ≈ (a1×b1, a2×b2, a3×b3) [for positive numbers]\n"
            "Division: A÷B ≈ (a1/b3, a2/b2, a3/b1) [for positive numbers]\n\n"
            "Example: A=(2,3,4), B=(1,2,3):\n"
            "A+B = (3,5,7); A−B = (−1,1,3); A×B = (2,6,12); A÷B = (0.67,1.5,4)\n\n"
            "FUZZY INFERENCE SYSTEM (FIS):\n"
            "Step 1: Fuzzification — crisp input → membership values\n"
            "Step 2: Rule evaluation — IF-THEN fuzzy rules\n"
            "Step 3: Aggregation — combine rule outputs\n"
            "Step 4: Defuzzification — fuzzy output → crisp value (Centroid: x* = Σ(x·μ(x))/Σ(μ(x)))\n\n"
            "APPLICATIONS: Washing machines, air conditioners, cameras, medical diagnosis, robotics, traffic control.\n\n"
            "CONCLUSION: Fuzzy logic bridges the gap between binary machine thinking and approximate human reasoning, "
            "making AI systems more natural, robust, and interpretable."
        ),
    ]
    for item in qa_block("10 Marks Questions with Answers (500–700 words each)",
                          HexColor('#00838f'), q10_fl, s):
        story.append(item)

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # TOPIC 2 ── KNOWLEDGE REPRESENTATION & INFERENCE
    # ════════════════════════════════════════════════════════════════════════
    story.append(banner("TOPIC 2 — KNOWLEDGE REPRESENTATION & INFERENCE MECHANISM", C['indigo'], s))
    story.append(Spacer(1,0.3*cm))
    story.append(badge_row("KR & Inference","80%",C['indigo'],
        "<b>HIGH probability!</b> 2024: KR techniques (10M), blackboard system (5M). "
        "2025: Knowledge representation ways (1.5M), blackboard architecture (5M short note), "
        "semantic nets and frames (5M short note). 2018: Semantic net, partitioned net (5+5M). "
        "Know ALL representation methods with examples.", s))
    story.append(Spacer(1,0.4*cm))

    # 2.1
    story.append(sec_box("2.1  What is Knowledge Representation?", s, C['indigo_bg'], C['indigo']))
    story.append(Spacer(1,0.15*cm))
    story.append(Paragraph(
        "<b>Knowledge Representation (KR)</b> is the process of storing knowledge about the world "
        "in a form that a computer system can use to solve complex problems. "
        "For an AI system to be intelligent, it must KNOW things — facts, rules, relationships, "
        "procedures. KR provides the structures and languages to capture this knowledge.",s['body']))
    story.append(Paragraph(
        "A good KR scheme must be: Representationally adequate (can represent all needed knowledge), "
        "Inferentially adequate (allows new knowledge to be derived), Inferentially efficient "
        "(derivation is fast), and Acquisitional adequate (easy to add new knowledge).",s['body']))

    # 2.2 — Types
    story.append(sec_box("2.2  Types / Techniques of Knowledge Representation", s, C['indigo_bg'], C['indigo']))
    story.append(Spacer(1,0.15*cm))

    # Logical Representation
    story.append(Paragraph("► 1. Logical Representation (Propositional & First-Order Predicate Logic)", s['subsec']))
    story.append(Paragraph(
        "Uses formal logic to represent facts and rules. Two types:",s['body']))
    story.append(Paragraph(
        "<b>Propositional Logic:</b> Deals with simple statements (propositions) that are TRUE or FALSE. "
        "Connectives: AND (∧), OR (∨), NOT (¬), IMPLIES (→), BICONDITIONAL (↔). "
        "Example: P='It is raining', Q='Roads are wet'. Rule: P → Q (If raining then roads wet). "
        "<b>Limitation:</b> Cannot handle objects, relationships, or quantifiers.",s['bullet']))
    story.append(Paragraph(
        "<b>First-Order Predicate Logic (FOPL):</b> More expressive. Uses predicates, variables, "
        "quantifiers (∀ = for all, ∃ = there exists), and functions. "
        "Example: 'Every human is mortal' → ∀x [Human(x) → Mortal(x)]. "
        "'Socrates is human' → Human(Socrates). Therefore: Mortal(Socrates). "
        "<b>Advantages:</b> Very expressive, formal proofs possible. "
        "<b>Disadvantages:</b> Computationally expensive, hard to handle uncertainty.",s['bullet']))

    # Semantic Networks
    story.append(Paragraph("► 2. Semantic Networks", s['subsec']))
    story.append(Paragraph(
        "A <b>Semantic Network</b> is a graphical representation of knowledge in the form of a "
        "<b>directed labeled graph</b>. Nodes represent objects/concepts, and edges/arcs represent "
        "relationships between them.",s['body']))
    sem_features = [
        "Nodes = Objects, concepts, events (e.g., 'Dog', 'Animal', 'Fido')",
        "Arcs = Relationships labeled with relation name (IS-A, HAS-A, HAS-PART, etc.)",
        "IS-A arc: Indicates class membership or inheritance (Dog IS-A Animal)",
        "HAS-A arc: Indicates property possession (Dog HAS-A Tail)",
        "Inheritance: Properties of parent node flow down to child via IS-A links",
    ]
    for f in sem_features:
        story.append(Paragraph(f"  • {f}", s['bullet']))
    story.append(Paragraph(
        "Example: Represent 'Fido is a dog that has a tail and can bark':\n"
        "Fido --IS-A--> Dog --IS-A--> Animal\n"
        "Dog --HAS-A--> Tail\n"
        "Dog --CAN--> Bark",s['note']))
    story.append(Paragraph(
        "<b>Advantage:</b> Visually intuitive, supports inheritance. "
        "<b>Disadvantage:</b> Cannot represent quantifiers (all, some), negative facts, or rules well.",s['body']))

    # Partitioned Networks
    story.append(Paragraph("► 3. Partitioned Networks (Extension of Semantic Networks)", s['subsec']))
    story.append(Paragraph(
        "A limitation of basic semantic networks is they cannot easily represent sentences like "
        "'Every lunatic hit a doctor' vs 'A lunatic hit every doctor' — the scope of quantifiers matters. "
        "<b>Partitioned Networks</b> solve this by dividing the network into <b>partitions (spaces)</b>. "
        "Each partition represents one context or scope. "
        "Universal quantifiers create 'generic' spaces; existential quantifiers create 'individual' spaces.",s['body']))
    pn_examples = [
        ("Every lunatic hit a doctor","Universal quantifier 'every' for lunatic, existential 'a' for doctor. Generic space for lunatic, individual space for doctor inside."),
        ("The lunatic hit the door","Both specific — individual spaces for both lunatic and door."),
        ("Every lunatic has hit every doctor","Both quantifiers universal — nested generic spaces."),
    ]
    pn_data = [["Sentence","Partitioned Network Interpretation"]] + [[a,b] for a,b in pn_examples]
    story.append(two_col_table(pn_data, 5.5*cm, C['indigo'], s))

    # Frames
    story.append(Paragraph("► 4. Frames", s['subsec']))
    story.append(Paragraph(
        "A <b>Frame</b> is a data structure for representing stereotyped situations or objects. "
        "Proposed by Marvin Minsky in 1975. A frame has <b>slots</b> (attributes) and each slot "
        "has a <b>value</b>. Frames are like templates that can be instantiated.",s['body']))
    story.append(Paragraph(
        "Frame structure:\n"
        "FRAME: Car\n"
        "  SLOT: Colour         VALUE: (Red, Blue, White)\n"
        "  SLOT: Number-of-wheels  VALUE: 4  DEFAULT: 4\n"
        "  SLOT: Engine-size    VALUE: (1.0L, 1.5L, 2.0L)\n"
        "  SLOT: Manufacturer   VALUE: (Toyota, Ford, Honda)\n"
        "  SLOT: Can-do         VALUE: Drive, Transport-people",s['note']))
    frame_features = [
        "Default values: Slots can have defaults that apply unless overridden.",
        "Inheritance: Child frames inherit slots and values from parent frames.",
        "Procedural attachment: Slots can trigger procedures (IF-NEEDED, IF-ADDED).",
        "Advantages: Natural for object-like knowledge, supports defaults, inheritance.",
        "Disadvantages: Rigid structure, not good for dynamic or rule-based knowledge.",
    ]
    for f in frame_features:
        story.append(Paragraph(f"  • {f}", s['bullet']))

    # Production Rules
    story.append(Paragraph("► 5. Production Rules (Rule-Based Systems)", s['subsec']))
    story.append(Paragraph(
        "Knowledge is stored as IF-THEN rules: IF (condition) THEN (action/conclusion). "
        "A <b>Rule-Based System</b> has: Working Memory (current facts), Production Memory "
        "(all the rules), Inference Engine (matches rules to facts and fires them).",s['body']))
    story.append(formula_box("IF <condition> THEN <conclusion/action>", s, C['orange_bg'], C['orange']))
    story.append(Paragraph(
        "Example rules for medical diagnosis:\n"
        "R1: IF patient has fever AND headache THEN suspect flu\n"
        "R2: IF patient has flu AND cough THEN prescribe antiviral\n"
        "R3: IF patient has rash AND fever THEN suspect measles",s['note']))

    # Scripts
    story.append(Paragraph("► 6. Scripts", s['subsec']))
    story.append(Paragraph(
        "Scripts represent sequences of events in a particular context. "
        "Proposed by Schank and Abelson. Like a frame but for EVENTS and PROCESSES in time. "
        "Example: 'Restaurant Script' — Enter, Sit, Order, Eat, Pay, Leave. "
        "Used in NLP to understand stories and infer unstated facts.",s['body']))

    # 2.3 — Inference
    story.append(sec_box("2.3  Inference Mechanisms", s, C['indigo_bg'], C['indigo']))
    story.append(Spacer(1,0.15*cm))
    story.append(Paragraph(
        "An <b>Inference Mechanism</b> is the procedure used to derive new knowledge from existing knowledge. "
        "The main inference methods are:",s['body']))

    infer_types = [
        ("Forward Chaining (Data-Driven)","Start with KNOWN FACTS and apply rules forward to derive new facts "
         "until the goal is reached or no more rules apply. Like filling out a form step-by-step. "
         "Example: Given it's raining → roads wet → accident possible → drive carefully. "
         "Used in: Expert systems, monitoring systems, diagnosis."),
        ("Backward Chaining (Goal-Driven)","Start with the GOAL and work backwards to find facts that support it. "
         "Ask: 'What do I need to prove this goal?' Recursively find sub-goals. "
         "Example: Goal: 'Should I take umbrella?' → Is rain expected? → What is weather forecast? → ... "
         "Used in: Prolog, planning systems, proving theorems."),
        ("Resolution Refutation","A proof technique for First-Order Logic. "
         "Convert statements to Conjunctive Normal Form (CNF), negate the goal, "
         "then use resolution rule to derive a contradiction (empty clause). "
         "If contradiction found → original goal is provable. Used in logic theorem provers."),
        ("Modus Ponens","Basic rule: IF P is true AND (P → Q) is true, THEN Q is true. "
         "Example: 'It is raining' (P). 'If raining then roads wet' (P→Q). Therefore: 'Roads are wet' (Q)."),
    ]
    for iname, idesc in infer_types:
        story.append(Paragraph(f"<b>► {iname}:</b>", s['subsec']))
        story.append(Paragraph(idesc, s['body']))

    # 2.4 — Blackboard System
    story.append(sec_box("2.4  Blackboard Architecture (Asked in 2025 as short note)", s, C['indigo_bg'], C['indigo']))
    story.append(Spacer(1,0.15*cm))
    story.append(Paragraph(
        "The <b>Blackboard Architecture</b> is a problem-solving model where multiple independent "
        "knowledge sources (KS) communicate via a shared global data structure called the "
        "<b>Blackboard</b>. Originated from the HEARSAY speech understanding system (1970s).",s['body']))
    story.append(Paragraph("<b>Components of Blackboard System:</b>", s['subsec']))
    bb_components = [
        ("Blackboard (Global Workspace)","A shared, structured memory where all partial solutions, "
         "hypotheses, and results are stored. All knowledge sources can read from and write to it. "
         "Divided into levels — each level represents a different abstraction of the problem."),
        ("Knowledge Sources (KS)","Independent modules, each specializing in a specific aspect of "
         "the problem. They are self-contained — each knows when it can contribute (trigger condition) "
         "and what it can contribute (action). They do NOT communicate with each other directly — "
         "only through the blackboard."),
        ("Control Component (Scheduler)","Decides WHICH knowledge source to activate next. "
         "Monitors the blackboard for changes, evaluates which KS is most applicable, "
         "and schedules execution. Acts like a manager coordinating the KSes."),
    ]
    for cname, cdesc in bb_components:
        story.append(Paragraph(f"<b>• {cname}:</b> {cdesc}", s['bullet']))
    story.append(Paragraph("<b>How it works:</b>", s['subsec']))
    story.append(Paragraph(
        "1. Problem placed on Blackboard. "
        "2. Control monitors blackboard, identifies which KS is triggered. "
        "3. Selected KS reads from blackboard, performs computation, writes result back. "
        "4. New data triggers other KSes. "
        "5. Process continues until a complete solution is built on the blackboard.",s['body']))
    story.append(Paragraph(
        "<b>Advantages:</b> Modular (easy to add/remove KSes), handles uncertain/incomplete data, "
        "flexible control, supports parallel processing. "
        "<b>Disadvantages:</b> Difficult to design, control strategy is complex, performance depends on KS quality.",s['body']))

    # KR Questions
    story.append(Spacer(1,0.3*cm))
    story.append(banner("PRACTICE QUESTIONS & ANSWERS — TOPIC 2: KR & INFERENCE", C['indigo'], s))
    story.append(Spacer(1,0.2*cm))

    q15_kr = [
        (
            "What is the semantic net? (Asked in 2024 — 1.5 marks)",
            "A Semantic Network is a graphical knowledge representation method using a directed labeled graph. "
            "Nodes represent concepts or objects; labeled arcs represent relationships (IS-A, HAS-A, CAN). "
            "Example: Dog IS-A Animal, Dog HAS-A Tail. It supports inheritance — child nodes inherit parent properties."
        ),
        (
            "Discuss the various ways of knowledge representation. (Asked in 2025 — 1.5 marks)",
            "Main knowledge representation methods: (1) Logical representation — propositional and predicate logic. "
            "(2) Semantic networks — directed graphs with nodes and arcs. (3) Frames — slot-value data structures. "
            "(4) Production rules — IF-THEN rule systems. (5) Scripts — event sequence templates. (6) Partitioned networks."
        ),
        (
            "What is the difference between forward chaining and backward chaining?",
            "Forward chaining: Starts from known facts and applies rules forward to reach the goal (data-driven). "
            "Backward chaining: Starts from the goal and works backwards to verify supporting facts (goal-driven). "
            "Forward: Used in monitoring systems. Backward: Used in Prolog, planning. "
            "Forward produces all conclusions; backward proves a specific goal."
        ),
        (
            "What is a production rule system? Give an example.",
            "A production rule system stores knowledge as IF <condition> THEN <action> rules. "
            "It has three parts: Working Memory (current facts), Production Memory (rules), "
            "Inference Engine (matches and fires rules). Example: IF patient has fever AND sore throat "
            "THEN diagnose strep throat. Used in expert systems."
        ),
        (
            "What is a frame? What are its main components?",
            "A frame is a data structure representing stereotyped objects or situations. "
            "Main components: Frame name (e.g., 'Car'), Slots (attributes like Color, Weight), "
            "Values (slot content), Default values, and Procedures (IF-NEEDED, IF-ADDED). "
            "Frames support inheritance — child frames inherit parent slot values. Proposed by Minsky (1975)."
        ),
    ]
    for item in qa_block("1.5 Marks Questions with Answers", HexColor('#283593'), q15_kr, s):
        story.append(item)

    story.append(Spacer(1,0.25*cm))

    q5_kr = [
        (
            "Draw the diagram of the blackboard system and explain each component. (Asked in 2024 & 2025 — 5 marks)",
            "BLACKBOARD ARCHITECTURE — COMPLETE EXPLANATION\n\n"
            "The Blackboard Architecture is a cooperative problem-solving model where independent "
            "Knowledge Sources (KS) collaborate through a shared global data structure — the BLACKBOARD. "
            "Originally developed for the HEARSAY-II speech understanding system in the 1970s.\n\n"
            "THREE MAIN COMPONENTS:\n\n"
            "1. THE BLACKBOARD (Central Shared Memory):\n"
            "The blackboard is a global, hierarchically-organized data structure that serves as the "
            "single communication medium. It stores: raw input data, partial solutions, hypotheses at "
            "various abstraction levels, and the final solution. "
            "It is organized into LEVELS — for example, in a speech recognition system: "
            "Level 1 = Acoustic signals, Level 2 = Phonemes, Level 3 = Syllables, Level 4 = Words, "
            "Level 5 = Phrases, Level 6 = Sentences.\n\n"
            "2. KNOWLEDGE SOURCES (KSes):\n"
            "Independent modules, each solving a specific aspect of the problem. "
            "Each KS has two parts:\n"
            "  a) Trigger Condition: Specifies WHEN the KS should be activated (based on blackboard state)\n"
            "  b) Action: What the KS computes and writes back to the blackboard\n"
            "KSes do not communicate with each other — only through the blackboard. "
            "This makes the system highly modular.\n\n"
            "3. CONTROL COMPONENT (Scheduler/Monitor):\n"
            "Acts as the 'manager' of the system. It:\n"
            "  • Continuously monitors the blackboard for changes\n"
            "  • Checks which KSes are triggered by the current state\n"
            "  • Uses a scheduling strategy to decide which KS to run next\n"
            "  • Scheduling can be: opportunistic (best first), priority-based, or round-robin\n\n"
            "WORKING OF BLACKBOARD SYSTEM:\n"
            "1. Problem/input data placed on blackboard at lowest level.\n"
            "2. Control detects which KS is triggered by this data.\n"
            "3. Selected KS reads relevant data from blackboard.\n"
            "4. KS performs computation and writes results (higher-level hypothesis) to blackboard.\n"
            "5. New data triggers other KSes — process continues.\n"
            "6. Cycle repeats until solution appears at the highest level.\n\n"
            "DIAGRAM DESCRIPTION:\n"
            "[Blackboard (vertical, layered)] ←reads/writes→ [KS1, KS2, KS3...KSn (surrounding)]\n"
            "                                     ↑control↑\n"
            "                              [Control Component (Scheduler)]\n\n"
            "APPLICATIONS: Speech recognition, image interpretation, scientific discovery systems, "
            "sonar signal processing, and multi-agent AI systems.\n\n"
            "ADVANTAGES: Modular, flexible, handles uncertainty, supports parallel execution.\n"
            "DISADVANTAGES: Complex control design, overhead of blackboard communication, "
            "hard to debug."
        ),
        (
            "Explain different techniques of Knowledge Representation with examples. (Asked in 2024 — 10 marks split as 5+5)",
            "KNOWLEDGE REPRESENTATION TECHNIQUES\n\n"
            "Knowledge Representation (KR) is the area of AI concerned with how knowledge about the "
            "world can be formally captured so an AI system can reason with it.\n\n"
            "1. LOGICAL REPRESENTATION:\n"
            "Uses formal logic. Two main types:\n"
            "a) Propositional Logic: Deals with TRUE/FALSE propositions connected by AND, OR, NOT, →.\n"
            "   Example: P='Raining', Q='Roads wet'. Rule: P → Q.\n"
            "b) FOPL (First-Order Predicate Logic): Uses predicates, variables, quantifiers.\n"
            "   Example: ∀x[Human(x) → Mortal(x)], Human(Socrates) ⊢ Mortal(Socrates).\n"
            "Good for formal proofs but computationally expensive.\n\n"
            "2. SEMANTIC NETWORKS:\n"
            "Directed graph — Nodes = concepts, Arcs = relationships.\n"
            "Example: Fido IS-A Dog IS-A Animal; Dog HAS-A Tail; Dog CAN Bark.\n"
            "Supports inheritance. Intuitive and visual. Limited expressiveness for quantifiers.\n\n"
            "3. FRAMES:\n"
            "Slot-value data structures for stereotyped objects.\n"
            "Example: FRAME: Bird | Slot: Wings=2 | Slot: Can=Fly (default) | Slot: Sound=Tweet.\n"
            "Penguin frame inherits Bird but overrides Can=Swim.\n"
            "Good for objects with defaults and inheritance.\n\n"
            "4. PRODUCTION RULES:\n"
            "IF-THEN rules. Example: IF fever AND cough THEN flu-likely.\n"
            "Used in expert systems. Easy to add/remove rules.\n\n"
            "5. SCRIPTS:\n"
            "Event sequences. Restaurant script: Enter→Sit→Order→Eat→Pay→Leave.\n"
            "Used in NLP to understand stories.\n\n"
            "Each technique has its strengths — the choice depends on what kind of knowledge "
            "needs to be represented."
        ),
        (
            "What is semantic net? How is it different from partitioned net? Use partitioned net to express: "
            "(i) Every lunatic hit a doctor (ii) The lunatic hit the door (iii) Every lunatic has hit every doctor. "
            "(Asked in 2018 — 5 marks)",
            "SEMANTIC NETS AND PARTITIONED NETS\n\n"
            "SEMANTIC NETWORK:\n"
            "A semantic network is a directed labeled graph where nodes represent objects/concepts and "
            "arcs represent named relationships between them. It is good for representing static facts, "
            "inheritance hierarchies, and properties.\n"
            "Limitation: Cannot distinguish 'Every lunatic hit A doctor' (one doctor) from "
            "'Every lunatic hit EVERY doctor' (all doctors) — the scope of quantifiers is ambiguous.\n\n"
            "PARTITIONED NETWORK:\n"
            "A partitioned network divides the network into named SPACES (partitions). "
            "Each space represents a specific scope or context:\n"
            "• Generic Space (G-space): Represents universally quantified (∀) variables\n"
            "• Individual Space (I-space): Represents existentially quantified (∃) variables\n\n"
            "REPRESENTING THE THREE SENTENCES:\n\n"
            "(i) 'Every lunatic hit a doctor' (∀ lunatic, ∃ doctor):\n"
            "G-space contains: variable 'L' representing ANY lunatic\n"
            "I-space (inside G-space): individual 'D' — one doctor (may be different for each lunatic)\n"
            "Arc: L --hit--> D\n\n"
            "(ii) 'The lunatic hit the door' (specific individuals):\n"
            "I-space for 'The-Lunatic' and I-space for 'The-Door'\n"
            "Arc: The-Lunatic --hit--> The-Door\n"
            "(No generic spaces — both are specific/individual)\n\n"
            "(iii) 'Every lunatic has hit every doctor' (∀ lunatic, ∀ doctor):\n"
            "Outer G-space: variable 'L' for any lunatic\n"
            "Inner G-space (nested inside): variable 'D' for any doctor\n"
            "Arc: L --hit--> D\n\n"
            "KEY DIFFERENCE: Semantic nets cannot represent quantifier scope — all facts are global. "
            "Partitioned nets use nested spaces to correctly represent the scope of each quantifier, "
            "making them more expressive for representing complex statements."
        ),
    ]
    for item in qa_block("5 Marks Questions with Answers (300–500 words each)",
                          HexColor('#3949ab'), q5_kr, s):
        story.append(item)

    story.append(Spacer(1,0.25*cm))

    q10_kr = [
        (
            "Explain different techniques of Knowledge Representation with examples. (Asked in 2024 — 10 marks)",
            "KNOWLEDGE REPRESENTATION — COMPLETE DETAILED ANSWER\n\n"
            "INTRODUCTION:\n"
            "Knowledge Representation (KR) is a fundamental area of AI concerned with how knowledge "
            "about the world can be formally captured in a computer system so that it can reason, "
            "make decisions, and solve problems intelligently. "
            "A good KR scheme must be representationally adequate, inferentially adequate, "
            "inferentially efficient, and acquisitionally adequate.\n\n"
            "TECHNIQUE 1: LOGICAL REPRESENTATION\n"
            "Uses formal logic to represent facts and rules with mathematical precision.\n"
            "a) Propositional Logic: Statements are true/false propositions.\n"
            "   Operators: ∧ (AND), ∨ (OR), ¬ (NOT), → (IMPLIES), ↔ (IFF)\n"
            "   Example: P = 'It rains'. Q = 'Roads are wet'. Rule: P → Q.\n"
            "   Limitation: Cannot handle objects, properties, or relationships explicitly.\n"
            "b) First-Order Predicate Logic (FOPL): Uses predicates, variables, quantifiers.\n"
            "   Universal: ∀x [Human(x) → Mortal(x)] — All humans are mortal.\n"
            "   Existential: ∃x [Dog(x) ∧ Friendly(x)] — Some dog is friendly.\n"
            "   Advantages: Very expressive, supports formal proofs.\n"
            "   Disadvantages: Computationally expensive, undecidable in general.\n\n"
            "TECHNIQUE 2: SEMANTIC NETWORKS\n"
            "Directed labeled graph — nodes = concepts, arcs = relationships.\n"
            "Key relationships: IS-A (class membership), HAS-A (possession), CAN (ability).\n"
            "Inheritance: Penguin IS-A Bird → Penguin inherits Wings=2 from Bird.\n"
            "Example: Tweety IS-A Bird IS-A Animal. Bird HAS Wings. Bird CAN Fly.\n"
            "Advantage: Visual, intuitive, inheritance supported.\n"
            "Disadvantage: Weak expressiveness for quantifiers and rules.\n\n"
            "TECHNIQUE 3: PARTITIONED NETWORKS\n"
            "Extension of semantic networks with named spaces to handle quantifier scope.\n"
            "G-space for universal (∀), I-space for existential (∃) quantifiers.\n"
            "Example: 'Every lunatic hit a doctor' → G-space(L) → I-space(D) with L-hit-D.\n\n"
            "TECHNIQUE 4: FRAMES\n"
            "Proposed by Minsky (1975). Slot-value structures for stereotyped objects.\n"
            "Components: Frame name, Slots, Values, Defaults, Procedures.\n"
            "Example:\n"
            "  FRAME: Bird | Slot: Feathers=Yes | Slot: Legs=2 | Slot: Can=Fly (DEFAULT)\n"
            "  FRAME: Penguin (IS-A Bird) | Slot: Can=Swim (OVERRIDES Fly)\n"
            "Advantage: Supports defaults, inheritance, procedural attachment.\n"
            "Disadvantage: Rigid structure, not good for dynamic knowledge.\n\n"
            "TECHNIQUE 5: PRODUCTION RULES\n"
            "IF-THEN rules stored in Production Memory. Inference Engine matches rules to "
            "Working Memory facts and fires applicable rules.\n"
            "Example medical expert system:\n"
            "R1: IF fever AND headache THEN flu-suspected\n"
            "R2: IF flu-suspected AND cough THEN prescribe-antiviral\n"
            "Conflict resolution: When multiple rules fire — choose by specificity, priority, recency.\n"
            "Advantage: Modular, easy to explain reasoning.\n"
            "Disadvantage: Many rules → slow matching, hard to maintain.\n\n"
            "TECHNIQUE 6: SCRIPTS\n"
            "Schank & Abelson (1977). Represent stereotyped event sequences.\n"
            "Components: Entry conditions, Roles, Props, Scenes, Results.\n"
            "Example 'Restaurant Script': Scene1=Entering, Scene2=Ordering, Scene3=Eating, Scene4=Paying.\n"
            "Used in NLP for story understanding and question answering.\n\n"
            "COMPARISON TABLE:\n"
            "Logical: Highest expressiveness, hardest to use.\n"
            "Semantic Nets: Visual, moderate expressiveness, good for hierarchies.\n"
            "Frames: Best for objects with properties and defaults.\n"
            "Rules: Best for procedural/diagnostic reasoning.\n"
            "Scripts: Best for event/process sequences.\n\n"
            "CONCLUSION: Different KR techniques suit different types of knowledge. "
            "Modern AI systems often combine multiple techniques — for example, an expert system "
            "might use production rules for reasoning and frames for object representation."
        ),
    ]
    for item in qa_block("10 Marks Questions with Answers (500–700 words each)",
                          HexColor('#1a237e'), q10_kr, s):
        story.append(item)

    story.append(Spacer(1,0.25*cm))

    q15_kr_long = [
        (
            "Write short notes on: (a) Semantic Nets and Frames (b) Blackboard Architecture. "
            "(Asked in 2025 as Q7 — 5+5+5=15 marks combined)",
            "SHORT NOTE (a): SEMANTIC NETS AND FRAMES\n\n"
            "SEMANTIC NETWORKS:\n"
            "A Semantic Network is a graphical knowledge representation method using a directed labeled graph. "
            "Proposed by Quillian (1968) based on psychological models of human memory.\n\n"
            "Structure: Nodes represent concepts, objects, or events. Directed arcs represent relationships. "
            "Each arc is labeled with the relationship type.\n\n"
            "Common Relationships:\n"
            "• IS-A: Class membership or subclass (Dog IS-A Animal)\n"
            "• HAS-A: Property/attribute possession (Dog HAS-A Tail)\n"
            "• HAS-PART: Component (Car HAS-PART Engine)\n"
            "• CAN: Capability (Bird CAN Fly)\n"
            "• IS-INSTANCE-OF: Object-class relationship (Fido IS-INSTANCE-OF Dog)\n\n"
            "Example Network: Fido IS-INSTANCE-OF Dog IS-A Mammal IS-A Animal. "
            "Dog HAS-A 4-Legs. Dog CAN Bark. Mammal HAS-A Warm-Blood. Animal CAN Breathe.\n"
            "By inheritance: Fido CAN Bark (from Dog), Fido HAS Warm-Blood (from Mammal), "
            "Fido CAN Breathe (from Animal).\n\n"
            "Advantages: Visually clear, natural representation of hierarchies, "
            "inheritance reduces redundancy, easy to understand.\n"
            "Disadvantages: Cannot represent quantifiers (∀, ∃), negative facts, complex rules, "
            "or procedural knowledge. Ambiguous for sentences with multiple quantifiers.\n\n"
            "FRAMES:\n"
            "Proposed by Marvin Minsky (1975). A Frame is a data structure for representing "
            "stereotyped situations or objects — a template with named slots and values.\n\n"
            "Frame Components:\n"
            "• Frame Name: Identifier (e.g., 'Car', 'Person', 'Meeting')\n"
            "• Slots: Attributes of the concept (Color, Size, Name, Speed)\n"
            "• Fillers: Values of slots (Red, Large, 'Toyota')\n"
            "• Default Values: Applied when no specific value given\n"
            "• Procedures: IF-NEEDED (computed when accessed), IF-ADDED (triggered when slot filled)\n"
            "• Inheritance: Child frames inherit parent frame slots\n\n"
            "Example: FRAME: Person | Name: <unknown> | Age: <unknown> | Occupation: Student (default) | "
            "Legs: 2 (default) | Arms: 2 (default)\n\n"
            "FRAME: Student (IS-A Person) | University: <unknown> | GPA: <unknown> | "
            "Takes-Courses: <unknown>\n\n"
            "When you create 'John IS-A Student': John inherits Legs=2, Arms=2, "
            "and the Student-specific slots.\n\n"
            "Advantage: Natural for objects, supports defaults and inheritance, "
            "enables both declarative and procedural knowledge.\n"
            "Disadvantage: Rigid template, not flexible for dynamic or relational knowledge.\n\n"
            "---\n\n"
            "SHORT NOTE (b): BLACKBOARD ARCHITECTURE\n\n"
            "The Blackboard Architecture is a cooperative problem-solving model where multiple "
            "independent Knowledge Sources (KSes) collaborate through a shared global data structure "
            "called the Blackboard. Developed for the HEARSAY-II speech recognition system (1970s).\n\n"
            "Three Components:\n\n"
            "1. Blackboard (Global Workspace): A hierarchically structured shared memory with multiple "
            "abstraction levels. All KSes read from and write to this. Stores partial results, "
            "hypotheses, and the evolving solution. Example levels in speech: "
            "Signal → Segment → Phoneme → Syllable → Word → Phrase → Sentence.\n\n"
            "2. Knowledge Sources (KSes): Independent, specialized problem-solving modules. "
            "Each KS has a Trigger Condition (when to activate) and an Action (what to do). "
            "KSes are activated by changes on the blackboard, perform local computation, "
            "and write results back. KSes do not communicate directly — only via blackboard.\n\n"
            "3. Control Component (Scheduler): The 'manager' that monitors the blackboard, "
            "identifies triggered KSes, evaluates their priority/usefulness, and decides which "
            "to execute next. Scheduling strategies: Opportunistic (best contribution first), "
            "priority-based, or breadth-first.\n\n"
            "Working Cycle:\n"
            "Input on blackboard → Control identifies triggered KS → KS executes, writes to blackboard "
            "→ New data triggers other KSes → Cycle repeats → Final solution at top level.\n\n"
            "Applications: Speech recognition (HEARSAY-II), image interpretation, sonar analysis, "
            "scientific discovery, distributed AI systems.\n\n"
            "Advantages: Modular (add/remove KSes freely), handles uncertain/incomplete data, "
            "flexible, supports parallelism, opportunistic problem-solving.\n\n"
            "Disadvantages: Complex to design, control strategy difficult to optimize, "
            "blackboard becomes a bottleneck with many KSes, debugging is hard."
        ),
    ]
    for item in qa_block("15 Marks Questions with Answers (700–1000 words each)",
                          HexColor('#b71c1c'), q15_kr_long, s):
        story.append(item)

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # TOPIC 3 ── GENETIC ALGORITHM
    # ════════════════════════════════════════════════════════════════════════
    story.append(banner("TOPIC 3 — GENETIC ALGORITHM (GA)", C['green'], s))
    story.append(Spacer(1,0.3*cm))
    story.append(badge_row("Genetic Algorithm","85%",C['green'],
        "<b>HIGH probability — appeared in every exam!</b> "
        "2025: What is GA + genetic operations (10M). "
        "2024: Explain each step of GA (10M), list applications (1.5M). "
        "2018: Explain GA (5M). "
        "Know the complete algorithm, all 5 operators (selection, crossover, mutation, etc.), "
        "fitness function, and applications.", s))
    story.append(Spacer(1,0.4*cm))

    # 3.1
    story.append(sec_box("3.1  Introduction to Genetic Algorithms", s, C['green_bg'], C['green']))
    story.append(Spacer(1,0.15*cm))
    story.append(Paragraph(
        "A <b>Genetic Algorithm (GA)</b> is a search and optimization technique inspired by "
        "<b>Charles Darwin's theory of natural evolution</b> — 'Survival of the Fittest'. "
        "Developed by John Holland in the 1970s, GA mimics the process of natural selection "
        "where the strongest individuals survive and reproduce, passing their genes to offspring.",s['body']))
    story.append(Paragraph(
        "Simple Analogy: Imagine you're trying to find the best possible schedule for 100 employees. "
        "Instead of trying every possible combination (which could be trillions), GA starts with "
        "a set of random schedules (population), evaluates which ones are better (fitness), "
        "combines the best ones (crossover), makes small random tweaks (mutation), "
        "and keeps improving generation after generation until it finds a great solution.",s['note']))

    # 3.2
    story.append(sec_box("3.2  Biological Inspiration — Genetics Terminology", s, C['green_bg'], C['green']))
    story.append(Spacer(1,0.15*cm))
    bio_ga = [
        ["Biological Term","GA Equivalent","Meaning in GA"],
        ["Chromosome","Individual / Solution","One complete candidate solution to the problem"],
        ["Gene","Bit / Character in string","One component/parameter of the solution"],
        ["Allele","Value of a gene","The actual value at a gene position (0 or 1 in binary)"],
        ["Population","Set of individuals","Collection of all current candidate solutions"],
        ["Fitness","Objective function value","How good is this solution? Higher = better"],
        ["Selection","Selecting parents","Choosing better solutions to reproduce"],
        ["Crossover","Recombination","Combining parts of two parents to create offspring"],
        ["Mutation","Random gene change","Random small change to maintain diversity"],
        ["Generation","Iteration","One complete cycle of GA"],
    ]
    story.append(three_col_table(bio_ga, [4*cm,4*cm,W-2.8*cm-8*cm], C['green']))

    # 3.3
    story.append(sec_box("3.3  Representation — Encoding Solutions", s, C['green_bg'], C['green']))
    story.append(Spacer(1,0.15*cm))
    story.append(Paragraph(
        "Before applying GA, each solution must be <b>encoded as a chromosome</b>. Common encodings:",s['body']))
    encodings = [
        ("Binary Encoding","Most common. Each gene is 0 or 1.",
         "Example: Chromosome = 101101 (6-bit binary string)"),
        ("Integer Encoding","Genes are integers.",
         "Example: [2,5,1,4,3,6] for a scheduling problem"),
        ("Real-Valued Encoding","Genes are real numbers. Good for continuous optimization.",
         "Example: [1.5, 3.7, 0.2, 4.1] for neural network weights"),
        ("Permutation Encoding","Each gene is a position. Used for ordering problems.",
         "Example: [3,1,4,2,5] for Travelling Salesman Problem (TSP)"),
    ]
    for ename, edesc, eex in encodings:
        story.append(Paragraph(f"<b>{ename}:</b> {edesc}  |  {eex}", s['bullet']))

    # 3.4
    story.append(sec_box("3.4  Complete GA Algorithm — Step by Step", s, C['green_bg'], C['green']))
    story.append(Spacer(1,0.15*cm))
    story.append(info_box(
        "⚡ EXAM KEY: This algorithm is asked almost every year. Write all steps with the "
        "correct GA terminology. Marks are given for knowing the complete flow.", s,
        C['yellow_bg'], C['orange']))
    story.append(Spacer(1,0.15*cm))

    ga_steps = [
        ("STEP 1","Initialize Population",
         "Randomly generate an initial population of N chromosomes. "
         "Each chromosome is a randomly encoded candidate solution. "
         "Population size N is typically 50–500. "
         "Example (binary, 6-bit): Pop = {101101, 011010, 110100, 001111, 100001}"),
        ("STEP 2","Evaluate Fitness",
         "Calculate the FITNESS VALUE for each chromosome using the Fitness Function f(x). "
         "The fitness function defines 'how good' a solution is. "
         "Example: For maximizing f(x) = x², decode binary to integer and compute x²: "
         "101101 → 45 → f(45) = 2025. "
         "Higher fitness = better solution."),
        ("STEP 3","Check Termination",
         "Stop if: (a) Maximum generations reached, OR "
         "(b) Fitness reaches acceptable threshold, OR "
         "(c) Population converges (all chromosomes similar). "
         "If not terminated, proceed to selection."),
        ("STEP 4","Selection",
         "Select chromosomes to be PARENTS for next generation. "
         "Better fitness → higher selection probability. "
         "Methods: (a) Roulette Wheel — probability ∝ fitness, (b) Tournament — pick best of random group, "
         "(c) Rank Selection — rank by fitness, select by rank probability."),
        ("STEP 5","Crossover (Recombination)",
         "Combine two parent chromosomes to create OFFSPRING. Applied with crossover probability Pc (typically 0.6–0.9). "
         "Types: Single-Point, Two-Point, Uniform crossover. "
         "Example (Single-Point, cut at position 3):\n"
         "Parent 1: 101|101  Parent 2: 011|010 → Child 1: 101010  Child 2: 011101"),
        ("STEP 6","Mutation",
         "Randomly alter one or more genes in a chromosome. Applied with very low probability Pm (typically 0.001–0.01). "
         "Prevents population from converging too early (avoids local optima). "
         "Example: Flip a random bit — 101101 → 101001 (bit 4 flipped). "
         "Too much mutation → random search. Too little → premature convergence."),
        ("STEP 7","Replace Population",
         "Form the new generation from offspring. Strategies: "
         "(a) Generational replacement — all offspring replace all parents, "
         "(b) Elitism — keep best few from previous generation + add offspring, "
         "(c) Steady-state — replace worst individuals with new offspring."),
        ("STEP 8","Go to Step 2",
         "Evaluate fitness of new population. Repeat the cycle until termination condition met. "
         "Each cycle = one GENERATION. Return the best chromosome found as the solution."),
    ]
    for step_no, step_name, step_desc in ga_steps:
        bg = C['green_bg'] if int(step_no[-1]) % 2 == 1 else C['accent']
        row = [[Paragraph(f"{step_no}: {step_name}",
                           ParagraphStyle('sn', fontName='Helvetica-Bold', fontSize=10,
                                          textColor=C['green'])),
                Paragraph(step_desc.replace('\n','<br/>'), s['body'])]]
        rt = Table(row, colWidths=[3.8*cm, W-6.6*cm])
        rt.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,-1),bg),
            ('GRID',(0,0),(-1,-1),0.5,HexColor('#bdbdbd')),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
            ('LEFTPADDING',(0,0),(-1,-1),8),
        ]))
        story.append(rt)

    # 3.5 — Genetic Operators
    story.append(sec_box("3.5  Genetic Operators in Detail", s, C['green_bg'], C['green']))
    story.append(Spacer(1,0.15*cm))

    story.append(Paragraph("► SELECTION OPERATORS:", s['subsec']))
    sel_ops = [
        ("Roulette Wheel Selection (Fitness Proportionate)",
         "Each chromosome gets a slice of the roulette wheel proportional to its fitness. "
         "A random spin selects a chromosome — higher fitness = bigger slice = higher chance.\n"
         "P(i) = f(i) / Σ f(j)  [Probability of selecting chromosome i]"),
        ("Tournament Selection",
         "Randomly pick k chromosomes from population. The best among these k wins. "
         "Repeat to get each parent. Parameter k controls selection pressure."),
        ("Rank Selection",
         "Rank all chromosomes by fitness. Assign selection probability based on RANK not raw fitness. "
         "Avoids domination by few high-fitness individuals."),
        ("Elitism",
         "Always copy the best individual(s) unchanged to next generation. "
         "Ensures the best solution is never lost."),
    ]
    for sname, sdesc in sel_ops:
        story.append(Paragraph(f"<b>{sname}:</b>", s['bullet']))
        story.append(Paragraph(sdesc.replace('\n','<br/>'), s['sub_bullet']))

    story.append(Paragraph("► CROSSOVER OPERATORS:", s['subsec']))
    cross_ops = [
        ("Single-Point Crossover",
         "Choose one random crossover point. Swap the tails of the two parents.\n"
         "P1=10110|01  P2=11001|10  →  C1=10110|10  C2=11001|01"),
        ("Two-Point Crossover",
         "Choose two crossover points. Swap the segment between them.\n"
         "P1=10|110|01  P2=11|001|10  →  C1=10|001|01  C2=11|110|10"),
        ("Uniform Crossover",
         "For each gene, flip a coin. Take from P1 if heads, P2 if tails. More disruptive than single-point."),
        ("Arithmetic Crossover",
         "For real-valued chromosomes: C = α·P1 + (1−α)·P2 for some weight α."),
    ]
    for cname, cdesc in cross_ops:
        story.append(Paragraph(f"<b>{cname}:</b>", s['bullet']))
        story.append(Paragraph(cdesc.replace('\n','<br/>'), s['sub_bullet']))

    story.append(Paragraph("► MUTATION OPERATORS:", s['subsec']))
    mut_ops = [
        ("Bit Flip Mutation (Binary)","Flip a randomly selected bit: 0→1 or 1→0."),
        ("Swap Mutation","Swap two randomly chosen genes in the chromosome."),
        ("Gaussian Mutation (Real-valued)","Add random Gaussian noise to a gene value."),
        ("Inversion Mutation","Reverse the order of genes between two random points."),
    ]
    for mname, mdesc in mut_ops:
        story.append(Paragraph(f"<b>{mname}:</b> {mdesc}", s['bullet']))

    # 3.6 — Fitness Function
    story.append(sec_box("3.6  Fitness Function — The Key to GA", s, C['green_bg'], C['green']))
    story.append(Paragraph(
        "The <b>Fitness Function</b> is the most important component of GA — it defines the problem. "
        "It evaluates how good a solution is. The GA tries to maximize fitness. "
        "Designing a good fitness function is an art — it must:\n"
        "• Accurately measure solution quality\n"
        "• Differentiate between good and bad solutions\n"
        "• Be computationally feasible\n"
        "• Guide the search in the right direction",s['body']))
    story.append(formula_box(
        "Example: Maximize f(x) = x²  for x ∈ [0, 31]\n"
        "Encoding: 5-bit binary  |  '11010' → x=26 → f(26) = 676\n"
        "Fitness proportionate probability: P(i) = f(i) / Σ f(j)", s))

    # 3.7 — Applications
    story.append(sec_box("3.7  Applications of Genetic Algorithms", s, C['green_bg'], C['green']))
    ga_apps = [
        ("Travelling Salesman Problem (TSP)","Find the shortest route visiting all cities exactly once."),
        ("Neural Network Training","Evolving optimal weights instead of backpropagation."),
        ("Job Scheduling","Optimize task assignment to minimize time/cost."),
        ("VLSI Circuit Design","Optimize circuit layout on a chip."),
        ("Machine Learning","Feature selection, hyperparameter tuning."),
        ("Game Playing","Evolving strategies for game agents."),
        ("Structural Engineering","Optimizing design of bridges, trusses."),
        ("Bioinformatics","Protein structure prediction, DNA sequence alignment."),
        ("Financial Optimization","Portfolio optimization, trading strategies."),
        ("Robot Motion Planning","Finding optimal path for robots."),
    ]
    app_data_ga = [["Application","Description"]] + [[a,b] for a,b in ga_apps]
    story.append(two_col_table(app_data_ga, 5*cm, C['green'], s))

    # 3.8 — Advantages & Disadvantages
    story.append(sec_box("3.8  Advantages and Disadvantages of GA", s, C['green_bg'], C['green']))
    ga_pros = [
        "Can solve problems with no closed-form solution or gradient information.",
        "Works well for large, complex search spaces.",
        "Naturally handles multi-modal problems (multiple local optima).",
        "Can optimize multiple objectives simultaneously.",
        "Easy to parallelize — multiple chromosomes evaluated independently.",
        "Requires only the fitness function — no mathematical model of the problem.",
    ]
    story.append(Paragraph("<b>ADVANTAGES:</b>", s['subsec']))
    for p in ga_pros: story.append(Paragraph(f"✅  {p}", s['bullet']))

    ga_cons = [
        "No guaranteed optimal solution — may find near-optimal.",
        "Computationally expensive for very large populations or complex fitness functions.",
        "Premature convergence — population may converge too early to a local optimum.",
        "Parameter tuning (population size, Pc, Pm) is problem-dependent and non-trivial.",
        "Encoding the problem as chromosomes can be difficult.",
        "Slower than specialized algorithms for well-understood problems.",
    ]
    story.append(Paragraph("<b>DISADVANTAGES:</b>", s['subsec']))
    for c in ga_cons: story.append(Paragraph(f"❌  {c}", s['bullet']))

    # GA Questions
    story.append(Spacer(1,0.3*cm))
    story.append(banner("PRACTICE QUESTIONS & ANSWERS — TOPIC 3: GENETIC ALGORITHM", C['green'], s))
    story.append(Spacer(1,0.2*cm))

    q15_ga = [
        (
            "List out the applications of the Genetic Algorithm. (Asked in 2024 — 1.5 marks)",
            "Applications of GA: (1) Travelling Salesman Problem — shortest route optimization. "
            "(2) Neural network weight optimization. (3) Job scheduling. (4) VLSI circuit design. "
            "(5) Feature selection in ML. (6) Robot path planning. (7) Bioinformatics — protein structure prediction. "
            "(8) Financial portfolio optimization."
        ),
        (
            "What is a genetic algorithm? What are its main components?",
            "A Genetic Algorithm is a search/optimization technique inspired by natural evolution (Darwin's survival of fittest). "
            "Developed by John Holland. Main components: Population (candidate solutions), Fitness Function (evaluation), "
            "Selection (choosing parents), Crossover (recombination), Mutation (random change), and Replacement strategy."
        ),
        (
            "What is the fitness function in GA? Why is it important?",
            "The fitness function evaluates how good a candidate solution (chromosome) is. "
            "It assigns a numerical score — higher score = better solution. "
            "GA tries to maximize this score. It is the most crucial component because it guides "
            "the entire search direction. Example: For maximizing f(x)=x², the fitness of chromosome '11010' (=26) is 676."
        ),
        (
            "What is crossover in GA? Name its types.",
            "Crossover is a genetic operator that combines two parent chromosomes to create offspring. "
            "It mimics biological reproduction. Types: (1) Single-Point — swap at one cut point. "
            "(2) Two-Point — swap segment between two cut points. (3) Uniform — gene-by-gene random selection. "
            "(4) Arithmetic — weighted combination for real-valued chromosomes. Applied with probability Pc≈0.6–0.9."
        ),
        (
            "What is mutation in GA? Why is it important?",
            "Mutation is a genetic operator that randomly alters one or more genes in a chromosome. "
            "Applied with very low probability (Pm ≈ 0.001–0.01). "
            "Importance: Maintains genetic diversity, prevents premature convergence to local optima, "
            "introduces new genetic material not present in initial population. Types: Bit-flip, swap, Gaussian, inversion."
        ),
    ]
    for item in qa_block("1.5 Marks Questions with Answers", HexColor('#1b5e20'), q15_ga, s):
        story.append(item)

    story.append(Spacer(1,0.25*cm))

    q5_ga = [
        (
            "Explain the Genetic Algorithm. (Asked in 2018 — 5 marks)",
            "GENETIC ALGORITHM — EXPLANATION\n\n"
            "A Genetic Algorithm (GA) is a probabilistic search and optimization technique inspired by "
            "biological evolution. Developed by John Holland (1975), it mimics natural selection — "
            "better solutions survive, reproduce, and improve over generations.\n\n"
            "KEY COMPONENTS:\n"
            "1. Chromosome: A candidate solution encoded as a string (binary: 101101, integer: [2,4,1,3]).\n"
            "2. Population: A set of N chromosomes (N = 50 to 500 typically).\n"
            "3. Fitness Function: Evaluates solution quality. Higher fitness = better solution.\n"
            "4. Selection: Probabilistically selects better chromosomes as parents.\n"
            "5. Crossover: Combines two parents to create offspring (mimics reproduction).\n"
            "6. Mutation: Randomly alters genes to maintain diversity.\n\n"
            "GA ALGORITHM:\n"
            "Step 1: Initialize random population of N chromosomes.\n"
            "Step 2: Evaluate fitness of each chromosome.\n"
            "Step 3: If termination condition met, stop.\n"
            "Step 4: Select parents using roulette wheel/tournament selection.\n"
            "Step 5: Apply crossover (Pc ≈ 0.8) to create offspring.\n"
            "Step 6: Apply mutation (Pm ≈ 0.01) to offspring.\n"
            "Step 7: Replace population with offspring (elitism optional).\n"
            "Step 8: Go to Step 2.\n\n"
            "EXAMPLE — Maximize f(x) = x² for 5-bit chromosomes:\n"
            "Chromosome '11010' → x=26 → f=676 (high fitness)\n"
            "Chromosome '00101' → x=5 → f=25 (low fitness)\n"
            "Roulette: '11010' gets larger selection probability.\n\n"
            "ADVANTAGES: Works without gradient, handles large complex spaces, finds near-optimal solutions.\n"
            "APPLICATIONS: TSP, scheduling, neural network training, robotics."
        ),
        (
            "Explain every step of the Genetic Algorithm in detail. (Asked in 2024 — 10 marks, split view as 5+5)",
            "GENETIC ALGORITHM — STEP-BY-STEP DETAIL\n\n"
            "Step 1 — INITIALIZATION:\n"
            "Generate N random chromosomes as initial population. "
            "Each chromosome encodes one candidate solution. "
            "For binary encoding with L bits: each gene is randomly set to 0 or 1. "
            "Population size N is chosen based on problem complexity (50–500).\n\n"
            "Step 2 — FITNESS EVALUATION:\n"
            "Decode each chromosome. Compute f(chromosome) using the fitness function. "
            "Store fitness values. Identify the best chromosome so far.\n\n"
            "Step 3 — SELECTION:\n"
            "Select parent pairs for reproduction. Roulette Wheel: P(i) = f(i)/Σf(j). "
            "Better chromosomes are more likely to be selected but weaker ones also have a chance "
            "(maintaining diversity).\n\n"
            "Step 4 — CROSSOVER:\n"
            "For each parent pair, with probability Pc, apply crossover. "
            "Single-point: Choose random point k. Child1 = P1[1..k] + P2[k+1..L]. "
            "Child2 = P2[1..k] + P1[k+1..L]. If no crossover, children = copies of parents.\n\n"
            "Step 5 — MUTATION:\n"
            "For each gene in each offspring, with probability Pm, flip the bit. "
            "Ensures exploration of new areas of search space. "
            "Too high Pm → random walk. Too low Pm → stuck in local optima.\n\n"
            "Step 6 — REPLACEMENT & REPEAT:\n"
            "Form new generation from offspring. With elitism: keep best individual from old gen. "
            "Increment generation counter. If termination not met, go to Step 2."
        ),
    ]
    for item in qa_block("5 Marks Questions with Answers (300–500 words each)",
                          HexColor('#2e7d32'), q5_ga, s):
        story.append(item)

    story.append(Spacer(1,0.25*cm))

    q10_ga = [
        (
            "What is a Genetic Algorithm and why is it used? Explain the various Genetic Operations. "
            "(Asked in 2025 — 5+10=15 marks, covered here as 10M)",
            "GENETIC ALGORITHM — COMPLETE ANSWER WITH ALL OPERATIONS\n\n"
            "INTRODUCTION AND WHY GA IS USED:\n"
            "A Genetic Algorithm is a search, optimization, and machine learning technique inspired by "
            "biological evolution. Created by John Holland (1975) at University of Michigan, GA is based "
            "on Darwin's principle: individuals with higher fitness survive and reproduce more.\n\n"
            "WHY GA IS USED:\n"
            "1. No gradient needed: Unlike calculus-based optimization (gradient descent), GA works with "
            "any fitness function — even non-differentiable, noisy, or discontinuous ones.\n"
            "2. Global Search: GA maintains a POPULATION of solutions, exploring multiple areas of the "
            "search space simultaneously — less likely to get stuck in local optima.\n"
            "3. Large Search Spaces: For combinatorial problems (TSP, scheduling) with factorial search "
            "spaces, exhaustive search is impossible. GA finds near-optimal solutions efficiently.\n"
            "4. Parallelizable: All chromosomes can be evaluated in parallel.\n"
            "5. No Domain Knowledge Required: GA needs only the fitness function, not deep problem knowledge.\n\n"
            "COMPLETE GA ALGORITHM:\n"
            "1. Initialize: Random population of N chromosomes (each = encoded solution)\n"
            "2. Evaluate: Compute fitness f(i) for each chromosome\n"
            "3. Terminate?: If max generations or fitness threshold reached, return best chromosome\n"
            "4. Select: Choose parents proportional to fitness\n"
            "5. Crossover: Combine parents to produce offspring\n"
            "6. Mutate: Randomly alter offspring genes\n"
            "7. Replace: Form new population. Goto Step 2.\n\n"
            "GENETIC OPERATIONS IN DETAIL:\n\n"
            "OPERATION 1 — SELECTION:\n"
            "Purpose: Choose chromosomes as parents. Better chromosomes should be chosen more often.\n"
            "a) Roulette Wheel Selection: Assign selection probability P(i) = f(i)/Σf(j). "
            "Spin a virtual roulette wheel — higher fitness = larger slice = higher chance.\n"
            "b) Tournament Selection: Pick k random chromosomes, best among them wins.\n"
            "c) Rank Selection: Sort by fitness, assign probability based on rank not raw fitness.\n"
            "d) Elitism: Best chromosome always copied to next generation unchanged.\n\n"
            "OPERATION 2 — CROSSOVER:\n"
            "Purpose: Combine genetic material of two parents to create offspring. "
            "Applied with probability Pc (0.6 to 0.9).\n"
            "a) Single-Point: Random cut point k. Swap tails.\n"
            "   P1=101|101, P2=011|010 → C1=101010, C2=011101\n"
            "b) Two-Point: Two cut points k1,k2. Swap middle segment.\n"
            "   P1=10|110|01, P2=11|001|10 → C1=10|001|01, C2=11|110|10\n"
            "c) Uniform Crossover: For each gene, randomly decide whether to take from P1 or P2.\n"
            "d) Arithmetic Crossover (real-valued): C = α·P1 + (1−α)·P2\n\n"
            "OPERATION 3 — MUTATION:\n"
            "Purpose: Maintain diversity, avoid premature convergence, explore new solutions. "
            "Applied with very small probability Pm (0.001 to 0.01).\n"
            "a) Bit-Flip Mutation: Flip a random bit (0→1 or 1→0).\n"
            "   Before: 101101, After: 101001 (bit 4 flipped)\n"
            "b) Swap Mutation: Swap two randomly selected genes.\n"
            "c) Gaussian Mutation: Add small random Gaussian noise to real-valued gene.\n"
            "d) Inversion Mutation: Reverse a sub-sequence of genes.\n\n"
            "OPERATION 4 — REPLACEMENT:\n"
            "a) Generational: All offspring replace entire previous population.\n"
            "b) Steady-State: Only replace worst individuals with new offspring.\n"
            "c) Elitist: Keep best k individuals from parents + rest from offspring.\n\n"
            "WORKED EXAMPLE (Maximize f(x)=x², 5-bit binary):\n"
            "Initial Population: [01101=13, 11000=24, 01000=8, 10011=19]\n"
            "Fitness: [169, 576, 64, 361]\n"
            "Total Fitness: 1170\n"
            "Selection Probabilities: [0.14, 0.49, 0.05, 0.31]\n"
            "After selection, crossover and mutation → new population with higher average fitness.\n\n"
            "APPLICATIONS: Travelling Salesman, VLSI design, Neural network weight optimization, "
            "Job scheduling, Robotics, Feature selection, Bioinformatics, Game strategies.\n\n"
            "CONCLUSION: GA is a powerful, flexible, and robust optimization technique. "
            "Its ability to explore large search spaces without gradients makes it invaluable "
            "for real-world AI and engineering problems."
        ),
    ]
    for item in qa_block("10 Marks Questions with Answers (500–700 words each)",
                          HexColor('#1b5e20'), q10_ga, s):
        story.append(item)

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # TOPIC 4 ── FUZZY NEURAL NETWORKS
    # ════════════════════════════════════════════════════════════════════════
    story.append(banner("TOPIC 4 — FUZZY NEURAL NETWORKS (FNN)", C['maroon'], s))
    story.append(Spacer(1,0.3*cm))
    story.append(badge_row("Fuzzy Neural Networks","45%",C['maroon'],
        "<b>Moderate probability.</b> Not directly asked recently but is in the syllabus. "
        "Could appear as a 5-mark question or as part of a 15-mark 'write notes on' question. "
        "Know the basic concept, architecture, two types (Fuzzy-ANN and Neuro-Fuzzy), "
        "and the ANFIS model.", s))
    story.append(Spacer(1,0.4*cm))

    story.append(sec_box("4.1  What is a Fuzzy Neural Network?", s, C['maroon_bg'], C['maroon']))
    story.append(Paragraph(
        "A <b>Fuzzy Neural Network (FNN)</b> is a hybrid intelligent system that combines the "
        "<b>learning ability of Artificial Neural Networks (ANN)</b> with the "
        "<b>reasoning ability of Fuzzy Logic</b>. "
        "It overcomes the individual limitations of both:",s['body']))
    story.append(Paragraph(
        "ANN limitation: Black box — cannot explain its reasoning. "
        "Fuzzy Logic limitation: Manually designed membership functions and rules — "
        "no automatic learning from data. "
        "FNN solution: ANN learns the optimal fuzzy membership functions and rules from data — "
        "it is interpretable (fuzzy logic) AND adaptive (ANN learning).",s['note']))

    story.append(sec_box("4.2  Types of Fuzzy Neural Networks", s, C['maroon_bg'], C['maroon']))
    fnn_types = [
        ("Type 1: Fuzzy-ANN (Neural networks with fuzzy inputs)",
         "A standard ANN where inputs are fuzzy membership values instead of crisp numbers. "
         "The network receives fuzzified inputs, processes them normally, and gives a crisp output "
         "after defuzzification. The neural network is unchanged — only inputs/outputs are fuzzy."),
        ("Type 2: Neuro-Fuzzy System (Fuzzy system with ANN learning)",
         "A fuzzy inference system whose parameters (membership function shapes, rule weights) "
         "are LEARNED using neural network training (backpropagation). "
         "The network structure represents the fuzzy system; weights correspond to fuzzy parameters. "
         "Most popular: ANFIS (Adaptive Neuro-Fuzzy Inference System)."),
        ("Type 3: Fuzzy Neurons",
         "Neurons that use fuzzy aggregation instead of weighted sum. "
         "Inputs are fuzzy numbers; connections have fuzzy weights; "
         "aggregation uses fuzzy AND/OR operators (min/max) instead of multiplication/addition."),
    ]
    for tname, tdesc in fnn_types:
        story.append(Paragraph(f"<b>► {tname}:</b>", s['subsec']))
        story.append(Paragraph(tdesc, s['body']))

    story.append(sec_box("4.3  ANFIS — Adaptive Neuro-Fuzzy Inference System", s, C['maroon_bg'], C['maroon']))
    story.append(Paragraph(
        "ANFIS (proposed by Jang, 1993) is the most well-known neuro-fuzzy system. "
        "It combines a Takagi-Sugeno fuzzy inference system with a backpropagation-based learning algorithm.",s['body']))
    story.append(Paragraph("<b>ANFIS has 5 layers:</b>", s['subsec']))
    anfis_layers = [
        ("Layer 1 — Fuzzification","Each node computes the membership degree of input to fuzzy sets. "
         "Output: μ_A(x) for each input variable."),
        ("Layer 2 — Rule Strength","Each node (×) multiplies membership values from Layer 1. "
         "Computes firing strength of each rule: wi = μ_Ai(x) × μ_Bi(y)."),
        ("Layer 3 — Normalization","Each node normalizes the firing strengths: "
         "w̄i = wi / Σwj (normalized rule strengths sum to 1)."),
        ("Layer 4 — Defuzzification","Each node computes: w̄i · fi where fi = pi·x + qi·y + ri "
         "(linear parameters pi, qi, ri are learned by gradient descent)."),
        ("Layer 5 — Output","Single node that sums all Layer 4 outputs: "
         "Overall Output = Σ(w̄i · fi)"),
    ]
    for lname, ldesc in anfis_layers:
        story.append(Paragraph(f"<b>{lname}:</b> {ldesc}", s['bullet']))

    story.append(Paragraph("<b>ANFIS Learning:</b>", s['subsec']))
    story.append(Paragraph(
        "Uses a hybrid learning algorithm: "
        "Forward pass — fix antecedent parameters (Layer 1), optimize consequent parameters (Layer 4) "
        "using least squares. "
        "Backward pass — fix consequent parameters, update antecedent parameters using backpropagation. "
        "This hybrid method is faster than pure gradient descent.",s['body']))

    story.append(sec_box("4.4  Advantages & Applications of FNN", s, C['maroon_bg'], C['maroon']))
    fnn_pros = [
        "Combines interpretability of fuzzy logic with learning power of ANN.",
        "Automatically learns fuzzy membership functions from data.",
        "More interpretable than pure ANN — rules can be extracted.",
        "Handles imprecise and uncertain data naturally.",
        "Better generalization than pure fuzzy systems designed manually.",
    ]
    story.append(Paragraph("<b>ADVANTAGES:</b>", s['subsec']))
    for p in fnn_pros: story.append(Paragraph(f"✅  {p}", s['bullet']))

    fnn_apps = [
        "Pattern recognition with noisy data",
        "Medical diagnosis — symptoms are naturally fuzzy",
        "Financial time-series forecasting",
        "Robot control — smooth, interpretable control rules",
        "Speech and image recognition",
    ]
    story.append(Paragraph("<b>APPLICATIONS:</b>", s['subsec']))
    for a in fnn_apps: story.append(Paragraph(f"✓  {a}", s['bullet']))

    # FNN Questions
    story.append(Spacer(1,0.3*cm))
    story.append(banner("PRACTICE QUESTIONS & ANSWERS — TOPIC 4: FUZZY NEURAL NETWORKS", C['maroon'], s))
    story.append(Spacer(1,0.2*cm))

    q15_fnn = [
        (
            "What is a Fuzzy Neural Network? What are its advantages?",
            "A Fuzzy Neural Network (FNN) is a hybrid system combining ANN's learning ability with "
            "fuzzy logic's reasoning ability. ANN learns optimal fuzzy membership functions and rules from data. "
            "Advantages: interpretable (unlike black-box ANN), learns automatically (unlike manually designed fuzzy systems), "
            "handles uncertainty, better generalization."
        ),
        (
            "What is ANFIS? Expand the acronym and give its key feature.",
            "ANFIS stands for Adaptive Neuro-Fuzzy Inference System (Jang, 1993). "
            "It implements a Takagi-Sugeno fuzzy inference system trained using backpropagation and least squares. "
            "Key feature: A hybrid learning algorithm — forward pass uses least squares for consequent parameters; "
            "backward pass uses gradient descent for antecedent (membership function) parameters."
        ),
    ]
    for item in qa_block("1.5 Marks Questions with Answers", HexColor('#880e4f'), q15_fnn, s):
        story.append(item)

    story.append(Spacer(1,0.25*cm))

    q5_fnn = [
        (
            "Explain Fuzzy Neural Networks. What are the types and how does ANFIS work?",
            "FUZZY NEURAL NETWORKS — EXPLANATION\n\n"
            "INTRODUCTION:\n"
            "A Fuzzy Neural Network (FNN) is a hybrid intelligent system that integrates fuzzy logic and "
            "artificial neural networks to overcome their individual limitations.\n"
            "• ANN limitation: Cannot explain reasoning (black box), requires crisp inputs.\n"
            "• Fuzzy limitation: Membership functions and rules must be manually designed.\n"
            "• FNN combines: ANN's adaptive learning + Fuzzy logic's interpretability.\n\n"
            "TYPES OF FNN:\n"
            "1. Fuzzy-ANN: Standard ANN that receives fuzzified inputs (membership values) and "
            "produces defuzzified outputs. ANN structure unchanged.\n"
            "2. Neuro-Fuzzy System: A fuzzy inference system whose parameters are learned via neural "
            "network training. Most important: ANFIS.\n"
            "3. Fuzzy Neurons: Neurons using fuzzy aggregation (min/max) instead of weighted sum.\n\n"
            "ANFIS (Adaptive Neuro-Fuzzy Inference System):\n"
            "A 5-layer network implementing a Takagi-Sugeno fuzzy system:\n"
            "Layer 1 (Fuzzification): Compute μ_A(x) for each input.\n"
            "Layer 2 (Rule Firing Strength): wi = μ_A1(x) × μ_B1(y)\n"
            "Layer 3 (Normalization): w̄i = wi / Σwj\n"
            "Layer 4 (Consequent): w̄i × fi where fi = pi·x + qi·y + ri\n"
            "Layer 5 (Output): y = Σ(w̄i·fi)\n\n"
            "Learning: Hybrid algorithm — forward pass: least squares for Layer 4 params; "
            "backward pass: backprop for Layer 1 params.\n\n"
            "APPLICATIONS: Medical diagnosis, forecasting, robot control, pattern recognition.\n\n"
            "KEY ADVANTAGE: ANFIS gives a transparent fuzzy rule system that is automatically "
            "tuned to match training data — the best of both worlds."
        ),
    ]
    for item in qa_block("5 Marks Questions with Answers (300–500 words each)",
                          HexColor('#ad1457'), q5_fnn, s):
        story.append(item)

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # QUICK REVISION
    # ════════════════════════════════════════════════════════════════════════
    story.append(banner("MODULE 2 — QUICK REVISION SHEET", C['dark_navy'], s))
    story.append(Spacer(1,0.3*cm))
    story.append(info_box(
        "📌  READ THIS PAGE 1 HOUR BEFORE YOUR EXAM. All key formulas, definitions, and must-know facts.",
        s, C['yellow_bg'], C['orange']))
    story.append(Spacer(1,0.2*cm))

    rev_rows = [
        ["TOPIC","MUST KNOW"],
        ["Fuzzy Logic Intro","Zadeh 1965 | Handles vagueness | Truth between 0 and 1"],
        ["Fuzzy Set","A = {(x, μ_A(x)) | x∈X}, 0 ≤ μ_A(x) ≤ 1"],
        ["Core","Core(A) = {x | μ_A(x) = 1} — elements with FULL membership"],
        ["Height","Height(A) = max{μ_A(x)} — max membership value in the set"],
        ["α-cut","A_α = {x | μ_A(x) ≥ α}"],
        ["Fuzzy Union","μ_(A∪B)(x) = max(μ_A(x), μ_B(x))"],
        ["Fuzzy Intersection","μ_(A∩B)(x) = min(μ_A(x), μ_B(x))"],
        ["Fuzzy Complement","μ_Ā(x) = 1 − μ_A(x)"],
        ["Fuzzy Addition","A+B = (a1+b1, a2+b2, a3+b3) for triangular fuzzy numbers"],
        ["FIS Steps","Fuzzification → Rule Evaluation → Aggregation → Defuzzification"],
        ["Centroid Defuzz","x* = Σ(x · μ(x)) / Σ(μ(x))"],
        ["Prob vs Fuzzy","Probability: likelihood of event. Fuzzy: degree of membership."],
        ["Semantic Net","Directed graph | Nodes=concepts, Arcs=relationships | IS-A, HAS-A"],
        ["Partitioned Net","G-space (∀), I-space (∃) | Handles quantifier scope"],
        ["Frame","Slot-value structure | Defaults | Inheritance | Minsky 1975"],
        ["Forward Chaining","Known facts → apply rules → reach goal (data-driven)"],
        ["Backward Chaining","From goal → find supporting facts (goal-driven, used in Prolog)"],
        ["Blackboard","Blackboard + Knowledge Sources + Control Scheduler"],
        ["GA Components","Population, Fitness Function, Selection, Crossover, Mutation"],
        ["GA Steps","Init → Evaluate → Select → Crossover → Mutate → Replace → Repeat"],
        ["Roulette Selection","P(i) = f(i) / Σf(j)"],
        ["Single-Point Crossover","P1=101|101, P2=011|010 → C1=101010, C2=011101"],
        ["Mutation","Bit flip | Low probability Pm ≈ 0.001–0.01 | Maintains diversity"],
        ["FNN","ANN learning + Fuzzy Logic reasoning = Hybrid system"],
        ["ANFIS","5-layer neuro-fuzzy | Hybrid learning (LS + backprop) | Jang 1993"],
    ]
    th_r = ParagraphStyle('th_r', fontName='Helvetica-Bold', fontSize=9.5, textColor=white, alignment=TA_CENTER)
    td_r = ParagraphStyle('td_r', fontName='Helvetica', fontSize=9.5, textColor=C['dark_text'])
    td_r2 = ParagraphStyle('td_r2', fontName='Helvetica-Bold', fontSize=9.5, textColor=C['navy'])
    rev_table_data = [[Paragraph(rev_rows[0][0], th_r), Paragraph(rev_rows[0][1], th_r)]]
    row_bgs = [C['accent'],C['green_bg'],C['teal_bg'],C['orange_bg'],C['purple_bg'],C['red_bg'],
               C['yellow_bg'],C['indigo_bg'],C['brown_bg'],C['accent'],C['green_bg'],
               C['teal_bg'],C['orange_bg'],C['purple_bg'],C['red_bg'],C['yellow_bg'],
               C['indigo_bg'],C['brown_bg'],C['accent'],C['green_bg'],C['teal_bg'],
               C['orange_bg'],C['purple_bg'],C['red_bg'],C['yellow_bg']]
    for row in rev_rows[1:]:
        rev_table_data.append([Paragraph(row[0], td_r2), Paragraph(row[1], td_r)])
    rev_t = Table(rev_table_data, colWidths=[5.5*cm, W-8.3*cm])
    style_cmds = [
        ('BACKGROUND',(0,0),(-1,0),C['dark_navy']),
        ('GRID',(0,0),(-1,-1),0.5,HexColor('#bdbdbd')),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),8),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ]
    for i, bg in enumerate(row_bgs, 1):
        if i < len(rev_table_data):
            style_cmds.append(('BACKGROUND',(0,i),(-1,i),bg))
    rev_t.setStyle(TableStyle(style_cmds))
    story.append(rev_t)
    story.append(Spacer(1,0.3*cm))

    story.append(info_box(
        "🎯  MOST LIKELY EXAM QUESTIONS MODULE 2:\n"
        "(1) Why fuzzy introduced + design fuzzy set for human age — 5 marks  "
        "(2) Crisp vs fuzzy logic — 1.5 marks  "
        "(3) Probability vs fuzzy logic — 5 marks  "
        "(4) Genetic Algorithm steps + operations — 10 marks  "
        "(5) Applications of GA — 1.5 marks  "
        "(6) KR techniques with examples — 10 marks  "
        "(7) Blackboard architecture — 5 marks  "
        "(8) Semantic nets and frames (short notes) — 5+5 marks",
        s, C['green_bg'], C['teal']))

    return story


# ── BUILD ─────────────────────────────────────────────────────────────────────
def main():
    out = "/mnt/user-data/outputs/IS_Module2_Complete_Notes.pdf"
    s = S()
    doc = SimpleDocTemplate(out, pagesize=A4,
        rightMargin=1.4*cm, leftMargin=1.4*cm,
        topMargin=1.4*cm, bottomMargin=1.4*cm,
        title="Intelligent Systems — Module 2 Complete Notes",
        author="PCC-CS-601 Study Material")

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(HexColor('#9e9e9e'))
        canvas.drawString(1.4*cm, 0.7*cm, "IS Module 2 | PCC-CS-601 | YMCA University")
        canvas.drawRightString(W-1.4*cm, 0.7*cm, f"Page {doc.page}")
        canvas.restoreState()

    doc.build(build(s), onFirstPage=footer, onLaterPages=footer)
    print(f"Done: {out}")

if __name__ == "__main__":
    main()