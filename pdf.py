from reportlab.lib.pagesizes import A4
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable, PageBreak)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

DARK_BLUE  = colors.HexColor('#1a237e')
MID_BLUE   = colors.HexColor('#283593')
ACC_BLUE   = colors.HexColor('#3949ab')
LT_BLUE    = colors.HexColor('#e8eaf6')
GREEN_BG   = colors.HexColor('#e8f5e9')
GREEN_ACC  = colors.HexColor('#2e7d32')
ORA_ACC    = colors.HexColor('#e65100')
ORA_BG     = colors.HexColor('#fff3e0')
RED_ACC    = colors.HexColor('#b71c1c')
RED_BG     = colors.HexColor('#ffebee')
PURPLE     = colors.HexColor('#4a148c')
PURPLE_BG  = colors.HexColor('#f3e5f5')
TEAL       = colors.HexColor('#006064')
TEAL_BG    = colors.HexColor('#e0f7fa')
BROWN      = colors.HexColor('#4e342e')
BROWN_BG   = colors.HexColor('#efebe9')
PINK       = colors.HexColor('#880e4f')
PINK_BG    = colors.HexColor('#fce4ec')
GREY_LINE  = colors.HexColor('#90a4ae')
WHITE      = colors.white

W, H = A4
doc = SimpleDocTemplate("HRM_Module4_Notes.pdf",
    pagesize=A4, rightMargin=1.8*cm, leftMargin=1.8*cm,
    topMargin=1.5*cm, bottomMargin=1.5*cm)

def S(name, **kw): return ParagraphStyle(name, **kw)
body  = S('B',  fontSize=9.5, fontName='Helvetica', leading=14, spaceAfter=4, alignment=TA_JUSTIFY)
blt   = S('BU', fontSize=9.5, fontName='Helvetica', leading=13, spaceAfter=2, leftIndent=14, firstLineIndent=-10)
sub_t = S('ST', fontSize=11, textColor=ACC_BLUE, fontName='Helvetica-Bold', leading=14, spaceBefore=6, spaceAfter=3)
sec_t = S('SE', fontSize=13, textColor=MID_BLUE,  fontName='Helvetica-Bold', leading=16, spaceBefore=8, spaceAfter=4)
imp   = S('IM', fontSize=9.5, fontName='Helvetica-BoldOblique', textColor=MID_BLUE, spaceAfter=5, leftIndent=8)
warn  = S('WN', fontSize=9.5, fontName='Helvetica-Bold', textColor=RED_ACC, spaceAfter=5, leftIndent=8)

def hl(c=GREY_LINE, t=0.8): return HRFlowable(width="100%", thickness=t, color=c, spaceAfter=4, spaceBefore=4)

def thdr(text, pct):
    bg = GREEN_BG if pct>=75 else ORA_BG if pct>=50 else RED_BG
    tc = GREEN_ACC if pct>=75 else ORA_ACC if pct>=50 else RED_ACC
    st = "★★★" if pct>=75 else "★★☆" if pct>=50 else "★☆☆"
    t = Table([[text, f"{pct}% {st}"]], colWidths=[W-7.5*cm, 2.5*cm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),LT_BLUE),('BACKGROUND',(1,0),(1,0),bg),
        ('TEXTCOLOR',(0,0),(0,0),DARK_BLUE),('TEXTCOLOR',(1,0),(1,0),tc),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),11),
        ('ALIGN',(0,0),(0,0),'LEFT'),('ALIGN',(1,0),(1,0),'CENTER'),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(0,0),8),('BOX',(0,0),(-1,-1),1,ACC_BLUE)]))
    return t

def qb(marks, q, a):
    if marks==1.5:  bc,hc,badge=colors.HexColor('#e3f2fd'),colors.HexColor('#1565c0'),"1.5 Marks"
    elif marks==5:  bc,hc,badge=PURPLE_BG,PURPLE,"5 Marks"
    elif marks==10: bc,hc,badge=GREEN_BG,GREEN_ACC,"10 Marks"
    else:           bc,hc,badge=ORA_BG,ORA_ACC,"15 Marks"
    t1=Table([[f"Q: {q}",badge]],colWidths=[W-6.3*cm,1.8*cm])
    t1.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),hc),('TEXTCOLOR',(0,0),(-1,-1),WHITE),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),8.5),
        ('ALIGN',(1,0),(1,0),'CENTER'),('ALIGN',(0,0),(0,0),'LEFT'),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(0,0),6)]))
    t2=Table([[a]],colWidths=[W-4.5*cm])
    t2.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),bc),('FONTNAME',(0,0),(-1,-1),'Helvetica'),
        ('FONTSIZE',(0,0),(-1,-1),8.5),('LEADING',(0,0),(-1,-1),12),('ALIGN',(0,0),(-1,-1),'LEFT'),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),6),('BOX',(0,0),(-1,-1),0.5,hc)]))
    return [t1,t2,Spacer(1,5)]

def mkt(data, cw, hc=MID_BLUE, rc=[WHITE,LT_BLUE]):
    t=Table(data,colWidths=cw)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),hc),('TEXTCOLOR',(0,0),(-1,0),WHITE),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,1),(-1,-1),'Helvetica'),
        ('FONTSIZE',(0,0),(-1,-1),8.5),('ROWBACKGROUNDS',(0,1),(-1,-1),rc),
        ('ALIGN',(0,0),(-1,-1),'LEFT'),('TOPPADDING',(0,0),(-1,-1),4),
        ('BOTTOMPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(-1,-1),5),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('BOX',(0,0),(-1,-1),1,hc),
        ('INNERGRID',(0,0),(-1,-1),0.3,GREY_LINE)]))
    return t

def qhdr(t): return Paragraph(f"<b>📝 EXAM QUESTIONS — {t}</b>",
    S('qh',fontSize=10.5,fontName='Helvetica-Bold',textColor=DARK_BLUE,spaceBefore=5,spaceAfter=4))

story=[]

# ─── COVER ───────────────────────────────────────────
story.append(Spacer(1,0.8*cm))
cov=Table([[Paragraph("HUMAN RESOURCE MANAGEMENT",S('ct',fontSize=26,textColor=WHITE,alignment=TA_CENTER,fontName='Helvetica-Bold',leading=32))],
    [Paragraph("OEC-CS-602 (I) | B.Tech 7th Semester",S('cs',fontSize=13,textColor=colors.HexColor('#c5cae9'),alignment=TA_CENTER,fontName='Helvetica'))],
    [Spacer(1,0.3*cm)],
    [Paragraph("MODULE 4",S('cm',fontSize=20,textColor=colors.HexColor('#fff9c4'),alignment=TA_CENTER,fontName='Helvetica-Bold'))],
    [Paragraph("Industrial Relations | Grievance | Employee Welfare | Dispute Resolution | IHRM | Contemporary Issues",
        S('cs2',fontSize=10.5,textColor=colors.HexColor('#c5cae9'),alignment=TA_CENTER,fontName='Helvetica-Bold',leading=15))],
    [Spacer(1,0.4*cm)]],colWidths=[W-3.6*cm])
cov.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),DARK_BLUE),('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
story.append(cov)
inf=Table([["📘 PYQ Analysis: Dec-2024 | May-2025 | Dec-2025  |  All Q&A at Correct Word Limits Included"]],colWidths=[W-3.6*cm])
inf.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#303f9f')),
    ('TEXTCOLOR',(0,0),(-1,-1),colors.HexColor('#e8eaf6')),('FONTNAME',(0,0),(-1,-1),'Helvetica'),
    ('FONTSIZE',(0,0),(-1,-1),9.5),('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
story.append(inf)
story.append(Spacer(1,0.4*cm))

toc=[["#","TOPIC","EXAM %"],
    ["1","Industrial Relations — Concept, Scope & Importance","80%"],
    ["2","Grievance Handling — Meaning, Causes & Procedure","85%"],
    ["3","Employee Welfare — Statutory & Non-Statutory","80%"],
    ["4","Dispute Resolution — Causes, Methods & Machinery","85%"],
    ["5","International HRM (IHRM) — Challenges & Expatriate Management","80%"],
    ["6","Knowledge Management in HRM","80%"],
    ["7","HR Audit & HR Accounting","75%"],
    ["8","HR in Virtual Organisations","75%"],
    ["9","Ethics & Corporate Social Responsibility (CSR)","80%"],
]
toct=Table(toc,colWidths=[0.6*cm,W-6*cm,1.5*cm])
toct.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),ACC_BLUE),('TEXTCOLOR',(0,0),(-1,0),WHITE),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,1),(-1,-1),'Helvetica'),
    ('FONTSIZE',(0,0),(-1,-1),9),('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,LT_BLUE]),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),('ALIGN',(1,0),(1,-1),'LEFT'),('LEFTPADDING',(1,0),(1,-1),6),
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ('BOX',(0,0),(-1,-1),1,ACC_BLUE),('INNERGRID',(0,0),(-1,-1),0.3,GREY_LINE),
    ('TEXTCOLOR',(2,1),(2,-1),GREEN_ACC),('FONTNAME',(2,1),(2,-1),'Helvetica-Bold')]))
story.append(Paragraph("MODULE 4 — CONTENTS & EXAM PROBABILITY",S('tc',fontSize=11,fontName='Helvetica-Bold',textColor=DARK_BLUE,alignment=TA_CENTER,spaceAfter=6)))
story.append(toct)
story.append(PageBreak())

# ══════════════════════════════════════════════════════
# TOPIC 1 — INDUSTRIAL RELATIONS
# ══════════════════════════════════════════════════════
story.append(thdr("TOPIC 1: Industrial Relations — Concept, Scope & Importance",80))
story.append(Spacer(1,4))

story.append(Paragraph("1.1  What is Industrial Relations (IR)?",sec_t))
story.append(hl())
story.append(Paragraph("<b>Industrial Relations (IR)</b> refers to the <b>complex system of relationships between employers (management), employees (workers/unions), and the government</b> in the context of work and employment. It governs the rules and procedures for determining wages, working conditions, and resolving conflicts in industry.",body))
story.append(Paragraph("V.B. Singh: Industrial Relations are a complex web of relationships, attitudes and approaches developed between management and workers.",blt))
story.append(Paragraph("Dunlop's IR System (1958): IR is a system with three actors — Employers, Workers/Unions, and Government — operating within a shared ideology and generating a body of rules governing the workplace.",blt))

