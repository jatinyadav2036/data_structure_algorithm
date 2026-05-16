from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import Flowable
from xml.sax.saxutils import escape

# ── Color palette ──────────────────────────────────────────────────────────────
DARK_BLUE   = colors.HexColor('#1a237e')
MED_BLUE    = colors.HexColor('#283593')
ACCENT_BLUE = colors.HexColor('#1565c0')
LIGHT_BLUE  = colors.HexColor('#e3f2fd')
TEAL        = colors.HexColor('#00695c')
LIGHT_TEAL  = colors.HexColor('#e0f2f1')
RED         = colors.HexColor('#b71c1c')
LIGHT_RED   = colors.HexColor('#ffebee')
ORANGE      = colors.HexColor('#e65100')
LIGHT_ORANGE= colors.HexColor('#fff3e0')
PURPLE      = colors.HexColor('#4a148c')
LIGHT_PURPLE= colors.HexColor('#f3e5f5')
GREEN       = colors.HexColor('#1b5e20')
LIGHT_GREEN = colors.HexColor('#e8f5e9')
YELLOW_BG   = colors.HexColor('#fffde7')
DARK_GRAY   = colors.HexColor('#212121')
MED_GRAY    = colors.HexColor('#424242')
LIGHT_GRAY  = colors.HexColor('#f5f5f5')
CODE_BG     = colors.HexColor('#1e1e2e')
CODE_TEXT   = colors.HexColor('#cdd6f4')
WHITE       = colors.white

W, H = A4

# ── Styles ─────────────────────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()
    s = {}

    s['cover_title'] = ParagraphStyle('cover_title',
        fontName='Helvetica-Bold', fontSize=28, textColor=WHITE,
        alignment=TA_CENTER, spaceAfter=8, leading=34)

    s['cover_sub'] = ParagraphStyle('cover_sub',
        fontName='Helvetica', fontSize=13, textColor=colors.HexColor('#bbdefb'),
        alignment=TA_CENTER, spaceAfter=4, leading=18)

    s['cover_code'] = ParagraphStyle('cover_code',
        fontName='Helvetica-Bold', fontSize=11, textColor=colors.HexColor('#ffcc02'),
        alignment=TA_CENTER, spaceAfter=4)

    s['module_banner'] = ParagraphStyle('module_banner',
        fontName='Helvetica-Bold', fontSize=18, textColor=WHITE,
        alignment=TA_CENTER, spaceAfter=4, leading=22)

    s['topic_header'] = ParagraphStyle('topic_header',
        fontName='Helvetica-Bold', fontSize=15, textColor=WHITE,
        alignment=TA_LEFT, spaceAfter=2, leading=20,
        leftIndent=8)

    s['subtopic'] = ParagraphStyle('subtopic',
        fontName='Helvetica-Bold', fontSize=11, textColor=DARK_BLUE,
        spaceBefore=10, spaceAfter=4, leading=15)

    s['body'] = ParagraphStyle('body',
        fontName='Helvetica', fontSize=9.5, textColor=DARK_GRAY,
        spaceBefore=3, spaceAfter=3, leading=14, alignment=TA_JUSTIFY)

    s['body_bold'] = ParagraphStyle('body_bold',
        fontName='Helvetica-Bold', fontSize=9.5, textColor=MED_GRAY,
        spaceBefore=2, spaceAfter=2, leading=14)

    s['bullet'] = ParagraphStyle('bullet',
        fontName='Helvetica', fontSize=9.5, textColor=DARK_GRAY,
        spaceBefore=2, spaceAfter=2, leading=14,
        leftIndent=14, firstLineIndent=-10)

    s['code'] = ParagraphStyle('code',
        fontName='Courier', fontSize=8.5, textColor=CODE_TEXT,
        spaceBefore=1, spaceAfter=1, leading=12,
        leftIndent=6)

    s['q_header'] = ParagraphStyle('q_header',
        fontName='Helvetica-Bold', fontSize=10, textColor=TEAL,
        spaceBefore=8, spaceAfter=3, leading=14)

    s['answer'] = ParagraphStyle('answer',
        fontName='Helvetica', fontSize=9.5, textColor=DARK_GRAY,
        spaceBefore=2, spaceAfter=2, leading=14, alignment=TA_JUSTIFY,
        leftIndent=8)

    s['note'] = ParagraphStyle('note',
        fontName='Helvetica-BoldOblique', fontSize=9, textColor=RED,
        spaceBefore=4, spaceAfter=4, leading=13,
        leftIndent=8)

    s['percent'] = ParagraphStyle('percent',
        fontName='Helvetica-Bold', fontSize=9, textColor=ORANGE,
        spaceBefore=0, spaceAfter=0)

    s['toc_item'] = ParagraphStyle('toc_item',
        fontName='Helvetica', fontSize=10, textColor=MED_BLUE,
        spaceBefore=3, spaceAfter=3, leading=14, leftIndent=10)

    s['toc_title'] = ParagraphStyle('toc_title',
        fontName='Helvetica-Bold', fontSize=14, textColor=DARK_BLUE,
        spaceBefore=0, spaceAfter=8, alignment=TA_CENTER)

    s['tip'] = ParagraphStyle('tip',
        fontName='Helvetica-Oblique', fontSize=9, textColor=PURPLE,
        spaceBefore=3, spaceAfter=3, leading=13, leftIndent=8)

    return s

S = make_styles()

# ── Helper Flowables ────────────────────────────────────────────────────────────
def hr(color=ACCENT_BLUE, thickness=1):
    return HRFlowable(width='100%', thickness=thickness, color=color, spaceAfter=4, spaceBefore=4)

def vspace(h=6):
    return Spacer(1, h)

def colored_box(text, bg=LIGHT_BLUE, border=ACCENT_BLUE, style_key='body'):
    data = [[Paragraph(text, S[style_key])]]
    t = Table(data, colWidths=[W - 4*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('BOX', (0,0), (-1,-1), 1, border),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    return t

def code_block(lines):
    items = []
    data = [[Paragraph(escape(l), S['code'])] for l in lines]
    t = Table(data, colWidths=[W - 4*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#45475a')),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('ROWPADDING', (0,0), (-1,-1), 1),
    ]))
    return t

def topic_header_box(num, title, pct):
    left = Paragraph(f'TOPIC {num}: {title}', S['topic_header'])
    right = Paragraph(f'★ Exam: {pct}%', S['percent'])
    right_style = ParagraphStyle('rp', fontName='Helvetica-Bold', fontSize=10,
                                  textColor=colors.HexColor('#ffcc02'), alignment=TA_LEFT)
    right = Paragraph(f'★ Exam Probability: {pct}%', right_style)
    data = [[left, right]]
    t = Table(data, colWidths=[W-5.5*cm, 3.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DARK_BLUE),
        ('LEFTPADDING', (0,0), (0,-1), 12),
        ('RIGHTPADDING', (-1,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t

def qa_block(marks, question, answer_paras):
    """Build a Q&A block with colored question and structured answer."""
    mark_colors = {1.5: (LIGHT_TEAL, TEAL), 5: (LIGHT_ORANGE, ORANGE),
                   10: (LIGHT_PURPLE, PURPLE), 15: (LIGHT_RED, RED)}
    bg, border = mark_colors.get(marks, (LIGHT_GRAY, MED_GRAY))
    mark_labels = {1.5:'SHORT (1.5 Marks | ~50 words)', 5:'MEDIUM (5 Marks | 300-500 words)',
                   10:'LONG (10 Marks | 500-700 words)', 15:'ESSAY (15 Marks | 700-1000 words)'}
    label = mark_labels.get(marks, f'{marks} Marks')
    elems = []
    q_data = [[Paragraph(f'<b>Q [{label}]:</b> {question}', S['q_header'])]]
    qt = Table(q_data, colWidths=[W-4*cm])
    qt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('BOX', (0,0), (-1,-1), 1.5, border),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    elems.append(qt)
    for p in answer_paras:
        elems.append(p)
    elems.append(vspace(4))
    return elems

def simple_table(headers, rows, col_widths=None):
    if col_widths is None:
        col_widths = [(W-4*cm)/len(headers)] * len(headers)
    data = [[Paragraph(f'<b>{h}</b>', S['body_bold']) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), S['body']) for c in row])
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT_GRAY]),
        ('BOX', (0,0), (-1,-1), 1, ACCENT_BLUE),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#b0bec5')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t

