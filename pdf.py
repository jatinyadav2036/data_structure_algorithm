from reportlab.lib.pagesizes import A4
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable, PageBreak)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

DARK_BLUE   = colors.HexColor('#1a237e')
MID_BLUE    = colors.HexColor('#283593')
ACCENT_BLUE = colors.HexColor('#3949ab')
LIGHT_BLUE  = colors.HexColor('#e8eaf6')
GREEN_BG    = colors.HexColor('#e8f5e9')
GREEN_ACC   = colors.HexColor('#2e7d32')
ORANGE_ACC  = colors.HexColor('#e65100')
ORANGE_BG   = colors.HexColor('#fff3e0')
RED_ACC     = colors.HexColor('#b71c1c')
RED_BG      = colors.HexColor('#ffebee')
PURPLE      = colors.HexColor('#4a148c')
PURPLE_BG   = colors.HexColor('#f3e5f5')
TEAL        = colors.HexColor('#006064')
TEAL_BG     = colors.HexColor('#e0f7fa')
GREY_LINE   = colors.HexColor('#90a4ae')
WHITE       = colors.white

W, H = A4

doc = SimpleDocTemplate(
    "HRM_Module2_Notes.pdf",
    pagesize=A4,
    rightMargin=1.8*cm, leftMargin=1.8*cm,
    topMargin=1.5*cm, bottomMargin=1.5*cm
)

def S(name, **kw): return ParagraphStyle(name, **kw)

body      = S('Body', fontSize=9.5, fontName='Helvetica', leading=14, spaceAfter=4, alignment=TA_JUSTIFY)
bullet    = S('Bullet', fontSize=9.5, fontName='Helvetica', leading=13, spaceAfter=2, leftIndent=14, firstLineIndent=-10)
sub_title = S('SubTitle', fontSize=11, textColor=ACCENT_BLUE, fontName='Helvetica-Bold', leading=14, spaceBefore=6, spaceAfter=3)
sec_title = S('SecTitle', fontSize=13, textColor=MID_BLUE, fontName='Helvetica-Bold', leading=16, spaceBefore=8, spaceAfter=4)

def hline(color=GREY_LINE, t=0.8): return HRFlowable(width="100%", thickness=t, color=color, spaceAfter=4, spaceBefore=4)

def topic_header(text, pct):
    bg = GREEN_BG if pct>=75 else ORANGE_BG if pct>=50 else RED_BG
    tc = GREEN_ACC if pct>=75 else ORANGE_ACC if pct>=50 else RED_ACC
    star = "★★★" if pct>=75 else "★★☆" if pct>=50 else "★☆☆"
    t = Table([[text, f"{pct}% {star}"]], colWidths=[W-7.5*cm, 2.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),LIGHT_BLUE),('BACKGROUND',(1,0),(1,0),bg),
        ('TEXTCOLOR',(0,0),(0,0),DARK_BLUE),('TEXTCOLOR',(1,0),(1,0),tc),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),11),
        ('ALIGN',(0,0),(0,0),'LEFT'),('ALIGN',(1,0),(1,0),'CENTER'),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(0,0),8),('BOX',(0,0),(-1,-1),1,ACCENT_BLUE),
    ]))
    return t

def q_box(marks, q_text, answer_text):
    if marks == 1.5:   bg_col,hdr_col,badge = colors.HexColor('#e3f2fd'),colors.HexColor('#1565c0'),"1.5 Marks"
    elif marks == 5:   bg_col,hdr_col,badge = colors.HexColor('#f3e5f5'),colors.HexColor('#6a1b9a'),"5 Marks"
    elif marks == 10:  bg_col,hdr_col,badge = GREEN_BG,GREEN_ACC,"10 Marks"
    else:              bg_col,hdr_col,badge = ORANGE_BG,ORANGE_ACC,"15 Marks"
    t1 = Table([[f"Q: {q_text}", badge]], colWidths=[W-6.3*cm, 1.8*cm])
    t1.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),hdr_col),('TEXTCOLOR',(0,0),(-1,-1),WHITE),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),8.5),
        ('ALIGN',(1,0),(1,0),'CENTER'),('ALIGN',(0,0),(0,0),'LEFT'),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(0,0),6),
    ]))
    t2 = Table([[answer_text]], colWidths=[W-4.5*cm])
    t2.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),bg_col),('FONTNAME',(0,0),(-1,-1),'Helvetica'),
        ('FONTSIZE',(0,0),(-1,-1),8.5),('LEADING',(0,0),(-1,-1),12),
        ('ALIGN',(0,0),(-1,-1),'LEFT'),('TOPPADDING',(0,0),(-1,-1),5),
        ('BOTTOMPADDING',(0,0),(-1,-1),5),('LEFTPADDING',(0,0),(-1,-1),8),
        ('RIGHTPADDING',(0,0),(-1,-1),6),('BOX',(0,0),(-1,-1),0.5,hdr_col),
    ]))
    return [t1, t2, Spacer(1,5)]

def make_table(data, col_widths, hdr_color=MID_BLUE, row_colors=[WHITE, LIGHT_BLUE]):
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),hdr_color),('TEXTCOLOR',(0,0),(-1,0),WHITE),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,1),(-1,-1),'Helvetica'),
        ('FONTSIZE',(0,0),(-1,-1),8.5),('ROWBACKGROUNDS',(0,1),(-1,-1),row_colors),
        ('ALIGN',(0,0),(-1,-1),'LEFT'),('TOPPADDING',(0,0),(-1,-1),4),
        ('BOTTOMPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(-1,-1),5),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('BOX',(0,0),(-1,-1),1,hdr_color),
        ('INNERGRID',(0,0),(-1,-1),0.3,GREY_LINE),
    ]))
    return t

def qhdr(text): return Paragraph(f"<b>📝 EXAM QUESTIONS — {text}</b>", S('qh', fontSize=10.5, fontName='Helvetica-Bold', textColor=DARK_BLUE, spaceBefore=5, spaceAfter=4))

# ─────────────────────────────────────────────
story = []

# COVER
cover = Table([
    [Paragraph("HUMAN RESOURCE MANAGEMENT", S('ct', fontSize=26, textColor=WHITE, alignment=TA_CENTER, fontName='Helvetica-Bold', leading=32))],
    [Paragraph("OEC-CS-602 (I) | B.Tech 7th Semester", S('cs', fontSize=13, textColor=colors.HexColor('#c5cae9'), alignment=TA_CENTER, fontName='Helvetica'))],
    [Spacer(1,0.3*cm)],
    [Paragraph("MODULE 2", S('cm', fontSize=20, textColor=colors.HexColor('#fff9c4'), alignment=TA_CENTER, fontName='Helvetica-Bold'))],
    [Paragraph("HR Sourcing, Job Analysis, Job Design, Job Evaluation & Performance Management", S('cs2', fontSize=12, textColor=colors.HexColor('#c5cae9'), alignment=TA_CENTER, fontName='Helvetica-Bold', leading=16))],
    [Spacer(1,0.4*cm)],
], colWidths=[W-3.6*cm])
cover.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),DARK_BLUE),('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
story.append(Spacer(1,0.8*cm))
story.append(cover)

info = Table([["📘 PYQ Analysis: Dec-2024 | May-2025 | Dec-2025  |  All Questions with Full Answers Included"]], colWidths=[W-3.6*cm])
info.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#303f9f')),('TEXTCOLOR',(0,0),(-1,-1),colors.HexColor('#e8eaf6')),('FONTNAME',(0,0),(-1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),9.5),('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
story.append(info)
story.append(Spacer(1,0.4*cm))

toc_data = [["#","TOPIC","EXAM %"],
    ["1","HR Sourcing & Recruitment — Sources, Process","90%"],
    ["2","Selection — Process, Stages, Techniques","90%"],
    ["3","Placement, Induction & Socialization","75%"],
    ["4","Job Analysis — Job Description & Job Specification","85%"],
    ["5","Job Design — Approaches & Methods","80%"],
    ["6","Job Evaluation — Concept & Methods","80%"],
    ["7","Performance Management System — Appraisal & Counselling","95%"],
]
toc = Table(toc_data, colWidths=[0.6*cm, W-6*cm, 1.5*cm])
toc.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0),ACCENT_BLUE),('TEXTCOLOR',(0,0),(-1,0),WHITE),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,1),(-1,-1),'Helvetica'),
    ('FONTSIZE',(0,0),(-1,-1),9),('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,LIGHT_BLUE]),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),('ALIGN',(1,0),(1,-1),'LEFT'),('LEFTPADDING',(1,0),(1,-1),6),
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ('BOX',(0,0),(-1,-1),1,ACCENT_BLUE),('INNERGRID',(0,0),(-1,-1),0.3,GREY_LINE),
    ('TEXTCOLOR',(2,1),(2,-1),GREEN_ACC),('FONTNAME',(2,1),(2,-1),'Helvetica-Bold'),
]))
story.append(Paragraph("MODULE 2 — CONTENTS & EXAM PROBABILITY", S('toch', fontSize=11, fontName='Helvetica-Bold', textColor=DARK_BLUE, alignment=TA_CENTER, spaceAfter=6)))
story.append(toc)
story.append(PageBreak())

