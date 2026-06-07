from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors

# ── colour palette ──────────────────────────────────────────────
SAFFRON      = HexColor("#FF6B00")
DARK_SAFFRON = HexColor("#CC5500")
GOLD         = HexColor("#FFD700")
DARK_GOLD    = HexColor("#B8860B")
DEEP_BLUE    = HexColor("#1A237E")
LIGHT_BLUE   = HexColor("#E8EAF6")
LIGHT_ORANGE = HexColor("#FFF3E0")
LIGHT_GREEN  = HexColor("#E8F5E9")
LIGHT_RED    = HexColor("#FFEBEE")
LIGHT_PURPLE = HexColor("#F3E5F5")
CREAM        = HexColor("#FFFDE7")
DARK_GREEN   = HexColor("#1B5E20")
MAROON       = HexColor("#880E4F")
TEAL         = HexColor("#004D40")
GRAY_BG      = HexColor("#F5F5F5")
DARK_GRAY    = HexColor("#424242")
INDIGO       = HexColor("#283593")
CYAN_DARK    = HexColor("#006064")
CYAN_LIGHT   = HexColor("#E0F7FA")
PURPLE_DARK  = HexColor("#4A148C")
PURPLE_LIGHT = HexColor("#EDE7F6")

WIDTH, HEIGHT = A4

def build_styles():
    def ps(name, **kw):
        return ParagraphStyle(name, **kw)
    return {
        "cover_title": ps("cover_title", fontName="Helvetica-Bold", fontSize=26,
            textColor=white, alignment=TA_CENTER, spaceAfter=8, leading=32),
        "cover_sub": ps("cover_sub", fontName="Helvetica-Bold", fontSize=13,
            textColor=GOLD, alignment=TA_CENTER, spaceAfter=6),
        "cover_info": ps("cover_info", fontName="Helvetica", fontSize=11,
            textColor=white, alignment=TA_CENTER, spaceAfter=4),
        "module_title": ps("module_title", fontName="Helvetica-Bold", fontSize=20,
            textColor=white, alignment=TA_CENTER, spaceAfter=4, leading=26),
        "topic_header": ps("topic_header", fontName="Helvetica-Bold", fontSize=13,
            textColor=white, alignment=TA_LEFT, spaceAfter=2, leading=17),
        "subtopic": ps("subtopic", fontName="Helvetica-Bold", fontSize=12,
            textColor=DEEP_BLUE, alignment=TA_LEFT, spaceBefore=8, spaceAfter=4, leading=16),
        "body": ps("body", fontName="Helvetica", fontSize=10.5,
            textColor=DARK_GRAY, alignment=TA_JUSTIFY, spaceBefore=3, spaceAfter=3, leading=16),
        "bullet": ps("bullet", fontName="Helvetica", fontSize=10.5,
            textColor=DARK_GRAY, alignment=TA_LEFT,
            leftIndent=16, firstLineIndent=-10, spaceBefore=2, spaceAfter=2, leading=15),
        "bold_bullet": ps("bold_bullet", fontName="Helvetica-Bold", fontSize=10.5,
            textColor=DARK_GRAY, alignment=TA_LEFT,
            leftIndent=16, firstLineIndent=-10, spaceBefore=2, spaceAfter=2, leading=15),
        "highlight_box": ps("highlight_box", fontName="Helvetica", fontSize=10.5,
            textColor=DARK_GRAY, alignment=TA_JUSTIFY,
            leftIndent=8, rightIndent=8, spaceBefore=2, spaceAfter=2, leading=15),
        "verse": ps("verse", fontName="Helvetica-Oblique", fontSize=10,
            textColor=TEAL, alignment=TA_CENTER, spaceBefore=2, spaceAfter=2, leading=14),
        "exam_q": ps("exam_q", fontName="Helvetica-Bold", fontSize=10.5,
            textColor=MAROON, alignment=TA_LEFT, spaceBefore=5, spaceAfter=2, leading=14),
        "exam_a": ps("exam_a", fontName="Helvetica", fontSize=10,
            textColor=DARK_GRAY, alignment=TA_JUSTIFY,
            leftIndent=12, spaceBefore=2, spaceAfter=4, leading=14),
        "section_label": ps("section_label", fontName="Helvetica-Bold", fontSize=11,
            textColor=DEEP_BLUE, alignment=TA_LEFT, spaceBefore=6, spaceAfter=2),
        "table_head": ps("table_head", fontName="Helvetica-Bold", fontSize=10,
            textColor=white, alignment=TA_CENTER),
        "table_cell": ps("table_cell", fontName="Helvetica", fontSize=9.5,
            textColor=DARK_GRAY, alignment=TA_LEFT, leading=13),
        "note": ps("note", fontName="Helvetica-Oblique", fontSize=9.5,
            textColor=MAROON, alignment=TA_LEFT, spaceBefore=2, spaceAfter=2, leading=13),
        "percent_badge": ps("percent_badge", fontName="Helvetica-Bold", fontSize=10,
            textColor=DARK_GREEN, alignment=TA_CENTER),
    }

# ── helpers ─────────────────────────────────────────────────────

def colored_box(items, bg=LIGHT_ORANGE, border=SAFFRON):
    data = [[i] for i in items]
    t = Table(data, colWidths=[16.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), bg),
        ("BOX",           (0,0),(-1,-1), 1.2, border),
        ("TOPPADDING",    (0,0),(-1,-1), 7),
        ("BOTTOMPADDING", (0,0),(-1,-1), 7),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
        ("RIGHTPADDING",  (0,0),(-1,-1), 10),
    ]))
    return t

def header_bar(text, styles, bg=SAFFRON):
    data = [[Paragraph(text, styles["topic_header"])]]
    t = Table(data, colWidths=[16.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), bg),
        ("LEFTPADDING",   (0,0),(-1,-1), 12),
        ("RIGHTPADDING",  (0,0),(-1,-1), 12),
        ("TOPPADDING",    (0,0),(-1,-1), 9),
        ("BOTTOMPADDING", (0,0),(-1,-1), 9),
    ]))
    return t

def prob_badge(topic, pct, styles):
    color = DARK_GREEN if pct >= 70 else (DARK_SAFFRON if pct >= 40 else MAROON)
    label = "VERY HIGH" if pct >= 85 else ("HIGH" if pct >= 70 else ("MEDIUM" if pct >= 40 else "LOW"))
    emoji = "🔥" if pct >= 85 else ("⚡" if pct >= 70 else "📌")
    data = [[
        Paragraph(f"<b>{topic}</b>", styles["body"]),
        Paragraph(f"<b>{emoji} {pct}% — {label}</b>",
                  ParagraphStyle("pb", fontName="Helvetica-Bold", fontSize=10,
                                 textColor=color, alignment=TA_CENTER)),
    ]]
    t = Table(data, colWidths=[12*cm, 4.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), GRAY_BG),
        ("BOX",           (0,0),(-1,-1), 0.8, HexColor("#BDBDBD")),
        ("LINEAFTER",     (0,0),(0,-1),  0.8, HexColor("#BDBDBD")),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("RIGHTPADDING",  (0,0),(-1,-1), 8),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ]))
    return t

def two_col_box(left_items, right_items, left_bg, right_bg, left_border, right_border):
    """Two side-by-side colored boxes."""
    def make_inner(items, bg, border):
        inner_data = [[i] for i in items]
        t = Table(inner_data, colWidths=[7.8*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), bg),
            ("BOX",           (0,0),(-1,-1), 1, border),
            ("TOPPADDING",    (0,0),(-1,-1), 7),
            ("BOTTOMPADDING", (0,0),(-1,-1), 7),
            ("LEFTPADDING",   (0,0),(-1,-1), 8),
            ("RIGHTPADDING",  (0,0),(-1,-1), 8),
        ]))
        return t
    row = [[make_inner(left_items, left_bg, left_border),
            make_inner(right_items, right_bg, right_border)]]
    outer = Table(row, colWidths=[8.1*cm, 8.1*cm], hAlign="LEFT")
    outer.setStyle(TableStyle([
        ("VALIGN",       (0,0),(-1,-1), "TOP"),
        ("LEFTPADDING",  (0,0),(-1,-1), 0),
        ("RIGHTPADDING", (0,0),(-1,-1), 3),
        ("TOPPADDING",   (0,0),(-1,-1), 0),
        ("BOTTOMPADDING",(0,0),(-1,-1), 0),
    ]))
    return outer

def exam_box_split(q_text, marks, *answer_boxes_data, styles=None):
    """Question label + multiple answer boxes (avoids overflow)."""
    S = styles
    result = []
    result.append(colored_box([
        Paragraph(f"Q: {q_text}  <font color='#880E4F'>[{marks}]</font>", S["exam_q"]),
    ], GRAY_BG, INDIGO))
    result.append(Spacer(1, 3))
    for (label, text, bg, border) in answer_boxes_data:
        result.append(colored_box([
            Paragraph(f"<b>{label}</b>", S["section_label"]),
            Paragraph(text, S["exam_a"]),
        ], bg, border))
        result.append(Spacer(1, 3))
    return result

def divider(color=SAFFRON):
    return HRFlowable(width="100%", thickness=1.5, color=color, spaceAfter=6, spaceBefore=6)

# ════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ════════════════════════════════════════════════════════════════

