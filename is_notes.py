from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# ── Output path ──────────────────────────────────────────────────────────────
import os
OUTPUT = os.path.join(os.getcwd(), "DataMining_PEC_CS_D601_TopicProbability.pdf")

# ── Colour palette ────────────────────────────────────────────────────────────
RED      = colors.HexColor("#C0392B")
ORANGE   = colors.HexColor("#E67E22")
YELLOW   = colors.HexColor("#F1C40F")
GREEN    = colors.HexColor("#27AE60")
DARK     = colors.HexColor("#1A1A2E")
ACCENT   = colors.HexColor("#16213E")
LIGHT_BG = colors.HexColor("#F8F9FA")
RED_BG   = colors.HexColor("#FDEDEC")
ORANGE_BG= colors.HexColor("#FEF5E7")
YELLOW_BG= colors.HexColor("#FEFDE7")
GREEN_BG = colors.HexColor("#EAFAF1")
HEADER_BG= colors.HexColor("#1A1A2E")
WHITE    = colors.white

# ── Document ──────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=1.8*cm, rightMargin=1.8*cm,
    topMargin=1.8*cm, bottomMargin=1.8*cm
)
W = A4[0] - 3.6*cm   # usable width

styles = getSampleStyleSheet()
story  = []

# ── Custom styles ─────────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

title_style = S("Title2",
    fontName="Helvetica-Bold", fontSize=18,
    textColor=WHITE, alignment=TA_CENTER,
    spaceAfter=4, leading=22)

sub_style = S("Sub",
    fontName="Helvetica", fontSize=9,
    textColor=colors.HexColor("#BDC3C7"), alignment=TA_CENTER,
    spaceAfter=2, leading=13)

section_style = S("Section",
    fontName="Helvetica-Bold", fontSize=11,
    textColor=WHITE, spaceAfter=4, leading=14)

body_style = S("Body2",
    fontName="Helvetica", fontSize=8.5,
    textColor=DARK, spaceAfter=2, leading=13)

note_style = S("Note",
    fontName="Helvetica-Oblique", fontSize=8,
    textColor=colors.HexColor("#555555"), leading=12)

card_style = S("Card",
    fontName="Helvetica-Bold", fontSize=9,
    textColor=DARK, leading=13)

code_style = S("Code",
    fontName="Courier", fontSize=8,
    textColor=DARK, leading=12, spaceAfter=2)

# ── Helper: coloured section header ──────────────────────────────────────────
def section_header(text, bg=ACCENT):
    data = [[Paragraph(text, section_style)]]
    t = Table(data, colWidths=[W])
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,-1), bg),
        ("TOPPADDING",  (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("RIGHTPADDING",(0,0), (-1,-1), 10),
        ("ROUNDEDCORNERS", [4]),
    ]))
    return t