story.append(Paragraph("Objectives of Industrial Relations:",sub_t))
ir_obj=["To maintain industrial peace and harmony in the organisation.",
"To protect the legitimate interests of both employers and employees.",
"To promote collective bargaining as a means of settling disputes.",
"To avoid industrial conflict — strikes, lockouts, go-slows.",
"To raise productivity and improve quality of work life.",
"To ensure compliance with labour laws and government regulations.",
"To develop democratic management through workers' participation.",
]
for o in ir_obj: story.append(Paragraph(f"&#8226; {o}",blt))

story.append(Paragraph("1.2  Scope of Industrial Relations",sec_t))
story.append(hl())
ir_scope=[("Labour-Management Relations","The relationship between employers/managers and workers — covering wages, working conditions, discipline, promotions and welfare."),
    ("Labour Legislation","All laws governing employment: Factories Act, Industrial Disputes Act, Payment of Wages Act, Minimum Wages Act, Trade Unions Act, Workmen's Compensation Act, ESI Act, PF Act, etc."),
    ("Trade Unions","Organisation and functioning of worker unions — recognition, collective bargaining, strikes and union-management negotiations."),
    ("Collective Bargaining","The process through which employers and unions negotiate wages, working hours, and conditions of employment."),
    ("Grievance Handling","Formal procedures for addressing and resolving employee complaints about working conditions, pay, treatment, promotions, etc."),
    ("Dispute Resolution","Mechanisms for resolving industrial disputes — conciliation, arbitration, adjudication."),
    ("Workers' Participation in Management","Employee involvement in decision-making through works committees, joint management councils, etc."),
]
for t,d in ir_scope: story.append(Paragraph(f"<b>{t}:</b> {d}",blt))

story.append(Paragraph("1.3  Parties in Industrial Relations",sub_t))
parties=[["Party","Role in IR","Examples"],
    ["Employer/Management","Sets wages, working conditions, policies; aims for productivity and profit","TATA, Infosys HR departments, Factory owners"],
    ["Employees/Trade Unions","Represent workers' collective interests; negotiate wages; protect rights","AITUC, INTUC, CITU, BMS — Indian trade unions"],
    ["Government","Enacts and enforces labour laws; provides dispute resolution machinery; acts as mediator","Ministry of Labour, Labour Courts, Industrial Tribunals"],
]
story.append(mkt(parties,[3*cm,5.5*cm,W-12.5*cm],TEAL,[WHITE,TEAL_BG]))
story.append(Spacer(1,5))

story.append(Paragraph("1.4  Approaches to Industrial Relations",sub_t))
approaches=[("Unitary Approach","Organisation is one united team working towards common goals. Conflict is seen as abnormal and caused by troublemakers. Management has the right to manage. Trade unions are unnecessary. Common in small owner-managed firms."),
    ("Pluralist Approach","Organisation contains many groups with different interests. Conflict is natural and inevitable. Trade unions are legitimate representatives. IR is about managing conflict through negotiation and compromise. Most widely accepted approach."),
    ("Marxist/Radical Approach","Sees IR as a reflection of class conflict between capital (employers) and labour (workers). Conflict is inherent in capitalism. Trade unions are instruments of working-class struggle. Advocates fundamental restructuring of society."),
    ("Systems Approach (Dunlop)","IR is a subsystem of society. Three actors (employers, workers, govt) produce a body of rules. Environmental factors (technology, market, power) shape IR."),
]
for a,d in approaches: story.append(Paragraph(f"<b>{a}:</b> {d}",blt))

story.append(hl(ACC_BLUE,1.2))
story.append(qhdr("Topic 1: Industrial Relations"))
story.append(hl(ACC_BLUE,1.2))
for item in qb(1.5,"What is Grievance? (1.5 marks)",
    "A grievance is any real or imagined feeling of personal injustice that an employee has regarding their work situation — relating to wages, working conditions, treatment by supervisors, promotions, transfers or disciplinary actions. It is a formal complaint raised through an established procedure. Grievances can be expressed (formally stated) or unexpressed (felt internally but not raised). The ILO defines a grievance as 'a complaint of one or more workers with respect to wages and allowances, conditions of work, interpretation of service agreements, and disciplinary actions.'"):
    story.append(item)
story.append(PageBreak())

# ══════════════════════════════════════════════════════
# TOPIC 2 — GRIEVANCE HANDLING
# ══════════════════════════════════════════════════════
story.append(thdr("TOPIC 2: Grievance Handling — Meaning, Causes & Procedure",85))
story.append(Spacer(1,4))

story.append(Paragraph("2.1  What is a Grievance?",sec_t))
story.append(hl())
story.append(Paragraph("<b>A grievance</b> is any <b>real or imagined feeling of personal injustice or dissatisfaction</b> that an employee has regarding their employment situation — covering wages, working conditions, supervision, promotions, transfers, disciplinary actions or interpersonal conflicts.",body))
story.append(Paragraph("Keith Davis: A grievance is any real or imagined feeling of personal injustice which an employee has concerning his employment relationship.",blt))
story.append(Paragraph("Important: Grievances must be distinguished from complaints (general dissatisfaction) and disputes (collective industrial conflict).",imp))

story.append(Paragraph("2.2  Causes / Sources of Grievances",sec_t))
story.append(hl())
causes=[["Category","Specific Causes"],
    ["Wages & Salary","Non-payment of wages, wrong calculation, unfair increments, denial of overtime, wrong grade placement"],
    ["Working Conditions","Unsafe workplace, faulty tools, poor ventilation, excessive noise, inadequate breaks, long shifts"],
    ["Supervision","Favouritism, bias, harassment, inconsistent treatment, excessive control, humiliation by supervisors"],
    ["Promotion & Career","Denial of promotion, unfair seniority rules, lack of career growth opportunities, transfers perceived as punitive"],
    ["Leave & Benefits","Denial of earned leave, unfair leave encashment, non-provision of statutory benefits (ESI, PF, gratuity)"],
    ["Discipline","Perceived unfair disciplinary action, inconsistent application of rules, wrongful suspension or termination"],
    ["Interpersonal Conflicts","Bullying, sexual harassment, discrimination based on gender/caste/religion, workplace politics"],
    ["Management Policies","Arbitrary rule changes, lack of communication, perceived violation of service agreement or settlement"],
]
story.append(mkt(causes,[3*cm,W-7*cm],PURPLE,[WHITE,PURPLE_BG]))
story.append(Spacer(1,5))

story.append(Paragraph("2.3  Effects of Unresolved Grievances",sub_t))
effects=["Reduced employee morale, motivation and productivity.",
"Increased absenteeism and employee turnover.",
"Poor quality of work and customer service.",
"Collective industrial disputes — strikes, go-slows, work-to-rule.",
"Damage to management-employee trust and organisational culture.",
"Legal action and labour court proceedings."]
for e in effects: story.append(Paragraph(f"✗ {e}",blt))

story.append(Paragraph("2.4  Grievance Handling Procedure — Step-by-Step",sec_t))
story.append(hl())
story.append(Paragraph("A well-designed grievance handling procedure must be: <b>Simple, Time-bound, Impartial, Clearly communicated to all employees, and Follow a step-by-step escalation process.</b>",imp))

grievance_steps=[["Step","Level","Who Handles","Time Limit"],
    ["Step 1","Informal / Verbal","Immediate Supervisor / Line Manager","24–48 hours — resolve informally first"],
    ["Step 2","Written Grievance","HR Manager / Department Head","3–5 working days — formal written complaint"],
    ["Step 3","Senior Management","Senior HR / GM / Director","7–10 working days — if unresolved at Step 2"],
    ["Step 4","Grievance Committee","Joint Committee (Management + Union/Employee Reps)","15 working days — formal committee review"],
    ["Step 5","Arbitration","Neutral third-party Arbitrator (mutually agreed)","30 days — binding decision"],
    ["Step 6","Labour Court","Government Labour Court / Industrial Tribunal","Varies — legal adjudication under ID Act 1947"],
]
story.append(mkt(grievance_steps,[0.8*cm,2*cm,3.5*cm,W-10.3*cm],DARK_BLUE,[WHITE,LT_BLUE]))
story.append(Spacer(1,5))

story.append(Paragraph("2.5  Principles of a Good Grievance Procedure",sub_t))
principles=["Speed — grievances must be resolved quickly before they fester and escalate.",
"Fairness — each grievance must be heard impartially without bias or favour.",
"Simplicity — the procedure must be easy to understand and follow.",
"Confidentiality — employee's grievance must be kept confidential to protect dignity.",
"Definiteness — each step must have a clear time limit for resolution.",
"Finality — the final step's decision must be binding on both parties.",
"Access — every employee must know the procedure and be able to use it without fear of retaliation."]
for p in principles: story.append(Paragraph(f"✦ {p}",blt))

story.append(hl(ACC_BLUE,1.2))
story.append(qhdr("Topic 2: Grievance Handling"))
story.append(hl(ACC_BLUE,1.2))
for item in qb(15,"Explain grievance handling procedure and the mechanism of dispute resolution in industry. (15 marks)",
    "GRIEVANCE HANDLING:\nA grievance is any real or imagined feeling of personal injustice that an employee has regarding their employment situation — covering wages, working conditions, supervision, promotions or discipline (Keith Davis).\n\nCauses of Grievances: Wage-related (underpayment, wrong grade), Working conditions (unsafe environment, faulty tools), Supervisory issues (favouritism, harassment), Promotion denial, Leave disputes, Disciplinary actions, and Interpersonal conflicts.\n\nGrievance Handling Procedure (5-Step Escalation):\n\nStep 1 — Informal Resolution (24-48 hours): The employee first verbally raises the issue with the immediate supervisor. Most grievances can and should be resolved at this stage. Quick, simple and non-confrontational.\n\nStep 2 — Written Grievance to HR (3-5 days): If unresolved, the employee submits a written grievance to the HR manager or department head. HR investigates and provides a written response.\n\nStep 3 — Senior Management Review (7-10 days): If still unresolved, the grievance is escalated to a senior HR executive or General Manager who conducts a thorough review and meets the employee.\n\nStep 4 — Grievance Committee (15 days): A joint committee comprising management representatives and union/employee representatives reviews the case. The committee's decision is binding within the organisation.\n\nStep 5 — Arbitration/External Resolution (30 days): A mutually agreed neutral third-party arbitrator examines the facts and gives a binding decision without going to court.\n\nStep 6 — Labour Court/Tribunal: Under the Industrial Disputes Act 1947, the matter is referred to a Labour Court or Industrial Tribunal for legal adjudication.\n\nPrinciples of Good Grievance Procedure: Speed, Fairness, Simplicity, Confidentiality, Definiteness (time limits), Finality (binding decision), Access (every employee can use it without fear).\n\nDISPUTE RESOLUTION MECHANISMS (covered in detail in Topic 4):\nWhen grievances escalate or when collective issues arise, formal dispute resolution machinery is used — Conciliation (a neutral conciliator helps parties reach agreement), Voluntary Arbitration (neutral arbitrator's binding decision), Adjudication (Labour Court/Industrial Tribunal under the Industrial Disputes Act 1947).\n\nConclusion: An effective grievance handling system is the first line of defence against industrial disputes. It resolves individual complaints before they become collective conflicts, protecting both employee rights and organisational productivity."):
    story.append(item)
