from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from xml.sax.saxutils import escape

DARK_BLUE    = colors.HexColor('#0d1b4b')
MED_BLUE     = colors.HexColor('#1a3a6b')
ACCENT_BLUE  = colors.HexColor('#1565c0')
LIGHT_BLUE   = colors.HexColor('#e3f2fd')
TEAL         = colors.HexColor('#00695c')
LIGHT_TEAL   = colors.HexColor('#e0f2f1')
RED          = colors.HexColor('#b71c1c')
LIGHT_RED    = colors.HexColor('#ffebee')
ORANGE       = colors.HexColor('#e65100')
LIGHT_ORANGE = colors.HexColor('#fff3e0')
PURPLE       = colors.HexColor('#4a148c')
LIGHT_PURPLE = colors.HexColor('#f3e5f5')
GREEN        = colors.HexColor('#1b5e20')
LIGHT_GREEN  = colors.HexColor('#e8f5e9')
YELLOW_BG    = colors.HexColor('#fffde7')
DARK_GRAY    = colors.HexColor('#212121')
MED_GRAY     = colors.HexColor('#424242')
LIGHT_GRAY   = colors.HexColor('#f5f5f5')
CODE_BG      = colors.HexColor('#1e1e2e')
CODE_TEXT    = colors.HexColor('#cdd6f4')
WHITE        = colors.white
GOLD         = colors.HexColor('#ffcc02')
W, H = A4

def S(name):
    styles = {
        'cover_title': ParagraphStyle('ct', fontName='Helvetica-Bold', fontSize=26,
            textColor=WHITE, alignment=TA_CENTER, spaceAfter=6, leading=32),
        'cover_sub': ParagraphStyle('cs', fontName='Helvetica', fontSize=12,
            textColor=colors.HexColor('#bbdefb'), alignment=TA_CENTER, spaceAfter=4, leading=17),
        'cover_code': ParagraphStyle('cc', fontName='Helvetica-Bold', fontSize=11,
            textColor=GOLD, alignment=TA_CENTER, spaceAfter=4),
        'module_banner': ParagraphStyle('mb', fontName='Helvetica-Bold', fontSize=17,
            textColor=WHITE, alignment=TA_CENTER, spaceAfter=4, leading=22),
        'topic_hdr': ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=14,
            textColor=WHITE, alignment=TA_LEFT, spaceAfter=2, leading=20, leftIndent=8),
        'subtopic': ParagraphStyle('st', fontName='Helvetica-Bold', fontSize=11,
            textColor=DARK_BLUE, spaceBefore=10, spaceAfter=4, leading=15),
        'body': ParagraphStyle('bd', fontName='Helvetica', fontSize=9.5,
            textColor=DARK_GRAY, spaceBefore=3, spaceAfter=3, leading=14, alignment=TA_JUSTIFY),
        'body_bold': ParagraphStyle('bb', fontName='Helvetica-Bold', fontSize=9.5,
            textColor=MED_GRAY, spaceBefore=2, spaceAfter=2, leading=14),
        'bullet': ParagraphStyle('bu', fontName='Helvetica', fontSize=9.5,
            textColor=DARK_GRAY, spaceBefore=2, spaceAfter=2, leading=14,
            leftIndent=14, firstLineIndent=-10),
        'code': ParagraphStyle('co', fontName='Courier', fontSize=8.2,
            textColor=CODE_TEXT, spaceBefore=1, spaceAfter=1, leading=12, leftIndent=6),
        'q_hdr': ParagraphStyle('qh', fontName='Helvetica-Bold', fontSize=10,
            textColor=TEAL, spaceBefore=8, spaceAfter=3, leading=14),
        'ans': ParagraphStyle('an', fontName='Helvetica', fontSize=9.5,
            textColor=DARK_GRAY, spaceBefore=2, spaceAfter=2, leading=14,
            alignment=TA_JUSTIFY, leftIndent=8),
        'note': ParagraphStyle('no', fontName='Helvetica-BoldOblique', fontSize=9,
            textColor=RED, spaceBefore=4, spaceAfter=4, leading=13, leftIndent=8),
        'toc_item': ParagraphStyle('ti', fontName='Helvetica', fontSize=10,
            textColor=MED_BLUE, spaceBefore=3, spaceAfter=3, leading=14, leftIndent=10),
        'toc_title': ParagraphStyle('tt', fontName='Helvetica-Bold', fontSize=14,
            textColor=DARK_BLUE, spaceBefore=0, spaceAfter=8, alignment=TA_CENTER),
        'tip': ParagraphStyle('tp', fontName='Helvetica-Oblique', fontSize=9,
            textColor=PURPLE, spaceBefore=3, spaceAfter=3, leading=13, leftIndent=8),
    }
    return styles[name]

def hr(color=ACCENT_BLUE, t=1):
    return HRFlowable(width='100%', thickness=t, color=color, spaceAfter=4, spaceBefore=4)

def vs(h=6): return Spacer(1, h)

def cbox(text, bg=LIGHT_BLUE, border=ACCENT_BLUE, sty='body'):
    t = Table([[Paragraph(text, S(sty))]], colWidths=[W-4*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),bg),('BOX',(0,0),(-1,-1),1,border),
        ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
    ]))
    return t

def cblock(lines):
    safe = []
    for l in lines:
        l2 = l.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
        safe.append([Paragraph(l2, S('code'))])
    t = Table(safe, colWidths=[W-4*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),CODE_BG),
        ('BOX',(0,0),(-1,-1),1,colors.HexColor('#45475a')),
        ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
    ]))
    return t

def topic_box(num, title, pct):
    rp = ParagraphStyle('rp', fontName='Helvetica-Bold', fontSize=10, textColor=GOLD, alignment=TA_LEFT)
    t = Table([[Paragraph(f'TOPIC {num}: {title}', S('topic_hdr')),
                Paragraph(f'* Exam Probability: {pct}%', rp)]],
              colWidths=[W-5.5*cm, 3.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),DARK_BLUE),
        ('LEFTPADDING',(0,0),(0,-1),12),('RIGHTPADDING',(-1,0),(-1,-1),10),
        ('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ]))
    return t

def qa(marks, question, paras):
    mc = {1.5:(LIGHT_TEAL,TEAL), 5:(LIGHT_ORANGE,ORANGE),
          10:(LIGHT_PURPLE,PURPLE), 15:(LIGHT_RED,RED)}
    bg, border = mc.get(marks, (LIGHT_GRAY, MED_GRAY))
    ml = {1.5:'SHORT (1.5 Marks | ~50 words)', 5:'MEDIUM (5 Marks | 300-500 words)',
          10:'LONG (10 Marks | 500-700 words)', 15:'ESSAY (15 Marks | 700-1000 words)'}
    label = ml.get(marks, f'{marks} Marks')
    qt = Table([[Paragraph(f'<b>Q [{label}]:</b> {question}', S('q_hdr'))]], colWidths=[W-4*cm])
    qt.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),bg),('BOX',(0,0),(-1,-1),1.5,border),
        ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
    ]))
    return [qt] + paras + [vs(4)]

def stbl(headers, rows, cw=None):
    if cw is None:
        cw = [(W-4*cm)/len(headers)]*len(headers)
    data = [[Paragraph(f'<b>{h}</b>', S('body_bold')) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), S('body')) for c in row])
    t = Table(data, colWidths=cw)
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),DARK_BLUE),('TEXTCOLOR',(0,0),(-1,0),WHITE),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,0),9),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,LIGHT_GRAY]),
        ('BOX',(0,0),(-1,-1),1,ACCENT_BLUE),
        ('INNERGRID',(0,0),(-1,-1),0.5,colors.HexColor('#b0bec5')),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ]))
    return t