# ── Helper: topic table ───────────────────────────────────────────────────────
def topic_table(rows, header_bg, row_bg, header_color=WHITE):
    # rows = list of (no, topic, module, notes)
    col_w = [0.08*W, 0.40*W, 0.10*W, 0.42*W]
    hdr = [
        Paragraph("<b>#</b>",    ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=8.5, textColor=header_color, alignment=TA_CENTER)),
        Paragraph("<b>Topic</b>",ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=8.5, textColor=header_color)),
        Paragraph("<b>Mod</b>",  ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=8.5, textColor=header_color, alignment=TA_CENTER)),
        Paragraph("<b>Remarks</b>",ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=8.5, textColor=header_color)),
    ]
    table_data = [hdr]
    for i, (no, topic, mod, notes) in enumerate(rows):
        bg = row_bg if i % 2 == 0 else WHITE
        table_data.append([
            Paragraph(str(no), ParagraphStyle("c", fontName="Helvetica-Bold", fontSize=8.5, textColor=DARK, alignment=TA_CENTER)),
            Paragraph(topic,   ParagraphStyle("b", fontName="Helvetica-Bold", fontSize=8.5, textColor=DARK, leading=12)),
            Paragraph(mod,     ParagraphStyle("c", fontName="Helvetica", fontSize=8.5, textColor=DARK, alignment=TA_CENTER)),
            Paragraph(notes,   ParagraphStyle("n", fontName="Helvetica", fontSize=7.8, textColor=colors.HexColor("#444444"), leading=11)),
        ])
    t = Table(table_data, colWidths=col_w, repeatRows=1)
    ts = [
        ("BACKGROUND",   (0,0), (-1,0), header_bg),
        ("TEXTCOLOR",    (0,0), (-1,0), header_color),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("GRID",         (0,0), (-1,-1), 0.4, colors.HexColor("#DDDDDD")),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [row_bg, WHITE]),
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
    ]
    t.setStyle(TableStyle(ts))
    return t

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — HEADER
# ═══════════════════════════════════════════════════════════════════════════════
header_data = [[
    Paragraph("DATA MINING", title_style),
    Paragraph("PEC-CS-D-601  |  B.Tech VI Semester", sub_style),
    Paragraph("TOPIC PROBABILITY GUIDE — FINAL EXAM", sub_style),
    Paragraph("Based on PYQ Analysis: May 2024 &amp; May 2025", sub_style),
]]
header_t = Table([[
    Paragraph("DATA MINING", title_style)],[
    Paragraph("PEC-CS-D-601  |  B.Tech VI Semester", sub_style)],[
    Paragraph("TOPIC PROBABILITY GUIDE — FINAL EXAM", sub_style)],[
    Paragraph("Based on PYQ Analysis: May 2024 &amp; May 2025  |  Max Marks: 75", sub_style)],
], colWidths=[W])
header_t.setStyle(TableStyle([
    ("BACKGROUND",  (0,0), (-1,-1), HEADER_BG),
    ("TOPPADDING",  (0,0), (-1,-1), 6),
    ("BOTTOMPADDING",(0,0),(-1,-1), 4),
    ("LEFTPADDING", (0,0), (-1,-1), 16),
    ("RIGHTPADDING",(0,0), (-1,-1), 16),
]))
story.append(header_t)
story.append(Spacer(1, 10))

# Legend row
legend_data = [[
    Paragraph("🔴  GUARANTEED", ParagraphStyle("l", fontName="Helvetica-Bold", fontSize=8, textColor=RED, alignment=TA_CENTER)),
    Paragraph("🟠  VERY HIGH",  ParagraphStyle("l", fontName="Helvetica-Bold", fontSize=8, textColor=ORANGE, alignment=TA_CENTER)),
    Paragraph("🟡  MODERATE",   ParagraphStyle("l", fontName="Helvetica-Bold", fontSize=8, textColor=colors.HexColor("#B7950B"), alignment=TA_CENTER)),
    Paragraph("🟢  LOWER",      ParagraphStyle("l", fontName="Helvetica-Bold", fontSize=8, textColor=GREEN, alignment=TA_CENTER)),
]]
lt = Table(legend_data, colWidths=[W/4]*4)
lt.setStyle(TableStyle([
    ("BACKGROUND",  (0,0),(0,0), RED_BG),
    ("BACKGROUND",  (1,0),(1,0), ORANGE_BG),
    ("BACKGROUND",  (2,0),(2,0), YELLOW_BG),
    ("BACKGROUND",  (3,0),(3,0), GREEN_BG),
    ("TOPPADDING",  (0,0),(-1,-1), 6),
    ("BOTTOMPADDING",(0,0),(-1,-1), 6),
    ("BOX",         (0,0),(-1,-1), 0.5, colors.HexColor("#CCCCCC")),
    ("INNERGRID",   (0,0),(-1,-1), 0.5, colors.HexColor("#CCCCCC")),
]))
story.append(lt)
story.append(Spacer(1, 12))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — GUARANTEED (RED)
# ═══════════════════════════════════════════════════════════════════════════════
story.append(section_header("🔴  GUARANTEED / ~100% Probability  —  Appeared in BOTH 2024 & 2025 Papers", RED))
story.append(Spacer(1, 4))