story.append(PageBreak())

# ══════════════════════════════════════════════════════
# TOPIC 3 — EMPLOYEE WELFARE
# ══════════════════════════════════════════════════════
story.append(thdr("TOPIC 3: Employee Welfare — Statutory & Non-Statutory Measures",80))
story.append(Spacer(1,4))

story.append(Paragraph("3.1  What is Employee Welfare?",sec_t))
story.append(hl())
story.append(Paragraph("<b>Employee Welfare</b> refers to all those <b>services, facilities and amenities provided to workers</b> to improve their working and living conditions, their health, safety, economic security and social well-being. It goes beyond the regular wages and benefits — it aims to make the work experience humane and dignified.",body))
story.append(Paragraph("Labour Investigation Committee: Employee welfare refers to such services, facilities and amenities as may be established in or in the vicinity of undertakings to enable persons employed to perform their work in healthy and congenial surroundings and to provide them with amenities conducive to good health and high morale.",blt))

story.append(Paragraph("Significance / Importance of Employee Welfare:",sub_t))
sig=["Improves employee morale, motivation and loyalty.",
"Reduces absenteeism, turnover and labour unrest.",
"Attracts better talent — welfare is part of the employee value proposition.",
"Improves productivity and quality of work.",
"Ensures compliance with labour laws and social obligations.",
"Builds positive employer brand and corporate image.",
"Reduces the incidence of industrial disputes and grievances.",
"Promotes overall physical, mental and social well-being of the workforce."]
for s in sig: story.append(Paragraph(f"&#8226; {s}",blt))
story.append(Spacer(1,5))

story.append(Paragraph("3.2  Types of Employee Welfare Measures",sec_t))
story.append(hl())

story.append(Paragraph("A. Statutory Welfare Measures (Required by Law)",sub_t))
story.append(Paragraph("These are <b>mandated by government legislation</b> and are non-negotiable. Failure to provide these is a legal offence.",body))
stat=[["Act / Law","Welfare Provisions"],
    ["Factories Act, 1948","Canteen (100+ workers), restrooms, crèche (30+ women), first aid (150+ workers), adequate lighting, ventilation, clean drinking water, spittoons"],
    ["Employees' State Insurance (ESI) Act, 1948","Medical care, maternity benefits, disability benefit, dependent's benefit, sickness cash benefit for workers earning up to Rs 21,000/month"],
    ["Employees' Provident Fund (EPF) Act, 1952","Compulsory provident fund, pension scheme, deposit-linked insurance — employer contributes 12% of basic salary"],
    ["Maternity Benefit Act, 1961 (amended 2017)","26 weeks paid maternity leave (first 2 children), 12 weeks for subsequent births, nursing breaks, crèche facility (50+ employees)"],
    ["Payment of Gratuity Act, 1972","Lump-sum payment for 5+ years of service = (15 days × last drawn salary × years of service) / 26"],
    ["Workmen's Compensation Act, 1923","Compensation to workers or their families for injury, disability or death arising from workplace accidents"],
    ["Minimum Wages Act, 1948","Ensures no worker is paid below the notified minimum wage; prevents exploitation"],
    ["Payment of Bonus Act, 1965","Mandatory annual bonus: minimum 8.33%, maximum 20% of annual wages for employees earning up to Rs 21,000/month"],
]
story.append(mkt(stat,[4*cm,W-8*cm],RED_ACC,[WHITE,RED_BG]))
story.append(Spacer(1,5))

story.append(Paragraph("B. Non-Statutory Welfare Measures (Voluntary by Employer)",sub_t))
story.append(Paragraph("These are <b>provided voluntarily by employers</b> beyond legal requirements — to attract, retain and motivate employees.",body))
nonstat_data=[["Category","Examples"],
    ["Housing & Transport","Company housing/quarters, housing loans at subsidised rates, company buses/transport allowances, car parks"],
    ["Health & Medical","Extended health insurance (family coverage), preventive health checkups, on-site clinics, gym/fitness centres, stress counselling/EAP"],
    ["Food & Refreshments","Subsidised canteens, free tea/coffee, sponsored meals, special food allowances"],
    ["Education & Skill Building","Tuition reimbursement, company libraries, online learning subscriptions (Coursera, LinkedIn Learning), children's education scholarships"],
    ["Recreation & Culture","Sports facilities, cultural programmes, annual picnics, club memberships, team outings, festivals and celebrations"],
    ["Financial Assistance","Soft loans (personal/housing), salary advances, financial counselling, retirement planning support, ESOPs"],
    ["Work-Life Balance","Flexible working hours, work-from-home, crèche/childcare, parental leave (beyond statutory), elder-care support"],
    ["Miscellaneous","Uniform/clothing allowance, tool allowance, long-service awards, recognition programmes, employee assistance programmes (EAP)"],
]
story.append(mkt(nonstat_data,[3*cm,W-7*cm],GREEN_ACC,[WHITE,GREEN_BG]))
story.append(Spacer(1,5))

story.append(hl(ACC_BLUE,1.2))
story.append(qhdr("Topic 3: Employee Welfare"))
story.append(hl(ACC_BLUE,1.2))
for item in qb(1.5,"Explain the concept of Employee Welfare. (1.5 marks)",
    "Employee Welfare refers to all services, facilities and amenities provided to workers — beyond wages — to improve their working and living conditions, health, safety and overall well-being. It is divided into: (1) Statutory Welfare — legally mandated measures under acts like the Factories Act 1948 (canteen, crèche, first aid), ESI Act, PF Act, Maternity Benefit Act; (2) Non-Statutory Welfare — voluntary measures like subsidised housing, recreation facilities, health insurance, education scholarships and flexible work arrangements. Welfare improves morale, reduces absenteeism, boosts productivity and reduces labour unrest."):
    story.append(item)
for item in qb(15,"Explain the different employee welfare measures, such as statutory and non-statutory welfare. Discuss its significance in improving employee satisfaction and productivity. (15 marks)",
    "Employee welfare refers to services, facilities and amenities provided to workers to improve their working and living conditions, health, safety and well-being beyond regular wages.\n\nSTATUTORY WELFARE MEASURES (Required by Law):\nThese are mandatory, enforceable welfare provisions under Indian labour legislation:\n\n1. Factories Act 1948: Mandates canteen (100+ workers), restrooms, crèche (30+ women workers), first-aid box (150+ workers), adequate lighting, ventilation, drinking water and sanitation.\n\n2. ESI Act 1948: Medical care, maternity benefits, disability benefit and sickness cash benefit for workers earning up to Rs 21,000/month. Employer contributes 3.25%, employee contributes 0.75% of wages.\n\n3. EPF Act 1952: Compulsory Provident Fund (employer and employee each contribute 12% of basic salary), Employees' Pension Scheme and Deposit-Linked Insurance.\n\n4. Maternity Benefit Act 1961 (amended 2017): 26 weeks paid maternity leave for first two children, nursing breaks and mandatory crèche for establishments with 50+ employees.\n\n5. Payment of Gratuity Act 1972: Lump-sum payment for 5+ years of service. Formula: (15 days × last salary × years of service) / 26.\n\n6. Payment of Bonus Act 1965: Annual bonus — minimum 8.33%, maximum 20% of wages for eligible employees.\n\n7. Workmen's Compensation Act 1923: Compensation for workplace accidents, injuries, disability or death.\n\nNON-STATUTORY WELFARE MEASURES (Voluntary):\nProvided beyond legal requirements by progressive employers:\n1. Housing: Company quarters, subsidised housing loans.\n2. Health: Extended health insurance (family cover), fitness centres, Employee Assistance Programmes (EAP), preventive health check-ups.\n3. Education: Tuition reimbursement, children's scholarships, company libraries.\n4. Recreation: Sports facilities, cultural events, annual outings, club memberships.\n5. Financial: Soft loans, salary advances, ESOPs, financial planning support.\n6. Work-Life Balance: Flexible hours, WFH, extended parental leave, childcare support.\n\nSIGNIFICANCE IN IMPROVING SATISFACTION AND PRODUCTIVITY:\n1. Higher Morale: Employees who feel cared for are more satisfied, engaged and committed.\n2. Reduced Absenteeism: Good health facilities and work-life balance reduce sick days and unplanned leave.\n3. Lower Turnover: Comprehensive welfare makes employees reluctant to leave for competitors.\n4. Better Productivity: Healthy, satisfied employees produce more, with fewer errors and better quality.\n5. Reduced Industrial Conflict: Welfare measures address the root causes of grievances before they escalate into disputes.\n6. Talent Attraction: Strong welfare programmes enhance employer brand, attracting top talent.\n7. Legal Compliance: Statutory welfare ensures the organisation avoids penalties and litigation.\n\nConclusion: Employee welfare is not charity — it is a strategic investment. Companies like Infosys, TATA and Google are known for exceptional welfare programmes, which directly contribute to their consistently high employee satisfaction scores and productivity levels."):
    story.append(item)
story.append(PageBreak())

# ══════════════════════════════════════════════════════
# TOPIC 4 — DISPUTE RESOLUTION
# ══════════════════════════════════════════════════════
story.append(thdr("TOPIC 4: Dispute Resolution — Causes, Methods & Machinery",85))
story.append(Spacer(1,4))