# ══════════════════════════════════════════════════════
# TOPIC 1 — RECRUITMENT
# ══════════════════════════════════════════════════════
story.append(topic_header("TOPIC 1: HR Sourcing & Recruitment — Sources, Process", 90))
story.append(Spacer(1,4))
story.append(Paragraph("1.1  What is Recruitment?", sec_title))
story.append(hline())
story.append(Paragraph("Recruitment is the process of <b>searching for prospective employees and stimulating them to apply for jobs in the organisation</b>. It is a positive process — it aims to attract as many candidates as possible to build a large talent pool from which the best can be selected.", body))
story.append(Paragraph("<b>Edwin Flippo:</b> Recruitment is the process of searching for prospective employees and stimulating them to apply for jobs.", bullet))
story.append(Paragraph("<b>Key difference:</b> Recruitment = POSITIVE (attract many). Selection = NEGATIVE (eliminate unsuitable).", S('note', fontSize=9.5, fontName='Helvetica-Bold', textColor=RED_ACC, spaceAfter=5, leftIndent=8)))

story.append(Paragraph("1.2  Sources of Recruitment", sec_title))
story.append(hline())
story.append(Paragraph("Recruitment sources are divided into two broad categories:", body))

src_data = [
    ["SOURCE","METHODS","ADVANTAGES","DISADVANTAGES"],
    ["INTERNAL SOURCES\n(from within the org)",
     "Promotions, Transfers, Job Rotation, Recalls from layoff, Employee Referrals, Internal Job Postings",
     "Cost-effective, faster, employees know the culture, boosts morale, no training needed for culture fit, strengthens loyalty",
     "Limited talent pool, stagnation of fresh ideas, may cause internal politics, inbreeding of ideas, creates new vacancy"],
    ["EXTERNAL SOURCES\n(from outside the org)",
     "Advertisements (newspaper, online), Job Portals (Naukri, LinkedIn), Campus Recruitment, Recruitment Agencies, Walk-ins, Employee Referrals (external), Labour contractors, Social Media (LinkedIn), AI-based tools",
     "Fresh talent & new ideas, larger pool of candidates, innovation, diversity in workforce, specialized skills available",
     "Costly, time-consuming, risk of bad hire, longer induction time, may demotivate existing employees"],
]
story.append(make_table(src_data, [2.5*cm, 4*cm, 4*cm, W-14.5*cm]))
story.append(Spacer(1,5))

story.append(Paragraph("1.3  The Recruitment Process (Step-by-Step)", sec_title))
story.append(hline())
steps_rec = [
    ("Step 1 — Identify Vacancy", "HR Planning reveals a gap. A vacancy arises due to retirement, resignation, expansion or new role creation. The need is formally communicated via a Manpower Requisition Form."),
    ("Step 2 — Job Analysis", "Conduct job analysis to prepare an accurate Job Description (duties, responsibilities) and Job Specification (qualifications, skills needed). This forms the basis of recruitment."),
    ("Step 3 — Decide Sourcing Strategy", "Decide whether to recruit internally (promotions, transfers) or externally (job portals, ads, agencies). Budget, urgency and role level influence this decision."),
    ("Step 4 — Advertise the Job", "Post the vacancy through appropriate channels — company website, Naukri, LinkedIn, campus drives, newspaper ads. The job ad must clearly state role, responsibilities, qualifications and how to apply."),
    ("Step 5 — Receive & Screen Applications", "Collect applications (resumes/CVs). Screen against minimum qualifications in the Job Specification. AI-based ATS tools auto-screen by keywords."),
    ("Step 6 — Shortlist Candidates", "Create a shortlist of candidates who meet the required profile. Shortlisted candidates are called for the selection process."),
    ("Step 7 — Selection Process", "Conduct tests, interviews and reference checks (detailed in Topic 2)."),
    ("Step 8 — Job Offer & Onboarding", "Make a formal offer letter. Once accepted, proceed to placement, induction and socialization."),
]
for s, d in steps_rec:
    story.append(Paragraph(f"<b>{s}:</b> {d}", bullet))
story.append(Spacer(1,5))

story.append(Paragraph("1.4  Modern Trends in Recruitment", sub_title))
trends = ["AI-Based Recruitment: Automated resume screening, chatbots for initial interviews (HireVue, Mya).",
"Social Media Recruiting: LinkedIn, Twitter, Instagram to post jobs and reach passive candidates.",
"Campus Recruitment: Visiting colleges and universities to hire fresh graduates.",
"Employee Referral Programmes (ERP): Existing employees recommend candidates — cheaper and more reliable.",
"Gig Economy & Freelancers: Hiring contractual/project-based talent through platforms like Upwork, Fiverr.",
"Employer Branding: Building the company's image as a great place to work to attract top talent organically."]
for t in trends: story.append(Paragraph(f"✦ {t}", bullet))

story.append(hline(ACCENT_BLUE, 1.2))
story.append(qhdr("Topic 1: Recruitment"))
story.append(hline(ACCENT_BLUE, 1.2))
for item in q_box(1.5,"Define Recruitment. State the different sources of recruitment. (1.5 marks)",
    "Recruitment is the process of attracting and encouraging prospective employees to apply for jobs (Edwin Flippo). It is a positive process aimed at building a large talent pool. Sources are: (1) Internal — promotions, transfers, employee referrals; (2) External — job portals (Naukri, LinkedIn), campus recruitment, advertisements, recruitment agencies, social media, AI-based tools."):
    story.append(item)
for item in q_box(15,"Discuss the various recruitment sources, including internal and external sources, and their advantages and disadvantages. (15 marks)",
    "Recruitment is the process of searching for prospective employees and stimulating them to apply for jobs. Sources of recruitment are broadly classified as Internal and External.\n\nINTERNAL SOURCES:\nInternal recruitment means filling vacancies from within the existing workforce.\n\n1. Promotions: Moving an employee to a higher position. Boosts morale, motivates performance.\n2. Transfers: Moving an employee from one department/location to another. Fills gaps without fresh hiring.\n3. Job Rotation: Employees gain experience across roles, preparing them for new positions.\n4. Employee Referrals: Existing employees recommend suitable candidates. Lower cost, high cultural fit.\n5. Recalls: Recalling employees who were laid off or who left under good terms.\n\nAdvantages of Internal Recruitment: Cheaper and faster, no cultural training needed, boosts employee morale, organisation already knows strengths and weaknesses of candidates, promotes loyalty.\n\nDisadvantages: Limited talent pool, no fresh ideas, internal politics, creates another vacancy, stagnation risk.\n\nEXTERNAL SOURCES:\n1. Advertisements: Newspaper, job portals (Naukri, Indeed, LinkedIn), company website. Reaches a large audience.\n2. Campus Recruitment: Visiting universities to hire fresh graduates. Brings in young, trainable talent.\n3. Recruitment Agencies: Placement agencies that match candidates with employers. Saves time but is costly.\n4. Walk-in Interviews: Candidates visit and apply directly. Common for mass hiring.\n5. Social Media: LinkedIn, Twitter. Ideal for reaching passive candidates not actively job-hunting.\n6. AI-Based Tools: ATS (Applicant Tracking Systems) auto-screens resumes; chatbots conduct initial interviews.\n7. Labour Contractors: Supplying contract workers for seasonal or short-term needs.\n\nAdvantages of External Recruitment: Fresh talent, innovative ideas, wider choice, helps achieve diversity targets, brings in specialised skills.\n\nDisadvantages: Expensive, time-consuming, risk of misfit, longer induction needed, may demotivate internal candidates.\n\nConclusion: A balanced mix of internal and external recruitment—using internal sources for culture-fit roles and external sources for fresh talent and specialised positions—gives the best results."):
    story.append(item)
story.append(PageBreak())

# ══════════════════════════════════════════════════════
# TOPIC 2 — SELECTION
# ══════════════════════════════════════════════════════
story.append(topic_header("TOPIC 2: Selection — Process, Stages & Techniques", 90))
story.append(Spacer(1,4))
story.append(Paragraph("2.1  What is Selection?", sec_title))
story.append(hline())
story.append(Paragraph("Selection is the process of <b>choosing the most suitable candidate from the pool of applicants attracted through recruitment</b>. It is a negative process — at each stage, unsuitable candidates are eliminated until the best fit is found.", body))
story.append(Paragraph("Recruitment vs Selection: Recruitment INVITES applications. Selection ELIMINATES unsuitable ones.", S('note2', fontSize=9.5, fontName='Helvetica-Bold', textColor=GREEN_ACC, spaceAfter=5, leftIndent=8)))

story.append(Paragraph("2.2  Selection Process — 8 Steps", sec_title))
story.append(hline())
sel_steps = [
    ("1. Preliminary Screening","Initial review of applications/CVs to eliminate candidates who clearly don't meet the minimum qualifications. Often done by ATS software or HR executives."),
    ("2. Selection Tests / Employment Tests","Objective tests to assess candidates' abilities:\n- Intelligence Tests (IQ): Measure mental ability, reasoning, memory.\n- Aptitude Tests: Potential to learn new skills (numerical, verbal, spatial).\n- Achievement/Proficiency Tests: Current skill level (typing speed, accounting test).\n- Personality Tests: Myers-Briggs, Big Five — assess behavioural traits.\n- Interest Tests: Holland's Interest Inventory — match career interests.\n- Psychometric Tests: Measure psychological traits; used for managerial roles."),
    ("3. Employment Interview","Most important stage. Interviewer evaluates the candidate face-to-face (or virtually).\nTypes of interviews: Structured (fixed questions), Unstructured (open-ended), Semi-structured, Panel Interview, Stress Interview, Behavioural Interview (STAR method), Situational Interview, Video Interview."),
    ("4. Reference & Background Checks","Verifying past employment, qualifications, criminal records and character from references provided by the candidate. Prevents fraudulent claims."),
    ("5. Medical / Physical Examination","Physical fitness test to ensure the candidate can perform the job without health risks. Mandatory for armed forces, certain factory roles, pilots, etc."),
    ("6. Selection Decision","After all rounds, the selection committee/HR manager takes the final decision. The candidate who best matches the job description and specification is chosen."),
    ("7. Job Offer","A formal offer letter is sent stating designation, CTC, joining date, benefits and terms of employment. The candidate must formally accept."),
    ("8. Contract of Employment","On joining, a formal employment contract is signed detailing roles, responsibilities, compensation, policies, confidentiality clauses and notice period."),
]
for s, d in sel_steps:
    story.append(Paragraph(f"<b>{s}:</b> {d}", bullet))
    story.append(Spacer(1,2))