guaranteed = [
    ("1", "Association Rule Mining<br/>(Apriori / FP-Growth) — Build FP-Tree, Conditional Pattern Base, find frequent itemsets", "M2", "Part B in BOTH years; always a 10-mark numerical question. Must practice tree construction."),
    ("2", "Decision Tree Induction + Information Gain<br/>— Calculate Info Gain for Weather/Temperature style dataset", "M3", "Part B both years; always paired with a given dataset. Most numerical-heavy question."),
    ("3", "K-Means Clustering<br/>— Execute 2 iterations, update centroids, assign points to clusters", "M2", "Part B both years; always a numerical problem with given coordinates."),
    ("4", "Hierarchical Clustering<br/>— Types, Single / Complete / Average Linkage, Dendrogram", "M2", "Part A + Part B both years; theory + types expected together."),
    ("5", "Data Warehouse Architecture + Schemas<br/>— Three-Tier Architecture, Star / Snowflake / Fact Constellation", "M1", "Part B both years; schema question includes example scenario."),
    ("6", "Euclidean vs Manhattan Distance / Distance Matrix<br/>— Numerical problem on given 1-D or 2-D points", "M2", "Part A + Part B both years; formula + calculation mandatory."),
    ("7", "Clustering Feature (CF)<br/>— Calculate CF triple (N, LS, SS) for given 2D data points", "M2", "Part A in BOTH 2024 & 2025 papers without fail."),
    ("8", "Time Series Analysis — Four Components<br/>Trend / Cyclic / Seasonal / Irregular + Trend Analysis", "M4", "Part A + Part B both years; component definitions + examples expected."),
    ("9", "Web Mining<br/>— Definition, three categories (Content / Structure / Usage), importance", "M5", "Part A + Part B both years; always asks all three categories with examples."),
    ("10","Sequential Pattern Mining<br/>— GSP approach with transaction dataset; concepts", "M2", "Part B both years; often given a database with min support to find subsequences."),
    ("11","Support and Confidence<br/>— Definitions, formulas, importance of both measures", "M2", "Part A in both years without exception."),
    ("12","Classification vs Clustering<br/>— Differentiate clearly with examples", "M2/M3", "Part A both years; standard short-answer comparison question."),
]
story.append(topic_table(guaranteed, RED, RED_BG))
story.append(Spacer(1, 12))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — VERY HIGH (ORANGE)
# ═══════════════════════════════════════════════════════════════════════════════
story.append(section_header("🟠  Very High Probability  —  Appeared in One Year's Part B or Both Part A's", ORANGE))
story.append(Spacer(1, 4))

very_high = [
    ("13","Backpropagation in Neural Networks<br/>— Forward propagation, loss calculation, backward propagation with full math", "M3", "Part B 2025; mathematical formulation expected. Very likely to return."),
    ("14","SVM — Best Fit Hyperplane / MMH<br/>— Numerical with positive and negative labelled points", "M3", "Part B 2024; find separating hyperplane from given labelled dataset."),
    ("15","Bayesian Classification<br/>— Prior, Conditional, Posterior probability; Naive Bayes calculation", "M3", "Part A 2025; full Naive Bayes worked example likely in Part B."),
    ("16","OLAP Operations + OLAP vs OLTP<br/>— Roll-Up, Drill-Down, Slice, Dice, Pivot with examples", "M1", "Part B 2024; comparison table + OLAP operation definitions."),
    ("17","ROLAP, MOLAP, HOLAP<br/>— Differentiate all three server types", "M1", "Part B 2025; short-answer comparison question."),
    ("18","Data Warehousing Features (SITN)<br/>— Difference from traditional/operational data processing", "M1", "Part A both years; Subject-Oriented, Integrated, Time-Variant, Non-Volatile."),
    ("19","Supervised vs Unsupervised Learning<br/>— Difference in context of data mining", "M2/M3","Part A 2025; concise definition + example for each."),
    ("20","Social Network Analysis<br/>— Characteristics: Densification, Shrinking Diameter, Heavy-tailed Degrees", "M5", "Part B 2025 short note; Forest Fire model may be asked."),
    ("21","Class Imbalance Problem<br/>— Description, SMOTE, oversampling, undersampling, cost-sensitive", "M5", "Part B 2025; solutions are most important — know SMOTE well."),
    ("22","Concept Hierarchy<br/>— Definition, need, example (city → province → country)", "M1", "Part A 2025; 1.5-mark short answer."),
    ("23","Genetic Algorithms<br/>— Crossover and Mutation process with encoding example", "M3", "Part A 2025; bit-string encoding + operators."),
    ("24","Data Streams — Properties and Challenges<br/>— Three properties, challenges in mining", "M4", "Part A both years; list 3 properties + mining challenges."),
]
story.append(topic_table(very_high, ORANGE, ORANGE_BG))
story.append(Spacer(1, 12))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — MODERATE (YELLOW)
# ═══════════════════════════════════════════════════════════════════════════════
story.append(section_header("🟡  Moderate Probability  —  Syllabus Topics Not Yet Tested in Part B", colors.HexColor("#D4AC0D")))
story.append(Spacer(1, 4))