story.append(Paragraph("4.1  What is an Industrial Dispute?",sec_t))
story.append(hl())
story.append(Paragraph("<b>Industrial Dispute</b> is defined under the <b>Industrial Disputes Act, 1947</b> as: 'Any dispute or difference between employers and employers, or between employers and workmen, or between workmen and workmen, which is connected with the employment or non-employment or the terms of employment or the conditions of labour of any person.'",body))

story.append(Paragraph("Common Causes of Industrial Disputes:",sub_t))
causes_data=[["Category","Specific Causes"],
    ["Wages & Allowances","Demand for higher wages, dearness allowance, non-payment of wages, bonus disputes"],
    ["Working Conditions","Unsafe workplace, excessive working hours, inadequate rest breaks, poor facilities"],
    ["Personnel Issues","Unfair dismissals, retrenchments, lay-offs, transfers, promotions"],
    ["Disciplinary Action","Perceived unfair suspension, punishment or termination"],
    ["Union Recognition","Management's refusal to recognise or deal with trade unions"],
    ["Management Practices","Victimisation of union members, unfair labour practices"],
    ["Economic Factors","Rising cost of living, economic inequality between management and workers"],
    ["Political Interference","Union rivalry, political workers' organisations using disputes for political gains"],
]
story.append(mkt(causes_data,[3.5*cm,W-7.5*cm],BROWN,[WHITE,BROWN_BG]))
story.append(Spacer(1,5))

story.append(Paragraph("4.2  Forms of Industrial Disputes",sub_t))
forms=[("Strike","Collective refusal by workers to work. Types: General Strike (all industries), Sympathetic Strike (support other workers), Stay-in/Sit-down Strike (remain in factory but refuse to work), Pen-down Strike, Go-slow."),
    ("Lockout","Employer's counterpart to strike — management closes the workplace or suspends operations temporarily to resist workers' demands. Defined under ID Act 1947."),
    ("Gherao","Workers surround and confine managers/supervisors in the workplace — a form of coercive pressure used in India. Legally controversial."),
    ("Picketing","Workers stand outside the workplace to persuade others not to enter and to publicise the dispute. Peaceful picketing is legal."),
    ("Boycott","Workers refuse to use or buy management's goods/services. Can extend to customers and suppliers."),
]
for f,d in forms: story.append(Paragraph(f"<b>{f}:</b> {d}",blt))

story.append(Paragraph("4.3  Machinery for Settlement of Industrial Disputes (ID Act 1947)",sec_t))
story.append(hl())
machinery=[["Method","Nature","Who Conducts","Binding?","When Used"],
    ["1. Works Committee","Bipartite — management + workers","Works Committee (statutory — factories with 100+ workers)","No","Day-to-day issues, minor disputes at workplace level"],
    ["2. Conciliation","Tripartite — neutral govt officer helps parties reach agreement","Conciliation Officer or Board of Conciliation (Govt appointed)","No (agreement is voluntary)","First step in formal dispute resolution under ID Act"],
    ["3. Voluntary Arbitration","Bipartite — both parties agree on neutral arbitrator","Agreed Arbitrator (private individual, retired judge)","Yes — arbitrator's award is binding","When parties trust each other enough to agree on an arbitrator"],
    ["4. Adjudication — Labour Court","Government quasi-judicial body","Presiding Officer of Labour Court","Yes — award is legally enforceable","Individual dismissal, disciplinary matters, rights disputes"],
    ["5. Adjudication — Industrial Tribunal","More powerful govt quasi-judicial body","Industrial Tribunal Presiding Officer","Yes","Wages, bonuses, hours, leave disputes affecting many workers"],
    ["6. Adjudication — National Tribunal","Highest govt adjudicatory body","National Industrial Tribunal","Yes","Disputes of national importance affecting multiple states"],
]
story.append(mkt(machinery,[2.5*cm,2*cm,3*cm,1.2*cm,W-12.7*cm],DARK_BLUE,[WHITE,LT_BLUE]))
story.append(Spacer(1,5))

story.append(Paragraph("4.4  Collective Bargaining",sub_t))
story.append(Paragraph("<b>Collective Bargaining (CB)</b> is the <b>process of negotiation between organised workers (through their union) and employers</b> to determine wages, hours, working conditions and other terms of employment. It is the most important preventive mechanism against industrial disputes.",body))
cb=[("Types of CB","Distributive Bargaining (win-lose — fixed pie dispute), Integrative Bargaining (win-win — finding creative solutions), Concessionary Bargaining (workers give up concessions during hard times), Productivity Bargaining (wage increases linked to productivity gains)."),
    ("Process of CB","(1) Preparation — both sides gather data; (2) Opening Demands — union presents demands; (3) Bargaining — negotiation rounds; (4) Agreement — settlement signed; (5) Implementation and Administration."),
    ("Role of CB in IR","Prevents disputes by providing a peaceful, systematic forum for resolving differences. Promotes industrial democracy. Agreements have legal standing."),
]
for t,d in cb: story.append(Paragraph(f"<b>{t}:</b> {d}",blt))

story.append(hl(ACC_BLUE,1.2))
story.append(qhdr("Topic 4: Dispute Resolution"))
story.append(hl(ACC_BLUE,1.2))
for item in qb(10,"Discuss the common causes of disputes in organisations. Explain the different methods of dispute resolution. (10 marks)",
    "CAUSES OF INDUSTRIAL DISPUTES:\nIndustrial disputes arise from conflicts between employers and workers on various issues:\n1. Wage and Allowance Disputes: Most common cause. Demands for higher wages, dearness allowance, bonus disputes and non-payment of wages create significant unrest.\n2. Working Conditions: Unsafe workplace, excessive hours, inadequate lighting/ventilation, faulty equipment cause worker dissatisfaction that escalates into collective action.\n3. Personnel Matters: Unfair dismissal, arbitrary retrenchment, forced transfers, denial of promotion and victimisation of union leaders are major flashpoints.\n4. Disciplinary Actions: Perceived unfair suspension or termination without due process triggers disputes.\n5. Union Recognition: Management's refusal to recognise a trade union or deal with it collectively is a fundamental IR conflict.\n6. Rising Cost of Living: When wages don't keep pace with inflation, workers organise to demand adjustments.\n7. Political Interference: Multiple unions with political affiliations sometimes manufacture disputes for political gains.\n\nMETHODS OF DISPUTE RESOLUTION (Under ID Act 1947):\n\n1. Works Committee: Statutory bipartite body (management + workers) in factories with 100+ workers. Handles day-to-day issues and minor disputes. First line of prevention.\n\n2. Conciliation: A government-appointed Conciliation Officer mediates between parties — facilitating discussion and helping them reach a voluntary agreement. The Conciliation Officer has no power to impose a solution. Non-binding unless parties agree.\n\n3. Voluntary Arbitration: Both parties agree on a neutral third-party arbitrator whose decision is binding on both. Faster than courts, less formal and preserves the relationship. An arbitrator's award is legally enforceable.\n\n4. Adjudication — Labour Court: Government quasi-judicial body that hears individual disputes — wrongful dismissal, disciplinary matters. Presiding Officer gives a legally binding award.\n\n5. Adjudication — Industrial Tribunal: Handles collective disputes affecting groups of workers — wages, hours, bonuses, working conditions. More powerful than Labour Court. Award is binding.\n\n6. Adjudication — National Tribunal: For disputes of national importance or those involving multiple states. Highest adjudicatory authority under the ID Act.\n\nCollective Bargaining: The most important preventive mechanism — unions and management negotiate wages and conditions periodically, reducing the build-up of resentment that leads to disputes.\n\nConclusion: A healthy IR system uses Works Committees and Collective Bargaining to prevent disputes, and uses Conciliation → Arbitration → Adjudication as a graduated escalation ladder when disputes do arise."):
    story.append(item)
for item in qb(5,"Evaluate the importance of communication and trust-building in managing virtual organisations. (5 marks)",
    "In virtual organisations (VOs), employees are geographically dispersed and interact primarily through digital channels — making communication and trust foundational to effective operation.\n\nImportance of Communication in VOs:\n1. Replaces Physical Presence: Without face-to-face interaction, explicit, frequent and structured communication becomes the only mechanism for coordination. Ambiguity in messages can derail projects.\n2. Prevents Isolation: Regular communication — video calls, team chats, virtual town halls — prevents employees from feeling isolated and disconnected from the organisation.\n3. Enables Collaboration: Technology-mediated communication (Slack, MS Teams, Zoom, email) must compensate for the informal hallway conversations of traditional offices.\n4. HR's Role: HR must implement communication protocols — response time norms, meeting frequency, escalation paths — and train employees in virtual communication etiquette.\n\nImportance of Trust in VOs:\n1. Replaces Supervisory Control: Managers cannot observe employees directly. Leadership in VOs is based on trust, not physical monitoring.\n2. Drives Performance: Research shows that high-trust virtual teams outperform low-trust teams significantly — members collaborate more freely and are more accountable.\n3. Builds Psychological Safety: Employees in trusting virtual environments are more willing to share ideas, admit mistakes and seek help.\n4. Reduces Micromanagement: Trust allows managers to focus on outcomes rather than time-monitoring, increasing employee autonomy and satisfaction.\n\nHR Strategies: Regular 1:1 check-ins, virtual team-building, transparent performance standards, recognition programmes, and consistent communication of organisational values are HR's tools for building trust in virtual settings."):
    story.append(item)
story.append(PageBreak())

# ══════════════════════════════════════════════════════
# TOPIC 5 — INTERNATIONAL HRM
# ══════════════════════════════════════════════════════
story.append(thdr("TOPIC 5: International Human Resource Management (IHRM)",80))
story.append(Spacer(1,4))

story.append(Paragraph("5.1  What is IHRM?",sec_t))
story.append(hl())
story.append(Paragraph("<b>International HRM (IHRM)</b> is the <b>process of procuring, allocating and effectively utilising human resources in an international business</b> — managing people across national boundaries. It involves managing three types of employees: Parent Country Nationals (PCNs), Host Country Nationals (HCNs) and Third Country Nationals (TCNs).",body))