story.append(Paragraph("2.3  Selection Techniques", sec_title))
story.append(hline())
tech_data = [
    ["Technique","Description","Best Used For"],
    ["Structured Interview","Pre-set questions asked to all candidates, scored on a scale. Reduces interviewer bias.","All roles — ensures fairness"],
    ["Assessment Centre","Multi-method evaluation: group discussions, in-basket exercises, role plays, presentations, psychometric tests. Observed by trained assessors.","Managerial & senior positions"],
    ["Psychometric Tests","Tests measuring personality, intelligence, emotional stability (MBTI, Big Five, 16PF).","Managerial, sales, counselling roles"],
    ["Work Sample Tests","Candidates perform actual job tasks. E.g., code review for IT, writing test for editors.","Technical and skilled roles"],
    ["Background Check","Verifying credentials, employment history, criminal records.","All critical roles"],
    ["Panel Interview","Multiple interviewers assess together. Reduces individual bias.","Senior and specialist roles"],
    ["Stress Interview","Deliberately creating pressure to test calmness and problem-solving under stress.","High-pressure roles like sales, journalism"],
    ["Video Interview","AI-scored video interviews analysing tone, expression, responses.","Mass hiring, initial screening"],
]
story.append(make_table(tech_data, [3*cm, 5.5*cm, W-12.5*cm], TEAL, [WHITE, TEAL_BG]))
story.append(Spacer(1,5))

story.append(hline(ACCENT_BLUE, 1.2))
story.append(qhdr("Topic 2: Selection"))
story.append(hline(ACCENT_BLUE, 1.2))
for item in q_box(1.5,"What is the meaning of Job Specification? How does it support selection? (1.5 marks)",
    "Job Specification is a written statement of the minimum qualifications, skills, physical characteristics and personality traits a person must possess to perform a job (Edwin Flippo: minimum acceptable human qualities). It supports selection by providing an objective checklist against which candidates are screened — ensuring only those who meet the requirements proceed to the next stage."):
    story.append(item)
for item in q_box(10,"Describe the various steps involved in the selection process, from initial screening to final appointment. (10 marks)",
    "Selection is the systematic process of choosing the most suitable candidate from applicants. Unlike recruitment which is positive (attracting many), selection is negative — eliminating unsuitable candidates at each stage.\n\nStep 1 — Preliminary Screening: HR reviews all applications/CVs and eliminates those not meeting minimum qualifications. ATS software automatically filters resumes based on keywords.\n\nStep 2 — Selection Tests: Objective tests to measure ability — Intelligence tests (IQ, reasoning), Aptitude tests (numerical, verbal), Achievement/Proficiency tests (current skills), Personality tests (Myers-Briggs, Big Five), and Psychometric tests for behavioural traits.\n\nStep 3 — Employment Interview: The most crucial stage. Types include Structured (fixed questions with scoring), Unstructured (open conversation), Panel (multiple interviewers), Stress (tests composure under pressure), Behavioural (STAR method: Situation, Task, Action, Result) and Video interviews.\n\nStep 4 — Reference and Background Checks: Past employers, academics and character references are contacted to verify claims made by the candidate. Criminal and academic background checks are conducted.\n\nStep 5 — Medical Examination: Physical fitness is checked to ensure the candidate can perform the job safely. Mandatory for physically demanding roles.\n\nStep 6 — Selection Decision: The selection committee reviews all data and selects the most suitable candidate. The decision must be objective, fair and documented.\n\nStep 7 — Job Offer: A formal offer letter is issued stating designation, CTC, joining date, benefits and conditions. The candidate accepts or negotiates.\n\nStep 8 — Contract of Employment: On joining, a legal employment contract is signed covering all terms — duties, pay, notice period, confidentiality, leave policy.\n\nA well-designed selection process reduces hiring errors, ensures legal compliance and improves long-term retention by finding the right person for the right job."):
    story.append(item)
story.append(PageBreak())

# ══════════════════════════════════════════════════════
# TOPIC 3 — PLACEMENT, INDUCTION & SOCIALIZATION
# ══════════════════════════════════════════════════════
story.append(topic_header("TOPIC 3: Placement, Induction & Socialization", 75))
story.append(Spacer(1,4))

story.append(Paragraph("3.1  Placement", sec_title))
story.append(hline())
story.append(Paragraph("<b>Placement</b> is the actual assignment of a specific job to a selected candidate. It is the process of fitting the right person into the right job after the selection decision is made.", body))
story.append(Paragraph("Placement is concerned with: (a) Assigning the role as per the Job Description; (b) Specifying the reporting structure; (c) Communicating performance expectations; (d) Explaining compensation and terms.", bullet))

story.append(Paragraph("3.2  Difference: Placement vs Induction", sub_title))
diff_data = [
    ["Basis","Placement","Induction"],
    ["Meaning","Assigning a specific job to the selected employee","Welcoming and orienting the new employee to the organisation"],
    ["Purpose","To match the employee to the right role","To help the employee settle in and feel at home"],
    ["Timing","Immediately after selection","After placement — first few days/weeks of joining"],
    ["Focus","Job assignment, duties, reporting structure","Organisation culture, policies, colleagues, facilities"],
    ["Outcome","Employee knows WHAT to do","Employee knows HOW the organisation works and WHO is who"],
]
story.append(make_table(diff_data, [2.5*cm, 4.5*cm, W-11*cm], PURPLE, [WHITE, PURPLE_BG]))
story.append(Spacer(1,5))

story.append(Paragraph("3.3  Induction / Orientation", sec_title))
story.append(hline())
story.append(Paragraph("<b>Induction</b> (also called Orientation) is the process of <b>receiving and welcoming new employees</b> when they first join a company, and giving them the basic information they need to settle in quickly and happily. It makes the new employee feel part of the team from day one.", body))

story.append(Paragraph("What Induction Covers:", sub_title))
ind_items = [("Company Introduction","History, vision, mission, values, products/services, organisational structure, key departments."),
("Policies & Rules","HR policies — attendance, leave, code of conduct, anti-harassment, IT usage, dress code."),
("Role Introduction","Detailed explanation of job duties, KPIs, reporting manager, team members, work tools."),
("Facilities & Infrastructure","Tour of the office — workstation, cafeteria, restrooms, parking, security, IT systems login."),
("Benefits & Compensation","Pay structure, insurance, PF/ESI, leave entitlement, reimbursements, ESOPs."),
("Mentorship / Buddy System","New employee is paired with an experienced buddy for the first 30–90 days."),
("Compliance Training","Mandatory training on safety, workplace ethics, POSH (Prevention of Sexual Harassment), data security."),
]
for t, d in ind_items: story.append(Paragraph(f"&#8226; <b>{t}:</b> {d}", bullet))

story.append(Paragraph("Importance of Effective Induction:", sub_title))
imp = ["Faster productivity: Employee can contribute sooner without confusion.",
"Reduced turnover: Good induction improves retention — employees feel valued.",
"Better engagement: Employee feels connected, motivated and part of the team.",
"Fewer mistakes: Clear communication of rules and expectations reduces errors.",
"Positive employer brand: Good onboarding = employees recommend the company."]
for i in imp: story.append(Paragraph(f"✦ {i}", bullet))

story.append(Paragraph("3.4  Socialization", sec_title))
story.append(hline())
story.append(Paragraph("<b>Organisational Socialization</b> is the ongoing process through which a new employee <b>learns the values, norms, culture, behaviours and social knowledge</b> required to become a full, accepted member of the organisation. It goes beyond the formal induction — it includes informal learning from colleagues.", body))
story.append(Paragraph("Stages of Socialization (Van Maanen & Schein):", sub_title))
soc_stages = [("Pre-arrival Stage","Everything the new employee brings in — prior work experience, personality, education, expectations. Happens before joining."),
("Encounter Stage","The new employee encounters the real organisation. May face surprises — gap between expectations and reality (reality shock)."),
("Metamorphosis Stage","The new employee adjusts and changes to fit the organisation. Becomes a productive, accepted member. Role is mastered, relationships formed."),
]
for s, d in soc_stages: story.append(Paragraph(f"&#8226; <b>{s}:</b> {d}", bullet))

story.append(hline(ACCENT_BLUE, 1.2))
story.append(qhdr("Topic 3: Placement, Induction & Socialization"))
story.append(hline(ACCENT_BLUE, 1.2))
for item in q_box(1.5,"Differentiate between Placement and Induction. (1.5 marks)",
    "Placement is the process of assigning a specific job role to a selected candidate — matching the person to the right position with defined duties and reporting structure. Induction (Orientation) is the subsequent process of welcoming and familiarising the new employee with the organisation's culture, policies, facilities and people. Placement answers 'what is the job?'; Induction answers 'how does this organisation work?'"):
    story.append(item)