# ═══════════════════════════════════════════════════════════════════
def build():
    doc = SimpleDocTemplate('Module3_Statistics_ExamNotes.pdf',
        pagesize=A4, leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm)
    story = []

    # ── COVER ──────────────────────────────────────────────────────
    story.append(vs(45))
    ct = Table([[Paragraph('DATA ANALYTICS USING PYTHON', S('cover_title'))]], colWidths=[W-4*cm])
    ct.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),DARK_BLUE),
        ('TOPPADDING',(0,0),(-1,-1),22),('BOTTOMPADDING',(0,0),(-1,-1),22),
        ('LEFTPADDING',(0,0),(-1,-1),20)]))
    story.append(ct); story.append(vs(10))

    it = Table([
        [Paragraph('CODE: PCC-IT-601-A-2024', S('cover_code'))],
        [Paragraph('B.Tech 6th Semester  |  Maximum Marks: 75', S('cover_sub'))],
        [Paragraph('MODULE 3 — INTRODUCTION TO DATA ANALYTICS', S('cover_sub'))],
        [Paragraph('Statistics, Probability, Hypothesis Testing, ANOVA, Chi-Square', S('cover_sub'))],
        [Paragraph('Complete Exam Notes with All Questions and Answers', S('cover_sub'))],
    ], colWidths=[W-4*cm])
    it.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),MED_BLUE),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),16)]))
    story.append(it); story.append(vs(18))

    tg = Table([
        [Paragraph('1. Descriptive Statistics (12%)', S('cover_sub')),
         Paragraph('2. Probability Distributions (12%)', S('cover_sub')),
         Paragraph('3. Inferential Statistics (10%)', S('cover_sub'))],
        [Paragraph('4. Hypothesis Testing (15%)', S('cover_sub')),
         Paragraph('5. Two-Sample Testing (10%)', S('cover_sub')),
         Paragraph('6. One-Way ANOVA (12%)', S('cover_sub'))],
        [Paragraph('7. Two-Way ANOVA (10%)', S('cover_sub')),
         Paragraph('8. Permutation Tests (8%)', S('cover_sub')),
         Paragraph('9. Chi-Square Test (11%)', S('cover_sub'))],
    ], colWidths=[(W-4*cm)/3]*3)
    tg.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#0d1b5e')),
        ('TEXTCOLOR',(0,0),(-1,-1),WHITE),
        ('BOX',(0,0),(-1,-1),1,colors.HexColor('#5c6bc0')),
        ('INNERGRID',(0,0),(-1,-1),0.5,colors.HexColor('#3949ab')),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LEFTPADDING',(0,0),(-1,-1),6),('ALIGN',(0,0),(-1,-1),'CENTER'),
    ]))
    story.append(tg); story.append(vs(26))
    story.append(Paragraph(
        'TOP PRIORITY: Hypothesis Testing (15%) | Descriptive Stats (12%) | '
        'Probability Distributions (12%) | One-Way ANOVA (12%) | Chi-Square (11%)',
        S('note')))
    story.append(PageBreak())

    # ── TOC ────────────────────────────────────────────────────────
    story.append(Paragraph('TABLE OF CONTENTS', S('toc_title')))
    story.append(hr(DARK_BLUE, 2)); story.append(vs(6))
    for num, title, pct in [
        ('TOPIC 1','DESCRIPTIVE STATISTICS','12%'),
        ('TOPIC 2','PROBABILITY DISTRIBUTIONS','12%'),
        ('TOPIC 3','INFERENTIAL STATISTICS — OVERVIEW','10%'),
        ('TOPIC 4','HYPOTHESIS TESTING — COMPLETE GUIDE','15%'),
        ('TOPIC 5','TWO-SAMPLE TESTING','10%'),
        ('TOPIC 6','ONE-WAY ANOVA','12%'),
        ('TOPIC 7','TWO-WAY ANOVA','10%'),
        ('TOPIC 8','PERMUTATION AND RANDOMIZATION TEST','8%'),
        ('TOPIC 9','CHI-SQUARE TEST','11%'),
    ]:
        rt = Table([[Paragraph(f'<b>{num}</b>',S('toc_item')),
                     Paragraph(title,S('toc_item')),
                     Paragraph(f'<b>{pct}</b>',S('toc_item'))]],
                   colWidths=[2.5*cm, W-7.5*cm, 2*cm])
        rt.setStyle(TableStyle([('LINEBELOW',(0,0),(-1,-1),0.5,colors.HexColor('#bbdefb')),
            ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)]))
        story.append(rt)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # TOPIC 1: DESCRIPTIVE STATISTICS
    # ══════════════════════════════════════════════════════════════
    story.append(topic_box(1,'DESCRIPTIVE STATISTICS',12))
    story.append(vs(8))
    story.append(Paragraph('What is Descriptive Statistics?', S('subtopic')))
    story.append(Paragraph(
        '<b>Descriptive statistics</b> is the branch of statistics that deals with '
        '<b>summarizing, organizing, and presenting data</b> in a meaningful way. '
        'It describes the basic features of data — its central tendency, spread, and shape — '
        'WITHOUT drawing any conclusions beyond the data itself. '
        'It answers: "What does the data look like?" '
        'It is the first step in any data analytics project.', S('body')))
    story.append(vs(4))
    story.append(cbox(
        'KEY DIVISION: Descriptive stats DESCRIBES data. '
        'Inferential stats DRAWS CONCLUSIONS from data. '
        'Descriptive stats = measures of central tendency + measures of spread + shape measures.',
        LIGHT_BLUE, ACCENT_BLUE))
    story.append(vs(6))

    story.append(Paragraph('Measures of Central Tendency', S('subtopic')))
    story.append(Paragraph(
        'Measures of central tendency describe the <b>center/typical value</b> of a dataset. '
        'The three main measures are Mean, Median, and Mode.', S('body')))
    story.append(stbl(
        ['Measure','Formula / Definition','Best Used When','Affected by Outliers?'],
        [
            ['Mean (Average)','Sum of all values / Number of values. x-bar = (x1+x2+...+xn)/n',
             'Data is symmetric, no extreme outliers','Yes — highly sensitive'],
            ['Median','Middle value when data is sorted. If n is even: average of two middle values',
             'Data has outliers or is skewed','No — robust to outliers'],
            ['Mode','Most frequently occurring value. A dataset can have no mode, one mode, or multiple modes',
             'Categorical data, finding most common value','No'],
            ['Weighted Mean','Sum(wi*xi) / Sum(wi) — each value has a weight',
             'Values have different importance/frequency','Yes'],
            ['Geometric Mean','(x1*x2*...*xn)^(1/n) — nth root of product',
             'Growth rates, ratios, financial returns','Less than arithmetic mean'],
        ],
        [2.5*cm, 4.5*cm, 3.5*cm, 3.5*cm]
    ))
    story.append(vs(6))

    story.append(Paragraph('Measures of Spread (Dispersion)', S('subtopic')))
    story.append(Paragraph(
        'Measures of dispersion describe how <b>spread out</b> the data is around the central value.',S('body')))
    story.append(stbl(
        ['Measure','Formula','Interpretation'],
        [
            ['Range','Max - Min','Simple but sensitive to outliers'],
            ['Variance (s2)','Sum((xi - mean)^2) / (n-1) for sample','Average squared deviation from mean'],
            ['Standard Deviation (s)','sqrt(Variance)','Same units as data. Most used spread measure'],
            ['Coefficient of Variation','(Std Dev / Mean) x 100%','Relative spread — compare datasets of different units'],
            ['Interquartile Range (IQR)','Q3 - Q1 (middle 50% spread)','Robust to outliers. Used in boxplots'],
            ['Mean Absolute Deviation','Sum(|xi - mean|) / n','Average absolute distance from mean'],
            ['Skewness','Measure of asymmetry of distribution','0=symmetric, positive=right skew, negative=left skew'],
            ['Kurtosis','Measure of tail heaviness','3=normal, >3=heavy tails, <3=light tails'],
        ],
        [3.5*cm, 5*cm, 6.5*cm]
    ))
    story.append(vs(6))

    story.append(Paragraph('Five-Number Summary and Quartiles', S('subtopic')))
    story.append(Paragraph(
        'The <b>five-number summary</b> provides a complete picture of data distribution: '
        '<b>Min, Q1, Median (Q2), Q3, Max</b>. '
        'Q1 = 25th percentile (lower quartile), Q2 = 50th percentile (median), '
        'Q3 = 75th percentile (upper quartile). '
        'IQR = Q3 - Q1. '
        'Outlier boundaries: below Q1 - 1.5*IQR or above Q3 + 1.5*IQR.', S('body')))
    story.append(vs(4))
    story.append(cblock([
        'import numpy as np',
        'import scipy.stats as stats',
        '',
        'data = [3, 21, 98, 203, 17, 9, 45, 62, 78, 34]',
        '',
        '# ── Measures of Central Tendency ──────────────────────────',
        'mean   = np.mean(data)           # 57.0',
        'median = np.median(data)         # 39.5',
        'mode   = stats.mode(data)        # ModeResult(mode=3, count=1)',
        '',
        '# ── Measures of Spread ────────────────────────────────────',
        'var    = np.var(data, ddof=1)    # Sample variance (ddof=1)',
        'std    = np.std(data, ddof=1)    # Sample std deviation',
        'rng    = np.ptp(data)            # Range = max - min',
        '',
        '# ── Percentiles and Quartiles ─────────────────────────────',
        'q1     = np.percentile(data, 25) # Q1',
        'q2     = np.percentile(data, 50) # Q2 = median',
        'q3     = np.percentile(data, 75) # Q3',
        'iqr    = q3 - q1                 # Interquartile Range',
        '',
        '# ── Skewness and Kurtosis ─────────────────────────────────',
        'skew   = stats.skew(data)',
        'kurt   = stats.kurtosis(data)',
        '',
        '# ── Full summary using pandas ─────────────────────────────',
        'import pandas as pd',
        'df = pd.DataFrame(data, columns=["values"])',
        'print(df.describe())',
        '# count   10.000',
        '# mean    57.000',
        '# std     58.xxx',
        '# min      3.000',
        '# 25%     17.250',
        '# 50%     39.500',
        '# 75%     75.500',
        '# max    203.000',
        '',
        '# ── Variance calculation for exam question ────────────────',
        '# data: 3, 21, 98, 203, 17, 9',
        'exam_data = [3, 21, 98, 203, 17, 9]',
        'mean_e = np.mean(exam_data)      # 58.5',
        'var_e  = np.var(exam_data)       # Population variance',
        'var_s  = np.var(exam_data, ddof=1)  # Sample variance',
        'print(f"Mean: {mean_e}")',
        'print(f"Population Variance: {var_e:.4f}")',
        'print(f"Sample Variance: {var_s:.4f}")',
    ]))
    story.append(vs(6))

    story.append(Paragraph('Shape of Distribution', S('subtopic')))
    story.append(stbl(
        ['Shape','Description','Relationship','Example'],
        [
            ['Symmetric / Normal','Bell-shaped, equal on both sides','Mean = Median = Mode','Heights, IQ scores'],
            ['Positively Skewed (Right)','Long tail on the right side','Mean > Median > Mode','Income distribution, house prices'],
            ['Negatively Skewed (Left)','Long tail on the left side','Mean < Median < Mode','Age at retirement, exam scores (easy test)'],
            ['Bimodal','Two peaks/humps','Two distinct modes','Mixed populations'],
            ['Uniform','All values equally likely','No central tendency','Dice rolls'],
        ],
        [3*cm, 4*cm, 3.5*cm, 4.5*cm]
    ))
    story.append(vs(6))

    # Q&A Topic 1
    story.append(hr(TEAL))
    story.append(Paragraph('EXAM QUESTIONS — DESCRIPTIVE STATISTICS', S('subtopic')))

    story.extend(qa(1.5, 'Find the variance for the data representing tree heights in feet: 3, 21, 98, 203, 17, 9', [
        Paragraph('<b>Step 1:</b> Find Mean = (3+21+98+203+17+9)/6 = 351/6 = <b>58.5</b>', S('ans')),
        Paragraph('<b>Step 2:</b> Find squared deviations from mean:', S('ans')),
        Paragraph('(3-58.5)^2=3080.25, (21-58.5)^2=1406.25, (98-58.5)^2=1560.25, (203-58.5)^2=20880.25, (17-58.5)^2=1722.25, (9-58.5)^2=2450.25', S('ans')),
        Paragraph('<b>Step 3:</b> Population Variance = Sum / n = (3080.25+1406.25+1560.25+20880.25+1722.25+2450.25)/6 = 31099.5/6 = <b>5183.25</b>', S('ans')),
        Paragraph('Sample Variance (ddof=1) = 31099.5/5 = <b>6219.9</b>', S('ans')),
    ]))

    story.extend(qa(1.5, 'Differentiate between inferential and descriptive statistics.', [
        Paragraph('<b>Descriptive Statistics:</b> Summarizes and describes the features of a dataset. Does NOT make conclusions beyond the given data. Uses measures like mean, median, variance, standard deviation. Example: "Average salary in this sample is Rs.50,000."', S('ans')),
        Paragraph('<b>Inferential Statistics:</b> Uses sample data to draw conclusions (inferences) about the broader population. Uses hypothesis tests, confidence intervals, regression. Example: "Based on this sample, average salary of ALL employees in India is Rs.50,000."', S('ans')),
    ]))

    story.extend(qa(5, 'Explain descriptive statistics in detail. Discuss measures of central tendency and measures of dispersion with examples and Python code.', [
        Paragraph('<b>DESCRIPTIVE STATISTICS</b> is the branch of statistics that summarizes, organizes, and presents data. It describes the basic features WITHOUT drawing conclusions beyond the data.', S('ans')),
        Paragraph('<b>MEASURES OF CENTRAL TENDENCY:</b>', S('body_bold')),
        Paragraph('<b>1. Mean</b> — arithmetic average. Mean = Sum(xi)/n. Sensitive to outliers.', S('bullet')),
        Paragraph('<b>2. Median</b> — middle value when sorted. Robust to outliers. For even n: average of two middle values.', S('bullet')),
        Paragraph('<b>3. Mode</b> — most frequent value. Used for categorical data.', S('bullet')),
        cblock([
            'data = [10, 20, 30, 40, 50, 100]',
            'print(np.mean(data))    # 41.67 — pulled up by 100',
            'print(np.median(data))  # 35.0  — unaffected by 100',
        ]),
        Paragraph('<b>MEASURES OF DISPERSION:</b>', S('body_bold')),
        Paragraph('<b>1. Range</b> = Max - Min. Simple but sensitive to outliers.', S('bullet')),
        Paragraph('<b>2. Variance</b> = Sum((xi-mean)^2)/(n-1). Average squared deviation. Units are squared.', S('bullet')),
        Paragraph('<b>3. Standard Deviation</b> = sqrt(Variance). Same units as data. MOST USED measure of spread.', S('bullet')),
        Paragraph('<b>4. IQR</b> = Q3 - Q1. Middle 50% spread. Robust to outliers. Used in boxplot whiskers.', S('bullet')),
        cblock([
            'data = [15, 20, 25, 30, 35, 40, 45]',
            'print(f"Mean:   {np.mean(data):.2f}")    # 30.0',
            'print(f"Median: {np.median(data):.2f}")  # 30.0',
            'print(f"Std:    {np.std(data,ddof=1):.2f}") # 10.8',
            'print(f"Var:    {np.var(data,ddof=1):.2f}") # 116.67',
            'print(f"IQR:    {np.percentile(data,75)-np.percentile(data,25):.2f}") # 20.0',
            'print(f"Range:  {np.ptp(data)}")          # 30',
        ]),
        Paragraph('<b>SKEWNESS AND KURTOSIS:</b> Skewness measures asymmetry (0=symmetric). Kurtosis measures tail heaviness (3=normal distribution). Both are available via scipy.stats.skew() and scipy.stats.kurtosis().', S('ans')),
        Paragraph('<b>CONCLUSION:</b> Descriptive statistics is the first step in any data analytics workflow. Always check mean, median, std, and skewness before applying any machine learning model.', S('ans')),
    ]))

    story.extend(qa(10, 'What are the various data visualization techniques? Explain descriptive statistics comprehensively with all measures, Python implementation, and practical applications.', [
        Paragraph('<b>DESCRIPTIVE STATISTICS — COMPLETE GUIDE:</b>', S('body_bold')),
        Paragraph('<b>PART 1 — MEASURES OF CENTRAL TENDENCY:</b>', S('body_bold')),
        Paragraph('<b>Mean:</b> x-bar = Sum(xi)/n. Best for symmetric data without outliers. Example: mean salary, mean marks.', S('bullet')),
        Paragraph('<b>Median:</b> Middle value. Best for skewed data or data with outliers. Example: median house price.', S('bullet')),
        Paragraph('<b>Mode:</b> Most frequent value. Best for categorical data. Example: most popular product.', S('bullet')),
        Paragraph('<b>Weighted Mean:</b> Sum(wi*xi)/Sum(wi). Used when values have different importance.', S('bullet')),
        Paragraph('<b>PART 2 — MEASURES OF DISPERSION:</b>', S('body_bold')),
        Paragraph('<b>Range:</b> Max - Min. Quick but sensitive to outliers.', S('bullet')),
        Paragraph('<b>Variance (s2):</b> Sum((xi-xbar)^2)/(n-1). Average squared deviation. Use ddof=1 for sample.', S('bullet')),
        Paragraph('<b>Standard Deviation:</b> sqrt(s2). Same unit as data. Lower = more consistent, higher = more spread.', S('bullet')),
        Paragraph('<b>IQR = Q3 - Q1:</b> Spread of middle 50%. Robust to outliers. Outlier: x < Q1-1.5*IQR or x > Q3+1.5*IQR.', S('bullet')),
        Paragraph('<b>CV = (Std/Mean)*100%:</b> Relative spread. Useful for comparing datasets with different units.', S('bullet')),
        cblock([
            'import numpy as np',
            'import pandas as pd',
            'import scipy.stats as stats',
            '',
            'marks = [45, 62, 78, 55, 90, 38, 72, 85, 48, 67]',
            '',
            '# Central Tendency',
            'print(f"Mean   : {np.mean(marks):.2f}")     # 64.0',
            'print(f"Median : {np.median(marks):.2f}")   # 64.5',
            'print(f"Mode   : {stats.mode(marks).mode}")',
            '',
            '# Dispersion',
            'print(f"Std Dev: {np.std(marks, ddof=1):.2f}")',
            'print(f"Variance:{np.var(marks, ddof=1):.2f}")',
            'print(f"Range  : {np.ptp(marks)}")',
            'q1, q3 = np.percentile(marks, [25, 75])',
            'print(f"IQR    : {q3-q1:.2f}")',
            '',
            '# Shape',
            'print(f"Skewness : {stats.skew(marks):.4f}")',
            'print(f"Kurtosis : {stats.kurtosis(marks):.4f}")',
            '',
            '# Full summary with Pandas',
            'df = pd.Series(marks)',
            'print(df.describe())',
        ]),
        Paragraph('<b>PART 3 — DATA VISUALIZATION TECHNIQUES:</b>', S('body_bold')),
        stbl(
            ['Visualization','Purpose','Best For'],
            [
                ['Histogram','Shows frequency distribution of continuous data','Understanding data shape and spread'],
                ['Box Plot','Shows 5-number summary and outliers visually','Comparing groups, detecting outliers'],
                ['Bar Chart','Compares categorical values','Category comparisons'],
                ['Scatter Plot','Shows relationship between two numeric variables','Correlation analysis'],
                ['Line Chart','Shows trends over time','Time series data'],
                ['Pie Chart','Shows proportion of categories','Part-to-whole relationships'],
                ['Heat Map','Shows matrix data with color intensity','Correlation matrices'],
                ['Violin Plot','Combines box plot with density estimation','Distribution shape comparison'],
            ],
            [3.5*cm, 5*cm, 6.5*cm]
        ),
        vs(4),
        cblock([
            'import matplotlib.pyplot as plt',
            '',
            '# Histogram',
            'plt.hist(marks, bins=5, edgecolor="black")',
            'plt.title("Distribution of Marks")',
            'plt.xlabel("Marks"); plt.ylabel("Frequency"); plt.show()',
            '',
            '# Boxplot',
            'plt.boxplot(marks)',
            'plt.title("Boxplot of Marks"); plt.show()',
            '',
            '# Scatter plot',
            'x = [1,2,3,4,5]; y = [2,4,5,4,5]',
            'plt.scatter(x, y)',
            'plt.title("Scatter Plot"); plt.show()',
        ]),
        Paragraph('<b>CONCLUSION:</b> Descriptive statistics and visualization together form the foundation of Exploratory Data Analysis (EDA). Always perform EDA before building models — it reveals distributions, outliers, relationships, and guides feature engineering decisions.', S('ans')),
    ]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # TOPIC 2: PROBABILITY DISTRIBUTIONS
    # ══════════════════════════════════════════════════════════════
    story.append(topic_box(2,'PROBABILITY DISTRIBUTIONS',12))
    story.append(vs(8))

    story.append(Paragraph('What is a Probability Distribution?', S('subtopic')))
    story.append(Paragraph(
        'A <b>probability distribution</b> is a function that describes the <b>likelihood '
        'of obtaining the possible values</b> that a random variable can take. '
        'It maps each possible outcome to its probability. '
        'There are two types: <b>Discrete</b> (finite/countable outcomes) and '
        '<b>Continuous</b> (infinite outcomes in a range). '
        'Probability distributions are the mathematical backbone of all statistical inference.', S('body')))
    story.append(vs(6))

    story.append(Paragraph('Discrete Probability Distributions', S('subtopic')))
    story.append(stbl(
        ['Distribution','Parameters','PMF Formula','Mean','Variance','Use Case'],
        [
            ['Bernoulli','p = prob of success','P(X=1)=p, P(X=0)=1-p','p','p(1-p)','Single binary outcome (coin flip)'],
            ['Binomial','n=trials, p=success prob','P(X=k)=C(n,k)*p^k*(1-p)^(n-k)','np','np(1-p)','Number of successes in n trials'],
            ['Poisson','lambda=avg rate','P(X=k)=e^(-lam)*lam^k/k!','lambda','lambda','Events per unit time/space'],
            ['Geometric','p=success prob','P(X=k)=(1-p)^(k-1)*p','1/p','(1-p)/p^2','Trials until first success'],
            ['Hypergeometric','N,K,n','Complex formula','nK/N','Complex','Sampling without replacement'],
        ],
        [2.5*cm, 2.5*cm, 4*cm, 1.5*cm, 2*cm, 3.5*cm]
    ))
    story.append(vs(6))

    story.append(Paragraph('Continuous Probability Distributions', S('subtopic')))
    story.append(stbl(
        ['Distribution','Parameters','PDF','Mean','Variance','Use Case'],
        [
            ['Normal (Gaussian)','mu, sigma','(1/sigma*sqrt(2pi))*e^(-(x-mu)^2/2sigma^2)','mu','sigma^2','Natural phenomena, errors, heights'],
            ['Standard Normal','mu=0, sigma=1','(1/sqrt(2pi))*e^(-z^2/2)','0','1','Z-scores, tables'],
            ['t-Distribution','df (degrees freedom)','Complex','0','df/(df-2)','Small sample hypothesis tests'],
            ['F-Distribution','df1, df2','Complex','df2/(df2-2)','Complex','ANOVA, comparing variances'],
            ['Chi-Square','df (degrees freedom)','Complex','df','2*df','Goodness of fit, independence tests'],
            ['Uniform','a=min, b=max','1/(b-a) for x in [a,b]','(a+b)/2','(b-a)^2/12','Equal probability outcomes'],
            ['Exponential','lambda=rate','lambda*e^(-lambda*x)','1/lambda','1/lambda^2','Time between events'],
            ['Beta','alpha, beta','Complex','alpha/(alpha+beta)','Complex','Probability modeling [0,1]'],
        ],
        [3*cm, 2.5*cm, 4*cm, 2*cm, 2*cm, 3.5*cm]
    ))
    story.append(vs(6))

    story.append(Paragraph('Normal Distribution — The Most Important', S('subtopic')))
    story.append(Paragraph(
        'The <b>Normal (Gaussian) distribution</b> is the most important distribution in statistics. '
        'It is symmetric, bell-shaped, and defined by mean (mu) and standard deviation (sigma). '
        'The <b>68-95-99.7 Rule (Empirical Rule)</b>: '
        '68% of data falls within 1 sigma, 95% within 2 sigma, 99.7% within 3 sigma of the mean.', S('body')))
    story.append(cblock([
        'import numpy as np',
        'from scipy import stats',
        'import matplotlib.pyplot as plt',
        '',
        '# Normal Distribution',
        'mu, sigma = 70, 10',
        'x = np.linspace(40, 100, 100)',
        'pdf = stats.norm.pdf(x, mu, sigma)   # Probability density',
        'cdf = stats.norm.cdf(x, mu, sigma)   # Cumulative probability',
        '',
        '# P(X < 80) for Normal(70, 10)',
        'p = stats.norm.cdf(80, mu, sigma)',
        'print(f"P(X < 80) = {p:.4f}")        # 0.8413',
        '',
        '# P(60 < X < 80)',
        'p2 = stats.norm.cdf(80, 70, 10) - stats.norm.cdf(60, 70, 10)',
        'print(f"P(60<X<80) = {p2:.4f}")       # 0.6827 (1 sigma = 68%)',
        '',
        '# Binomial Distribution',
        'n, p = 10, 0.5',
        'k = 6',
        'prob = stats.binom.pmf(k, n, p)',
        'print(f"P(X=6) for Binom(10,0.5) = {prob:.4f}")  # 0.2051',
        '',
        '# Poisson Distribution',
        'lam = 3   # average 3 events per hour',
        'k2 = 5',
        'prob2 = stats.poisson.pmf(k2, lam)',
        'print(f"P(X=5) for Poisson(3) = {prob2:.4f}")     # 0.1008',
        '',
        '# Generate random samples from distributions',
        'normal_samples   = np.random.normal(70, 10, 1000)',
        'binomial_samples = np.random.binomial(10, 0.5, 1000)',
        'poisson_samples  = np.random.poisson(3, 1000)',
    ]))
    story.append(vs(6))

    # Q&A Topic 2
    story.append(hr(TEAL))
    story.append(Paragraph('EXAM QUESTIONS — PROBABILITY DISTRIBUTIONS', S('subtopic')))

    story.extend(qa(5, 'Explain probability distribution types in Python with examples.', [
        Paragraph('<b>PROBABILITY DISTRIBUTION:</b> A probability distribution maps each possible outcome of a random variable to its probability. Two main types: Discrete and Continuous.', S('ans')),
        Paragraph('<b>DISCRETE DISTRIBUTIONS:</b>', S('body_bold')),
        Paragraph('<b>1. Bernoulli Distribution:</b> Single binary outcome (success=1, failure=0). P(X=1)=p, P(X=0)=1-p. Example: coin flip.', S('bullet')),
        Paragraph('<b>2. Binomial Distribution:</b> Number of successes in n independent Bernoulli trials. P(X=k) = C(n,k)*p^k*(1-p)^(n-k). Mean=np, Variance=np(1-p).', S('bullet')),
        Paragraph('<b>3. Poisson Distribution:</b> Number of events in fixed time/space. P(X=k) = e^(-lam)*lam^k/k!. Mean=Variance=lambda.', S('bullet')),
        cblock([
            'from scipy import stats',
            '',
            '# Binomial: P(X=3) from 10 trials, p=0.4',
            'print(stats.binom.pmf(3, 10, 0.4))   # 0.2150',
            '',
            '# Poisson: P(X=2) given lambda=3',
            'print(stats.poisson.pmf(2, 3))        # 0.2240',
        ]),
        Paragraph('<b>CONTINUOUS DISTRIBUTIONS:</b>', S('body_bold')),
        Paragraph('<b>1. Normal Distribution:</b> Bell-shaped, symmetric. Described by mean (mu) and std (sigma). 68-95-99.7 rule. Most widely used in statistics.', S('bullet')),
        Paragraph('<b>2. t-Distribution:</b> Like normal but heavier tails. Used for small samples. Converges to normal as df increases.', S('bullet')),
        Paragraph('<b>3. Chi-Square Distribution:</b> Used in goodness-of-fit and independence tests. Always positive, right-skewed.', S('bullet')),
        Paragraph('<b>4. F-Distribution:</b> Ratio of two chi-square distributions. Used in ANOVA and comparing variances.', S('bullet')),
        cblock([
            '# Normal: P(X < 75) given Normal(70, 10)',
            'print(stats.norm.cdf(75, loc=70, scale=10))   # 0.6915',
            '',
            '# t-Distribution: PDF at x=1 with df=5',
            'print(stats.t.pdf(1, df=5))                   # 0.2195',
            '',
            '# Chi-Square: CDF at x=5.99 with df=2',
            'print(stats.chi2.cdf(5.99, df=2))             # 0.9500',
        ]),
        Paragraph('<b>EMPIRICAL RULE (Normal Distribution):</b> mu +/- 1*sigma = 68% | mu +/- 2*sigma = 95% | mu +/- 3*sigma = 99.7% of data.', S('ans')),
    ]))

    story.extend(qa(10, 'Explain all important probability distributions with formulas, properties, Python implementation and when to use each distribution.', [
        Paragraph('<b>INTRODUCTION:</b> A probability distribution describes the likelihood of all possible outcomes of a random variable. Choosing the right distribution is fundamental to correct statistical analysis.', S('ans')),
        Paragraph('<b>PART 1 — DISCRETE DISTRIBUTIONS:</b>', S('body_bold')),
        Paragraph('<b>1. BERNOULLI DISTRIBUTION:</b>', S('body_bold')),
        Paragraph('Single trial with two outcomes: success (1) or failure (0). P(X=1)=p, P(X=0)=1-p. Mean=p, Var=p(1-p). Example: Will a patient recover? Will email be spam?', S('ans')),
        Paragraph('<b>2. BINOMIAL DISTRIBUTION Bin(n,p):</b>', S('body_bold')),
        Paragraph('Number of successes in n independent Bernoulli trials. PMF: P(X=k)=C(n,k)*p^k*(1-p)^(n-k). Mean=np, Var=np(1-p). Example: Number of heads in 10 coin flips.', S('ans')),
        cblock(['# P(exactly 6 heads in 10 fair coin flips)', 'print(stats.binom.pmf(6, n=10, p=0.5))   # 0.2051', '# P(at most 6 heads)', 'print(stats.binom.cdf(6, n=10, p=0.5))   # 0.8281']),
        Paragraph('<b>3. POISSON DISTRIBUTION Pois(lambda):</b>', S('body_bold')),
        Paragraph('Number of events in a fixed time interval. PMF: P(X=k)=e^(-lam)*lam^k/k!. Mean=Var=lambda. Use when: events occur randomly, independently, at constant average rate.', S('ans')),
        cblock(['# P(3 customers arrive if avg=2 per minute)', 'print(stats.poisson.pmf(3, mu=2))       # 0.1804']),
        Paragraph('<b>PART 2 — CONTINUOUS DISTRIBUTIONS:</b>', S('body_bold')),
        Paragraph('<b>4. NORMAL DISTRIBUTION N(mu, sigma^2):</b>', S('body_bold')),
        Paragraph('Most important distribution. Bell-shaped, symmetric. PDF: f(x)=(1/sigma*sqrt(2pi))*e^(-(x-mu)^2/2sigma^2). Empirical Rule: 68%-95%-99.7%.', S('ans')),
        cblock([
            'mu, sigma = 70, 10',
            'print(stats.norm.cdf(80, mu, sigma))               # P(X<80) = 0.8413',
            'print(stats.norm.ppf(0.95, mu, sigma))             # 95th percentile = 86.45',
            '# Standardize: Z = (X - mu) / sigma',
            'z = (80 - 70) / 10    # Z = 1.0',
        ]),
        Paragraph('<b>5. t-DISTRIBUTION t(df):</b>', S('body_bold')),
        Paragraph('Like normal but heavier tails for small samples. Degrees of freedom df = n-1. As df increases, approaches standard normal. Used in t-tests when population std is unknown.', S('ans')),
        cblock(['# t critical value for 95% CI, df=9', 'print(stats.t.ppf(0.975, df=9))   # 2.2622']),
        Paragraph('<b>6. CHI-SQUARE DISTRIBUTION chi2(df):</b>', S('body_bold')),
        Paragraph('Sum of squared standard normal variables. Right-skewed, always positive. Used in: goodness-of-fit test, independence test. df = number of categories - 1.', S('ans')),
        Paragraph('<b>7. F-DISTRIBUTION F(df1,df2):</b>', S('body_bold')),
        Paragraph('Ratio of two chi-square distributions divided by their df. Right-skewed. Used in ANOVA to compare group variances.', S('ans')),
        Paragraph('<b>8. UNIFORM DISTRIBUTION U(a,b):</b> All values in [a,b] equally likely. Mean=(a+b)/2. Used for random number generation.', S('ans')),
        Paragraph('<b>9. EXPONENTIAL DISTRIBUTION Exp(lambda):</b> Time between Poisson events. Mean=1/lambda. Memoryless property: P(X>s+t|X>s)=P(X>t).', S('ans')),
        Paragraph('<b>CONCLUSION:</b> Selecting the right distribution depends on: data type (discrete/continuous), range of values, nature of the problem (counts, rates, continuous measurements). Always plot data first to identify the likely distribution.', S('ans')),
    ]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # TOPIC 3: INFERENTIAL STATISTICS
    # ══════════════════════════════════════════════════════════════
    story.append(topic_box(3,'INFERENTIAL STATISTICS — OVERVIEW',10))
    story.append(vs(8))

    story.append(Paragraph('What is Inferential Statistics?', S('subtopic')))
    story.append(Paragraph(
        '<b>Inferential statistics</b> uses data from a <b>sample</b> to make '
        '<b>inferences (conclusions) about the population</b>. '
        'It goes beyond simply describing the data — it tests hypotheses, '
        'estimates parameters, and quantifies uncertainty. '
        'Key tools: hypothesis tests, confidence intervals, regression analysis.', S('body')))
    story.append(vs(4))
    story.append(stbl(
        ['Concept','Description','Example'],
        [
            ['Population','The entire group of interest','All students in India'],
            ['Sample','A subset of the population selected for study','500 randomly selected students'],
            ['Parameter','Numerical summary of the population (mu, sigma)','True average marks of ALL students'],
            ['Statistic','Numerical summary of the sample (x-bar, s)','Average marks of 500 sampled students'],
            ['Sampling Error','Difference between sample statistic and population parameter','x-bar != mu'],
            ['Confidence Interval','Range of values likely to contain population parameter','"95% CI: [65, 75]"'],
            ['p-value','Probability of getting results as extreme as observed, assuming H0 is true','p=0.03 means 3% chance'],
            ['Significance Level (alpha)','Threshold for rejecting H0. Usually 0.05 (5%)','If p < alpha: reject H0'],
        ],
        [3.5*cm, 5.5*cm, 6*cm]
    ))
    story.append(vs(6))

    story.append(Paragraph('Confidence Intervals', S('subtopic')))
    story.append(Paragraph(
        'A <b>confidence interval (CI)</b> gives a range of values that likely contains '
        'the true population parameter. '
        'A 95% CI means: if we repeat the experiment 100 times, 95 of the intervals '
        'will contain the true parameter. '
        'CI = x-bar +/- (critical_value * SE), where SE = s / sqrt(n).', S('body')))
    story.append(cblock([
        'import numpy as np',
        'from scipy import stats',
        '',
        'data = [52, 58, 63, 47, 71, 65, 55, 68, 49, 60]',
        'n    = len(data)',
        'mean = np.mean(data)',
        'se   = stats.sem(data)   # Standard error = std/sqrt(n)',
        '',
        '# 95% Confidence Interval',
        'ci_95 = stats.t.interval(0.95, df=n-1, loc=mean, scale=se)',
        'print(f"Mean: {mean:.2f}")',
        'print(f"95% CI: {ci_95[0]:.2f} to {ci_95[1]:.2f}")',
        '',
        '# 99% Confidence Interval',
        'ci_99 = stats.t.interval(0.99, df=n-1, loc=mean, scale=se)',
        'print(f"99% CI: {ci_99[0]:.2f} to {ci_99[1]:.2f}")',
    ]))
    story.append(vs(6))

    # Q&A Topic 3
    story.append(hr(TEAL))
    story.append(Paragraph('EXAM QUESTIONS — INFERENTIAL STATISTICS', S('subtopic')))

    story.extend(qa(1.5, 'Explain overfitting and underfitting of data in data analytics.', [
        Paragraph('<b>Overfitting:</b> The model learns the training data TOO WELL including its noise and random fluctuations. It has very low training error but very high test error — it does not generalize to new data. Caused by overly complex model (too many parameters).', S('ans')),
        Paragraph('<b>Underfitting:</b> The model is TOO SIMPLE to capture the underlying patterns. It has high training error AND high test error. Caused by insufficient model complexity or too few features.', S('ans')),
        Paragraph('<b>Solution:</b> Use cross-validation, regularization (L1/L2), pruning, or choose appropriate model complexity via bias-variance tradeoff.', S('ans')),
    ]))

    story.extend(qa(5, 'Explain inferential statistics and its key concepts including confidence intervals, p-values and significance levels.', [
        Paragraph('<b>INFERENTIAL STATISTICS</b> uses sample data to draw conclusions about populations. It quantifies uncertainty and enables evidence-based decision making.', S('ans')),
        Paragraph('<b>KEY CONCEPTS:</b>', S('body_bold')),
        Paragraph('<b>1. Population vs Sample:</b> Population = all individuals of interest. Sample = subset we study. We use sample statistics to estimate population parameters.', S('bullet')),
        Paragraph('<b>2. Standard Error (SE):</b> SE = sigma/sqrt(n). Measures how much sample mean varies from true mean. Larger sample = smaller SE = more precise estimate.', S('bullet')),
        Paragraph('<b>3. Confidence Interval:</b> CI = x-bar +/- z*(sigma/sqrt(n)). A 95% CI means we are 95% confident the true parameter lies in this range.', S('bullet')),
        Paragraph('<b>4. p-value:</b> Probability of observing results as extreme as ours if H0 is true. Small p-value = strong evidence against H0.', S('bullet')),
        Paragraph('<b>5. Significance Level (alpha):</b> Pre-set threshold (usually 0.05). If p-value < alpha, reject H0. If p-value >= alpha, fail to reject H0.', S('bullet')),
        cblock([
            'data = [52, 58, 63, 47, 71, 65, 55, 68, 49, 60]',
            'n, mean = len(data), np.mean(data)',
            'se = stats.sem(data)',
            '',
            '# 95% CI',
            'ci = stats.t.interval(0.95, df=n-1, loc=mean, scale=se)',
            'print(f"95% CI: ({ci[0]:.2f}, {ci[1]:.2f})")',
            '',
            '# Interpretation: We are 95% confident true mean lies in this interval',
        ]),
        Paragraph('<b>TYPE I and TYPE II ERRORS:</b> Type I Error (False Positive) = Rejecting true H0. Probability = alpha. Type II Error (False Negative) = Failing to reject false H0. Probability = beta. Power of test = 1 - beta.', S('ans')),
    ]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # TOPIC 4: HYPOTHESIS TESTING
    # ══════════════════════════════════════════════════════════════
    story.append(topic_box(4,'HYPOTHESIS TESTING — COMPLETE GUIDE',15))
    story.append(cbox('MOST IMPORTANT TOPIC — 15% Exam Probability — GUARANTEED IN PAPER!',
                      LIGHT_RED, RED, 'note'))
    story.append(vs(8))

    story.append(Paragraph('What is Hypothesis Testing?', S('subtopic')))
    story.append(Paragraph(
        '<b>Hypothesis testing</b> is a statistical procedure used to make decisions about '
        'population parameters based on sample data. '
        'It tests whether there is enough statistical evidence in a sample to infer '
        'that a condition holds for the entire population. '
        'Every hypothesis test involves: formulating hypotheses, choosing a test statistic, '
        'computing p-value, and making a decision.', S('body')))
    story.append(vs(6))

    story.append(Paragraph('Steps in Hypothesis Testing', S('subtopic')))
    story.append(stbl(
        ['Step','Name','Description'],
        [
            ['1','State the Hypotheses',
             'H0 (Null Hypothesis): No effect/difference — assume true initially. '
             'H1/Ha (Alternative Hypothesis): The claim we want to test.'],
            ['2','Choose Significance Level (alpha)',
             'Usually alpha=0.05 (5%). This is the probability of Type I error we accept.'],
            ['3','Choose the Test',
             'Based on data type, sample size, number of groups. '
             'Options: z-test, t-test, chi-square, F-test, ANOVA.'],
            ['4','Compute Test Statistic',
             'Calculate the test statistic value from sample data '
             '(z-score, t-score, F-ratio, chi-square value).'],
            ['5','Find p-value or Critical Value',
             'p-value = P(getting test statistic as extreme as observed | H0 true). '
             'Or compare test statistic to critical value.'],
            ['6','Make Decision',
             'If p-value < alpha: REJECT H0 (significant result). '
             'If p-value >= alpha: FAIL TO REJECT H0 (insufficient evidence).'],
            ['7','State Conclusion',
             'Interpret the result in context of the original problem.'],
        ],
        [1*cm, 3.5*cm, 10.5*cm]
    ))
    story.append(vs(6))

    story.append(Paragraph('Types of Hypothesis Tests', S('subtopic')))
    story.append(stbl(
        ['Test','Use When','Test Statistic','Assumptions'],
        [
            ['One-sample z-test','Test if sample mean equals hypothesized population mean. n>30 or sigma known',
             'z = (x-bar - mu0) / (sigma / sqrt(n))','Large sample or known sigma. Normal population.'],
            ['One-sample t-test','Test if sample mean equals hypothesized value. n<30 or sigma unknown.',
             't = (x-bar - mu0) / (s / sqrt(n)), df=n-1','Normal population. Small sample.'],
            ['Two-sample t-test','Compare means of two independent groups.',
             't = (x1-bar - x2-bar) / sqrt(s1^2/n1 + s2^2/n2)','Normal populations. Independent samples.'],
            ['Paired t-test','Compare means of same group before and after (dependent samples).',
             't = d-bar / (sd / sqrt(n)), d = x1-x2','Differences are normally distributed.'],
            ['Chi-square test','Test independence or goodness of fit for categorical data.',
             'chi2 = Sum((O-E)^2/E)','Expected freq >= 5 in each cell.'],
            ['F-test (ANOVA)','Compare means of 3 or more groups.',
             'F = MSB / MSW (between/within variance)','Normal populations. Equal variances.'],
        ],
        [2.5*cm, 4*cm, 4*cm, 4.5*cm]
    ))
    story.append(vs(6))

    story.append(Paragraph('One-Sample t-Test — Complete Python Example', S('subtopic')))
    story.append(cblock([
        'import numpy as np',
        'from scipy import stats',
        '',
        '# PROBLEM: A school claims average marks = 70.',
        '# Sample of 12 students gives marks below. Test at alpha=0.05.',
        'sample = [65, 72, 68, 74, 61, 78, 69, 71, 64, 73, 70, 67]',
        '',
        '# Step 1: State Hypotheses',
        '# H0: mu = 70  (school claim is correct)',
        '# H1: mu != 70 (two-tailed test)',
        '',
        '# Step 2: Significance level',
        'alpha = 0.05',
        '',
        '# Step 3 & 4: Compute t-statistic and p-value',
        't_stat, p_value = stats.ttest_1samp(sample, popmean=70)',
        'print(f"Sample Mean: {np.mean(sample):.4f}")',
        'print(f"t-statistic: {t_stat:.4f}")',
        'print(f"p-value:     {p_value:.4f}")',
        '',
        '# Step 5 & 6: Decision',
        'if p_value < alpha:',
        '    print("REJECT H0: Significant evidence that mean != 70")',
        'else:',
        '    print("FAIL TO REJECT H0: No significant evidence against mean=70")',
        '',
        '# Step 7: Conclusion',
        '# If p > 0.05: The sample does not provide enough evidence to reject',
        '# the school claim that the true average is 70.',
    ]))
    story.append(vs(6))

    story.append(Paragraph('One-tailed vs Two-tailed Tests', S('subtopic')))
    story.append(stbl(
        ['Test Type','Hypothesis','When to Use','Critical Region'],
        [
            ['Two-tailed','H1: mu != mu0 (not equal to)','When we only care if it is different (either direction)',
             'Both tails: alpha/2 in each tail'],
            ['Right-tailed (upper)','H1: mu > mu0 (greater than)','When we suspect the mean is HIGHER',
             'Right tail only: alpha'],
            ['Left-tailed (lower)','H1: mu < mu0 (less than)','When we suspect the mean is LOWER',
             'Left tail only: alpha'],
        ],
        [3*cm, 3.5*cm, 4.5*cm, 4*cm]
    ))
    story.append(vs(4))
    story.append(cblock([
        '# Two-tailed test (default)',
        't_two, p_two = stats.ttest_1samp(sample, popmean=70)',
        '',
        '# One-tailed (right) test: H1: mu > 70',
        'p_right = p_two / 2 if t_two > 0 else 1 - p_two/2',
        '',
        '# One-tailed (left) test: H1: mu < 70',
        'p_left = p_two / 2 if t_two < 0 else 1 - p_two/2',
        '',
        '# Or use alternative parameter in newer scipy:',
        't_g, p_g = stats.ttest_1samp(sample, 70, alternative="greater")',
        't_l, p_l = stats.ttest_1samp(sample, 70, alternative="less")',
    ]))
    story.append(vs(6))

    story.append(Paragraph('Type I and Type II Errors', S('subtopic')))
    story.append(stbl(
        ['Error Type','Definition','Probability','Consequence','Remedy'],
        [
            ['Type I Error (alpha)\nFalse Positive',
             'Rejecting H0 when it is actually TRUE',
             'alpha (significance level)',
             'Concluding effect exists when it does not',
             'Lower alpha (e.g., 0.01 instead of 0.05)'],
            ['Type II Error (beta)\nFalse Negative',
             'Failing to reject H0 when it is actually FALSE',
             'beta',
             'Missing a real effect',
             'Increase sample size, use more powerful test'],
            ['Power = 1-beta','Probability of correctly rejecting false H0',
             '1-beta','Desirable to be high (>0.8)','Larger n, larger effect size, lower sigma'],
        ],
        [3*cm, 4*cm, 2*cm, 3.5*cm, 3*cm]
    ))
    story.append(vs(6))

    # Q&A Topic 4
    story.append(hr(TEAL))
    story.append(Paragraph('EXAM QUESTIONS — HYPOTHESIS TESTING', S('subtopic')))

    story.extend(qa(1.5, 'What is hypothesis testing?', [
        Paragraph('<b>Hypothesis testing</b> is a statistical method to decide whether there is enough evidence in a sample to support or reject a claim about a population parameter.', S('ans')),
        Paragraph('<b>H0 (Null Hypothesis):</b> Default assumption — no effect or difference exists.', S('bullet')),
        Paragraph('<b>H1 (Alternative Hypothesis):</b> The claim we want to test.', S('bullet')),
        Paragraph('If <b>p-value < alpha</b> (significance level, usually 0.05), we <b>reject H0</b>. Otherwise we <b>fail to reject H0</b>.', S('ans')),
    ]))

    story.extend(qa(10, 'What is hypothesis testing? Explain the various steps used in hypothesis testing with a complete example and Python code.', [
        Paragraph('<b>HYPOTHESIS TESTING</b> is a formal statistical procedure to make evidence-based decisions about population parameters using sample data. It answers: "Is the observed difference real or just due to chance?"', S('ans')),
        Paragraph('<b>KEY TERMINOLOGY:</b>', S('body_bold')),
        Paragraph('<b>H0 (Null Hypothesis):</b> Statement of no effect/difference. Always assumed true initially. Example: H0: mu = 70.', S('bullet')),
        Paragraph('<b>H1 (Alternative Hypothesis):</b> The claim being tested. Example: H1: mu != 70.', S('bullet')),
        Paragraph('<b>p-value:</b> Probability of observing results as extreme as ours IF H0 is true. Small p = strong evidence against H0.', S('bullet')),
        Paragraph('<b>alpha:</b> Significance level. Usually 0.05. If p < alpha, reject H0.', S('bullet')),
        Paragraph('<b>7 STEPS OF HYPOTHESIS TESTING:</b>', S('body_bold')),
        Paragraph('Step 1: STATE HYPOTHESES — Define H0 and H1 clearly.', S('bullet')),
        Paragraph('Step 2: CHOOSE SIGNIFICANCE LEVEL — Usually alpha = 0.05 or 0.01.', S('bullet')),
        Paragraph('Step 3: SELECT APPROPRIATE TEST — Based on data type, sample size, number of groups.', S('bullet')),
        Paragraph('Step 4: COMPUTE TEST STATISTIC — Calculate t, z, chi-square, or F value.', S('bullet')),
        Paragraph('Step 5: FIND p-VALUE — Using tables or scipy.stats functions.', S('bullet')),
        Paragraph('Step 6: MAKE DECISION — If p < alpha: reject H0. If p >= alpha: fail to reject H0.', S('bullet')),
        Paragraph('Step 7: INTERPRET CONCLUSION — State result in context of original problem.', S('bullet')),
        Paragraph('<b>COMPLETE EXAMPLE — One-Sample t-Test:</b>', S('body_bold')),
        Paragraph('Problem: A company claims average delivery time is 5 days. A random sample of 10 deliveries gave: [6,4,5,7,5,6,4,5,6,8]. Test at alpha=0.05.', S('ans')),
        cblock([
            'import numpy as np',
            'from scipy import stats',
            '',
            '# Data',
            'deliveries = [6, 4, 5, 7, 5, 6, 4, 5, 6, 8]',
            '',
            '# Step 1: Hypotheses',
            '# H0: mu = 5  (company claim is correct)',
            '# H1: mu != 5 (two-tailed test)',
            '',
            '# Step 2: alpha = 0.05',
            '',
            '# Step 3: One-sample t-test (n=10, sigma unknown)',
            '',
            '# Step 4 & 5: Test statistic and p-value',
            't_stat, p_value = stats.ttest_1samp(deliveries, popmean=5)',
            '',
            'print(f"Sample Mean : {np.mean(deliveries):.2f}")    # 5.6',
            'print(f"Std Dev     : {np.std(deliveries,ddof=1):.2f}")',
            'print(f"t-statistic : {t_stat:.4f}")',
            'print(f"p-value     : {p_value:.4f}")',
            '',
            '# Step 6: Decision',
            'alpha = 0.05',
            'if p_value < alpha:',
            '    print(f"p={p_value:.4f} < {alpha}: REJECT H0")',
            'else:',
            '    print(f"p={p_value:.4f} >= {alpha}: FAIL TO REJECT H0")',
            '',
            '# Step 7: Conclusion',
            '# If p < 0.05: Evidence suggests delivery time is NOT 5 days.',
            '# If p >= 0.05: Insufficient evidence to contradict the claim.',
        ]),
        Paragraph('<b>TYPES OF ERRORS:</b>', S('body_bold')),
        Paragraph('Type I Error (alpha): Reject true H0 — False Positive. Probability = alpha.', S('bullet')),
        Paragraph('Type II Error (beta): Fail to reject false H0 — False Negative. Probability = beta.', S('bullet')),
        Paragraph('Power = 1 - beta: Probability of correctly detecting a real effect. Should be > 0.8.', S('bullet')),
        Paragraph('<b>CONCLUSION:</b> Hypothesis testing is the backbone of statistical inference. Always clearly state H0 and H1 before collecting data, choose alpha appropriately, and interpret the result in the context of the real-world problem.', S('ans')),
    ]))

    story.extend(qa(15, 'Explain hypothesis testing in complete detail. Include: types of tests, one-tailed vs two-tailed, Type I and II errors, p-value interpretation, and implement z-test, t-test with full Python code.', [
        Paragraph('<b>HYPOTHESIS TESTING — COMPREHENSIVE GUIDE:</b>', S('body_bold')),
        Paragraph('<b>DEFINITION:</b> Hypothesis testing is a formal statistical framework for making decisions about population parameters based on sample evidence. It answers: "Is the observed effect real (statistically significant) or just due to random chance?"', S('ans')),
        Paragraph('<b>THE HYPOTHESIS FRAMEWORK:</b>', S('body_bold')),
        Paragraph('<b>H0 (Null Hypothesis):</b> The default claim. Assumes no effect, no difference, or no relationship. We start by assuming H0 is true. Examples: mu=70, p=0.5, means are equal.', S('bullet')),
        Paragraph('<b>H1 (Alternative Hypothesis):</b> The research claim. What we want to prove. Can be two-tailed (!=), right-tailed (>), or left-tailed (<).', S('bullet')),
        Paragraph('<b>ONE-TAILED vs TWO-TAILED TESTS:</b>', S('body_bold')),
        stbl(
            ['Test','H1','Use When','p-value'],
            [
                ['Two-tailed','mu != mu0','Effect in either direction possible','Full p from test'],
                ['Right-tailed','mu > mu0','Expecting mean to be HIGHER','p = p_two/2 if t>0'],
                ['Left-tailed','mu < mu0','Expecting mean to be LOWER','p = p_two/2 if t<0'],
            ],
            [3*cm, 3*cm, 5*cm, 4*cm]
        ),
        vs(4),
        Paragraph('<b>COMPLETE z-TEST (large sample n>30):</b>', S('body_bold')),
        cblock([
            '# z-test: population sigma known or n > 30',
            'import numpy as np',
            'from scipy import stats',
            '',
            '# Problem: Population sigma=15. Sample n=36, mean=72.',
            '# Test H0: mu=70, H1: mu>70 at alpha=0.05',
            'pop_sigma = 15',
            'n = 36',
            'x_bar = 72',
            'mu0 = 70',
            '',
            '# Compute z-statistic',
            'se = pop_sigma / np.sqrt(n)',
            'z = (x_bar - mu0) / se',
            'print(f"z = {z:.4f}")   # 0.8000',
            '',
            '# p-value for right-tailed',
            'p = 1 - stats.norm.cdf(z)',
            'print(f"p = {p:.4f}")   # 0.2119',
            '',
            'if p < 0.05:',
            '    print("Reject H0")',
            'else:',
            '    print("Fail to reject H0")  # This will print',
        ]),
        Paragraph('<b>COMPLETE t-TEST (small sample, sigma unknown):</b>', S('body_bold')),
        cblock([
            '# One-sample t-test',
            'data = [62, 68, 75, 58, 72, 65, 70, 55, 68, 73]',
            'mu0  = 65',
            '',
            't_stat, p_two = stats.ttest_1samp(data, mu0)',
            'print(f"t = {t_stat:.4f}")',
            'print(f"p (two-tailed) = {p_two:.4f}")',
            '',
            '# Two-sample t-test (comparing two groups)',
            'group1 = [75, 80, 85, 72, 78, 82]',
            'group2 = [65, 70, 68, 72, 74, 69]',
            't2, p2 = stats.ttest_ind(group1, group2)',
            'print(f"Two-sample t = {t2:.4f}, p = {p2:.4f}")',
            '',
            '# Paired t-test (before/after)',
            'before = [200, 210, 190, 220, 185]',
            'after  = [195, 200, 188, 215, 180]',
            'tp, pp = stats.ttest_rel(before, after)',
            'print(f"Paired t = {tp:.4f}, p = {pp:.4f}")',
        ]),
        Paragraph('<b>TYPE I AND TYPE II ERRORS — DETAILED:</b>', S('body_bold')),
        stbl(
            ['','H0 is True','H0 is False'],
            [
                ['Reject H0','Type I Error (alpha)\nFalse Positive','Correct Decision\nTrue Positive (Power = 1-beta)'],
                ['Fail to Reject H0','Correct Decision\nTrue Negative','Type II Error (beta)\nFalse Negative'],
            ],
            [3*cm, 5.5*cm, 6.5*cm]
        ),
        vs(4),
        Paragraph('<b>p-VALUE INTERPRETATION GUIDE:</b>', S('body_bold')),
        stbl(
            ['p-value Range','Interpretation'],
            [
                ['p < 0.001','Extremely strong evidence against H0. Highly significant.'],
                ['0.001 <= p < 0.01','Very strong evidence against H0. Highly significant.'],
                ['0.01 <= p < 0.05','Moderate evidence against H0. Statistically significant.'],
                ['0.05 <= p < 0.10','Weak evidence against H0. Marginal significance.'],
                ['p >= 0.10','Little to no evidence against H0. Not significant.'],
            ],
            [3.5*cm, 11.5*cm]
        ),
        vs(4),
        Paragraph('<b>IMPORTANT NOTES:</b>', S('body_bold')),
        Paragraph('1. p-value is NOT the probability that H0 is true. It is P(data | H0).', S('bullet')),
        Paragraph('2. Statistical significance does NOT imply practical significance. A large sample can make tiny differences significant.', S('bullet')),
        Paragraph('3. "Fail to reject H0" does NOT mean H0 is proved true — it means insufficient evidence.', S('bullet')),
        Paragraph('4. Always state hypothesis BEFORE looking at data to avoid p-hacking.', S('bullet')),
        Paragraph('<b>CONCLUSION:</b> Hypothesis testing is the cornerstone of scientific inquiry and data-driven decision making. Mastering the 7-step procedure, understanding p-values, recognizing test types, and avoiding common misinterpretations are essential skills for any data analyst.', S('ans')),
    ]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # TOPIC 5: TWO-SAMPLE TESTING
    # ══════════════════════════════════════════════════════════════
    story.append(topic_box(5,'TWO-SAMPLE TESTING',10))
    story.append(vs(8))

    story.append(Paragraph('What is Two-Sample Testing?', S('subtopic')))
    story.append(Paragraph(
        '<b>Two-sample tests</b> compare parameters of <b>two separate groups</b> to determine '
        'if there is a statistically significant difference. '
        'Examples: comparing exam scores of male vs female students, '
        'drug vs placebo effect, method A vs method B. '
        'Three types: Independent samples, Paired samples, and testing for equality of variances.', S('body')))
    story.append(vs(6))

    story.append(stbl(
        ['Test','When to Use','H0','Python Function'],
        [
            ['Independent t-test (equal var)','Two independent groups, assume equal variances',
             'mu1 = mu2','stats.ttest_ind(g1, g2, equal_var=True)'],
            ['Welch t-test (unequal var)','Two independent groups, unequal/unknown variances',
             'mu1 = mu2','stats.ttest_ind(g1, g2, equal_var=False)'],
            ['Paired t-test','Same subjects measured twice (before/after)',
             'mu_d = 0 (mean difference=0)','stats.ttest_rel(before, after)'],
            ['Mann-Whitney U test','Non-parametric alternative to independent t-test',
             'Distributions are equal','stats.mannwhitneyu(g1, g2)'],
            ['Wilcoxon signed-rank','Non-parametric alternative to paired t-test',
             'Median difference=0','stats.wilcoxon(before, after)'],
            ['F-test / Levene test','Test equality of variances between two groups',
             'sigma1 = sigma2','stats.levene(g1, g2)'],
        ],
        [3.5*cm, 4.5*cm, 3*cm, 4*cm]
    ))
    story.append(vs(6))

    story.append(cblock([
        'import numpy as np',
        'from scipy import stats',
        '',
        '# ── INDEPENDENT TWO-SAMPLE t-TEST ──────────────────────────',
        '# Problem: Compare test scores of two teaching methods',
        'method_A = [85, 90, 78, 92, 88, 76, 95, 83, 87, 91]',
        'method_B = [75, 80, 72, 85, 79, 68, 88, 74, 81, 77]',
        '',
        '# H0: mu_A = mu_B (no difference between methods)',
        '# H1: mu_A != mu_B',
        '',
        '# Check variance equality first with Levene test',
        'lev_stat, lev_p = stats.levene(method_A, method_B)',
        'print(f"Levene p-value: {lev_p:.4f}")',
        '',
        '# If lev_p > 0.05: use equal_var=True (Student t-test)',
        '# If lev_p < 0.05: use equal_var=False (Welch t-test)',
        't_stat, p_val = stats.ttest_ind(method_A, method_B, equal_var=False)',
        'print(f"t-statistic: {t_stat:.4f}")',
        'print(f"p-value:     {p_val:.4f}")',
        'print(f"Mean A: {np.mean(method_A):.2f}, Mean B: {np.mean(method_B):.2f}")',
        '',
        '# ── PAIRED t-TEST ────────────────────────────────────────',
        '# Problem: Blood pressure before and after medication (same patients)',
        'before = [160, 155, 170, 148, 162, 158, 175, 152]',
        'after  = [145, 148, 155, 140, 150, 145, 160, 138]',
        '',
        '# H0: mu_difference = 0 (medication has no effect)',
        '# H1: mu_difference != 0',
        't_p, p_p = stats.ttest_rel(before, after)',
        'differences = np.array(before) - np.array(after)',
        'print(f"Mean difference: {np.mean(differences):.2f}")',
        'print(f"t-statistic: {t_p:.4f}")',
        'print(f"p-value:     {p_p:.4f}")',
        '',
        '# ── NON-PARAMETRIC: Mann-Whitney U ───────────────────────',
        'u_stat, p_mw = stats.mannwhitneyu(method_A, method_B, alternative="two-sided")',
        'print(f"Mann-Whitney U: {u_stat:.4f}, p: {p_mw:.4f}")',
    ]))
    story.append(vs(6))

    # Q&A Topic 5
    story.append(hr(TEAL))
    story.append(Paragraph('EXAM QUESTIONS — TWO SAMPLE TESTING', S('subtopic')))

    story.extend(qa(5, 'What is two-sample testing? Explain independent t-test and paired t-test with Python code.', [
        Paragraph('<b>TWO-SAMPLE TESTING</b> compares parameters (usually means) of two groups to determine if they are significantly different. H0: mu1 = mu2. H1: mu1 != mu2 (two-tailed) or mu1 > mu2 / mu1 < mu2 (one-tailed).', S('ans')),
        Paragraph('<b>1. INDEPENDENT TWO-SAMPLE t-TEST:</b> Used when two groups have NO relationship. Example: compare marks of class A vs class B.', S('body_bold')),
        cblock([
            'group1 = [85, 90, 78, 92, 88, 76]   # Class A',
            'group2 = [75, 80, 72, 85, 79, 68]   # Class B',
            't, p = stats.ttest_ind(group1, group2, equal_var=False)',
            'print(f"t={t:.4f}, p={p:.4f}")',
            'if p < 0.05: print("Significant difference between classes")',
            'else: print("No significant difference")',
        ]),
        Paragraph('<b>2. PAIRED t-TEST:</b> Used when same subjects measured twice. Example: before and after treatment.', S('body_bold')),
        cblock([
            'before = [200, 215, 190, 225, 210]',
            'after  = [190, 200, 185, 210, 195]',
            'tp, pp = stats.ttest_rel(before, after)',
            'd = np.array(before) - np.array(after)',
            'print(f"Avg reduction: {np.mean(d):.2f}")',
            'print(f"t={tp:.4f}, p={pp:.4f}")',
            'if pp < 0.05: print("Treatment has significant effect")',
        ]),
        Paragraph('<b>KEY DIFFERENCE:</b> Independent t-test: Two different groups, no link between observations. Paired t-test: Same group measured twice, observations are linked.', S('ans')),
    ]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # TOPIC 6: ONE-WAY ANOVA
    # ══════════════════════════════════════════════════════════════
    story.append(topic_box(6,'ONE-WAY ANOVA (Analysis of Variance)',12))
    story.append(vs(8))

    story.append(Paragraph('What is ANOVA?', S('subtopic')))
    story.append(Paragraph(
        '<b>ANOVA (Analysis of Variance)</b> is a statistical technique used to compare '
        'the means of <b>three or more groups</b> simultaneously. '
        'Instead of running multiple t-tests (which increases Type I error), '
        'ANOVA tests whether AT LEAST ONE group mean is different. '
        '<b>One-Way ANOVA</b> has one independent variable (factor) with 3+ levels (groups). '
        'It compares <b>between-group variance</b> to <b>within-group variance</b> using the F-statistic.', S('body')))
    story.append(vs(4))
    story.append(cbox(
        'H0: mu1 = mu2 = mu3 = ... = muk (ALL group means are equal) | '
        'H1: At least one group mean is different from the others. | '
        'ANOVA does NOT tell WHICH groups differ — need Post-hoc tests (Tukey, Bonferroni) for that.',
        LIGHT_ORANGE, ORANGE))
    story.append(vs(6))

    story.append(Paragraph('ANOVA Assumptions', S('subtopic')))
    story.append(Paragraph(
        '1. <b>Independence:</b> Observations are independent within and across groups. '
        '2. <b>Normality:</b> Each group\'s data is approximately normally distributed. '
        '3. <b>Homogeneity of Variances (Homoscedasticity):</b> All groups have approximately equal variances (test with Levene or Bartlett). '
        '4. <b>Continuous dependent variable:</b> The response variable is measured on interval/ratio scale.', S('body')))
    story.append(vs(6))

    story.append(Paragraph('ANOVA Calculations — Step by Step', S('subtopic')))
    story.append(stbl(
        ['Term','Symbol','Formula','Meaning'],
        [
            ['Grand Mean','x-bar-grand','Sum of all observations / total N','Overall mean across all groups'],
            ['Sum of Squares Between','SSB','Sum of ni*(xi-bar - grand-mean)^2','Variation BETWEEN group means'],
            ['Sum of Squares Within','SSW','Sum of (xij - xi-bar)^2 for all i,j','Variation WITHIN each group'],
            ['Total SS','SST','SSB + SSW','Total variation in data'],
            ['Degrees of Freedom Between','dfB','k - 1 (k=number of groups)','Groups minus 1'],
            ['Degrees of Freedom Within','dfW','N - k (N=total observations)','Total N minus groups'],
            ['Mean Square Between','MSB','SSB / dfB','Average between-group variance'],
            ['Mean Square Within','MSW','SSW / dfW','Average within-group variance (pooled error)'],
            ['F-statistic','F','MSB / MSW','Ratio of between to within variance'],
        ],
        [4*cm, 2*cm, 4.5*cm, 4.5*cm]
    ))
    story.append(vs(6))

    story.append(cblock([
        'import numpy as np',
        'from scipy import stats',
        '',
        '# PROBLEM from exam paper:',
        '# Three teaching methods, test scores:',
        'group1 = [56, 58, 60, 62, 64]   # Traditional',
        'group2 = [68, 70, 72, 74, 76]   # Online',
        'group3 = [75, 78, 80, 82, 85]   # Blended',
        '',
        '# H0: mu1 = mu2 = mu3 (all teaching methods give same scores)',
        '# H1: At least one method gives significantly different scores',
        '# alpha = 0.05',
        '',
        '# ── METHOD 1: scipy.stats.f_oneway ────────────────────────',
        'f_stat, p_value = stats.f_oneway(group1, group2, group3)',
        'print(f"F-statistic: {f_stat:.4f}")',
        'print(f"p-value:     {p_value:.4f}")',
        '',
        'if p_value < 0.05:',
        '    print("REJECT H0: Significant difference between teaching methods")',
        'else:',
        '    print("FAIL TO REJECT H0: No significant difference")',
        '',
        '# ── METHOD 2: Manual ANOVA Table ──────────────────────────',
        'all_data = group1 + group2 + group3',
        'N = len(all_data)',
        'k = 3                              # Number of groups',
        'grand_mean = np.mean(all_data)',
        '',
        'groups = [group1, group2, group3]',
        'group_means = [np.mean(g) for g in groups]',
        'group_ns    = [len(g) for g in groups]',
        '',
        '# SSB — Sum of Squares Between groups',
        'SSB = sum(n*(m - grand_mean)**2 for n,m in zip(group_ns, group_means))',
        '',
        '# SSW — Sum of Squares Within groups',
        'SSW = sum(sum((x - m)**2 for x in g) for g, m in zip(groups, group_means))',
        '',
        '# SST = SSB + SSW',
        'SST = SSB + SSW',
        '',
        '# Degrees of freedom',
        'dfB = k - 1       # 2',
        'dfW = N - k       # 12',
        '',
        '# Mean Squares',
        'MSB = SSB / dfB',
        'MSW = SSW / dfW',
        '',
        '# F-statistic',
        'F = MSB / MSW',
        'p = 1 - stats.f.cdf(F, dfB, dfW)',
        '',
        'print(f"SSB = {SSB:.2f}, SSW = {SSW:.2f}, SST = {SST:.2f}")',
        'print(f"MSB = {MSB:.2f}, MSW = {MSW:.2f}")',
        'print(f"F   = {F:.4f},  p   = {p:.6f}")',
        '',
        '# ── POST-HOC TEST: Tukey HSD (which groups differ?) ───────',
        'from statsmodels.stats.multicomp import pairwise_tukeyhsd',
        'import pandas as pd',
        '',
        'data_col  = group1 + group2 + group3',
        'group_col = ["Trad"]*5 + ["Online"]*5 + ["Blended"]*5',
        '',
        'result = pairwise_tukeyhsd(data_col, group_col, alpha=0.05)',
        'print(result)',
    ]))
    story.append(vs(6))

    story.append(Paragraph('ANOVA Summary Table Format', S('subtopic')))
    story.append(stbl(
        ['Source of Variation','SS','df','MS','F','p-value','Decision'],
        [
            ['Between Groups (Treatment)','SSB','k-1','MSB=SSB/dfB','F=MSB/MSW','from F-table','Reject H0 if p < alpha'],
            ['Within Groups (Error)','SSW','N-k','MSW=SSW/dfW','—','—','—'],
            ['Total','SST=SSB+SSW','N-1','—','—','—','—'],
        ],
        [3.5*cm, 1.5*cm, 1.2*cm, 2.5*cm, 2*cm, 2*cm, 2.3*cm]
    ))
    story.append(vs(6))

    # Q&A Topic 6
    story.append(hr(TEAL))
    story.append(Paragraph('EXAM QUESTIONS — ONE-WAY ANOVA', S('subtopic')))

    story.extend(qa(1.5, 'Differentiate between classification and clustering. (Also: When do we use ANOVA vs t-test?)', [
        Paragraph('<b>Classification:</b> A supervised learning technique where the model learns from labeled data to predict the category of new observations. Labels are known during training. Example: spam/not-spam email detection.', S('ans')),
        Paragraph('<b>Clustering:</b> An unsupervised learning technique where the model groups similar data points together WITHOUT predefined labels. Labels are discovered from data. Example: customer segmentation by purchase behavior.', S('ans')),
        Paragraph('<b>ANOVA vs t-test:</b> Use t-test for 2 groups. Use ANOVA for 3 or more groups (avoids inflated Type I error from multiple t-tests).', S('ans')),
    ]))

    story.extend(qa(10, 'What is ANOVA? A researcher wants to know if average test scores from three teaching methods are the same. Perform ANOVA analysis with the given data: Group 1(Traditional):56,58,60,62,64 | Group 2(Online):68,70,72,74,76 | Group 3(Blended):75,78,80,82,85', [
        Paragraph('<b>ANOVA (Analysis of Variance)</b> tests whether the means of three or more groups are statistically equal. It compares between-group variance to within-group variance via the F-statistic.', S('ans')),
        Paragraph('<b>H0: mu1 = mu2 = mu3</b> (all teaching methods produce same scores)', S('bullet')),
        Paragraph('<b>H1: At least one mean is different</b>', S('bullet')),
        Paragraph('<b>alpha = 0.05</b>', S('bullet')),
        Paragraph('<b>MANUAL CALCULATIONS:</b>', S('body_bold')),
        cblock([
            'group1 = [56, 58, 60, 62, 64]   # Traditional — mean=60.0',
            'group2 = [68, 70, 72, 74, 76]   # Online      — mean=72.0',
            'group3 = [75, 78, 80, 82, 85]   # Blended     — mean=80.0',
            '',
            'N=15, k=3, grand_mean = (60+72+80)/3 = 70.67 (approx)',
            '',
            '# SSB = 5*(60-70.67)^2 + 5*(72-70.67)^2 + 5*(80-70.67)^2',
            '#     = 5*113.78 + 5*1.78 + 5*86.78',
            '#     = 568.9 + 8.9 + 433.9 = 1011.7',
            '',
            '# SSW = sum of squared deviations within each group',
            '# Group1: (-4)^2+(-2)^2+0^2+2^2+4^2 = 40',
            '# Group2: same pattern = 40',
            '# Group3: (-5)^2+(-2)^2+0^2+2^2+5^2 = 58',
            '# SSW = 40+40+58 = 138',
            '',
            '# dfB = k-1 = 2, dfW = N-k = 12',
            '# MSB = 1011.7/2 = 505.85',
            '# MSW = 138/12 = 11.5',
            '# F   = 505.85/11.5 = 44.0 (approx)',
        ]),
        Paragraph('<b>PYTHON IMPLEMENTATION:</b>', S('body_bold')),
        cblock([
            'from scipy import stats',
            '',
            'group1 = [56, 58, 60, 62, 64]',
            'group2 = [68, 70, 72, 74, 76]',
            'group3 = [75, 78, 80, 82, 85]',
            '',
            'f_stat, p_value = stats.f_oneway(group1, group2, group3)',
            'print(f"F-statistic = {f_stat:.4f}")',
            'print(f"p-value     = {p_value:.8f}")',
            '',
            'alpha = 0.05',
            'if p_value < alpha:',
            '    print("REJECT H0: Teaching methods have significantly different outcomes")',
            'else:',
            '    print("FAIL TO REJECT H0")',
        ]),
        Paragraph('<b>ANOVA TABLE:</b>', S('body_bold')),
        stbl(
            ['Source','SS','df','MS','F','p-value'],
            [
                ['Between Groups','~1011.7','2','~505.85','~44.0','< 0.0001'],
                ['Within Groups','~138.0','12','~11.5','—','—'],
                ['Total','~1149.7','14','—','—','—'],
            ],
            [3.5*cm, 2.5*cm, 1.2*cm, 2.5*cm, 2*cm, 3.3*cm]
        ),
        vs(4),
        Paragraph('<b>CONCLUSION:</b> Since F = ~44.0 and p-value << 0.05, we REJECT H0. There is strong statistical evidence that at least one teaching method produces significantly different test scores. Post-hoc tests (Tukey HSD) can identify which specific pairs differ.', S('ans')),
    ]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # TOPIC 7: TWO-WAY ANOVA
    # ══════════════════════════════════════════════════════════════
    story.append(topic_box(7,'TWO-WAY ANOVA',10))
    story.append(vs(8))

    story.append(Paragraph('What is Two-Way ANOVA?', S('subtopic')))
    story.append(Paragraph(
        '<b>Two-Way ANOVA</b> extends One-Way ANOVA to examine the effect of '
        '<b>TWO independent variables (factors)</b> on a dependent variable simultaneously. '
        'It tests: (1) Main effect of Factor A, (2) Main effect of Factor B, and '
        '(3) <b>Interaction effect</b> of A x B (does the effect of A depend on B?). '
        'Interaction is the unique and most important insight of Two-Way ANOVA.', S('body')))
    story.append(vs(4))
    story.append(cbox(
        'THREE HYPOTHESES in Two-Way ANOVA: '
        'H0_A: No main effect of Factor A | '
        'H0_B: No main effect of Factor B | '
        'H0_AxB: No interaction between A and B. '
        'Each tested separately using its own F-statistic.',
        LIGHT_GREEN, GREEN))
    story.append(vs(6))

    story.append(Paragraph('Two-Way ANOVA — Concepts', S('subtopic')))
    story.append(stbl(
        ['Term','Description','Interpretation'],
        [
            ['Main Effect of A','Effect of Factor A averaging over all levels of B','Does Factor A independently affect outcome?'],
            ['Main Effect of B','Effect of Factor B averaging over all levels of A','Does Factor B independently affect outcome?'],
            ['Interaction A x B','Effect of A depends on the level of B (or vice versa)','Most interesting finding in Two-Way ANOVA'],
            ['No Interaction','Effect of A is same regardless of level of B','Lines in interaction plot are PARALLEL'],
            ['Interaction Present','Effect of A changes depending on level of B','Lines in interaction plot CROSS or are NOT parallel'],
            ['Cell Mean','Mean of observations at specific (A level, B level) combination','Each cell = one treatment combination'],
        ],
        [3*cm, 5*cm, 7*cm]
    ))
    story.append(vs(6))

    story.append(cblock([
        'import pandas as pd',
        'import numpy as np',
        'from scipy import stats',
        'import statsmodels.api as sm',
        'from statsmodels.formula.api import ols',
        '',
        '# PROBLEM: Effect of fertilizer type AND watering frequency on plant growth',
        '# Factor A: Fertilizer (Type1, Type2)',
        '# Factor B: Watering (Low, High)',
        '',
        'data = pd.DataFrame({',
        '    "growth": [20, 22, 24, 18, 25, 27, 30, 28,',
        '               32, 35, 38, 30, 40, 42, 45, 38],',
        '    "fertilizer": ["F1","F1","F1","F1","F1","F1","F1","F1",',
        '                   "F2","F2","F2","F2","F2","F2","F2","F2"],',
        '    "watering":   ["Low","Low","Low","Low","High","High","High","High",',
        '                   "Low","Low","Low","Low","High","High","High","High"],',
        '})',
        '',
        '# Two-Way ANOVA with interaction',
        'model  = ols("growth ~ C(fertilizer) + C(watering) + C(fertilizer):C(watering)",',
        '             data=data).fit()',
        'anova_table = sm.stats.anova_lm(model, typ=2)',
        'print(anova_table)',
        '',
        '# Output shows:',
        '# C(fertilizer)              — Main effect of fertilizer',
        '# C(watering)                — Main effect of watering',
        '# C(fertilizer):C(watering)  — Interaction effect',
        '# Residual                   — Within-group error',
        '',
        '# Interpret each row:',
        '# If PR(>F) < 0.05: that effect is statistically significant',
        '',
        '# Check assumptions',
        'residuals = model.resid',
        'stat, p_normal = stats.shapiro(residuals)',
        'print(f"Shapiro-Wilk (normality): p = {p_normal:.4f}")',
    ]))
    story.append(vs(6))

    # Q&A Topic 7
    story.append(hr(TEAL))
    story.append(Paragraph('EXAM QUESTIONS — TWO-WAY ANOVA', S('subtopic')))

    story.extend(qa(5, 'What is Two-Way ANOVA? How does it differ from One-Way ANOVA? Explain with example.', [
        Paragraph('<b>TWO-WAY ANOVA</b> extends One-Way ANOVA to test the effects of TWO independent factors simultaneously. It tests three things: main effect of Factor A, main effect of Factor B, and their interaction (A x B).', S('ans')),
        Paragraph('<b>ONE-WAY vs TWO-WAY ANOVA:</b>', S('body_bold')),
        stbl(
            ['Feature','One-Way ANOVA','Two-Way ANOVA'],
            [
                ['Factors','1 independent variable','2 independent variables'],
                ['Hypotheses','1 H0 (all means equal)','3 H0 (main A, main B, interaction)'],
                ['Example','3 teaching methods on scores','Teaching method + gender effect on scores'],
                ['Interaction','Cannot detect','CAN detect if A and B interact'],
                ['F-statistics','1 F value','3 separate F values'],
            ],
            [3.5*cm, 5*cm, 6.5*cm]
        ),
        vs(4),
        Paragraph('<b>EXAMPLE:</b> Testing effect of Drug Type (A, B) AND Dosage (Low, High) on pain relief.', S('body_bold')),
        cblock([
            '# Main effect of Drug: Does drug type affect pain relief overall?',
            '# Main effect of Dosage: Does dosage level affect pain relief overall?',
            '# Interaction: Does the effect of drug type DEPEND on dosage level?',
            '',
            'model = ols("pain_relief ~ C(drug) + C(dosage) + C(drug):C(dosage)",',
            '            data=df).fit()',
            'anova_table = sm.stats.anova_lm(model, typ=2)',
            'print(anova_table)',
            '# Interpret: rows with PR(>F) < 0.05 have significant effects',
        ]),
        Paragraph('<b>INTERACTION INTERPRETATION:</b> If the interaction term is significant (p < 0.05), it means the effect of one factor CHANGES depending on the level of the other. This is the most important finding in Two-Way ANOVA.', S('ans')),
    ]))

    story.extend(qa(10, 'Explain Two-Way ANOVA in detail. What are main effects and interaction effects? How to interpret the ANOVA table?', [
        Paragraph('<b>TWO-WAY ANOVA</b> simultaneously examines the effect of two categorical independent variables (factors) on a continuous dependent variable. It is more efficient than running separate one-way ANOVAs because it also detects INTERACTIONS.', S('ans')),
        Paragraph('<b>THREE COMPONENTS TESTED:</b>', S('body_bold')),
        Paragraph('<b>1. Main Effect of Factor A:</b> The overall effect of Factor A, averaging across all levels of Factor B. H0: All levels of A produce equal means.', S('bullet')),
        Paragraph('<b>2. Main Effect of Factor B:</b> The overall effect of Factor B, averaging across all levels of Factor A. H0: All levels of B produce equal means.', S('bullet')),
        Paragraph('<b>3. Interaction Effect A x B:</b> Does the effect of Factor A depend on which level of Factor B is present? H0: No interaction. This is the UNIQUE insight of Two-Way ANOVA.', S('bullet')),
        Paragraph('<b>UNDERSTANDING INTERACTION:</b>', S('body_bold')),
        Paragraph('NO interaction: Drug A works better than Drug B regardless of whether dosage is low or high — lines in interaction plot are PARALLEL.', S('bullet')),
        Paragraph('INTERACTION PRESENT: Drug A works better at low dose but Drug B works better at high dose — lines CROSS in interaction plot.', S('bullet')),
        Paragraph('<b>COMPLETE PYTHON EXAMPLE:</b>', S('body_bold')),
        cblock([
            'import pandas as pd',
            'import statsmodels.api as sm',
            'from statsmodels.formula.api import ols',
            '',
            '# Dataset: Effect of Study Hours AND Coaching on exam scores',
            'data = pd.DataFrame({',
            '    "score": [60,65,70,75,70,75,80,85, 72,78,82,88,82,88,92,96],',
            '    "hours": ["Low","Low","Low","Low","High","High","High","High",',
            '              "Low","Low","Low","Low","High","High","High","High"],',
            '    "coaching": ["No","No","No","No","No","No","No","No",',
            '                 "Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes"],',
            '})',
            '',
            '# Build model with interaction term',
            'model = ols("score ~ C(hours) + C(coaching) + C(hours):C(coaching)",',
            '            data=data).fit()',
            '',
            '# Two-Way ANOVA Table',
            'anova = sm.stats.anova_lm(model, typ=2)',
            'print(anova)',
            '# Columns: sum_sq, df, F, PR(>F)',
            '# Rows: C(hours), C(coaching), C(hours):C(coaching), Residual',
            '',
            '# Interpretation:',
            '# C(hours)            PR>F < 0.05 => Study hours significantly affect scores',
            '# C(coaching)         PR>F < 0.05 => Coaching significantly affects scores',
            '# C(hours):C(coaching)PR>F < 0.05 => Interaction: effect of hours DEPENDS on coaching',
        ]),
        Paragraph('<b>TWO-WAY ANOVA TABLE STRUCTURE:</b>', S('body_bold')),
        stbl(
            ['Source','SS','df','MS','F','p-value'],
            [
                ['Factor A (between A)','SSA','a-1','MSA=SSA/dfA','F_A=MSA/MSE','p_A'],
                ['Factor B (between B)','SSB','b-1','MSB=SSB/dfB','F_B=MSB/MSE','p_B'],
                ['Interaction A x B','SSAB','(a-1)(b-1)','MSAB','F_AB=MSAB/MSE','p_AB'],
                ['Error (within cells)','SSE','N-ab','MSE','—','—'],
                ['Total','SST','N-1','—','—','—'],
            ],
            [3.5*cm, 1.5*cm, 2*cm, 2.5*cm, 2*cm, 3.5*cm]
        ),
        vs(4),
        Paragraph('<b>ASSUMPTIONS:</b> Independence, normality within cells, homogeneity of variance across cells. Check with Shapiro-Wilk for normality and Levene test for equal variance.', S('ans')),
        Paragraph('<b>CONCLUSION:</b> Two-Way ANOVA is a powerful technique because it is more efficient than multiple one-way tests AND uniquely reveals interaction effects that simpler tests cannot detect.', S('ans')),
    ]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # TOPIC 8: PERMUTATION TEST
    # ══════════════════════════════════════════════════════════════
    story.append(topic_box(8,'PERMUTATION AND RANDOMIZATION TEST',8))
    story.append(vs(8))

    story.append(Paragraph('What is a Permutation Test?', S('subtopic')))
    story.append(Paragraph(
        'A <b>permutation test</b> (also called a randomization test) is a '
        '<b>non-parametric</b> hypothesis testing method that does NOT assume '
        'any particular distribution (like normality). '
        'It creates the null distribution by randomly shuffling (permuting) the data labels '
        'many times, computing a test statistic for each permutation, and comparing the '
        'observed statistic to this distribution. '
        'It is based on the principle: if H0 is true (no difference), randomly reassigning '
        'group labels should produce statistics similar to the observed one.', S('body')))
    story.append(vs(4))
    story.append(cbox(
        'KEY ADVANTAGE: No distributional assumptions (non-parametric). '
        'Works with any test statistic. Perfect for small samples or non-normal data. '
        'p-value = proportion of permutations with statistic as extreme as observed.',
        LIGHT_PURPLE, PURPLE))
    story.append(vs(6))

    story.append(Paragraph('Steps in Permutation Test', S('subtopic')))
    story.append(stbl(
        ['Step','Description'],
        [
            ['1. Compute observed statistic','Calculate test statistic (e.g., difference in means) for actual data'],
            ['2. Pool the data','Combine both groups into a single dataset'],
            ['3. Permute (shuffle) labels','Randomly reassign group labels (many times, e.g., 10,000 iterations)'],
            ['4. Compute permuted statistic','Calculate test statistic for each permuted dataset'],
            ['5. Build null distribution','Collect all permuted statistics — this is the null distribution'],
            ['6. Compute p-value','p = number of permutations with statistic >= observed / total permutations'],
            ['7. Decision','If p < alpha: reject H0 (observed difference is unlikely under H0)'],
        ],
        [3.5*cm, 11.5*cm]
    ))
    story.append(vs(6))

    story.append(cblock([
        'import numpy as np',
        'from scipy import stats',
        '',
        '# PERMUTATION TEST: Are means of two groups significantly different?',
        'group_A = np.array([85, 90, 78, 92, 88, 76, 95, 83])',
        'group_B = np.array([75, 80, 72, 85, 79, 68, 88, 74])',
        '',
        '# Step 1: Observed test statistic (difference in means)',
        'obs_diff = np.mean(group_A) - np.mean(group_B)',
        'print(f"Observed difference in means: {obs_diff:.4f}")',
        '',
        '# Step 2: Pool data',
        'pooled = np.concatenate([group_A, group_B])',
        'n_A    = len(group_A)',
        'n_total= len(pooled)',
        '',
        '# Step 3-5: Permutation loop',
        'n_permutations = 10000',
        'permuted_diffs = np.zeros(n_permutations)',
        '',
        'np.random.seed(42)',
        'for i in range(n_permutations):',
        '    shuffled = np.random.permutation(pooled)    # Shuffle labels',
        '    perm_A   = shuffled[:n_A]                   # First n_A as "group A"',
        '    perm_B   = shuffled[n_A:]                   # Rest as "group B"',
        '    permuted_diffs[i] = np.mean(perm_A) - np.mean(perm_B)',
        '',
        '# Step 6: p-value (two-tailed)',
        'p_value = np.mean(np.abs(permuted_diffs) >= np.abs(obs_diff))',
        'print(f"Permutation test p-value: {p_value:.4f}")',
        '',
        '# Compare with parametric t-test',
        't_stat, p_ttest = stats.ttest_ind(group_A, group_B)',
        'print(f"t-test p-value:            {p_ttest:.4f}")',
        '',
        'if p_value < 0.05:',
        '    print("REJECT H0: Groups are significantly different")',
        'else:',
        '    print("FAIL TO REJECT H0")',
        '',
        '# Quick permutation test using scipy',
        'perm_result = stats.permutation_test(',
        '    (group_A, group_B),',
        '    lambda x, y: np.mean(x) - np.mean(y),',
        '    permutation_type="independent",',
        '    n_resamples=10000,',
        '    alternative="two-sided"',
        ')',
        'print(f"scipy permutation p: {perm_result.pvalue:.4f}")',
    ]))
    story.append(vs(6))

    # Q&A Topic 8
    story.append(hr(TEAL))
    story.append(Paragraph('EXAM QUESTIONS — PERMUTATION TEST', S('subtopic')))

    story.extend(qa(5, 'Explain the Permutation and Randomization Test in Python with a complete example.', [
        Paragraph('<b>PERMUTATION TEST</b> is a non-parametric hypothesis test that creates the null distribution by randomly shuffling data labels many times. It makes NO assumptions about the underlying data distribution.', S('ans')),
        Paragraph('<b>CORE IDEA:</b> Under H0 (no difference between groups), any random assignment of labels should give a similar result. If the observed difference is much larger than most permuted differences, H0 is rejected.', S('ans')),
        Paragraph('<b>ALGORITHM:</b>', S('body_bold')),
        Paragraph('1. Compute observed test statistic (e.g., difference in means)', S('bullet')),
        Paragraph('2. Pool both groups together', S('bullet')),
        Paragraph('3. Repeat 10,000 times: shuffle labels, compute statistic', S('bullet')),
        Paragraph('4. p-value = fraction of permutations with |statistic| >= |observed|', S('bullet')),
        cblock([
            'group_A = np.array([25, 30, 28, 35, 32])',
            'group_B = np.array([18, 22, 20, 25, 23])',
            '',
            'obs_diff = np.mean(group_A) - np.mean(group_B)',
            'pooled   = np.concatenate([group_A, group_B])',
            'n_A      = len(group_A)',
            '',
            'np.random.seed(0)',
            'perm_diffs = [np.mean(np.random.permutation(pooled)[:n_A]) -',
            '              np.mean(np.random.permutation(pooled)[n_A:]) for _ in range(10000)]',
            '',
            'p_val = np.mean(np.abs(perm_diffs) >= np.abs(obs_diff))',
            'print(f"Observed: {obs_diff:.2f}, p={p_val:.4f}")',
            '',
            'if p_val < 0.05: print("Significant difference!")',
            'else: print("No significant difference")',
        ]),
        Paragraph('<b>WHEN TO USE:</b> Small samples | Non-normal data | Non-standard test statistics | When parametric assumptions are violated. Permutation tests are exact and always valid.', S('ans')),
    ]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # TOPIC 9: CHI-SQUARE TEST
    # ══════════════════════════════════════════════════════════════
    story.append(topic_box(9,'CHI-SQUARE TEST',11))
    story.append(vs(8))

    story.append(Paragraph('What is the Chi-Square Test?', S('subtopic')))
    story.append(Paragraph(
        'The <b>Chi-Square (chi2) test</b> is a non-parametric statistical test used for '
        '<b>categorical data</b>. It compares observed frequencies with expected frequencies. '
        'There are two main types: '
        '(1) <b>Chi-Square Goodness of Fit Test</b> — tests if observed data follows an expected distribution. '
        '(2) <b>Chi-Square Test of Independence</b> — tests if two categorical variables are independent.', S('body')))
    story.append(vs(4))
    story.append(cbox(
        'CHI-SQUARE FORMULA: chi2 = Sum[(Observed - Expected)^2 / Expected] | '
        'df (goodness of fit) = k - 1 (k = number of categories) | '
        'df (independence) = (rows-1) * (cols-1) | '
        'Reject H0 if chi2_calculated > chi2_critical OR if p-value < alpha.',
        LIGHT_ORANGE, ORANGE))
    story.append(vs(6))

    story.append(Paragraph('Type 1: Chi-Square Goodness of Fit Test', S('subtopic')))
    story.append(Paragraph(
        '<b>Purpose:</b> Tests whether the observed frequency distribution of a categorical variable '
        'matches an expected (theoretical) distribution. '
        '<b>H0:</b> Observed frequencies follow the expected distribution. '
        '<b>H1:</b> Observed frequencies do NOT follow the expected distribution.', S('body')))
    story.append(cblock([
        'from scipy import stats',
        'import numpy as np',
        '',
        '# PROBLEM: A die is rolled 60 times. Is it fair?',
        '# Expected: each face appears 10 times (60/6 = 10)',
        'observed  = [8, 12, 9, 11, 10, 10]   # Actual counts for faces 1-6',
        'expected  = [10, 10, 10, 10, 10, 10]  # Fair die: equal probability',
        '',
        '# H0: Die is fair (observed matches expected)',
        '# H1: Die is NOT fair',
        '',
        'chi2_stat, p_value = stats.chisquare(f_obs=observed, f_exp=expected)',
        'print(f"Chi-square statistic: {chi2_stat:.4f}")',
        'print(f"p-value:             {p_value:.4f}")',
        'print(f"Degrees of freedom:  {len(observed)-1}")',
        '',
        'if p_value < 0.05:',
        '    print("REJECT H0: Die is NOT fair")',
        'else:',
        '    print("FAIL TO REJECT H0: No evidence die is unfair")',
        '',
        '# Manual chi-square calculation',
        'chi2_manual = sum([(o-e)**2/e for o,e in zip(observed, expected)])',
        'print(f"Manual chi2 = {chi2_manual:.4f}")',
    ]))
    story.append(vs(6))

    story.append(Paragraph('Type 2: Chi-Square Test of Independence', S('subtopic')))
    story.append(Paragraph(
        '<b>Purpose:</b> Tests whether two categorical variables are <b>independent</b> or associated. '
        'Uses a <b>contingency table</b> (cross-tabulation) of observed frequencies. '
        '<b>H0:</b> The two variables are independent (no association). '
        '<b>H1:</b> The two variables are NOT independent (they are associated). '
        'Expected frequency for each cell = (row total * col total) / grand total.', S('body')))
    story.append(cblock([
        'import numpy as np',
        'from scipy import stats',
        'import pandas as pd',
        '',
        '# PROBLEM: Is there association between gender and product preference?',
        '# Contingency table (observed frequencies):',
        '#              Product A  Product B  Product C',
        '# Male              30        20        10',
        '# Female            15        25        20',
        '',
        'observed_table = np.array([[30, 20, 10],',
        '                           [15, 25, 20]])',
        '',
        '# H0: Gender and product preference are INDEPENDENT',
        '# H1: Gender and product preference are ASSOCIATED',
        '',
        'chi2, p, dof, expected = stats.chi2_contingency(observed_table)',
        '',
        'print(f"Chi-square: {chi2:.4f}")',
        'print(f"p-value:    {p:.4f}")',
        'print(f"df:         {dof}")',
        'print("Expected frequencies:")',
        'print(np.round(expected, 2))',
        '',
        'if p < 0.05:',
        '    print("REJECT H0: Gender and preference are ASSOCIATED")',
        'else:',
        '    print("FAIL TO REJECT H0: Variables are INDEPENDENT")',
        '',
        '# Manual expected frequency formula:',
        '# E_ij = (Row_i total * Col_j total) / Grand total',
        'row_totals = observed_table.sum(axis=1)',
        'col_totals = observed_table.sum(axis=0)',
        'grand_total = observed_table.sum()',
        '',
        'for i in range(2):',
        '    for j in range(3):',
        '        E = row_totals[i] * col_totals[j] / grand_total',
        '        O = observed_table[i, j]',
        '        print(f"Cell({i},{j}): O={O}, E={E:.2f}, (O-E)^2/E={(O-E)**2/E:.4f}")',
        '',
        '# Using pandas for cleaner contingency table',
        'df = pd.DataFrame({',
        '    "Gender":    ["M"]*60 + ["F"]*60,',
        '    "Product":   ["A"]*30+["B"]*20+["C"]*10 + ["A"]*15+["B"]*25+["C"]*20',
        '})',
        'ct = pd.crosstab(df["Gender"], df["Product"])',
        'print(ct)',
        'chi2_pd, p_pd, dof_pd, exp_pd = stats.chi2_contingency(ct)',
    ]))
    story.append(vs(6))

    story.append(Paragraph('Chi-Square Test Assumptions and Conditions', S('subtopic')))
    story.append(stbl(
        ['Assumption','Requirement','What to Do if Violated'],
        [
            ['Sample size','Each expected frequency >= 5 in ALL cells','Combine categories or use Fisher exact test'],
            ['Independence','Observations are independent','Ensure proper sampling design'],
            ['Categorical data','Both variables must be categorical (nominal/ordinal)','For continuous: discretize into bins'],
            ['Random sample','Data is from random sample','Verify sampling methodology'],
        ],
        [3.5*cm, 5.5*cm, 6*cm]
    ))
    story.append(vs(6))

    # Q&A Topic 9
    story.append(hr(TEAL))
    story.append(Paragraph('EXAM QUESTIONS — CHI-SQUARE TEST', S('subtopic')))

    story.extend(qa(1.5, 'What is a Chi-Square test? When is it used?', [
        Paragraph('The <b>Chi-Square test</b> is a non-parametric statistical test for <b>categorical data</b>. It compares observed and expected frequencies using: chi2 = Sum[(O-E)^2/E].', S('ans')),
        Paragraph('<b>Used for:</b>', S('body_bold')),
        Paragraph('1. <b>Goodness of Fit Test:</b> Does observed distribution match expected? (e.g., Is a die fair?)', S('bullet')),
        Paragraph('2. <b>Test of Independence:</b> Are two categorical variables associated? (e.g., Is gender related to product preference?)', S('bullet')),
        Paragraph('Reject H0 if p-value < 0.05 (or chi2_calc > chi2_critical).', S('ans')),
    ]))

    story.extend(qa(10, 'Explain the Chi-Square test in detail. Include goodness of fit test, test of independence, formula, assumptions, and Python implementation.', [
        Paragraph('<b>CHI-SQUARE TEST</b> is a non-parametric test for categorical variables. It tests whether observed frequencies match expected frequencies. Formula: chi2 = Sum[(O-E)^2/E] where O=observed count, E=expected count.', S('ans')),
        Paragraph('<b>TYPE 1 — GOODNESS OF FIT TEST:</b>', S('body_bold')),
        Paragraph('<b>Purpose:</b> Test if observed categorical data follows a specified distribution.', S('bullet')),
        Paragraph('<b>H0:</b> Observed frequencies match expected distribution.', S('bullet')),
        Paragraph('<b>H1:</b> Observed frequencies do NOT match.', S('bullet')),
        Paragraph('<b>df = k - 1</b> where k = number of categories.', S('bullet')),
        cblock([
            '# Example: Is a die fair? (60 rolls)',
            'observed = [8, 12, 9, 11, 10, 10]',
            'expected = [10, 10, 10, 10, 10, 10]',
            '',
            '# Manual: chi2 = (8-10)^2/10 + (12-10)^2/10 + ... = 4/10+4/10+... = 1.0',
            'chi2, p = stats.chisquare(observed, expected)',
            'print(f"chi2={chi2:.4f}, p={p:.4f}, df={len(observed)-1}")',
            '# If p > 0.05: Die appears to be fair',
        ]),
        Paragraph('<b>TYPE 2 — TEST OF INDEPENDENCE:</b>', S('body_bold')),
        Paragraph('<b>Purpose:</b> Test if two categorical variables are independent or associated.', S('bullet')),
        Paragraph('<b>H0:</b> Variables are independent (no association).', S('bullet')),
        Paragraph('<b>H1:</b> Variables are associated (dependent).', S('bullet')),
        Paragraph('<b>Expected frequency formula:</b> E_ij = (Row_i_total * Col_j_total) / Grand_total', S('bullet')),
        Paragraph('<b>df = (rows-1) * (cols-1)</b>', S('bullet')),
        cblock([
            '# Contingency table: Smoking status vs Disease',
            '#               Disease  No Disease',
            '# Smoker            50         30',
            '# Non-Smoker        20        100',
            'observed = np.array([[50, 30], [20, 100]])',
            '',
            'chi2, p, dof, expected = stats.chi2_contingency(observed)',
            'print(f"chi2={chi2:.4f}")',
            'print(f"p   ={p:.6f}")',
            'print(f"df  ={dof}")',
            'print("Expected:", np.round(expected, 2))',
            '',
            '# Interpretation:',
            '# If p < 0.05: Smoking status and disease ARE associated',
            '# The two variables are NOT independent',
        ]),
        Paragraph('<b>COMPLETE CALCULATION EXAMPLE (Manual):</b>', S('body_bold')),
        Paragraph('For a 2x2 table with row totals R1, R2 and column totals C1, C2, grand total N:', S('ans')),
        Paragraph('E11 = R1*C1/N, E12 = R1*C2/N, E21 = R2*C1/N, E22 = R2*C2/N', S('ans')),
        Paragraph('chi2 = (O11-E11)^2/E11 + (O12-E12)^2/E12 + (O21-E21)^2/E21 + (O22-E22)^2/E22', S('ans')),
        Paragraph('Compare chi2_calc to chi2_critical from table with df=(rows-1)*(cols-1). If chi2_calc > chi2_critical: REJECT H0.', S('ans')),
        Paragraph('<b>ASSUMPTIONS:</b> All expected frequencies >= 5. Independent observations. Categorical data. If expected < 5: use Fisher Exact Test.', S('ans')),
        Paragraph('<b>CONCLUSION:</b> Chi-square test is one of the most widely used statistical tests for analyzing categorical data. It is essential in survey analysis, A/B testing, medical research, and market research for detecting associations between categorical variables.', S('ans')),
    ]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # CHEAT SHEET
    # ══════════════════════════════════════════════════════════════
    bt = Table([[Paragraph('QUICK REVISION CHEAT SHEET — MODULE 3 (Statistics)', S('module_banner'))]],
               colWidths=[W-4*cm])
    bt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),TEAL),
        ('TOPPADDING',(0,0),(-1,-1),14),('BOTTOMPADDING',(0,0),(-1,-1),14),
        ('LEFTPADDING',(0,0),(-1,-1),10)]))
    story.append(bt); story.append(vs(10))

    cheat = [
        ['TOPIC','KEY FORMULAS AND POINTS TO REMEMBER','%'],
        ['Descriptive Stats',
         'Mean=Sum(x)/n | Median=middle value (sorted) | Mode=most frequent | '
         'Variance=Sum((x-mean)^2)/(n-1) | Std=sqrt(Var) | IQR=Q3-Q1 | '
         'Skewness: positive=right skew, negative=left skew','12%'],
        ['Probability Distributions',
         'Normal N(mu,sigma): 68-95-99.7 rule | Binomial B(n,p): mean=np, var=np(1-p) | '
         'Poisson P(lam): mean=var=lam | t-dist: small samples | F-dist: ANOVA | '
         'Chi2: categorical tests','12%'],
        ['Inferential Statistics',
         'Sample stats estimate population parameters | SE=sigma/sqrt(n) | '
         '95% CI: xbar +/- 1.96*SE | p-value interpretation | alpha=0.05 (usually) | '
         'Type I error=alpha, Type II error=beta, Power=1-beta','10%'],
        ['Hypothesis Testing',
         '7 Steps: State H0/H1 > Choose alpha > Select test > Compute statistic > Find p > Decision > Conclude | '
         'p<alpha: Reject H0 | Two-tailed vs one-tailed | '
         'ttest_1samp(), ttest_ind(), ttest_rel()','15%'],
        ['Two-Sample Testing',
         'Independent t: ttest_ind(equal_var=True/False) | '
         'Paired t: ttest_rel(before, after) | '
         'Non-parametric: mannwhitneyu(), wilcoxon() | '
         'Check variances: levene() before t-test','10%'],
        ['One-Way ANOVA',
         'F = MSB/MSW | SSB=between groups | SSW=within groups | '
         'dfB=k-1, dfW=N-k | MSB=SSB/dfB, MSW=SSW/dfW | '
         'f_oneway(g1,g2,g3) | Post-hoc: Tukey HSD','12%'],
        ['Two-Way ANOVA',
         'Tests Factor A, Factor B, AND Interaction AxB | '
         '3 separate F-statistics | Interaction = effect of A depends on B | '
         'ols formula: y ~ C(A) + C(B) + C(A):C(B) | sm.stats.anova_lm()','10%'],
        ['Permutation Test',
         'Non-parametric. No distribution assumptions. Shuffle labels 10000x. '
         'p-value = fraction of permuted stats >= observed stat. '
         'Use: np.random.permutation(pooled). Works with any test statistic.','8%'],
        ['Chi-Square Test',
         'chi2=Sum[(O-E)^2/E] | Goodness of fit: df=k-1, chisquare(obs,exp) | '
         'Independence: df=(r-1)(c-1), chi2_contingency(table) | '
         'Expected_ij=Row_i*Col_j/N | All E >= 5 required','11%'],
    ]
    rows_data = []
    for i, row in enumerate(cheat):
        if i == 0:
            rows_data.append([Paragraph(f'<b>{c}</b>', S('body_bold')) for c in row])
        else:
            rows_data.append([Paragraph(f'<b>{row[0]}</b>', S('body_bold')),
                               Paragraph(escape(str(row[1])), S('body')),
                               Paragraph(f'<b>{row[2]}</b>', S('body_bold'))])
    ct2 = Table(rows_data, colWidths=[3*cm, 11*cm, 1*cm])
    ct2.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),DARK_BLUE),('TEXTCOLOR',(0,0),(-1,0),WHITE),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,LIGHT_BLUE]),
        ('BOX',(0,0),(-1,-1),1,ACCENT_BLUE),
        ('INNERGRID',(0,0),(-1,-1),0.5,colors.HexColor('#b0bec5')),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    story.append(ct2); story.append(vs(14))

    story.append(cbox(
        'CRITICAL CODE TO REMEMBER:\n'
        'scipy.stats.ttest_1samp(data, popmean) | '
        'stats.ttest_ind(g1, g2, equal_var=False) | '
        'stats.ttest_rel(before, after) | '
        'stats.f_oneway(g1, g2, g3) | '
        'stats.chi2_contingency(table) | '
        'stats.chisquare(observed, expected) | '
        'stats.norm.cdf(x, mu, sigma) | '
        'stats.t.interval(0.95, df, loc, scale) for CI | '
        'np.random.permutation(data) for permutation test',
        YELLOW_BG, ORANGE, 'note'))
    story.append(vs(10))
    story.append(hr(DARK_BLUE, 2))
    story.append(Paragraph(
        'MODULE 3 — DATA ANALYTICS USING PYTHON (PCC-IT-601-A-2024) | '
        'Statistics Complete Exam Notes | B.Tech 6th Semester', S('tip')))

    doc.build(story)
    print('Module 3 PDF generated successfully!')

build()