emp_types=[["Employee Type","Definition","Example"],
    ["PCN (Parent Country National)","Citizens of the country where HQ is located — sent as expatriates","An Indian Infosys employee sent to the USA office"],
    ["HCN (Host Country National)","Citizens of the country where the subsidiary is located","A US citizen working in Infosys USA office"],
    ["TCN (Third Country National)","Citizens of a third country — neither HQ nor host country","A British citizen working for Indian company's Germany office"],
]
story.append(mkt(emp_types,[3*cm,5*cm,W-12*cm],TEAL,[WHITE,TEAL_BG]))
story.append(Spacer(1,5))

story.append(Paragraph("5.2  Differences: Domestic HRM vs IHRM",sub_t))
diff=[["Dimension","Domestic HRM","International HRM"],
    ["Geographic Scope","Single country","Multiple countries and cultures"],
    ["Complexity","Relatively simple — one legal system","High — multiple legal systems, cultures, currencies"],
    ["Functions","Standard HR functions","Standard + expatriate management, repatriation, cross-cultural training"],
    ["Risk","Lower","Higher — political risk, cultural risk, legal risk"],
    ["Labour Laws","Single national law system","Must comply with host country laws AND home country laws"],
    ["HR Focus","Efficiency and productivity","Also cultural sensitivity, legal compliance, global talent strategy"],
]
story.append(mkt(diff,[3*cm,4*cm,W-11*cm],PURPLE,[WHITE,PURPLE_BG]))
story.append(Spacer(1,5))

story.append(Paragraph("5.3  Challenges in IHRM",sec_t))
story.append(hl())
challenges=[("Cultural Differences","Every country has a unique culture — different attitudes towards authority, time, communication, gender roles and work-life balance. Geert Hofstede's 5 Cultural Dimensions (Power Distance, Individualism vs Collectivism, Uncertainty Avoidance, Masculinity vs Femininity, Long vs Short-term Orientation) help understand these differences. HR must design culturally sensitive policies."),
    ("Legal and Regulatory Compliance","Each host country has its own labour laws, tax laws, social security requirements, visa/work permit regulations and employment standards. Non-compliance can result in heavy fines and forced closures."),
    ("Managing Expatriates","Selecting, training, compensating, supporting and repatriating employees sent to work in foreign countries is complex and expensive. Expatriate failure rates are high (30-50%) without proper support."),
    ("Compensation Complexity","International compensation must consider: base salary in which currency, housing allowances, cost-of-living adjustments, tax equalisation, education allowances for children, home leave — making packages very complex."),
    ("Repatriation","Bringing expatriates back home after their assignment is as challenging as sending them. Many face reverse culture shock — they find home has changed, and their new skills are not utilised."),
    ("Diversity Management","Managing a diverse workforce across cultures, languages, religions and backgrounds requires inclusive HR policies, anti-discrimination frameworks and cultural competency training."),
    ("Political Risk","Political instability, expropriation risks, sanctions and sudden changes in government can disrupt IHRM operations. HR must have contingency plans."),
]
for c,d in challenges: story.append(Paragraph(f"<b>{c}:</b> {d}",blt))

story.append(Paragraph("5.4  Expatriate Management",sub_t))
story.append(Paragraph("<b>Expatriate Management</b> is one of the most critical IHRM functions. It involves:",body))
expat=[("Selection","Select employees with technical competence AND cultural sensitivity, language skills, adaptability and family stability. The family's willingness to relocate is crucial."),
    ("Pre-departure Training","Cross-cultural training (Hofstede dimensions, local customs), language training, briefing on host country laws, practical relocation assistance."),
    ("Compensation Package","Balance approach: Base salary + Cost-of-Living Adjustment (COLA) + Housing Allowance + Education Allowance + Home Leave allowance + Tax Equalisation + ESOP/incentives."),
    ("On-assignment Support","Cultural mentors, expat networks, regular check-ins by HR, family support (spouse employment assistance, school admission for children), EAP."),
    ("Repatriation Planning","Career planning for return, utilisation of international experience, reverse culture shock counselling — planned before departure, not just at the end."),
]
for t,d in expat: story.append(Paragraph(f"<b>{t}:</b> {d}",blt))

story.append(hl(ACC_BLUE,1.2))
story.append(qhdr("Topic 5: IHRM"))
story.append(hl(ACC_BLUE,1.2))
for item in qb(1.5,"State the challenge faced in managing expatriates. (1.5 marks)",
    "The main challenges in managing expatriates are: (1) Selection difficulty — choosing employees with both technical competence AND cultural adaptability, language skills and family willingness to relocate; (2) High failure rate — 30-50% of expatriate assignments fail due to poor cultural adjustment, family problems or inadequate support; (3) Compensation complexity — international packages must account for cost-of-living differences, housing, children's education and tax equalisation; (4) Repatriation — returning expatriates often face reverse culture shock and find their new global skills are underutilised."):
    story.append(item)
for item in qb(10,"Discuss the challenges and opportunities of managing a global workforce. How do cultural, economic and political differences impact HRM in multinational corporations? (10 marks)",
    "IHRM (International HRM) is the process of managing human resources across national boundaries. Managing a global workforce presents both significant challenges and valuable opportunities.\n\nCHALLENGES:\n1. Cultural Differences: Geert Hofstede's research identified 5 cultural dimensions (Power Distance, Individualism, Uncertainty Avoidance, Masculinity, Long-term Orientation) that vary dramatically across countries. Example: High Power Distance cultures (India, Japan) accept hierarchical management; low Power Distance cultures (Denmark, Netherlands) expect flat structures and open feedback.\n\n2. Legal Compliance: Each country has unique labour laws — employment contracts, minimum wages, working hours, termination procedures, social security, visa and work permit regulations. Non-compliance risks fines, litigation and forced closure.\n\n3. Expatriate Management: Selecting, training, compensating and repatriating expatriates is expensive and complex. Expatriate failure rates are 30-50% without proper cross-cultural training and family support.\n\n4. Compensation Complexity: International compensation must address currency fluctuations, cost-of-living differences, tax equalisation, housing, education and home leave — making packages significantly more complex than domestic pay.\n\n5. Economic Differences: Developed vs developing country wage expectations, purchasing power parity, inflation rates and local cost structures all affect compensation design.\n\n6. Political Risk: Government instability, nationalisation threats, sanctions, sudden policy changes can disrupt operations. HR must have evacuation and contingency plans.\n\nOPPORTUNITIES:\n1. Access to Global Talent: MNCs can recruit the best talent worldwide — specialists unavailable in the home country.\n2. Diverse Perspectives: Diverse global teams bring varied thinking styles that drive innovation.\n3. Knowledge Transfer: Global workforce facilitates sharing of best practices, technology and expertise across borders.\n4. 24/7 Operations: Time-zone-distributed workforce enables round-the-clock operations and customer service.\n\nConclusion: Successful global HRM requires cultural intelligence, legal expertise, flexible policies and strong expatriate support systems to convert global diversity into competitive advantage."):
    story.append(item)
story.append(PageBreak())

# ══════════════════════════════════════════════════════
# TOPIC 6 — KNOWLEDGE MANAGEMENT
# ══════════════════════════════════════════════════════
story.append(thdr("TOPIC 6: Knowledge Management in HRM",80))
story.append(Spacer(1,4))

story.append(Paragraph("6.1  What is Knowledge Management (KM)?",sec_t))
story.append(hl())
story.append(Paragraph("<b>Knowledge Management (KM)</b> is the systematic process of <b>creating, capturing, organising, sharing, applying and retaining knowledge and expertise</b> within the organisation — so that intellectual capital is not lost when people leave, retire or are transferred.",body))
story.append(Paragraph("Simple analogy: When a senior developer who knows how to fix a critical bug in the core system resigns, the company faces a knowledge blackout. KM prevents this by documenting the fix and training others before the person leaves.",imp))

story.append(Paragraph("Types of Knowledge:",sub_t))
know_types=[["Type","Definition","Example"],
    ["Explicit Knowledge","Formally documented, easily stored and shared","Manuals, procedures, databases, training materials, SOPs"],
    ["Tacit Knowledge","Personal experience-based, hard to articulate and transfer","A senior negotiator's intuition, a skilled artisan's technique"],
    ["Embedded Knowledge","Stored in organisational routines, culture and processes","Company culture, team collaboration patterns, organisational memory"],
]
story.append(mkt(know_types,[2.5*cm,4*cm,W-10.5*cm],TEAL,[WHITE,TEAL_BG]))
story.append(Spacer(1,5))

story.append(Paragraph("6.2  KM Process — SECI Model (Nonaka & Takeuchi)",sub_t))
seci=[["Mode","Meaning","Example"],
    ["Socialisation (T→T)","Tacit to Tacit: sharing experience through observation, apprenticeship, informal interaction","Junior learns from senior by working alongside them"],
    ["Externalisation (T→E)","Tacit to Explicit: converting experience into documented knowledge","Senior expert writes manual documenting their process"],
    ["Combination (E→E)","Explicit to Explicit: combining existing documented knowledge","Combining two reports into a comprehensive strategy document"],
    ["Internalisation (E→T)","Explicit to Tacit: learning from documented knowledge and practising until internalized","Reading the manual then practising until it becomes skill"],
]
story.append(mkt(seci,[3*cm,5*cm,W-12*cm],PURPLE,[WHITE,PURPLE_BG]))
story.append(Spacer(1,5))

story.append(Paragraph("6.3  Role of HR in Knowledge Management",sec_t))
story.append(hl())
km_hr=[("Creating KM Culture","HR builds incentives and recognition for knowledge sharing — 'Knowledge Champion' awards, linking KM participation to appraisal and promotion. Without culture, KM tools go unused."),
    ("Knowledge Capture","Before key employees leave, retire or transfer: knowledge transfer workshops, documentation handovers, successor shadowing programmes."),
    ("Knowledge Sharing","HR facilitates Communities of Practice (CoPs), after-action reviews (AARs), internal wikis, mentoring programmes, cross-functional teams."),
    ("HR + IT Partnership","HR partners with IT to ensure KM platforms (SharePoint, Confluence, internal wikis, AI chatbots) are user-friendly, adopted and maintained."),
    ("Learning & Development","Using project debriefs, reflection sessions and case-based learning — capturing institutional wisdom from past successes and failures."),
    ("Retention Strategies","The best KM is keeping knowledge-rich employees. HR designs competitive retention packages and career paths for key knowledge holders."),
]
for t,d in km_hr: story.append(Paragraph(f"<b>{t}:</b> {d}",blt))