for item in q_box(5,"Explain the induction process and its importance in reducing employee turnover. (5 marks)",
    "Induction is the formal process of receiving and welcoming new employees and giving them basic information to settle into their new role comfortably and quickly. A well-structured induction programme typically covers:\n\n1. Company Introduction: History, vision, mission, values, products, services and organisational structure.\n2. HR Policies: Attendance, leave, code of conduct, dress code, anti-harassment policies.\n3. Role Introduction: Job duties, KPIs, reporting manager, team members and tools.\n4. Facilities: Office tour — workstation, cafeteria, IT systems and security.\n5. Buddy System: Pairing the new hire with an experienced mentor for 30-90 days.\n6. Compliance Training: Safety, data security, POSH training.\n\nImportance of Effective Induction:\n1. Reduces Turnover: Studies show most employees quit in the first 90 days. A good induction makes them feel valued and committed, reducing early exits.\n2. Faster Productivity: Clear onboarding means the employee spends less time confused and more time contributing.\n3. Better Engagement: Employees who feel welcomed and informed are more motivated and loyal.\n4. Fewer Errors: Awareness of rules and expectations reduces costly mistakes.\n5. Positive Culture: Good induction embeds the company values and culture from day one.\n\nIn short, induction is an investment — companies with structured onboarding see significantly higher retention rates and productivity."):
    story.append(item)
story.append(PageBreak())

# ══════════════════════════════════════════════════════
# TOPIC 4 — JOB ANALYSIS
# ══════════════════════════════════════════════════════
story.append(topic_header("TOPIC 4: Job Analysis — Job Description & Job Specification", 85))
story.append(Spacer(1,4))

story.append(Paragraph("4.1  What is Job Analysis?", sec_title))
story.append(hline())
story.append(Paragraph("<b>Job Analysis</b> is the systematic process of <b>studying and collecting information about the operations, duties, responsibilities, qualifications and working conditions</b> of a specific job. It is the foundation of all HR activities.", body))
story.append(Paragraph("Edwin Flippo: Job analysis is the process of studying and collecting information relating to the operations and responsibility of a specific job.", bullet))
story.append(Paragraph("Harry Wylie: Job analysis deals with the anatomy of the job — the complete study of the job embodying every known and determinable factor, including duties, conditions, performance nature, qualifications required and conditions of employment.", bullet))

story.append(Paragraph("4.2  Uses / Importance of Job Analysis", sub_title))
uses = ["HR Planning — determines manpower requirements.",
"Recruitment & Selection — job description and specification guide hiring.",
"Training & Development — identifies skill gaps and training needs.",
"Performance Appraisal — sets KPIs based on job duties.",
"Job Evaluation — determines the worth/grade of a job.",
"Job Design — redesigns jobs for better efficiency and satisfaction.",
"Compensation Management — links pay to job difficulty and responsibility.",
"Career Planning — maps progression paths for employees.",
"Safety & Health — identifies hazardous job conditions for prevention.",
"Organisation Audit — understanding all roles in the organisation."]
for u in uses: story.append(Paragraph(f"&#8226; {u}", bullet))

story.append(Paragraph("4.3  Process / Steps of Job Analysis", sec_title))
story.append(hline())
ja_steps = [
    ("1. Collect Background Information","Review existing org charts, process documents and previous job descriptions."),
    ("2. Select Representative Jobs","Choose sample jobs to be analysed — especially important when there are many similar positions."),
    ("3. Collect Job Analysis Data","Gather information using methods: Personal Observation, Questionnaires/Surveys, Individual Interviews, Group Interviews, Maintenance of log/diary records."),
    ("4. Prepare Job Description","Document the duties, tasks, responsibilities and working conditions of the job."),
    ("5. Develop Job Specification","Convert job analysis data into a statement of human qualifications required to perform the job."),
]
for s, d in ja_steps: story.append(Paragraph(f"<b>{s}:</b> {d}", bullet))

story.append(Paragraph("4.4  Job Description (JD)", sec_title))
story.append(hline())
story.append(Paragraph("<b>Job Description</b> is an <b>organised factual statement of the duties, responsibilities and working conditions of a specific job</b>. It focuses on the JOB — what is to be done, how it is done and why.", body))
story.append(Paragraph("Edwin Flippo: Job Description is an organised factual statement of the duties and responsibilities of a specific job — it should tell what is to be done, how it is done and why.", bullet))

jd_data = [["Contents of a Job Description"],
    ["1. Job Title — e.g., HR Manager, Software Engineer"],
    ["2. Job Location / Department — HR Department, Floor 3"],
    ["3. Job Summary — brief 2-3 line description of the overall purpose"],
    ["4. Duties & Tasks — complete list (daily, weekly, monthly) with estimated time"],
    ["5. Supervision Given & Received — who the job holder reports to and who reports to them"],
    ["6. Tools, Machines, Equipment Used"],
    ["7. Working Conditions — location, environment, hazards, shift"],
    ["8. Salary/Pay Structure — basic pay, allowances, incentives"],
    ["9. Promotional Opportunities"],
]
jd_t = Table(jd_data, colWidths=[W-3.6*cm])
jd_t.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(0,0),GREEN_ACC),('TEXTCOLOR',(0,0),(0,0),WHITE),
    ('FONTNAME',(0,0),(0,0),'Helvetica-Bold'),('FONTNAME',(0,1),(0,-1),'Helvetica'),
    ('FONTSIZE',(0,0),(-1,-1),9),('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,GREEN_BG]),
    ('ALIGN',(0,0),(-1,-1),'LEFT'),('TOPPADDING',(0,0),(-1,-1),3),
    ('BOTTOMPADDING',(0,0),(-1,-1),3),('LEFTPADDING',(0,0),(-1,-1),8),
    ('BOX',(0,0),(-1,-1),1,GREEN_ACC),('INNERGRID',(0,0),(-1,-1),0.3,GREY_LINE),
]))
story.append(jd_t)
story.append(Spacer(1,5))

story.append(Paragraph("4.5  Job Specification (JS)", sec_title))
story.append(hline())
story.append(Paragraph("<b>Job Specification</b> is a written statement of the <b>minimum acceptable human qualities (qualifications, skills, experience, traits) required to perform a job</b>. It focuses on the PERSON — who should do the job.", body))
story.append(Paragraph("Edwin Flippo: Job Specification is a statement of minimum acceptable human qualities necessary to perform a job properly.", bullet))

js_data = [["Job Specification Covers"],
    ["1. Educational Qualifications — minimum degree, certifications required"],
    ["2. Work Experience — years of experience, type of experience"],
    ["3. Technical Skills — programming, data analysis, machine operation"],
    ["4. Soft Skills — communication, leadership, teamwork, problem-solving"],
    ["5. Physical Fitness — strength, stamina (for physical jobs)"],
    ["6. Intelligence & Mental Requirements — analytical ability, attention to detail"],
    ["7. Personality Traits — emotional stability, adaptability, initiative"],
    ["8. Special Qualities — travel readiness, language skills, driving licence"],
]
js_t = Table(js_data, colWidths=[W-3.6*cm])
js_t.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(0,0),TEAL),('TEXTCOLOR',(0,0),(0,0),WHITE),
    ('FONTNAME',(0,0),(0,0),'Helvetica-Bold'),('FONTNAME',(0,1),(0,-1),'Helvetica'),
    ('FONTSIZE',(0,0),(-1,-1),9),('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,TEAL_BG]),
    ('ALIGN',(0,0),(-1,-1),'LEFT'),('TOPPADDING',(0,0),(-1,-1),3),
    ('BOTTOMPADDING',(0,0),(-1,-1),3),('LEFTPADDING',(0,0),(-1,-1),8),
    ('BOX',(0,0),(-1,-1),1,TEAL),('INNERGRID',(0,0),(-1,-1),0.3,GREY_LINE),
]))
story.append(js_t)
story.append(Spacer(1,5))

jd_vs_js = [
    ["Basis","Job Description","Job Specification"],
    ["Focus","The JOB","The PERSON"],
    ["Content","Duties, responsibilities, working conditions","Qualifications, skills, experience, traits"],
    ["Question Answered","What does the job require?","Who should do the job?"],
    ["Purpose","Tells candidate what they will do","Tells HR what to look for in a candidate"],
    ["Used For","Recruitment ads, performance standards","Screening, shortlisting, selection tests"],
]
story.append(Paragraph("JD vs JS — Quick Comparison:", sub_title))
story.append(make_table(jd_vs_js, [2.5*cm, 4.5*cm, W-11*cm], PURPLE, [WHITE, PURPLE_BG]))
story.append(Spacer(1,5))

story.append(hline(ACCENT_BLUE, 1.2))
story.append(qhdr("Topic 4: Job Analysis, JD & JS"))
story.append(hline(ACCENT_BLUE, 1.2))
for item in q_box(1.5,"What is the meaning of Job Specification? (1.5 marks)",
    "Job Specification is a written statement of minimum acceptable human qualities — qualifications, skills, experience, intelligence and personality traits — that a person must possess to perform a job effectively. Edwin Flippo: Job specification is a statement of minimum acceptable human qualities necessary to perform a job properly. It focuses on the PERSON required, not the job itself."):
    story.append(item)
for item in q_box(1.5,"Explain the meaning of Job Rotation. (1.5 marks)",
    "Job Rotation is a job design technique where employees are periodically moved from one job to another over a set time period. The jobs themselves are not changed — only the employees rotate among various roles. Benefits: reduces boredom and monotony, builds multi-skill capability, prepares employees for contingencies, improves cross-functional understanding. Limitation: does not fundamentally change the nature of jobs, so motivated employees may still feel unchallenged."):
    story.append(item)