# ══════════════════════════════════════════════════════════════════════════════
# BUILD DOCUMENT
# ══════════════════════════════════════════════════════════════════════════════
def build_pdf():
    doc = SimpleDocTemplate(
    'Module1_DAP_ExamNotes.pdf',
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )
    story = []

    # ── COVER PAGE ────────────────────────────────────────────────────────────
    story.append(vspace(60))
    cover_data = [[Paragraph('DATA ANALYTICS<br/>USING PYTHON', S['cover_title'])]]
    ct = Table(cover_data, colWidths=[W-4*cm])
    ct.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DARK_BLUE),
        ('TOPPADDING', (0,0), (-1,-1), 24),
        ('BOTTOMPADDING', (0,0), (-1,-1), 24),
        ('LEFTPADDING', (0,0), (-1,-1), 20),
        ('RIGHTPADDING', (0,0), (-1,-1), 20),
    ]))
    story.append(ct)
    story.append(vspace(12))

    info_data = [
        [Paragraph('CODE: PCC-IT-601-A-2024', S['cover_code'])],
        [Paragraph('B.Tech 6th Semester | Maximum Marks: 75', S['cover_sub'])],
        [Paragraph('MODULE 1 — PYTHON FUNDAMENTALS &amp; OBJECTS IN PYTHON', S['cover_sub'])],
        [Paragraph('Complete Exam Notes with All Questions &amp; Answers', S['cover_sub'])],
    ]
    it = Table(info_data, colWidths=[W-4*cm])
    it.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), MED_BLUE),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
    ]))
    story.append(it)
    story.append(vspace(20))

    topics_grid = [
        ['1. Lists (8%)', '2. Dictionaries (8%)', '3. Functions (10%)'],
        ['4. File Handling (7%)', '5. Class &amp; Instance Attrs (9%)', '6. Inheritance (12%)'],
        ['7. MRO (8%)', '8. Magic Methods (10%)', '9. Metaclasses (7%)'],
        ['10. Abstract Classes (7%)', '11. Exception Handling (9%)', '12. Packages (5%)'],
    ]
    tg_data = [[Paragraph(c, S['cover_sub']) for c in row] for row in topics_grid]
    tg = Table(tg_data, colWidths=[(W-4*cm)/3]*3)
    tg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0d1b5e')),
        ('TEXTCOLOR', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#5c6bc0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#3949ab')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(tg)
    story.append(vspace(30))
    story.append(Paragraph('⚡ TOP PRIORITY TOPICS: Inheritance (12%) | Magic Methods (10%) | Functions (10%) | Exception Handling (9%) | Class Attributes (9%)', S['note']))
    story.append(PageBreak())

    # ── TABLE OF CONTENTS ─────────────────────────────────────────────────────
    story.append(Paragraph('TABLE OF CONTENTS', S['toc_title']))
    story.append(hr(DARK_BLUE, 2))
    story.append(vspace(6))
    toc_items = [
        ('TOPIC 1', 'LISTS IN PYTHON', '8%'),
        ('TOPIC 2', 'DICTIONARIES IN PYTHON', '8%'),
        ('TOPIC 3', 'FUNCTIONS IN PYTHON', '10%'),
        ('TOPIC 4', 'FILE HANDLING IN PYTHON', '7%'),
        ('TOPIC 5', 'CLASS &amp; INSTANCE ATTRIBUTES', '9%'),
        ('TOPIC 6', 'INHERITANCE &amp; MULTIPLE INHERITANCE', '12%'),
        ('TOPIC 7', 'METHOD RESOLUTION ORDER (MRO)', '8%'),
        ('TOPIC 8', 'MAGIC METHODS &amp; OPERATOR OVERLOADING', '10%'),
        ('TOPIC 9', 'METACLASSES IN PYTHON', '7%'),
        ('TOPIC 10', 'ABSTRACT &amp; INNER CLASSES', '7%'),
        ('TOPIC 11', 'EXCEPTION HANDLING', '9%'),
        ('TOPIC 12', 'MODULAR PROGRAMS &amp; PACKAGES', '5%'),
    ]
    for num, title, pct in toc_items:
        row_data = [[
            Paragraph(f'<b>{num}</b>', S['toc_item']),
            Paragraph(title, S['toc_item']),
            Paragraph(f'<b>{pct}</b>', S['toc_item']),
        ]]
        rt = Table(row_data, colWidths=[2.5*cm, W-7.5*cm, 2*cm])
        rt.setStyle(TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#bbdefb')),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        story.append(rt)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # TOPIC 1: LISTS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(topic_header_box(1, 'LISTS IN PYTHON', 8))
    story.append(vspace(8))

    story.append(Paragraph('What is a List?', S['subtopic']))
    story.append(Paragraph(
        'A <b>list</b> in Python is an <b>ordered</b>, <b>mutable</b> (changeable), and <b>heterogeneous</b> '
        'collection of items enclosed in square brackets <b>[ ]</b>. It is the most fundamental and widely '
        'used data structure in Python. Lists can store integers, floats, strings, other lists, or any Python '
        'object. Lists maintain the order of insertion — the first element you put in will always be at '
        'position 0 (index 0). Lists are the backbone of data processing, NumPy arrays, Pandas Series, '
        'and all data analytics pipelines.', S['body']))
    story.append(vspace(4))
    story.append(colored_box(
        '🔑 KEY RULE: Lists are ORDERED (index-based) | MUTABLE (can change after creation) | '
        'ALLOWS DUPLICATES | Uses SQUARE BRACKETS [ ] | HETEROGENEOUS (mixed types allowed)',
        LIGHT_BLUE, ACCENT_BLUE))
    story.append(vspace(6))

    story.append(Paragraph('Creating Lists — All Ways', S['subtopic']))
    story.append(code_block([
        '# 1. Empty list',
        'empty = []',
        '',
        '# 2. Integer list',
        'nums = [1, 2, 3, 4, 5]',
        '',
        '# 3. String list',
        'names = ["Alice", "Bob", "Charlie"]',
        '',
        '# 4. Mixed types (heterogeneous)',
        'mixed = [1, "hello", 3.14, True, None]',
        '',
        '# 5. Nested / 2D list',
        'nested = [[1,2,3], [4,5,6], [7,8,9]]',
        '',
        '# 6. From range',
        'from_range = list(range(1, 11))   # [1,2,3,...,10]',
        '',
        '# 7. From string',
        'chars = list("python")            # ["p","y","t","h","o","n"]',
    ]))
    story.append(vspace(6))

    story.append(Paragraph('List Indexing and Slicing', S['subtopic']))
    story.append(Paragraph(
        'Python lists use <b>zero-based indexing</b>. The first element is at index 0. '
        '<b>Negative indexing</b> allows access from the end: -1 is the last element, -2 is second last. '
        '<b>Slicing</b> extracts a portion using <b>list[start:stop:step]</b> format. '
        'start is inclusive, stop is exclusive.', S['body']))
    story.append(code_block([
        'fruits = ["apple", "banana", "cherry", "date", "elderberry"]',
        '',
        '# Positive indexing',
        'fruits[0]    # "apple"   — first element',
        'fruits[1]    # "banana"  — second element',
        'fruits[4]    # "elderberry" — last by positive index',
        '',
        '# Negative indexing',
        'fruits[-1]   # "elderberry" — last element',
        'fruits[-2]   # "date"       — second last',
        '',
        '# Slicing: list[start:stop:step]',
        'fruits[1:3]   # ["banana", "cherry"] — index 1 to 2 (stop excluded)',
        'fruits[::2]   # ["apple", "cherry", "elderberry"] — every 2nd element',
        'fruits[::-1]  # Reversed: ["elderberry","date","cherry","banana","apple"]',
        'fruits[1:4:2] # ["banana", "date"] — from 1 to 3, step 2',
    ]))
    story.append(vspace(6))

    story.append(Paragraph('All Essential List Methods', S['subtopic']))
    story.append(simple_table(
        ['Method', 'What it Does', 'Example'],
        [
            ['append(x)', 'Adds x to the END of the list', 'lst.append(5) → adds 5 at end'],
            ['insert(i, x)', 'Inserts x at position i (shifts others right)', 'lst.insert(2, "hi")'],
            ['extend(iterable)', 'Adds ALL items of another list/iterable to end', 'lst.extend([6,7,8])'],
            ['remove(x)', 'Removes FIRST occurrence of x (raises ValueError if not found)', 'lst.remove(3)'],
            ['pop()', 'Removes & returns LAST element', 'lst.pop()'],
            ['pop(i)', 'Removes & returns element at index i', 'lst.pop(0)'],
            ['clear()', 'Removes ALL elements — list becomes empty []', 'lst.clear()'],
            ['index(x)', 'Returns index of first occurrence of x', 'lst.index(5)'],
            ['count(x)', 'Counts how many times x appears in list', 'lst.count(2)'],
            ['sort()', 'Sorts list in ascending order IN-PLACE', 'lst.sort()'],
            ['sort(reverse=True)', 'Sorts in descending order IN-PLACE', 'lst.sort(reverse=True)'],
            ['reverse()', 'Reverses the list in-place', 'lst.reverse()'],
            ['copy()', 'Returns a shallow copy of the list', 'lst2 = lst.copy()'],
            ['len(lst)', 'Returns total number of elements (built-in)', 'len(lst)'],
            ['sorted(lst)', 'Returns NEW sorted list (does NOT modify original)', 'sorted(lst)'],
            ['sum(lst)', 'Returns sum of all numeric elements', 'sum([1,2,3]) → 6'],
            ['max(lst)', 'Returns maximum element', 'max([3,1,5]) → 5'],
            ['min(lst)', 'Returns minimum element', 'min([3,1,5]) → 1'],
        ],
        [3.5*cm, 6.5*cm, 5*cm]
    ))
    story.append(vspace(6))

    story.append(Paragraph('List Comprehension', S['subtopic']))
    story.append(Paragraph(
        'List Comprehension is a concise, elegant, and faster way to create lists using a '
        '<b>single line</b> with a for loop inside brackets. It is considered very Pythonic '
        '(the preferred Python way). It is faster than regular loops and more readable.',
        S['body']))
    story.append(Paragraph('<b>Syntax:</b>  [expression  for  item  in  iterable  if  condition]', S['body_bold']))
    story.append(code_block([
        '# 1. Squares of 1 to 5',
        'squares = [x**2 for x in range(1, 6)]         # [1, 4, 9, 16, 25]',
        '',
        '# 2. Even numbers from 0 to 18',
        'evens = [x for x in range(20) if x % 2 == 0]  # [0,2,4,...,18]',
        '',
        '# 3. Convert strings to uppercase',
        'upper = [s.upper() for s in ["a","b","c"]]    # ["A","B","C"]',
        '',
        '# 4. Flatten nested list',
        'flat = [x for row in [[1,2],[3,4]] for x in row]  # [1,2,3,4]',
        '',
        '# 5. Filter and transform together',
        'result = [x**2 for x in range(10) if x % 2 == 0]  # [0,4,16,36,64]',
    ]))
    story.append(vspace(6))

    story.append(Paragraph('2D Lists (Matrix Operations)', S['subtopic']))
    story.append(Paragraph(
        'A <b>2D list</b> (or matrix) is a list of lists. Very useful for representing grids, tables, '
        'or matrices in data analytics. Access element at row r, column c using <b>matrix[r][c]</b>.',
        S['body']))
    story.append(code_block([
        'matrix = [[1,2,3],',
        '          [4,5,6],',
        '          [7,8,9]]',
        '',
        'print(matrix[0][0])   # 1  — row 0, col 0',
        'print(matrix[1][2])   # 6  — row 1, col 2',
        'print(matrix[2][1])   # 8  — row 2, col 1',
        '',
        '# Iterate all rows',
        'for row in matrix:',
        '    print(row)',
        '',
        '# Iterate all elements',
        'for row in matrix:',
        '    for elem in row:',
        '        print(elem, end=" ")   # 1 2 3 4 5 6 7 8 9',
    ]))
    story.append(vspace(6))

    # Q&A for Lists
    story.append(hr(TEAL))
    story.append(Paragraph('📝 EXAM QUESTIONS — LISTS', S['subtopic']))

    elems = qa_block(1.5, 'What is a list in Python? Give an example.', [
        Paragraph('A <b>list</b> in Python is an <b>ordered</b>, <b>mutable</b> collection of elements enclosed in square brackets [ ]. It can store <b>heterogeneous data types</b> (integers, strings, floats, etc.) and allows duplicate values. Lists support indexing and slicing for easy access.', S['answer']),
        Paragraph('<b>Example:</b>  fruits = ["apple", "banana", "cherry"]', S['answer']),
        Paragraph('Access: fruits[0] gives "apple". fruits[-1] gives "cherry". Lists are the most versatile built-in data structure in Python.', S['answer']),
    ])
    story.extend(elems)

    elems = qa_block(1.5, 'Write a Python code to concatenate two lists.', [
        Paragraph('Two lists in Python can be concatenated using the <b>+ operator</b> or the <b>extend()</b> method.', S['answer']),
        code_block([
            'list1 = [1, 2, 3]',
            'list2 = [4, 5, 6]',
            '',
            '# Method 1: + operator (creates new list)',
            'result = list1 + list2',
            'print(result)   # [1, 2, 3, 4, 5, 6]',
            '',
            '# Method 2: extend() (modifies list1 in-place)',
            'list1.extend(list2)',
            'print(list1)    # [1, 2, 3, 4, 5, 6]',
        ]),
    ])
    story.extend(elems)

    elems = qa_block(5, 'Explain List operations and built-in methods in Python with examples.', [
        Paragraph('<b>INTRODUCTION:</b> A list in Python is a mutable, ordered sequence that can hold any type of data. It is one of the most powerful data structures used in everyday programming and data analytics.', S['answer']),
        Paragraph('<b>CREATING LISTS:</b>', S['body_bold']),
        code_block([
            'nums = [10, 20, 30, 40, 50]',
            'mixed = [1, "hello", 3.14, True]',
            'nested = [[1,2], [3,4], [5,6]]',
        ]),
        Paragraph('<b>INDEXING AND SLICING:</b> Indexing starts from 0. Negative index -1 accesses last element. Slicing: list[start:stop:step] extracts a portion.', S['answer']),
        code_block([
            'nums[0]     # 10 — first element',
            'nums[-1]    # 50 — last element',
            'nums[1:3]   # [20, 30] — index 1 to 2',
            'nums[::2]   # [10, 30, 50] — every alternate element',
        ]),
        Paragraph('<b>KEY LIST METHODS:</b>', S['body_bold']),
        Paragraph('• <b>append(x)</b> — Adds element x at the end.', S['bullet']),
        Paragraph('• <b>insert(i, x)</b> — Inserts x at index i.', S['bullet']),
        Paragraph('• <b>extend(lst)</b> — Merges another list at the end.', S['bullet']),
        Paragraph('• <b>remove(x)</b> — Removes first occurrence of x.', S['bullet']),
        Paragraph('• <b>pop(i)</b> — Removes and returns element at index i.', S['bullet']),
        Paragraph('• <b>sort()</b> — Sorts in ascending order (in-place).', S['bullet']),
        Paragraph('• <b>reverse()</b> — Reverses the list in-place.', S['bullet']),
        Paragraph('• <b>count(x)</b> — Counts occurrences of x.', S['bullet']),
        Paragraph('• <b>index(x)</b> — Returns index of first x.', S['bullet']),
        Paragraph('• <b>len(lst)</b> — Returns total number of elements.', S['bullet']),
        code_block([
            'fruits = ["banana", "apple", "cherry"]',
            'fruits.sort()           # ["apple", "banana", "cherry"]',
            'fruits.append("date")   # adds date at end',
            'fruits.remove("apple")  # removes apple',
            'print(len(fruits))      # 3',
        ]),
        Paragraph('<b>LIST COMPREHENSION:</b> One-line technique to generate lists.', S['body_bold']),
        Paragraph('Syntax: [expression for item in iterable if condition]', S['answer']),
        code_block([
            'squares = [x**2 for x in range(1,6)]       # [1,4,9,16,25]',
            'evens   = [x for x in range(10) if x%2==0] # [0,2,4,6,8]',
        ]),
        Paragraph('<b>NESTED LISTS:</b> Lists can contain other lists (2D lists/matrices). matrix = [[1,2],[3,4],[5,6]] — access with matrix[1][0] gives 3. Lists are the foundation of data processing in Python and data analytics applications.', S['answer']),
    ])
    story.extend(elems)

    elems = qa_block(10, 'Describe Python Lists in detail covering creation, operations, methods, comprehension and applications with code examples.', [
        Paragraph('<b>INTRODUCTION:</b> A list in Python is an ordered, mutable, heterogeneous collection of items enclosed in square brackets [ ]. It is the most widely used data structure in Python. Unlike arrays in C or Java, Python lists can hold elements of different data types — integers, strings, floats, booleans, or even other lists. They are dynamic (size can grow/shrink), and form the backbone of all data analytics workflows.', S['answer']),
        Paragraph('<b>CREATING LISTS — ALL TYPES:</b>', S['body_bold']),
        code_block([
            'empty      = []                     # Empty list',
            'numbers    = [1, 2, 3, 4, 5]        # Integer list',
            'names      = ["Alice","Bob","Charlie"] # String list',
            'mixed      = [1, "hi", 3.14, True]  # Mixed types',
            'nested     = [[1,2,3],[4,5,6]]       # 2D list (matrix)',
            'from_range = list(range(1,11))       # [1,2,...,10]',
            'chars      = list("python")          # ["p","y","t","h","o","n"]',
        ]),
        Paragraph('<b>INDEXING (POSITIVE AND NEGATIVE):</b> Positive index starts from 0 (left to right). Negative index starts from -1 (right to left). This dual indexing makes Python extremely powerful for accessing elements.', S['answer']),
        code_block([
            'lst = ["a","b","c","d","e"]',
            'lst[0]    # "a" — first element',
            'lst[-1]   # "e" — last element',
            'lst[-2]   # "d" — second last',
            'lst[2]    # "c" — third element',
        ]),
        Paragraph('<b>SLICING — Format: list[start : stop : step]</b>', S['body_bold']),
        Paragraph('• start — inclusive starting index (default 0)', S['bullet']),
        Paragraph('• stop — exclusive ending index (default end)', S['bullet']),
        Paragraph('• step — jump/skip interval (default 1)', S['bullet']),
        code_block([
            'lst[1:4]    # ["b","c","d"] — index 1,2,3',
            'lst[::2]    # ["a","c","e"] — every alternate element',
            'lst[::-1]   # ["e","d","c","b","a"] — reversed',
            'lst[1:4:2]  # ["b","d"] — index 1,3',
        ]),
        Paragraph('<b>MODIFYING LISTS:</b> Lists are mutable — elements can be changed, added, or removed after creation.', S['answer']),
        code_block([
            'lst[0] = "z"        # Change first element',
            'lst[1:3] = [1,2,3]  # Replace a slice with new values',
            'del lst[2]          # Delete element at index 2',
        ]),
        Paragraph('<b>IMPORTANT METHODS (WITH EXAMPLES):</b>', S['body_bold']),
        code_block([
            'fruits = ["mango", "banana", "apple"]',
            '',
            'fruits.append("grape")      # ["mango","banana","apple","grape"]',
            'fruits.insert(1, "kiwi")    # inserts kiwi at index 1',
            'fruits.extend(["pear","fig"]) # merges two lists',
            'fruits.remove("banana")     # removes first "banana"',
            'fruits.pop()                # removes & returns last element',
            'fruits.pop(0)              # removes & returns element at index 0',
            'fruits.sort()              # sorts alphabetically (in-place)',
            'fruits.sort(reverse=True)  # reverse alphabetical',
            'fruits.reverse()           # reverses in place',
            'idx = fruits.index("apple") # returns position of "apple"',
            'cnt = fruits.count("mango") # counts occurrences of "mango"',
            'fruits.clear()             # removes all elements → []',
            'new = fruits.copy()        # shallow copy',
        ]),
        Paragraph('<b>LIST COMPREHENSION:</b> It is a compact, readable, and faster alternative to for-loop-based list creation. The syntax is: [expression for var in iterable if condition].', S['answer']),
        code_block([
            'squares   = [x**2 for x in range(1,11)]           # Squares of 1 to 10',
            'even_sq   = [x**2 for x in range(10) if x%2==0]   # Even squares',
            'caps      = [w.upper() for w in ["hello","world"]] # ["HELLO","WORLD"]',
            'flat      = [x for sub in [[1,2],[3,4]] for x in sub] # [1,2,3,4]',
        ]),
        Paragraph('<b>2D LISTS (MATRICES):</b> A 2D list is a list of lists. Used to represent tables, grids, and matrices in data analytics.', S['answer']),
        code_block([
            'matrix = [[1,2,3],[4,5,6],[7,8,9]]',
            'print(matrix[0][1])  # 2 — row 0, col 1',
            'for row in matrix:',
            '    print(row)       # Prints each row',
        ]),
        Paragraph('<b>BUILT-IN FUNCTIONS WITH LISTS:</b> len(lst) — number of elements | sum(lst) — sum of numeric elements | max(lst) — maximum element | min(lst) — minimum element | sorted(lst) — returns new sorted list | reversed(lst) — returns reversed iterator.', S['answer']),
        Paragraph('<b>APPLICATIONS IN DATA ANALYTICS:</b> Lists are used to store datasets, feature values, labels, and results. They serve as the base for NumPy arrays, Pandas Series, and are heavily used in data preprocessing pipelines, storing column values, holding model predictions, and processing CSV data row by row.', S['answer']),
        Paragraph('<b>CONCLUSION:</b> Lists are the backbone of Python programming. Their versatility, rich method library, and support for comprehension make them essential for every Python developer and data analyst.', S['answer']),
    ])
    story.extend(elems)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # TOPIC 2: DICTIONARIES
    # ══════════════════════════════════════════════════════════════════════════
    story.append(topic_header_box(2, 'DICTIONARIES IN PYTHON', 8))
    story.append(vspace(8))

    story.append(Paragraph('What is a Dictionary?', S['subtopic']))
    story.append(Paragraph(
        'A <b>dictionary</b> in Python is an <b>unordered</b> (Python 3.7+ maintains insertion order), '
        '<b>mutable</b> collection of <b>key-value pairs</b> enclosed in curly braces <b>{ }</b>. '
        'Each element is a pair: a <b>key</b> (unique identifier) and a <b>value</b> (data associated with that key). '
        'Think of it like a real dictionary — you look up a word (key) to find its meaning (value). '
        'Keys must be <b>immutable</b> (strings, numbers, tuples) but values can be anything.', S['body']))
    story.append(vspace(4))
    story.append(colored_box(
        '🔑 KEY RULE: Keys must be UNIQUE and IMMUTABLE. Values can be ANY type and can be DUPLICATE. '
        'Dictionaries use {} curly braces. Access values by key, NOT by index number.',
        LIGHT_ORANGE, ORANGE))
    story.append(vspace(6))

    story.append(Paragraph('Creating and Accessing Dictionaries', S['subtopic']))
    story.append(code_block([
        '# Creating dictionaries',
        'student = {"name": "Alice", "age": 21, "grade": "A"}  # Basic dict',
        'empty   = {}                                            # Empty dict',
        'd2      = dict(name="Bob", age=20)                     # Using dict() constructor',
        'mixed   = {"id": 1, "scores": [90,85,92], "active": True}  # Nested values',
        '',
        '# Accessing values',
        'print(d["name"])              # "Alice" — direct key access',
        'print(d.get("age"))           # 21 — safe access (no KeyError)',
        'print(d.get("phone", "N/A"))  # "N/A" — default if key missing',
        '',
        '# Adding, modifying, deleting',
        'd["city"] = "Mumbai"         # Add new key',
        'd["age"]  = 22               # Modify existing key',
        'del d["grade"]               # Delete a key',
        'd.pop("city")                # Remove & return value of "city"',
    ]))
    story.append(vspace(6))

    story.append(Paragraph('Dictionary Methods — Complete Reference', S['subtopic']))
    story.append(simple_table(
        ['Method', 'Description', 'Example'],
        [
            ['keys()', 'Returns all keys as a view object', 'dict_keys(["name","age"])'],
            ['values()', 'Returns all values as a view object', 'dict_values(["Alice",21])'],
            ['items()', 'Returns all key-value pairs as tuples', 'dict_items([("name","Alice")])'],
            ['get(key, default)', 'Returns value; default if key not found (no error)', 'd.get("x","N/A")'],
            ['update(dict2)', 'Merges dict2 into current dict (overwrites existing keys)', 'd.update({"age":25})'],
            ['pop(key)', 'Removes key and returns its value', 'd.pop("age") → 21'],
            ['popitem()', 'Removes and returns last key-value pair (Python 3.7+)', 'd.popitem()'],
            ['setdefault(k,v)', 'Returns value; sets key=v if key missing', 'd.setdefault("x",0)'],
            ['clear()', 'Removes all items — dict becomes empty {}', 'd.clear()'],
            ['copy()', 'Returns a shallow copy of the dictionary', 'd2 = d.copy()'],
            ['fromkeys(keys,val)', 'Creates dict from list of keys, all with same value', 'dict.fromkeys(["a","b"],0)'],
            ['in operator', 'Check if key exists in dictionary', '"name" in d → True'],
        ],
        [3.2*cm, 6.8*cm, 5*cm]
    ))
    story.append(vspace(6))

    story.append(Paragraph('Dictionary Comprehension and Nested Dictionaries', S['subtopic']))
    story.append(code_block([
        '# Dictionary comprehension',
        'squares  = {x: x**2 for x in range(1,6)}        # {1:1, 2:4, 3:9, 4:16, 5:25}',
        'even_sq  = {x: x**2 for x in range(10) if x%2==0}',
        'word_len = {w: len(w) for w in ["apple","cat","banana"]}  # {"apple":5,...}',
        '',
        '# Iterating a dictionary',
        'for key in d:                  # iterate keys',
        '    print(key)',
        'for key, val in d.items():     # iterate key-value pairs',
        '    print(f"{key} → {val}")',
        '',
        '# Nested Dictionary',
        'students = {',
        '    "Alice": {"age": 21, "grade": "A", "marks": 92},',
        '    "Bob":   {"age": 22, "grade": "B", "marks": 85}',
        '}',
        'print(students["Alice"]["grade"])  # "A"',
        'print(students["Bob"]["marks"])    # 85',
    ]))
    story.append(vspace(6))

    # Q&A Dictionaries
    story.append(hr(TEAL))
    story.append(Paragraph('📝 EXAM QUESTIONS — DICTIONARIES', S['subtopic']))

    elems = qa_block(1.5, 'What is a Python dictionary? How is it different from a list?', [
        Paragraph('A <b>dictionary</b> is an unordered collection of <b>key-value pairs</b> enclosed in curly braces {}. Unlike lists (which use integer indices 0,1,2...), dictionaries use <b>custom keys</b> for data access.', S['answer']),
        Paragraph('<b>Example:</b>  d = {"name": "Alice", "age": 21}   →   d["name"] gives "Alice"', S['answer']),
        Paragraph('Keys must be <b>unique</b> and <b>immutable</b>; values can be of any type. Lists are ordered sequences; dictionaries are key-based mappings.', S['answer']),
    ])
    story.extend(elems)

    elems = qa_block(5, 'Explain Python dictionaries with all operations and methods with examples.', [
        Paragraph('<b>DEFINITION:</b> A dictionary is a mutable, insertion-ordered (Python 3.7+) collection of key-value pairs. It allows fast O(1) data retrieval using keys instead of numeric indices.', S['answer']),
        Paragraph('<b>CREATING A DICTIONARY:</b>', S['body_bold']),
        code_block([
            'student = {"name": "Alice", "age": 21, "marks": 85.5}',
            'empty   = {}',
            'd2      = dict(city="Delhi", pin=110001)',
        ]),
        Paragraph('<b>ACCESSING DATA:</b>', S['body_bold']),
        code_block([
            'print(student["name"])           # "Alice" — direct access',
            'print(student.get("marks"))      # 85.5 — safe access',
            'print(student.get("phone","N/A"))# "N/A" — default if missing',
        ]),
        Paragraph('<b>ADDING, MODIFYING, DELETING:</b>', S['body_bold']),
        code_block([
            'student["email"] = "alice@ex.com"  # Add new key',
            'student["age"]   = 22               # Modify existing key',
            'del student["marks"]                # Delete key',
        ]),
        Paragraph('<b>IMPORTANT METHODS:</b>', S['body_bold']),
        Paragraph('• <b>keys()</b> → returns all keys: dict_keys(["name","age","email"])', S['bullet']),
        Paragraph('• <b>values()</b> → returns all values', S['bullet']),
        Paragraph('• <b>items()</b> → returns (key,value) tuples — use in for loops', S['bullet']),
        Paragraph('• <b>update({"phone":"9876"})</b> → merges new dict into existing', S['bullet']),
        Paragraph('• <b>pop("age")</b> → removes and returns value of "age"', S['bullet']),
        Paragraph('• <b>clear()</b> → empties the dictionary completely', S['bullet']),
        Paragraph('• <b>copy()</b> → creates a shallow copy', S['bullet']),
        Paragraph('<b>ITERATING A DICTIONARY:</b>', S['body_bold']),
        code_block([
            'for key, value in student.items():',
            '    print(f"{key} → {value}")',
        ]),
        Paragraph('<b>DICTIONARY COMPREHENSION:</b>', S['body_bold']),
        code_block([
            'squares = {x: x**2 for x in range(1,6)}   # {1:1, 2:4, 3:9, 4:16, 5:25}',
        ]),
        Paragraph('<b>NESTED DICTIONARIES:</b>', S['body_bold']),
        code_block([
            'school = {"Alice": {"age":21,"grade":"A"}, "Bob": {"age":22,"grade":"B"}}',
            'print(school["Alice"]["grade"])  # "A"',
        ]),
        Paragraph('Dictionaries are ideal for JSON-like data, configuration settings, frequency counting, lookup tables, and grouping data in analytics pipelines.', S['answer']),
    ])
    story.extend(elems)

    elems = qa_block(10, 'Create a dictionary that stores mobile names as value for "Mobiles" key and price list as value for "Price" key. Create DataFrame from this dictionary.', [
        Paragraph('<b>EXPLANATION:</b> A DataFrame is a 2D tabular data structure in Pandas. We can create it from a dictionary where each key becomes a column name and the corresponding list becomes the column values. All lists must be of equal length.', S['answer']),
        code_block([
            'import pandas as pd',
            '',
            '# Step 1: Create the dictionary',
            'mobile_data = {',
            '    "Mobiles": ["Samsung Galaxy S24", "iPhone 15", "OnePlus 12",',
            '                "Pixel 8", "Xiaomi 14"],',
            '    "Price":   [79999, 89999, 64999, 74999, 69999]',
            '}',
            '',
            '# Step 2: Create DataFrame from dictionary',
            'df = pd.DataFrame(mobile_data)',
            '',
            '# Step 3: Display the DataFrame',
            'print(df)',
            '# Output:',
            '#              Mobiles  Price',
            '# 0  Samsung Galaxy S24  79999',
            '# 1         iPhone 15   89999',
            '# 2         OnePlus 12  64999',
            '# 3           Pixel 8   74999',
            '# 4         Xiaomi 14   69999',
            '',
            '# Accessing columns',
            'print(df["Mobiles"])       # Series of mobile names',
            'print(df["Price"])         # Series of prices',
            '',
            '# Basic operations on DataFrame',
            'print(df.shape)            # (5, 2) — 5 rows, 2 columns',
            'print(df.head(3))          # First 3 rows',
            'print(df.describe())       # Statistical summary of Price',
            '',
            '# Finding most expensive mobile',
            'max_price = df["Price"].max()',
            'expensive = df[df["Price"] == max_price]',
            'print(expensive)           # iPhone 15 — 89999',
            '',
            '# Sort by price',
            'df_sorted = df.sort_values("Price", ascending=False)',
            'print(df_sorted)',
        ]),
        Paragraph('<b>KEY POINTS TO REMEMBER:</b>', S['body_bold']),
        Paragraph('• Dictionary keys become column names in the DataFrame', S['bullet']),
        Paragraph('• Dictionary values (lists) become column data — all lists must be same length', S['bullet']),
        Paragraph('• pd.DataFrame(dict) is the simplest way to create a DataFrame', S['bullet']),
        Paragraph('• DataFrame is the most important data structure in Pandas for data analytics', S['bullet']),
        Paragraph('• Each row gets an automatic integer index (0, 1, 2, ...)', S['bullet']),
    ])
    story.extend(elems)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # TOPIC 3: FUNCTIONS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(topic_header_box(3, 'FUNCTIONS IN PYTHON', 10))
    story.append(vspace(8))

    story.append(Paragraph('What is a Function?', S['subtopic']))
    story.append(Paragraph(
        'A <b>function</b> is a reusable, named block of code that performs a specific task. '
        'You define it once using the <b>def</b> keyword and call it multiple times. '
        'Functions promote <b>code reuse</b>, <b>modularity</b>, and <b>readability</b>. '
        'In Python, functions are <b>first-class objects</b> — meaning they can be assigned to '
        'variables, passed as arguments, or returned from other functions.', S['body']))
    story.append(code_block([
        'def greet(name):              # Defining a function',
        '    """Returns a greeting."""  # Docstring (optional but recommended)',
        '    return f"Hello, {name}!"  # Return statement',
        '',
        'print(greet("Alice"))  # Calling: Hello, Alice!',
        'print(greet("Bob"))    # Reuse: Hello, Bob!',
    ]))
    story.append(vspace(6))

    story.append(Paragraph('Types of Arguments', S['subtopic']))
    story.append(simple_table(
        ['Type', 'Description', 'Example'],
        [
            ['Positional', 'Passed in exact order — position matters', 'add(3, 5) → a=3, b=5'],
            ['Keyword', 'Passed with param name — order doesn\'t matter', 'add(b=5, a=3)'],
            ['Default', 'Parameter has preset value — optional to pass', 'greet() uses "World" default'],
            ['*args', 'Variable positional args — stored as TUPLE — any count', 'total(1,2,3,4,5)'],
            ['**kwargs', 'Variable keyword args — stored as DICT — any count', 'info(name="Alice",age=21)'],
            ['Mixed', 'Combine all types — order: pos, *args, default, **kwargs', 'f(a, *b, x=1, **kw)'],
        ],
        [2.5*cm, 6.5*cm, 6*cm]
    ))
    story.append(vspace(6))

    story.append(code_block([
        '# 1. Positional Arguments',
        'def add(a, b): return a + b',
        'add(3, 5)    # a=3, b=5 → 8',
        '',
        '# 2. Keyword Arguments',
        'add(b=5, a=3)  # Same result — order doesn\'t matter',
        '',
        '# 3. Default Arguments',
        'def greet(name="World"):',
        '    return f"Hello {name}"',
        'greet()        # "Hello World" — uses default',
        'greet("Alice") # "Hello Alice" — overrides default',
        '',
        '# 4. *args — variable positional (stored as tuple)',
        'def total(*nums):',
        '    return sum(nums)',
        'total(1,2,3,4,5)  # 15',
        'total(10, 20)     # 30',
        '',
        '# 5. **kwargs — variable keyword (stored as dict)',
        'def info(**data):',
        '    print(data)',
        'info(name="Alice", age=21, city="Delhi")',
        '# {"name":"Alice", "age":21, "city":"Delhi"}',
        '',
        '# 6. Combined example',
        'def display(name, *subjects, **details):',
        '    print(name, subjects, details)',
        'display("Alice", "Maths", "Python", grade="A", year=3)',
        '# Alice ("Maths","Python") {"grade":"A","year":3}',
    ]))
    story.append(vspace(6))

    story.append(Paragraph('Lambda (Anonymous) Functions', S['subtopic']))
    story.append(Paragraph(
        'A <b>lambda function</b> is a small, anonymous (nameless) function defined in a single line '
        'using the <b>lambda</b> keyword. It can have any number of arguments but only <b>ONE expression</b>. '
        'Used mainly with map(), filter(), sorted(). Lambda functions do NOT need a return statement — '
        'the expression is automatically returned.', S['body']))
    story.append(Paragraph('<b>Syntax:</b>  lambda  arguments  :  expression', S['body_bold']))
    story.append(code_block([
        'square  = lambda x: x**2',
        'print(square(5))      # 25',
        '',
        'add     = lambda x, y: x + y',
        'print(add(3, 4))      # 7',
        '',
        'greet   = lambda name: f"Hello, {name}!"',
        'print(greet("Alice")) # "Hello, Alice!"',
        '',
        '# Used with sorted() — sort by second element',
        'pairs = [(1,"b"),(3,"a"),(2,"c")]',
        'pairs.sort(key=lambda p: p[1])    # Sort by second element',
        '# [(3,"a"),(1,"b"),(2,"c")]',
        '',
        '# Descending sort',
        'nums = [3,1,4,1,5,9,2]',
        'sorted(nums, key=lambda x: -x)    # [9,5,4,3,2,1,1]',
    ]))
    story.append(vspace(6))

    story.append(Paragraph('Higher-Order Functions — map(), filter(), reduce()', S['subtopic']))
    story.append(Paragraph(
        'Python supports <b>higher-order functions</b> that take other functions as arguments. '
        'These three are the most important ones and form the basis of <b>functional programming</b> in Python:', S['body']))
    story.append(code_block([
        'from functools import reduce',
        'nums = [1, 2, 3, 4, 5]',
        '',
        '# map(function, iterable) — applies function to EVERY element',
        'squared = list(map(lambda x: x**2, nums))    # [1,4,9,16,25]',
        'strs    = list(map(str, nums))                # ["1","2","3","4","5"]',
        '',
        '# filter(function, iterable) — keeps elements where function returns True',
        'evens    = list(filter(lambda x: x%2==0, nums))  # [2,4]',
        'positive = list(filter(lambda x: x>0, [-1,2,-3,4]))  # [2,4]',
        '',
        '# reduce(function, iterable) — accumulates to single value',
        'total   = reduce(lambda a,b: a+b, nums)      # 15',
        'product = reduce(lambda a,b: a*b, nums)      # 120',
        'maximum = reduce(lambda a,b: a if a>b else b, nums) # 5',
        '',
        '# COMBINED EXAMPLE (chain all three)',
        'data   = [1, -2, 3, -4, 5]',
        'result = reduce(lambda a,b: a+b,              # Step 3: reduce → 35',
        '          map(lambda x: x**2,                  # Step 2: map   → [1,9,25]',
        '           filter(lambda x: x>0, data)))       # Step 1: filter→ [1,3,5]',
        'print(result)  # 35',
    ]))
    story.append(vspace(6))

    story.append(Paragraph('Recursion', S['subtopic']))
    story.append(Paragraph(
        '<b>Recursion</b> is when a function calls itself. Every recursive function must have a '
        '<b>base case</b> (stopping condition) to prevent infinite loops. Classic examples: '
        'factorial, Fibonacci, binary search. Recursion is elegant but can be slow for large inputs '
        'due to function call overhead.', S['body']))
    story.append(code_block([
        '# Factorial using recursion',
        'def factorial(n):',
        '    if n == 0 or n == 1:   # Base case — STOP condition',
        '        return 1',
        '    return n * factorial(n-1)  # Recursive call',
        '',
        'print(factorial(5))  # 5*4*3*2*1 = 120',
        '',
        '# Fibonacci using recursion',
        'def fibonacci(n):',
        '    if n <= 1: return n    # Base cases: fib(0)=0, fib(1)=1',
        '    return fibonacci(n-1) + fibonacci(n-2)',
        '',
        'print([fibonacci(i) for i in range(8)])  # [0,1,1,2,3,5,8,13]',
    ]))
    story.append(vspace(6))

    story.append(Paragraph('Decorators', S['subtopic']))
    story.append(Paragraph(
        'A <b>decorator</b> is a function that wraps another function to extend its behavior '
        'WITHOUT modifying its original code. Decorators use the <b>@decorator_name</b> syntax '
        'placed above the function definition. Think of it as adding a "wrapper" around a function.', S['body']))
    story.append(code_block([
        '# Basic decorator',
        'def uppercase(func):',
        '    def wrapper():',
        '        result = func()         # Call original function',
        '        return result.upper()   # Add extra behavior',
        '    return wrapper',
        '',
        '@uppercase                      # Apply decorator',
        'def greet():',
        '    return "hello"',
        '',
        'print(greet())  # "HELLO" — automatically uppercased',
        '',
        '# Timer decorator — measures execution time',
        'def timer(func):',
        '    def wrapper(*args, **kwargs):',
        '        import time',
        '        start  = time.time()',
        '        result = func(*args, **kwargs)',
        '        print(f"Time: {time.time()-start:.4f}s")',
        '        return result',
        '    return wrapper',
        '',
        '@timer',
        'def compute():',
        '    return sum(range(1000000))',
        '',
        'compute()  # Prints execution time automatically',
        '',
        '# Built-in decorators: @staticmethod, @classmethod, @property',
    ]))
    story.append(vspace(6))

    story.append(Paragraph('Scope Rules — LEGB', S['subtopic']))
    story.append(Paragraph(
        'Python follows <b>LEGB</b> scope resolution order when looking up variables:', S['body']))
    story.append(simple_table(
        ['Scope', 'Stands For', 'Description', 'Example'],
        [
            ['L', 'Local', 'Variables inside the current function', 'x defined in def f():'],
            ['E', 'Enclosing', 'Variables in outer (enclosing) functions — closures', 'x in outer() seen by inner()'],
            ['G', 'Global', 'Variables at module level (outside all functions)', 'x = 10 at top of file'],
            ['B', 'Built-in', 'Python\'s built-in names (len, print, range, etc.)', 'len(), print(), sum()'],
        ],
        [1*cm, 2.5*cm, 5*cm, 5.5*cm]
    ))
    story.append(vspace(4))
    story.append(code_block([
        'x = "global"',
        '',
        'def outer():',
        '    x = "enclosing"',
        '    def inner():',
        '        x = "local"',
        '        print(x)  # "local" — L scope found first',
        '    inner()',
        '',
        'outer()  # prints "local"',
        '',
        '# global keyword — modify global variable inside function',
        'count = 0',
        'def increment():',
        '    global count',
        '    count += 1',
        '',
        '# nonlocal keyword — modify enclosing scope variable',
        'def outer2():',
        '    val = 0',
        '    def inner2():',
        '        nonlocal val',
        '        val += 1',
        '    inner2()',
        '    print(val)   # 1',
    ]))
    story.append(vspace(6))

    # Q&A Functions
    story.append(hr(TEAL))
    story.append(Paragraph('📝 EXAM QUESTIONS — FUNCTIONS', S['subtopic']))

    elems = qa_block(1.5, 'What is __init__ in Python?', [
        Paragraph('<b>__init__</b> is a special <b>magic method</b> (constructor) in Python classes. It is <b>automatically called</b> when a new object is created from a class. It is used to <b>initialize instance attributes</b> — giving each object its own data.', S['answer']),
        code_block([
            'class Student:',
            '    def __init__(self, name, roll):  # Called automatically on object creation',
            '        self.name = name              # Initialize instance attribute',
            '        self.roll = roll',
            '',
            's1 = Student("Alice", 101)  # __init__ called here',
            'print(s1.name)  # "Alice"',
        ]),
        Paragraph('The <b>self</b> parameter refers to the current object being created. __init__ does NOT return any value.', S['answer']),
    ])
    story.extend(elems)

    elems = qa_block(1.5, 'What are *args and **kwargs in Python functions?', [
        Paragraph('<b>*args</b> allows a function to accept <b>any number of positional arguments</b>, stored as a <b>tuple</b>. <b>**kwargs</b> allows any number of <b>keyword arguments</b>, stored as a <b>dictionary</b>.', S['answer']),
        code_block([
            'def f(*args, **kwargs):',
            '    print(args)    # Tuple of positional args',
            '    print(kwargs)  # Dict of keyword args',
            '',
            'f(1, 2, 3, name="Alice", age=21)',
            '# (1, 2, 3)',
            '# {"name":"Alice", "age":21}',
        ]),
    ])
    story.extend(elems)

    elems = qa_block(5, 'Explain lambda functions and higher-order functions map(), filter(), and reduce() in Python.', [
        Paragraph('<b>LAMBDA FUNCTIONS:</b> A lambda function is an anonymous, single-expression function defined using the <b>lambda</b> keyword. It is used for short, throwaway functions — especially as arguments to map(), filter(), sorted(). It does not need a return statement.', S['answer']),
        Paragraph('<b>Syntax:</b>  lambda arguments: expression', S['body_bold']),
        code_block([
            'square = lambda x: x**2',
            'print(square(7))    # 49',
            '',
            'add = lambda x, y: x + y',
            'print(add(3, 4))    # 7',
            '',
            'pairs = [(1,"b"),(3,"a"),(2,"c")]',
            'pairs.sort(key=lambda p: p[0])  # Sort by first element',
        ]),
        Paragraph('<b>HIGHER-ORDER FUNCTIONS:</b> A higher-order function takes another function as an argument or returns a function.', S['answer']),
        Paragraph('<b>1. map(function, iterable):</b> Applies the function to EVERY element of the iterable. Returns a map object (must convert to list).', S['body_bold']),
        code_block([
            'nums    = [1, 2, 3, 4, 5]',
            'doubled = list(map(lambda x: x*2, nums))  # [2,4,6,8,10]',
            'strs    = list(map(str, nums))             # ["1","2","3","4","5"]',
        ]),
        Paragraph('<b>2. filter(function, iterable):</b> Keeps only elements for which the function returns True.', S['body_bold']),
        code_block([
            'evens    = list(filter(lambda x: x%2==0, nums))  # [2,4]',
            'positive = list(filter(lambda x: x>0, [-1,2,-3,4]))  # [2,4]',
        ]),
        Paragraph('<b>3. reduce(function, iterable) — from functools:</b> Applies function cumulatively to reduce iterable to a single value.', S['body_bold']),
        code_block([
            'from functools import reduce',
            'product = reduce(lambda a,b: a*b, [1,2,3,4,5])  # 120',
            'maximum = reduce(lambda a,b: a if a>b else b, nums)  # 5',
        ]),
        Paragraph('<b>COMBINED EXAMPLE (chaining all three):</b>', S['body_bold']),
        code_block([
            'data   = [1, -2, 3, -4, 5]',
            '# Step 1: filter keeps positive → [1,3,5]',
            '# Step 2: map squares them     → [1,9,25]',
            '# Step 3: reduce sums them     → 35',
            'result = reduce(lambda a,b: a+b,',
            '         map(lambda x: x**2,',
            '          filter(lambda x: x>0, data)))',
            'print(result)  # 35',
        ]),
        Paragraph('Lambda and higher-order functions are core tools in functional programming style and are widely used in data analytics pipelines for data transformation and filtering.', S['answer']),
    ])
    story.extend(elems)

    elems = qa_block(10, 'Describe Python Functions in detail — types of arguments, decorators, recursion, scope rules.', [
        Paragraph('<b>INTRODUCTION:</b> A function is a named, reusable block of code that performs a specific task. Functions are defined with the <b>def</b> keyword and called by their name. They make code modular, readable, and maintainable. In Python, functions are first-class objects.', S['answer']),
        Paragraph('<b>SYNTAX:</b>', S['body_bold']),
        code_block([
            'def function_name(parameters):',
            '    """Docstring — describes what function does"""',
            '    # function body — code to execute',
            '    return value   # optional — returns result to caller',
        ]),
        Paragraph('<b>TYPES OF ARGUMENTS — ALL 5 TYPES:</b>', S['body_bold']),
        Paragraph('<b>1. POSITIONAL ARGUMENTS</b> — passed in exact order; position matters', S['bullet']),
        code_block(['def area(length, breadth): return length * breadth', 'area(5, 3)  # length=5, breadth=3 → 15']),
        Paragraph('<b>2. KEYWORD ARGUMENTS</b> — passed with parameter name; order doesn\'t matter', S['bullet']),
        code_block(['area(breadth=3, length=5)  # Same result → 15']),
        Paragraph('<b>3. DEFAULT ARGUMENTS</b> — have a preset value; optional when calling', S['bullet']),
        code_block(['def power(base, exp=2): return base ** exp', 'power(3)     # 9  — uses default exp=2', 'power(3, 3)  # 27 — overrides default']),
        Paragraph('<b>4. *args</b> — variable positional arguments (stored as tuple)', S['bullet']),
        code_block(['def sum_all(*nums): return sum(nums)', 'sum_all(1,2,3,4,5)  # 15 — any number of args']),
        Paragraph('<b>5. **kwargs</b> — variable keyword arguments (stored as dict)', S['bullet']),
        code_block(['def profile(**info): print(info)', 'profile(name="Alice", age=21, city="Delhi")', '# {"name":"Alice","age":21,"city":"Delhi"}']),
        Paragraph('<b>SCOPE RULES — LEGB:</b> Python searches variables in this order: Local → Enclosing → Global → Built-in.', S['body_bold']),
        code_block([
            'x = "global"',
            'def outer():',
            '    x = "enclosing"',
            '    def inner():',
            '        x = "local"',
            '        print(x)   # "local" — found in L scope',
            '    inner()',
            'outer()',
            '',
            '# global keyword — to modify global variable inside function',
            'count = 0',
            'def increment():',
            '    global count',
            '    count += 1',
        ]),
        Paragraph('<b>RECURSION:</b> A function that calls itself. MUST have a base case to stop infinite recursion.', S['body_bold']),
        code_block([
            'def fibonacci(n):',
            '    if n <= 1: return n                    # Base case',
            '    return fibonacci(n-1) + fibonacci(n-2) # Recursive call',
            '',
            'print([fibonacci(i) for i in range(8)])  # [0,1,1,2,3,5,8,13]',
        ]),
        Paragraph('<b>LAMBDA FUNCTIONS:</b> Anonymous one-line functions. lambda arguments: expression', S['body_bold']),
        code_block(['evens = list(filter(lambda x: x%2==0, range(10)))', 'square = lambda x: x**2']),
        Paragraph('<b>DECORATORS:</b> Decorators modify the behavior of a function without changing its source code. They use the @syntax.', S['body_bold']),
        code_block([
            'def uppercase(func):',
            '    def wrapper():',
            '        result = func()',
            '        return result.upper()',
            '    return wrapper',
            '',
            '@uppercase',
            'def greet(): return "hello"',
            'print(greet())  # "HELLO"',
            '',
            '# Built-in decorators: @staticmethod, @classmethod, @property',
        ]),
        Paragraph('<b>GENERATORS AND yield:</b> A generator function uses yield instead of return to produce values one at a time, saving memory. Ideal for large datasets in analytics.', S['body_bold']),
        code_block([
            'def count_up(n):',
            '    for i in range(1, n+1):',
            '        yield i   # Produces values one at a time',
            '',
            'for val in count_up(5):',
            '    print(val)  # 1 2 3 4 5',
        ]),
        Paragraph('<b>CONCLUSION:</b> Functions are the backbone of Python programming. Mastering argument types, scope, recursion, decorators, and lambda functions is essential for writing professional, Pythonic code and data analytics scripts.', S['answer']),
    ])
    story.extend(elems)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # TOPIC 4: FILE HANDLING
    # ══════════════════════════════════════════════════════════════════════════
    story.append(topic_header_box(4, 'FILE HANDLING IN PYTHON', 7))
    story.append(vspace(8))

    story.append(Paragraph('What is File Handling?', S['subtopic']))
    story.append(Paragraph(
        'File handling in Python allows you to <b>create, read, write, append, and delete</b> files '
        'stored on disk. Python provides a built-in <b>open()</b> function to work with files. '
        'Always close files after use — or use the <b>with</b> statement for automatic closing. '
        'File handling is critical in data analytics for reading datasets, saving results, and logging.', S['body']))
    story.append(vspace(4))
    story.append(colored_box(
        '⚠️ GOLDEN RULE: Always use "with open()" — it automatically closes the file even if '
        'an error occurs! This is safer than manually calling f.close().',
        LIGHT_RED, RED))
    story.append(vspace(6))

    story.append(Paragraph('File Modes — Complete Reference', S['subtopic']))
    story.append(simple_table(
        ['Mode', 'Description', 'File Exists?', 'File Not Found?'],
        [
            ['"r"', 'Read only (DEFAULT) — reads existing file', 'Reads normally', 'FileNotFoundError'],
            ['"w"', 'Write — creates new or OVERWRITES existing file completely', 'Overwrites!', 'Creates new file'],
            ['"a"', 'Append — adds to end of file without overwriting', 'Appends at end', 'Creates new file'],
            ['"x"', 'Exclusive create — error if file already exists', 'FileExistsError', 'Creates new file'],
            ['"r+"', 'Read AND Write — file must exist', 'Read+Write', 'FileNotFoundError'],
            ['"rb"', 'Read Binary — for images, PDFs, audio files', 'Reads binary', 'FileNotFoundError'],
            ['"wb"', 'Write Binary — for images, PDFs, audio files', 'Writes binary', 'Creates new file'],
        ],
        [1.5*cm, 6*cm, 3.5*cm, 4*cm]
    ))
    story.append(vspace(6))

    story.append(Paragraph('Reading and Writing Files', S['subtopic']))
    story.append(code_block([
        '# WRITING to a file (creates or overwrites)',
        'with open("data.txt", "w") as f:',
        '    f.write("Hello, World!\\n")      # write() — single string',
        '    f.write("Python File Handling\\n")',
        '    f.writelines(["Line 1\\n", "Line 2\\n"])  # Write list of strings',
        '',
        '# READING — entire file at once',
        'with open("data.txt", "r") as f:',
        '    content = f.read()         # Reads ALL content as single string',
        '    print(content)',
        '',
        '# READING — one line at a time',
        'with open("data.txt", "r") as f:',
        '    line = f.readline()        # Reads FIRST line',
        '    print(line.strip())        # strip() removes \\n',
        '',
        '# READING — all lines as a list',
        'with open("data.txt", "r") as f:',
        '    lines = f.readlines()      # Returns LIST of all lines',
        '    for line in lines:',
        '        print(line.strip())',
        '',
        '# APPENDING — adds to end without overwriting',
        'with open("data.txt", "a") as f:',
        '    f.write("New line added\\n")',
        '',
        '# Checking file existence before operations',
        'import os',
        'if os.path.exists("data.txt"):',
        '    print("File exists!")',
        '    os.remove("data.txt")    # Delete file',
        '',
        '# Working with CSV files',
        'import csv',
        'with open("students.csv", "w", newline="") as f:',
        '    writer = csv.writer(f)',
        '    writer.writerow(["Name","Age","Grade"])  # Header',
        '    writer.writerow(["Alice", 21, "A"])',
        '    writer.writerow(["Bob",   22, "B"])',
        '',
        'with open("students.csv", "r") as f:',
        '    reader = csv.reader(f)',
        '    for row in reader:',
        '        print(row)',
    ]))
    story.append(vspace(6))

    # Q&A File Handling
    story.append(hr(TEAL))
    story.append(Paragraph('📝 EXAM QUESTIONS — FILE HANDLING', S['subtopic']))

    elems = qa_block(1.5, 'What is the purpose of the "with" statement in file handling?', [
        Paragraph('The <b>"with"</b> statement (context manager) ensures the file is <b>automatically closed</b> after the block finishes, even if an exception occurs. It is safer and cleaner than manually calling f.close().', S['answer']),
        code_block(['with open("file.txt", "r") as f:', '    content = f.read()    # File auto-closes after this block', '# No need to call f.close() explicitly']),
        Paragraph('"with" runs __enter__ on open and __exit__ on close — handling cleanup automatically even on errors.', S['answer']),
    ])
    story.extend(elems)

    elems = qa_block(5, 'What is a file? Describe the various modes of operation in a file with examples.', [
        Paragraph('<b>WHAT IS A FILE?</b> A file is a named location on disk used to store data permanently. Unlike variables (which are in RAM and lost when program ends), files persist data. Python allows working with external files using the built-in <b>open()</b> function.', S['answer']),
        Paragraph('<b>Syntax:</b>  file_object = open("filename", mode)', S['body_bold']),
        Paragraph('<b>FILE MODES:</b>', S['body_bold']),
        Paragraph('• <b>"r"</b> — Read only (default); file must exist; raises FileNotFoundError if missing', S['bullet']),
        Paragraph('• <b>"w"</b> — Write; creates new file or OVERWRITES existing file completely; dangerous!', S['bullet']),
        Paragraph('• <b>"a"</b> — Append; adds new content to end without deleting old content; creates if not exists', S['bullet']),
        Paragraph('• <b>"x"</b> — Exclusive create; raises FileExistsError if file already exists; safest for new files', S['bullet']),
        Paragraph('• <b>"r+"</b> — Read AND Write; file must exist', S['bullet']),
        Paragraph('• <b>"rb", "wb"</b> — Binary modes for images, PDFs, audio files', S['bullet']),
        Paragraph('<b>WRITING TO A FILE:</b>', S['body_bold']),
        code_block(['with open("notes.txt", "w") as f:', '    f.write("Hello Python!\\n")', '    f.write("File Handling is easy.\\n")']),
        Paragraph('<b>READING FROM A FILE:</b>', S['body_bold']),
        code_block([
            'with open("notes.txt", "r") as f:',
            '    content = f.read()         # Read all at once',
            '',
            'with open("notes.txt", "r") as f:',
            '    line = f.readline()        # Read one line',
            '',
            'with open("notes.txt", "r") as f:',
            '    lines = f.readlines()      # List of all lines',
        ]),
        Paragraph('<b>APPENDING:</b>', S['body_bold']),
        code_block(['with open("notes.txt", "a") as f:', '    f.write("Appended line\\n")']),
        Paragraph('<b>CHECKING FILE EXISTENCE AND DELETION:</b>', S['body_bold']),
        code_block(['import os', 'if os.path.exists("notes.txt"):', '    os.remove("notes.txt")   # Delete file']),
        Paragraph('File handling is the backbone of data input/output in analytics — reading datasets, saving results, and logging program output.', S['answer']),
    ])
    story.extend(elems)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # TOPIC 5: CLASS & INSTANCE ATTRIBUTES
    # ══════════════════════════════════════════════════════════════════════════
    story.append(topic_header_box(5, 'CLASS & INSTANCE ATTRIBUTES', 9))
    story.append(vspace(8))

    story.append(Paragraph('Object-Oriented Programming (OOP) Basics', S['subtopic']))
    story.append(Paragraph(
        'OOP is a programming paradigm that organizes code around <b>objects</b> (real-world entities). '
        'A <b>class</b> is a blueprint/template for creating objects. An <b>object</b> (instance) is a '
        'specific realization of a class. Python supports OOP with class definitions using the <b>class</b> keyword. '
        'The four pillars of OOP are: <b>Encapsulation, Inheritance, Polymorphism, Abstraction</b>.', S['body']))
    story.append(vspace(6))

    story.append(Paragraph('Class Attributes vs Instance Attributes', S['subtopic']))
    story.append(simple_table(
        ['Feature', 'Class Attribute', 'Instance Attribute'],
        [
            ['Definition location', 'Inside class body, OUTSIDE any method', 'Inside __init__() using self'],
            ['Sharing', 'SHARED by ALL instances of the class', 'UNIQUE to each individual object'],
            ['Access', 'ClassName.attr or self.attr', 'Only via self.attr'],
            ['When to use', 'Data common to all objects (college name, species)', 'Data unique per object (name, age, marks)'],
            ['Memory', 'ONE copy in memory for all objects', 'ONE copy per object — more memory'],
            ['Change effect', 'Changing via class affects ALL instances', 'Changing one object does NOT affect others'],
        ],
        [3*cm, 5.5*cm, 5.5*cm]
    ))
    story.append(vspace(6))

    story.append(code_block([
        'class Student:',
        '    # CLASS ATTRIBUTE — shared by all instances',
        '    college = "ABC University"',
        '    count   = 0               # Tracks total number of students',
        '',
        '    def __init__(self, name, roll, marks):',
        '        # INSTANCE ATTRIBUTES — unique per object',
        '        self.name  = name',
        '        self.roll  = roll',
        '        self.marks = marks',
        '        Student.count += 1    # Increment class attribute',
        '',
        '    def display(self):',
        '        print(f"Name: {self.name}, Roll: {self.roll}, Marks: {self.marks}")',
        '        print(f"College: {Student.college}")',
        '',
        's1 = Student("Alice", 101, 92)',
        's2 = Student("Bob",   102, 85)',
        '',
        's1.display()           # Alice, 101, 92, ABC University',
        's2.display()           # Bob,   102, 85, ABC University',
        'print(Student.count)   # 2 — class attribute shared by all',
        'print(s1.college)      # "ABC University"',
        '',
        '# Changing class attribute affects ALL instances',
        'Student.college = "XYZ University"',
        'print(s1.college)  # "XYZ University"',
        'print(s2.college)  # "XYZ University"',
        '',
        '# But adding instance attr does NOT change class attr',
        's1.college = "PQR University"   # Creates instance attr for s1 only',
        'print(s1.college)  # "PQR University" — s1 own attr',
        'print(s2.college)  # "XYZ University" — class attr unchanged',
    ]))
    story.append(vspace(6))

    story.append(Paragraph('Types of Methods in a Class', S['subtopic']))
    story.append(simple_table(
        ['Method Type', 'Decorator', 'First Parameter', 'Can Access', 'When to Use'],
        [
            ['Instance Method', 'None (default)', 'self', 'Instance attrs + Class attrs', 'Most common — works on object data'],
            ['Class Method', '@classmethod', 'cls', 'Class attrs only (not instance)', 'Factory methods, modify class data'],
            ['Static Method', '@staticmethod', 'None (no self/cls)', 'Neither instance nor class attrs', 'Utility functions related to class'],
        ],
        [3*cm, 2.5*cm, 2.5*cm, 3.5*cm, 3.5*cm]
    ))
    story.append(vspace(4))
    story.append(code_block([
        'class MathHelper:',
        '    pi = 3.14159   # Class attribute',
        '',
        '    def __init__(self, value):',
        '        self.value = value     # Instance attribute',
        '',
        '    def show_value(self):           # Instance method',
        '        print(f"Value: {self.value}")',
        '',
        '    @classmethod',
        '    def circle_area(cls, r):        # Class method — uses cls.pi',
        '        return cls.pi * r * r',
        '',
        '    @staticmethod',
        '    def add(a, b):                  # Static method — no self/cls',
        '        return a + b',
        '',
        'm = MathHelper(10)',
        'm.show_value()                      # "Value: 10" — instance method',
        'print(MathHelper.circle_area(5))    # 78.539 — class method',
        'print(MathHelper.add(3, 4))         # 7 — static method',
    ]))
    story.append(vspace(6))

    # Q&A Class Attrs
    story.append(hr(TEAL))
    story.append(Paragraph('📝 EXAM QUESTIONS — CLASS & INSTANCE ATTRIBUTES', S['subtopic']))

    elems = qa_block(1.5, 'Differentiate between class attribute and instance attribute.', [
        Paragraph('<b>Class Attribute:</b> Shared by ALL objects of a class. Defined outside methods directly in the class body. Accessed via ClassName.attribute.', S['answer']),
        Paragraph('<b>Instance Attribute:</b> Unique to each object. Defined inside __init__() using self. Changes to one object do NOT affect others.', S['answer']),
        code_block(['class Dog:', '    species = "Canine"      # Class attr — shared by ALL dogs', '    def __init__(self, name):', '        self.name = name    # Instance attr — unique per dog', '', 'd1 = Dog("Buddy")', 'd2 = Dog("Max")', 'print(d1.name)     # "Buddy"', 'print(d2.name)     # "Max"', 'print(Dog.species) # "Canine" — same for all']),
    ])
    story.extend(elems)

    elems = qa_block(5, 'Explain class and instance attributes with @classmethod and @staticmethod examples in Python OOP.', [
        Paragraph('<b>OBJECT-ORIENTED PROGRAMMING:</b> OOP organizes code around objects. A class is a blueprint; an object is a real instance created from that blueprint. Python supports four OOP pillars: Encapsulation, Inheritance, Polymorphism, Abstraction.', S['answer']),
        Paragraph('<b>CLASS vs INSTANCE ATTRIBUTES:</b>', S['body_bold']),
        Paragraph('CLASS ATTRIBUTE: Defined at class level (outside methods). Shared by ALL objects — same value for all instances. Accessed as ClassName.attribute or self.attribute.', S['answer']),
        Paragraph('INSTANCE ATTRIBUTE: Defined inside __init__ using self. Each object has its OWN independent copy. Accessed only through self.', S['answer']),
        code_block([
            'class BankAccount:',
            '    bank_name     = "National Bank"   # Class attribute',
            '    interest_rate = 0.05               # Class attribute',
            '',
            '    def __init__(self, holder, balance):',
            '        self.holder  = holder           # Instance attribute',
            '        self.balance = balance          # Instance attribute',
            '',
            '    def deposit(self, amount):          # Instance method',
            '        self.balance += amount',
            '',
            '    def show(self):',
            '        print(f"{self.holder}: Rs.{self.balance} at {BankAccount.bank_name}")',
            '',
            'a1 = BankAccount("Alice", 10000)',
            'a2 = BankAccount("Bob",   25000)',
            'a1.deposit(5000)',
            'a1.show()  # Alice: Rs.15000 at National Bank',
        ]),
        Paragraph('<b>@CLASSMETHOD</b> — accesses and modifies class attributes using cls:', S['body_bold']),
        code_block([
            '    @classmethod',
            '    def change_rate(cls, new_rate):',
            '        cls.interest_rate = new_rate',
            '',
            'BankAccount.change_rate(0.07)  # Changes for ALL accounts',
        ]),
        Paragraph('<b>@STATICMETHOD</b> — no self/cls, independent utility function related to class:', S['body_bold']),
        code_block([
            '    @staticmethod',
            '    def validate_amount(amount):',
            '        return amount > 0   # Returns True if valid',
            '',
            'print(BankAccount.validate_amount(500))   # True',
            'print(BankAccount.validate_amount(-100))  # False',
        ]),
        Paragraph('<b>SUMMARY:</b> Instance method — takes self, accesses instance + class data. Class method — takes cls, accesses/modifies class data. Static method — no self/cls, pure utility helper function.', S['answer']),
    ])
    story.extend(elems)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # TOPIC 6: INHERITANCE
    # ══════════════════════════════════════════════════════════════════════════
    story.append(topic_header_box(6, 'INHERITANCE & MULTIPLE INHERITANCE', 12))
    story.append(colored_box('⚡ MOST IMPORTANT TOPIC — 12% Exam Probability — Guaranteed in Paper!', LIGHT_RED, RED, 'note'))
    story.append(vspace(8))

    story.append(Paragraph('What is Inheritance?', S['subtopic']))
    story.append(Paragraph(
        'Inheritance is one of the <b>four pillars of OOP</b>. It allows a <b>child class</b> (subclass) '
        'to acquire the properties and methods of a <b>parent class</b> (superclass) without rewriting the code. '
        'This promotes <b>code reuse</b>, <b>extensibility</b>, and <b>hierarchical relationships</b> between classes. '
        'The child class can also <b>override</b> parent methods to provide its own specific implementation. '
        'Inheritance models IS-A relationships: Dog IS-A Animal, Car IS-A Vehicle.', S['body']))
    story.append(vspace(6))

    story.append(Paragraph('Types of Inheritance — Complete Guide', S['subtopic']))
    story.append(simple_table(
        ['Type', 'Description', 'Structure', 'Example'],
        [
            ['Single', 'One child, one parent — simplest form', 'Child → Parent', 'Dog → Animal'],
            ['Multilevel', 'Chain: Child → Parent → Grandparent', 'GrandChild → Child → Parent', 'GrandChild → Child → Parent'],
            ['Multiple', 'One child inherits from MULTIPLE parents', 'C(A, B) → A and B', 'C(Father, Mother)'],
            ['Hierarchical', 'Multiple children share ONE parent', 'Dog, Cat → Animal', 'Dog, Cat, Fish → Animal'],
            ['Hybrid', 'Combination of multiple inheritance types', 'Mix of above', 'Mix of multiple + multilevel'],
        ],
        [2.5*cm, 4*cm, 4*cm, 4.5*cm]
    ))
    story.append(vspace(6))

    story.append(Paragraph('Single Inheritance — Example', S['subtopic']))
    story.append(code_block([
        'class Animal:                          # Parent class',
        '    def __init__(self, name, sound):',
        '        self.name  = name',
        '        self.sound = sound',
        '',
        '    def speak(self):',
        '        print(f"{self.name} says {self.sound}")',
        '',
        '    def breathe(self):',
        '        print(f"{self.name} breathes oxygen")',
        '',
        '',
        'class Dog(Animal):                     # Child class inherits from Animal',
        '    def __init__(self, name, breed):',
        '        super().__init__(name, "Woof") # Call parent __init__',
        '        self.breed = breed             # Additional attribute',
        '',
        '    def fetch(self):                   # New method in child',
        '        print(f"{self.name} fetches the ball!")',
        '',
        '',
        'd = Dog("Buddy", "Labrador")',
        'd.speak()   # Inherited from Animal: Buddy says Woof',
        'd.breathe() # Inherited: Buddy breathes oxygen',
        'd.fetch()   # Own method: Buddy fetches the ball!',
    ]))
    story.append(vspace(6))

    story.append(Paragraph('Multiple Inheritance — Example', S['subtopic']))
    story.append(Paragraph(
        '<b>Multiple Inheritance</b> allows a class to inherit from MORE THAN ONE parent class. '
        'The child class gets access to methods and attributes of ALL parent classes. '
        'Python handles method resolution using <b>MRO (C3 Linearization)</b> algorithm.', S['body']))
    story.append(code_block([
        'class Father:',
        '    def work(self):  print("Father works")',
        '    def cook(self):  print("Father can cook")',
        '',
        'class Mother:',
        '    def cook(self):  print("Mother cooks better")  # Same method name!',
        '    def nurture(self): print("Mother nurtures")',
        '',
        'class Child(Father, Mother):  # Inherits from BOTH (Father listed first)',
        '    def play(self): print("Child plays")',
        '',
        'c = Child()',
        'c.work()    # From Father: "Father works"',
        'c.cook()    # From Father (listed FIRST in MRO) — "Father can cook"',
        'c.nurture() # From Mother: "Mother nurtures"',
        'c.play()    # Own method: "Child plays"',
        '',
        'print(Child.__mro__)  # [Child, Father, Mother, object]',
    ]))
    story.append(vspace(6))

    story.append(Paragraph('Multilevel Inheritance', S['subtopic']))
    story.append(code_block([
        'class GrandParent:',
        '    def cook(self): print("GrandParent cooks")',
        '',
        'class Parent(GrandParent):',
        '    def work(self): print("Parent works")',
        '',
        'class Child(Parent):         # Child inherits Parent who inherits GrandParent',
        '    def play(self): print("Child plays")',
        '',
        'c = Child()',
        'c.cook()   # Inherited from GrandParent',
        'c.work()   # Inherited from Parent',
        'c.play()   # Own method',
    ]))
    story.append(vspace(6))

    story.append(Paragraph('Method Overriding', S['subtopic']))
    story.append(Paragraph(
        '<b>Method Overriding</b> occurs when a child class provides its OWN implementation of a method '
        'already defined in the parent class. The child\'s version takes priority. '
        'The parent\'s version can still be called using <b>super()</b>. '
        'This is the basis of <b>polymorphism</b> — same method name, different behaviors.', S['body']))
    story.append(code_block([
        'class Shape:',
        '    def area(self): return 0',
        '    def describe(self): print(f"I am a shape with area {self.area()}")',
        '',
        'class Circle(Shape):',
        '    def __init__(self, r): self.r = r',
        '    def area(self): return 3.14 * self.r ** 2   # OVERRIDES Shape.area',
        '',
        'class Rectangle(Shape):',
        '    def __init__(self, l, w): self.l, self.w = l, w',
        '    def area(self): return self.l * self.w       # OVERRIDES Shape.area',
        '',
        '# POLYMORPHISM — same method, different behaviors',
        'shapes = [Circle(5), Rectangle(4, 6)]',
        'for s in shapes:',
        '    print(s.area())     # 78.5 then 24',
        '    s.describe()        # Inherited from Shape, calls overridden area()',
    ]))
    story.append(vspace(6))

    story.append(Paragraph('super() — Accessing Parent Class', S['subtopic']))
    story.append(Paragraph(
        '<b>super()</b> is a built-in function that returns a proxy object representing the parent class. '
        'It is used to call the parent\'s methods from within the child class, especially in __init__(). '
        'super() avoids hardcoding the parent class name and works correctly with MRO in multiple inheritance.', S['body']))
    story.append(code_block([
        'class Employee:',
        '    def __init__(self, name, salary):',
        '        self.name   = name',
        '        self.salary = salary',
        '',
        '    def show(self):',
        '        print(f"Employee: {self.name}, Salary: {self.salary}")',
        '',
        'class Manager(Employee):',
        '    def __init__(self, name, salary, team_size):',
        '        super().__init__(name, salary)   # Calls Employee.__init__',
        '        self.team_size = team_size       # Additional attribute',
        '',
        '    def show(self):',
        '        super().show()                   # Calls Employee.show()',
        '        print(f"Team Size: {self.team_size}")',
        '',
        'm = Manager("Alice", 80000, 10)',
        'm.show()',
        '# Employee: Alice, Salary: 80000',
        '# Team Size: 10',
        '',
        '# Useful functions for inheritance',
        'print(isinstance(m, Manager))    # True',
        'print(isinstance(m, Employee))   # True — due to inheritance!',
        'print(issubclass(Manager, Employee))  # True',
    ]))
    story.append(vspace(6))

    # Q&A Inheritance
    story.append(hr(TEAL))
    story.append(Paragraph('📝 EXAM QUESTIONS — INHERITANCE', S['subtopic']))

    elems = qa_block(1.5, 'What is inheritance in Python? Name its types.', [
        Paragraph('Inheritance is an OOP feature where a <b>child class</b> acquires properties and methods of a <b>parent class</b>, enabling <b>code reuse</b>. Types: <b>Single</b> (one parent), <b>Multiple</b> (many parents), <b>Multilevel</b> (chain), <b>Hierarchical</b> (one parent many children), <b>Hybrid</b> (combination).', S['answer']),
        code_block(['class Child(Parent): pass  # Single inheritance', 'class C(A, B): pass        # Multiple inheritance']),
        Paragraph('Child inherits all non-private members of Parent. Use super() to call parent methods.', S['answer']),
    ])
    story.extend(elems)

    elems = qa_block(1.5, 'What are Inheritance types in Python?', [
        Paragraph('<b>Five types of inheritance in Python:</b>', S['answer']),
        Paragraph('1. <b>Single</b> — One child, one parent: class Dog(Animal)', S['bullet']),
        Paragraph('2. <b>Multiple</b> — One child, multiple parents: class C(A, B)', S['bullet']),
        Paragraph('3. <b>Multilevel</b> — Chain of inheritance: GrandChild → Child → Parent', S['bullet']),
        Paragraph('4. <b>Hierarchical</b> — Multiple children, one parent: Dog, Cat both inherit Animal', S['bullet']),
        Paragraph('5. <b>Hybrid</b> — Combination of multiple types; handled by Python\'s MRO (C3 Algorithm)', S['bullet']),
    ])
    story.extend(elems)

    elems = qa_block(10, 'Explain all types of inheritance in Python with examples and super() usage.', [
        Paragraph('<b>INTRODUCTION:</b> Inheritance allows a child class (subclass) to inherit attributes and methods from a parent class (superclass). This promotes code reuse, modularity, and establishes IS-A relationships (Dog IS-A Animal). Python supports 5 types of inheritance.', S['answer']),
        Paragraph('<b>1. SINGLE INHERITANCE — one child, one parent:</b>', S['body_bold']),
        code_block(['class Animal:', '    def breathe(self): print("Breathing...")', 'class Dog(Animal):', '    def bark(self): print("Woof!")', '', 'd = Dog()', 'd.breathe()  # Inherited from Animal', 'd.bark()     # Own method']),
        Paragraph('<b>2. MULTILEVEL INHERITANCE — chain of classes:</b>', S['body_bold']),
        code_block(['class GrandParent:', '    def cook(self): print("GrandParent cooks")', 'class Parent(GrandParent):', '    def work(self): print("Parent works")', 'class Child(Parent):', '    def play(self): print("Child plays")', '', 'c = Child()', 'c.cook()   # From GrandParent', 'c.work()   # From Parent', 'c.play()   # Own method']),
        Paragraph('<b>3. MULTIPLE INHERITANCE — one child, multiple parents:</b>', S['body_bold']),
        code_block(['class A:', '    def show(self): print("From A")', 'class B:', '    def display(self): print("From B")', 'class C(A, B):     # Inherits from both', '    def info(self): print("From C")', '', 'obj = C()', 'obj.show()     # From A', 'obj.display()  # From B', 'obj.info()     # From C']),
        Paragraph('<b>4. HIERARCHICAL INHERITANCE — multiple children, one parent:</b>', S['body_bold']),
        code_block(['class Animal:', '    def breathe(self): print("Breathes")', 'class Cat(Animal):', '    def meow(self): print("Meow!")', 'class Dog(Animal):', '    def bark(self): print("Woof!")', '', '# Both Cat and Dog inherit breathe() from Animal']),
        Paragraph('<b>5. HYBRID INHERITANCE — combination:</b> Mix of Multiple + Multilevel (or other types). Python handles via MRO.', S['body_bold']),
        Paragraph('<b>METHOD OVERRIDING:</b> When child defines same method as parent, child\'s version is called.', S['body_bold']),
        code_block(['class Bird:', '    def sound(self): return "Generic sound"', 'class Parrot(Bird):', '    def sound(self): return "Hello!"     # Overrides', 'class Crow(Bird):', '    def sound(self): return "Caw Caw!"  # Overrides', '', 'birds = [Parrot(), Crow()]', 'for b in birds: print(b.sound())  # Polymorphism!']),
        Paragraph('<b>super() FUNCTION:</b> Calls parent methods without naming parent explicitly.', S['body_bold']),
        code_block(['class Employee:', '    def __init__(self, name, salary):', '        self.name = name; self.salary = salary', '    def show(self): print(f"Employee: {self.name}, Rs.{self.salary}")', '', 'class Manager(Employee):', '    def __init__(self, name, salary, team_size):', '        super().__init__(name, salary)   # Calls Employee.__init__', '        self.team_size = team_size', '    def show(self):', '        super().show()                    # Calls Employee.show()', '        print(f"Team: {self.team_size}")', '', 'm = Manager("Alice", 80000, 10)', 'm.show()', '# Employee: Alice, Rs.80000', '# Team: 10']),
        Paragraph('<b>isinstance() and issubclass():</b>', S['body_bold']),
        code_block(['print(isinstance(m, Manager))      # True', 'print(isinstance(m, Employee))     # True — due to inheritance!', 'print(issubclass(Manager, Employee)) # True']),
        Paragraph('<b>CONCLUSION:</b> Inheritance is fundamental to OOP design. It models real-world hierarchies, reduces code duplication, and supports polymorphism. Python\'s support for multiple and multilevel inheritance with MRO makes it one of the most powerful OOP languages.', S['answer']),
    ])
    story.extend(elems)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # TOPIC 7: MRO
    # ══════════════════════════════════════════════════════════════════════════
    story.append(topic_header_box(7, 'METHOD RESOLUTION ORDER (MRO)', 8))
    story.append(vspace(8))

    story.append(Paragraph('What is MRO?', S['subtopic']))
    story.append(Paragraph(
        '<b>Method Resolution Order (MRO)</b> defines the <b>ORDER</b> in which Python searches for '
        'a method or attribute when there is inheritance involved — especially in multiple inheritance. '
        'Python uses the <b>C3 Linearization Algorithm</b> (also called C3 superclass linearization) '
        'to determine MRO. It ensures a consistent, predictable order. '
        'You can check MRO using <b>ClassName.mro()</b> or <b>ClassName.__mro__</b>.', S['body']))
    story.append(vspace(4))
    story.append(colored_box(
        '🔑 MRO Rules: (1) Child class always comes BEFORE its parents. '
        '(2) Parents listed LEFT to RIGHT take priority. '
        '(3) A class appears in MRO only AFTER all classes that depend on it.',
        LIGHT_PURPLE, PURPLE))
    story.append(vspace(6))

    story.append(Paragraph('The Diamond Problem — Why MRO Matters', S['subtopic']))
    story.append(Paragraph(
        'The <b>Diamond Problem</b> occurs in multiple inheritance when a class inherits from two classes '
        'that both inherit from a common base class. Without MRO, it\'s unclear which parent\'s method '
        'to call. Python solves this elegantly with <b>C3 Linearization</b>.', S['body']))
    story.append(code_block([
        'class A:',
        '    def show(self): print("A")',
        '',
        'class B(A):',
        '    def show(self): print("B")',
        '',
        'class C(A):',
        '    def show(self): print("C")',
        '',
        'class D(B, C):  # Diamond: D→B→A and D→C→A',
        '    pass',
        '',
        'd = D()',
        'd.show()         # Output: "B" (follows MRO — B comes before C)',
        '',
        'print(D.mro())   # [D, B, C, A, object]',
        'print(D.__mro__) # Same as tuple: (<D>, <B>, <C>, <A>, <object>)',
        '',
        '# MRO ORDER: D → B → C → A → object',
        '# Python searches: D (not found) → B (found!) → calls B.show()',
    ]))
    story.append(vspace(6))

    story.append(Paragraph('C3 Linearization Formula', S['subtopic']))
    story.append(Paragraph(
        'The C3 algorithm computes MRO as: <b>Class itself + merge of parents\' MROs + list of parents</b>. '
        'The "merge" step picks the first element that does NOT appear in the TAIL of any other list:', S['body']))
    story.append(code_block([
        '# For class D(B, C):',
        '# L[D] = D + merge(L[B], L[C], [B, C])',
        '# L[B] = [B, A, object]',
        '# L[C] = [C, A, object]',
        '',
        '# Step 1: First of L[B] is B — not in tail of any list → pick B',
        '# Step 2: First of L[B] now is A — A IS in tail of [C,A,object] → skip',
        '#         First of L[C] is C — not in tail of any remaining → pick C',
        '# Step 3: First of L[B] is A — now not in any tail → pick A',
        '# Step 4: object',
        '',
        '# Result: D → B → C → A → object   ✓',
        '',
        '# More complex example',
        'class X: pass',
        'class Y(X): pass',
        'class Z(X): pass',
        'class W(Y, Z): pass',
        '',
        'print(W.mro())',
        '# [W, Y, Z, X, object]',
    ]))
    story.append(vspace(6))

    # Q&A MRO
    story.append(hr(TEAL))
    story.append(Paragraph('📝 EXAM QUESTIONS — MRO', S['subtopic']))

    elems = qa_block(1.5, 'What is MRO in Python? Which algorithm is used?', [
        Paragraph('<b>MRO (Method Resolution Order)</b> defines the order in which Python searches classes when a method is called in an inheritance hierarchy. Python uses the <b>C3 Linearization Algorithm</b> to compute MRO.', S['answer']),
        Paragraph('Check MRO using <b>ClassName.mro()</b> or <b>ClassName.__mro__</b>. MRO ensures child class always comes before parent class and parents are searched left-to-right.', S['answer']),
    ])
    story.extend(elems)

    elems = qa_block(5, 'Explain MRO and the Diamond Problem in Python with C3 Linearization.', [
        Paragraph('<b>METHOD RESOLUTION ORDER (MRO):</b> When Python encounters a method call, it needs to know WHICH class\'s method to use — especially in complex inheritance trees. MRO defines the precise search order using the <b>C3 Linearization Algorithm</b> (introduced Python 2.3).', S['answer']),
        Paragraph('<b>Guarantees:</b> Consistent left-to-right ordering of parents | Child always comes before parent | Monotonicity — order is preserved throughout.', S['answer']),
        Paragraph('<b>THE DIAMOND PROBLEM:</b>', S['body_bold']),
        code_block([
            'class A:',
            '    def method(self): print("Method from A")',
            'class B(A):',
            '    def method(self): print("Method from B")',
            'class C(A):',
            '    def method(self): print("Method from C")',
            'class D(B, C): pass   # Diamond — both B and C inherit from A',
            '',
            'd = D()',
            'd.method()            # "Method from B" — B comes first in MRO',
            'print(D.mro())',
            '# [D, B, C, A, object]',
        ]),
        Paragraph('<b>MRO for D is: D → B → C → A → object</b>. Python first looks in D (not found), then B (found!) → calls B\'s method.', S['answer']),
        Paragraph('<b>C3 LINEARIZATION:</b> L[D(B,C)] = D + merge(L[B], L[C], [B,C]) → Result: D, B, C, A, object', S['answer']),
        Paragraph('<b>CHECKING MRO:</b>', S['body_bold']),
        code_block(['print(D.__mro__)  # Tuple of class hierarchy', 'print(D.mro())    # List version']),
        Paragraph('<b>USING super() WITH MRO:</b> super() follows the correct MRO chain even in complex hierarchies, making Python\'s multiple inheritance safe and predictable.', S['answer']),
    ])
    story.extend(elems)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # TOPIC 8: MAGIC METHODS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(topic_header_box(8, 'MAGIC METHODS & OPERATOR OVERLOADING', 10))
    story.append(vspace(8))

    story.append(Paragraph('What are Magic Methods (Dunder Methods)?', S['subtopic']))
    story.append(Paragraph(
        '<b>Magic methods</b> (also called <b>dunder methods</b> — Double UNDERscore) are special methods '
        'in Python with names surrounded by double underscores like <b>__init__</b>, <b>__str__</b>, '
        '<b>__len__</b>, <b>__add__</b>, etc. They are NOT called directly — Python calls them '
        '<b>AUTOMATICALLY</b> in response to specific operations. For example, when you write <b>a + b</b>, '
        'Python internally calls <b>a.__add__(b)</b>. Magic methods allow you to define how your custom '
        'objects behave with built-in Python syntax.', S['body']))
    story.append(colored_box(
        '⚡ RULE: Dunder methods are NEVER called directly by the programmer. '
        'They are triggered AUTOMATICALLY by Python\'s syntax and built-in functions.',
        LIGHT_PURPLE, PURPLE))
    story.append(vspace(6))

    story.append(Paragraph('Complete Table of Important Magic Methods', S['subtopic']))
    story.append(simple_table(
        ['Magic Method', 'Triggered By', 'Purpose'],
        [
            ['__init__(self,...)', 'obj = MyClass()', 'Constructor — initialize object attributes'],
            ['__str__(self)', 'str(obj) or print(obj)', 'Human-readable string representation'],
            ['__repr__(self)', 'repr(obj) or in shell', 'Developer/debug string — how to recreate object'],
            ['__len__(self)', 'len(obj)', 'Return length/size of object'],
            ['__add__(self,other)', 'obj1 + obj2', 'Addition operator +'],
            ['__sub__(self,other)', 'obj1 - obj2', 'Subtraction operator -'],
            ['__mul__(self,other)', 'obj1 * obj2', 'Multiplication operator *'],
            ['__truediv__(self,other)', 'obj1 / obj2', 'Division operator /'],
            ['__eq__(self,other)', 'obj1 == obj2', 'Equality comparison =='],
            ['__lt__(self,other)', 'obj1 < obj2', 'Less than comparison <'],
            ['__gt__(self,other)', 'obj1 > obj2', 'Greater than comparison >'],
            ['__le__(self,other)', 'obj1 <= obj2', 'Less than or equal <='],
            ['__ge__(self,other)', 'obj1 >= obj2', 'Greater than or equal >='],
            ['__ne__(self,other)', 'obj1 != obj2', 'Not equal comparison !='],
            ['__contains__(self,item)', 'item in obj', 'Membership test (in operator)'],
            ['__getitem__(self,key)', 'obj[key]', 'Subscript/indexing access'],
            ['__setitem__(self,key,val)', 'obj[key] = val', 'Subscript assignment'],
            ['__delitem__(self,key)', 'del obj[key]', 'Subscript deletion'],
            ['__iter__(self)', 'for x in obj:', 'Iterator protocol — make iterable'],
            ['__next__(self)', 'next(obj)', 'Return next item in iterator'],
            ['__call__(self,...)', 'obj(...)', 'Make object callable like a function'],
            ['__del__(self)', 'del obj', 'Destructor — cleanup when object destroyed'],
            ['__bool__(self)', 'bool(obj) or if obj:', 'Boolean truth value of object'],
            ['__hash__(self)', 'hash(obj)', 'Hash value for use as dict key'],
        ],
        [4*cm, 3.5*cm, 7.5*cm]
    ))
    story.append(vspace(6))

    story.append(Paragraph('Operator Overloading — Complete Example', S['subtopic']))
    story.append(Paragraph(
        '<b>Operator Overloading</b> means redefining how standard Python operators (+, -, *, ==, <, >, etc.) '
        'work for your custom classes. This makes your objects behave like built-in types.', S['body']))
    story.append(code_block([
        'class Vector:',
        '    def __init__(self, x, y):',
        '        self.x = x',
        '        self.y = y',
        '',
        '    def __str__(self):            # Called by print(v) or str(v)',
        '        return f"Vector({self.x}, {self.y})"',
        '',
        '    def __repr__(self):           # Called by repr(v) — for debugging',
        '        return f"Vector(x={self.x}, y={self.y})"',
        '',
        '    def __add__(self, other):     # v1 + v2',
        '        return Vector(self.x + other.x, self.y + other.y)',
        '',
        '    def __sub__(self, other):     # v1 - v2',
        '        return Vector(self.x - other.x, self.y - other.y)',
        '',
        '    def __mul__(self, scalar):    # v1 * 3 (scalar multiplication)',
        '        return Vector(self.x * scalar, self.y * scalar)',
        '',
        '    def __eq__(self, other):      # v1 == v2',
        '        return self.x == other.x and self.y == other.y',
        '',
        '    def __lt__(self, other):      # v1 < v2 (compare magnitudes)',
        '        return (self.x**2 + self.y**2) < (other.x**2 + other.y**2)',
        '',
        '    def __len__(self):            # len(v) — returns magnitude as int',
        '        return int((self.x**2 + self.y**2) ** 0.5)',
        '',
        '    def __bool__(self):           # bool(v) — True if non-zero vector',
        '        return self.x != 0 or self.y != 0',
        '',
        '',
        'v1 = Vector(3, 4)',
        'v2 = Vector(1, 2)',
        '',
        'print(v1 + v2)    # Vector(4, 6)',
        'print(v1 - v2)    # Vector(2, 2)',
        'print(v1 * 2)     # Vector(6, 8)',
        'print(v1 == v2)   # False',
        'print(v1 < v2)    # False (25 > 5)',
        'print(len(v1))    # 5 (magnitude of 3,4,5 right triangle)',
        'print(str(v1))    # Vector(3, 4)',
        'print(bool(v1))   # True (non-zero)',
    ]))
    story.append(vspace(6))

    # Q&A Magic Methods
    story.append(hr(TEAL))
    story.append(Paragraph('📝 EXAM QUESTIONS — MAGIC METHODS', S['subtopic']))

    elems = qa_block(1.5, 'What are dunder/magic methods in Python? Give two examples.', [
        Paragraph('<b>Magic methods</b> (dunder methods) are special Python methods with <b>double underscores</b> on both sides. Python calls them <b>automatically</b> in response to specific operations or syntax.', S['answer']),
        Paragraph('• <b>__init__</b> is called automatically when creating an object: obj = MyClass()', S['bullet']),
        Paragraph('• <b>__str__</b> is called by print(obj) or str(obj) to return a string representation', S['bullet']),
        Paragraph('• <b>__add__</b> is called when using + operator: obj1 + obj2', S['bullet']),
    ])
    story.extend(elems)

    elems = qa_block(1.5, 'List 3 magic methods in Python.', [
        Paragraph('Three important magic (dunder) methods in Python:', S['answer']),
        Paragraph('1. <b>__init__(self, ...)</b> — Constructor; automatically called when object is created; used to initialize instance attributes.', S['bullet']),
        Paragraph('2. <b>__str__(self)</b> — Called by print() and str(); returns human-readable string representation of object.', S['bullet']),
        Paragraph('3. <b>__len__(self)</b> — Called by len(); returns integer representing size/length of object.', S['bullet']),
    ])
    story.extend(elems)

    elems = qa_block(15, 'Explain Magic Methods and Operator Overloading in Python in detail with complete examples.', [
        Paragraph('<b>INTRODUCTION:</b> Magic methods (dunder methods) are predefined methods in Python that allow custom class objects to respond to Python\'s built-in operations and syntax. They make user-defined classes behave like built-in types (int, list, string, etc.). Every operator in Python has a corresponding magic method. When you write a + b, Python internally calls a.__add__(b). This mechanism is called OPERATOR OVERLOADING.', S['answer']),
        Paragraph('<b>OBJECT LIFECYCLE MAGIC METHODS:</b>', S['body_bold']),
        code_block([
            'class MyClass:',
            '    def __init__(self, val):',
            '        self.val = val',
            '        print(f"Object created with val={val}")   # __init__',
            '',
            '    def __del__(self):',
            '        print(f"Object with val={self.val} destroyed")  # __del__',
            '',
            'obj = MyClass(10)   # Triggers __init__',
            'del obj             # Triggers __del__',
        ]),
        Paragraph('<b>STRING REPRESENTATION METHODS:</b>', S['body_bold']),
        Paragraph('• <b>__str__:</b> Called by str(obj) or print(obj) — user-friendly output', S['bullet']),
        Paragraph('• <b>__repr__:</b> Called by repr(obj) — developer/debug output; should show how to recreate the object', S['bullet']),
        code_block([
            'class Book:',
            '    def __init__(self, title, author, price):',
            '        self.title  = title',
            '        self.author = author',
            '        self.price  = price',
            '',
            '    def __str__(self):',
            '        return f\'"{self.title}" by {self.author} - Rs.{self.price}\'',
            '',
            '    def __repr__(self):',
            '        return f\'Book("{self.title}", "{self.author}", {self.price})\'',
            '',
            'b = Book("Python Pro", "Alice", 499)',
            'print(b)        # "Python Pro" by Alice - Rs.499',
            'print(repr(b))  # Book("Python Pro", "Alice", 499)',
        ]),
        Paragraph('<b>ARITHMETIC OPERATOR OVERLOADING:</b>', S['body_bold']),
        code_block([
            'class Fraction:',
            '    def __init__(self, num, den):',
            '        self.num = num; self.den = den',
            '',
            '    def __str__(self): return f"{self.num}/{self.den}"',
            '',
            '    def __add__(self, other):     # Overloads +',
            '        n = self.num*other.den + other.num*self.den',
            '        d = self.den * other.den',
            '        return Fraction(n, d)',
            '',
            '    def __sub__(self, other):     # Overloads -',
            '        n = self.num*other.den - other.num*self.den',
            '        d = self.den * other.den',
            '        return Fraction(n, d)',
            '',
            '    def __mul__(self, other):     # Overloads *',
            '        return Fraction(self.num*other.num, self.den*other.den)',
            '',
            'f1 = Fraction(1,2); f2 = Fraction(1,3)',
            'print(f1 + f2)  # 5/6',
            'print(f1 - f2)  # 1/6',
            'print(f1 * f2)  # 1/6',
        ]),
        Paragraph('<b>COMPARISON OPERATOR OVERLOADING:</b>', S['body_bold']),
        code_block([
            'class Student:',
            '    def __init__(self, name, marks):',
            '        self.name  = name',
            '        self.marks = marks',
            '',
            '    def __eq__(self, other): return self.marks == other.marks  # ==',
            '    def __lt__(self, other): return self.marks <  other.marks  # <',
            '    def __gt__(self, other): return self.marks >  other.marks  # >',
            '    def __le__(self, other): return self.marks <= other.marks  # <=',
            '    def __ge__(self, other): return self.marks >= other.marks  # >=',
            '    def __str__(self): return f"{self.name}:{self.marks}"',
            '',
            's1 = Student("Alice", 90); s2 = Student("Bob", 85)',
            'print(s1 > s2)   # True',
            'print(s1 == s2)  # False',
            'students = [s2, s1]; students.sort()  # Uses __lt__',
            'print([str(s) for s in students])  # ["Bob:85","Alice:90"]',
        ]),
        Paragraph('<b>CONTAINER/SEQUENCE MAGIC METHODS:</b>', S['body_bold']),
        code_block([
            'class NumberCollection:',
            '    def __init__(self, *nums): self.nums = list(nums)',
            '    def __len__(self):         return len(self.nums)',
            '    def __getitem__(self, idx):return self.nums[idx]',
            '    def __setitem__(self, idx, val): self.nums[idx] = val',
            '    def __contains__(self, item):    return item in self.nums',
            '    def __iter__(self):         return iter(self.nums)',
            '    def __str__(self):          return str(self.nums)',
            '',
            'nc = NumberCollection(1, 2, 3, 4, 5)',
            'print(len(nc))        # 5',
            'print(nc[2])          # 3',
            'print(3 in nc)        # True',
            'for n in nc: print(n, end=" ")  # 1 2 3 4 5',
        ]),
        Paragraph('<b>CALLABLE OBJECTS — __call__:</b> Makes an object callable like a function!', S['body_bold']),
        code_block([
            'class Multiplier:',
            '    def __init__(self, factor): self.factor = factor',
            '    def __call__(self, value): return value * self.factor',
            '',
            'triple = Multiplier(3)',
            'print(triple(5))   # 15 — object called like a function!',
            'print(triple(10))  # 30',
        ]),
        Paragraph('<b>CONTEXT MANAGER — __enter__ and __exit__:</b> Used with "with" statement for automatic resource management.', S['body_bold']),
        code_block([
            'class FileManager:',
            '    def __init__(self, name, mode): self.name=name; self.mode=mode',
            '    def __enter__(self):', 
            '        self.file = open(self.name, self.mode); return self.file',
            '    def __exit__(self, exc_type, exc_val, exc_tb):',
            '        self.file.close()',
            '',
            'with FileManager("test.txt", "w") as f:',
            '    f.write("Using context manager!")',
            '# File automatically closed after with block',
        ]),
        Paragraph('<b>CONCLUSION:</b> Magic methods transform custom classes into first-class Python citizens. They allow custom objects to support arithmetic, comparison, indexing, iteration, string conversion, and much more — using standard Python syntax. Operator overloading is heavily used in libraries like NumPy and Pandas to make mathematical operations intuitive.', S['answer']),
    ])
    story.extend(elems)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # TOPIC 9: METACLASSES
    # ══════════════════════════════════════════════════════════════════════════
    story.append(topic_header_box(9, 'METACLASSES IN PYTHON', 7))
    story.append(vspace(8))

    story.append(Paragraph('What is a Metaclass?', S['subtopic']))
    story.append(Paragraph(
        'In Python, <b>everything is an object</b> — including classes. A <b>metaclass</b> is the '
        '<b>class of a class</b>. Just as an object is an instance of a class, a class is an instance '
        'of its metaclass. By default, the metaclass for all Python classes is <b>type</b>. '
        'Metaclasses allow you to control class <b>CREATION</b> — you can intercept class creation, '
        'modify class attributes, enforce rules (like interfaces), add methods automatically, etc. '
        'Used in frameworks like Django and SQLAlchemy.', S['body']))
    story.append(colored_box(
        '🔑 MEMORY HIERARCHY: Object → instance of → Class → instance of → Metaclass (type)\n'
        'type is Python\'s default metaclass. type(42) → <class int>. type(int) → <class type>.',
        LIGHT_ORANGE, ORANGE))
    story.append(vspace(6))

    story.append(code_block([
        '# type — The built-in metaclass',
        'class Dog:',
        '    def bark(self): print("Woof!")',
        '',
        'print(type(Dog))    # <class "type"> — Dog\'s metaclass is type',
        'print(type(42))     # <class "int">',
        'print(type("hello"))# <class "str">',
        'print(type(type))   # <class "type"> — type is its OWN metaclass!',
        '',
        '# Create a class DYNAMICALLY using type()',
        '# Syntax: type(class_name, bases_tuple, attributes_dict)',
        'Cat = type("Cat", (), {"sound": "Meow",',
        '                        "speak": lambda self: print("Meow!")})',
        'c = Cat()',
        'c.speak()           # Meow!',
        'print(Cat.sound)    # Meow',
        '',
        '# Dynamic subclass',
        'Animal = type("Animal", (), {"breathe": lambda self: print("Breathing")})',
        'Dog2   = type("Dog2", (Animal,), {"bark": lambda self: print("Woof!")})',
        'd = Dog2()',
        'd.breathe()  # From Animal',
        'd.bark()     # From Dog2',
    ]))
    story.append(vspace(6))

    story.append(Paragraph('Custom Metaclass', S['subtopic']))
    story.append(code_block([
        '# Custom metaclass — converts all method names to UPPERCASE',
        'class MyMeta(type):',
        '    def __new__(mcs, name, bases, attrs):',
        '        uppercase_attrs = {}',
        '        for key, val in attrs.items():',
        '            if not key.startswith("__"):   # Skip dunder methods',
        '                uppercase_attrs[key.upper()] = val',
        '            else:',
        '                uppercase_attrs[key] = val',
        '        return super().__new__(mcs, name, bases, uppercase_attrs)',
        '',
        'class MyClass(metaclass=MyMeta):',
        '    def hello(self):',
        '        print("Hello!")',
        '',
        'obj = MyClass()',
        'obj.HELLO()   # Method was renamed to uppercase!',
        '',
        '# Validation metaclass — enforce all methods are lowercase',
        'class ValidationMeta(type):',
        '    def __new__(mcs, name, bases, attrs):',
        '        for key in attrs:',
        '            if not key.startswith("_") and not key.islower():',
        '                raise TypeError(f"Method {key} must be lowercase!")',
        '        return super().__new__(mcs, name, bases, attrs)',
        '',
        'class MyAPI(metaclass=ValidationMeta):',
        '    def get_data(self): pass   # OK — lowercase',
        '    # def GetData(self): pass  # This WOULD raise TypeError!',
    ]))
    story.append(vspace(6))

    story.append(Paragraph('Singleton Pattern using Metaclass', S['subtopic']))
    story.append(code_block([
        '# Singleton — ensures only ONE instance of a class ever exists',
        'class SingletonMeta(type):',
        '    _instances = {}',
        '    def __call__(cls, *args, **kwargs):',
        '        if cls not in cls._instances:',
        '            cls._instances[cls] = super().__call__(*args, **kwargs)',
        '        return cls._instances[cls]  # Always return same instance',
        '',
        'class Database(metaclass=SingletonMeta):',
        '    def __init__(self): self.connection = "Connected"',
        '',
        'db1 = Database()',
        'db2 = Database()',
        'print(db1 is db2)        # True — SAME instance!',
        'print(id(db1) == id(db2))# True — same memory address',
    ]))
    story.append(vspace(6))

    # Q&A Metaclasses
    story.append(hr(TEAL))
    story.append(Paragraph('📝 EXAM QUESTIONS — METACLASSES', S['subtopic']))

    elems = qa_block(5, 'What are metaclasses in Python? Explain with an example.', [
        Paragraph('<b>METACLASS IN PYTHON:</b> In Python, everything is an object — even classes. The type of a class is called its metaclass. The default metaclass in Python is <b>type</b>.', S['answer']),
        Paragraph('<b>THE HIERARCHY:</b>', S['body_bold']),
        Paragraph('• Object is an instance of → Class', S['bullet']),
        Paragraph('• Class is an instance of → Metaclass (type, by default)', S['bullet']),
        Paragraph('• type is its OWN metaclass!', S['bullet']),
        code_block(['class Dog: pass', 'print(type(Dog))   # <class "type"> — metaclass is type', 'print(type(type))  # <class "type"> — type is its own metaclass']),
        Paragraph('<b>CREATING CLASSES WITH type():</b> type() can dynamically create a class at runtime. Syntax: type(name, bases, attributes_dict)', S['body_bold']),
        code_block(['Animal = type("Animal", (), {"legs": 4, "breathe": lambda self: print("Breathing")})', 'a = Animal()', 'a.breathe()    # Breathing', 'print(Animal.legs)  # 4']),
        Paragraph('<b>CUSTOM METACLASS:</b> Inherit from type and override __new__ or __init__ to control class creation.', S['body_bold']),
        code_block([
            'class ValidationMeta(type):',
            '    def __new__(mcs, name, bases, attrs):',
            '        for key in attrs:',
            '            if not key.startswith("_") and not key.islower():',
            '                raise TypeError(f"Method {key} must be lowercase!")',
            '        return super().__new__(mcs, name, bases, attrs)',
            '',
            'class MyAPI(metaclass=ValidationMeta):',
            '    def get_data(self): pass   # OK',
        ]),
        Paragraph('<b>USE CASES OF METACLASSES:</b>', S['body_bold']),
        Paragraph('• Enforcing coding standards (all methods lowercase/uppercase)', S['bullet']),
        Paragraph('• Singleton Pattern — only one instance of a class', S['bullet']),
        Paragraph('• Django ORM Models — automatically creates database schema', S['bullet']),
        Paragraph('• Abstract Base Classes (ABC) use metaclass=ABCMeta internally', S['bullet']),
        Paragraph('• Automatic registration of subclasses (plugin systems)', S['bullet']),
        Paragraph('Metaclasses are advanced Python, typically used in framework development. Understanding them shows deep Python mastery.', S['answer']),
    ])
    story.extend(elems)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # TOPIC 10: ABSTRACT & INNER CLASSES
    # ══════════════════════════════════════════════════════════════════════════
    story.append(topic_header_box(10, 'ABSTRACT & INNER CLASSES', 7))
    story.append(vspace(8))

    story.append(Paragraph('Abstract Classes', S['subtopic']))
    story.append(Paragraph(
        'An <b>abstract class</b> is a class that <b>CANNOT be instantiated</b> (you cannot create objects of it directly). '
        'It acts as a <b>blueprint/contract</b> for other classes. It can define <b>abstract methods</b> — '
        'methods that have NO implementation in the abstract class but <b>MUST be implemented</b> by any child class. '
        'In Python, abstract classes are created using the <b>abc module</b> (Abstract Base Classes).', S['body']))
    story.append(colored_box(
        '⚠️ CRITICAL RULE: If a child class does NOT implement ALL abstract methods, '
        'it also becomes abstract and cannot be instantiated! Attempting to instantiate '
        'an abstract class raises TypeError.',
        LIGHT_RED, RED))
    story.append(vspace(6))

    story.append(code_block([
        'from abc import ABC, abstractmethod',
        '',
        'class Shape(ABC):                  # Abstract class — inherits from ABC',
        '    @abstractmethod',
        '    def area(self):                # Abstract method — no implementation',
        '        pass',
        '',
        '    @abstractmethod',
        '    def perimeter(self):           # Another abstract method',
        '        pass',
        '',
        '    def describe(self):            # CONCRETE (non-abstract) method',
        '        print(f"I am a shape with area {self.area()}")',
        '',
        '# s = Shape()   # ERROR! Cannot instantiate abstract class',
        '# TypeError: Can\'t instantiate abstract class Shape',
        '',
        'class Circle(Shape):',
        '    def __init__(self, r): self.r = r',
        '    def area(self):        return 3.14 * self.r**2   # MUST implement!',
        '    def perimeter(self):   return 2 * 3.14 * self.r  # MUST implement!',
        '',
        'class Rectangle(Shape):',
        '    def __init__(self, l, w): self.l = l; self.w = w',
        '    def area(self):           return self.l * self.w',
        '    def perimeter(self):      return 2*(self.l + self.w)',
        '',
        'c = Circle(5)',
        'r = Rectangle(4, 6)',
        '',
        'c.describe()      # I am a shape with area 78.5 — inherited!',
        'print(r.area())   # 24',
        'print(c.perimeter())  # 31.4',
        '',
        '# Polymorphism with abstract classes',
        'shapes = [Circle(3), Rectangle(4,5), Circle(7)]',
        'for shape in shapes:',
        '    print(f"Area: {shape.area():.2f}")',
    ]))
    story.append(vspace(6))

    story.append(Paragraph('Inner Classes (Nested Classes)', S['subtopic']))
    story.append(Paragraph(
        'An <b>inner class</b> (nested class) is a class defined <b>INSIDE another class</b>. '
        'The outer class can use the inner class to logically group related functionality. '
        'Inner classes help organize complex data structures and <b>hide implementation details</b> (encapsulation).', S['body']))
    story.append(code_block([
        'class University:',
        '    def __init__(self, name):',
        '        self.name = name',
        '        self.dept = self.Department("Computer Science")  # Inner class instance',
        '',
        '    class Department:              # Inner class — defined inside University',
        '        def __init__(self, dname):',
        '            self.dname = dname',
        '',
        '        def info(self):',
        '            print(f"Department: {self.dname}")',
        '',
        '    def info(self):',
        '        print(f"University: {self.name}")',
        '        self.dept.info()           # Uses inner class',
        '',
        '',
        'u = University("ABC University")',
        'u.info()',
        '# University: ABC University',
        '# Department: Computer Science',
        '',
        '# Access inner class from OUTSIDE:',
        'd = University.Department("Physics")',
        'd.info()   # Department: Physics',
    ]))
    story.append(vspace(6))

    # Q&A Abstract
    story.append(hr(TEAL))
    story.append(Paragraph('📝 EXAM QUESTIONS — ABSTRACT & INNER CLASSES', S['subtopic']))

    elems = qa_block(1.5, 'What is an abstract class in Python? Can you instantiate it?', [
        Paragraph('An <b>abstract class</b> is a class that <b>cannot be instantiated</b> directly. It is defined using Python\'s <b>ABC (Abstract Base Class)</b> module. It contains <b>abstract methods</b> that must be overridden by all subclasses.', S['answer']),
        code_block(['from abc import ABC, abstractmethod', 'class Animal(ABC):', '    @abstractmethod', '    def sound(self): pass  # Must implement in child']),
        Paragraph('<b>No</b> — you cannot create an object of an abstract class. Attempting raises <b>TypeError</b>: "Can\'t instantiate abstract class". It serves as a template/contract for subclasses.', S['answer']),
    ])
    story.extend(elems)

    elems = qa_block(5, 'Explain abstract classes and inner classes in Python with examples.', [
        Paragraph('<b>ABSTRACT CLASSES:</b> An abstract class is a class with at least one abstract method. It serves as a template/contract — any subclass must implement all abstract methods. Uses the <b>abc module</b>.', S['answer']),
        code_block([
            'from abc import ABC, abstractmethod',
            '',
            'class Animal(ABC):',
            '    @abstractmethod',
            '    def sound(self): pass   # Must implement in all subclasses',
            '',
            '    @abstractmethod',
            '    def move(self): pass',
            '',
            '    def breathe(self):      # Concrete — inherited as-is',
            '        print(f"{self.__class__.__name__} breathes air")',
            '',
            '# a = Animal()   # TypeError!',
            '',
            'class Dog(Animal):',
            '    def sound(self): print("Woof")',
            '    def move(self):  print("Dog runs")',
            '',
            'class Fish(Animal):',
            '    def sound(self): print("...")',
            '    def move(self):  print("Fish swims")',
            '',
            'd = Dog(); d.sound(); d.breathe()  # Works!',
        ]),
        Paragraph('<b>KEY POINTS:</b>', S['body_bold']),
        Paragraph('• Abstract class cannot be instantiated directly', S['bullet']),
        Paragraph('• Abstract method has @abstractmethod decorator and no implementation body', S['bullet']),
        Paragraph('• Subclass MUST implement ALL abstract methods or it also becomes abstract', S['bullet']),
        Paragraph('• Can have both abstract and concrete (normal) methods', S['bullet']),
        Paragraph('<b>INNER CLASSES:</b> A class defined inside another class body. Used for logical grouping and encapsulation.', S['body_bold']),
        code_block([
            'class Car:',
            '    def __init__(self, brand):',
            '        self.brand  = brand',
            '        self.engine = self.Engine(1500, "Petrol")',
            '',
            '    class Engine:              # Inner class',
            '        def __init__(self, cc, fuel):',
            '            self.cc = cc; self.fuel = fuel',
            '        def specs(self):',
            '            print(f"Engine: {self.cc}cc, {self.fuel}")',
            '',
            '    def show(self):',
            '        print(f"Car: {self.brand}")',
            '        self.engine.specs()',
            '',
            'c = Car("Toyota")',
            'c.show()',
            '# Car: Toyota',
            '# Engine: 1500cc, Petrol',
        ]),
        Paragraph('<b>USES OF INNER CLASSES:</b> Logical grouping of related classes | Hiding implementation details (encapsulation) | Linked list nodes/tree nodes inside container class | GUI components (Frame inside Window).', S['answer']),
    ])
    story.extend(elems)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # TOPIC 11: EXCEPTION HANDLING
    # ══════════════════════════════════════════════════════════════════════════
    story.append(topic_header_box(11, 'EXCEPTION HANDLING', 9))
    story.append(colored_box('⚡ GUARANTEED IN PAPER — 9% Probability — All Mark Types Expected!', LIGHT_RED, RED, 'note'))
    story.append(vspace(8))

    story.append(Paragraph('What is an Exception?', S['subtopic']))
    story.append(Paragraph(
        'An <b>exception</b> is an error that occurs during program execution (runtime). '
        'When Python encounters an error it cannot handle, it <b>raises an exception</b> that, '
        'if not caught, terminates the program. '
        '<b>Exception Handling</b> is the mechanism to gracefully handle such runtime errors, '
        'log them, and allow the program to continue or fail safely instead of crashing.', S['body']))
    story.append(vspace(6))

    story.append(Paragraph('Common Built-in Exceptions', S['subtopic']))
    story.append(simple_table(
        ['Exception', 'Cause / When It Occurs'],
        [
            ['ZeroDivisionError', 'Dividing by zero: 10 / 0'],
            ['ValueError', 'Wrong value passed: int("abc")'],
            ['TypeError', 'Wrong type for operation: "hello" + 5'],
            ['NameError', 'Variable not defined/not in scope'],
            ['IndexError', 'List index out of range: lst[100]'],
            ['KeyError', 'Dictionary key not found: d["missing_key"]'],
            ['FileNotFoundError', 'Trying to open a file that doesn\'t exist'],
            ['AttributeError', 'Object doesn\'t have the attribute: obj.missing_attr'],
            ['ImportError', 'Module cannot be imported'],
            ['RecursionError', 'Maximum recursion depth exceeded'],
            ['StopIteration', 'Iterator has no more items (next() called)'],
            ['OverflowError', 'Numeric value too large for Python to represent'],
        ],
        [5*cm, 10*cm]
    ))
    story.append(vspace(6))

    story.append(Paragraph('try-except-else-finally — Complete Structure', S['subtopic']))
    story.append(code_block([
        'try:',
        '    # Code that MIGHT raise an exception — put risky code here',
        '    risky_code()',
        '',
        'except SomeException as e:',
        '    # Runs ONLY if SomeException occurs in try block',
        '    print(f"Error: {e}")',
        '',
        'except (TypeError, ValueError) as e:',
        '    # Catches MULTIPLE exception types in one clause',
        '    print(f"Type/Value Error: {e}")',
        '',
        'except Exception as e:',
        '    # Catches ANY exception — general catch-all (use as last resort)',
        '    print(f"Unexpected error: {e}")',
        '',
        'else:',
        '    # Runs ONLY if NO exception occurred in try block',
        '    print("Success! No error occurred.")',
        '',
        'finally:',
        '    # ALWAYS runs — whether exception occurred or not',
        '    # Used for cleanup: close files, DB connections, release resources',
        '    print("Cleanup code here")',
    ]))
    story.append(vspace(6))

    story.append(Paragraph('Comprehensive Practical Example', S['subtopic']))
    story.append(code_block([
        'def safe_division(a, b):',
        '    try:',
        '        result = a / b',
        '    except ZeroDivisionError:',
        '        print("Error: Cannot divide by zero!")',
        '        return None',
        '    except TypeError as e:',
        '        print(f"Type Error: {e}")',
        '        return None',
        '    else:',
        '        print(f"{a} / {b} = {result}")',
        '        return result',
        '    finally:',
        '        print("Division function executed.")   # Always runs',
        '',
        'safe_division(10, 2)   # 10 / 2 = 5.0 → Division function executed.',
        'safe_division(10, 0)   # Error: Cannot divide by zero! → Division function executed.',
        'safe_division(10,"a")  # Type Error → Division function executed.',
    ]))
    story.append(vspace(6))

    story.append(Paragraph('Raising Exceptions — raise', S['subtopic']))
    story.append(code_block([
        'def check_age(age):',
        '    if not isinstance(age, int):',
        '        raise TypeError("Age must be an integer!")',
        '    if age < 0 or age > 150:',
        '        raise ValueError(f"Invalid age: {age}. Must be 0-150.")',
        '    print(f"Valid age: {age}")',
        '',
        'check_age(25)    # Valid age: 25',
        'check_age(-5)    # ValueError: Invalid age: -5. Must be 0-150.',
        'check_age("abc") # TypeError: Age must be an integer!',
    ]))
    story.append(vspace(6))

    story.append(Paragraph('Custom (User-Defined) Exceptions', S['subtopic']))
    story.append(code_block([
        '# Custom exception inherits from Exception',
        'class InsufficientFundsError(Exception):',
        '    def __init__(self, balance, amount):',
        '        self.balance = balance',
        '        self.amount  = amount',
        '        message = f"Need Rs.{amount} but only have Rs.{balance}"',
        '        super().__init__(message)  # Call parent Exception __init__',
        '',
        'class BankAccount:',
        '    def __init__(self, balance): self.balance = balance',
        '',
        '    def withdraw(self, amount):',
        '        if amount > self.balance:',
        '            raise InsufficientFundsError(self.balance, amount)',
        '        self.balance -= amount',
        '        print(f"Withdrew Rs.{amount}. Balance: Rs.{self.balance}")',
        '',
        'acc = BankAccount(5000)',
        'try:',
        '    acc.withdraw(3000)   # OK — Withdrew Rs.3000. Balance: Rs.2000',
        '    acc.withdraw(5000)   # Raises InsufficientFundsError!',
        'except InsufficientFundsError as e:',
        '    print(f"Custom Error: {e}")',
        '    # Custom Error: Need Rs.5000 but only have Rs.2000',
    ]))
    story.append(vspace(6))

    # Q&A Exception
    story.append(hr(TEAL))
    story.append(Paragraph('📝 EXAM QUESTIONS — EXCEPTION HANDLING', S['subtopic']))

    elems = qa_block(1.5, 'What is the role of "finally" block in exception handling?', [
        Paragraph('The <b>"finally"</b> block <b>always executes</b> regardless of whether an exception occurred or was caught. It is used for <b>cleanup operations</b> like closing files, database connections, or releasing resources.', S['answer']),
        code_block(['try:', '    f = open("data.txt")', '    data = f.read()', 'except FileNotFoundError:', '    print("File not found!")', 'finally:', '    f.close()   # ALWAYS runs — even if exception occurred']),
        Paragraph('"finally" runs even if the program exits via return or sys.exit(). It guarantees cleanup code always executes.', S['answer']),
    ])
    story.extend(elems)

    elems = qa_block(10, 'Write a program in Python to demonstrate Exception Handling. Explain with custom exceptions, raise, and practical examples.', [
        Paragraph('<b>EXCEPTION HANDLING IN PYTHON — COMPLETE GUIDE:</b>', S['body_bold']),
        Paragraph('<b>WHAT IS AN EXCEPTION?</b> An exception is a runtime error that disrupts the normal flow of a program. Python provides a robust exception handling mechanism using try-except-else-finally blocks.', S['answer']),
        Paragraph('<b>EXCEPTION HIERARCHY:</b>', S['body_bold']),
        Paragraph('BaseException → Exception → ArithmeticError → ZeroDivisionError', S['bullet']),
        Paragraph('Exception → LookupError → IndexError, KeyError', S['bullet']),
        Paragraph('Exception → ValueError, TypeError, IOError → FileNotFoundError', S['bullet']),
        Paragraph('<b>BASIC try-except:</b>', S['body_bold']),
        code_block([
            'try:',
            '    num    = int(input("Enter number: "))',
            '    result = 100 / num',
            '    print(f"Result: {result}")',
            'except ZeroDivisionError:',
            '    print("Cannot divide by zero!")',
            'except ValueError:',
            '    print("Invalid input — must be a number!")',
        ]),
        Paragraph('<b>MULTIPLE EXCEPT CLAUSES + else + finally:</b>', S['body_bold']),
        code_block([
            'def process_data(data):',
            '    try:',
            '        result = [int(x) for x in data]',
            '        total  = sum(result)',
            '    except ValueError as e:',
            '        print(f"Conversion Error: {e}")',
            '        return None',
            '    else:',
            '        print(f"Processing successful! Total: {total}")',
            '        return total',
            '    finally:',
            '        print("process_data() function completed.")',
            '',
            'process_data(["1","2","3"])   # Success',
            'process_data(["1","abc","3"]) # ValueError caught',
        ]),
        Paragraph('<b>USING raise — Deliberately raise exceptions:</b>', S['body_bold']),
        code_block([
            'def validate_score(score):',
            '    if not isinstance(score, (int, float)):',
            '        raise TypeError(f"Score must be numeric")',
            '    if score < 0 or score > 100:',
            '        raise ValueError(f"Score {score} out of range [0-100]")',
            '    return True',
        ]),
        Paragraph('<b>CUSTOM EXCEPTIONS — For domain-specific errors:</b>', S['body_bold']),
        code_block([
            'class AgeError(Exception):',
            '    def __init__(self, age, message="Invalid age"):',
            '        self.age = age',
            '        super().__init__(f"{message}: {age}")',
            '',
            'class VoterRegistration:',
            '    def register(self, name, age):',
            '        try:',
            '            if age < 18:',
            '                raise AgeError(age, "Must be 18+ to register")',
            '            print(f"{name} registered successfully!")',
            '        except AgeError as e:',
            '            print(f"Registration Failed — {e}")',
            '',
            'v = VoterRegistration()',
            'v.register("Alice", 25)  # Registered successfully!',
            'v.register("Bob",   16)  # Registration Failed — Must be 18+: 16',
        ]),
        Paragraph('<b>CONTEXT MANAGER (with) FOR AUTOMATIC CLEANUP:</b>', S['body_bold']),
        code_block([
            'try:',
            '    with open("data.txt", "r") as f:  # File closes automatically!',
            '        data = f.read()',
            'except FileNotFoundError:',
            '    print("File not found!")',
        ]),
        Paragraph('<b>BEST PRACTICES:</b>', S['body_bold']),
        Paragraph('• Always catch SPECIFIC exceptions, not bare except:', S['bullet']),
        Paragraph('• Always clean up resources in finally block', S['bullet']),
        Paragraph('• Use custom exceptions for domain-specific errors', S['bullet']),
        Paragraph('• Never use exceptions for normal control flow', S['bullet']),
        Paragraph('• Always log exceptions with context for debugging', S['bullet']),
        Paragraph('Exception handling is critical in data analytics — reading corrupt data files, handling network failures, and processing malformed inputs all require robust exception handling.', S['answer']),
    ])
    story.extend(elems)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # TOPIC 12: PACKAGES
    # ══════════════════════════════════════════════════════════════════════════
    story.append(topic_header_box(12, 'MODULAR PROGRAMS & PACKAGES', 5))
    story.append(vspace(8))

    story.append(Paragraph('What are Modules?', S['subtopic']))
    story.append(Paragraph(
        'A <b>module</b> is a Python file (.py) containing functions, classes, and variables that '
        'can be reused in other programs. Instead of writing all code in one file, you split it '
        'into multiple modules — this is called <b>modular programming</b>. '
        'Python has hundreds of built-in modules (os, sys, math, random, datetime, csv, json, etc.) '
        'and millions of third-party modules available via pip.', S['body']))
    story.append(code_block([
        '# geometry.py — Our custom module',
        'PI = 3.14159',
        'def circle_area(r): return PI * r * r',
        'def rect_area(l, w): return l * w',
        'def factorial(n): return 1 if n<=1 else n*factorial(n-1)',
        '',
        '# main.py — Using our module',
        'import geometry                     # Full import',
        'print(geometry.circle_area(5))      # 78.539...',
        '',
        'from geometry import circle_area    # Import specific function',
        'print(circle_area(5))               # No need for prefix',
        '',
        'import geometry as geo             # Alias — shorter name',
        'print(geo.rect_area(4, 6))          # 24',
        '',
        'from geometry import *             # Import everything (NOT recommended)',
        '',
        '# Built-in modules',
        'import math;     print(math.sqrt(16))      # 4.0',
        'import os;       print(os.getcwd())         # Current directory',
        'import random;   print(random.randint(1,100))',
        'import datetime; print(datetime.date.today())',
        'import json;     data = json.dumps({"key":"value"})',
    ]))
    story.append(vspace(6))

    story.append(Paragraph('What are Packages?', S['subtopic']))
    story.append(Paragraph(
        'A <b>package</b> is a directory/folder containing multiple modules, organized together. '
        'It must contain a special file called <b>__init__.py</b> (can be empty or contain initialization code) '
        'to tell Python that the directory is a package. '
        'Packages enable organizing large codebases into logical namespaces.', S['body']))
    story.append(code_block([
        '# Package directory structure:',
        'analytics/              # Package (directory)',
        '    __init__.py         # Makes it a package — required!',
        '    data_loader.py      # Module 1',
        '    preprocessor.py     # Module 2',
        '    visualizer.py       # Module 3',
        '    models/             # Sub-package (nested package)',
        '        __init__.py',
        '        linear_model.py',
        '        neural_net.py',
        '',
        '# Using the package:',
        'from analytics import data_loader',
        'from analytics.models import linear_model',
        'import analytics.preprocessor as prep',
        '',
        '# __init__.py can expose selected functions:',
        '# In analytics/__init__.py:',
        'from .data_loader import load_csv     # Expose directly',
        'from .preprocessor import clean_data  # Short access path',
    ]))
    story.append(vspace(6))

    story.append(Paragraph('__name__ == "__main__" — The Entry Point Guard', S['subtopic']))
    story.append(Paragraph(
        'Every Python file has a built-in variable <b>__name__</b>. '
        'When a file is <b>RUN directly</b>, __name__ equals <b>"__main__"</b>. '
        'When it is <b>IMPORTED</b> as a module, __name__ equals the module\'s name. '
        'The guard <b>if __name__ == "__main__":</b> is used to write code that runs '
        'ONLY when the file is executed directly, NOT when imported.', S['body']))
    story.append(code_block([
        '# mymodule.py',
        'def greet(name): return f"Hello, {name}!"',
        'def add(a, b):   return a + b',
        '',
        'if __name__ == "__main__":',
        '    # This block runs ONLY when mymodule.py is run directly',
        '    # It is SKIPPED when mymodule is imported by another file',
        '    print(greet("World"))  # Hello, World!',
        '    print(add(3, 4))       # 7',
        '    print("Running tests...")',
        '',
        '# When another file does: import mymodule',
        '# → __name__ = "mymodule" → guard block is SKIPPED',
    ]))
    story.append(vspace(6))

    # Q&A Packages
    story.append(hr(TEAL))
    story.append(Paragraph('📝 EXAM QUESTIONS — PACKAGES', S['subtopic']))

    elems = qa_block(1.5, 'What is the difference between a module and a package in Python? Also explain what are Packages.', [
        Paragraph('<b>Module:</b> A single Python <b>.py file</b> containing functions, classes, and variables. Imported using "import module_name".', S['answer']),
        Paragraph('<b>Package:</b> A <b>directory of modules</b> with a special <b>__init__.py</b> file. Enables organizing multiple related modules together under one namespace.', S['answer']),
        Paragraph('<b>Example:</b> "math" is a module. "numpy" or "pandas" is a package containing many sub-modules and sub-packages inside.', S['answer']),
        code_block(['import math            # Module', 'import numpy as np     # Package', 'from os import path    # Importing from a module']),
    ])
    story.extend(elems)

    elems = qa_block(5, 'Explain modules and packages in Python with how to create and import them.', [
        Paragraph('<b>MODULES IN PYTHON:</b> A module is a .py file containing Python code (functions, classes, variables) that can be reused in other scripts. Promotes code reuse and modular programming.', S['answer']),
        Paragraph('<b>CREATING A MODULE (geometry.py):</b>', S['body_bold']),
        code_block([
            'PI = 3.14159',
            'def circle_area(r):   return PI * r * r',
            'def rect_area(l, w):  return l * w',
            'class Triangle:',
            '    def __init__(self, b, h): self.b=b; self.h=h',
            '    def area(self):  return 0.5 * self.b * self.h',
        ]),
        Paragraph('<b>IMPORTING A MODULE:</b>', S['body_bold']),
        code_block([
            'import geometry                  # Full import',
            'print(geometry.circle_area(5))',
            '',
            'from geometry import rect_area   # Specific import',
            'print(rect_area(4, 6))',
            '',
            'import geometry as geo           # Alias',
            'print(geo.PI)',
        ]),
        Paragraph('<b>PACKAGES:</b> A package is a directory with __init__.py containing multiple modules. Packages organize large codebases into logical namespaces.', S['body_bold']),
        Paragraph('<b>STRUCTURE:</b>', S['body_bold']),
        code_block([
            'mypackage/',
            '    __init__.py    # Required — makes it a package',
            '    module1.py',
            '    module2.py',
            '    subpackage/',
            '        __init__.py',
            '        module3.py',
        ]),
        Paragraph('<b>IMPORTING FROM PACKAGE:</b>', S['body_bold']),
        code_block([
            'import mypackage.module1',
            'from mypackage import module2',
            'from mypackage.subpackage import module3',
        ]),
        Paragraph('<b>__name__ GUARD:</b>', S['body_bold']),
        code_block(['if __name__ == "__main__":', '    # Only runs when file is directly executed', '    run_tests()']),
        Paragraph('<b>THIRD-PARTY PACKAGES:</b> Install via pip: pip install numpy pandas matplotlib. Then import: import numpy as np; import pandas as pd.', S['answer']),
    ])
    story.extend(elems)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # QUICK REVISION CHEAT SHEET
    # ══════════════════════════════════════════════════════════════════════════
    banner_data = [[Paragraph('⚡ QUICK REVISION CHEAT SHEET — MODULE 1', S['module_banner'])]]
    bt = Table(banner_data, colWidths=[W-4*cm])
    bt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), TEAL),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(bt)
    story.append(vspace(10))

    cheat = [
        ['TOPIC', 'KEY POINTS TO REMEMBER', 'EXAM %'],
        ['Lists', 'Ordered, Mutable, Allows Duplicates, [ ]. Methods: append, pop, sort, reverse, extend. List comprehension: [expr for x in iterable if cond]', '8%'],
        ['Dictionaries', 'Key-Value pairs, { }. Keys=unique+immutable. Methods: keys(), values(), items(), get(), update(), pop(). Dict comprehension.', '8%'],
        ['Functions', 'def keyword. 5 argument types: positional, keyword, default, *args, **kwargs. Lambda, decorators (@), recursion, LEGB scope.', '10%'],
        ['File Handling', 'open(), modes: r/w/a/x/rb/wb. ALWAYS use "with open()" statement. Methods: read(), readline(), readlines(), write(), writelines()', '7%'],
        ['Class Attrs', 'Class attr=shared by all objects (outside methods). Instance attr=unique per object via self in __init__. @classmethod @staticmethod', '9%'],
        ['Inheritance', 'Types: Single, Multiple, Multilevel, Hierarchical, Hybrid. super() to call parent. Method overriding = same name different impl.', '12%'],
        ['MRO', 'C3 Linearization Algorithm. ClassName.mro(). Diamond Problem solved. Order: Child → Parents left-right → object', '8%'],
        ['Magic Methods', '__init__, __str__, __repr__, __add__, __eq__, __len__, __call__, __iter__. Operator Overloading. Never called directly!', '10%'],
        ['Metaclasses', 'Class of a class. Default: type. Custom: inherit from type. Control class creation. Singleton pattern. Django uses metaclasses.', '7%'],
        ['Abstract Classes', 'from abc import ABC, abstractmethod. @abstractmethod. Cannot instantiate abstract class. Child MUST implement all abstract methods.', '7%'],
        ['Exception Handling', 'try-except-else-finally. raise to manually throw. Custom exceptions inherit from Exception. ZeroDivisionError, ValueError, etc.', '9%'],
        ['Packages', 'Directory + __init__.py. import/from...import. __name__=="__main__" guard. pip install for third-party packages.', '5%'],
    ]
    cheat_data = []
    for i, row in enumerate(cheat):
        if i == 0:
            cheat_data.append([Paragraph(f'<b>{c}</b>', S['body_bold']) for c in row])
        else:
            cheat_data.append([
                Paragraph(f'<b>{row[0]}</b>', S['body_bold']),
                Paragraph(row[1], S['body']),
                Paragraph(f'<b>{row[2]}</b>', S['body_bold']),
            ])
    ct2 = Table(cheat_data, colWidths=[2.5*cm, 11.5*cm, 1*cm])
    ct2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT_BLUE]),
        ('BOX', (0,0), (-1,-1), 1, ACCENT_BLUE),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#b0bec5')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(ct2)
    story.append(vspace(16))

    story.append(colored_box(
        '🏆 TOP 5 MOST IMPORTANT TOPICS:\n'
        '1st: Inheritance (12%) | 2nd: Magic Methods (10%) = Functions (10%) | '
        '4th: Exception Handling (9%) = Class Attributes (9%)\n'
        'Focus MAXIMUM study time on these five topics!',
        YELLOW_BG, ORANGE, 'note'))
    story.append(vspace(10))

    story.append(hr(DARK_BLUE, 2))
    story.append(Paragraph('MODULE 1 — DATA ANALYTICS USING PYTHON (PCC-IT-601-A-2024) | Complete Exam Notes | B.Tech 6th Semester', S['tip']))

    doc.build(story)
    print("PDF generated successfully!")

build_pdf()