moderate = [
    ("25","KDD Process<br/>— All 7 steps: Clean → Integrate → Select → Transform → Mine → Evaluate → Present", "M1", "Core foundational topic; short answer in Part A very likely."),
    ("26","Rule-Based Classification<br/>— IF-THEN rules, sequential covering algorithm, coverage & accuracy", "M3", "Syllabus topic not yet in Part B; overdue to appear."),
    ("27","Linear and Non-Linear Regression<br/>— Least squares formula, polynomial regression, variable transformation", "M3", "Prediction half of M3 underrepresented in PYQs; prepare formulas."),
    ("28","BIRCH Clustering<br/>— CF-tree concept, Phase 1 & Phase 2, advantages", "M2", "Part of hierarchical methods; usually tested as a sub-part."),
    ("29","Bitmap Indexing in Data Warehouse", "M1", "Part A 2025; short definition with working."),
    ("30","Outlier Detection<br/>— Definition, types, methods of detection", "M2", "Part A 2024; 'Define Outlier' style short answer."),
    ("31","Missing Value Imputation<br/>— Methods: mean substitution, most probable value, etc.", "M1", "Part A 2024; explain any two methods."),
    ("32","Similarity Search in Time Series<br/>— DFT, subsequence vs whole sequence matching", "M4", "Syllabus mandates it; short answer expected."),
    ("33","Histogram Sampling Method<br/>— Basic idea, V-optimal histograms", "M4", "Part A 2024; concept-level question."),
    ("34","k-Medoids (PAM)<br/>— Difference from k-Means, medoid concept, robustness to outliers", "M2", "Common comparison question; appears alongside k-Means."),
    ("35","Stream Data Processing Methods<br/>— Reservoir sampling, sliding window, sketches, synopsis structures", "M4", "Syllabus mandates all; not yet in Part B but expected soon."),
]
story.append(topic_table(moderate, colors.HexColor("#B7950B"), YELLOW_BG))
story.append(Spacer(1, 12))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — LOWER (GREEN)
# ═══════════════════════════════════════════════════════════════════════════════
story.append(section_header("🟢  Lower Probability  —  Syllabus-Listed but Not Yet Appeared", GREEN))
story.append(Spacer(1, 4))

lower = [
    ("36","Web Page Link Structure Mining<br/>— HITS algorithm, PageRank concept, hub & authority", "M5", "Mentioned in syllabus; short note possible in Part B."),
    ("37","Graph Mining<br/>— Frequent subgraph discovery, gSpan algorithm overview", "M5", "Advanced topic; 5-mark short note most likely."),
    ("38","Lossy Counting Algorithm<br/>— Frequent pattern mining in streams, error bound ε", "M4", "Deep stream topic; short definition or algorithm steps possible."),
    ("39","CVFDT / Hoeffding Tree<br/>— Concept drift handling, sliding window, alternate subtree", "M4", "Concept drift is key; short note likely if stream classification asked."),
    ("40","Distributed Data Mining & Privacy<br/>— Secure Multiparty Computation, Data Obscuration, OECD principles", "M5", "Recent trends question; 5-mark short note."),
    ("41","Periodicity Analysis<br/>— Full vs partial periodic patterns, cyclic association rules", "M4", "Syllabus topic; short note possible; rarely tested in PYQs."),
    ("42","CluStream<br/>— Microcluster representation, on-line vs off-line phases", "M4", "Advanced; concept-level question only if stream clustering is asked."),
    ("43","Web Usage Mining (Weblog Mining)<br/>— 3 steps: preprocessing, OLAP, mining; applications", "M5", "Sub-part of web mining; may appear if full web mining question asked."),
    ("44","Classifier Accuracy & Evaluation Parameters<br/>— Accuracy, speed, robustness, scalability, interpretability", "M3", "Part A 2024; 1.5-mark short answer style."),
]
story.append(topic_table(lower, GREEN, GREEN_BG))
story.append(Spacer(1, 14))