for item in q_box(15,"What is job analysis? How do job description and job specification support HR decisions? (15 marks)",
    "Job analysis is the systematic process of studying and collecting information about the operations, duties, responsibilities, working conditions and qualifications of a specific job (Edwin Flippo). It is the cornerstone of all HR activities.\n\nProcess of Job Analysis:\n1. Collect background information from org charts and previous JDs.\n2. Select representative jobs to analyse.\n3. Collect data using personal observation, questionnaires, interviews and log records.\n4. Prepare Job Description documenting duties and conditions.\n5. Develop Job Specification stating required human qualities.\n\nJOB DESCRIPTION (JD):\nJob Description is an organised factual statement of duties, responsibilities, working conditions and requirements of a specific job (Flippo). It tells WHAT is done, HOW it is done and WHY. Key contents: Job title, location, summary, complete duties list, supervision structure, tools used, working conditions, salary, promotional channels.\n\nRole of JD in HR Decisions:\n- Recruitment: JD forms the basis of job advertisements, clearly communicating what the role involves.\n- Performance Management: KPIs are derived from the duties listed in the JD.\n- Training: Gaps between current performance and JD requirements identify training needs.\n- Legal: JD serves as evidence of job requirements in disputes.\n\nJOB SPECIFICATION (JS):\nJob Specification is a statement of minimum acceptable human qualities needed to perform a job properly (Flippo). It focuses on the PERSON. Key contents: educational qualifications, work experience, technical skills, soft skills, physical requirements, personality traits, special qualities.\n\nRole of JS in HR Decisions:\n- Recruitment Advertising: Specifies what candidates must bring — helps attract the right pool.\n- Screening & Shortlisting: HR uses JS as a checklist to eliminate unqualified applicants.\n- Selection Tests: Tests are designed around the competencies listed in the JS.\n- Compensation: JS complexity (skills required) justifies higher pay grades through job evaluation.\n\nIn summary, JD answers 'What is the job?' while JS answers 'Who can do it?' Together, they ensure the right person is placed in the right role, reducing hiring errors, improving performance and supporting fair pay structures."):
    story.append(item)
story.append(PageBreak())

# ══════════════════════════════════════════════════════
# TOPIC 5 — JOB DESIGN
# ══════════════════════════════════════════════════════
story.append(topic_header("TOPIC 5: Job Design — Approaches & Methods", 80))
story.append(Spacer(1,4))

story.append(Paragraph("5.1  What is Job Design?", sec_title))
story.append(hline())
story.append(Paragraph("<b>Job Design</b> is the process of <b>deciding on the content, duties, responsibilities, methods and relationships of a job</b> — to satisfy both the organisational requirements (productivity, efficiency) and the individual employee's needs (satisfaction, motivation).", body))
story.append(Paragraph("Michael Armstrong: Job design is the process of deciding on the content of a job in terms of its duties and responsibilities; on the methods to be used in carrying out the job; and on the relationships that should exist between the job holder and superiors, subordinates and colleagues.", bullet))

story.append(Paragraph("Two Goals of Job Design:", sub_title))
story.append(Paragraph("1. Organisational Goal — higher productivity, operational efficiency, quality output, cost reduction.", bullet))
story.append(Paragraph("2. Individual Goal — employee satisfaction, interest, challenge, sense of achievement and accomplishment.", bullet))

story.append(Paragraph("Poorly Designed Jobs Lead To:", sub_title))
poor = ["Boredom and monotony","High absenteeism","Increased employee turnover","Reduced motivation","Low job satisfaction","Suboptimal productivity","Higher organisational costs"]
for p in poor: story.append(Paragraph(f"✗ {p}", bullet))

story.append(Paragraph("5.2  Approaches / Methods of Job Design", sec_title))
story.append(hline())

story.append(Paragraph("A. Job Simplification", sub_title))
story.append(Paragraph("Jobs are broken down into their <b>smallest, simplest units</b>. Each worker performs a small, repetitive subunit of the total job. Based on Taylor's Scientific Management — time-motion studies, standardisation.", body))
story.append(Paragraph("Advantages: Requires little training, less costly unskilled labour, high speed, easy to supervise. Disadvantages: High monotony and boredom, reduced motivation, no skill growth.", bullet))

story.append(Paragraph("B. Job Rotation", sub_title))
story.append(Paragraph("Employees are <b>periodically moved from one job to another</b> at the same level. The jobs themselves don't change — only employees rotate. Reduces boredom, builds multi-skills, prepares employees for contingencies.", body))
story.append(Paragraph("Limitation: Does not change the basic nature of jobs — employees may still feel monotonous jobs are being rotated.", bullet))

story.append(Paragraph("C. Job Enlargement (Horizontal Expansion)", sub_title))
story.append(Paragraph("Adding <b>more tasks of a similar nature</b> to a job — expanding the scope horizontally. Combats boredom from over-specialisation. Example: A typist who only types is also given filing, sorting mail and drafting simple letters — all similar-level tasks.", body))
story.append(Paragraph("Advantage: More variety, reduces monotony. Limitation: Just 'more of the same' — may not increase meaningfulness or responsibility.", bullet))

story.append(Paragraph("D. Job Enrichment (Vertical Expansion)", sub_title))
story.append(Paragraph("Adding <b>higher-level responsibilities, autonomy and decision-making authority</b> to a job — expanding vertically. Based on Herzberg's Two-Factor Theory. Gives employees achievement, recognition, responsibility, advancement and growth.", body))
story.append(Paragraph("Example: A delivery worker who only loaded boxes is now also responsible for verifying customer orders — vertical expansion of responsibility.", bullet))
story.append(Paragraph("Advantage: Increases intrinsic motivation, satisfaction, productivity. Limitation: Not suitable for everyone; some employees may feel overwhelmed.", bullet))

story.append(Paragraph("5.3  Three Approaches to Job Design", sec_title))
story.append(hline())
app_data = [
    ["Approach","Theorist","Key Idea","Focus"],
    ["Scientific Management Approach","F.W. Taylor","Standardise jobs into one best way. Specialisation, time-motion studies, monetary rewards.","Efficiency, productivity"],
    ["Behavioural Approach","Herzberg's Two-Factor Theory; Hackman & Oldham's Job Characteristics Model","Job must provide psychological meaning, responsibility and knowledge of results. Job enrichment is the tool.","Motivation, satisfaction"],
    ["Socio-Technical Systems Approach","Trist & Bamforth","Both technical system (machines, processes) AND social system (people, relationships) must be jointly optimised. Work teams, not just individual jobs.","Holistic, team-based design"],
]
story.append(make_table(app_data, [3.5*cm, 3*cm, 5.5*cm, W-16*cm], ORANGE_ACC, [WHITE, ORANGE_BG]))
story.append(Spacer(1,5))

story.append(Paragraph("5.4  Hackman & Oldham's Job Characteristics Model", sub_title))
story.append(Paragraph("The most influential model of job design. Five core job dimensions lead to three psychological states, which lead to high performance and satisfaction:", body))
hjo_data = [
    ["Core Job Dimension","Psychological State","Outcome"],
    ["1. Skill Variety — uses multiple skills","Experienced Meaningfulness of Work","High intrinsic motivation"],
    ["2. Task Identity — does a whole, complete piece of work","Experienced Meaningfulness","High quality work performance"],
    ["3. Task Significance — job impacts others","Experienced Meaningfulness","High satisfaction"],
    ["4. Autonomy — freedom and independence","Experienced Responsibility","Low absenteeism & turnover"],
    ["5. Feedback — knowledge of actual results","Knowledge of Results","Personal growth"],
]
story.append(make_table(hjo_data, [5*cm, 4.5*cm, W-13.5*cm], TEAL, [WHITE, TEAL_BG]))
story.append(Spacer(1,5))

story.append(hline(ACCENT_BLUE, 1.2))
story.append(qhdr("Topic 5: Job Design"))
story.append(hline(ACCENT_BLUE, 1.2))
for item in q_box(1.5,"State two approaches to job design. (1.5 marks)",
    "Two approaches to job design are: (1) Scientific Management Approach (F.W. Taylor) — jobs are standardised into their most efficient form through time-motion studies, specialisation and monetary incentives to maximise efficiency; (2) Behavioural Approach (Herzberg) — jobs must be enriched with meaningful tasks, autonomy and responsibility to satisfy higher-level needs and motivate employees through intrinsic rewards."):
    story.append(item)
for item in q_box(10,"Explain Job Enrichment and Job Enlargement. How do they differ from each other? (10 marks)",
    "Job Enrichment and Job Enlargement are both techniques of job design aimed at overcoming the disadvantages of over-specialisation and division of labour, but they differ fundamentally in approach.\n\nJOB ENLARGEMENT (Horizontal Expansion):\nJob Enlargement involves adding more tasks of a similar nature to a job without increasing the level of responsibility or authority. It is a horizontal expansion — more of the same kind of work.\n\nExample: A data entry operator who only enters data is also assigned the task of sorting reports, filing documents and preparing summaries. All tasks are at the same skill level.\n\nObjective: To combat monotony by giving the employee more variety in tasks.\nAdvantage: Reduces boredom, gives a broader view of the work.\nLimitation: Merely more of the same — does not make the job more challenging or meaningful. Employees may refer to it sarcastically as 'the same meaningless job, just more of it.'\n\nJOB ENRICHMENT (Vertical Expansion):\nJob Enrichment involves adding higher-level responsibilities, greater autonomy, decision-making authority and opportunities for growth to a job. It is a vertical expansion — work is made more challenging and meaningful.\n\nBasis: Herzberg's Two-Factor Theory — to truly motivate employees, the job itself must provide achievement, recognition, responsibility, advancement and growth.\n\nExample: A worker who only loaded delivery boxes is now also responsible for verifying customer orders, managing inventory for his route, and resolving delivery complaints — a vertical expansion of responsibility.\n\nObjective: To improve intrinsic motivation, job satisfaction and productivity.\nAdvantage: High motivation, job satisfaction, lower absenteeism, better quality of work.\nLimitation: Not all employees want more responsibility; some prefer routine. Requires training and adjustment.\n\nKEY DIFFERENCE:\nJob Enlargement = MORE work at the SAME level (horizontal). Job Enrichment = HIGHER level work with MORE responsibility (vertical). Enlargement adds variety; Enrichment adds meaning and autonomy. Enrichment is generally more effective at improving motivation."):
    story.append(item)