def build_content(styles):
    S = styles
    story = []

    # ── COVER ────────────────────────────────────────────────────
    story.append(Spacer(1, 1*cm))
    cover_rows = [
        [Paragraph("📖  MESSAGE OF BHAGAVAD GITA", S["cover_title"])],
        [Paragraph("CODE: AC-02-23  |  B.Tech / M.Tech  |  Theory Exam: 75 Marks", S["cover_sub"])],
        [Paragraph("MODULE 2  —  COMPREHENSIVE EXAM NOTES", S["cover_sub"])],
        [Paragraph("Unit II :  Karma Yoga  ·  Living in the Present  ·  Nishkama Karma", S["cover_info"])],
        [Paragraph("Swadharma  ·  Dhyana Yoga  ·  Quantity/Quality/Direction of Thoughts", S["cover_info"])],
        [Paragraph("Reaching Inner Silence", S["cover_info"])],
        [Paragraph("✦  Deep Explanations  ✦  Exam % Probability  ✦  All Q&A  ✦  Concept Maps  ✦", S["cover_info"])],
    ]
    ct = Table(cover_rows, colWidths=[16.5*cm])
    ct.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), DARK_SAFFRON),
        ("TOPPADDING",    (0,0),(-1,-1), 12),
        ("BOTTOMPADDING", (0,0),(-1,-1), 12),
        ("LEFTPADDING",   (0,0),(-1,-1), 18),
        ("RIGHTPADDING",  (0,0),(-1,-1), 18),
    ]))
    story.append(ct)
    story.append(Spacer(1, 0.5*cm))

    # exam structure
    estruct = [
        [Paragraph("<b>Marks</b>",S["table_head"]), Paragraph("<b>Type</b>",S["table_head"]),
         Paragraph("<b>Word Limit</b>",S["table_head"]), Paragraph("<b>Strategy</b>",S["table_head"])],
        [Paragraph("1.5",S["table_cell"]), Paragraph("Short Answer",S["table_cell"]),
         Paragraph("~50 words",S["table_cell"]), Paragraph("Define + 1 crisp key point",S["table_cell"])],
        [Paragraph("5",S["table_cell"]), Paragraph("Short Essay",S["table_cell"]),
         Paragraph("300-500 words",S["table_cell"]), Paragraph("Intro + 3-4 main points + conclusion",S["table_cell"])],
        [Paragraph("10",S["table_cell"]), Paragraph("Essay",S["table_cell"]),
         Paragraph("500-700 words",S["table_cell"]), Paragraph("Detailed analysis + examples + verses",S["table_cell"])],
        [Paragraph("15",S["table_cell"]), Paragraph("Long Essay",S["table_cell"]),
         Paragraph("700-1000 words",S["table_cell"]), Paragraph("Full depth + modern links + conclusion",S["table_cell"])],
    ]
    et = Table(estruct, colWidths=[2.5*cm,3.5*cm,3.5*cm,7*cm])
    et.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),DEEP_BLUE),
        ("BACKGROUND",(0,1),(-1,1),LIGHT_BLUE),
        ("BACKGROUND",(0,2),(-1,2),CREAM),
        ("BACKGROUND",(0,3),(-1,3),LIGHT_BLUE),
        ("BACKGROUND",(0,4),(-1,4),CREAM),
        ("GRID",(0,0),(-1,-1),0.5,HexColor("#90A4AE")),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),7),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    story.append(et)
    story.append(Spacer(1, 0.4*cm))

    # ── PROBABILITY TABLE ────────────────────────────────────────
    story.append(divider())
    story.append(Paragraph("🎯  TOPIC-WISE EXAM PROBABILITY — MODULE 2", S["subtopic"]))
    probs = [
        ("Karma Yoga — Definition & Yoga of Action", 90),
        ("Living in the Present (Present-moment awareness)", 80),
        ("Nishkama Karma — Dedicated Action without Anxiety over Results", 95),
        ("Concept of Swadharma (One's own duty)", 90),
        ("Comparison: Karma Yoga vs Modern Mindfulness", 75),
        ("Dhyana Yoga — Definition & Tuning the Mind", 85),
        ("Quantity, Quality and Direction of Thoughts", 90),
        ("Reaching Inner Silence (Meditation process)", 85),
        ("Role of Intention in Karma Yoga", 70),
        ("Body-Mind-Consciousness Distinction (Dhyana Yoga context)", 75),
    ]
    for topic, pct in probs:
        story.append(prob_badge(topic, pct, S))
        story.append(Spacer(1, 2))

    # ════════════════════════════════════════════════════════════
    # KARMA YOGA — SECTION 1
    # ════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(header_bar("📚  KARMA YOGA (Chapter 3 & related) — YOGA OF ACTION", S, DARK_SAFFRON))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("🔍  What is Karma Yoga?", S["subtopic"]))
    story.append(Paragraph(
        "The word <b>Karma</b> comes from Sanskrit root 'kri' meaning 'to do' or 'to act.' "
        "The word <b>Yoga</b> means union or discipline. So <b>Karma Yoga</b> literally means "
        "'the discipline of action' or 'the yoga of work.' It is the path to spiritual growth and "
        "liberation through selfless, dedicated action — performing one's duties excellently, "
        "without craving for rewards or fear of failure.", S["body"]))
    story.append(Spacer(1, 0.2*cm))

    story.append(colored_box([
        Paragraph("KEY VERSE — Bhagavad Gita 2.47 (Most Important Verse of Karma Yoga):", S["section_label"]),
        Paragraph(
            "karmany evadhikaras te ma phalesu kadacana<br/>"
            "ma karma-phala-hetur bhur ma te sango stv akarmani",
            S["verse"]),
        Paragraph(
            "<b>Translation:</b> 'You have the right to perform your prescribed duties, but you are "
            "not entitled to the fruits of your actions. Never consider yourself the cause of the "
            "results of your activities, and never be attached to not doing your duty.'",
            S["highlight_box"]),
        Paragraph(
            "This single verse contains the entire philosophy of Karma Yoga. It is arguably the most "
            "quoted verse of the Bhagavad Gita in the entire world.",
            S["note"]),
    ], LIGHT_ORANGE, SAFFRON))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("📌  Three Pillars of Karma Yoga", S["subtopic"]))
    pillars = [
        ("PILLAR 1: Do Your Duty (Kartavya Karma)", LIGHT_BLUE, DEEP_BLUE,
         "You have the RIGHT and RESPONSIBILITY to act — to perform your prescribed duty "
         "(svadharma). Inaction is NOT an option in the Gita. Even renouncing action is itself "
         "an action. No one can remain inactive even for a moment — nature (prakriti) forces "
         "everyone to act through the three gunas. So the question is not WHETHER to act, "
         "but HOW to act. The Gita says: Act! But act wisely."),
        ("PILLAR 2: No Claim on Fruits (Ma Phalesu Kadachana)", LIGHT_GREEN, DARK_GREEN,
         "You have NO RIGHT over the fruits (results) of your actions. Why? Because results "
         "depend on countless factors beyond your control: time, place, other people's actions, "
         "God's will, your past karma. You control only your effort — not the outcome. "
         "When you work without attachment to results: (a) you give 100% to the process, "
         "(b) you are not paralyzed by fear of failure, (c) you are not corrupted by greed "
         "for rewards. This is the secret of peak performance AND inner peace simultaneously."),
        ("PILLAR 3: No Attachment to Inaction (Ma Te Sango Stv Akarmani)", LIGHT_ORANGE, SAFFRON,
         "The third instruction is often missed: do NOT use 'detachment from results' as an "
         "excuse for laziness or inaction! The Gita is not saying 'don't care about anything.' "
         "It is saying: care deeply about the quality of your action, but don't be anxious "
         "about results. Many people misread Karma Yoga as: 'Just do your thing, doesn't "
         "matter what happens.' NO — it means: act with full dedication and excellence, "
         "but without psychological attachment to outcomes."),
    ]
    for title, bg, border, content in pillars:
        story.append(colored_box([
            Paragraph(f"<b>⚡ {title}</b>", S["section_label"]),
            Paragraph(content, S["highlight_box"]),
        ], bg, border))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("🌟  Why Karma Yoga is the Path of Liberation", S["subtopic"]))
    story.append(Paragraph(
        "The Gita teaches that every action creates karma (cause-effect impressions) that binds "
        "the soul to the cycle of rebirth (samsara). How do we act without creating binding karma? "
        "By offering all actions to God/the Universe (Ishvara Arpana Buddhi). When you work as an "
        "instrument of God — doing your best without ego-investment in results — actions do not "
        "bind. This is called 'Yoga' — the action that liberates rather than binds.", S["body"]))
    story.append(Spacer(1, 0.2*cm))

    story.append(colored_box([
        Paragraph("🗺️  CONCEPT MAP — HOW KARMA YOGA WORKS:", S["section_label"]),
        Paragraph("ACTION + EGO + CRAVING FOR RESULTS = Binding Karma (more bondage, suffering)", S["bold_bullet"]),
        Paragraph("ACTION + DEDICATION + DETACHMENT FROM RESULTS = Karma Yoga (liberation)", S["bold_bullet"]),
        Paragraph("", S["body"]),
        Paragraph("FORMULA: Right Action (Svadharma) + Right Intention (Ishvara Arpana) + "
                  "Right Attitude (No Result Anxiety) = KARMA YOGA = Inner Peace + Outer Excellence", S["note"]),
    ], LIGHT_PURPLE, PURPLE_DARK))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("🔬  Modern Parallels of Karma Yoga", S["subtopic"]))
    story.append(Paragraph(
        "Karma Yoga is not just ancient philosophy — it maps perfectly onto modern psychology "
        "and peak performance science:", S["body"]))
    modern_parallels = [
        ("Mihaly Csikszentmihalyi's 'Flow State'",
         "The psychologist described 'flow' as a state of complete absorption in an activity, "
         "where ego disappears and performance peaks. This IS Karma Yoga — action without "
         "ego-self-consciousness, fully engaged in the present moment."),
        ("Sports Psychology — 'Process Focus'",
         "Top athletes (Sachin Tendulkar, Virat Kohli) are coached to focus on the process "
         "(technique, shot selection) not the result (winning, records). This is exactly "
         "BG 2.47: 'Your right is to work only, not to its fruits.'"),
        ("Stoic Philosophy (Marcus Aurelius)",
         "'You have power over your mind, not outside events. Realize this and you will find "
         "strength.' The Stoics independently arrived at the same insight as Karma Yoga: "
         "distinguish what is in your control (action) from what is not (results)."),
        ("Mindfulness-Based Stress Reduction (MBSR)",
         "Dr. Jon Kabat-Zinn's MBSR teaches doing tasks with full attention and without "
         "judgment about outcomes — a secular, clinical version of Nishkama Karma."),
    ]
    for pt, pc in modern_parallels:
        story.append(colored_box([
            Paragraph(f"<b>◆ {pt}:</b>", S["section_label"]),
            Paragraph(pc, S["highlight_box"]),
        ], CYAN_LIGHT, CYAN_DARK))
        story.append(Spacer(1, 3))

    # ════════════════════════════════════════════════════════════
    # TOPIC 2 — LIVING IN THE PRESENT
    # ════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(header_bar("📚  TOPIC 2: LIVING IN THE PRESENT (Present-Moment Awareness)", S, INDIGO))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("🔍  The Gita's Teaching on the Present Moment", S["subtopic"]))
    story.append(Paragraph(
        "The Bhagavad Gita does not use the modern term 'mindfulness,' but its entire teaching "
        "on Karma Yoga is grounded in present-moment awareness. The Gita teaches that the mind "
        "has three typical movement patterns — and liberation comes from transcending all three:", S["body"]))
    story.append(Spacer(1, 0.2*cm))

    mind_movements = [
        ("The Past-Dwelling Mind", LIGHT_RED, MAROON,
         "The mind constantly replays past events — regrets, grudges, nostalgia, shame. "
         "'If only I had done X differently...' This is what tormented Arjuna: he was "
         "mentally replaying his relationships and imagining the grief of past bonds being broken. "
         "The Gita calls this 'shoka' (grief rooted in past-attachment). It achieves nothing "
         "and destroys the present."),
        ("The Future-Worrying Mind", LIGHT_ORANGE, DARK_SAFFRON,
         "The mind projects into future fears and anxieties. 'What if I fail? What if they "
         "die? What if I lose?' Arjuna worried about future consequences of battle. "
         "The Gita calls this 'chinta' (anxiety about future). BG 2.47 directly addresses "
         "this: your right is to action NOW, not to results in the future."),
        ("The Present-Engaged Mind", LIGHT_GREEN, DARK_GREEN,
         "The liberated mind is fully present in THIS action, THIS moment, with full "
         "awareness and skill. This is what Krishna calls the 'Yoga' state. When Arjuna "
         "finally accepts his duty and picks up his bow, he is present. The Gita's entire "
         "teaching moves Arjuna from past-grief and future-anxiety to present-action."),
    ]
    for title, bg, border, content in mind_movements:
        story.append(colored_box([
            Paragraph(f"<b>{title}</b>", S["section_label"]),
            Paragraph(content, S["highlight_box"]),
        ], bg, border))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("🧠  Why 'Living in the Present' is Central to Karma Yoga", S["subtopic"]))

    present_points = [
        ("Only the Present Moment Can Be Acted In",
         "The past is gone — no action is possible in the past. The future hasn't come — "
         "you cannot act in a future that doesn't exist yet. The ONLY moment where "
         "action is possible is NOW. Therefore, Karma Yoga — yoga of action — is by "
         "definition yoga of the present moment. Krishna's instruction to 'perform your "
         "duty' is always an instruction to act RIGHT NOW."),
        ("Past and Future Are Mental Constructs",
         "The Gita teaches (through Sankhya philosophy) that only the soul (Atman) "
         "and Brahman are truly real — permanent and unchanging. The past and future "
         "exist only as thought-forms in the mind. When we are trapped in past grief "
         "or future anxiety, we are living in mental fictions, not reality. "
         "Present-moment awareness is therefore the most truthful way of living."),
        ("Anxiety Over Results = Future-Mind = Obstacle to Karma Yoga",
         "Krishna's instruction 'ma phalesu kadachana' (no attachment to fruits) is "
         "fundamentally an instruction to stay present. When you're anxious about "
         "results, your mind is in the future. When you're dwelling on past failures, "
         "your mind is in the past. Karma Yoga means: bring the mind back to THIS "
         "action, THIS moment. Full presence = full performance = karma yoga."),
        ("The Present Moment is Where God Meets You",
         "The Gita teaches that the Divine (Brahman/Krishna) is eternally present — "
         "not in the past or future, but in the eternal NOW. When Arjuna is fully "
         "present on the battlefield, he can hear Krishna's voice. When we are fully "
         "present in our actions, we can experience the divine guidance that is always "
         "available. Meditation and karma yoga both develop this capacity."),
    ]
    for pt, pc in present_points:
        story.append(colored_box([
            Paragraph(f"<b>◆ {pt}</b>", S["section_label"]),
            Paragraph(pc, S["highlight_box"]),
        ], CREAM, DARK_GOLD))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 0.2*cm))
    story.append(colored_box([
        Paragraph("💡  LIVING IN THE PRESENT — PRACTICAL APPLICATION:", S["section_label"]),
        Paragraph("Gita's Present-Moment Practice in Daily Life:", S["bold_bullet"]),
        Paragraph("• While studying: 100% attention on THIS page, THIS concept — not exam results", S["bullet"]),
        Paragraph("• While working: full focus on THIS task — not on appraisal, promotion, or office politics", S["bullet"]),
        Paragraph("• While talking: LISTEN completely to THIS person — not planning your reply", S["bullet"]),
        Paragraph("• While eating: taste THIS food — not scrolling phone or worrying about calories", S["bullet"]),
        Paragraph("• While exercising: feel THIS movement — not dreading the next rep", S["bullet"]),
        Paragraph("RESULT: Every activity becomes meditation. Every moment becomes yoga.", S["note"]),
    ], LIGHT_PURPLE, PURPLE_DARK))

    # ════════════════════════════════════════════════════════════
    # TOPIC 3 — NISHKAMA KARMA
    # ════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(header_bar("📚  TOPIC 3: NISHKAMA KARMA — DEDICATED ACTION WITHOUT ANXIETY OVER RESULTS", S, DARK_GREEN))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("🔍  Understanding Nishkama Karma", S["subtopic"]))
    story.append(Paragraph(
        "<b>Nishkama</b> = Nish (without) + Kama (desire/craving). "
        "<b>Nishkama Karma</b> = Action without selfish desire for results. "
        "This is the practical heart of Karma Yoga. It does NOT mean being lazy, "
        "indifferent, or robotic. It means performing every action with complete "
        "dedication and excellence — while being psychologically free from anxiety "
        "about whether the result will match your expectation.", S["body"]))
    story.append(Spacer(1, 0.2*cm))

    story.append(colored_box([
        Paragraph("KEY VERSE — Bhagavad Gita 4.18:", S["section_label"]),
        Paragraph(
            "karmany akarma yah pasyed akarmani ca karma yah<br/>"
            "sa buddhiman manusyesu sa yuktah krtsna-karma-krit",
            S["verse"]),
        Paragraph(
            "<b>Translation:</b> 'One who sees inaction in action, and action in inaction, "
            "is intelligent among men, and is in the transcendental position, although "
            "engaged in all sorts of activities.' — This verse points to the secret of "
            "Karma Yoga: externally active, internally still. Working without working.",
            S["highlight_box"]),
    ], LIGHT_ORANGE, SAFFRON))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("🎯  What 'No Anxiety Over Results' Actually Means", S["subtopic"]))
    story.append(Paragraph("Let's demolish common misconceptions:", S["body"]))
    story.append(Spacer(1, 0.1*cm))

    miscon_data = [
        [Paragraph("<b>WRONG Understanding</b>", S["table_head"]),
         Paragraph("<b>RIGHT Understanding (Gita)</b>", S["table_head"])],
        [Paragraph("Don't care about results at all", S["table_cell"]),
         Paragraph("Care 100% about the QUALITY of your action; just don't obsess over outcomes", S["table_cell"])],
        [Paragraph("Do mediocre work — 'results don't matter'", S["table_cell"]),
         Paragraph("Do EXCELLENT work — that IS the offering. Poor work = not Karma Yoga", S["table_cell"])],
        [Paragraph("Be passive and wait for things to happen", S["table_cell"]),
         Paragraph("Be proactive, decisive, courageous — full engagement, no laziness", S["table_cell"])],
        [Paragraph("Have no goals or ambitions", S["table_cell"]),
         Paragraph("Have goals — but hold them lightly. Work toward them without being destroyed if they shift", S["table_cell"])],
        [Paragraph("Don't plan for the future", S["table_cell"]),
         Paragraph("Plan thoroughly and act in the present — but don't be anxious about future outcomes", S["table_cell"])],
    ]
    mt = Table(miscon_data, colWidths=[8*cm, 8.5*cm])
    mt.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),MAROON),
        ("BACKGROUND",(0,1),(-1,1),LIGHT_RED),
        ("BACKGROUND",(0,2),(-1,2),LIGHT_GREEN),
        ("BACKGROUND",(0,3),(-1,3),LIGHT_RED),
        ("BACKGROUND",(0,4),(-1,4),LIGHT_GREEN),
        ("BACKGROUND",(0,5),(-1,5),LIGHT_RED),
        ("GRID",(0,0),(-1,-1),0.5,HexColor("#BDBDBD")),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),7),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    story.append(mt)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("⚙️  The Psychology of Nishkama Karma", S["subtopic"]))
    psych_points = [
        ("Why Result-Attachment Destroys Performance",
         "When you desperately NEED a particular result, the fear of not getting it "
         "creates tension, anxiety, and mental noise. This noise interferes with clear "
         "thinking and skilled action. Athletes call this 'choking under pressure.' "
         "Nishkama Karma removes this noise. When results don't define your worth, "
         "you perform with freedom, creativity, and full skill — paradoxically achieving "
         "BETTER results through non-attachment."),
        ("The Motivation Question: Why Act if Not for Results?",
         "This is the most common objection. The Gita's answer: act because it is your "
         "DUTY (dharma), because it is the RIGHT thing to do, because you are an "
         "instrument of the divine purpose. This is called 'Ishvara Arpana Buddhi' "
         "(offering your actions to God). When your motivation shifts from personal "
         "gain to dharmic service, you tap into an infinite reservoir of energy, "
         "enthusiasm, and creativity that ego-driven motivation cannot match."),
        ("The Role of Intention (Sankalpa)",
         "BG teaches that the QUALITY of intention behind an action determines its "
         "spiritual impact. The same external action — giving money, for example — "
         "can be: selfish (for tax benefit), egotistic (for social recognition), "
         "or Nishkama (pure service without expectation). Only the last is Karma Yoga. "
         "Intention is invisible to observers but fully known to the self and to God."),
        ("Dedication Without Anxiety — The Surgeon Analogy",
         "A great surgeon must be fully dedicated to saving the patient's life, "
         "using every skill with complete focus — yet cannot be emotionally overwhelmed "
         "or paralyzed by the fear that the patient might die. Too much emotional "
         "attachment impairs surgical precision. This is Nishkama Karma: "
         "100% dedication + 0% psychological anxiety = peak performance + inner peace."),
    ]
    for pt, pc in psych_points:
        story.append(colored_box([
            Paragraph(f"<b>◆ {pt}</b>", S["section_label"]),
            Paragraph(pc, S["highlight_box"]),
        ], LIGHT_BLUE, DEEP_BLUE))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 0.2*cm))
    story.append(colored_box([
        Paragraph("KEY VERSE — BG 3.19 (Ultimate instruction on Nishkama Karma):", S["section_label"]),
        Paragraph(
            "tasmad asaktah satatam karyam karma samacara<br/>"
            "asakto hy acaran karma param apnoti purusah",
            S["verse"]),
        Paragraph(
            "<b>Translation:</b> 'Therefore, without attachment, perform always the work "
            "that has to be done; for a man performing action without attachment attains "
            "the Supreme.' — Detachment from results is not weakness — it is the "
            "secret to both material excellence and spiritual liberation.",
            S["highlight_box"]),
    ], CREAM, DARK_GOLD))

    # ════════════════════════════════════════════════════════════
    # TOPIC 4 — SWADHARMA
    # ════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(header_bar("📚  TOPIC 4: CONCEPT OF SWADHARMA — ONE'S OWN DUTY", S, TEAL))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("🔍  What is Swadharma?", S["subtopic"]))
    story.append(Paragraph(
        "<b>Swadharma</b> = Swa (own) + Dharma (duty, righteousness, role). "
        "It literally means 'one's own duty' or 'one's own nature-based role.' "
        "The concept of Swadharma is one of the most practical and important teachings "
        "of the Bhagavad Gita — it tells each person WHAT they should be doing with their life "
        "and HOW they should be doing it.", S["body"]))
    story.append(Spacer(1, 0.2*cm))

    story.append(colored_box([
        Paragraph("KEY VERSE — Bhagavad Gita 3.35 (The Gold Standard of Swadharma):", S["section_label"]),
        Paragraph(
            "sreyan sva-dharmo vigunah para-dharmat sv-anusthitat<br/>"
            "sva-dharme nidhanam sreyah para-dharmo bhayavahah",
            S["verse"]),
        Paragraph(
            "<b>Translation:</b> 'It is far better to perform one's natural prescribed duty, "
            "though tinged with faults, than to perform the duty of another, even though "
            "perfectly. In fact, it is preferable to die in the discharge of one's duty, "
            "than to follow the path of another, which is full of danger.'",
            S["highlight_box"]),
        Paragraph(
            "This is one of the most quoted and debated verses of the Gita — deeply practical "
            "for career, life choices, and self-discovery.",
            S["note"]),
    ], LIGHT_ORANGE, SAFFRON))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("📋  Dimensions of Swadharma", S["subtopic"]))
    swadharma_dims = [
        ("1. Varna-based Swadharma (Role by Nature/Profession)",
         "The Gita recognizes four types of human temperament/function: "
         "Brahmin (intellectual/spiritual), Kshatriya (warrior/leader/protector), "
         "Vaishya (trader/entrepreneur), Shudra (craftsman/service). "
         "These are based on GUNA (inner quality) and KARMA (aptitude/action), "
         "NOT by birth (BG 4.13). For Arjuna — a Kshatriya — fighting a righteous "
         "war IS his Swadharma. Refusing to fight out of emotional attachment "
         "is abandoning his Swadharma, which the Gita calls a greater sin."),
        ("2. Ashrama-based Swadharma (Duty by Stage of Life)",
         "Duties differ across the four stages of life: Brahmacharya (student — duty: learning), "
         "Grihastha (householder — duty: family & work), Vanaprastha (retirement — duty: service & reflection), "
         "Sannyasa (renunciation — duty: spiritual practice). "
         "The Gita says: fulfilling the duties of your current stage IS your spiritual practice."),
        ("3. Situational Swadharma (Role in a Given Situation)",
         "Beyond profession and age, Swadharma is also situational: as a son, your duty is "
         "one thing; as a citizen, another; as an employee, another; as a parent, yet another. "
         "The Gita teaches that each role carries specific duties — and fulfilling them "
         "with integrity (without craving or aversion) IS Karma Yoga."),
        ("4. Inner Nature Swadharma (Following Your True Calling)",
         "Most deeply, Swadharma means acting in alignment with your innate nature "
         "(svabhava). When you do what you are naturally gifted for and genuinely called "
         "to do, work becomes effortless, joyful, and excellent. Forcing yourself to live "
         "someone else's life (paradharma) creates inner conflict, mediocrity, and suffering. "
         "The Gita says this is 'bhayavahah' — full of danger."),
    ]
    for title, content in swadharma_dims:
        story.append(colored_box([
            Paragraph(f"<b>◆ {title}</b>", S["section_label"]),
            Paragraph(content, S["highlight_box"]),
        ], LIGHT_PURPLE, PURPLE_DARK))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("🆚  Swadharma vs Paradharma — The Critical Distinction", S["subtopic"]))
    story.append(Spacer(1, 0.1*cm))
    compare_data = [
        [Paragraph("<b>SWADHARMA (Own Duty)</b>",S["table_head"]),
         Paragraph("<b>PARADHARMA (Others' Duty)</b>",S["table_head"])],
        [Paragraph("Aligned with your nature and calling",S["table_cell"]),
         Paragraph("Forced, artificial, borrowed identity",S["table_cell"])],
        [Paragraph("May seem imperfect but is genuinely yours",S["table_cell"]),
         Paragraph("May appear perfect but lacks authenticity",S["table_cell"])],
        [Paragraph("Produces inner peace and integrity",S["table_cell"]),
         Paragraph("Produces inner conflict and exhaustion",S["table_cell"])],
        [Paragraph("Even dying in it is better (BG 3.35)",S["table_cell"]),
         Paragraph("Even succeeding in it is dangerous (bhayavahah)",S["table_cell"])],
        [Paragraph("Example: Einstein doing physics (his true calling)",S["table_cell"]),
         Paragraph("Example: Einstein forced to be a soldier",S["table_cell"])],
        [Paragraph("Example: Arjuna fighting the righteous war",S["table_cell"]),
         Paragraph("Example: Arjuna becoming a monk to avoid battle",S["table_cell"])],
    ]
    ct = Table(compare_data, colWidths=[8.25*cm, 8.25*cm])
    ct.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),TEAL),
        ("BACKGROUND",(0,1),(-1,1),LIGHT_GREEN),
        ("BACKGROUND",(0,2),(-1,2),LIGHT_RED),
        ("BACKGROUND",(0,3),(-1,3),LIGHT_GREEN),
        ("BACKGROUND",(0,4),(-1,4),LIGHT_RED),
        ("BACKGROUND",(0,5),(-1,5),LIGHT_GREEN),
        ("BACKGROUND",(0,6),(-1,6),LIGHT_RED),
        ("GRID",(0,0),(-1,-1),0.5,HexColor("#BDBDBD")),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),7),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    story.append(ct)
    story.append(Spacer(1, 0.3*cm))

    story.append(colored_box([
        Paragraph("🌍  Swadharma in Modern Life:", S["section_label"]),
        Paragraph("• A doctor's Swadharma = heal patients with full skill and compassion", S["bullet"]),
        Paragraph("• A teacher's Swadharma = educate with patience and inspiration", S["bullet"]),
        Paragraph("• A soldier's Swadharma = protect the nation with courage and discipline", S["bullet"]),
        Paragraph("• A parent's Swadharma = nurture children with love and wisdom", S["bullet"]),
        Paragraph("• An engineer's Swadharma = design safe, excellent, honest solutions", S["bullet"]),
        Paragraph("KEY INSIGHT: Swadharma is not about what you WANT to do — it is about "
                  "what you are CALLED to do by your nature, situation, and role. When you "
                  "align these, Karma Yoga flows naturally.", S["note"]),
    ], CREAM, DARK_GOLD))

    # ════════════════════════════════════════════════════════════
    # KARMA YOGA Q&A
    # ════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(header_bar("📝  EXAM QUESTIONS — KARMA YOGA (All Mark Levels)", S, DEEP_BLUE))
    story.append(Spacer(1, 0.3*cm))

    # 1.5 mark questions
    short_qas = [
        ("What is Karma Yoga?",
         "Karma Yoga is the yoga of selfless action — performing one's prescribed duty with full "
         "dedication but without attachment to results. BG 2.47 is its cornerstone: 'You have the "
         "right to work, but never to the fruits of work.' It is the path of liberation through "
         "righteous, ego-free action."),
        ("What does 'Living in the Present' mean?",
         "Living in the present means performing actions with full awareness and engagement in the "
         "current moment — without being trapped in past regrets or future anxieties. In Karma Yoga, "
         "the present is the only space where action is possible. Full presence = full performance."),
        ("What is the meaning of Swadharma according to the Gita?",
         "Swadharma means one's own duty — the specific responsibilities arising from one's "
         "nature, profession, stage of life, and situation. The Gita teaches: 'Better to perform "
         "one's own duty imperfectly than another's perfectly.' Authentic alignment with one's "
         "calling is essential for inner peace and spiritual growth."),
        ("What is the role of intention in Karma Yoga?",
         "In Karma Yoga, INTENTION (sankalpa) determines the spiritual quality of action. The same "
         "external action can be selfish (sakama karma) or selfless (nishkama karma) depending on "
         "motive. Action done for personal gain creates binding karma; action offered to God/dharma "
         "without personal craving is liberating Karma Yoga."),
    ]
    for q, a in short_qas:
        story.append(colored_box([
            Paragraph(f"<b>Q: {q} [1.5 marks]</b>", S["exam_q"]),
            Paragraph(a, S["exam_a"]),
        ], GRAY_BG, HexColor("#BDBDBD")))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 0.2*cm))
    story.append(divider(DARK_GREEN))

    # 5 mark
    story.append(Paragraph("5-Mark Questions:", S["subtopic"]))
    story.append(colored_box([
        Paragraph("Q: Define Karma Yoga and explain how it teaches the principle of action without attachment to results. [5 marks]", S["exam_q"]),
        Paragraph(
            "<b>Introduction:</b> Karma Yoga, taught primarily in Chapters 3 and 4 of the Bhagavad Gita, "
            "is the yoga of selfless, dedicated action. It is one of the three main paths to liberation "
            "alongside Jnana Yoga (knowledge) and Bhakti Yoga (devotion).<br/><br/>"
            "<b>Definition:</b> Karma Yoga is the discipline of performing one's prescribed duty (svadharma) "
            "with complete dedication and skill, without craving for personal rewards or fear of failure. "
            "The practitioner acts, but dedicates the fruits of action to God or to dharma, remaining "
            "internally free from the outcome.<br/><br/>"
            "<b>Core Principle — BG 2.47:</b> 'You have a right to perform your prescribed duties, "
            "but you are not entitled to the fruits of your actions.' This verse establishes the "
            "fundamental distinction: you control the ACTION (your effort, skill, dedication), "
            "but the RESULT depends on many factors beyond you (time, others, God's will, past karma). "
            "Attaching your happiness to results is therefore both irrational and spiritually binding.<br/><br/>"
            "<b>Why Detachment Enhances Performance:</b> Paradoxically, when you release result-anxiety, "
            "performance improves. Athletes in 'flow state,' surgeons in crisis, artists in creative "
            "immersion — all describe a state of pure engagement where self-consciousness dissolves and "
            "excellence emerges naturally. This IS Karma Yoga.<br/><br/>"
            "<b>Three Instructions (BG 2.47):</b> (1) Perform your duty, (2) No claim on results, "
            "(3) Don't use non-attachment as excuse for inaction — all three must be practiced together.<br/><br/>"
            "<b>Conclusion:</b> Karma Yoga is revolutionary: it offers both peak performance AND inner "
            "peace simultaneously. By working without ego-attachment, every action becomes a spiritual "
            "practice and a step toward liberation.",
            S["exam_a"]),
    ], LIGHT_BLUE, DEEP_BLUE))
    story.append(Spacer(1, 0.3*cm))

    story.append(colored_box([
        Paragraph("Q: Compare Karma Yoga vs. Modern Mindfulness. [5 marks]", S["exam_q"]),
        Paragraph(
            "<b>Introduction:</b> Though separated by millennia and cultural contexts, Karma Yoga "
            "(Bhagavad Gita, ~3000 BCE) and Modern Mindfulness (Jon Kabat-Zinn, 1979 CE) share "
            "profound philosophical parallels — and important distinctions.<br/><br/>"
            "<b>Similarities:</b><br/>"
            "1. PRESENT-MOMENT FOCUS: Both teach bringing full attention to the present action, "
            "not scattered between past and future.<br/>"
            "2. NON-ATTACHMENT: Both cultivate non-grasping relationship with outcomes — "
            "doing the activity fully without being defined by results.<br/>"
            "3. REDUCING ANXIETY: Both are powerful tools for stress reduction and mental clarity.<br/>"
            "4. PERFORMANCE ENHANCEMENT: Both improve performance by eliminating the interference "
            "of result-anxiety and self-consciousness.<br/><br/>"
            "<b>Differences:</b><br/>"
            "1. PURPOSE: Karma Yoga aims at spiritual liberation (moksha); mindfulness aims primarily "
            "at mental health and wellbeing.<br/>"
            "2. FRAMEWORK: Karma Yoga is embedded in a complete spiritual framework (Dharma, Atman, God); "
            "mindfulness is secular and clinical.<br/>"
            "3. DUTY: Karma Yoga specifically teaches Swadharma — acting from one's role/duty; "
            "mindfulness is context-neutral.<br/>"
            "4. OFFERING: Karma Yoga includes 'Ishvara Arpana' (offering actions to God); "
            "mindfulness has no such theological dimension.<br/><br/>"
            "<b>Conclusion:</b> Modern mindfulness is a secular, therapeutic subset of what Karma Yoga "
            "offers at a deeper, more comprehensive level. The Gita subsumes mindfulness within a "
            "complete vision of human purpose and liberation.",
            S["exam_a"]),
    ], LIGHT_GREEN, DARK_GREEN))
    story.append(Spacer(1, 0.3*cm))

    # 10 mark
    story.append(divider(DARK_SAFFRON))
    story.append(Paragraph("10-Mark Questions:", S["subtopic"]))
    story.append(colored_box([
        Paragraph("Q: Discuss the relevance of living in the present and the concept of Swadharma in modern life. [10 marks]", S["exam_q"]),
        Paragraph(
            "<b>INTRODUCTION:</b><br/>"
            "Two of the most practically relevant teachings of the Bhagavad Gita for modern life are "
            "'Living in the Present' and the concept of Swadharma. Together, they provide a complete "
            "framework for meaningful, peaceful, and effective living in the 21st century.<br/><br/>"
            "<b>PART 1 — LIVING IN THE PRESENT:</b><br/>"
            "The Gita's entire teaching on Karma Yoga is rooted in present-moment awareness. "
            "Krishna's instruction to 'perform your duty' is always an instruction to act NOW — "
            "not to dwell on past failures or future anxieties. BG 2.47 defines this perfectly: "
            "your right is to action (present), not to results (future).<br/><br/>"
            "In modern life, the epidemic of anxiety and depression is largely driven by the mind's "
            "inability to stay present. Studies show that the average person spends 47% of their "
            "waking time thinking about something other than what they're currently doing (Harvard "
            "research by Killingsworth and Gilbert, 2010). This mind-wandering directly correlates "
            "with unhappiness. The Gita's remedy is exact: bring the mind fully to THIS moment, "
            "THIS action.<br/><br/>"
            "Living in the present means: (1) While working — full focus on the task, not on the "
            "appraisal. (2) While in relationships — genuinely present with the person, not "
            "distracted by the phone. (3) While studying — fully engaged with the subject, "
            "not worried about marks. This is Karma Yoga in practice.<br/><br/>"
            "Modern neuroscience confirms: present-moment focus activates the prefrontal cortex "
            "(executive function, creativity, emotional regulation) and deactivates the default "
            "mode network (mind-wandering, rumination, anxiety). The Gita's ancient wisdom is "
            "validated by modern brain science.<br/><br/>"
            "<b>PART 2 — SWADHARMA IN MODERN LIFE:</b><br/>"
            "Swadharma (one's own duty) is the Gita's answer to the modern question: "
            "'What should I do with my life?' BG 3.35 declares: 'Better to perform one's own "
            "duty imperfectly than another's perfectly.' This is a radical call to authenticity.<br/><br/>"
            "In modern terms, Swadharma = your calling, your authentic role, your dharmic purpose. "
            "It encompasses: your professional duty (perform your job with integrity and excellence), "
            "your relational duty (be present and responsible in your roles as child, parent, friend, "
            "citizen), and your inner calling (align your work with your deepest gifts and values).<br/><br/>"
            "The modern crisis of 'choosing the right career' is essentially a Swadharma question. "
            "When people choose careers based on social pressure, parental expectation, or financial "
            "reward alone (paradharma), they often succeed externally but suffer internally. "
            "When they follow their genuine calling (swadharma), work becomes energizing "
            "and life feels purposeful.<br/><br/>"
            "Viktor Frankl's 'Man's Search for Meaning' — the foundational text of existential "
            "psychology — echoes the Gita: humans need meaning (dharma) and present-moment "
            "engagement to thrive. His logotherapy is essentially a Western version of "
            "Swadharma + Present-moment Karma Yoga.<br/><br/>"
            "<b>CONCLUSION:</b><br/>"
            "Living in the present and following Swadharma are not abstract ideals — they are "
            "the most practical prescriptions for modern mental health, professional excellence, "
            "and personal fulfillment. In an age of distraction, comparison, and identity crisis, "
            "these Gita teachings are more urgently needed than ever. Their timeless wisdom "
            "finds validation in modern psychology, neuroscience, and organizational management.",
            S["exam_a"]),
    ], LIGHT_ORANGE, SAFFRON))

    # 15 mark — split into boxes
    story.append(PageBreak())
    story.append(header_bar("📝  15-MARK ANSWER: KARMA YOGA — COMPLETE", S, MAROON))
    story.append(Spacer(1, 0.2*cm))
    story.append(colored_box([
        Paragraph("Q: How does the Gita resolve duty vs. emotion? [15 marks]", S["exam_q"]),
    ], GRAY_BG, INDIGO))
    story.append(Spacer(1, 4))

    for label, text, bg, border in [
        ("INTRODUCTION — The Central Conflict:",
         "The Bhagavad Gita's most dramatic moment is Arjuna's collapse on the battlefield — "
         "a perfect illustration of the universal human conflict between DUTY (dharma) and EMOTION "
         "(moha/attachment). This conflict is not unique to Arjuna. Every person faces it: the "
         "doctor who must give a painful diagnosis to a loved one, the judge who must sentence "
         "a friend, the soldier who must fight, the manager who must fire someone. The Gita's "
         "resolution of this conflict is one of its greatest gifts to humanity.",
         LIGHT_BLUE, DEEP_BLUE),
        ("THE PROBLEM — How Emotion Hijacks Duty:",
         "Arjuna's emotional attachment (moha) causes him to: misidentify himself (as a family "
         "member rather than a soul with a warrior's duty), confuse sentimentality with wisdom, "
         "construct 'logical' arguments that are actually rationalizations of fear and grief, "
         "and abandon his prescribed duty (Swadharma). Krishna diagnoses this precisely in "
         "BG 2.3: 'O Arjuna, yield not to this unmanliness. It does not become you. Shake off "
         "your faint-heartedness and arise.' The problem is not emotion per se — it is "
         "letting emotion override discernment (viveka) and duty (dharma).",
         LIGHT_RED, MAROON),
        ("RESOLUTION STEP 1 — Self-Knowledge (Know WHO You Are):",
         "Krishna first addresses the root cause: Arjuna's misidentification. He teaches that "
         "Arjuna is NOT the son of Kunti, the student of Drona, the friend of Duryodhana. "
         "He is an eternal soul (Atman) with a Kshatriya's duty in THIS lifetime. When "
         "you know your true identity (eternal soul), emotional entanglements with temporary "
         "bodily relationships lose their tyrannical grip. This is why self-knowledge "
         "(Sankhya Yoga) must precede Karma Yoga — you must first know WHO you are before "
         "you can know WHAT you must do.",
         CREAM, DARK_GOLD),
        ("RESOLUTION STEP 2 — Swadharma (Know WHAT You Must Do):",
         "Once Arjuna knows his true identity, his duty becomes clear: he is a Kshatriya, "
         "the battle is righteous (dharma-yuddha), and fighting is his Swadharma. "
         "BG 3.35: 'Better to perform one's own duty, though imperfectly, than to perform "
         "another's duty perfectly.' The Gita does not say 'suppress your emotions and fight.' "
         "It says 'understand the deeper reality and let your duty flow from that understanding.'",
         LIGHT_GREEN, DARK_GREEN),
        ("RESOLUTION STEP 3 — Nishkama Karma (HOW to Fulfill Duty Without Emotional Suffering):",
         "Even if Arjuna accepts his duty, how does he fight without being destroyed by grief "
         "at killing his loved ones? The answer is Nishkama Karma: act as an instrument of "
         "dharma, not as a personal agent driven by ego. When you offer your actions to God "
         "(Ishvara Arpana), you are no longer personally responsible for outcomes — you are "
         "an instrument. This frees you from both the paralysis of emotional attachment "
         "and the guilt of results. The surgeon performs the operation with full skill, "
         "but offers the outcome to God — this is how duty and emotion are reconciled.",
         LIGHT_PURPLE, PURPLE_DARK),
        ("RESOLUTION STEP 4 — Equanimity (Sama-Bhava) and the Gita's Final Answer:",
         "The Gita doesn't ask Arjuna to stop feeling love for his family. It asks him to "
         "develop EQUANIMITY — the ability to feel emotions without being controlled by them. "
         "BG 2.48: 'Be steadfast in yoga, O Arjuna. Perform your duty and abandon all "
         "attachment to success or failure. Such equanimity is called yoga.' Equanimity "
         "is NOT indifference — it is the mature capacity to feel deeply AND act wisely "
         "simultaneously. This is the highest integration of duty and emotion.",
         LIGHT_ORANGE, SAFFRON),
        ("MODERN APPLICATION AND CONCLUSION:",
         "This resolution is urgently needed today. Medical professionals face duty vs. emotion "
         "daily. Judges must separate personal feelings from justice. Parents must balance love "
         "with firmness. The Gita's framework — Self-Knowledge + Swadharma + Nishkama Karma "
         "+ Equanimity — provides a complete, practically applicable solution. "
         "The Gita resolves duty vs. emotion not by suppressing emotion or ignoring duty, "
         "but by elevating consciousness to the level where both can coexist in wisdom. "
         "This is the definition of psychological maturity — and the Gita described it "
         "5,000 years ago.",
         CYAN_LIGHT, CYAN_DARK),
    ]:
        story.append(colored_box([
            Paragraph(f"<b>{label}</b>", S["section_label"]),
            Paragraph(text, S["exam_a"]),
        ], bg, border))
        story.append(Spacer(1, 4))

    # ════════════════════════════════════════════════════════════
    # DHYANA YOGA — SECTION 5
    # ════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(header_bar("📚  DHYANA YOGA (Chapter 6) — TUNING THE MIND", S, PURPLE_DARK))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("🔍  What is Dhyana Yoga?", S["subtopic"]))
    story.append(Paragraph(
        "<b>Dhyana</b> = Meditation / Contemplation. "
        "<b>Dhyana Yoga</b> is the yoga of meditation — the systematic practice of training, "
        "calming, and ultimately transcending the mind to rest in pure awareness. "
        "Chapter 6 of the Gita is titled 'Dhyana Yoga' or 'Atma-Samyama Yoga' (yoga of "
        "self-restraint/self-mastery). It is the chapter where Krishna gives detailed, "
        "practical instructions on meditation — how to sit, where to sit, how to train "
        "the mind, what to do when the mind wanders, and what the final state of "
        "meditation feels like.", S["body"]))
    story.append(Spacer(1, 0.2*cm))

    story.append(colored_box([
        Paragraph("KEY VERSE — BG 6.5 (Most Powerful Verse on Self-Mastery):", S["section_label"]),
        Paragraph(
            "uddhared atmanatmanam natmanam avasadayet<br/>"
            "atmaiva hy atmano bandhur atmaiva ripur atmanah",
            S["verse"]),
        Paragraph(
            "<b>Translation:</b> 'A person must elevate himself by his own mind, and not degrade "
            "himself. The mind is the friend of the conditioned soul, and his enemy as well.' "
            "— This verse establishes the central theme of Dhyana Yoga: YOU are responsible "
            "for your mind. The mind can be your greatest ally or your worst enemy — "
            "the choice is made through meditation and self-discipline.",
            S["highlight_box"]),
    ], LIGHT_PURPLE, PURPLE_DARK))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("🔑  What 'Tuning the Mind' Means", S["subtopic"]))
    story.append(Paragraph(
        "Krishna uses the term 'tuning the mind' (in modern translation) to describe the process "
        "of bringing the mind into alignment — like tuning a musical instrument or a radio "
        "receiver. A tuned mind picks up the signal of truth, wisdom, and peace clearly. "
        "An untuned mind receives only noise: random thoughts, desires, fears, memories. "
        "The practice of Dhyana Yoga is the process of tuning.", S["body"]))
    story.append(Spacer(1, 0.2*cm))

    tuning_elements = [
        ("What Makes a Mind 'Untuned'?",
         "An untuned mind is characterized by: Constant internal chatter (monkey mind), "
         "Racing between past memories and future worries, Compulsive reactions to every "
         "stimulus, Inability to concentrate on one thing for more than a few minutes, "
         "Emotional reactivity — being 'triggered' by minor events, No access to deep "
         "intuition or inner wisdom. This is most people's default state in the modern world."),
        ("What Does a 'Tuned' Mind Look Like?",
         "A tuned mind (as described by Krishna in BG 6): Is calm but alert, "
         "Can focus completely on one object/task for extended periods, "
         "Observes thoughts without being swept away by them, "
         "Responds to situations rather than reacting compulsively, "
         "Has access to deep intuition, creativity, and wisdom, "
         "Rests in inner silence even while engaged in outer activity."),
        ("How Karma Yoga and Dhyana Yoga Connect",
         "Karma Yoga (outer) and Dhyana Yoga (inner) are complementary practices. "
         "Karma Yoga tunes the mind through action — by practicing non-attachment, "
         "present-moment focus, and Swadharma in daily life. "
         "Dhyana Yoga tunes the mind through formal meditation — by training it "
         "in stillness and withdrawal. Together they create the complete yogic life: "
         "active and still, engaged and at peace, working and meditating."),
    ]
    for title, content in tuning_elements:
        story.append(colored_box([
            Paragraph(f"<b>◆ {title}</b>", S["section_label"]),
            Paragraph(content, S["highlight_box"]),
        ], LIGHT_BLUE, DEEP_BLUE))
        story.append(Spacer(1, 4))

    # ════════════════════════════════════════════════════════════
    # TOPIC 6 — QUANTITY QUALITY DIRECTION OF THOUGHTS
    # ════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(header_bar("📚  TOPIC 6: QUANTITY, QUALITY AND DIRECTION OF THOUGHTS", S, INDIGO))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("🔍  The Gita's Analysis of the Mind's Three Problems", S["subtopic"]))
    story.append(Paragraph(
        "Dhyana Yoga is, at its core, a systematic science of the mind. The Gita identifies that "
        "the untrained mind has THREE fundamental problems that meditation must address. "
        "Understanding these three dimensions — Quantity, Quality, and Direction of thoughts — "
        "gives a complete picture of what mental training involves.", S["body"]))
    story.append(Spacer(1, 0.2*cm))

    # QUANTITY
    story.append(colored_box([
        Paragraph("1. QUANTITY OF THOUGHTS — The Mind Thinks Too Much", S["section_label"]),
    ], DEEP_BLUE, DEEP_BLUE))
    story.append(Spacer(1, 0.1*cm))

    quantity_content = [
        ("The Problem — Thought Overload",
         "Modern research suggests the average human mind generates 60,000–80,000 thoughts per day. "
         "Of these, approximately 95% are repetitive (the same thoughts recycled over and over) "
         "and 80% are negative. This constant mental noise is exhausting, prevents clear thinking, "
         "and creates chronic stress. The Gita describes this as 'chanchal' (restless) and "
         "'pramathi' (agitating) and 'balavad' (powerfully forceful) mind — BG 6.34."),
        ("The Gita's Solution — Reduce Thought Volume",
         "Krishna teaches that meditation reduces the sheer quantity of thoughts by: "
         "(1) Training the mind to focus on ONE object (Dharana), reducing scattered thinking. "
         "(2) Watching thoughts without feeding them — a thought without attention dies "
         "naturally. (3) Gradually creating gaps between thoughts — these gaps are where "
         "peace resides. (4) The practice of Pratyahara (withdrawal of senses) reduces "
         "the external stimuli that generate thoughts."),
        ("BG 6.34-35 — Arjuna's Complaint and Krishna's Answer",
         "Arjuna himself admits: 'The mind is restless, turbulent, obstinate, and very strong, "
         "O Krishna, and to subdue it, I think, is more difficult than controlling the wind.' "
         "(BG 6.34). Krishna agrees — the mind IS difficult to control. But he gives "
         "the solution in BG 6.35: 'Undoubtedly the mind is restless and difficult to "
         "control, but it can be controlled by constant practice (abhyasa) and "
         "detachment (vairagya).' These two — PRACTICE and DETACHMENT — are the "
         "master keys to reducing thought quantity."),
    ]
    for title, content in quantity_content:
        story.append(colored_box([
            Paragraph(f"<b>{title}</b>", S["section_label"]),
            Paragraph(content, S["highlight_box"]),
        ], LIGHT_BLUE, INDIGO))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 0.2*cm))

    # QUALITY
    story.append(colored_box([
        Paragraph("2. QUALITY OF THOUGHTS — The Mind Thinks Unhealthy Thoughts", S["section_label"]),
    ], DARK_GREEN, DARK_GREEN))
    story.append(Spacer(1, 0.1*cm))

    quality_content = [
        ("The Problem — Toxic Thought Patterns",
         "Not just the quantity but the QUALITY of thoughts determines mental health. "
         "The Gita describes how impure thoughts (driven by desire, anger, greed, jealousy) "
         "create a cascade of destruction. BG 2.62-63 describes the 'chain of ruin': "
         "Contemplating sense objects -> Attachment -> Desire -> Anger -> "
         "Delusion -> Memory failure -> Intelligence destroyed -> Fall. "
         "Each low-quality thought strengthens the neural pathway of that thought pattern."),
        ("Three Categories of Thought Quality (related to Three Gunas)",
         "TAMASIC thoughts: Dull, dark, depressive, destructive, delusional — 'Everything "
         "is hopeless, I am worthless, nothing matters.' These drag consciousness down. "
         "RAJASIC thoughts: Excited, agitated, craving, ambitious, anxious — 'I must have "
         "this, I fear that, I want more.' These scatter energy. "
         "SATTVIC thoughts: Clear, compassionate, truthful, peaceful, wisdom-oriented — "
         "'What is right? How can I help? What is true?' These elevate consciousness."),
        ("The Gita's Solution — Cultivate Sattvic Thoughts",
         "Dhyana Yoga improves thought quality by: (1) REPLACING tamasic/rajasic thoughts "
         "with sattvic ones through satsanga (good company), svadhyaya (self-study/scripture), "
         "and mantra. (2) OBSERVING thoughts without identification — when you watch a "
         "toxic thought without believing it, its power dissolves. (3) MEDITATION purifies "
         "thought quality at the source — regular deep meditation progressively reduces "
         "negative thought generation. BG 17.16: 'Purity of mind (chitta-prasada) is "
         "austerity of the mind — cultivating thoughts of equanimity, compassion, silence.'"),
    ]
    for title, content in quality_content:
        story.append(colored_box([
            Paragraph(f"<b>{title}</b>", S["section_label"]),
            Paragraph(content, S["highlight_box"]),
        ], LIGHT_GREEN, DARK_GREEN))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 0.2*cm))

    # DIRECTION
    story.append(colored_box([
        Paragraph("3. DIRECTION OF THOUGHTS — The Mind Points in the Wrong Direction", S["section_label"]),
    ], DARK_SAFFRON, DARK_SAFFRON))
    story.append(Spacer(1, 0.1*cm))

    direction_content = [
        ("The Problem — Outward-Pointing Mind",
         "The untrained mind is habitually EXTROVERTED — constantly directed outward toward "
         "sense objects, external events, other people's opinions. It seeks happiness, security, "
         "and meaning entirely in the external world. The Gita calls this 'bahirmukhi' "
         "(outward-facing). This creates perpetual dependence on external circumstances "
         "for inner wellbeing — an impossible and exhausting condition."),
        ("The Solution — Inward-Pointing Mind (Antarmukhi)",
         "Dhyana Yoga teaches the mind to turn INWARD — toward the source of awareness itself. "
         "This is called 'pratyahara' (withdrawal of senses) in the Yoga tradition. "
         "When the mind rests in pure awareness — the silent witness behind all thoughts "
         "and perceptions — it discovers the only permanently satisfying peace. "
         "BG 6.20-21: 'In that state of yoga, the meditator, by the grace of the self, "
         "becomes free from anxiety, and in that condition of self-realization, "
         "one finds nothing superior. Being so situated, one is never shaken even in "
         "the midst of the greatest difficulty.'"),
        ("God/Brahman as the Final Direction",
         "The ultimate direction for thoughts in Dhyana Yoga is toward the Divine — toward "
         "Brahman, Krishna, the eternal truth. BG 6.14: 'With a serene and fearless mind, "
         "firm in the brahmacharya vow, controlling the mind, let him sit in yoga, "
         "thinking of Me and having Me as the supreme goal.' When thoughts are directed "
         "toward the highest — toward truth, beauty, love, God — they become devotion "
         "(bhakti) and meditation simultaneously. Direction of thought = direction of life."),
        ("The Three Directions in Practice",
         "DOWNWARD direction (tamas): Thoughts toward self-pity, addiction, violence, "
         "delusion — spiritually degrading. "
         "HORIZONTAL direction (rajas): Thoughts toward worldly ambitions, sensory pleasure, "
         "social status — spiritually neutral, potentially purifiable. "
         "UPWARD direction (sattva/beyond): Thoughts toward truth, wisdom, service, God — "
         "spiritually elevating. Dhyana Yoga progressively shifts the default direction "
         "of thinking from downward/horizontal to upward."),
    ]
    for title, content in direction_content:
        story.append(colored_box([
            Paragraph(f"<b>{title}</b>", S["section_label"]),
            Paragraph(content, S["highlight_box"]),
        ], CREAM, DARK_SAFFRON))
        story.append(Spacer(1, 3))

    # ════════════════════════════════════════════════════════════
    # TOPIC 7 — REACHING INNER SILENCE
    # ════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(header_bar("📚  TOPIC 7: REACHING INNER SILENCE — THE GOAL OF DHYANA YOGA", S, TEAL))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("🔍  What is Inner Silence?", S["subtopic"]))
    story.append(Paragraph(
        "Inner Silence does not mean complete absence of thoughts or the death of the mind. "
        "It means a state of <b>deep inner stillness and peace</b> that coexists with — and "
        "underlies — all external activity. It is the silence between the notes that makes "
        "music possible; the space between words that makes language meaningful; the "
        "stillness behind all movement. In the Gita and Yoga traditions, this is called "
        "<b>Shanti</b> (peace), <b>Samadhi</b> (absorption), or <b>Nirvana</b> — the "
        "ultimate goal of all meditation.", S["body"]))
    story.append(Spacer(1, 0.2*cm))

    story.append(colored_box([
        Paragraph("KEY VERSE — BG 6.20-22 (Description of Inner Silence / Samadhi):", S["section_label"]),
        Paragraph(
            "In the stage of perfection called trance or samadhi, one's mind is completely "
            "restrained from material mental activities by practice of yoga. This is "
            "characterized by one's ability to see the self by the pure mind, and to relish "
            "and rejoice in the self. In that joyous state, one is situated in boundless "
            "transcendental happiness, realized through transcendental senses. Established "
            "thus, one never departs from the truth, and upon gaining this he thinks "
            "there is no greater gain.",
            S["verse"]),
        Paragraph(
            "This is the state of Inner Silence — not emptiness, but fullness. "
            "Not nothingness, but pure consciousness. Not absence, but the most "
            "profound presence.",
            S["note"]),
    ], LIGHT_ORANGE, SAFFRON))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("🧘  The Step-by-Step Process of Reaching Inner Silence", S["subtopic"]))
    story.append(Paragraph(
        "The Gita and classical Yoga tradition (Patanjali's Ashtanga Yoga) describe "
        "a progressive process of moving from outer noise to inner silence:", S["body"]))
    story.append(Spacer(1, 0.2*cm))

    steps_data = [
        [Paragraph("<b>Step</b>",S["table_head"]),
         Paragraph("<b>Sanskrit Term</b>",S["table_head"]),
         Paragraph("<b>Practice</b>",S["table_head"]),
         Paragraph("<b>What Happens</b>",S["table_head"])],
        [Paragraph("1",S["table_cell"]),
         Paragraph("Yama / Niyama",S["table_cell"]),
         Paragraph("Ethical living, self-discipline",S["table_cell"]),
         Paragraph("Mind stops generating guilt, conflict. Foundation for peace.",S["table_cell"])],
        [Paragraph("2",S["table_cell"]),
         Paragraph("Asana",S["table_cell"]),
         Paragraph("Physical posture — sitting still (BG 6.13)",S["table_cell"]),
         Paragraph("Body stillness reduces mental agitation. 'Sukham sthiram asanam.'",S["table_cell"])],
        [Paragraph("3",S["table_cell"]),
         Paragraph("Pranayama",S["table_cell"]),
         Paragraph("Breath regulation",S["table_cell"]),
         Paragraph("Breath and mind are connected. Slow breath = slow mind. Thought quantity drops.",S["table_cell"])],
        [Paragraph("4",S["table_cell"]),
         Paragraph("Pratyahara",S["table_cell"]),
         Paragraph("Withdrawal of senses from objects",S["table_cell"]),
         Paragraph("External stimuli stop feeding thoughts. Like tortoise withdrawing limbs (BG 2.58).",S["table_cell"])],
        [Paragraph("5",S["table_cell"]),
         Paragraph("Dharana",S["table_cell"]),
         Paragraph("Concentration on one point",S["table_cell"]),
         Paragraph("Mind narrows to one focus. Thought quantity dramatically reduces.",S["table_cell"])],
        [Paragraph("6",S["table_cell"]),
         Paragraph("Dhyana",S["table_cell"]),
         Paragraph("Sustained meditation — unbroken flow of attention",S["table_cell"]),
         Paragraph("Observer and object begin to merge. Deep peace. Time sense dissolves.",S["table_cell"])],
        [Paragraph("7",S["table_cell"]),
         Paragraph("Samadhi",S["table_cell"]),
         Paragraph("Complete absorption — Inner Silence",S["table_cell"]),
         Paragraph("No subject-object division. Pure awareness. Boundless joy. This IS Inner Silence.",S["table_cell"])],
    ]
    st = Table(steps_data, colWidths=[1.2*cm, 3*cm, 5*cm, 7.3*cm])
    st.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),TEAL),
        ("BACKGROUND",(0,1),(-1,1),LIGHT_ORANGE),
        ("BACKGROUND",(0,2),(-1,2),CREAM),
        ("BACKGROUND",(0,3),(-1,3),LIGHT_ORANGE),
        ("BACKGROUND",(0,4),(-1,4),CREAM),
        ("BACKGROUND",(0,5),(-1,5),LIGHT_ORANGE),
        ("BACKGROUND",(0,6),(-1,6),CREAM),
        ("BACKGROUND",(0,7),(-1,7),LIGHT_ORANGE),
        ("GRID",(0,0),(-1,-1),0.5,HexColor("#80CBC4")),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),6),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    story.append(st)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("🌊  Characteristics of Inner Silence (What It Feels Like)", S["subtopic"]))
    inner_silence_chars = [
        ("Beyond Happiness and Unhappiness",
         "Inner silence is not 'feeling happy' (which depends on external events). It is "
         "a baseline state of peace that is independent of circumstances. The Gita calls "
         "it 'atma-tusti' (contentment in the self) — a joy that has no opposite, "
         "because it does not come from any cause."),
        ("The Witness State (Sakshi Bhava)",
         "In inner silence, one rests as the witness (sakshi) — the awareness that "
         "observes thoughts, emotions, and perceptions without being identified with "
         "any of them. Like a mirror that reflects everything but is not touched by "
         "any reflection. BG 6.29: 'A yogi sees all beings equally — in me, and me in all.'"),
        ("Unshakeable Stability",
         "BG 6.20: 'In that state one is never shaken even in the midst of greatest "
         "difficulty.' This is not emotional numbness — it is a stability so deep that "
         "external storms cannot reach the center. The ocean's surface has waves; "
         "its depths are always still. Inner silence is the depth."),
        ("Effortless Action (Sahaja Yoga)",
         "Paradoxically, from a state of inner silence, action becomes MORE effective, "
         "not less. Without mental noise, decisions are clear. Without result-anxiety, "
         "performance is free. This is why the greatest creative work, the wisest "
         "decisions, and the most courageous actions often arise from a state of "
         "inner stillness. Inner silence and outer excellence go together."),
    ]
    for title, content in inner_silence_chars:
        story.append(colored_box([
            Paragraph(f"<b>◆ {title}</b>", S["section_label"]),
            Paragraph(content, S["highlight_box"]),
        ], CYAN_LIGHT, CYAN_DARK))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("📋  Practical Instructions for Meditation (BG Chapter 6)", S["subtopic"]))
    story.append(colored_box([
        Paragraph("Krishna's Practical Meditation Instructions (BG 6.10-17):", S["section_label"]),
        Paragraph("PLACE: Sit in a clean, secluded place. Not too high, not too low. "
                  "Use a seat of kusha grass, deer skin, and cloth (modern: meditation cushion/chair).", S["bullet"]),
        Paragraph("POSTURE: Hold body, neck, and head in a straight line. Eyes gently "
                  "focused at the tip of the nose or between eyebrows. Neither staring nor closed.", S["bullet"]),
        Paragraph("DIET: Not too much, not too little. BG 6.17: 'Yoga is not for one "
                  "who eats too much or too little, nor for one who sleeps too much or too little.'", S["bullet"]),
        Paragraph("REGULARITY: Practice at the same time daily (traditionally: dawn and dusk). "
                  "Consistency builds the groove (samskara) of meditation faster than intensity.", S["bullet"]),
        Paragraph("OBJECT OF FOCUS: Fix the mind on the Self (Atman) or on God (Krishna). "
                  "When the mind wanders — and it will — gently bring it back without frustration. "
                  "BG 6.26: 'From wherever the mind wanders due to its flickering and unsteady nature, "
                  "one must certainly withdraw it and bring it back under the control of the Self.'", S["bullet"]),
        Paragraph("ATTITUDE: No force, no strain. The Gita recommends 'yukta-cheshta' — "
                  "balanced effort. Neither too tight (suppression) nor too loose (indulgence).", S["bullet"]),
        Paragraph("DURATION: Start with 15-20 minutes. Krishna says even a little practice "
                  "saves from great fear. BG 2.40: 'In this endeavor there is no loss or diminution, "
                  "and a little advancement on this path can protect one from the most dangerous type of fear.'", S["bullet"]),
    ], LIGHT_PURPLE, PURPLE_DARK))

    # ════════════════════════════════════════════════════════════
    # DHYANA YOGA Q&A
    # ════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(header_bar("📝  EXAM QUESTIONS — DHYANA YOGA (All Mark Levels)", S, DEEP_BLUE))
    story.append(Spacer(1, 0.3*cm))

    # 1.5 mark
    dhyana_short = [
        ("What is Dhyana Yoga?",
         "Dhyana Yoga is the yoga of meditation — the systematic practice of calming, "
         "purifying, and mastering the mind to rest in pure inner awareness. Chapter 6 of "
         "the Gita describes it in detail. The mind is first concentrated (dharana), then "
         "flows in sustained meditation (dhyana), culminating in complete absorption (samadhi) "
         "— the state of inner silence and transcendental joy."),
        ("Define meditation in the Gita context.",
         "In the Gita context, meditation (dhyana) is the unbroken flow of attention toward "
         "a single object — the Self (Atman) or God. It is the 6th step in the 8-limb yoga "
         "path, following concentration (dharana). When attention flows without interruption "
         "like oil poured from one vessel to another, that is dhyana. The goal is samadhi — "
         "complete union with the object of meditation."),
        ("What does living in the present mean?",
         "Living in the present means acting with full awareness in THIS moment — not "
         "trapped in past regrets or future anxieties. In Karma Yoga, only the present "
         "moment contains the possibility of action. Krishna's instruction to 'perform "
         "your duty' is always an instruction to act NOW, with complete attention and "
         "without anxiety about results."),
        ("Name the two aspects of the Divine.",
         "The Gita describes the Divine in two aspects: (1) <b>Saguna Brahman</b> — "
         "the Divine with qualities/form (Krishna, Vishnu, Shiva — the personal God "
         "with attributes like compassion, wisdom, power). (2) <b>Nirguna Brahman</b> — "
         "the Divine without qualities/form (the formless, attribute-less absolute "
         "consciousness — the impersonal Absolute). Both are valid and lead to liberation."),
    ]
    for q, a in dhyana_short:
        story.append(colored_box([
            Paragraph(f"<b>Q: {q} [1.5 marks]</b>", S["exam_q"]),
            Paragraph(a, S["exam_a"]),
        ], GRAY_BG, HexColor("#BDBDBD")))
        story.append(Spacer(1, 4))

    story.append(divider(PURPLE_DARK))
    # 5 mark
    story.append(Paragraph("5-Mark Questions:", S["subtopic"]))
    story.append(colored_box([
        Paragraph("Q: How does self-knowledge lead to peace? [5 marks]", S["exam_q"]),
        Paragraph(
            "<b>Introduction:</b> The Gita establishes a direct causal link: self-knowledge "
            "(Atma-Jnana) leads to freedom from fear and grief, which is the foundation of "
            "genuine peace (Shanti).<br/><br/>"
            "<b>Step 1 — Self-Knowledge Removes the Root Cause of Anxiety:</b> All anxiety "
            "arises from identifying with the temporary (body, relationships, possessions, "
            "reputation). When we know ourselves as the eternal Atman — beyond birth, death, "
            "pleasure, and pain — the root cause of anxiety dissolves. There is nothing to "
            "fear when you know yourself as indestructible.<br/><br/>"
            "<b>Step 2 — Desires Naturally Reduce:</b> BG 2.55 — when one abandons all "
            "mental desires and finds contentment within the self alone, that is the Sthita-Prajna. "
            "Self-knowledge reveals that the self is already complete — no external acquisition "
            "is needed for inner fullness. This eliminates craving (the source of all suffering).<br/><br/>"
            "<b>Step 3 — Equanimity Naturally Arises:</b> Knowing the soul is beyond sorrow and "
            "joy, the self-knower becomes equanimous — able to experience life's ups and downs "
            "without being destabilized. This equanimity IS peace — not the peace of numbness, "
            "but the peace of deep, unshakeable clarity.<br/><br/>"
            "<b>Step 4 — Meditation Deepens and Stabilizes Peace:</b> Self-knowledge gained "
            "intellectually through study (jnana) must be stabilized through meditation (dhyana). "
            "Dhyana Yoga takes the intellectual understanding of 'I am the eternal Atman' "
            "and makes it a direct, living experience. This experiential knowledge IS samadhi — "
            "the state of permanent inner peace.<br/><br/>"
            "<b>Conclusion:</b> Self-knowledge leads to peace through a clear sequence: "
            "knowing the eternal self removes fear and craving, which produces equanimity, "
            "which deepens through meditation into the permanent inner silence described "
            "in BG 6.20-22.",
            S["exam_a"]),
    ], LIGHT_BLUE, DEEP_BLUE))
    story.append(Spacer(1, 0.3*cm))

    story.append(colored_box([
        Paragraph("Q: Explain the body-mind-consciousness distinction. [5 marks]", S["exam_q"]),
        Paragraph(
            "<b>Introduction:</b> The Bhagavad Gita, particularly in Sankhya and Dhyana Yoga, "
            "presents a sophisticated three-level understanding of the human being: "
            "Body, Mind, and Consciousness (Soul). Understanding this distinction is "
            "essential for both Karma Yoga and Dhyana Yoga practice.<br/><br/>"
            "<b>1. The Body (Sthula Sharira — Gross Body):</b> The physical body composed of "
            "five elements (earth, water, fire, air, space). It is temporary, changing, and "
            "ultimately dissolved at death. The body is the outermost layer (kosha) — the "
            "tool through which the soul interacts with the world. "
            "Gita teaching: The body is like a garment — it can be worn and discarded. "
            "Don't misidentify yourself as the body.<br/><br/>"
            "<b>2. The Mind (Sukshma Sharira — Subtle Body):</b> The mind includes Manas "
            "(processing mind), Buddhi (intellect/discriminating intelligence), Ahamkara "
            "(ego/sense of 'I'), and Chitta (memory/subconscious storehouse). It survives "
            "the death of the gross body and carries karmic impressions (samskaras) into "
            "the next life. Dhyana Yoga specifically works on purifying and stilling the mind.<br/><br/>"
            "<b>3. Consciousness (Atman/Soul):</b> The eternal, pure awareness that animates "
            "both body and mind. It is the witness (sakshi) — the one who sees without being "
            "seen, knows without being known. It is unborn, undying, unchanging. "
            "All yoga practices ultimately aim at the direct EXPERIENCE of this consciousness.<br/><br/>"
            "<b>Practical Implication:</b> Meditation works progressively through these layers: "
            "first stilling the body (asana), then calming the mind (pranayama, pratyahara, "
            "dharana, dhyana), until pure consciousness (Atman) shines in its own glory as "
            "inner silence. The meditator realizes: 'I am not the body, not the mind — "
            "I am the pure consciousness witnessing all.'",
            S["exam_a"]),
    ], LIGHT_PURPLE, PURPLE_DARK))

    # 15 mark Dhyana Yoga
    story.append(PageBreak())
    story.append(header_bar("📝  15-MARK: DHYANA YOGA — FULL ANSWER", S, TEAL))
    story.append(Spacer(1, 0.2*cm))
    story.append(colored_box([
        Paragraph("Q: Describe the essence and practice of Dhyana Yoga. How does tuning the mind help in achieving inner silence? [15 marks]", S["exam_q"]),
    ], GRAY_BG, TEAL))
    story.append(Spacer(1, 4))

    dhyana_15 = [
        ("INTRODUCTION — What is Dhyana Yoga?",
         "Dhyana Yoga (Chapter 6 of the Bhagavad Gita, also called Atma-Samyama Yoga — Yoga of "
         "Self-Restraint) is the systematic science and art of meditation. 'Dhyana' means "
         "unbroken, sustained attention — like oil flowing from one vessel to another without "
         "interruption. Krishna dedicates an entire chapter to this because, while Karma Yoga "
         "purifies the mind through righteous action, Dhyana Yoga completes the purification "
         "by bringing the mind to perfect stillness — Inner Silence. The ultimate goal is "
         "Samadhi: complete absorption in the Self, the state of transcendental peace and joy.",
         LIGHT_BLUE, DEEP_BLUE),
        ("ESSENCE OF DHYANA YOGA — BG 6.5 (The Core Teaching):",
         "The most important verse of Dhyana Yoga: BG 6.5 — 'One must elevate oneself by one's "
         "own mind, and not degrade oneself. The mind is the friend of the conditioned soul, "
         "and his enemy as well.' This captures the essence: YOU are responsible for your mind. "
         "The mind in its untrained state is the greatest enemy — restless, scattered, addicted "
         "to sense pleasure, driven by fear. The mind in its trained state is the greatest friend — "
         "a clear, focused instrument that reveals truth and produces peace.",
         CREAM, DARK_GOLD),
        ("TUNING THE MIND — QUANTITY, QUALITY AND DIRECTION OF THOUGHTS:",
         "Dhyana Yoga tunes the mind across THREE dimensions:<br/>"
         "(A) QUANTITY: BG 6.34-35 — The mind generates thousands of repetitive, negative "
         "thoughts daily. Abhyasa (regular practice) and Vairagya (detachment) reduce this "
         "mental noise. Concentration on a single object (dharana) focuses the scattered mind.<br/>"
         "(B) QUALITY: The Gita (through the Trigunas) shows thought quality ranges from "
         "tamasic (dark/depressive), through rajasic (restless/craving), to sattvic "
         "(clear/compassionate). Meditation, good company (satsanga), scripture study, and "
         "mantra systematically upgrade thought quality from tamas/rajas to sattva.<br/>"
         "(C) DIRECTION: The untrained mind is 'bahirmukhi' (outward-facing) — always seeking "
         "happiness in external objects. Pratyahara (sense-withdrawal) turns the mind "
         "INWARD (antarmukhi). The final direction is toward God/Atman — the source of "
         "all peace and joy. BG 6.14: 'Let him sit thinking of Me and having Me as the supreme goal.'",
         LIGHT_GREEN, DARK_GREEN),
        ("STEP-BY-STEP PRACTICE (BG Chapter 6 Instructions):",
         "Krishna gives remarkably practical instructions: "
         "PLACE: Clean, quiet, secluded. Neither too high nor too low. "
         "POSTURE (BG 6.13): Body/neck/head straight. Eyes softly focused. "
         "DIET (BG 6.17): Balanced — not excessive or deficient in food, sleep, or activity. "
         "TIMING: Regular practice at same time. Consistency over intensity. "
         "FOCUS: Fix attention on the Self or God. "
         "WHEN MIND WANDERS (BG 6.26): 'From wherever the mind wanders, bring it back "
         "to the Self.' Not with frustration — gently, patiently, repeatedly. "
         "ATTITUDE: Neither too tight (suppression) nor too loose (indulgence). "
         "Balanced effort — yukta-cheshta.",
         LIGHT_ORANGE, SAFFRON),
        ("THE PROGRESSIVE JOURNEY TO INNER SILENCE:",
         "Inner silence is reached progressively through the eight limbs of yoga: "
         "Ethical living (Yama/Niyama) creates a foundation of mental peace. "
         "Asana (physical stillness) reduces gross agitation. "
         "Pranayama (breath regulation) — slow breath = slow mind. "
         "Pratyahara (sense withdrawal) stops external stimuli from feeding thoughts. "
         "Dharana (concentration) narrows the mind to one focus. "
         "Dhyana (sustained meditation) — observer and object begin to merge. "
         "Samadhi — the final state: no subject-object division; pure awareness; "
         "transcendental joy; THIS is Inner Silence.",
         LIGHT_PURPLE, PURPLE_DARK),
        ("WHAT INNER SILENCE ACTUALLY IS (BG 6.20-22):",
         "BG 6.20-22 beautifully describes Inner Silence: mind restrained from material "
         "activities; ability to see the self by the pure mind; relishing joy IN the self; "
         "boundless transcendental happiness; established in truth; 'there is no greater gain.' "
         "Inner Silence is: NOT emptiness but fullness, NOT numbness but heightened awareness, "
         "NOT absence but the most profound presence, NOT passive but the source of most "
         "effective action. The ocean metaphor: surface has waves (activity), depths are "
         "always still (inner silence). The yogi lives at the depth while engaging the surface.",
         CYAN_LIGHT, CYAN_DARK),
        ("MODERN SCIENCE VALIDATION AND CONCLUSION:",
         "Modern neuroscience validates Dhyana Yoga: Regular meditation increases gray matter "
         "density in prefrontal cortex (focus, decision-making), reduces amygdala reactivity "
         "(fear, anger), increases anterior insula activity (self-awareness), and strengthens "
         "default mode network regulation (reduces mind-wandering). Dr. Herbert Benson (Harvard) "
         "calls meditation 'the relaxation response' — physiologically opposite to the stress "
         "response. Long-term meditators show measurable changes in brain structure and function "
         "consistent with the states the Gita describes. Dhyana Yoga, therefore, is both "
         "ancient wisdom AND cutting-edge neuroscience. Its practice of tuning the mind — "
         "reducing quantity of thoughts, improving their quality, and redirecting them inward "
         "toward the Divine — is the most reliable path to the Inner Silence that the human "
         "soul has always sought.",
         LIGHT_GREEN, DARK_GREEN),
    ]
    for label, text, bg, border in dhyana_15:
        story.append(colored_box([
            Paragraph(f"<b>{label}</b>", S["section_label"]),
            Paragraph(text, S["exam_a"]),
        ], bg, border))
        story.append(Spacer(1, 4))

    # 10 mark - Compare
    story.append(PageBreak())
    story.append(header_bar("📝  10-MARK: COMPARE BHAKTI, KARMA, DHYANA YOGA", S, INDIGO))
    story.append(Spacer(1, 0.2*cm))
    story.append(colored_box([
        Paragraph("Q: Compare Bhakti, Karma, Dhyana Yoga. [15 marks / 10 marks]", S["exam_q"]),
    ], GRAY_BG, INDIGO))
    story.append(Spacer(1, 4))

    compare_yoga = [
        [Paragraph("<b>Aspect</b>",S["table_head"]),
         Paragraph("<b>Karma Yoga</b>",S["table_head"]),
         Paragraph("<b>Dhyana Yoga</b>",S["table_head"]),
         Paragraph("<b>Bhakti Yoga</b>",S["table_head"])],
        [Paragraph("Meaning",S["table_cell"]),
         Paragraph("Yoga of Action",S["table_cell"]),
         Paragraph("Yoga of Meditation",S["table_cell"]),
         Paragraph("Yoga of Devotion",S["table_cell"])],
        [Paragraph("Main Chapter",S["table_cell"]),
         Paragraph("Chapter 3, 4",S["table_cell"]),
         Paragraph("Chapter 6",S["table_cell"]),
         Paragraph("Chapter 12",S["table_cell"])],
        [Paragraph("Core Teaching",S["table_cell"]),
         Paragraph("Act without ego-attachment to results",S["table_cell"]),
         Paragraph("Calm the mind through meditation",S["table_cell"]),
         Paragraph("Love and surrender to God",S["table_cell"])],
        [Paragraph("Primary Path",S["table_cell"]),
         Paragraph("Through DOING",S["table_cell"]),
         Paragraph("Through BEING STILL",S["table_cell"]),
         Paragraph("Through LOVING",S["table_cell"])],
        [Paragraph("Main Tool",S["table_cell"]),
         Paragraph("Righteous work, Swadharma",S["table_cell"]),
         Paragraph("Meditation, concentration",S["table_cell"]),
         Paragraph("Prayer, chanting, worship",S["table_cell"])],
        [Paragraph("Obstacle to Overcome",S["table_cell"]),
         Paragraph("Desire for rewards, ego",S["table_cell"]),
         Paragraph("Restless, scattered mind",S["table_cell"]),
         Paragraph("Self-centeredness, pride",S["table_cell"])],
        [Paragraph("Who Is It For?",S["table_cell"]),
         Paragraph("Active temperament (Kshatriya/Vaishya nature)",S["table_cell"]),
         Paragraph("Introspective/Intellectual nature",S["table_cell"]),
         Paragraph("Emotional/Devotional temperament",S["table_cell"])],
        [Paragraph("Key Verse",S["table_cell"]),
         Paragraph("BG 2.47",S["table_cell"]),
         Paragraph("BG 6.5, 6.35",S["table_cell"]),
         Paragraph("BG 12.13-14",S["table_cell"])],
        [Paragraph("Goal",S["table_cell"]),
         Paragraph("Liberation through selfless work",S["table_cell"]),
         Paragraph("Liberation through inner silence/samadhi",S["table_cell"]),
         Paragraph("Liberation through love and surrender",S["table_cell"])],
        [Paragraph("Modern Parallel",S["table_cell"]),
         Paragraph("Flow state, process focus, mindful work",S["table_cell"]),
         Paragraph("Mindfulness meditation, MBSR",S["table_cell"]),
         Paragraph("Positive psychology, gratitude practice",S["table_cell"])],
    ]
    cyt = Table(compare_yoga, colWidths=[3*cm, 4.5*cm, 4.5*cm, 4.5*cm])
    cyt.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),INDIGO),
        ("BACKGROUND",(0,1),(-1,1),CREAM),
        ("BACKGROUND",(0,2),(-1,2),LIGHT_BLUE),
        ("BACKGROUND",(0,3),(-1,3),CREAM),
        ("BACKGROUND",(0,4),(-1,4),LIGHT_BLUE),
        ("BACKGROUND",(0,5),(-1,5),CREAM),
        ("BACKGROUND",(0,6),(-1,6),LIGHT_BLUE),
        ("BACKGROUND",(0,7),(-1,7),CREAM),
        ("BACKGROUND",(0,8),(-1,8),LIGHT_BLUE),
        ("BACKGROUND",(0,9),(-1,9),CREAM),
        ("BACKGROUND",(0,10),(-1,10),LIGHT_BLUE),
        ("GRID",(0,0),(-1,-1),0.5,HexColor("#90A4AE")),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),6),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    story.append(cyt)
    story.append(Spacer(1, 0.3*cm))

    story.append(colored_box([
        Paragraph("KEY INSIGHT — The Three Yogas Are ONE Path:", S["section_label"]),
        Paragraph(
            "The Gita does not present these as competing paths — they are three aspects of "
            "the ONE complete yogic life. Krishna says in BG 5.4-5: 'Only the ignorant speak "
            "of Karma Yoga and Sankhya (Jnana) Yoga as different. Those truly learned say that "
            "one who applies oneself to either path obtains the results of both.'<br/><br/>"
            "In practice: A person acts in the world with Karma Yoga (non-attached, dutiful action), "
            "worships and loves God with Bhakti Yoga (devotion, surrender), and meditates daily "
            "with Dhyana Yoga (inner stillness). Together they form the complete spiritual life "
            "that the Gita envisions. All three ultimately lead to the same destination: "
            "liberation (moksha) and permanent peace (shanti).",
            S["highlight_box"]),
    ], LIGHT_PURPLE, PURPLE_DARK))

    # ════════════════════════════════════════════════════════════
    # FINAL RAPID REVISION TABLE
    # ════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(header_bar("⚡  RAPID REVISION — MODULE 2 MASTER SUMMARY", S, TEAL))
    story.append(Spacer(1, 0.3*cm))

    rev_data = [
        [Paragraph("<b>Topic</b>",S["table_head"]),
         Paragraph("<b>Core Concept</b>",S["table_head"]),
         Paragraph("<b>Key Verse</b>",S["table_head"]),
         Paragraph("<b>Exam %</b>",S["table_head"])],
        [Paragraph("Karma Yoga",S["table_cell"]),
         Paragraph("Action without ego-attachment; 3 pillars: do duty / no claim on results / no inaction",S["table_cell"]),
         Paragraph("BG 2.47, 3.19, 4.18",S["table_cell"]),
         Paragraph("90%",S["table_cell"])],
        [Paragraph("Nishkama Karma",S["table_cell"]),
         Paragraph("Dedicated action without anxiety over results; 100% effort + 0% result-anxiety",S["table_cell"]),
         Paragraph("BG 2.47, 3.19",S["table_cell"]),
         Paragraph("95%",S["table_cell"])],
        [Paragraph("Living in Present",S["table_cell"]),
         Paragraph("Only present moment has action; past=grief, future=anxiety, present=yoga",S["table_cell"]),
         Paragraph("BG 2.47",S["table_cell"]),
         Paragraph("80%",S["table_cell"])],
        [Paragraph("Swadharma",S["table_cell"]),
         Paragraph("Own duty by nature/role/stage; better imperfect own duty than perfect others'",S["table_cell"]),
         Paragraph("BG 3.35, 4.13",S["table_cell"]),
         Paragraph("90%",S["table_cell"])],
        [Paragraph("Dhyana Yoga",S["table_cell"]),
         Paragraph("Meditation; mind = friend or enemy (BG 6.5); abhyasa + vairagya",S["table_cell"]),
         Paragraph("BG 6.5, 6.35",S["table_cell"]),
         Paragraph("85%",S["table_cell"])],
        [Paragraph("Qty of Thoughts",S["table_cell"]),
         Paragraph("Mind too restless; solution: abhyasa (practice) + vairagya (detachment)",S["table_cell"]),
         Paragraph("BG 6.34-35",S["table_cell"]),
         Paragraph("90%",S["table_cell"])],
        [Paragraph("Quality of Thoughts",S["table_cell"]),
         Paragraph("Tamas (dark) -> Rajas (restless) -> Sattva (clear); meditation upgrades quality",S["table_cell"]),
         Paragraph("BG 17.16, 2.62-63",S["table_cell"]),
         Paragraph("90%",S["table_cell"])],
        [Paragraph("Direction of Thoughts",S["table_cell"]),
         Paragraph("Bahirmukhi (outward) -> Antarmukhi (inward) -> toward God; pratyahara",S["table_cell"]),
         Paragraph("BG 6.14, 2.58",S["table_cell"]),
         Paragraph("90%",S["table_cell"])],
        [Paragraph("Inner Silence",S["table_cell"]),
         Paragraph("Samadhi: pure awareness, no subject-object division, boundless joy (BG 6.20-22)",S["table_cell"]),
         Paragraph("BG 6.20-22",S["table_cell"]),
         Paragraph("85%",S["table_cell"])],
    ]
    rt = Table(rev_data, colWidths=[3*cm, 7*cm, 3.5*cm, 3*cm])
    rt.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),TEAL),
        ("BACKGROUND",(0,1),(-1,1),LIGHT_ORANGE),
        ("BACKGROUND",(0,2),(-1,2),CREAM),
        ("BACKGROUND",(0,3),(-1,3),LIGHT_ORANGE),
        ("BACKGROUND",(0,4),(-1,4),CREAM),
        ("BACKGROUND",(0,5),(-1,5),LIGHT_ORANGE),
        ("BACKGROUND",(0,6),(-1,6),CREAM),
        ("BACKGROUND",(0,7),(-1,7),LIGHT_ORANGE),
        ("BACKGROUND",(0,8),(-1,8),CREAM),
        ("BACKGROUND",(0,9),(-1,9),LIGHT_ORANGE),
        ("GRID",(0,0),(-1,-1),0.5,HexColor("#80CBC4")),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),6),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    story.append(rt)
    story.append(Spacer(1, 0.4*cm))

    # ALL 1.5 mark summary
    story.append(Paragraph("📌  ALL LIKELY 1.5-MARK QUESTIONS AT A GLANCE — MODULE 2", S["subtopic"]))
    all_short = [
        ("What is Karma Yoga?", "Yoga of selfless action. Perform duty without attachment to results (BG 2.47). Three instructions: act, no claim on fruits, no excuse for inaction."),
        ("What is Dhyana Yoga?", "Yoga of meditation. Systematic training of mind from restlessness to inner silence. Abhyasa + vairagya are the keys (BG 6.35)."),
        ("What is Nishkama Karma?", "Nish = without, Kama = desire. Dedicated action without craving for results. 100% effort + 0% result-anxiety = peak performance + inner peace."),
        ("What is Swadharma?", "One's own duty based on nature, role, stage of life. Better imperfect own duty than perfect others'. Authentic calling (BG 3.35)."),
        ("What does living in the present mean?", "Full engagement in THIS moment — not past regrets or future anxieties. Only present contains action. Karma Yoga is always present-moment yoga."),
        ("What is the role of intention in Karma Yoga?", "Intention (sankalpa) determines spiritual quality of action. Selfish intent = binding karma. Offering action to God without craving = liberating Karma Yoga."),
        ("What is Dhyana Yoga / Define meditation in Gita context?", "Unbroken flow of attention toward Atman or God. Leads from dharana (concentration) through dhyana to samadhi (inner silence). BG 6.10-26."),
        ("Name the two aspects of the Divine.", "Saguna Brahman (personal God with qualities — Krishna) and Nirguna Brahman (formless, attribute-less Absolute). Both lead to liberation."),
        ("What is meant by Quantity, Quality, Direction of thoughts?", "Qty = mind thinks too many thoughts (solution: abhyasa); Quality = thoughts range from tamas to sattva (solution: meditation, satsanga); Direction = outward to inward to Divine (solution: pratyahara, focus on God)."),
        ("What is Inner Silence?", "Samadhi — state of pure, boundless awareness beyond thought-activity. Transcendental joy. Observer merged with object. Described in BG 6.20-22 as the highest state."),
    ]
    for q, a in all_short:
        story.append(colored_box([
            Paragraph(f"<b>Q: {q}</b>", S["exam_q"]),
            Paragraph(a, S["exam_a"]),
        ], GRAY_BG, HexColor("#BDBDBD")))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 0.3*cm))
    story.append(colored_box([
        Paragraph("📖  STUDY TIPS FOR MODULE 2:", S["section_label"]),
        Paragraph("TOP 3 most likely long questions: (1) Dhyana Yoga + Inner Silence 15-mark, "
                  "(2) Karma Yoga + Swadharma 10-mark, (3) Compare three Yogas. "
                  "Always remember BG 2.47 for any Karma Yoga question — it is THE most important verse. "
                  "For Dhyana Yoga: remember BG 6.5 (mind = friend/enemy) and BG 6.35 (abhyasa + vairagya). "
                  "Use modern examples: sports psychology for Karma Yoga; neuroscience for Dhyana Yoga. "
                  "Structure long answers: Introduction + numbered sections + conclusion. "
                  "The examiner wants to see you APPLY the concept to modern life — always add a practical dimension.", S["highlight_box"]),
    ], LIGHT_ORANGE, DARK_SAFFRON))

    # footer
    story.append(Spacer(1, 0.4*cm))
    story.append(HRFlowable(width="100%", thickness=2, color=SAFFRON))
    story.append(Spacer(1, 0.2*cm))
    footer_data = [[
        Paragraph("<b>MODULE 2 COMPLETE</b> | AC-02-23 Message of Bhagavad Gita", S["note"]),
        Paragraph("<b>Share Module 3 Syllabus for Bhakti Yoga + Gunatraya Vibhaga Yoga Notes!</b>",
                  ParagraphStyle("fn", fontName="Helvetica-Bold", fontSize=9.5,
                                 textColor=DARK_SAFFRON, alignment=TA_CENTER)),
    ]]
    ft = Table(footer_data, colWidths=[9*cm, 7.5*cm])
    ft.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),4),
    ]))
    story.append(ft)

    return story


def main():
    out = "Gita_Module2_ExamNotes.pdf"
    doc = SimpleDocTemplate(
        out, pagesize=A4,
        rightMargin=1.8*cm, leftMargin=1.8*cm,
        topMargin=1.5*cm, bottomMargin=1.5*cm,
        title="Message of Bhagavad Gita — Module 2 Exam Notes",
        author="AC-02-23 Study Guide",
    )
    styles = build_styles()
    story  = build_content(styles)
    doc.build(story)
    print(f"PDF created: {out}")

if __name__ == "__main__":
    main()

# python /home/claude/gita_module2_notes.py 