story.append(Paragraph("Contemporary KM Challenges:",sub_t))
km_challenges=["Remote and hybrid work: Knowledge scattered across emails, chat logs, cloud drives — HR must build a Single Source of Truth.",
"Information overload: Too much data, not enough organised knowledge.",
"Rapid turnover: Institutional wisdom disappears faster than it can be documented.",
"Technology adoption gaps: Buying KM tools without embedding the culture makes them white elephants.",
"AI-generated knowledge: How to validate and integrate AI-generated insights into organisational knowledge."]
for k in km_challenges: story.append(Paragraph(f"&#8226; {k}",blt))

story.append(hl(ACC_BLUE,1.2))
story.append(qhdr("Topic 6: Knowledge Management"))
story.append(hl(ACC_BLUE,1.2))
for item in qb(5,"What is Knowledge Management? Explain the role of HR in KM. (5 marks)",
    "Knowledge Management (KM) is the systematic process of creating, capturing, sharing and retaining the knowledge and expertise of employees so that the organisation does not lose intellectual capital when people leave, retire or are transferred.\n\nTypes of Knowledge: Explicit (documented — manuals, SOPs), Tacit (personal experience — intuition, skill) and Embedded (organisational routines and culture).\n\nNonaka & Takeuchi's SECI Model: Knowledge conversion happens through Socialisation (tacit to tacit), Externalisation (tacit to explicit), Combination (explicit to explicit) and Internalisation (explicit to tacit).\n\nRole of HR in KM:\n1. Building KM Culture: HR creates incentives for knowledge sharing — Knowledge Champion awards, linking KM participation to appraisal scores and promotion decisions.\n2. Knowledge Capture: Before key employees retire or leave — knowledge transfer workshops, documentation drives, successor shadowing.\n3. Communities of Practice: HR facilitates cross-functional learning groups where employees share expertise regularly.\n4. Learning System Design: After-action reviews, project debriefs, case studies from past projects — capturing institutional wisdom from real experiences.\n5. IT Partnership: HR ensures KM platforms (wikis, chatbots, SharePoint) are user-friendly and actually adopted.\n6. Retention: The best KM is keeping knowledge holders — HR designs competitive packages and development paths for critical experts.\n\nKM is a contemporary HR issue because knowledge-intensive economies cannot afford knowledge loss — it directly impacts innovation, productivity and competitive advantage."):
    story.append(item)
story.append(PageBreak())

# ══════════════════════════════════════════════════════
# TOPIC 7 — HR AUDIT & ACCOUNTING
# ══════════════════════════════════════════════════════
story.append(thdr("TOPIC 7: HR Audit & HR Accounting",75))
story.append(Spacer(1,4))

story.append(Paragraph("7.1  What is HR Audit?",sec_t))
story.append(hl())
story.append(Paragraph("<b>HR Audit</b> is a <b>systematic, independent examination (health check) of all HR policies, practices, processes, records and compliance</b> — to determine whether they are legal, fair, efficient and aligned with business goals.",body))
story.append(Paragraph("Analogy: Just as a financial audit checks whether accounts are accurate and compliant, an HR audit checks whether people practices are correct and strategic. The auditor compares 'what the policy says' with 'what actually happens' and identifies gaps.",imp))

story.append(Paragraph("Types of HR Audit:",sub_t))
audit_types=[["Type","What is Checked","Example"],
    ["Compliance Audit","Adherence to labour laws — minimum wage, PF/ESI, working hours, anti-harassment, data privacy","Checking if overtime is paid correctly across all branches; verifying POSH committee exists"],
    ["Functional Audit","How well specific HR functions work — recruitment, training, performance, compensation, grievance","Measuring time-to-hire, quality-of-hire; checking if appraisals are done as per policy schedule"],
    ["Strategic Audit","Whether HR strategy supports business goals — talent pipeline, leadership bench, engagement","Evaluating if the current recruitment plan can support a planned 50% headcount increase"],
    ["Cultural Audit","Organisation's culture, values, diversity and inclusion effectiveness","Employee engagement surveys, D&I representation data, culture assessment"],
]
story.append(mkt(audit_types,[2.5*cm,4.5*cm,W-11*cm],DARK_BLUE,[WHITE,LT_BLUE]))
story.append(Spacer(1,5))

story.append(Paragraph("HR Audit Process:",sub_t))
audit_proc=[("1. Define Scope","Decide which HR areas to audit — e.g., performance management and compensation."),
    ("2. Design Audit Plan","Prepare questions, checklists and documents to review — policy manuals, HRIS data, employment contracts."),
    ("3. Collect Data","Review HR documents, interview managers and HR team, conduct employee surveys."),
    ("4. Analyse Findings","Compare 'what the policy says' vs 'what actually happens' — identify gaps, risks and non-compliance."),
    ("5. Prepare Report","Document findings, risk levels and recommended corrective actions with timelines."),
    ("6. Implement and Track","HR implements audit recommendations and tracks progress in follow-up audits."),
]
for s,d in audit_proc: story.append(Paragraph(f"<b>{s}:</b> {d}",blt))

story.append(Paragraph("7.2  What is HR Accounting (HRA)?",sec_t))
story.append(hl())
story.append(Paragraph("<b>Human Resource Accounting (HRA)</b> is the <b>process of identifying, measuring and reporting the cost and value of human resources as organisational assets</b> in financial terms — treating employees as human capital rather than just expenses.",body))

story.append(Paragraph("Methods of HRA:",sub_t))
hra_methods=[["Method","What it Measures","Example"],
    ["Historical Cost Method","Total cost of recruiting, hiring, training and developing each employee since joining","A software engineer: Rs 1 lakh recruitment + Rs 2 lakh training + Rs 12 lakh salary = Rs 15 lakh HRA value"],
    ["Replacement Cost Method","How much it would cost to hire and train a similar replacement employee today","Replacing the same engineer today would cost Rs 18 lakh — justifies retention investment"],
    ["Opportunity Cost Method","Value of the employee's next-best alternative use within or outside the org","An employee's market value based on what competitors would pay"],
    ["ROI / Value-Based Method","Financial returns from HR investments — training ROI, cost-per-hire, productivity per employee","Sales training costs Rs 5 lakh; sales increase Rs 10 lakh → ROI = 100%"],
    ["Economic Value Method","Present value of expected future services of employees discounted at appropriate rate","Actuarial/economic valuation of the human capital stock"],
]
story.append(mkt(hra_methods,[3.5*cm,4*cm,W-11.5*cm],GREEN_ACC,[WHITE,GREEN_BG]))
story.append(Spacer(1,5))

story.append(Paragraph("HR Audit vs HR Accounting — Difference:",sub_t))
diff_hrahr=[["Basis","HR Audit","HR Accounting"],
    ["Meaning","Systematic examination of HR policies and practices","Measuring and reporting value of human resources in financial terms"],
    ["Purpose","Identify compliance gaps, inefficiencies, misalignment","Show economic value and ROI of HR investments"],
    ["Output","HR Audit Report with recommendations","Financial figures — HRA value, ROI, replacement cost"],
    ["Focus","Process quality and legal compliance","Financial value of people"],
    ["Frequency","Annual or bi-annual","Ongoing financial reporting"],
]
story.append(mkt(diff_hrahr,[2.5*cm,4.5*cm,W-11*cm],TEAL,[WHITE,TEAL_BG]))
story.append(Spacer(1,5))

story.append(hl(ACC_BLUE,1.2))
story.append(qhdr("Topic 7: HR Audit & Accounting"))
story.append(hl(ACC_BLUE,1.2))
for item in qb(1.5,"Define HR Audit. / Differentiate between HR Audit and HR Accounting. (1.5 marks)",
    "HR Audit is a systematic health-check of all HR practices, policies, records and compliance to determine whether they are legal, fair, efficient and aligned with business goals. Types: Compliance (legal adherence), Functional (HR function effectiveness), Strategic (alignment with business goals). HR Accounting (HRA) is the process of measuring and reporting the economic value of human resources as assets — methods include Historical Cost, Replacement Cost and ROI-based value. Key difference: HR Audit checks HOW HR works; HRA measures WHAT HR is worth financially."):
    story.append(item)
story.append(PageBreak())

# ══════════════════════════════════════════════════════
# TOPIC 8 — HR IN VIRTUAL ORGANISATIONS
# ══════════════════════════════════════════════════════
story.append(thdr("TOPIC 8: HR in Virtual Organisations",75))
story.append(Spacer(1,4))

story.append(Paragraph("8.1  What is a Virtual Organisation (VO)?",sec_t))
story.append(hl())
story.append(Paragraph("A <b>Virtual Organisation (VO)</b> is a <b>technology-enabled organisation</b> where geographically dispersed employees (and sometimes external partners) collaborate through digital communication tools — without a traditional physical office structure.",body))

story.append(Paragraph("Characteristics of Virtual Organisations:",sub_t))
vo_chars=["Members are geographically dispersed but electronically connected.",
"Work is task/project-oriented — usually time-bound and goal-centric.",
"Communication happens through email, video conferencing, collaboration platforms (Slack, MS Teams, Zoom).",
"Traditional departments and physical office structures largely disappear.",
"Leadership and control are self-managed, not based on physical supervision.",
"Performance evaluation is based on outputs/results, not time spent in office."]
for c in vo_chars: story.append(Paragraph(f"&#8226; {c}",blt))

story.append(Paragraph("Benefits of Virtual Organisations:",sub_t))
vo_benefits=["Elimination of geographical barriers — global talent pool.",
"Significant reduction in overhead costs (no office rent, utilities, maintenance).",
"Round-the-clock operations across time zones.",
"Better work-life balance for employees (reduced commute, flexible hours).",
"Reduced absenteeism — employees work from home even when mildly unwell.",
"Access to specialised talent anywhere in the world.",
"Lower organisational carbon footprint — green advantage."]
for b in vo_benefits: story.append(Paragraph(f"✦ {b}",blt))