story.append(PageBreak())

# ══════════════════════════════════════════════════════
# TOPIC 6 — JOB EVALUATION
# ══════════════════════════════════════════════════════
story.append(topic_header("TOPIC 6: Job Evaluation — Concept & Methods", 80))
story.append(Spacer(1,4))

story.append(Paragraph("6.1  What is Job Evaluation?", sec_title))
story.append(hline())
story.append(Paragraph("<b>Job Evaluation</b> is a <b>systematic way of determining the value or worth of a job in relation to other jobs in an organisation</b>. It makes a systematic comparison between jobs to assess their relative worth, for the purpose of establishing a rational and equitable pay structure.", body))
story.append(Paragraph("Important: Job Evaluation assesses the JOB, NOT the person doing the job.", S('note3', fontSize=9.5, fontName='Helvetica-Bold', textColor=RED_ACC, spaceAfter=5, leftIndent=8)))

story.append(Paragraph("6.2  Features of Job Evaluation", sub_title))
feats = ["It tries to assess jobs, not people (job holder).",
"Standards of job evaluation are relative, not absolute.",
"The basis of job evaluation is job analysis — it begins with JD and JS.",
"It is carried out by a committee, not by an individual.",
"Some degree of subjectivity is always present.",
"The outcome is an equitable, rational wage structure."]
for f in feats: story.append(Paragraph(f"&#8226; {f}", bullet))

story.append(Paragraph("6.3  Process of Job Evaluation", sec_title))
story.append(hline())
je_process = [("1. Gaining Acceptance","Explain the purpose and benefits of job evaluation to management and employees/unions. Overcome resistance."),
("2. Creating Job Evaluation Committee","Form a committee of HR experts, managers and employee representatives to ensure objectivity and fairness."),
("3. Finding Jobs to be Evaluated","Identify all jobs (or a representative sample) that need to be evaluated."),
("4. Analysing & Preparing Job Description","Conduct job analysis and prepare accurate JDs for each job to be evaluated."),
("5. Selecting the Method of Evaluation","Choose the appropriate method: Ranking, Classification, Factor Comparison or Point Method."),
("6. Classifying Jobs","Apply the chosen method, rank or grade jobs according to their relative worth."),
("7. Installing the Programme","Implement the new pay structure based on job evaluation results. Communicate to all employees."),
("8. Reviewing Periodically","Review the job evaluation programme regularly (every 2-3 years) as jobs evolve with technology and business changes."),
]
for s, d in je_process: story.append(Paragraph(f"<b>{s}:</b> {d}", bullet))
story.append(Spacer(1,5))

story.append(Paragraph("6.4  Methods of Job Evaluation", sec_title))
story.append(hline())

story.append(Paragraph("Method 1: Ranking Method (Non-Quantitative)", sub_title))
story.append(Paragraph("The <b>simplest</b> method. Jobs are arranged from highest to lowest in order of their value/merit to the organisation. The job at the top has the highest value; the job at the bottom has the lowest. Jobs are ranked department-wise and combined for an organisation ranking. Pay is assigned based on rank.", body))
story.append(Paragraph("Merit: Simple, quick, low cost. Best for small organisations. Demerit: Highly subjective, no definite criteria, difficult in large organisations.", bullet))

story.append(Paragraph("Method 2: Classification / Grading Method (Non-Quantitative)", sub_title))
story.append(Paragraph("Jobs are grouped into <b>pre-defined grades or classes</b>. Grade descriptions are prepared first, then each job is matched to the most appropriate grade.", body))
grade_data = [["Grade","Category","Example Jobs"],
    ["Class 1","Executives","Office Manager, Deputy Manager"],["Class 2","Skilled Workers","Cashier, Purchasing Assistant"],
    ["Class 3","Semi-Skilled","Stenographers, Machine Operators"],["Class 4","Less Skilled","Daftaris, File Clerks, Office Boys"]]
story.append(make_table(grade_data, [1.5*cm, 3.5*cm, W-9*cm], PURPLE, [WHITE, PURPLE_BG]))
story.append(Paragraph("Merit: Less subjective, easy to understand, acceptable to employees. Demerit: Cumbersome, oversimplifies differences, tendency for subjective classification.", bullet))
story.append(Spacer(1,4))

story.append(Paragraph("Method 3: Factor Comparison Method (Quantitative)", sub_title))
story.append(Paragraph("Instead of ranking whole jobs, <b>each job is ranked on specific compensable factors</b> (mental effort, physical effort, skill, responsibility, working conditions). Money values are assigned to each factor level. The total wage = sum of money values across all factors.", body))
story.append(Paragraph("Steps: Select 15-20 key jobs → identify factors → rank key jobs on each factor → assign money values → rate all other jobs by comparing to key jobs.", bullet))
story.append(Paragraph("Merit: Systematic, money directly assigned. Demerit: Complex, time-consuming, hard to construct, may become inaccurate over time.", bullet))

story.append(Paragraph("Method 4: Point Method (Quantitative) — Most Widely Used", sub_title))
story.append(Paragraph("Jobs are broken into <b>compensable factors</b> (skill, effort, responsibility, working conditions). Each factor is divided into degrees/levels. Points are assigned to each degree. Total points for a job = sum of points across all factors. Total points are converted to a money wage rate.", body))
point_data = [["Factor","Degree 1","Degree 2","Degree 3","Degree 4","Degree 5","Max"],
    ["Skill","10","20","30","40","50","150"],["Physical Effort","8","16","24","32","40","120"],
    ["Mental Effort","5","10","15","20","25","75"],["Responsibility","7","14","21","28","35","105"],["Working Conditions","6","12","18","24","30","90"]]
story.append(make_table(point_data, [3*cm, 1.4*cm, 1.4*cm, 1.4*cm, 1.4*cm, 1.4*cm, 1.2*cm], TEAL, [WHITE, TEAL_BG]))
story.append(Paragraph("Merit: Most objective, widely used, systematic, easy to update. Demerit: Complex to develop, time-consuming, costly for managerial jobs.", bullet))
story.append(Spacer(1,5))

je_compare = [
    ["Method","Type","How Evaluated","Advantage","Disadvantage"],
    ["Ranking","Non-Quantitative","Subjective whole-job ordering","Quick, simple, cheap","Entirely subjective"],
    ["Classification","Non-Quantitative","Match job to grade descriptions","Readily available, easy to use","Cumbersome, oversimplified"],
    ["Factor Comparison","Quantitative","Compare job to key jobs on factors","Easy to use, systematic","Hard to construct, inaccurate over time"],
    ["Point Method","Quantitative","Points to factors and sub-factors","Accurate, widely accepted","Complex, costly"],
]
story.append(Paragraph("Comparison of All 4 Methods:", sub_title))
story.append(make_table(je_compare, [3*cm, 2.5*cm, 4*cm, 3.5*cm, W-17*cm], MID_BLUE))
story.append(Spacer(1,5))

story.append(hline(ACCENT_BLUE, 1.2))
story.append(qhdr("Topic 6: Job Evaluation"))
story.append(hline(ACCENT_BLUE, 1.2))
for item in q_box(1.5,"Why is Job Evaluation important? (1.5 marks)",
    "Job Evaluation is important because: (1) It establishes a rational, equitable pay structure — linking pay to the actual requirements of the job, not personal preferences; (2) It reduces pay inequity and grievances by ensuring similar jobs receive similar pay; (3) It provides a scientific basis for compensation management; (4) It helps evaluate new jobs objectively; (5) It ensures employees and unions trust the fairness of the pay system."):
    story.append(item)
for item in q_box(10,"Explain the four methods of Job Evaluation with their merits and demerits. (10 marks)",
    "Job evaluation is the systematic process of determining the relative worth of jobs in an organisation to establish a fair, rational pay structure.\n\nMethod 1: Ranking Method\nThe simplest method — jobs are arranged from highest to lowest in order of their value/merit. No specific criteria are used; the entire job is subjectively ranked.\nMerit: Simple, quick, inexpensive — best for small organisations.\nDemerit: Highly subjective, no clear criteria, ranks may offend employees, difficult in large organisations.\n\nMethod 2: Classification/Grading Method\nPre-defined grade descriptions are prepared first (e.g., Class 1: Executives, Class 2: Skilled Workers, Class 3: Semi-Skilled). Each job is then matched to the most appropriate class based on its duties.\nMerit: Less subjective than ranking, easy to understand, widely acceptable.\nDemerit: Oversimplifies complex jobs, tendency to use subjective judgment when jobs don't fit neatly into a grade.\n\nMethod 3: Factor Comparison Method\nEach job is ranked on specific compensable factors — mental effort, physical effort, skill required, responsibility and working conditions. Money values are assigned to each level of each factor. The wage for any job = sum of money values across all factors.\nExample: A painter's wage = Electrician's skill value + Fitter's mental effort value + Welder's physical effort value, etc.\nMerit: Systematic, directly links factors to money, easy to use once established.\nDemerit: Hard to construct, inaccurate over time as wages change.\n\nMethod 4: Point Method (Most Widely Used)\nJobs are analysed on compensable factors (skill, effort, responsibility, working conditions) which are divided into degrees. Points are assigned to each degree. Total points for a job determine its pay grade. Jobs with similar total points are placed in the same pay grade.\nMerit: Most objective and scientific, widely used, flexible, easy to update, reduces subjective bias.\nDemerit: Complex and time-consuming to design, expensive, may be inaccurate for managerial jobs where work cannot be easily quantified.\n\nConclusion: The Point Method is considered superior because it is the most accurate, objective and widely accepted. The Ranking Method is best for small organisations needing a quick solution."):
    story.append(item)