# ═══════════════════════════════════════════════════════════════════════════════
# QUICK SUMMARY CARD
# ═══════════════════════════════════════════════════════════════════════════════
story.append(section_header("📌  QUICK REVISION SUMMARY CARD", HEADER_BG))
story.append(Spacer(1, 6))

card_content = [
    [
        Paragraph("🔴  MUST PREPARE FIRST (No compromise)", ParagraphStyle("ch", fontName="Helvetica-Bold", fontSize=9, textColor=RED)),
        Paragraph("Estimated Part B weightage: ~60 marks", ParagraphStyle("cw", fontName="Helvetica", fontSize=8, textColor=colors.HexColor("#777777"), alignment=TA_CENTER)),
    ],
    [
        Paragraph(
            "FP-Growth Tree Construction  •  Decision Tree + Info Gain Calculation  •  K-Means (2 iterations)  •  "
            "Hierarchical Clustering (linkage types)  •  Data Warehouse 3-Tier + Schemas  •  "
            "Time Series 4 Components  •  Sequential Patterns / GSP  •  "
            "Association Rules (Support + Confidence)  •  Clustering Feature CF",
            ParagraphStyle("cb", fontName="Helvetica", fontSize=8.5, textColor=DARK, leading=14)),
        Paragraph("", body_style),
    ],
]
card1 = Table(card_content, colWidths=[0.72*W, 0.28*W])
card1.setStyle(TableStyle([
    ("BACKGROUND",  (0,0),(-1,-1), RED_BG),
    ("TOPPADDING",  (0,0),(-1,-1), 8),
    ("BOTTOMPADDING",(0,0),(-1,-1), 8),
    ("LEFTPADDING", (0,0),(-1,-1), 10),
    ("RIGHTPADDING",(0,0),(-1,-1), 10),
    ("VALIGN",      (0,0),(-1,-1), "TOP"),
    ("BOX",         (0,0),(-1,-1), 1, RED),
]))
story.append(card1)
story.append(Spacer(1, 6))

card2_content = [
    [Paragraph("🟠  PREPARE THOROUGHLY", ParagraphStyle("ch", fontName="Helvetica-Bold", fontSize=9, textColor=ORANGE))],
    [Paragraph(
        "Backpropagation (math)  •  SVM Hyperplane (numerical)  •  Naive Bayes  •  "
        "OLAP Operations  •  ROLAP/MOLAP/HOLAP  •  Social Network Analysis  •  "
        "Class Imbalance + SMOTE  •  Genetic Algorithms (crossover + mutation)",
        ParagraphStyle("cb", fontName="Helvetica", fontSize=8.5, textColor=DARK, leading=14))],
]
card2 = Table(card2_content, colWidths=[W])
card2.setStyle(TableStyle([
    ("BACKGROUND",  (0,0),(-1,-1), ORANGE_BG),
    ("TOPPADDING",  (0,0),(-1,-1), 7),
    ("BOTTOMPADDING",(0,0),(-1,-1), 7),
    ("LEFTPADDING", (0,0),(-1,-1), 10),
    ("RIGHTPADDING",(0,0),(-1,-1), 10),
    ("BOX",         (0,0),(-1,-1), 1, ORANGE),
]))
story.append(card2)
story.append(Spacer(1, 6))