story.append(Paragraph("8.2  HR Challenges in Virtual Organisations",sec_t))
story.append(hl())
hr_vo=[("Recruitment & Selection","Must identify candidates who are self-directed, tech-savvy, highly productive without direct supervision, and capable of working in isolation. E-recruitment (online assessments, video interviews) is standard."),
    ("Onboarding & Induction","Virtual onboarding — digital orientation, online buddy systems, virtual introductions. Must ensure the new hire feels welcomed and connected despite never visiting a physical office."),
    ("Training & Development","E-learning platforms are essential — CBT (Computer-Based Training), WBT (Web-Based Training), virtual workshops, e-mentoring. Training must be self-paced and accessible 24/7."),
    ("Performance Management","No face-to-face observation. Performance is evaluated on outputs, results, goal achievement and quality standards. HR must define clear, measurable KPIs. Electronic performance monitoring tools are used."),
    ("Compensation","Pay should be output-based, not time-based. However, equity must be maintained — employees in different locations/countries may expect location-specific rates."),
    ("Communication & Trust","Most critical challenge. HR must implement: explicit communication protocols, regular video check-ins, virtual team-building, digital water-cooler conversations and periodic face-to-face meetings."),
    ("Maintaining Culture","Organisational culture is difficult to build and maintain virtually. HR must be deliberate about values communication, virtual celebrations, recognition programmes and inclusive practices."),
    ("Legal Compliance","Remote workers in different states/countries create complex legal and tax compliance challenges — local labour laws, data privacy (GDPR), tax treaties."),
]
for t,d in hr_vo: story.append(Paragraph(f"<b>{t}:</b> {d}",blt))

story.append(Paragraph("Traditional Organisation vs Virtual Organisation:",sub_t))
vo_vs=[["Dimension","Traditional Organisation","Virtual Organisation"],
    ["Physical Presence","Required — fixed office hours","Not required — location-independent"],
    ["Communication","Face-to-face, direct","Digital — email, video, chat"],
    ["Performance Appraisal","Activity and time-based","Output and results-based"],
    ["Leadership/Control","Hierarchical, top-down","Self-managed, output-driven"],
    ["HR/HRD","Physical HR department","e-HRM — digital HR platform"],
    ["Power Base","Position/hierarchy","Role and results"],
]
story.append(mkt(vo_vs,[3.5*cm,4.5*cm,W-12*cm],BROWN,[WHITE,BROWN_BG]))
story.append(Spacer(1,5))

story.append(hl(ACC_BLUE,1.2))
story.append(qhdr("Topic 8: HR in Virtual Organisations"))
story.append(hl(ACC_BLUE,1.2))
for item in qb(1.5,"Write a note on HR in virtual organisations. (1.5 marks)",
    "A Virtual Organisation (VO) is a technology-enabled organisation where geographically dispersed employees collaborate via digital tools (email, video conferencing, collaboration platforms) without a fixed physical office. HR in VOs is performed through e-HRM. Key HR challenges: selecting self-directed, tech-capable employees; virtual onboarding; e-learning-based training; output-based performance evaluation; communication and trust-building; maintaining organisational culture virtually; and complex legal compliance across locations. HR must adopt a strategic, flexible and cost-efficient approach — acting as a digital-first business partner rather than traditional personnel manager."):
    story.append(item)
story.append(PageBreak())

# ══════════════════════════════════════════════════════
# TOPIC 9 — ETHICS & CSR
# ══════════════════════════════════════════════════════
story.append(thdr("TOPIC 9: Ethics & Corporate Social Responsibility (CSR) in HRM",80))
story.append(Spacer(1,4))

story.append(Paragraph("9.1  Business Ethics in HRM",sec_t))
story.append(hl())
story.append(Paragraph("<b>Business Ethics</b> refers to the <b>application of moral principles — right vs wrong, good vs bad</b> — to business decisions and practices. HR ethics specifically relates to the fair, honest and responsible management of people.",body))

story.append(Paragraph("Key Ethical Issues in HRM:",sub_t))
eth_issues=[("Workplace Discrimination","Making adverse decisions against employees or applicants based on group membership (race, gender, religion, caste, disability) rather than individual merit. Three tests: decision is based on group membership, based on prejudice/stereotype, causes harm. HR must: hire on job-related criteria, ensure equal pay for equal work, offer merit-based promotions."),
    ("Privacy Violations","Employees have a right to privacy in personal matters (religion, lifestyle, political beliefs). Ethical dilemmas: CCTV monitoring, tapping phone calls, reading emails without consent, intrusive background checks, medical testing."),
    ("Performance Management Ethics","PA systems can be manipulated — ratings adjusted to promote/transfer/dismiss a specific person. HR must ensure objective, documented, bias-free evaluations."),
    ("Whistle-blowing","Disclosure by employees of illegal or unethical organisational practices. Ethical justification: report first internally → then externally only after internal channels are exhausted. Organisations must protect whistle-blowers from retaliation."),
    ("Safety and Health Ethics","Organisation's moral duty to provide a safe, hazard-free workplace. The Bhopal Gas Tragedy (Dec 3, 1984) — worst industrial disaster — 4,000 immediate deaths, 20,000+ over years — illustrates the catastrophic consequences of ethics failure in industrial safety."),
    ("Retrenchment Ethics","Retrenchment is not inherently unethical, but the manner matters — adequate notice, fair compensation, dignity in communication, exploring alternatives (reduced hours, pay cuts, hiring freeze) before layoffs."),
    ("Equal Pay for Equal Work","Equal Remuneration Act — prohibiting gender-based pay gaps for the same work. Gender pay gap remains a significant ethical challenge in India and globally."),
    ("Workplace Harassment (POSH)","Prevention of Sexual Harassment at Workplace Act (2013) mandates Internal Complaints Committees with zero tolerance. HR's role: establish policy, train employees, investigate complaints impartially."),
]
for t,d in eth_issues: story.append(Paragraph(f"<b>{t}:</b> {d}",blt))

story.append(Paragraph("Managing Ethics — Tools:",sub_t))
mgmt_eth=["Code of Ethics — written document stating acceptable/unacceptable behaviour for all employees.",
"Ethics Committee — governance body overseeing compliance and ethical dilemmas.",
"Ethics Training Programmes — regular training on ethical decision-making.",
"Whistle-blower Protection Policy — safe, anonymous reporting channels.",
"Compliance Department — dedicated team monitoring adherence to legal and ethical standards.",
"Ethical Leadership — top management modelling ethical behaviour (tone from the top)."]
for m in mgmt_eth: story.append(Paragraph(f"&#8226; {m}",blt))

story.append(Paragraph("9.2  Corporate Social Responsibility (CSR)",sec_t))
story.append(hl())
story.append(Paragraph("<b>CSR</b> is the <b>voluntary commitment by businesses to conduct themselves ethically, contribute to economic development, improve the quality of life of employees, their families, the local community and society at large</b> — while also being profitable.",body))
story.append(Paragraph("Carroll's CSR Pyramid (1979): Economic (be profitable) → Legal (obey laws) → Ethical (be ethical beyond law) → Philanthropic (be a good corporate citizen).",imp))

story.append(Paragraph("CSR in the HR Context:",sub_t))
csr_hr=[("Employee Well-being CSR","Going beyond statutory welfare — extended health insurance, mental health EAPs, flexible work, childcare. Treating employees as stakeholders, not just resources."),
    ("Diversity & Inclusion","Actively recruiting women, minorities, persons with disabilities, LGBTQ+ employees. Building inclusive cultures. Publishing D&I data."),
    ("Learning & Development","Investing in employees' lifelong learning — tuition reimbursement, skills training, career development. Building community skills through CSR programmes."),
    ("Fair Employment Practices","Paying fair wages (above minimum wage), safe working conditions, no forced labour or child labour in supply chains, fair termination practices."),
    ("Community Development","Skill development programmes for local communities, employment of local talent, supporting NGOs and education initiatives."),
    ("Environmental Sustainability","Green HRM — remote work reduces carbon footprint, sustainable office practices, energy-efficient workplaces, promoting eco-friendly behaviour."),
    ("Ethical Supply Chain","Ensuring suppliers and contractors also follow ethical labour practices — no child labour, forced labour or discrimination."),
]
for t,d in csr_hr: story.append(Paragraph(f"<b>{t}:</b> {d}",blt))

story.append(Paragraph("India's CSR Mandate — Section 135, Companies Act 2013:",sub_t))
story.append(Paragraph("Companies with annual turnover ≥ Rs 1,000 crore OR net worth ≥ Rs 500 crore OR net profit ≥ Rs 5 crore are required to spend at least 2% of their average 3-year net profit on CSR activities. CSR Committee must be formed. Activities include education, health, poverty alleviation, gender equality, environmental sustainability, rural development, Swachh Bharat, Skill India.",blt))

story.append(hl(ACC_BLUE,1.2))
story.append(qhdr("Topic 9: Ethics & CSR"))
story.append(hl(ACC_BLUE,1.2))
for item in qb(5,"Discuss the importance of corporate social responsibility. (5 marks)",
    "Corporate Social Responsibility (CSR) is a business's voluntary commitment to conduct itself ethically and contribute to society beyond its legal obligations. Carroll's CSR Pyramid identifies four levels: Economic (profitability), Legal (compliance), Ethical (beyond law) and Philanthropic (giving back).\n\nImportance of CSR:\n\n1. Employee Attraction and Retention: Millennials and Gen Z strongly prefer to work for socially responsible organisations. Companies with strong CSR records attract better talent and retain them longer — employees feel proud to be associated with a values-driven organisation.\n\n2. Enhanced Reputation and Brand Value: CSR activities build a positive public image. Consumers prefer CSR-active brands (Tata, ITC, Unilever). This translates directly into customer loyalty and revenue.\n\n3. Investor Confidence: ESG (Environmental, Social, Governance) investing is now mainstream. Companies with strong CSR/ESG scores attract more responsible investors and often enjoy higher market valuations.\n\n4. Employee Engagement: Employees who participate in CSR activities (volunteering, community programmes) report higher engagement, pride and job satisfaction.\n\n5. Risk Management: Ethical supply chains, fair labour practices and environmental responsibility reduce regulatory risk, legal exposure and reputational crises.\n\n6. Community Development: Skill development, education support and healthcare initiatives create human capital in the surrounding community — building the long-term talent pipeline.\n\n7. Legal Requirement (India): Section 135 of Companies Act 2013 mandates 2% of average net profit on CSR for eligible companies.\n\nIn conclusion, CSR transforms HR from a cost centre into a value creator — building human capital, social capital and reputational capital simultaneously."):
    story.append(item)