story.append(PageBreak())

# ══════════════════════════════════════════════════════
# TOPIC 7 — PERFORMANCE MANAGEMENT SYSTEM
# ══════════════════════════════════════════════════════
story.append(topic_header("TOPIC 7: Performance Management System — Appraisal & Counselling", 95))
story.append(Spacer(1,4))

story.append(Paragraph("7.1  What is Performance Management System (PMS)?", sec_title))
story.append(hline())
story.append(Paragraph("<b>Performance Management System (PMS)</b> is a <b>continuous process of setting goals, measuring performance, providing feedback, coaching employees and linking performance to rewards</b>. It is not just annual appraisal — it is an ongoing cycle that aligns individual performance with organisational objectives.", body))
story.append(Paragraph("PMS Cycle: Goal Setting → Performance Monitoring → Performance Review (Appraisal) → Feedback & Coaching → Reward / Development Plan → New Goal Setting", S('note4', fontSize=9.5, fontName='Helvetica-Bold', textColor=MID_BLUE, spaceAfter=5, leftIndent=8)))

story.append(Paragraph("7.2  Performance Appraisal — Definition & Purpose", sec_title))
story.append(hline())
story.append(Paragraph("<b>Performance Appraisal</b> is the <b>systematic evaluation of an employee's job performance</b> by comparing actual performance against pre-defined standards, goals or expected behaviour, and communicating the results to the employee.", body))
story.append(Paragraph("Objectives of Performance Appraisal:", sub_title))
obj_pa = ["Provide feedback on performance strengths and weaknesses.",
"Identify training and development needs.",
"Make decisions on promotions, increments, transfers, terminations.",
"Set new performance goals for the next period.",
"Motivate employees through recognition of good performance.",
"Provide documentation for HR decisions (legal protection).",
"Improve communication between manager and employee.",
"Support succession planning by identifying high-potential employees."]
for o in obj_pa: story.append(Paragraph(f"&#8226; {o}", bullet))

story.append(Paragraph("7.3  Methods of Performance Appraisal", sec_title))
story.append(hline())

story.append(Paragraph("A. Traditional Methods", sub_title))
trad_methods = [
    ("1. Graphic Rating Scale","The most widely used traditional method. A rating scale lists traits (quality of work, initiative, teamwork) and the appraiser rates the employee on each trait on a scale (1=Poor to 5=Excellent). Simple but subjective."),
    ("2. Ranking Method","Employees are ranked from best to worst performer. Simple comparison. Limitation: No clear criteria, difficult for large groups."),
    ("3. Paired Comparison","Each employee is compared with every other employee one at a time. The employee who wins the most comparisons is ranked highest."),
    ("4. Forced Distribution / Bell Curve","Employees are forced into a distribution (e.g., top 20%, middle 70%, bottom 10%). Popularised by Jack Welch at GE. Advantage: Prevents leniency. Limitation: Unfair in high-performing teams."),
    ("5. Critical Incident Method","Appraiser records specific incidents — both very good and very bad — of the employee's performance throughout the year. More objective than rating scales."),
    ("6. Essay / Narrative Appraisal","Manager writes a descriptive essay about the employee's performance. Subjective, time-consuming but comprehensive."),
    ("7. Checklist Method","A list of descriptive statements about job behaviour. Appraiser checks 'YES' or 'NO' for each statement. Simple to use."),
    ("8. MBO (Management by Objectives)","Developed by Peter Drucker. Manager and employee together set SMART goals at the start of the period. At the end, performance is judged against those mutually agreed goals. Employee is involved — increases commitment. Modern and widely used."),
]
for m, d in trad_methods: story.append(Paragraph(f"<b>{m}:</b> {d}", bullet))

story.append(Paragraph("B. Modern Methods", sub_title))
modern_methods = [
    ("9. 360-Degree Feedback / Appraisal","Most comprehensive modern method. Feedback is collected from ALL directions: Self, Superiors (above), Subordinates (below), Peers (same level) and Customers. Gives a holistic, multi-source picture of performance. Reduces bias. Used widely in leadership development."),
    ("10. Assessment Centres","Multi-day evaluation using in-basket exercises, group discussions, role plays, presentations and psychometric tests. Mainly used for managerial selection and development."),
    ("11. Behaviourally Anchored Rating Scales (BARS)","Combines graphic rating scale with critical incident method. Specific behavioural examples anchor each rating point. More objective than simple rating scales."),
    ("12. Balanced Scorecard (BSC)","Kaplan and Norton's model. Measures performance on 4 dimensions: Financial, Customer, Internal Business Processes, Learning and Growth. Used for strategic performance management."),
    ("13. OKR (Objectives and Key Results)","Used by Google, Intel. Employees set ambitious Objectives and define 3-5 measurable Key Results for each. Promotes transparency and alignment."),
    ("14. HR Analytics / Data-Driven Appraisal","Using data dashboards, productivity metrics, attendance, project completion rates and customer satisfaction scores to provide objective performance evidence."),
]
for m, d in modern_methods: story.append(Paragraph(f"<b>{m}:</b> {d}", bullet))
story.append(Spacer(1,4))

trad_vs_mod = [
    ["Basis","Traditional Methods","Modern Methods"],
    ["Focus","Past performance","Past + Future development"],
    ["Frequency","Annual","Continuous / quarterly"],
    ["Feedback source","Manager only","Multiple sources (360 degrees)"],
    ["Employee involvement","Low","High (MBO, OKR)"],
    ["Objectivity","Low (subjective)","Higher (BARS, data analytics)"],
    ["Examples","Graphic Rating, Ranking, Essay","360-degree, MBO, BARS, OKR, BSC"],
]
story.append(Paragraph("Traditional vs Modern Appraisal — Comparison:", sub_title))
story.append(make_table(trad_vs_mod, [3*cm, 4.5*cm, W-11.5*cm], MID_BLUE))
story.append(Spacer(1,5))

story.append(Paragraph("7.4  Employee Counselling in Performance Management", sec_title))
story.append(hline())
story.append(Paragraph("<b>Employee Counselling</b> is a <b>confidential, supportive discussion between a manager/HR and an employee</b> aimed at helping the employee understand their performance issues, identify root causes, and develop an improvement plan. It is a key part of performance management.", body))

story.append(Paragraph("Types of Counselling:", sub_title))
counsel_types = [
    ("Directive Counselling","The counsellor (manager) tells the employee exactly what the problem is and what they need to do. Manager-driven. Best for clear performance violations."),
    ("Non-Directive Counselling","The employee is encouraged to talk freely and identify their own solutions. Counsellor listens and guides without imposing. Best for personal/emotional issues."),
    ("Participative / Eclectic Counselling","A balanced approach — both counsellor and employee discuss issues together and agree on a plan. Most commonly used in organisations."),
]
for t, d in counsel_types: story.append(Paragraph(f"<b>{t}:</b> {d}", bullet))

story.append(Paragraph("Role of Counselling in Performance Management:", sub_title))
counsel_role = ["Helps employees understand their performance gap — where they are vs where they should be.",
"Identifies root causes of poor performance (personal issues, skill gap, unclear goals, poor tools).",
"Develops a concrete improvement plan — training, coaching, mentoring or resources.",
"Prevents escalation — counselling resolves issues before they become disciplinary problems.",
"Boosts employee morale — feeling supported increases commitment and engagement.",
"Reduces turnover — employees who receive counselling feel valued and stay longer.",
"Documents performance issues — creates a formal record for HR decisions."]
for c in counsel_role: story.append(Paragraph(f"&#8226; {c}", bullet))

story.append(hline(ACCENT_BLUE, 1.2))
story.append(qhdr("Topic 7: PMS, Appraisal & Counselling"))
story.append(hline(ACCENT_BLUE, 1.2))
for item in q_box(15,"Define a performance management system. Explain the different methods of performance appraisal. Discuss the importance of counselling in the performance management process. (15 marks)",
    "A Performance Management System (PMS) is a continuous, integrated process of setting goals, monitoring performance, appraising results, providing feedback and linking outcomes to rewards and development. Unlike a simple annual appraisal, PMS is an ongoing cycle: Goal Setting → Performance Monitoring → Appraisal → Feedback & Coaching → Reward/Development → New Goals.\n\nMETHODS OF PERFORMANCE APPRAISAL:\n\nTRADITIONAL METHODS:\n1. Graphic Rating Scale: Most widely used. Traits like quality, initiative, teamwork rated on a 1-5 scale by the appraiser. Simple but subjective.\n2. Ranking Method: Employees ranked best to worst. Simple but no clear criteria.\n3. Forced Distribution (Bell Curve): Employees distributed into top/middle/bottom percentages. Prevents leniency bias; unfair in high-performing teams.\n4. Critical Incident Method: Manager records specific notable incidents throughout the year — both positive and negative. More objective.\n5. MBO (Management by Objectives): Manager and employee jointly set SMART goals. Performance judged against mutually agreed targets. Increases employee ownership and commitment (Peter Drucker).\n6. Essay Method: Manager writes a descriptive evaluation. Comprehensive but subjective and time-consuming.\n\nMODERN METHODS:\n7. 360-Degree Appraisal: Most comprehensive. Feedback collected from all directions — self, superiors, subordinates, peers and customers. Reduces individual bias, gives holistic picture. Used in leadership development.\n8. BARS (Behaviourally Anchored Rating Scales): Combines rating scales with specific behavioural examples. More objective than simple scales.\n9. Balanced Scorecard (Kaplan & Norton): Measures performance on 4 dimensions — Financial, Customer, Internal Process, Learning & Growth. Strategic alignment.\n10. OKR (Objectives and Key Results): Used by Google/Intel. Ambitious objectives with measurable key results. Promotes transparency.\n\nIMPORTANCE OF COUNSELLING IN PMS:\nCounselling is a confidential, supportive conversation between a manager/HR and an employee to address performance gaps, understand root causes and create an improvement plan.\n\nTypes: Directive (manager-led), Non-Directive (employee-led), Participative/Eclectic (joint discussion — most effective).\n\nImportance:\n1. Identifies root causes of poor performance — whether it is a skill gap, personal problem, unclear goals or lack of resources.\n2. Creates an improvement plan — specific actions, training and timelines to bring performance up.\n3. Prevents disciplinary action — early counselling resolves issues before they escalate.\n4. Boosts morale — employees who feel supported stay more committed and loyal.\n5. Reduces turnover — counselled employees are less likely to quit due to performance-related frustration.\n6. Documentation — creates a formal record of performance discussions for HR and legal purposes.\n\nIn conclusion, PMS integrates goal-setting, continuous appraisal, diverse evaluation methods and supportive counselling into a holistic system that drives both individual growth and organisational performance."):
    story.append(item)