card3_content = [
    [
        Paragraph("🟡  READ ONCE — short notes ready", ParagraphStyle("ch", fontName="Helvetica-Bold", fontSize=9, textColor=colors.HexColor("#B7950B"))),
        Paragraph("🟢  SKIM IF TIME PERMITS", ParagraphStyle("ch2", fontName="Helvetica-Bold", fontSize=9, textColor=GREEN)),
    ],
    [
        Paragraph("KDD 7 Steps  •  Rule-Based Classification  •  Linear & Polynomial Regression  •  BIRCH CF-tree  •  Similarity Search / DFT  •  Stream Methodologies",
            ParagraphStyle("cb", fontName="Helvetica", fontSize=8.3, textColor=DARK, leading=13)),
        Paragraph("Graph Mining  •  Distributed Mining  •  CluStream  •  Periodicity Analysis  •  Web Link Structure / HITS",
            ParagraphStyle("cb", fontName="Helvetica", fontSize=8.3, textColor=DARK, leading=13)),
    ],
]
card3 = Table(card3_content, colWidths=[W*0.5, W*0.5])
card3.setStyle(TableStyle([
    ("BACKGROUND",  (0,0),(0,-1), YELLOW_BG),
    ("BACKGROUND",  (1,0),(1,-1), GREEN_BG),
    ("TOPPADDING",  (0,0),(-1,-1), 7),
    ("BOTTOMPADDING",(0,0),(-1,-1), 7),
    ("LEFTPADDING", (0,0),(-1,-1), 10),
    ("RIGHTPADDING",(0,0),(-1,-1), 10),
    ("VALIGN",      (0,0),(-1,-1), "TOP"),
    ("BOX",         (0,0),(0,-1), 1, colors.HexColor("#D4AC0D")),
    ("BOX",         (1,0),(1,-1), 1, GREEN),
]))
story.append(card3)
story.append(Spacer(1, 12))

# ── Pro Tips ──────────────────────────────────────────────────────────────────
story.append(HRFlowable(width=W, thickness=1, color=colors.HexColor("#CCCCCC")))
story.append(Spacer(1, 6))

tip_data = [
    [Paragraph("<b>💡 PRO TIPS FOR EXAM DAY</b>", ParagraphStyle("pt", fontName="Helvetica-Bold", fontSize=9.5, textColor=ACCENT))],
    [Paragraph(
        "<b>Numerical problems always tested:</b> FP-Tree construction, K-Means (2 iterations), "
        "Information Gain calculation, Clustering Feature (N, LS, SS), Distance Matrix generation. "
        "Practice these with the EXACT datasets from both PYQs — similar datasets reappear.<br/><br/>"
        "<b>Part-A strategy:</b> All 10 questions are compulsory (1.5 marks each = 15 marks). "
        "Topics 1–12 (Guaranteed) almost always have at least 4–5 Part A sub-questions. "
        "Prepare one-paragraph answers for every topic in the Guaranteed list.<br/><br/>"
        "<b>Part-B strategy:</b> Answer 4 of 6 questions (15 marks each = 60 marks). "
        "Choose questions from Guaranteed + Very High probability topics. Always attempt the "
        "FP-Growth question, Decision Tree question, and K-Means question — they repeat every year.",
        ParagraphStyle("tb", fontName="Helvetica", fontSize=8.5, textColor=DARK, leading=14))],
]
tip_t = Table(tip_data, colWidths=[W])
tip_t.setStyle(TableStyle([
    ("BACKGROUND",  (0,0),(-1,-1), colors.HexColor("#EBF5FB")),
    ("TOPPADDING",  (0,0),(-1,-1), 8),
    ("BOTTOMPADDING",(0,0),(-1,-1), 8),
    ("LEFTPADDING", (0,0),(-1,-1), 12),
    ("RIGHTPADDING",(0,0),(-1,-1), 12),
    ("BOX",         (0,0),(-1,-1), 1, colors.HexColor("#2E86C1")),
]))
story.append(tip_t)
story.append(Spacer(1, 10))

# ── Footer ────────────────────────────────────────────────────────────────────
footer_data = [[
    Paragraph(
        "Data Mining (PEC-CS-D-601)  |  B.Tech VI Semester  |  "
        "PYQ Sources: May 2024 (Sr. No. 015605) &amp; May 2025 (Sr. No. 003603)  |  Max Marks: 75",
        ParagraphStyle("f", fontName="Helvetica", fontSize=7.5,
                       textColor=colors.HexColor("#AAAAAA"), alignment=TA_CENTER))
]]
ft = Table(footer_data, colWidths=[W])
ft.setStyle(TableStyle([
    ("TOPPADDING",  (0,0),(-1,-1), 6),
    ("BOTTOMPADDING",(0,0),(-1,-1), 6),
    ("LINEABOVE",   (0,0),(-1,0), 0.5, colors.HexColor("#CCCCCC")),
]))
story.append(ft)

# ── Build ─────────────────────────────────────────────────────────────────────
doc.build(story)
print("PDF created:", OUTPUT)