story.append(PageBreak())

# ══════════════════════════════════════════════════════
# QUICK REVISION CARD
# ══════════════════════════════════════════════════════
rb=Table([["⚡ QUICK REVISION CARD — MODULE 4: IR, WELFARE, DISPUTE, IHRM & CONTEMPORARY ISSUES"]],colWidths=[W-3.6*cm])
rb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),DARK_BLUE),('TEXTCOLOR',(0,0),(-1,-1),WHITE),
    ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),11),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
story.append(rb)
story.append(Spacer(1,8))

rev=[["Topic","Key Points to Remember","Exam %"],
    ["Industrial Relations","Dunlop's 3 actors: Employer + Workers/Union + Govt | 4 approaches: Unitary, Pluralist, Marxist, Systems | Objectives: peace, collective bargaining, productivity | Scope: labour laws, unions, CB, grievances, workers' participation","80%"],
    ["Grievance Handling","Grievance = real/imagined injustice | Causes: wages, conditions, supervision, promotion, discipline | 6-step procedure: Informal→Written→Senior Mgmt→Committee→Arbitration→Labour Court | Principles: speed, fairness, confidentiality","85%"],
    ["Employee Welfare","Labour Investigation Committee definition | Statutory: Factories Act (canteen, crèche), ESI, PF, Maternity Benefit, Gratuity, Bonus, Workmen's Compensation | Non-statutory: housing, health, transport, recreation, education, financial, WLB","80%"],
    ["Dispute Resolution","Causes: wages, conditions, personnel, discipline, union recognition | Forms: Strike, Lockout, Gherao, Picketing, Boycott | Machinery (ID Act 1947): Works Committee→Conciliation→Arbitration→Labour Court→Industrial Tribunal→National Tribunal","85%"],
    ["IHRM","PCN + HCN + TCN | Hofstede 5 dimensions | Challenges: culture, legal compliance, expatriate management, compensation, repatriation | Expatriate: selection, pre-departure training, compensation (COLA, housing, education, tax equalisation), repatriation","80%"],
    ["KM","Explicit+Tacit+Embedded | SECI: Socialisation, Externalisation, Combination, Internalisation (Nonaka & Takeuchi) | HR role: KM culture, knowledge capture, CoPs, e-learning, retention | Contemporary issues: remote work, fast turnover, silos","80%"],
    ["HR Audit & HRA","Audit = health check of HR practices | Types: Compliance, Functional, Strategic | Process: Scope→Plan→Data→Analyse→Report→Implement | HRA = value of people as assets | Methods: Historical Cost, Replacement Cost, ROI, Opportunity Cost","75%"],
    ["Virtual Org & HR","VO = tech-enabled distributed org | Benefits: no geographic barriers, lower costs, WLB | HR challenges: e-recruitment, virtual onboarding, e-learning, output-based PA, communication, culture building, legal compliance | e-HRM is primary mode","75%"],
    ["Ethics & CSR","Carroll's Pyramid: Economic→Legal→Ethical→Philanthropic | Ethical issues: discrimination, privacy, PA manipulation, whistle-blowing, safety, harassment (POSH) | Tools: Code of Ethics, Ethics Committee, Whistle-blower policy | CSR Section 135 = 2% profit","80%"],
]
revt=Table(rev,colWidths=[2.5*cm,W-7.5*cm,1.2*cm])
revt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),ACC_BLUE),('TEXTCOLOR',(0,0),(-1,0),WHITE),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,1),(1,-1),'Helvetica'),
    ('FONTNAME',(2,1),(2,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),7.5),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,LT_BLUE]),('TEXTCOLOR',(2,1),(2,-1),GREEN_ACC),
    ('ALIGN',(0,0),(-1,-1),'LEFT'),('ALIGN',(2,0),(2,-1),'CENTER'),
    ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ('LEFTPADDING',(0,0),(-1,-1),4),('VALIGN',(0,0),(-1,-1),'TOP'),
    ('BOX',(0,0),(-1,-1),1.5,ACC_BLUE),('INNERGRID',(0,0),(-1,-1),0.3,GREY_LINE)]))
story.append(revt)
story.append(Spacer(1,8))

tb=Table([["📌 KEY TERMS, ACTS, CASES & THEORISTS — MODULE 4"]],colWidths=[W-3.6*cm])
tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),ORA_ACC),('TEXTCOLOR',(0,0),(-1,-1),WHITE),
    ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),11),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
story.append(tb)
story.append(Spacer(1,5))

terms=[["Term / Person / Act","What to Remember"],
    ["Industrial Disputes Act, 1947","Foundation of IR machinery in India — defines dispute, provides conciliation, arbitration, adjudication"],
    ["Factories Act, 1948","Canteen (100+), crèche (30+ women), first aid (150+), lighting, ventilation — Section numbers often asked"],
    ["ESI Act, 1948","Medical + maternity + disability + sickness benefits | Employer: 3.25%, Employee: 0.75%"],
    ["PF Act, 1952","Employer + Employee each: 12% of basic salary | PF + Pension + Insurance"],
    ["Maternity Benefit Act, 1961 (2017)","26 weeks paid leave for 1st-2nd child | 12 weeks thereafter | Crèche mandatory for 50+ employees"],
    ["Gratuity Act, 1972","Formula: (15 × Last Salary × Years) / 26 | After 5+ years of service"],
    ["Dunlop (1958)","IR Systems Theory: 3 actors (Employer, Workers, Govt) + shared ideology + rules body"],
    ["Hofstede","5 Cultural Dimensions for IHRM: Power Distance, Individualism, Uncertainty Avoidance, Masculinity, Long-term Orientation"],
    ["Nonaka & Takeuchi","SECI Model of Knowledge Creation: Socialisation → Externalisation → Combination → Internalisation"],
    ["Carroll (1979)","CSR Pyramid: Economic → Legal → Ethical → Philanthropic"],
    ["POSH Act, 2013","Prevention of Sexual Harassment at Workplace | Mandatory Internal Complaints Committee (ICC)"],
    ["Bhopal Gas Tragedy","Dec 3, 1984 | Union Carbide | 4,000 immediate deaths | Worst industrial disaster | Ethics of industrial safety"],
    ["Section 135, Companies Act 2013","CSR mandate — 2% of 3-year average net profit for companies above threshold"],
    ["Whistle-blowing","Disclosing illegal/unethical practices | Justify by exhausting internal channels first | Must be protected from retaliation"],
    ["Keith Davis","Grievance = real or imagined feeling of personal injustice regarding employment relationship"],
]
termst=Table(terms,colWidths=[3.8*cm,W-7.8*cm])
termst.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#bf360c')),('TEXTCOLOR',(0,0),(-1,0),WHITE),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,1),(0,-1),'Helvetica-Bold'),
    ('FONTNAME',(1,1),(1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),8),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,ORA_BG]),('ALIGN',(0,0),(-1,-1),'LEFT'),
    ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
    ('LEFTPADDING',(0,0),(-1,-1),5),('VALIGN',(0,0),(-1,-1),'TOP'),
    ('BOX',(0,0),(-1,-1),1,colors.HexColor('#bf360c')),('INNERGRID',(0,0),(-1,-1),0.3,GREY_LINE)]))
story.append(termst)
story.append(Spacer(1,6))

# FINAL MASTER FORMULA SHEET
fb2=Table([["🏆 MASTER FORMULA & QUICK-FACTS SHEET"]],colWidths=[W-3.6*cm])
fb2.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),GREEN_ACC),('TEXTCOLOR',(0,0),(-1,-1),WHITE),
    ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),11),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
story.append(fb2)
story.append(Spacer(1,4))
formulas=[["Formula / Fact","Details"],
    ["Gratuity Formula","(15 days × Last Basic Salary × Completed Years of Service) ÷ 26"],
    ["Bonus Range","Minimum: 8.33% | Maximum: 20% of annual wages (Payment of Bonus Act)"],
    ["PF Contribution","Employer: 12% of Basic + DA | Employee: 12% of Basic + DA"],
    ["ESI Contribution","Employer: 3.25% | Employee: 0.75% of wages (for employees earning ≤ Rs 21,000/month)"],
    ["CSR Spending (India)","2% of average 3-year net profit | Applicable for companies with turnover ≥ Rs 1,000 Cr / net worth ≥ Rs 500 Cr / profit ≥ Rs 5 Cr"],
    ["Maternity Leave","26 weeks (1st & 2nd child) | 12 weeks (3rd+ child) | 8 weeks (adoption/surrogacy)"],
    ["ROI of Training","[(Benefits of Training − Cost of Training) / Cost of Training] × 100"],
    ["HRA — Replacement Cost","Cost to hire + train a similar employee TODAY if current one leaves"],
    ["Expatriate Failure Rate","30–50% without proper cross-cultural training and family support"],
    ["Kirkpatrick's 4 Levels","Level 1: Reaction | Level 2: Learning | Level 3: Behaviour | Level 4: Results"],
    ["Hofstede 5 Dimensions","Power Distance | Individualism | Uncertainty Avoidance | Masculinity | Long-term Orientation"],
]
fmlt=Table(formulas,colWidths=[4.5*cm,W-8.5*cm])
fmlt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),DARK_BLUE),('TEXTCOLOR',(0,0),(-1,0),WHITE),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,1),(0,-1),'Helvetica-Bold'),
    ('FONTNAME',(1,1),(1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),8.5),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,GREEN_BG]),('ALIGN',(0,0),(-1,-1),'LEFT'),
    ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ('LEFTPADDING',(0,0),(-1,-1),5),('VALIGN',(0,0),(-1,-1),'TOP'),
    ('BOX',(0,0),(-1,-1),1,DARK_BLUE),('INNERGRID',(0,0),(-1,-1),0.3,GREY_LINE)]))
story.append(fmlt)
story.append(Spacer(1,6))

fb=Table([["HRM Module 4 Notes | OEC-CS-602(I) | PYQ Analysis: Dec-2024, May-2025, Dec-2025 | All Modules Complete ✓"]],colWidths=[W-3.6*cm])
fb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),DARK_BLUE),('TEXTCOLOR',(0,0),(-1,-1),colors.HexColor('#c5cae9')),
    ('FONTNAME',(0,0),(-1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),8),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
story.append(fb)

doc.build(story)
print("Module 4 PDF created successfully!")