for item in q_box(10,"Explain Performance Management System and its techniques. How does employee counselling improve employee performance? (10 marks)",
    "Performance Management System (PMS) is the continuous process of aligning individual performance with organisational goals through: goal setting, monitoring, appraisal, feedback and development.\n\nPMS Cycle: Goal Setting (SMART/OKRs) → Continuous Monitoring → Formal Appraisal → Feedback → Reward/Development Plan → New Goals.\n\nKey Appraisal Techniques:\n1. Graphic Rating Scale: Rating employees on traits like quality, initiative on a 1-5 scale. Simple, widely used.\n2. MBO: Manager and employee jointly agree on SMART goals. At year-end, performance is measured against those goals — high employee ownership.\n3. 360-Degree Feedback: Feedback from superiors, peers, subordinates, self and customers. Most comprehensive, reduces bias.\n4. Critical Incident: Manager records specific notable incidents. Objective evidence for the appraisal.\n5. BARS: Behavioural examples anchor each rating point — combines objectivity with specificity.\n\nHOW COUNSELLING IMPROVES PERFORMANCE:\nEmployee counselling is a supportive, confidential dialogue to help employees understand and bridge their performance gaps.\n\n1. Clarifies Expectations: Counselling ensures the employee clearly understands job expectations, KPIs and standards — eliminating confusion as a cause of poor performance.\n2. Identifies Root Causes: Poor performance may stem from skill gaps, personal issues, unclear goals, inadequate tools or management failures. Counselling identifies the real cause.\n3. Motivates Improvement: An employee who feels heard and supported is more willing to change and improve.\n4. Builds Skill Awareness: Counselling identifies specific skills the employee lacks — leading to targeted training interventions.\n5. Builds Trust: Regular counselling creates a culture of open communication and trust between employee and manager.\n6. Prevents Resignation: Many employees leave because they feel unsupported. Good counselling retains talent by making them feel valued.\n\nEffective counselling, especially the Participative (Eclectic) approach, creates a collaborative improvement plan that is more likely to succeed because the employee is an active participant."):
    story.append(item)
story.append(PageBreak())

# ══════════════════════════════════════════════════════
# QUICK REVISION CARD
# ══════════════════════════════════════════════════════
rev_banner = Table([["⚡ QUICK REVISION CARD — MODULE 2: HR SOURCING, JOB ANALYSIS, DESIGN, EVALUATION & PMS"]], colWidths=[W-3.6*cm])
rev_banner.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),DARK_BLUE),('TEXTCOLOR',(0,0),(-1,-1),WHITE),('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),12),('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
story.append(rev_banner)
story.append(Spacer(1,8))

rev_data = [
    ["Topic","Key Points to Remember","Exam %"],
    ["Recruitment","Definition (Flippo) | Internal (promotions, transfers, referrals) vs External (ads, portals, campus, AI tools) | 7-step process | Modern trends: AI, ATS, LinkedIn, employer branding","90%"],
    ["Selection","Negative process — elimination | 8 steps: Screening→Tests→Interview→Reference→Medical→Decision→Offer→Contract | Tests: IQ, aptitude, psychometric, achievement | Interview types: structured, panel, stress, STAR","90%"],
    ["Placement, Induction, Socialization","Placement = job assignment. Induction = welcoming+orientation (company intro, policies, buddy system). Socialization = 3 stages (Pre-arrival, Encounter, Metamorphosis). Importance: faster productivity, lower turnover.","75%"],
    ["Job Analysis","Flippo definition | Output: JD + JS | JD = what job does (duties, conditions) | JS = who does it (qualifications, skills) | Process: 5 steps | Uses: 10 HR functions | Methods: observation, questionnaire, interview, log","85%"],
    ["Job Design","4 techniques: Simplification, Rotation, Enlargement (horizontal), Enrichment (vertical) | 3 approaches: Scientific (Taylor), Behavioural (Herzberg), Socio-Technical | Hackman & Oldham: 5 dimensions→3 states→outcomes","80%"],
    ["Job Evaluation","Systematic worth comparison — assesses JOB not person | 4 methods: Ranking (non-quantitative, simplest), Classification (grading), Factor Comparison (quantitative), Point Method (most accurate, widely used) | 8-step process","80%"],
    ["PMS & Appraisal","PMS = continuous cycle | Traditional: Graphic Rating, Ranking, Forced Distribution, MBO, Critical Incident, Essay | Modern: 360-degree (most comprehensive), BARS, BSC (Kaplan & Norton), OKR | Counselling: 3 types — Directive, Non-Directive, Participative","95%"],
]
rev_t = Table(rev_data, colWidths=[2.5*cm, W-7.5*cm, 1.2*cm])
rev_t.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0),ACCENT_BLUE),('TEXTCOLOR',(0,0),(-1,0),WHITE),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,1),(1,-1),'Helvetica'),
    ('FONTNAME',(2,1),(2,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),8),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,LIGHT_BLUE]),('TEXTCOLOR',(2,1),(2,-1),GREEN_ACC),
    ('ALIGN',(0,0),(-1,-1),'LEFT'),('ALIGN',(2,0),(2,-1),'CENTER'),
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ('LEFTPADDING',(0,0),(-1,-1),5),('VALIGN',(0,0),(-1,-1),'TOP'),
    ('BOX',(0,0),(-1,-1),1.5,ACCENT_BLUE),('INNERGRID',(0,0),(-1,-1),0.3,GREY_LINE),
]))
story.append(rev_t)
story.append(Spacer(1,8))

terms_banner = Table([["📌 KEY TERMS, THEORISTS & MNEMONICS TO REMEMBER"]], colWidths=[W-3.6*cm])
terms_banner.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),ORANGE_ACC),('TEXTCOLOR',(0,0),(-1,-1),WHITE),('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),11),('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
story.append(terms_banner)
story.append(Spacer(1,5))

terms_data = [
    ["Term / Person","What to Remember"],
    ["Edwin Flippo","Recruitment definition | Job Analysis definition | JD definition | JS definition — All Flippo!"],
    ["Peter Drucker","Father of MBO (Management by Objectives) — mutually agreed SMART goals"],
    ["Herzberg","Two-Factor Theory → Job Enrichment → Behavioural Approach to Job Design"],
    ["F.W. Taylor","Scientific Management → Job Simplification → one best method → piece-rate wages"],
    ["Hackman & Oldham","Job Characteristics Model: 5 dimensions (Skill Variety, Task Identity, Task Significance, Autonomy, Feedback)"],
    ["Kaplan & Norton","Balanced Scorecard (BSC) — 4 perspectives: Financial, Customer, Internal Process, Learning & Growth"],
    ["STAR Method","Behavioural Interview: Situation, Task, Action, Result"],
    ["360 Degree Appraisal","Feedback from ALL: Self + Superior + Subordinates + Peers + Customers"],
    ["MBO vs OKR","MBO = realistic, agreed targets | OKR = ambitious stretch goals (Google)"],
    ["JD vs JS","JD = about the JOB (what) | JS = about the PERSON (who). Flippo defines both."],
    ["4 Job Eval Methods","Rank-Class-Factor-Point (RCFP). Point = most accurate. Ranking = simplest."],
    ["Socialization Stages","Pre-Arrival → Encounter (reality shock) → Metamorphosis (adjustment)"],
]
terms_t = Table(terms_data, colWidths=[3.5*cm, W-7.5*cm])
terms_t.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#bf360c')),('TEXTCOLOR',(0,0),(-1,0),WHITE),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,1),(0,-1),'Helvetica-Bold'),
    ('FONTNAME',(1,1),(1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),8.5),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,ORANGE_BG]),('ALIGN',(0,0),(-1,-1),'LEFT'),
    ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ('LEFTPADDING',(0,0),(-1,-1),5),('VALIGN',(0,0),(-1,-1),'TOP'),
    ('BOX',(0,0),(-1,-1),1,colors.HexColor('#bf360c')),('INNERGRID',(0,0),(-1,-1),0.3,GREY_LINE),
]))
story.append(terms_t)
story.append(Spacer(1,8))

footer = Table([["HRM Module 2 Notes | OEC-CS-602(I) | Based on PYQ Analysis: Dec-2024, May-2025, Dec-2025"]], colWidths=[W-3.6*cm])
footer.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),DARK_BLUE),('TEXTCOLOR',(0,0),(-1,-1),colors.HexColor('#c5cae9')),('FONTNAME',(0,0),(-1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),8),('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
story.append(footer)

doc.build(story)
print("Module 2 PDF created successfully!")