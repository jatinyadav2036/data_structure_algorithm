from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, HRFlowable)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

W, H = A4

C = {
    'navy'   : HexColor('#0d1b2a'), 'dark'   : HexColor('#1a237e'),
    'blue'   : HexColor('#283593'), 'med'    : HexColor('#3949ab'),
    'acc'    : HexColor('#e8eaf6'), 'teal'   : HexColor('#004d40'),
    'tl'     : HexColor('#e0f2f1'), 'green'  : HexColor('#1b5e20'),
    'gl'     : HexColor('#e8f5e9'), 'purple' : HexColor('#4a148c'),
    'pl'     : HexColor('#f3e5f5'), 'orange' : HexColor('#e65100'),
    'ol'     : HexColor('#fff3e0'), 'red'    : HexColor('#b71c1c'),
    'rl'     : HexColor('#fce4ec'), 'maroon' : HexColor('#880e4f'),
    'ml'     : HexColor('#fce4ec'), 'brown'  : HexColor('#4e342e'),
    'bl'     : HexColor('#efebe9'), 'yl'     : HexColor('#fffde7'),
    'gy'     : HexColor('#f5f5f5'), 'dk'     : HexColor('#212121'),
    'md'     : HexColor('#424242'), 'cyan'   : HexColor('#006064'),
    'cl'     : HexColor('#e0f7fa'),
}

def mk():
    s = {}
    def p(n, **kw):
        d = dict(fontName='Helvetica', fontSize=10.5, textColor=C['dk'],
                 leading=16, spaceAfter=5, alignment=TA_JUSTIFY)
        d.update(kw); s[n] = ParagraphStyle(n, **d)
    p('ct', fontName='Helvetica-Bold', fontSize=24, textColor=white,
      alignment=TA_CENTER, leading=32, spaceAfter=8)
    p('cs', fontSize=12, textColor=HexColor('#b0bec5'),
      alignment=TA_CENTER, leading=17, spaceAfter=5)
    p('ban', fontName='Helvetica-Bold', fontSize=14, textColor=white,
      alignment=TA_LEFT, leading=19, leftIndent=10)
    p('sec', fontName='Helvetica-Bold', fontSize=12, textColor=C['dark'],
      leading=17, spaceBefore=10, spaceAfter=4)
    p('sub', fontName='Helvetica-Bold', fontSize=11, textColor=C['blue'],
      leading=15, spaceBefore=7, spaceAfter=3)
    p('body', leading=16, spaceAfter=6, alignment=TA_JUSTIFY)
    p('bul',  leading=15, spaceAfter=4, leftIndent=14, alignment=TA_JUSTIFY)
    p('sbul', fontSize=10, textColor=C['md'], leading=14, spaceAfter=3,
      leftIndent=28, alignment=TA_JUSTIFY)
    p('note', fontName='Helvetica-Oblique', fontSize=10, textColor=C['purple'],
      leading=14, spaceAfter=5, leftIndent=8)
    p('form', fontName='Helvetica-Bold', fontSize=11, textColor=C['purple'],
      alignment=TA_CENTER, leading=18, spaceAfter=5, spaceBefore=4)
    p('qm',  fontName='Helvetica-Bold', fontSize=10, textColor=white,
      alignment=TA_LEFT, leading=14, leftIndent=6)
    p('qn',  fontName='Helvetica-Bold', fontSize=10.5, textColor=C['navy'],
      leading=14, spaceAfter=2)
    p('th',  fontName='Helvetica-Bold', fontSize=9.5, textColor=white,
      alignment=TA_CENTER, leading=13)
    p('td',  fontSize=9.5, leading=14, spaceAfter=3, alignment=TA_JUSTIFY)
    p('yr',  fontName='Helvetica-Bold', fontSize=10, textColor=C['maroon'],
      leading=13, spaceAfter=2)
    return s

S = mk()

def ban(t, c): 
    x=Table([[Paragraph(t,S['ban'])]],colWidths=[W-2.8*cm])
    x.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),c),
        ('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9),
        ('LEFTPADDING',(0,0),(-1,-1),14)])); return x

def sbox(t, bg, bd):
    x=Table([[Paragraph(f"◆  {t}",S['sec'])]],colWidths=[W-2.8*cm])
    x.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),bg),
        ('BOX',(0,0),(-1,-1),1.5,bd),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),10)])); return x

def fbox(t, bg=None, bd=None):
    bg=bg or C['pl']; bd=bd or C['purple']
    x=Table([[Paragraph(t,S['form'])]],colWidths=[W-2.8*cm])
    x.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),bg),
        ('BOX',(0,0),(-1,-1),1.5,bd),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)])); return x

def ibox(t, bg=None, bd=None):
    bg=bg or C['ol']; bd=bd or C['orange']
    x=Table([[Paragraph(t,S['body'])]],colWidths=[W-2.8*cm])
    x.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),bg),
        ('BOX',(0,0),(-1,-1),1.2,bd),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12)])); return x

def ctab(rows, widths, hc, rbgs=None):
    built=[]
    for i,row in enumerate(rows):
        sty=S['th'] if i==0 else S['td']
        built.append([Paragraph(str(c),sty) for c in row])
    t=Table(built,colWidths=widths)
    cmds=[('BACKGROUND',(0,0),(-1,0),hc),
          ('GRID',(0,0),(-1,-1),0.5,HexColor('#bdbdbd')),
          ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
          ('LEFTPADDING',(0,0),(-1,-1),7),('VALIGN',(0,0),(-1,-1),'MIDDLE')]
    if rbgs:
        for i,bg in enumerate(rbgs,1):
            if i<len(built): cmds.append(('BACKGROUND',(0,i),(-1,i),bg))
    t.setStyle(TableStyle(cmds)); return t

def year_tag(years):
    return Paragraph(f"📅  Asked in: {years}", S['yr'])

def qa(q_text, marks, years, answer, color, topic_bg=None):
    """Render one Q&A block"""
    items = []
    topic_bg = topic_bg or C['gy']
    # Question header
    qs = ParagraphStyle('qsh', fontName='Helvetica-Bold', fontSize=11,
                        textColor=white, leading=15, spaceAfter=0,
                        spaceBefore=0, leftIndent=8, backColor=color)
    items.append(Spacer(1,0.15*cm))
    qh = Table([[Paragraph(f"Q  [{marks}]  {q_text}", qs)]],
               colWidths=[W-2.8*cm])
    qh.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),color),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',(0,0),(-1,-1),10)]))
    items.append(qh)
    # Year tag
    yt = Table([[Paragraph(f"  📅 Asked in: {years}  |  Word limit: ~{marks}", 
                           ParagraphStyle('yt',fontName='Helvetica-Oblique',fontSize=9,
                           textColor=C['maroon'],leading=12,leftIndent=6))]],
               colWidths=[W-2.8*cm])
    yt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),C['yl']),
        ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
        ('LEFTPADDING',(0,0),(-1,-1),8)]))
    items.append(yt)
    # Answer
    as_ = ParagraphStyle('ans_', fontName='Helvetica', fontSize=10.3,
                         textColor=C['dk'], leading=16, spaceAfter=4,
                         leftIndent=10, alignment=TA_JUSTIFY, backColor=topic_bg)
    items.append(Paragraph("<b>✍ Answer:</b>", ParagraphStyle('ah',
        fontName='Helvetica-Bold',fontSize=10,textColor=C['teal'],
        leading=13,spaceBefore=4,spaceAfter=2,leftIndent=10,backColor=topic_bg)))
    items.append(Paragraph(answer.replace('\n','<br/>'), as_))
    items.append(HRFlowable(width="100%",thickness=0.8,color=HexColor('#e0e0e0'),spaceAfter=3))
    return items

# ════════════════════════════════════════════════════════════════════════════
def build():
    story = []

    # COVER
    cov = Table([
        [Paragraph("INTELLIGENT SYSTEMS", S['ct'])],
        [Paragraph("PCC-CS-601  |  B.Tech 6th Semester  |  YMCA University, Faridabad", S['cs'])],
        [Spacer(1,0.4*cm)],
        [Paragraph("COMPLETE PREVIOUS YEAR QUESTIONS", ParagraphStyle('cm',
            fontName='Helvetica-Bold',fontSize=18,textColor=HexColor('#ffd54f'),
            alignment=TA_CENTER,leading=24))],
        [Paragraph("WITH FULL DETAILED ANSWERS", ParagraphStyle('cm2',
            fontName='Helvetica-Bold',fontSize=16,textColor=HexColor('#ffcc02'),
            alignment=TA_CENTER,leading=22))],
        [Spacer(1,0.3*cm)],
        [Paragraph("2017  •  2018  •  2022  •  2023  •  2024  •  2025", S['cs'])],
        [Spacer(1,0.4*cm)],
        [Paragraph("Word Limits: 1.5M = 100 words  |  5M = 500–800 words  |  10M = 800–1200 words  |  15M = 1200–1500 words",
                   ParagraphStyle('wl',fontName='Helvetica-Oblique',fontSize=10,
                   textColor=HexColor('#90a4ae'),alignment=TA_CENTER,leading=15))],
    ], colWidths=[W-2*cm])
    cov.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),C['navy']),
        ('TOPPADDING',(0,0),(-1,-1),18),('BOTTOMPADDING',(0,0),(-1,-1),18),
        ('BOX',(0,0),(-1,-1),3,HexColor('#546e7a'))]))
    story += [Spacer(1,1*cm), cov, Spacer(1,0.6*cm)]

    # INDEX TABLE
    story.append(Paragraph("📚  SECTION INDEX", S['sec']))
    idx = ctab([
        ["#","SECTION / TOPIC","YEARS COVERED","MARKS TYPES"],
        ["1","Introduction to AI & Intelligent Systems","2017,2018,2022,2023","1.5M, 5M, 10M"],
        ["2","Artificial Neural Networks (ANN)","2017,2018,2022,2023,2024,2025","1.5M, 5M, 10M"],
        ["3","Backpropagation Networks","2022,2023,2024,2025","1.5M, 10M"],
        ["4","RBF & Recurrent Networks","2022,2023,2024,2025","1.5M, 5M, 10M"],
        ["5","Fuzzy Logic & Fuzzy Neural Networks","2018,2022,2023,2024,2025","1.5M, 5M, 7M, 10M"],
        ["6","Search Methods: BFS, DFS, IDDFS","2017,2018,2022,2023,2024,2025","1.5M, 5M, 10M, 15M"],
        ["7","Heuristic Search: A*, AO*, Hill Climbing","2017,2018,2022,2023,2024,2025","1.5M, 5M, 10M"],
        ["8","Knowledge Representation (Semantic Nets, Frames, Logic)","2017,2018,2022,2023,2024,2025","1.5M, 5M, 10M, 15M"],
        ["9","Expert Systems & Knowledge-Based Systems","2017,2018,2022,2023,2024,2025","5M, 10M, 15M"],
        ["10","Genetic Algorithms","2017,2018,2022,2023,2024,2025","1.5M, 5M, 8M, 10M"],
        ["11","Uncertainty: Bayesian, CF, Dempster-Shafer","2017,2018,2022,2023,2024,2025","1.5M, 5M, 10M, 15M"],
        ["12","Learning: Statistical, Induction, Evolutionary","2017,2022,2023,2024,2025","1.5M, 5M, 10M"],
        ["13","Logic & Inference (Resolution, Tableaux, FOPL)","2018,2022,2023,2025","1.5M, 5M, 10M"],
        ["14","Miscellaneous (NLP, Planning, Turing Test, Reasoning)","2017,2018,2022,2023","1.5M, 5M, 10M"],
    ],[1*cm,7*cm,4.5*cm,W-2.8*cm-12.5*cm], C['navy'],
    [C['acc'],C['gl'],C['ol'],C['pl'],C['yl'],C['rl'],C['tl'],C['bl'],
     C['acc'],C['gl'],C['ol'],C['pl'],C['yl'],C['rl']])
    story += [idx, PageBreak()]

    # ════════════════════ SECTION 1: INTRODUCTION TO AI ═════════════════════
    story.append(ban("SECTION 1 — INTRODUCTION TO AI & INTELLIGENT SYSTEMS", C['dark']))
    story.append(Spacer(1,0.2*cm))
    story.append(ibox("This section covers: What is AI, components of AI, Turing test, task domains, "
                      "strong AI, AI problem issues. These appear as 1.5M Part-A questions almost every year.",
                      C['acc'],C['dark']))
    story.append(Spacer(1,0.2*cm))

    for q,marks,years,ans,c,bg in [
        ("What is Artificial Intelligence? List all its components.",
         "1.5 Marks — 100 words", "2017,2018",
         "Artificial Intelligence (AI) is a branch of computer science that aims to create machines capable of performing tasks that require human intelligence — reasoning, learning, problem-solving, understanding language, and perceiving the environment.\n\n"
         "Components of AI:\n"
         "1. Reasoning: Drawing conclusions from facts (deductive/inductive).\n"
         "2. Knowledge Representation: Storing world knowledge in structures computers can process.\n"
         "3. Planning: Generating sequences of actions to achieve goals.\n"
         "4. Learning: Improving performance from experience (supervised, unsupervised, reinforcement).\n"
         "5. Natural Language Processing (NLP): Understanding and generating human language.\n"
         "6. Perception: Interpreting sensory input — vision, speech, touch.\n"
         "7. Problem Solving & Search: Finding solutions through state-space exploration.\n"
         "8. Robotics: Physical agents that sense and act in the real world.\n"
         "Together these components enable machines to exhibit intelligent behavior.", C['dark'], C['acc']),

        ("What is an Intelligent System? (Asked 2022)",
         "1.5 Marks — 100 words", "2022",
         "An Intelligent System is a computing system that exhibits intelligence — the ability to learn from experience, reason about knowledge, adapt to new situations, and solve complex problems autonomously or semi-autonomously.\n\n"
         "Key properties of intelligent systems: (1) Perception — can sense the environment; (2) Reasoning — can draw logical conclusions; (3) Learning — improves with experience; (4) Problem Solving — finds solutions to complex problems; (5) Communication — interacts in natural language.\n\n"
         "Examples: Chess-playing programs (Deep Blue), medical diagnostic systems (MYCIN), virtual assistants (Siri, Alexa), self-driving cars, recommendation engines (Netflix, Amazon).\n\n"
         "Applications: Medical diagnosis, financial forecasting, robotics, image recognition, fraud detection.", C['dark'], C['acc']),

        ("What are the Task Domains of AI? (Asked 2018, 2023)",
         "1.5 Marks — 100 words", "2018, 2023",
         "Task domains of AI define the areas/categories of problems AI systems are designed to solve:\n\n"
         "1. Formal Tasks: Mathematics (theorem proving, geometry), games (chess, Go), logic (resolution, verification).\n"
         "2. Mundane Tasks (Human Expert Tasks): Perception (vision, speech), natural language (understanding, generation, translation), common sense reasoning.\n"
         "3. Expert Tasks: Engineering design, scientific discovery, medical diagnosis, financial analysis, fault diagnosis.\n"
         "4. Cognitive Tasks: Learning, planning, scheduling, autonomous systems.\n"
         "5. Physical Tasks: Robot motion planning, object manipulation, navigation.\n\n"
         "The breadth of these domains shows why AI is fundamental to modern technology.", C['dark'], C['acc']),

        ("Explain Turing Test in AI. (Asked 2018, 2023)",
         "1.5 Marks — 100 words", "2018, 2023",
         "The Turing Test was proposed by Alan Turing in 1950 as a measure of machine intelligence. In the test, a human evaluator conducts text-based conversations with both a human and a machine (without knowing which is which). If the evaluator cannot reliably distinguish the machine from the human, the machine is considered to have demonstrated human-level intelligence.\n\n"
         "The test evaluates: Natural language understanding, reasoning, knowledge, and appropriate social response.\n\n"
         "Limitations: The test only measures conversational ability, not general intelligence. A machine can pass it by clever deception without truly understanding. Critics argue genuine intelligence requires consciousness and understanding, not just output imitation.", C['dark'], C['acc']),

        ("Define Strong Artificial Intelligence. (Asked 2023)",
         "1.5 Marks — 100 words", "2023",
         "Strong AI (or Artificial General Intelligence — AGI) refers to a hypothetical AI system that possesses the full range of human cognitive abilities — the ability to reason, plan, solve problems, think abstractly, comprehend complex ideas, learn quickly, and learn from experience across any domain.\n\n"
         "Strong AI vs Weak AI:\n"
         "Weak AI: Designed for specific narrow tasks (e.g., playing chess, facial recognition). Has no general intelligence beyond its programmed domain.\n"
         "Strong AI: Can perform ANY intellectual task that a human can. Has self-awareness, consciousness, and general reasoning.\n\n"
         "Current state: No Strong AI exists yet. All current AI (GPT, AlphaGo, etc.) is Weak AI.", C['dark'], C['acc']),

        ("What are the basic issues/problems in solving an AI problem? (Asked 2017)",
         "1.5 Marks — 100 words", "2017",
         "Key issues in solving AI problems:\n\n"
         "1. Representation Problem: How to represent knowledge, states, and goals formally so computers can process them efficiently.\n"
         "2. Search Problem: The solution space is often enormous — exhaustive search is computationally infeasible. Need smart search strategies.\n"
         "3. Combinatorial Explosion: As problem size grows, the number of possibilities grows exponentially, making brute force impossible.\n"
         "4. Frame Problem: When actions occur, efficiently representing what does NOT change is surprisingly difficult.\n"
         "5. Uncertainty: Real-world data is incomplete, noisy, and ambiguous.\n"
         "6. Learning: Systems need to generalize from limited training examples.\n"
         "7. Real-time Constraints: Many AI tasks require decisions within milliseconds.", C['dark'], C['acc']),

        ("What is reasoning in AI? What are its types? (Asked 2022, 2023)",
         "1.5 Marks — 100 words", "2022, 2023",
         "Reasoning in AI is the process of drawing conclusions, making inferences, or solving problems from known facts and rules. It is fundamental to intelligence.\n\n"
         "Types of Reasoning:\n"
         "1. Deductive Reasoning: From general rules to specific conclusions. Logically guaranteed. Example: All men are mortal + Socrates is a man → Socrates is mortal.\n"
         "2. Inductive Reasoning: From specific observations to general rules. Not guaranteed. Example: All observed swans are white → All swans are white.\n"
         "3. Abductive Reasoning: Best explanation for observations. Example: Wet ground → It rained.\n"
         "4. Common-Sense Reasoning: Using everyday knowledge.\n"
         "5. Non-Monotonic Reasoning: Conclusions can be retracted with new information.", C['dark'], C['acc']),
    ]:
        for item in qa(q, marks, years, ans, c, bg): story.append(item)

    story.append(PageBreak())

    # ════════════════════ SECTION 2: ANN ════════════════════════════════════
    story.append(ban("SECTION 2 — ARTIFICIAL NEURAL NETWORKS (ANN)", C['teal']))
    story.append(Spacer(1,0.2*cm))
    story.append(ibox("Core topic — appears every year. Know: biological neuron comparison, architecture, "
                      "activation functions, types of ANN, learning rules, applications.",
                      C['tl'], C['teal']))
    story.append(Spacer(1,0.2*cm))

    for q,marks,years,ans,c,bg in [
        ("What are the applications of Artificial Neural Networks? (Asked 2022, 2023, 2024)",
         "1.5 Marks — 100 words", "2022, 2023, 2024",
         "Applications of ANN:\n"
         "1. Image Recognition: Face detection, handwriting recognition, medical image analysis (X-rays, MRI).\n"
         "2. Speech Recognition: Siri, Alexa, Google Assistant converting speech to text.\n"
         "3. Natural Language Processing: Language translation, sentiment analysis, chatbots.\n"
         "4. Medical Diagnosis: Detecting cancer, predicting heart disease from patient data.\n"
         "5. Financial Systems: Stock market prediction, credit scoring, fraud detection.\n"
         "6. Autonomous Vehicles: Object detection, path planning, real-time decision making.\n"
         "7. Game Playing: AlphaGo, chess engines, video game AI.\n"
         "8. Recommendation Systems: Netflix, Amazon suggesting content/products.\n"
         "9. Industrial Control: Quality inspection on production lines.\n"
         "10. Weather Forecasting: Predicting rainfall, temperature patterns.", C['teal'], C['tl']),

        ("What is a Perceptron? What are its limitations? (Asked 2024)",
         "1.5 Marks — 100 words", "2024",
         "A Perceptron is the simplest form of artificial neural network, consisting of a single layer with input nodes and one output node. Proposed by Frank Rosenblatt (1957), it computes a weighted sum of inputs, adds a bias, and applies a step activation function: output = 1 if (Σwixi + b) ≥ threshold, else 0.\n\n"
         "The Perceptron Learning Rule adjusts weights: Δwi = η × (target − output) × xi.\n\n"
         "Limitations:\n"
         "1. Can only solve LINEARLY SEPARABLE problems (AND, OR gates work; XOR does NOT).\n"
         "2. Cannot represent complex non-linear decision boundaries.\n"
         "3. Minsky and Papert (1969) proved XOR impossibility — this limitation nearly killed ANN research for a decade.", C['teal'], C['tl']),

        ("What is Neural Network? How is ANN derived from Natural Biological Neuron? (Asked 2018, 2022, 2023)",
         "10 Marks — 800–1200 words", "2018, 2022, 2023",
         "INTRODUCTION:\n"
         "An Artificial Neural Network (ANN) is a computational model inspired by the structure and functioning of biological neural networks in the human brain. The brain contains approximately 100 billion neurons, each connected to thousands of others, processing information in a massively parallel fashion. ANNs replicate this architecture using mathematical models.\n\n"
         "PART A: BIOLOGICAL NEURON STRUCTURE\n"
         "The human brain's basic processing unit is the biological neuron. Its components:\n\n"
         "1. Dendrites: Tree-like branches that RECEIVE electrochemical signals from other neurons. Multiple dendrites allow a single neuron to receive thousands of inputs simultaneously.\n"
         "2. Cell Body (Soma): The main body of the neuron. It INTEGRATES all incoming signals — summing excitatory (+) and inhibitory (−) signals. If the total exceeds a threshold, the neuron fires.\n"
         "3. Axon: A long cable that TRANSMITS the output signal (action potential) to other neurons. The axon can be several feet long.\n"
         "4. Synapses: The junction between neurons. The STRENGTH of a synapse determines how much signal passes through. Strong synapse = strong signal. This synaptic strength is modified by learning — more signal use → stronger synapse (Hebbian learning: 'neurons that fire together, wire together').\n"
         "5. Myelin Sheath: Insulating cover around the axon that speeds signal transmission.\n\n"
         "PART B: THE ARTIFICIAL NEURON (PERCEPTRON MODEL)\n"
         "Each component of the biological neuron has a direct artificial counterpart:\n\n"
         "Dendrites → Input values (x1, x2, ..., xn). Each input represents a signal from another neuron.\n"
         "Synapse strength → Weights (w1, w2, ..., wn). Higher weight = stronger influence.\n"
         "Cell body integration → Weighted summation: net = Σ(wi × xi) + bias b.\n"
         "Firing threshold → Activation function f(net). The neuron 'fires' if net exceeds threshold.\n"
         "Axon output → Output value y = f(net) transmitted to next neurons.\n\n"
         "Mathematical model of one artificial neuron:\n"
         "net = w1·x1 + w2·x2 + ... + wn·xn + b = Σ(wi·xi) + b\n"
         "y = f(net)   where f is the activation function\n\n"
         "PART C: ACTIVATION FUNCTIONS\n"
         "Different activation functions model different firing behaviors:\n\n"
         "1. Step Function: f(x) = 1 if x ≥ 0, else 0. Binary fire/no-fire. Used in early perceptron.\n"
         "2. Sigmoid: f(x) = 1/(1+e^(-x)). Smooth S-curve. Output 0 to 1. Differentiable — used in backprop.\n"
         "3. Tanh: f(x) = (e^x − e^(−x))/(e^x + e^(−x)). Output −1 to 1. Zero-centered.\n"
         "4. ReLU: f(x) = max(0,x). Most popular today. Fast, no vanishing gradient for positive values.\n"
         "5. Softmax: Converts outputs to probability distribution summing to 1. Used in output layer for classification.\n\n"
         "PART D: ANN ARCHITECTURE\n"
         "ANN is organized into layers:\n\n"
         "1. Input Layer: Receives raw data (features). No computation — just distribution. Number of neurons = number of features.\n"
         "2. Hidden Layer(s): The processing powerhouse. One or more layers where weighted sums and activations are computed. More hidden layers → deeper network → can learn more complex patterns. This is the foundation of Deep Learning.\n"
         "3. Output Layer: Produces the final result. One neuron for binary classification, n neurons for n-class problems.\n\n"
         "Information flows FORWARD through layers (feedforward network). Each layer extracts increasingly abstract features — early layers detect edges, middle layers detect shapes, deep layers detect objects (in image recognition).\n\n"
         "PART E: TYPES OF ANN\n"
         "1. Feedforward Neural Network: Information flows in one direction only. Used for classification and regression.\n"
         "2. Recurrent Neural Network (RNN): Has feedback connections — output feeds back as input. Has memory. Used for sequential data (text, speech, time series).\n"
         "3. Convolutional Neural Network (CNN): Uses convolution operations for spatial feature extraction. Dominant in image processing.\n"
         "4. Radial Basis Function Network (RBFNN): Uses Gaussian activation in hidden layer. Fast training.\n\n"
         "PART F: LEARNING IN ANN\n"
         "Learning = adjusting weights and biases to minimize error.\n"
         "1. Supervised Learning: Learn from labeled input-output pairs. Error = (target − output). Adjust weights to minimize error.\n"
         "2. Unsupervised Learning: Discover patterns without labels (clustering).\n"
         "3. Reinforcement Learning: Learn from rewards and penalties through trial and error.\n\n"
         "Hebbian Learning Rule (biologically inspired): Δwij = η × xi × yj. If pre- and post-synaptic neurons fire together, strengthen the weight.\n"
         "Delta Rule: Δwi = η × (target − output) × xi. Minimizes squared error.\n\n"
         "PART G: APPLICATIONS\n"
         "Image recognition, speech recognition, NLP, medical diagnosis, financial prediction, autonomous vehicles, game playing, weather forecasting, drug discovery.\n\n"
         "CONCLUSION:\n"
         "ANN is a powerful computational paradigm directly inspired by the brain's parallel, distributed architecture. By mimicking how biological neurons process and learn from information, ANNs have revolutionized AI — achieving superhuman performance in image recognition, game playing, and natural language processing. The key insight: just as the brain learns by strengthening synapses used frequently, ANN learns by adjusting weights to reduce prediction error.", C['teal'], C['tl']),

        ("Differentiate between ANN and Biological Neural Network (BNN). (Asked 2022, 2025)",
         "5 Marks — 500–800 words", "2022, 2025",
         "ANN VS BIOLOGICAL NEURAL NETWORK (BNN) — DETAILED COMPARISON\n\n"
         "INTRODUCTION:\n"
         "Artificial Neural Networks are inspired by biological neural networks but differ in many fundamental ways — in scale, in mechanism, in energy efficiency, and in the types of problems they solve.\n\n"
         "STRUCTURAL COMPARISON:\n\n"
         "1. SCALE AND COMPLEXITY:\n"
         "BNN: The human brain contains approximately 100 BILLION neurons, each forming up to 10,000 synaptic connections — giving roughly 100 trillion connections total.\n"
         "ANN: Modern large ANNs (like GPT-3) have ~175 billion parameters. While large in absolute terms, they are still orders of magnitude simpler than the brain.\n\n"
         "2. SIGNAL TYPE:\n"
         "BNN: Uses ELECTROCHEMICAL signals — action potentials that are binary (fire/no-fire) but with variable timing and frequency.\n"
         "ANN: Uses continuous-valued NUMERICAL signals. Activation values are real numbers (e.g., 0.7, -0.3).\n\n"
         "3. NEURON STRUCTURE:\n"
         "BNN: Complex biological cell with soma, dendrites, axon, myelin sheath, and thousands of synapses of different types.\n"
         "ANN: Simplified mathematical node computing weighted sum + activation function.\n\n"
         "4. LEARNING MECHANISM:\n"
         "BNN: Synaptic plasticity — Long-Term Potentiation (LTP) and Long-Term Depression (LTD) modify synapse strength based on firing patterns. Governed by many neurochemicals.\n"
         "ANN: Backpropagation — computes gradient of error and adjusts weights numerically using gradient descent. Mathematical, not biochemical.\n\n"
         "5. PARALLELISM:\n"
         "BNN: True massively parallel processing — billions of neurons fire simultaneously in real time.\n"
         "ANN: Simulated parallelism on CPUs/GPUs. While GPUs enable some parallelism, it is far less than biological brains.\n\n"
         "6. ENERGY EFFICIENCY:\n"
         "BNN: The human brain runs on only about 20 WATTS — extraordinarily efficient.\n"
         "ANN: Training large ANNs requires thousands of watts (GPU farms), consuming massive amounts of electricity.\n\n"
         "7. FAULT TOLERANCE:\n"
         "BNN: Highly fault-tolerant — losing thousands of neurons causes no noticeable effect because knowledge is distributed.\n"
         "ANN: Also has distributed representation, so it has some fault tolerance, but not as robust as the brain.\n\n"
         "8. SPEED:\n"
         "BNN: Individual neurons fire at 100-200 Hz (signals per second) — slower than transistors.\n"
         "ANN: Operations run at GHz speeds on silicon.\n\n"
         "9. LEARNING SPEED:\n"
         "BNN: Humans learn new concepts from very few examples (one-shot learning).\n"
         "ANN: Requires millions of training examples for comparable performance.\n\n"
         "10. CAPABILITIES:\n"
         "BNN: General intelligence — creativity, consciousness, emotion, sensorimotor integration, common sense.\n"
         "ANN: Narrow intelligence — excels at specific tasks but cannot generalize across domains.\n\n"
         "TABULAR SUMMARY:\n"
         "Neurons: BNN=100 billion | ANN=thousands to millions.\n"
         "Connections: BNN=100 trillion | ANN=millions to billions.\n"
         "Signal: BNN=electrochemical spikes | ANN=real-valued numbers.\n"
         "Learning: BNN=synaptic plasticity | ANN=backpropagation/gradient descent.\n"
         "Energy: BNN=~20W | ANN=thousands of watts.\n"
         "Speed: BNN=100-200Hz | ANN=GHz.\n"
         "Fault tolerance: BNN=very high | ANN=moderate.\n"
         "General intelligence: BNN=yes | ANN=no (narrow).\n\n"
         "CONCLUSION:\n"
         "Despite being inspired by the brain, ANN is a vast simplification. Biological neural networks operate on entirely different principles — biochemical, adaptive, and conscious. ANNs excel at pattern recognition within narrow domains but still lack the flexibility, energy efficiency, and generality of biological intelligence. The quest to close this gap drives research in neuromorphic computing, spiking neural networks, and Artificial General Intelligence.", C['teal'], C['tl']),
    ]:
        for item in qa(q, marks, years, ans, c, bg): story.append(item)

    story.append(PageBreak())

    # ════════════════════ SECTION 3: BACKPROPAGATION ══════════════════════
    story.append(ban("SECTION 3 — BACKPROPAGATION NETWORKS", C['dark']))
    story.append(Spacer(1,0.2*cm))

    for q,marks,years,ans,c,bg in [
        ("Why is a backpropagation network required? Discuss its need. (Asked 2025)",
         "1.5 Marks — 100 words", "2025",
         "A Backpropagation network is required because single-layer perceptrons can only solve linearly separable problems (XOR problem is unsolvable). Multi-layer networks can solve complex non-linear problems, but we need an efficient method to train them — to compute how each weight in every layer contributed to the error.\n\n"
         "Backpropagation provides this by propagating the error signal BACKWARDS from output to input through the chain rule of calculus. It computes the gradient of the error with respect to each weight and adjusts them using gradient descent.\n\n"
         "Without backpropagation, training deep neural networks would be computationally impossible. It enabled the modern deep learning revolution.", C['dark'], C['acc']),

        ("Explain the Backpropagation Network in detail. Discuss advantages and disadvantages. (Asked 2022, 2024)",
         "10 Marks — 800–1200 words", "2022, 2024",
         "BACKPROPAGATION NETWORK — COMPLETE ANSWER\n\n"
         "INTRODUCTION:\n"
         "Backpropagation (Backward Propagation of Errors) is the most widely used algorithm for training multi-layer feedforward neural networks. Popularized by Rumelhart, Hinton, and Williams (1986), it revolutionized AI by making deep networks trainable. The algorithm uses the chain rule of calculus to compute gradients of the loss function with respect to every weight in the network, then applies gradient descent to minimize the loss.\n\n"
         "THE MATHEMATICAL FOUNDATION:\n\n"
         "1. Error / Loss Function:\n"
         "For each training example, we compute how wrong the network's output is:\n"
         "E = (1/2) × Σ (target_k − output_k)²\n"
         "The factor 1/2 is added for mathematical convenience (cancels with derivative's 2).\n\n"
         "2. Gradient Descent:\n"
         "We want to minimize E. Gradient descent moves weights in the direction of steepest error decrease:\n"
         "Δw = −η × (∂E/∂w)   →   w_new = w_old + Δw\n"
         "η (learning rate) controls step size. Typical values: 0.001 to 0.1.\n\n"
         "3. Chain Rule:\n"
         "For a weight in a hidden layer, the error depends on the output through multiple intermediate computations. The chain rule multiplies derivatives across each step:\n"
         "∂E/∂w = (∂E/∂output) × (∂output/∂net) × (∂net/∂w)\n\n"
         "THE COMPLETE ALGORITHM — STEP BY STEP:\n\n"
         "PHASE 0 — INITIALIZATION:\n"
         "Initialize all weights wij and biases bi to small random values (e.g., uniform(-0.5, 0.5)). Set learning rate η, momentum α (optional), max epochs.\n\n"
         "PHASE 1 — FORWARD PASS:\n"
         "For each training example (x, t):\n"
         "a) Feed input x through the network layer by layer.\n"
         "b) For each neuron j in each layer: net_j = Σ(wij × yi) + bj\n"
         "c) Apply activation function: yj = f(net_j)\n"
         "d) Record actual output y at the output layer.\n\n"
         "PHASE 2 — COMPUTE OUTPUT ERROR:\n"
         "For each output neuron k:\n"
         "δk (output) = (tk − yk) × f'(net_k)\n"
         "where f'(net_k) is the derivative of the activation function at net_k.\n"
         "For sigmoid: f'(x) = f(x) × (1 − f(x)) = yk × (1 − yk)\n\n"
         "PHASE 3 — BACKWARD PASS (Error Propagation through Hidden Layers):\n"
         "For each hidden neuron j (working backwards from output to input):\n"
         "δj (hidden) = f'(net_j) × Σ(δk × wjk)   for all k in next layer\n"
         "This distributes the error back to each neuron proportional to its weight contribution.\n\n"
         "PHASE 4 — WEIGHT UPDATE:\n"
         "Update all weights using accumulated deltas:\n"
         "Δwij = η × δj × yi\n"
         "wij(new) = wij(old) + Δwij\n"
         "Update biases: Δbj = η × δj\n\n"
         "With Momentum (improvement for speed and stability):\n"
         "Δwij(t) = η × δj × yi + α × Δwij(t−1)\n"
         "Momentum prevents oscillation and helps escape shallow local minima.\n\n"
         "PHASE 5 — REPEAT:\n"
         "Iterate over all training examples (one epoch). Repeat for many epochs until:\n"
         "a) Error falls below acceptable threshold, OR\n"
         "b) Maximum epochs reached, OR\n"
         "c) Error stops decreasing (early stopping).\n\n"
         "VARIANTS OF GRADIENT DESCENT:\n"
         "1. Batch Gradient Descent: Update weights after seeing ALL training examples. Stable but slow.\n"
         "2. Stochastic Gradient Descent (SGD): Update after EACH example. Fast but noisy.\n"
         "3. Mini-Batch: Update after small batches (32–256 examples). Best balance of speed and stability.\n\n"
         "ADVANTAGES OF BACKPROPAGATION:\n"
         "1. Can train networks of arbitrary depth — overcame limitation of single-layer networks.\n"
         "2. Mathematically rigorous — grounded in calculus and gradient descent.\n"
         "3. General purpose — works for classification, regression, and function approximation.\n"
         "4. Scales well with parallel hardware (GPUs).\n"
         "5. The foundation of all modern deep learning (CNN, RNN, Transformers).\n"
         "6. Widely implemented in frameworks (TensorFlow, PyTorch, Keras).\n\n"
         "DISADVANTAGES OF BACKPROPAGATION:\n"
         "1. Vanishing Gradient Problem: As error propagates backwards through many layers, gradients shrink exponentially. Early layers receive almost zero gradient signal — they barely learn. Caused by sigmoid/tanh activations whose derivatives are always less than 1. Solution: ReLU activation, batch normalization, residual connections (ResNets).\n"
         "2. Exploding Gradient Problem: In very deep networks or RNNs, gradients can grow exponentially. Solution: Gradient clipping.\n"
         "3. Local Minima: Gradient descent may converge to a local minimum, not the global optimum.\n"
         "4. Requires Large Training Data: With insufficient data, the network overfits.\n"
         "5. Slow Convergence: May require millions of iterations for complex problems.\n"
         "6. Learning Rate Sensitivity: Too large η → oscillation and divergence. Too small → impractically slow.\n"
         "7. Black Box: Difficult to interpret what the network has learned.\n"
         "8. Computationally Expensive: Training deep networks requires GPU clusters and significant time.\n\n"
         "CONCLUSION:\n"
         "Backpropagation remains the cornerstone algorithm of modern AI. Despite its limitations (vanishing gradient, local minima), innovations like ReLU, Adam optimizer, batch normalization, and residual connections have largely addressed these issues. It enabled the deep learning revolution that transformed computer vision, NLP, and virtually every domain of AI. Understanding backpropagation is essential for any AI practitioner.", C['dark'], C['acc']),
    ]:
        for item in qa(q, marks, years, ans, c, bg): story.append(item)

    story.append(PageBreak())

    # ════════════════════ SECTION 4: RBF & RNN ═══════════════════════════
    story.append(ban("SECTION 4 — RBF NETWORKS & RECURRENT NEURAL NETWORKS", C['purple']))
    story.append(Spacer(1,0.2*cm))

    for q,marks,years,ans,c,bg in [
        ("What is a Recurrent Network? (Asked 2022, 2024, 2025)",
         "1.5 Marks — 100 words", "2022, 2024, 2025",
         "A Recurrent Neural Network (RNN) is a neural network with FEEDBACK connections — the output of neurons at time t feeds back as input at time t+1. This gives RNN a MEMORY of past inputs through its hidden state h(t).\n\n"
         "Key equations: h(t) = f(Wx·x(t) + Wh·h(t-1) + b)   [hidden state update]\n"
         "y(t) = g(Wy·h(t) + by)   [output]\n\n"
         "Unlike feedforward networks (fixed input size, no memory), RNNs handle variable-length sequences. Applications: NLP, speech recognition, time-series prediction, machine translation.\n\n"
         "Problem: Vanishing gradient during training. Solution: LSTM and GRU architectures with gating mechanisms.", C['purple'], C['pl']),

        ("What is RBFNN? How is it different from Multilayer Feed-Forward NN? (Asked 2023)",
         "5 Marks — 500–800 words", "2023",
         "RADIAL BASIS FUNCTION NEURAL NETWORK (RBFNN)\n\n"
         "INTRODUCTION:\n"
         "A Radial Basis Function Neural Network is a three-layer feedforward network that uses radial basis functions (typically Gaussian) as activation functions in its hidden layer. Unlike standard ANNs which use global activation functions (sigmoid affecting the whole space), RBF neurons respond locally — strongly to inputs near their center, weakly to distant inputs.\n\n"
         "ARCHITECTURE — THREE LAYERS:\n\n"
         "1. Input Layer: Receives input features. No computation. Passes data directly to hidden layer.\n\n"
         "2. Hidden Layer (RBF Layer): Each neuron has a CENTER (μ) and WIDTH (σ). Applies Gaussian function:\n"
         "φ(x) = exp(−||x − μ||² / (2σ²))\n"
         "The neuron outputs 1.0 when input exactly equals center, decreasing smoothly as distance increases.\n"
         "Number of hidden neurons = number of cluster centers.\n\n"
         "3. Output Layer: Simple LINEAR combination of hidden layer outputs:\n"
         "y(x) = Σ wk × φk(x) + bias\n"
         "Weights here are learned by least squares — no backpropagation needed!\n\n"
         "TWO-PHASE TRAINING:\n\n"
         "Phase 1 — Unsupervised (find centers and widths):\n"
         "Use K-means clustering on training data to find K cluster centers μk.\n"
         "Set width: σk = d_max / √(2K) where d_max = max distance between centers.\n\n"
         "Phase 2 — Supervised (find output weights):\n"
         "Compute φ matrix (RBF activations for all training points).\n"
         "Solve: w = (ΦᵀΦ)⁻¹ Φᵀ t   [pseudo-inverse / least squares]\n"
         "This is a direct algebraic solution — guaranteed to find the optimal output weights!\n\n"
         "HOW RBFNN DIFFERS FROM MLP (MULTILAYER FEEDFORWARD NN):\n\n"
         "1. Activation Function:\n"
         "RBFNN: Gaussian (radial basis) — LOCAL response around center.\n"
         "MLP: Sigmoid/ReLU/Tanh — GLOBAL response across all inputs.\n\n"
         "2. Training Method:\n"
         "RBFNN: Two-phase: unsupervised (K-means) + linear algebra (least squares).\n"
         "MLP: Iterative backpropagation through all layers.\n\n"
         "3. Training Speed:\n"
         "RBFNN: Much FASTER — Phase 2 solved in one algebraic step.\n"
         "MLP: Slow — requires many epochs of gradient descent.\n\n"
         "4. Convergence:\n"
         "RBFNN: Guaranteed — linear output layer has unique solution.\n"
         "MLP: Not guaranteed — may converge to local minima.\n\n"
         "5. Interpolation:\n"
         "RBFNN: Exact interpolation possible — passes through all training points.\n"
         "MLP: Approximate — learns a smooth generalization.\n\n"
         "6. Network Size:\n"
         "RBFNN: Usually needs more hidden neurons for complex problems.\n"
         "MLP: Can be more compact with fewer hidden neurons.\n\n"
         "7. Best Applications:\n"
         "RBFNN: Function approximation, time-series prediction, control systems, pattern classification with well-defined clusters.\n"
         "MLP: Complex classification, image recognition, speech processing.\n\n"
         "ADVANTAGES OF RBFNN:\n"
         "Fast training, guaranteed convergence, good for function approximation, interpretable neurons.\n\n"
         "DISADVANTAGES:\n"
         "Curse of dimensionality with high-dimensional inputs, choosing number of centers K is non-trivial, may need many neurons for complex problems.\n\n"
         "CONCLUSION:\n"
         "RBFNN offers a compelling alternative to MLP when fast training and guaranteed convergence are priorities. Its local response nature makes it particularly effective for interpolation and function approximation tasks where the data naturally clusters.", C['purple'], C['pl']),

        ("Why is RNN preferred in AI? How many layers? Disadvantages? (Asked 2025 — 10M)",
         "10 Marks — 800–1200 words", "2025",
         "RECURRENT NEURAL NETWORKS — COMPLETE ANSWER\n\n"
         "INTRODUCTION:\n"
         "A Recurrent Neural Network (RNN) is a specialized neural network designed for SEQUENTIAL data — data where the order matters and each element depends on previous elements. Unlike feedforward networks that treat each input independently, RNNs maintain a HIDDEN STATE — a memory vector that carries information from previous time steps.\n\n"
         "Hidden state equation: h(t) = f(Wx·x(t) + Wh·h(t−1) + b)\n"
         "Output equation: y(t) = g(Wy·h(t) + by)\n\n"
         "WHY RNN IS PREFERRED IN AI:\n\n"
         "1. HANDLES SEQUENTIAL DATA NATURALLY:\n"
         "Real-world data is often sequential — text, speech, music, time series, video. Feedforward networks require fixed-size inputs and ignore temporal order. RNNs process sequences of any length while maintaining context.\n\n"
         "2. MEMORY OF PAST INFORMATION:\n"
         "The hidden state h(t) carries information from ALL previous time steps. This allows RNN to understand context — 'The bank by the river' vs 'The bank approved the loan' — the word 'bank' has different meaning depending on context that came before.\n\n"
         "3. WEIGHT SHARING ACROSS TIME:\n"
         "The SAME weight matrices (Wx, Wh, Wy) are used at every time step. This dramatically reduces the number of parameters compared to having separate parameters for each position. It also allows generalization across different sequence lengths.\n\n"
         "4. VARIABLE-LENGTH INPUT AND OUTPUT:\n"
         "Unlike feedforward networks (fixed input → fixed output), RNNs support:\n"
         "One-to-many: Image → caption (image captioning)\n"
         "Many-to-one: Review text → sentiment (sentiment analysis)\n"
         "Many-to-many: English → French (machine translation)\n"
         "Many-to-many (sync): Video → frame labels (video classification)\n\n"
         "5. REAL-TIME STREAMING:\n"
         "RNNs can process streaming data — they update their hidden state as each new input arrives, making them ideal for real-time systems.\n\n"
         "LAYERS IN AN RNN:\n\n"
         "Theoretically, an RNN can have ANY number of recurrent layers. In practice:\n"
         "1. Single Layer RNN: One recurrent layer. Processes input and maintains hidden state. Used for simple sequential tasks.\n"
         "2. Stacked/Deep RNN: Multiple recurrent layers stacked vertically. Each layer takes the hidden states of the layer below as input. Learns hierarchical temporal representations. 2-4 layers typical in practice.\n"
         "3. Bidirectional RNN: Processes sequence in BOTH forward and backward directions. Gives context from both past AND future. Used in NLP where full sentence context is available.\n"
         "4. Encoder-Decoder (Seq2Seq): Two RNNs — encoder compresses input sequence to a fixed vector, decoder generates output sequence from that vector. Foundation of machine translation and text summarization.\n\n"
         "Adding more layers gives higher capacity to learn complex patterns but also increases training difficulty (deeper vanishing gradient).\n\n"
         "DISADVANTAGES OF RNN:\n\n"
         "1. VANISHING GRADIENT PROBLEM (Most Critical):\n"
         "During Backpropagation Through Time (BPTT), gradients must flow back through many time steps. Each step multiplies by the recurrent weight matrix and activation derivative (less than 1 for tanh/sigmoid). After many steps, gradients shrink to near-zero — early time steps receive essentially NO training signal. The network cannot learn long-range dependencies. Example: In a 100-word sentence, the network forgets what was said at the beginning when processing the end.\n\n"
         "2. EXPLODING GRADIENT PROBLEM:\n"
         "Conversely, if recurrent weights are large, gradients can grow exponentially. This causes wild weight updates that destabilize training. Partial solution: Gradient clipping — scale gradients down if their norm exceeds a threshold.\n\n"
         "3. SEQUENTIAL PROCESSING CANNOT BE PARALLELIZED:\n"
         "Each time step depends on the previous one — RNNs must be computed sequentially. This makes training SLOW on modern parallel hardware (GPUs). In contrast, Transformers (attention-based models) process all positions simultaneously. This limitation is why Transformers have largely replaced RNNs for NLP.\n\n"
         "4. DIFFICULTY LEARNING LONG-TERM DEPENDENCIES:\n"
         "Due to vanishing gradients, standard RNNs struggle with sequences where relevant information is far apart. Example: 'I grew up in France... I speak fluent French.' — 20 words separate 'France' from 'French' but they're related.\n\n"
         "5. COMPUTATIONALLY EXPENSIVE TO TRAIN:\n"
         "Unrolling through time steps creates very deep (virtual) networks, making BPTT computationally expensive and memory-intensive.\n\n"
         "SOLUTIONS TO RNN PROBLEMS:\n\n"
         "1. LSTM (Long Short-Term Memory, Hochreiter & Schmidhuber 1997):\n"
         "Adds a CELL STATE — a highway of information with gating mechanisms:\n"
         "Forget Gate: f(t) = σ(Wf·[h(t−1), x(t)] + bf) — what to forget\n"
         "Input Gate: i(t) = σ(Wi·[h(t−1), x(t)] + bi) — what to store\n"
         "Output Gate: o(t) = σ(Wo·[h(t−1), x(t)] + bo) — what to output\n"
         "Cell State update: C(t) = f(t)⊗C(t−1) + i(t)⊗tanh(Wc·[h(t−1),x(t)]+bc)\n"
         "The cell state gradients can flow unchanged across many time steps — solving vanishing gradient!\n\n"
         "2. GRU (Gated Recurrent Unit, Cho et al. 2014):\n"
         "Simplified LSTM with just two gates: Reset Gate and Update Gate. Fewer parameters, comparable performance.\n\n"
         "APPLICATIONS OF RNN/LSTM:\n"
         "Natural Language Processing, Speech Recognition (Siri, Google Voice), Machine Translation (Google Translate), Text Generation, Music Composition, Time Series Forecasting (stock prices, weather), Video Analysis, Handwriting Recognition.\n\n"
         "CONCLUSION:\n"
         "RNNs revolutionized sequential data processing in AI. Despite their limitations (vanishing gradient, no parallelism), the introduction of LSTM and GRU largely addressed these issues. While Transformers now dominate NLP, RNNs remain valuable for real-time streaming applications, embedded systems with limited memory, and problems where sequential processing is inherently needed.", C['purple'], C['pl']),
    ]:
        for item in qa(q, marks, years, ans, c, bg): story.append(item)

    story.append(PageBreak())

    # ════════════════════ SECTION 5: FUZZY LOGIC ══════════════════════════
    story.append(ban("SECTION 5 — FUZZY LOGIC & FUZZY NEURAL NETWORKS", C['teal']))
    story.append(Spacer(1,0.2*cm))

    for q,marks,years,ans,c,bg in [
        ("What do you mean by membership value in fuzzy logic? (Asked 2022)",
         "1.5 Marks — 100 words", "2022",
         "The membership value (or membership degree) μ_A(x) in fuzzy logic is a number between 0 and 1 that indicates the DEGREE to which an element x belongs to a fuzzy set A. Unlike crisp sets where membership is binary (0 or 1), fuzzy membership is gradual.\n\n"
         "μ_A(x) = 0: x does not belong to A at all.\n"
         "μ_A(x) = 0.5: x is the crossover point — equally in and out.\n"
         "μ_A(x) = 1: x fully belongs to A.\n\n"
         "Example: For fuzzy set 'TALL': μ_TALL(5'6\") = 0.5, μ_TALL(6'0\") = 0.9, μ_TALL(5'0\") = 0.1. The membership function defines the shape of this gradual transition.", C['teal'], C['tl']),

        ("What is Fuzzy Logic? Why is it important? Explain fuzzy operations and support/core of fuzzy set. (Asked 2018, 2023 — 5/7M)",
         "5 Marks — 500–800 words", "2018, 2023",
         "FUZZY LOGIC — COMPLETE ANSWER\n\n"
         "WHAT IS FUZZY LOGIC:\n"
         "Fuzzy Logic, introduced by Lotfi A. Zadeh (1965), is a form of multi-valued logic that extends classical binary logic to handle degrees of truth between 0 and 1. Rather than strict TRUE or FALSE, fuzzy logic allows PARTIAL TRUTH — 'somewhat hot', 'very tall', 'mostly done'.\n\n"
         "Classical logic: Temperature > 30°C is HOT (binary — yes or no).\n"
         "Fuzzy logic: Temperature 28°C is HOT with degree 0.7, and WARM with degree 0.5.\n\n"
         "WHY FUZZY LOGIC IS IMPORTANT:\n"
         "1. Models Human Reasoning: Humans naturally use approximate, vague terms — 'fairly fast', 'quite old'. Fuzzy logic formally captures this.\n"
         "2. Handles Real-World Vagueness: Most real-world concepts lack sharp boundaries. 'Middle-aged', 'healthy', 'expensive' are all fuzzy.\n"
         "3. Better Control Systems: Fuzzy controllers give smooth, gradual responses vs abrupt on/off switching. Example: Fuzzy air conditioners avoid temperature fluctuations.\n"
         "4. Simple Rules for Complex Behavior: Complex systems described with intuitive IF-THEN rules.\n"
         "5. No Mathematical Model Needed: Fuzzy systems don't need precise mathematical models.\n\n"
         "SUPPORT AND CORE OF A FUZZY SET:\n"
         "For fuzzy set A defined on universe X:\n\n"
         "Support(A) = {x ∈ X | μ_A(x) > 0}\n"
         "= All elements with ANY membership (strictly greater than 0).\n"
         "Example: For TALL: heights where μ > 0 (say 5'0\" to 7'0\").\n\n"
         "Core(A) = {x ∈ X | μ_A(x) = 1}\n"
         "= Elements with COMPLETE membership.\n"
         "Example: For TALL: heights of 6'3\" and above might have μ = 1.\n\n"
         "Height(A) = max{μ_A(x) | x ∈ X}\n"
         "= The maximum membership value. For a normal fuzzy set, Height = 1.\n\n"
         "α-cut: A_α = {x | μ_A(x) ≥ α} — all elements with membership at least α.\n\n"
         "Crossover point: Where μ_A(x) = 0.5 exactly.\n\n"
         "FUZZY SET OPERATIONS:\n\n"
         "1. Union (OR — max operator):\n"
         "μ_(A∪B)(x) = max(μ_A(x), μ_B(x))\n"
         "Example: μ_A=0.6, μ_B=0.8 → Union = 0.8\n\n"
         "2. Intersection (AND — min operator):\n"
         "μ_(A∩B)(x) = min(μ_A(x), μ_B(x))\n"
         "Example: μ_A=0.6, μ_B=0.8 → Intersection = 0.6\n\n"
         "3. Complement (NOT):\n"
         "μ_Ā(x) = 1 − μ_A(x)\n"
         "Example: μ_A=0.6 → Complement = 0.4\n\n"
         "FUZZY ARITHMETIC OPERATIONS:\n"
         "For triangular fuzzy numbers A=(a1,a2,a3) and B=(b1,b2,b3):\n"
         "Addition: A+B = (a1+b1, a2+b2, a3+b3)\n"
         "Subtraction: A−B = (a1−b3, a2−b2, a3−b1)\n"
         "Multiplication: A×B ≈ (a1×b1, a2×b2, a3×b3) [for positive numbers]\n\n"
         "FUZZY INFERENCE SYSTEM (FIS) — HOW FUZZY CONTROL WORKS:\n"
         "Step 1: Fuzzification — crisp input → membership degrees.\n"
         "Step 2: Rule Evaluation — evaluate IF-THEN fuzzy rules.\n"
         "Step 3: Aggregation — combine rule outputs.\n"
         "Step 4: Defuzzification — fuzzy output → crisp value.\n"
         "Most common defuzzification: Centroid x* = Σ(x·μ(x))/Σ(μ(x)).\n\n"
         "APPLICATIONS:\n"
         "Washing machines, air conditioners, camera autofocus, medical diagnosis, traffic control, robotics, NLP.\n\n"
         "CONCLUSION:\n"
         "Fuzzy logic bridges the gap between binary machine logic and approximate human reasoning. By allowing degrees of truth, it enables AI systems to handle the inherent vagueness of the real world.", C['teal'], C['tl']),

        ("Draw and explain the architecture of Fuzzy Neural System. (Asked 2023 — 5M)",
         "5 Marks — 500–800 words", "2023",
         "FUZZY NEURAL SYSTEM (NEURO-FUZZY SYSTEM) ARCHITECTURE\n\n"
         "INTRODUCTION:\n"
         "A Fuzzy Neural System (FNS), also called a Neuro-Fuzzy System, is a hybrid intelligent system that integrates Fuzzy Logic with Artificial Neural Networks. It combines the INTERPRETABILITY of fuzzy logic (human-readable IF-THEN rules) with the LEARNING ABILITY of neural networks (automatically adjusting parameters from data).\n\n"
         "WHY COMBINE FUZZY AND NEURAL?\n"
         "Pure ANN: Learns from data but is a black box — cannot explain reasoning.\n"
         "Pure Fuzzy System: Interpretable rules but must be manually designed by experts.\n"
         "Fuzzy Neural System: ANN learns the optimal membership functions and rule weights automatically from data — both interpretable AND adaptive.\n\n"
         "ANFIS ARCHITECTURE (Adaptive Neuro-Fuzzy Inference System — Jang, 1993):\n"
         "The most important and widely used FNS. Implements a Takagi-Sugeno fuzzy system trained with neural network methods.\n\n"
         "ANFIS has 5 layers:\n\n"
         "LAYER 1 — FUZZIFICATION LAYER:\n"
         "Each node computes the membership degree of the input to a fuzzy set.\n"
         "Output: Oi1 = μ_Ai(x) for input x, or μ_Bj(y) for input y.\n"
         "Uses Gaussian or triangular membership functions whose parameters (center, width) are LEARNED.\n"
         "These are called PREMISE PARAMETERS (antecedent parameters).\n\n"
         "LAYER 2 — RULE LAYER (AND layer):\n"
         "Each node represents one fuzzy rule. Computes the FIRING STRENGTH of each rule by multiplying the membership values from Layer 1:\n"
         "wi = μ_Ai(x) × μ_Bi(y)   [T-norm, usually product or min]\n"
         "Each node's output is the strength of one IF-THEN rule.\n\n"
         "LAYER 3 — NORMALIZATION LAYER:\n"
         "Each node normalizes the firing strengths so they sum to 1:\n"
         "w̄i = wi / Σwj\n"
         "This allows fair comparison between rules regardless of their absolute firing strengths.\n\n"
         "LAYER 4 — DEFUZZIFICATION LAYER:\n"
         "Each node computes the contribution of rule i to the output:\n"
         "Oi4 = w̄i × fi   where fi = pi×x + qi×y + ri (linear function of inputs)\n"
         "Parameters pi, qi, ri are called CONSEQUENT PARAMETERS — learned by least squares.\n\n"
         "LAYER 5 — OUTPUT LAYER:\n"
         "Single node that sums all Layer 4 outputs:\n"
         "y = Σ(w̄i × fi) = Σ(wi × fi) / Σwj\n"
         "This is the final crisp output of the fuzzy neural system.\n\n"
         "LEARNING IN ANFIS (Hybrid Algorithm):\n"
         "Forward pass: Fix Layer 1 parameters (premise). Use LEAST SQUARES to find optimal Layer 4 parameters (consequent).\n"
         "Backward pass: Fix Layer 4 parameters. Use BACKPROPAGATION (gradient descent) to update Layer 1 parameters.\n"
         "This hybrid method converges faster than pure gradient descent.\n\n"
         "ADVANTAGES OF FUZZY NEURAL SYSTEMS:\n"
         "1. Automatically learns membership functions from data.\n"
         "2. Produces interpretable fuzzy rules.\n"
         "3. Handles noisy, uncertain, and incomplete data.\n"
         "4. Faster convergence than pure gradient descent (hybrid learning).\n"
         "5. Universal approximator — can approximate any smooth function.\n\n"
         "APPLICATIONS:\n"
         "Medical diagnosis, robot control, financial forecasting, pattern recognition, time-series prediction, adaptive control systems.\n\n"
         "CONCLUSION:\n"
         "Fuzzy Neural Systems, especially ANFIS, represent the best fusion of symbolic (fuzzy rules) and connectionist (neural network) AI approaches. They provide the transparency humans need to trust AI decisions while retaining the powerful learning capabilities of neural networks.", C['teal'], C['tl']),
    ]:
        for item in qa(q, marks, years, ans, c, bg): story.append(item)

    story.append(PageBreak())

    # ════════════════════ SECTION 6: SEARCH METHODS ═══════════════════════
    story.append(ban("SECTION 6 — SEARCH METHODS: BFS, DFS, IDDFS", C['green']))
    story.append(Spacer(1,0.2*cm))

    for q,marks,years,ans,c,bg in [
        ("List advantages, disadvantages, time and space complexity of BFS. (Asked 2023)",
         "1.5 Marks — 100 words", "2023",
         "Breadth-First Search (BFS) — Quick Reference:\n\n"
         "Data Structure: Queue (FIFO). Strategy: Level by level.\n\n"
         "ADVANTAGES: Complete (always finds solution if exists). Optimal (finds shortest path when all step costs equal). Guaranteed minimum depth solution.\n\n"
         "DISADVANTAGES: Memory intensive — stores all nodes at current level. Impractical for large search spaces.\n\n"
         "TIME COMPLEXITY: O(b^d) — b = branching factor, d = depth of solution. Exponential.\n\n"
         "SPACE COMPLEXITY: O(b^d) — must store entire frontier. This is BFS's biggest weakness. For b=10, d=10: stores 10 billion nodes!", C['green'], C['gl']),

        ("Explain Iterative Deepening Search with advantages over brute force. Compare time/space complexity. (Asked 2023 — 15M)",
         "15 Marks — 1200–1500 words", "2023",
         "ITERATIVE DEEPENING DEPTH-FIRST SEARCH (IDDFS) — COMPLETE ANSWER\n\n"
         "INTRODUCTION:\n"
         "Iterative Deepening Depth-First Search (IDDFS) is an intelligent hybrid search strategy that combines the COMPLETENESS and OPTIMALITY of Breadth-First Search with the SPACE EFFICIENCY of Depth-First Search. It is considered the preferred uninformed search algorithm for large state spaces where solution depth is unknown.\n\n"
         "The intuition: BFS is excellent (complete, optimal) but memory-hungry. DFS uses minimal memory but may loop forever or miss the optimal solution. IDDFS eliminates both weaknesses by running DFS with an increasing depth limit.\n\n"
         "THE THREE FUNDAMENTAL SEARCH METHODS:\n\n"
         "1. BREADTH-FIRST SEARCH (BFS):\n"
         "Algorithm: Use a Queue (FIFO). Explore level by level — all depth-1 nodes before depth-2, etc.\n"
         "Properties:\n"
         "Completeness: YES — will find solution if it exists.\n"
         "Optimality: YES — finds shallowest (minimum steps) solution.\n"
         "Time Complexity: O(b^d) where b = branching factor, d = depth of solution.\n"
         "Space Complexity: O(b^d) — must store all nodes at each level simultaneously.\n"
         "PROBLEM: For b=10, d=6: stores 10^6 = 1 MILLION nodes. d=10: 10 BILLION nodes. Completely impractical for deep searches.\n\n"
         "2. DEPTH-FIRST SEARCH (DFS):\n"
         "Algorithm: Use a Stack (LIFO) or recursion. Go as deep as possible, backtrack when stuck.\n"
         "Properties:\n"
         "Completeness: NO — can follow infinite branch and never return. Can loop in cyclic spaces.\n"
         "Optimality: NO — finds deepest solution, not necessarily shortest.\n"
         "Time Complexity: O(b^m) — m = maximum depth. Could be infinite!\n"
         "Space Complexity: O(b×m) — only stores ONE current path. For b=10, d=10: only 100 nodes!\n"
         "ADVANTAGE: Excellent memory efficiency.\n"
         "PROBLEM: Incomplete and non-optimal.\n\n"
         "3. DEPTH-LIMITED SEARCH (DLS):\n"
         "DFS with a cutoff at depth limit L. Returns CUTOFF if depth reached without finding goal.\n"
         "Fixes infinite loop problem but introduces new problem: choosing the correct L.\n"
         "Too small L → misses solution. Too large L → wastes time.\n\n"
         "4. ITERATIVE DEEPENING DFS (IDDFS) — THE SOLUTION:\n\n"
         "Core idea: Try DLS with L=0, then L=1, then L=2, ... until solution found.\n\n"
         "IDDFS Algorithm:\n"
         "For limit = 0, 1, 2, 3, ...:\n"
         "    result = DLS(start_node, goal, limit)\n"
         "    if result ≠ CUTOFF:\n"
         "        return result\n\n"
         "DLS(node, goal, limit) — Recursive:\n"
         "    if node == goal: return SUCCESS\n"
         "    if limit == 0: return CUTOFF\n"
         "    cutoff_found = False\n"
         "    for each child of node:\n"
         "        result = DLS(child, goal, limit−1)\n"
         "        if result == CUTOFF: cutoff_found = True\n"
         "        elif result != FAILURE: return result\n"
         "    if cutoff_found: return CUTOFF\n"
         "    else: return FAILURE\n\n"
         "TRACE EXAMPLE:\n"
         "Tree: Root → {A, B}, A → {C, D}, B → {E, F}. Goal: E.\n"
         "Iteration L=0: Check Root. Not E. CUTOFF.\n"
         "Iteration L=1: Check Root→A, Root→B. A not E. B not E. CUTOFF.\n"
         "Iteration L=2: Check Root→A→C (not E), Root→A→D (not E), Root→B→E (E found!) → RETURN PATH.\n"
         "Result: [Root, B, E] — optimal path!\n\n"
         "WHY RE-EXPANSION IS NOT COSTLY:\n"
         "This is the key insight that makes IDDFS practical!\n\n"
         "For a tree with branching factor b and solution at depth d:\n"
         "Nodes generated by IDDFS at final iteration:\n"
         "Total = b^d + 2×b^(d−1) + 3×b^(d−2) + ... + d×b + (d+1)\n"
         "= O(b^d) — same asymptotic complexity as BFS!\n\n"
         "Why? Because the vast majority of nodes are at level d (exponentially more than earlier levels).\n"
         "Level d: b^d nodes (expanded once)\n"
         "Level d-1: b^(d-1) nodes (expanded twice)\n"
         "Level d-2: b^(d-2) nodes (expanded three times)\n"
         "For b=10: Level d has 10× more nodes than d-1. Re-expansion cost is only ~(10/9) ≈ 11% overhead!\n\n"
         "COMPLETE COMPLEXITY COMPARISON:\n"
         "BFS: Time=O(b^d), Space=O(b^d), Complete=YES, Optimal=YES\n"
         "DFS: Time=O(b^m), Space=O(b×m), Complete=NO, Optimal=NO\n"
         "DLS: Time=O(b^L), Space=O(b×L), Complete=NO (if L wrong), Optimal=NO\n"
         "IDDFS: Time=O(b^d), Space=O(b×d), Complete=YES, Optimal=YES\n\n"
         "SPACE ADVANTAGE — CONCRETE NUMBERS:\n"
         "For b=10, d=5, branchings=100,000 nodes:\n"
         "BFS space: 100,000 nodes must be stored simultaneously.\n"
         "IDDFS space: Only 5×10 = 50 nodes! (depth × branching)\n"
         "That's a 2000× reduction in memory!\n\n"
         "ADVANTAGES OF IDDFS OVER BRUTE FORCE:\n"
         "1. Memory Efficient: Space = O(b×d) vs BFS's O(b^d). Exponential improvement in memory.\n"
         "2. Complete: Like BFS, will always find a solution if one exists.\n"
         "3. Optimal: Like BFS, finds the minimum-depth (fewest steps) solution.\n"
         "4. No depth limit selection problem: Unlike DLS, doesn't need to guess the right depth.\n"
         "5. Simple implementation: Just calls DLS with increasing limits — minimal additional code.\n"
         "6. Handles infinite search spaces: Unlike BFS which would run out of memory.\n"
         "7. Time comparable to BFS: Only ~11% overhead from re-expansion (for b=10).\n\n"
         "WHEN TO USE EACH SEARCH METHOD:\n"
         "Use BFS: When solution is shallow AND memory is unlimited AND all costs equal.\n"
         "Use DFS: When any solution is acceptable AND memory is severely limited AND search space has no cycles.\n"
         "Use IDDFS: When solution depth is unknown AND memory is limited AND optimal solution is needed. BEST GENERAL-PURPOSE CHOICE.\n\n"
         "APPLICATIONS OF IDDFS:\n"
         "1. Game playing (chess, puzzle solving) where depth is unknown.\n"
         "2. Theorem proving with depth-bounded search.\n"
         "3. Compiler optimization (code analysis).\n"
         "4. Model checking in software verification.\n"
         "5. Large-scale pathfinding in robotics.\n\n"
         "CONCLUSION:\n"
         "IDDFS elegantly solves the fundamental tension between BFS and DFS. By sacrificing a small constant factor in time (roughly 11% overhead for branching factor 10), it achieves the memory efficiency of DFS while retaining the completeness and optimality of BFS. For any problem where solution depth is unknown and memory is at a premium, IDDFS is the algorithm of choice. Its simplicity, theoretical elegance, and practical efficiency make it a fundamental algorithm in AI.", C['green'], C['gl']),
    ]:
        for item in qa(q, marks, years, ans, c, bg): story.append(item)

    story.append(PageBreak())

    # ════════════════════ SECTION 7: HEURISTIC SEARCH ═════════════════════
    story.append(ban("SECTION 7 — HEURISTIC SEARCH: A*, AO*, BEST-FIRST, HILL CLIMBING", C['purple']))
    story.append(Spacer(1,0.2*cm))

    for q,marks,years,ans,c,bg in [
        ("What are the advantages of A* algorithm over hill climbing? (Asked 2022)",
         "1.5 Marks — 100 words", "2022",
         "A* vs Hill Climbing — Key Advantages of A*:\n\n"
         "1. COMPLETENESS: A* always finds a solution if one exists. Hill climbing can get permanently stuck at local optima.\n"
         "2. OPTIMALITY: A* finds the OPTIMAL (least cost) path when heuristic is admissible. Hill climbing finds only local optimum — not necessarily global.\n"
         "3. BACKTRACKING: A* maintains an OPEN list — can backtrack and explore other paths. Hill climbing has no backtracking.\n"
         "4. GLOBAL SEARCH: A* explores the entire relevant search space using f=g+h. Hill climbing is local — only looks at immediate neighbors.\n"
         "5. HANDLES PLATEAUX AND RIDGES: A* naturally handles these via the g(n) component. Hill climbing gets stuck.", C['purple'], C['pl']),

        ("Explain Best-First Search. Why is it preferred over Hill Climbing? (Asked 2023 — 10M)",
         "10 Marks — 800–1200 words", "2023",
         "BEST-FIRST SEARCH — COMPLETE ANSWER\n\n"
         "INTRODUCTION:\n"
         "Best-First Search is a heuristic search algorithm that selects the node to expand based on an EVALUATION FUNCTION that estimates how promising each node is. Unlike uninformed search (BFS, DFS) which explore blindly, Best-First Search uses domain knowledge to guide the search towards the goal more efficiently.\n\n"
         "The key idea: At each step, expand the node that appears to be closest to the goal according to our heuristic estimate h(n).\n\n"
         "GREEDY BEST-FIRST SEARCH:\n"
         "Evaluation function: f(n) = h(n)\n"
         "h(n) = heuristic estimate of cost from n to goal.\n"
         "Uses a PRIORITY QUEUE ordered by h(n) — lowest h is expanded first.\n\n"
         "ALGORITHM:\n"
         "1. Initialize: OPEN = {start with f=h(start)}.\n"
         "2. While OPEN is not empty:\n"
         "   a. Remove node n with MINIMUM f(n) from OPEN.\n"
         "   b. If n is GOAL → return path.\n"
         "   c. Expand n: generate all successors.\n"
         "   d. For each successor s: compute f(s) = h(s). Add to OPEN if not visited.\n"
         "3. If OPEN empty → no solution.\n\n"
         "EXAMPLE: Romania Map Problem.\n"
         "Goal: Travel from Arad to Bucharest.\n"
         "h(n) = straight-line distance to Bucharest.\n"
         "h(Arad)=366, h(Sibiu)=253, h(Timisoara)=329, h(Zerind)=374...\n"
         "Greedy Best-First: Arad → Sibiu (h=253) → Fagaras (h=176) → Bucharest (h=0).\n"
         "This finds a solution quickly but it may NOT be the optimal path!\n\n"
         "PROPERTIES:\n"
         "Completeness: NO — can follow a dead-end path indefinitely if h leads to a cycle.\n"
         "Optimality: NO — greedy choice ignores actual path cost g(n).\n"
         "Time: O(b^m) worst case. With good heuristic, much better in practice.\n"
         "Space: O(b^m) — stores all generated nodes.\n\n"
         "A* SEARCH — THE BEST-FIRST SEARCH VARIANT:\n"
         "A* combines actual path cost g(n) with heuristic h(n):\n"
         "f(n) = g(n) + h(n)\n"
         "g(n) = actual cost from start to n. h(n) = admissible heuristic.\n\n"
         "This makes A* both complete AND optimal (with admissible h).\n\n"
         "WHY BEST-FIRST SEARCH IS PREFERRED OVER HILL CLIMBING:\n\n"
         "1. GLOBAL VS LOCAL SEARCH:\n"
         "Hill Climbing: Only looks at current node and immediate neighbors. Makes purely LOCAL decisions.\n"
         "Best-First: Maintains a frontier of ALL generated nodes. Can jump to any promising node — makes GLOBAL decisions.\n\n"
         "2. HANDLES LOCAL OPTIMA:\n"
         "Hill Climbing: Gets permanently stuck at local maximum — no way to escape.\n"
         "Best-First: If current best path gets stuck, can backtrack and try other paths from OPEN list.\n\n"
         "3. COMPLETENESS:\n"
         "Hill Climbing: NOT complete — may never find solution if stuck at local optimum.\n"
         "Best-First: Complete in finite spaces — will eventually explore all nodes.\n\n"
         "4. PATH MEMORY:\n"
         "Hill Climbing: Maintains NO path memory — only knows current state.\n"
         "Best-First: Records entire path from start to each node — can reconstruct solution path.\n\n"
         "5. EXPLORATION BREADTH:\n"
         "Hill Climbing: Explores only 1 path at a time.\n"
         "Best-First: Explores MULTIPLE paths simultaneously — the OPEN list tracks all alternatives.\n\n"
         "6. HANDLES PLATEAUX:\n"
         "Hill Climbing: Gets stuck when all neighbors have equal value.\n"
         "Best-First: Can randomly select among equal-valued nodes or use tie-breaking.\n\n"
         "COMPARISON TABLE:\n"
         "Evaluation function: HC=h(n) current only | BFS=h(n) all frontier nodes.\n"
         "Data structure: HC=none (single state) | BFS=priority queue.\n"
         "Backtracking: HC=NO | BFS=YES (via OPEN list).\n"
         "Local optima: HC=gets stuck | BFS=can escape.\n"
         "Complete: HC=NO | BFS=YES (finite spaces).\n"
         "Optimal: HC=NO | BFS=NO (A* YES with admissible h).\n"
         "Memory: HC=O(1) | BFS=O(b^m).\n\n"
         "HEURISTIC FUNCTIONS:\n"
         "A good heuristic h(n) must be:\n"
         "1. Informative: Should closely estimate true cost h*(n).\n"
         "2. Admissible: h(n) ≤ h*(n) — never overestimates (for A* optimality).\n"
         "3. Consistent: h(n) ≤ c(n,a,n') + h(n') — satisfies triangle inequality.\n"
         "4. Computationally cheap to evaluate.\n\n"
         "Examples for 8-puzzle:\n"
         "h1 = Number of misplaced tiles (admissible).\n"
         "h2 = Sum of Manhattan distances (admissible, more informed than h1).\n"
         "h2 dominates h1: h2(n) ≥ h1(n) for all n → A* with h2 expands fewer nodes.\n\n"
         "APPLICATIONS:\n"
         "Best-First Search and A* are used in GPS navigation (Google Maps), game AI (pathfinding in video games), robot motion planning, network routing, puzzle solving (8-puzzle, 15-puzzle), and scheduling.\n\n"
         "CONCLUSION:\n"
         "Best-First Search represents a fundamental improvement over blind search methods and local search like hill climbing. By maintaining a global view of the search space through the OPEN list and guiding expansion with an informative heuristic, it achieves a practical balance between search efficiency and solution quality.", C['purple'], C['pl']),

        ("What is Means-End Analysis? Explain with algorithm. (Asked 2018 — 5M)",
         "5 Marks — 500–800 words", "2018",
         "MEANS-END ANALYSIS — COMPLETE ANSWER\n\n"
         "INTRODUCTION:\n"
         "Means-End Analysis (MEA) is a problem-solving technique that reduces the DIFFERENCE between the current state and the goal state by selecting and applying appropriate OPERATORS (means). Proposed by Newell and Simon (1963), it is the core mechanism of the General Problem Solver (GPS).\n\n"
         "The key idea: Instead of searching forward from start or backward from goal, MEA focuses on WHAT DIFFERENCE exists and WHAT ACTION would reduce that difference.\n\n"
         "ANALOGY:\n"
         "You want to travel from Delhi to Mumbai (goal) but you're currently in Delhi with no vehicle. The difference is: 'no vehicle'. The means to reduce this difference: 'get transport'. You book a flight. Now you're at Delhi airport. Difference: 'not at destination'. Means: 'board plane'. You arrive at Mumbai airport. Difference: 'not at hotel'. Means: 'take taxi'. Goal achieved!\n\n"
         "CORE CONCEPTS:\n"
         "1. Current State: Where we are now.\n"
         "2. Goal State: Where we want to be.\n"
         "3. Difference: What distinguishes current from goal state.\n"
         "4. Operators: Actions that can reduce specific differences.\n"
         "5. Operator Table: Maps each type of difference to operators that reduce it.\n"
         "6. Preconditions: Conditions required before an operator can be applied.\n"
         "7. Sub-goals: When an operator's preconditions aren't met, create a sub-goal to achieve them first.\n\n"
         "MEA ALGORITHM:\n\n"
         "function MEA(Current_State, Goal_State):\n"
         "1. If Current_State = Goal_State: return SUCCESS.\n"
         "2. Compute Difference D = diff(Current_State, Goal_State).\n"
         "3. If D = empty: return SUCCESS.\n"
         "4. Select operator Op that reduces the most important difference in D.\n"
         "5. Check if Op is APPLICABLE to Current_State:\n"
         "   a. If YES: Apply Op. New_State = Op(Current_State).\n"
         "      Return MEA(New_State, Goal_State).\n"
         "   b. If NO (preconditions not met):\n"
         "      Create sub-goal S = preconditions of Op.\n"
         "      MEA(Current_State, S)  [achieve sub-goal first]\n"
         "      Apply Op. Return MEA(New_State, Goal_State).\n"
         "6. If no applicable operator found: return FAILURE.\n\n"
         "EXAMPLE — Monkey and Banana Problem:\n"
         "Current State: Monkey at door (A), box at window (B), banana at ceiling (C), monkey not on box.\n"
         "Goal State: Monkey has banana.\n\n"
         "Step 1: Difference D = Monkey doesn't have banana.\n"
         "Op to reduce D: GRAB banana.\n"
         "Precondition of GRAB: Monkey must be directly below banana AND on box.\n\n"
         "Step 2: Monkey not on box — create sub-goal: Monkey on box at C.\n"
         "Difference D2: Box not at C. Op: PUSH(box, C). Precondition: Monkey at B (at box).\n\n"
         "Step 3: Monkey not at B — create sub-goal: Move monkey to B.\n"
         "Op: WALK(A→B). No preconditions needed. Apply.\n"
         "Now monkey at B.\n\n"
         "Step 4: PUSH box from B to C. Now box at C, monkey at C.\n\n"
         "Step 5: CLIMB on box. Now monkey on box at C.\n\n"
         "Step 6: GRAB banana. Sub-goals all satisfied. Goal achieved!\n\n"
         "Solution sequence: WALK(A,B) → PUSH(B,C) → CLIMB → GRAB.\n\n"
         "ADVANTAGES:\n"
         "1. Focuses on relevant differences — doesn't explore irrelevant states.\n"
         "2. Natural decomposition into sub-goals.\n"
         "3. Handles complex problems by recursive goal reduction.\n"
         "4. Works in planning, robotics, and natural language processing.\n\n"
         "DISADVANTAGES:\n"
         "1. Difference table must be manually designed — requires domain knowledge.\n"
         "2. Can cycle if sub-goals create the original goal as their prerequisite.\n"
         "3. May be inefficient if sub-goal chains are long.\n\n"
         "APPLICATIONS:\n"
         "GPS (General Problem Solver), robot task planning, automated theorem proving, game playing strategies.", C['purple'], C['pl']),
    ]:
        for item in qa(q, marks, years, ans, c, bg): story.append(item)

    story.append(PageBreak())

    # ════════════════════ SECTION 8: KR ═══════════════════════════════════
    story.append(ban("SECTION 8 — KNOWLEDGE REPRESENTATION (FOPL, SEMANTIC NETS, FRAMES, SCRIPTS)", C['maroon']))
    story.append(Spacer(1,0.2*cm))

    for q,marks,years,ans,c,bg in [
        ("What are disadvantages of FOPL over Propositional Logic? (Asked 2018)",
         "1.5 Marks — 100 words", "2018",
         "Disadvantages of FOPL compared to Propositional Logic:\n\n"
         "1. More Complex: FOPL adds predicates, variables, quantifiers (∀, ∃), and functions — more syntax to learn and implement.\n"
         "2. Computationally Expensive: Inference in FOPL is more expensive than propositional logic. Resolution in PL is decidable in polynomial time; FOPL resolution is only semi-decidable.\n"
         "3. Undecidability: FOPL is semi-decidable — if a formula is valid we can prove it, but if it's invalid we may search forever.\n"
         "4. Harder to Automate: Unification (matching variables to terms) adds complexity to automated reasoning.\n"
         "5. Harder Debugging: Complex quantifier scoping errors are difficult to detect.", C['maroon'], C['ml']),

        ("What is Predicate Logic? Why is it preferred over Propositional Logic? Explain with examples for KR. (Asked 2023 — 10M)",
         "10 Marks — 800–1200 words", "2023",
         "PREDICATE LOGIC (FOPL) — COMPLETE ANSWER\n\n"
         "INTRODUCTION:\n"
         "First-Order Predicate Logic (FOPL), also called First-Order Logic (FOL) or Predicate Calculus, is a formal logical system that extends Propositional Logic by introducing predicates, variables, constants, functions, and quantifiers. It is the most widely used formal language for knowledge representation in AI, providing expressive power to represent complex relationships and reason about them.\n\n"
         "PROPOSITIONAL LOGIC — LIMITATIONS:\n"
         "Propositional Logic (PL) deals with simple statements (propositions) that are either TRUE or FALSE. Example: P = 'It is raining', Q = 'Roads are wet'. Rule: P → Q.\n\n"
         "Critical limitations:\n"
         "1. Cannot represent OBJECTS and their PROPERTIES individually.\n"
         "2. Cannot represent RELATIONSHIPS between objects.\n"
         "3. Cannot represent QUANTIFIED statements (all, some, none).\n"
         "4. 'All humans are mortal' requires a separate proposition for EACH human — impractical.\n"
         "5. Cannot represent general rules that apply to all members of a class.\n\n"
         "FOPL — COMPONENTS AND SYNTAX:\n\n"
         "1. CONSTANTS: Specific named individuals.\n"
         "Examples: Socrates, Paris, 42, John, YMCA\n\n"
         "2. VARIABLES: Represent unspecified individuals.\n"
         "Examples: x, y, z, person, city\n\n"
         "3. PREDICATES: Represent properties of objects or relationships between objects.\n"
         "Unary predicate (property): Human(x) = 'x is human', Tall(x) = 'x is tall'\n"
         "Binary predicate (relationship): Loves(x,y) = 'x loves y', GreaterThan(x,y)\n"
         "n-ary predicate: Between(x,y,z) = 'x is between y and z'\n\n"
         "4. FUNCTIONS: Map individuals to individuals.\n"
         "Examples: father(x) = father of x, age(x) = age of x, sqrt(x) = square root of x\n\n"
         "5. UNIVERSAL QUANTIFIER ∀ ('for all'):\n"
         "∀x [Human(x) → Mortal(x)] = 'Every human is mortal'\n"
         "∀x ∀y [Parent(x,y) → Loves(x,y)] = 'All parents love their children'\n\n"
         "6. EXISTENTIAL QUANTIFIER ∃ ('there exists'):\n"
         "∃x [Dog(x) ∧ Friendly(x)] = 'Some dog is friendly'\n"
         "∃x ∃y [City(x) ∧ City(y) ∧ CapitalOf(x, France)] = 'There is a capital city of France'\n\n"
         "7. LOGICAL CONNECTIVES (same as PL):\n"
         "¬ (NOT), ∧ (AND), ∨ (OR), → (IMPLIES), ↔ (IFF)\n\n"
         "WHY FOPL IS PREFERRED OVER PROPOSITIONAL LOGIC:\n\n"
         "1. EXPRESSIVENESS:\n"
         "PL: Cannot say 'All dogs have tails' in general — must write Dog_Fido_has_tail ∧ Dog_Rex_has_tail ∧ ...\n"
         "FOPL: ∀x [Dog(x) → HasTail(x)] — one general statement covers ALL dogs.\n\n"
         "2. QUANTIFICATION:\n"
         "PL: No quantifiers. Cannot express 'some', 'all', 'none'.\n"
         "FOPL: ∀ (universal) and ∃ (existential) quantifiers handle these naturally.\n\n"
         "3. RELATIONSHIPS BETWEEN OBJECTS:\n"
         "PL: Cannot represent binary or n-ary relationships.\n"
         "FOPL: Loves(John, Mary), GreaterThan(5, 3), Between(Paris, London, Berlin).\n\n"
         "4. CONCISENESS:\n"
         "PL: Need separate propositions for each individual.\n"
         "FOPL: Single formula with variables covers all individuals.\n\n"
         "5. INFERENCE POWER:\n"
         "PL: Resolution-based inference is limited.\n"
         "FOPL: Unification + Resolution enables powerful automated theorem proving.\n\n"
         "USING FOPL FOR KNOWLEDGE REPRESENTATION:\n\n"
         "Example 1 — Family Relationships:\n"
         "'John is the father of Mary': Father(John, Mary)\n"
         "'All fathers are parents': ∀x ∀y [Father(x,y) → Parent(x,y)]\n"
         "'Every parent loves their child': ∀x ∀y [Parent(x,y) → Loves(x,y)]\n"
         "Derived (by modus ponens + universal instantiation): Loves(John, Mary) ✓\n\n"
         "Example 2 — Block World:\n"
         "'Block A is on Block B': On(A, B)\n"
         "'Nothing is on top of Block A': ∀x ¬On(x, A)\n"
         "'A is clear': Clear(A) ← ∀x ¬On(x,A)\n\n"
         "Example 3 — Medical Knowledge:\n"
         "'Every patient with fever has elevated temperature': ∀x [Patient(x) ∧ Fever(x) → HighTemp(x)]\n"
         "'Some patients have allergies': ∃x [Patient(x) ∧ HasAllergy(x)]\n\n"
         "Example 4 — Represent 'Every Gardner likes the sun' (2017 exam):\n"
         "∀x [Gardner(x) → Likes(x, Sun)]\n\n"
         "INFERENCE IN FOPL:\n\n"
         "1. Universal Instantiation (UI): From ∀x P(x), conclude P(a) for any specific a.\n"
         "2. Existential Instantiation (EI): From ∃x P(x), conclude P(c) for new constant c.\n"
         "3. Modus Ponens: From P and P→Q, conclude Q.\n"
         "4. Resolution: Powerful unification-based inference used in theorem provers.\n\n"
         "LIMITATIONS OF FOPL:\n"
         "1. Undecidable: Validity checking is only semi-decidable.\n"
         "2. Computationally expensive: Inference is more costly than PL.\n"
         "3. Cannot easily represent procedural knowledge or uncertainty.\n"
         "4. Frame problem: Expensive to represent what doesn't change.\n\n"
         "CONCLUSION:\n"
         "FOPL is the language of choice for formal knowledge representation in AI. Its ability to express general rules, relationships, and quantified statements makes it far more powerful than propositional logic. It underpins expert systems, automated theorem provers, logic programming (Prolog), semantic web technologies (OWL, RDF), and formal verification systems.", C['maroon'], C['ml']),

        ("Represent knowledge about a Laptop using semantic net. (Asked 2018 — 1.5M)",
         "1.5 Marks — 100 words", "2018",
         "Semantic network for a Laptop:\n\n"
         "Nodes: Laptop, Computer, ElectronicDevice, CPU, RAM, Storage, Screen, Keyboard, Battery, Windows\n\n"
         "Arcs (relationships):\n"
         "Laptop ──IS-A──► Computer\n"
         "Computer ──IS-A──► ElectronicDevice\n"
         "Laptop ──HAS-PART──► CPU\n"
         "Laptop ──HAS-PART──► RAM\n"
         "Laptop ──HAS-PART──► Storage (SSD/HDD)\n"
         "Laptop ──HAS-PART──► Screen\n"
         "Laptop ──HAS-PART──► Keyboard\n"
         "Laptop ──HAS-PART──► Battery\n"
         "Laptop ──RUNS──► Windows/Linux\n"
         "Laptop ──CAN──► BrowseInternet\n"
         "Laptop ──CAN──► RunPrograms\n\n"
         "By inheritance: Laptop IS-A Computer IS-A ElectronicDevice → Laptop uses electricity, has processor.", C['maroon'], C['ml']),

        ("Write short notes on: Blackboard Architecture, Inductive and Deductive Reasoning, Semantic Nets and Frames. (Asked 2022 Q7 — 15M)",
         "15 Marks — 1200–1500 words", "2022",
         "SHORT NOTE (a): BLACKBOARD ARCHITECTURE\n\n"
         "INTRODUCTION AND ORIGIN:\n"
         "The Blackboard Architecture is a cooperative AI problem-solving model developed for the HEARSAY-II speech recognition system at Carnegie Mellon University in the 1970s. It is based on the metaphor of multiple expert people collaborating around a single large blackboard — each expert reads from and writes to the blackboard, gradually building a solution.\n\n"
         "THREE COMPONENTS:\n\n"
         "1. The Blackboard (Global Workspace):\n"
         "A hierarchically structured shared memory — the SOLE communication medium. No module communicates directly with another; all coordination happens through the blackboard. Organized into abstraction levels:\n"
         "Level 1: Raw data / lowest-level representation (acoustic signals in HEARSAY-II)\n"
         "Level 2: Low-level hypotheses (phonemes, syllables)\n"
         "Level 3: Mid-level hypotheses (words)\n"
         "Level 4: High-level hypotheses (phrases, sentences)\n"
         "The evolving partial solution is stored on the blackboard. When complete, it appears at the highest level.\n\n"
         "2. Knowledge Sources (KSes):\n"
         "Independent, specialized expert modules. Each KS is self-contained and domain-specific. Each KS has:\n"
         "Trigger Condition: When is this KS applicable? (Monitors specific patterns on the blackboard)\n"
         "Action: What does the KS do? (Reads data from BB, computes, writes result to higher level)\n"
         "KSes do NOT communicate with each other — only through the blackboard. Different KSes may use entirely different knowledge representations (rules, neural networks, fuzzy systems).\n\n"
         "3. Control Component (Scheduler):\n"
         "The 'conductor' — monitors the blackboard for changes, identifies triggered KSes, selects the most appropriate one using a scheduling strategy (opportunistic/best-first, priority-based, breadth-first, depth-first).\n\n"
         "WORKING CYCLE:\n"
         "Input placed on BB → Control identifies triggered KSes → Best KS selected → KS reads, computes, writes → New data triggers more KSes → Repeat until solution at highest level.\n\n"
         "Applications: HEARSAY-II (speech), HASP (sonar), PROTEAN (protein structure), multi-agent systems.\n"
         "Advantages: Modular, flexible, handles uncertainty, parallel.\n"
         "Disadvantages: Complex control, communication overhead.\n\n"
         "---\n\n"
         "SHORT NOTE (b): INDUCTIVE AND DEDUCTIVE REASONING\n\n"
         "DEDUCTIVE REASONING:\n"
         "Deductive reasoning moves from GENERAL principles to SPECIFIC conclusions. If the premises are true and the argument is valid, the conclusion is LOGICALLY GUARANTEED.\n\n"
         "Form: Major Premise + Minor Premise → Conclusion\n"
         "Example: All humans are mortal (general rule).\n"
         "Socrates is human (specific fact).\n"
         "Therefore Socrates is mortal. (conclusion — guaranteed)\n\n"
         "Deductive inference rules: Modus Ponens (P, P→Q ⊢ Q), Modus Tollens (¬Q, P→Q ⊢ ¬P), Hypothetical Syllogism.\n\n"
         "In AI: Used in expert systems (backward/forward chaining with rules), theorem provers, logic programming (Prolog).\n"
         "Strength: Logically guaranteed conclusions.\n"
         "Weakness: Cannot generate new knowledge beyond what's already in premises.\n\n"
         "INDUCTIVE REASONING:\n"
         "Inductive reasoning moves from SPECIFIC observations to GENERAL rules. The conclusion is NOT logically guaranteed — it is a probable generalization.\n\n"
         "Form: Multiple specific observations → General rule\n"
         "Example: Sun rose in the east yesterday. And the day before. And every recorded day in history.\n"
         "Therefore the sun always rises in the east. (generalization — probable but not guaranteed)\n\n"
         "Classic problem: 1000 white swans observed → 'All swans are white.' Then a black swan is discovered in Australia — the rule was wrong! No amount of confirming evidence makes induction certain.\n\n"
         "In AI/ML: Machine learning IS inductive reasoning — learn general rules from specific training examples. ID3 decision tree, neural network training, rule learning algorithms all use induction.\n\n"
         "Induction in AI: See positive/negative examples → Induce hypothesis that generalizes. Key: Occam's Razor — prefer simpler hypotheses. Use validation data to check if induced rule generalizes.\n\n"
         "COMPARISON:\n"
         "Deduction: General → Specific | Logically guaranteed | Used in expert systems, theorem provers.\n"
         "Induction: Specific → General | Probable, not guaranteed | Used in machine learning, data mining.\n\n"
         "---\n\n"
         "SHORT NOTE (c): SEMANTIC NETS AND FRAMES\n\n"
         "SEMANTIC NETWORKS (Quillian, 1968):\n"
         "A Semantic Network is a directed labeled graph for knowledge representation.\n"
         "Nodes represent concepts, objects, events, or entities.\n"
         "Labeled arcs represent typed relationships between nodes.\n\n"
         "Core relationship types:\n"
         "IS-A: Class membership/subtype (Dog IS-A Animal, Fido IS-A Dog)\n"
         "HAS-A: Attribute possession (Dog HAS-A Tail, Car HAS-A Engine)\n"
         "HAS-PART: Component relationship (Car HAS-PART Wheel)\n"
         "CAN: Capability (Bird CAN Fly, Dog CAN Bark)\n"
         "IS-INSTANCE-OF: Specific individual to class (Fido IS-INSTANCE-OF Dog)\n\n"
         "INHERITANCE: Properties flow downward via IS-A links. Fido inherits all properties of Dog, and Dog inherits all properties of Animal. This eliminates redundancy — no need to state 'Fido can bark' separately if we know 'Fido IS-A Dog' and 'Dog CAN Bark'.\n\n"
         "Example network:\n"
         "Animal ──CAN──► Breathe | Animal ──HAS──► WarmBlood\n"
         "Dog ──IS-A──► Animal | Dog ──HAS-A──► Tail | Dog ──CAN──► Bark\n"
         "Fido ──IS-INSTANCE-OF──► Dog\n"
         "By inheritance: Fido CAN Bark (from Dog) + Fido CAN Breathe (from Animal).\n\n"
         "Advantages: Visual, intuitive, supports inheritance, reduces redundancy.\n"
         "Disadvantages: Limited expressiveness (no quantifiers, negation, rules).\n\n"
         "FRAMES (Minsky, 1975):\n"
         "A Frame is a data structure representing stereotyped objects or situations. Like a class in object-oriented programming — a template with named slots and values.\n\n"
         "Frame components:\n"
         "Frame Name: The concept (e.g., Car, Person, Meeting)\n"
         "Slots: Attributes (Color, Weight, Speed, Name)\n"
         "Fillers: Actual values (Color = Red, Speed = 120 km/h)\n"
         "Default Values: Assumed when no value provided (Wheels = 4 for Car)\n"
         "Demons: IF-NEEDED (compute when accessed), IF-ADDED (trigger on insertion)\n"
         "IS-A link: Inheritance from parent frame\n\n"
         "Example:\n"
         "FRAME: Vehicle | Wheels=4 (default) | Engine=yes | CanDo=Transport\n"
         "FRAME: Car IS-A Vehicle | Doors=4 (default) | FuelType=(Petrol/Diesel/Electric)\n"
         "FRAME: ElectricCar IS-A Car | FuelType=Electric | Battery=integer kWh\n\n"
         "Instantiation: MyTesla IS-A ElectricCar | Color=Red | Battery=100kWh\n"
         "MyTesla automatically inherits: Wheels=4, Engine=yes, Doors=4 via inheritance chain.\n\n"
         "Advantages: Natural for objects, supports defaults, inheritance, demons combine declarative and procedural knowledge.\n"
         "Disadvantages: Rigid structure, multiple inheritance conflicts, no formal semantics.", C['maroon'], C['ml']),
    ]:
        for item in qa(q, marks, years, ans, c, bg): story.append(item)

    story.append(PageBreak())

    # ════════════════════ SECTION 9: EXPERT SYSTEMS ═══════════════════════
    story.append(ban("SECTION 9 — EXPERT SYSTEMS & KNOWLEDGE-BASED SYSTEMS", C['green']))
    story.append(Spacer(1,0.2*cm))

    for q,marks,years,ans,c,bg in [
        ("Compare rule-based expert system with non-rule-based expert system. (Asked 2017 — 10M)",
         "10 Marks — 800–1200 words", "2017",
         "RULE-BASED VS NON-RULE-BASED EXPERT SYSTEMS\n\n"
         "INTRODUCTION:\n"
         "An Expert System is a knowledge-based AI system designed to replicate the decision-making capabilities of a human expert in a specific domain. Expert systems can be categorized based on their knowledge representation and reasoning mechanisms. The two main categories are Rule-Based and Non-Rule-Based (also called Non-Production System) expert systems.\n\n"
         "PART A: RULE-BASED EXPERT SYSTEMS\n\n"
         "A Rule-Based Expert System stores all domain knowledge in the form of IF-THEN production rules. This is the most common type of expert system.\n\n"
         "Architecture Components:\n\n"
         "1. Knowledge Base: Contains IF-THEN rules.\n"
         "Rule format: IF <condition> THEN <conclusion/action> [CF = certainty factor]\n"
         "Example rules for medical diagnosis:\n"
         "R1: IF fever > 101 AND cough THEN suspect-pneumonia [CF=0.7]\n"
         "R2: IF suspect-pneumonia AND WBC-high THEN diagnose-pneumonia [CF=0.8]\n"
         "R3: IF diagnose-pneumonia THEN recommend-antibiotic [CF=0.9]\n\n"
         "2. Working Memory (Fact Base): Current problem facts and derived conclusions.\n\n"
         "3. Inference Engine: Pattern-match rules against working memory. Uses:\n"
         "Forward Chaining: Data-driven. Known facts → apply rules → derive conclusions.\n"
         "Backward Chaining: Goal-driven. Start from hypothesis → find supporting facts.\n\n"
         "4. Conflict Resolution: When multiple rules match, choose by:\n"
         "Specificity (most specific rule wins), Recency (newest fact wins), Priority (assigned rank).\n\n"
         "5. Explanation Facility: WHY (why was this question asked?) and HOW (how was conclusion reached?).\n\n"
         "Examples: MYCIN (bacterial infection diagnosis), DENDRAL (molecular structure analysis), XCON (DEC computer configuration), PROSPECTOR (mineral exploration).\n\n"
         "Advantages of Rule-Based ES:\n"
         "1. Modular — rules can be added/removed independently without affecting others.\n"
         "2. Transparent — clear reasoning chain; easy to explain decisions (WHY/HOW modules).\n"
         "3. Consistent — always applies same rules to same facts.\n"
         "4. Easy to validate — each rule can be checked independently.\n"
         "5. Maintainable — domain experts can understand and update rules.\n\n"
         "Disadvantages of Rule-Based ES:\n"
         "1. Knowledge acquisition bottleneck — extracting rules from experts is time-consuming.\n"
         "2. Many rules → slow matching (RETE algorithm helps).\n"
         "3. Cannot handle continuous/numeric domains well.\n"
         "4. Brittle at domain boundaries — fails outside programmed rules.\n"
         "5. Cannot learn from experience — rules must be manually updated.\n\n"
         "PART B: NON-RULE-BASED EXPERT SYSTEMS\n\n"
         "Non-rule-based expert systems use knowledge representations OTHER than production rules — frames, neural networks, cases, or model-based approaches.\n\n"
         "Types of Non-Rule-Based ES:\n\n"
         "1. Frame-Based Expert Systems:\n"
         "Knowledge represented in frames (slot-value structures with inheritance).\n"
         "Reasoning through frame inheritance and demons (IF-NEEDED procedures).\n"
         "Better for object-oriented domains with many properties and hierarchies.\n"
         "Example: Medical ES representing patient records as frames with inheritance.\n\n"
         "2. Case-Based Reasoning (CBR) Systems:\n"
         "Solve new problems by finding similar PAST CASES and adapting their solutions.\n"
         "No explicit rules — knowledge is implicit in the case library.\n"
         "4R cycle: Retrieve → Reuse → Revise → Retain.\n"
         "Example: CASEY (cardiac diagnosis by case retrieval), legal case systems.\n"
         "Advantage: Natural learning — automatically improves by adding new cases.\n\n"
         "3. Model-Based Expert Systems:\n"
         "Uses a CAUSAL MODEL of the system's structure and behavior.\n"
         "Understands WHY things fail, not just WHAT rules to apply.\n"
         "Can diagnose novel faults not covered by existing rules.\n"
         "Example: Automobile fault diagnosis understanding physical causality.\n\n"
         "4. Neural Network-Based Expert Systems:\n"
         "Knowledge encoded in network weights through training.\n"
         "Can handle noisy, uncertain, and pattern-based knowledge.\n"
         "Disadvantage: Black box — cannot explain reasoning.\n\n"
         "COMPARISON TABLE:\n"
         "Knowledge form: Rule-based=IF-THEN rules | Non-rule=Frames/cases/neural/models.\n"
         "Reasoning: Rule-based=Forward/backward chaining | Non-rule=Inheritance/retrieval/propagation.\n"
         "Transparency: Rule-based=HIGH (explainable) | Non-rule=Variable (low for neural).\n"
         "Learning: Rule-based=NO (manual updates) | CBR=YES (case accumulation).\n"
         "Best domain: Rule-based=Diagnostic, advisory | Non-rule=Object-rich, case-based, continuous.\n"
         "Example: Rule-based=MYCIN, XCON | Non-rule=CASEY, KATE, neural-diagnosis systems.\n\n"
         "CONCLUSION:\n"
         "Rule-based expert systems are preferred when domain knowledge is naturally expressible as IF-THEN rules, explainability is critical, and consistency is paramount. Non-rule-based systems are better when the domain is case-driven, object-rich, or involves continuous sensor data. Modern hybrid expert systems combine multiple representations — using rules for diagnosis, frames for objects, neural networks for pattern recognition, and cases for novel situations.", C['green'], C['gl']),
    ]:
        for item in qa(q, marks, years, ans, c, bg): story.append(item)

    story.append(PageBreak())

    # ════════════════════ SECTION 10: GENETIC ALGORITHM ═══════════════════
    story.append(ban("SECTION 10 — GENETIC ALGORITHM (All PYQ Questions)", C['orange']))
    story.append(Spacer(1,0.2*cm))

    for q,marks,years,ans,c,bg in [
        ("What is Genetic Algorithm? When is it applicable? How can it be applied on TSP? (Asked 2023 — 8M)",
         "10 Marks — 800–1200 words", "2023",
         "GENETIC ALGORITHM — COMPLETE ANSWER WITH TSP APPLICATION\n\n"
         "WHAT IS A GENETIC ALGORITHM:\n"
         "A Genetic Algorithm (GA) is a population-based stochastic search and optimization technique inspired by Charles Darwin's theory of natural evolution — 'survival of the fittest'. Developed by John Holland (1975) at University of Michigan, GA maintains a POPULATION of candidate solutions and evolves them through selection, crossover, and mutation over multiple generations.\n\n"
         "Core principle: Better solutions (higher fitness) survive and reproduce more. Their offspring inherit their characteristics, with occasional mutations introducing diversity. Over generations, the population evolves toward increasingly better solutions.\n\n"
         "WHEN IS GA APPLICABLE:\n"
         "GA is most appropriate when:\n"
         "1. The search space is LARGE and complex with many local optima (GA explores multiple areas simultaneously).\n"
         "2. No gradient information is available — GA requires only a fitness function, not derivatives.\n"
         "3. The objective function is non-differentiable, discontinuous, or noisy.\n"
         "4. Multiple objectives need to be optimized simultaneously.\n"
         "5. The problem is combinatorial (scheduling, routing, assignment).\n"
         "6. Problem-specific algorithms don't exist or are too slow.\n"
         "Not suitable: When problem is smooth, convex, and gradient methods work well; when real-time response is needed; when exact optimal solution is required.\n\n"
         "GA ALGORITHM — COMPLETE STEPS:\n\n"
         "Step 1 — REPRESENTATION:\n"
         "Encode each candidate solution as a CHROMOSOME. Binary: 10110101. Integer: [2,5,1,4,3]. Real-valued: [1.5, 3.7, 0.2].\n\n"
         "Step 2 — INITIALIZE POPULATION:\n"
         "Generate N random chromosomes. N typically 50-500. Larger N = better exploration, slower computation.\n\n"
         "Step 3 — EVALUATE FITNESS:\n"
         "Compute fitness f(chromosome) for each individual. Higher fitness = better solution. This is the problem-specific objective function.\n\n"
         "Step 4 — CHECK TERMINATION:\n"
         "Stop if: maximum generations reached, fitness threshold met, or population converged. Otherwise continue.\n\n"
         "Step 5 — SELECTION:\n"
         "Select parents for reproduction. Better fitness = higher selection probability.\n"
         "Roulette Wheel: P(i) = f(i)/Σf(j).\n"
         "Tournament: Pick k random individuals, best wins.\n"
         "Elitism: Always copy best individual(s) unchanged.\n\n"
         "Step 6 — CROSSOVER (probability Pc ≈ 0.7-0.9):\n"
         "Combine two parents to create offspring:\n"
         "Single-Point: P1=10110|01, P2=11001|10 → C1=1011010, C2=1100101\n"
         "Two-Point: Swap middle segment between two cut points.\n"
         "Uniform: Gene-by-gene random selection from parents.\n\n"
         "Step 7 — MUTATION (probability Pm ≈ 0.001-0.01):\n"
         "Randomly alter one or more genes. Maintains diversity, prevents premature convergence.\n"
         "Bit-flip: 10110 → 10010 (bit 3 flipped).\n"
         "Swap mutation: Swap positions of two randomly selected genes.\n\n"
         "Step 8 — REPLACE AND REPEAT:\n"
         "Form new generation. Apply elitism if desired. Go to Step 3.\n\n"
         "APPLYING GA TO TRAVELLING SALESMAN PROBLEM (TSP):\n\n"
         "TSP: Given N cities and distances between them, find the shortest route that visits each city exactly once and returns to the starting city. This is an NP-hard problem with N!/2 possible routes.\n\n"
         "For N=20 cities: 20!/2 ≈ 1.2×10^18 routes — exhaustive search is impossible. GA provides near-optimal solutions efficiently.\n\n"
         "REPRESENTATION FOR TSP:\n"
         "Use PERMUTATION ENCODING — chromosome is an ordering of city numbers.\n"
         "For 5 cities: Chromosome = [3, 1, 4, 2, 5] means visit city 3 first, then 1, then 4, then 2, then 5, and return to 3.\n\n"
         "FITNESS FUNCTION:\n"
         "Fitness = 1 / (total tour length)\n"
         "Total tour length = d(c3,c1) + d(c1,c4) + d(c4,c2) + d(c2,c5) + d(c5,c3)\n"
         "Shorter tour = higher fitness = better solution.\n\n"
         "CROSSOVER FOR TSP — ORDER CROSSOVER (OX):\n"
         "Standard crossover creates INVALID routes (a city visited twice or not at all).\n"
         "Order Crossover (OX) preserves valid permutations:\n"
         "P1: [1, 2 | 3, 4, 5 | 6, 7, 8]\n"
         "P2: [5, 3 | 7, 2, 1 | 8, 4, 6]\n"
         "Child: Copy middle segment from P1: [_, _ | 3, 4, 5 | _, _, _]\n"
         "Fill remaining positions from P2 in order (skipping already included cities):\n"
         "P2 order: 5, 3*, 7, 2, 1*, 8, 4*, 6 (* = already in child)\n"
         "Child = [7, 2, 3, 4, 5, 8, 6, 1]\n\n"
         "MUTATION FOR TSP:\n"
         "Swap Mutation: Randomly swap two city positions in the tour.\n"
         "[3,1,4,2,5] → swap positions 2 and 4 → [3,2,4,1,5]\n"
         "Inversion Mutation: Reverse a random sub-segment of the tour.\n\n"
         "EXAMPLE EXECUTION:\n"
         "5 cities: A, B, C, D, E. Distances given.\n"
         "Generation 0: [A,B,C,D,E]=120km, [A,C,B,E,D]=145km, [A,D,C,B,E]=110km...\n"
         "Fitness: [A,D,C,B,E] is fittest (shortest).\n"
         "After selection+crossover+mutation over 1000 generations: route approaches optimal.\n\n"
         "CONCLUSION:\n"
         "GA provides near-optimal TSP solutions in polynomial time where exact algorithms require exponential time. For 100 cities, exact solution takes trillions of years; GA finds near-optimal in seconds. GA is particularly suited to TSP because: no gradient needed, permutation encoding natural, OX preserves valid tours, and population diversity explores multiple regions of the solution space simultaneously.", C['orange'], C['ol']),
    ]:
        for item in qa(q, marks, years, ans, c, bg): story.append(item)

    story.append(PageBreak())

    # ════════════════════ SECTION 11: UNCERTAINTY ═════════════════════════
    story.append(ban("SECTION 11 — UNCERTAINTY REASONING: BAYESIAN, CF, DEMPSTER-SHAFER", C['maroon']))
    story.append(Spacer(1,0.2*cm))

    for q,marks,years,ans,c,bg in [
        ("Explain Bayesian reasoning in detail. (Asked 2022, 2023 — 10M)",
         "10 Marks — 800–1200 words", "2022, 2023",
         "BAYESIAN REASONING — COMPLETE 10-MARK ANSWER\n\n"
         "INTRODUCTION TO UNCERTAINTY IN AI:\n"
         "Real-world AI systems must make decisions with incomplete, noisy, and uncertain information. Classical logic fails here — it requires complete, certain facts. Bayesian reasoning provides a mathematically principled framework for representing and updating uncertainty based on evidence.\n\n"
         "PROBABILITY FUNDAMENTALS:\n\n"
         "Prior Probability P(H): The probability of hypothesis H before observing any evidence. Based on background knowledge, historical frequency, or expert assessment. Example: P(Disease) = 0.01 (1% of population has this disease).\n\n"
         "Likelihood P(E|H): The probability of observing evidence E given that hypothesis H is true. Represents how well H 'explains' E. Example: P(Positive_Test|Disease) = 0.95.\n\n"
         "Marginal Probability P(E): The total probability of observing evidence E regardless of which hypothesis is true. Computed using the Law of Total Probability.\n\n"
         "Posterior Probability P(H|E): The updated probability of H after observing E. This is what we compute using Bayes' theorem — our updated belief.\n\n"
         "BAYES' THEOREM:\n"
         "P(H|E) = [P(E|H) × P(H)] / P(E)\n"
         "P(E) = P(E|H)·P(H) + P(E|¬H)·P(¬H)   [Law of Total Probability]\n\n"
         "For multiple hypotheses H1,...,Hn:\n"
         "P(Hi|E) = [P(E|Hi) × P(Hi)] / Σj[P(E|Hj) × P(Hj)]\n\n"
         "WORKED EXAMPLE 1 — Medical Test:\n"
         "P(Cancer) = 0.01; P(Positive|Cancer) = 0.90; P(Positive|NoCancer) = 0.09\n"
         "P(Positive) = (0.90×0.01) + (0.09×0.99) = 0.009 + 0.0891 = 0.0981\n"
         "P(Cancer|Positive) = (0.90 × 0.01) / 0.0981 = 0.009/0.0981 ≈ 0.0917 = 9.17%\n"
         "Result: Only 9.17% chance despite positive test! Low prior dominates.\n"
         "This counter-intuitive result demonstrates the BASE RATE FALLACY — people tend to ignore prior probability and overweight the test result.\n\n"
         "WORKED EXAMPLE 2 — Weather Prediction:\n"
         "P(Rain)=0.3; P(Cloudy|Rain)=0.8; P(Cloudy|NRain)=0.4\n"
         "P(Cloudy) = 0.8×0.3 + 0.4×0.7 = 0.24+0.28 = 0.52\n"
         "P(Rain|Cloudy) = (0.8×0.3)/0.52 = 0.24/0.52 ≈ 0.46 = 46%\n"
         "Seeing clouds raises rain probability from 30% to 46%.\n\n"
         "SEQUENTIAL BAYESIAN UPDATING:\n"
         "Posterior after first evidence E1 becomes the prior for second evidence E2:\n"
         "P(H|E1,E2) ∝ P(E2|H) × P(E1|H) × P(H)   [if E1,E2 independent given H]\n"
         "Each new piece of evidence refines our belief incrementally.\n\n"
         "NAIVE BAYES CLASSIFIER:\n"
         "Assumes conditional independence of features given class:\n"
         "P(Class|f1,...,fn) ∝ P(Class) × P(f1|Class) × P(f2|Class) × ... × P(fn|Class)\n"
         "Predicted class = argmax over classes of this product.\n"
         "Application: Spam detection. P(Spam|FREE,MONEY) ∝ 0.4×0.8×0.7=0.224 vs P(Ham|FREE,MONEY)∝0.6×0.1×0.2=0.012. Classify as Spam.\n\n"
         "BAYESIAN NETWORKS:\n"
         "A Bayesian Network is a Directed Acyclic Graph (DAG) where:\n"
         "Nodes = random variables (events, hypotheses)\n"
         "Directed edges = direct causal/probabilistic dependencies\n"
         "Each node has a Conditional Probability Table (CPT): P(node|parents)\n\n"
         "Classic example: B→A←E, A→J, A→M (Burglary-Earthquake-Alarm-JohnCalls-MaryCalls)\n"
         "P(B)=0.001; P(E)=0.002; P(A|B,E)=0.95; P(J|A)=0.90; P(M|A)=0.70\n"
         "Query: P(Burglary|JohnCalls=True, MaryCalls=True) — computed by Bayesian inference.\n\n"
         "Features of Bayesian Networks:\n"
         "1. Compact representation — stores O(n×2^k) instead of O(2^n) probabilities.\n"
         "2. Supports both diagnostic (symptoms→disease) and predictive (cause→effects) inference.\n"
         "3. Handles missing data — unobserved variables are marginalized out.\n"
         "4. Natural representation of causal knowledge.\n\n"
         "ADVANTAGES OF BAYESIAN REASONING:\n"
         "1. Mathematically rigorous — based on probability axioms.\n"
         "2. Incremental updating — new evidence smoothly updates beliefs.\n"
         "3. Optimal decision-making under uncertainty.\n"
         "4. Clear semantics — probabilities are interpretable.\n\n"
         "LIMITATIONS:\n"
         "1. Requires prior probabilities — hard to obtain accurately.\n"
         "2. Computationally expensive for large networks.\n"
         "3. Independence assumptions may not hold.\n\n"
         "APPLICATIONS:\n"
         "Medical diagnosis, spam filtering, fault detection in manufacturing, speech recognition, recommendation systems, forensic analysis, weather forecasting.\n\n"
         "CONCLUSION:\n"
         "Bayesian reasoning is the gold standard for AI decision-making under uncertainty. By combining prior knowledge with observed evidence through Bayes' theorem, AI systems can continuously refine their beliefs as new information arrives, enabling rational decision-making in an uncertain world.", C['maroon'], C['ml']),

        ("Explain Dempster-Shafer Theory of Evidence with derivation. (Asked 2023, 2025 — 5/10M)",
         "10 Marks — 800–1200 words", "2023, 2025",
         "DEMPSTER-SHAFER THEORY — COMPLETE ANSWER\n\n"
         "MOTIVATION:\n"
         "Classical Bayesian probability requires complete knowledge of prior probabilities. When evidence is sparse or ambiguous, it is hard to justify specific probability assignments. Dempster-Shafer (DS) Theory provides a generalization that can handle IGNORANCE explicitly — it doesn't force us to distribute probability when we genuinely don't know.\n\n"
         "DEVELOPMENT:\n"
         "Arthur Dempster (1967) developed the mathematical foundation; Glenn Shafer (1976) gave it the formal framework in 'A Mathematical Theory of Evidence'.\n\n"
         "KEY DEFINITIONS:\n\n"
         "1. Frame of Discernment (Θ):\n"
         "The complete set of all mutually exclusive and exhaustive hypotheses about the domain.\n"
         "Example for disease diagnosis: Θ = {Flu, Cold, COVID, Allergy}\n"
         "Every possible answer to the question must be in Θ.\n\n"
         "2. Power Set 2^Θ:\n"
         "The set of ALL possible subsets of Θ, including ∅ and Θ itself.\n"
         "For Θ = {A, B, C}: 2^Θ = {∅, {A}, {B}, {C}, {A,B}, {A,C}, {B,C}, {A,B,C}}\n"
         "DS theory assigns belief to ANY element of 2^Θ — including multi-element subsets.\n\n"
         "3. Basic Probability Assignment (BPA) / Mass Function m:\n"
         "m: 2^Θ → [0,1] such that:\n"
         "a) m(∅) = 0 (no belief in the empty set)\n"
         "b) Σ m(A) = 1 for all A ⊆ Θ (masses sum to 1)\n\n"
         "Interpretation of m(A):\n"
         "m({Flu}) = 0.5 means: 50% of belief is specifically committed to Flu and NOTHING smaller.\n"
         "m({Flu, Cold}) = 0.3 means: 30% of belief is committed to 'Flu or Cold' but doesn't know which.\n"
         "m(Θ) = 0.2 means: 20% belief is UNASSIGNED — complete ignorance about which hypothesis.\n\n"
         "CRITICAL DIFFERENCE FROM PROBABILITY:\n"
         "In probability: P(Flu) + P(Cold) + P(COVID) + P(Allergy) = 1 exactly.\n"
         "In DS: We can have m({Flu,Cold}) = 0.3 — explicitly saying 'it's one of these two but I don't know which'.\n"
         "Probability forces us to split 0.3 between Flu and Cold (50/50? But we have no basis!). DS lets us keep it as a unit.\n\n"
         "4. Belief Function Bel(A):\n"
         "Bel(A) = Σ m(B) for all B ⊆ A\n"
         "= The total belief COMMITTED to A (sum of masses of all subsets contained within A).\n"
         "= Lower bound on probability of A.\n\n"
         "5. Plausibility Function Pl(A):\n"
         "Pl(A) = Σ m(B) for all B where B ∩ A ≠ ∅\n"
         "= Maximum possible belief in A (sum of masses of all sets not contradicting A).\n"
         "= 1 − Bel(¬A)\n"
         "= Upper bound on probability of A.\n\n"
         "Interval [Bel(A), Pl(A)] = range of possible probability of A.\n"
         "Width = Pl(A) − Bel(A) = degree of IGNORANCE about A.\n\n"
         "WORKED EXAMPLE:\n"
         "Θ = {Cancer(C), Not-Cancer(NC)}\n"
         "Evidence (biopsy result): m({C}) = 0.6, m({NC}) = 0.1, m(Θ) = 0.3\n\n"
         "Bel({C}) = m({C}) = 0.6  [only subset of {C} is {C} itself]\n"
         "Pl({C}) = m({C}) + m(Θ) = 0.6 + 0.3 = 0.9  [sets intersecting {C}: {C} and Θ]\n"
         "Bel({NC}) = m({NC}) = 0.1\n"
         "Pl({NC}) = m({NC}) + m(Θ) = 0.1 + 0.3 = 0.4\n\n"
         "Interpretation: Probability of Cancer lies in [0.6, 0.9]. We're fairly confident (min 60%) but uncertain up to 90%. The 0.3 ignorance mass is why the upper bound is 0.9.\n\n"
         "DEMPSTER'S COMBINATION RULE:\n"
         "When two INDEPENDENT sources provide evidence m1 and m2, combine:\n\n"
         "(m1 ⊕ m2)(A) = Σ{m1(B)·m2(C) | B∩C=A} / (1−K)   for A ≠ ∅\n\n"
         "where K = Σ{m1(B)·m2(C) | B∩C=∅} = CONFLICT between sources\n\n"
         "The denominator (1−K) normalizes away conflicting evidence.\n"
         "If K=1, sources completely contradict → combination undefined.\n\n"
         "COMBINATION EXAMPLE:\n"
         "Source 1 (blood test): m1({C})=0.7, m1(Θ)=0.3\n"
         "Source 2 (imaging): m2({NC})=0.6, m2(Θ)=0.4\n\n"
         "Products:\n"
         "m1({C})×m2({NC}): {C}∩{NC}=∅ → K += 0.7×0.6=0.42 [CONFLICT]\n"
         "m1({C})×m2(Θ): {C}∩Θ={C} → m({C}) += 0.7×0.4=0.28\n"
         "m1(Θ)×m2({NC}): → m({NC}) += 0.3×0.6=0.18\n"
         "m1(Θ)×m2(Θ): → m(Θ) += 0.3×0.4=0.12\n\n"
         "K=0.42, (1−K)=0.58\n"
         "Combined: m({C})=0.28/0.58≈0.483, m({NC})=0.18/0.58≈0.310, m(Θ)=0.12/0.58≈0.207\n\n"
         "Result: Despite conflicting evidence, 48.3% belief in Cancer, 31% in No-Cancer, 20.7% ignorance.\n\n"
         "ADVANTAGES:\n"
         "1. Explicitly models ignorance — m(Θ) represents 'I don't know'.\n"
         "2. Assigns belief to sets — more flexible than single hypotheses.\n"
         "3. No prior probabilities needed.\n"
         "4. Interval [Bel, Pl] gives honest uncertainty range.\n"
         "5. Rigorous mathematical framework for combining multiple independent sources.\n\n"
         "DISADVANTAGES:\n"
         "1. Exponential complexity O(2^n) — impractical for large Θ.\n"
         "2. Zadeh's paradox — produces counter-intuitive results with highly conflicting evidence.\n"
         "3. Difficult to elicit mass assignments from domain experts.\n"
         "4. Sensitive to assumption of independence between sources.\n\n"
         "APPLICATIONS:\n"
         "Sensor fusion, medical diagnosis, target tracking in military systems, forensic evidence combination, fault diagnosis, automated classification with uncertain labels.\n\n"
         "CONCLUSION:\n"
         "DS Theory fills the gap between probabilistic certainty and complete ignorance. It enables AI systems to honestly represent 'I'm not sure' alongside specific beliefs, and to combine evidence from multiple independent sources in a principled way. Though computationally expensive, it remains valuable for applications requiring explicit ignorance modeling.", C['maroon'], C['ml']),
    ]:
        for item in qa(q, marks, years, ans, c, bg): story.append(item)

    story.append(PageBreak())

    # ════════════════════ SECTION 12: LEARNING ════════════════════════════
    story.append(ban("SECTION 12 — LEARNING: STATISTICAL, INDUCTION, EVOLUTIONARY", C['cyan']))
    story.append(Spacer(1,0.2*cm))

    for q,marks,years,ans,c,bg in [
        ("Explain various types of learning strategies with examples. (Asked 2017 — 10M)",
         "10 Marks — 800–1200 words", "2017",
         "LEARNING STRATEGIES IN AI — COMPLETE ANSWER\n\n"
         "INTRODUCTION:\n"
         "Learning is the process by which an AI system improves its performance through experience. Aristotle said 'Learning is an ornament in prosperity, a refuge in adversity, and a provision in old age.' For AI systems, learning enables adaptation, generalization, and improvement without explicit reprogramming. Different learning strategies capture different aspects of how knowledge is acquired.\n\n"
         "1. ROTE LEARNING (Learning by Memorization):\n"
         "The simplest form — directly store every experience and retrieve it when needed. No generalization.\n"
         "Example: Samuel's checker-playing program stored board positions and their evaluations. When a position was encountered again, it retrieved the stored evaluation — faster than recomputing.\n"
         "Advantages: Simple, exact recall. Disadvantages: Requires huge memory, doesn't generalize to new situations.\n\n"
         "2. LEARNING BY ANALOGY:\n"
         "Transfer knowledge from a similar KNOWN situation to a NEW situation by recognizing structural similarity.\n"
         "Example: If you know how to drive a car, you can analogically transfer that knowledge to driving a truck — similar steering, similar pedals, different scale.\n"
         "Process: Find structural mapping between source (known) and target (new). Transfer relevant rules/knowledge. Adapt for differences.\n"
         "Applications: Case-based reasoning, story understanding, learning new programming languages.\n\n"
         "3. INDUCTION LEARNING (Learning from Examples):\n"
         "Generalize from specific positive and negative examples to a rule that covers all positives and excludes all negatives.\n"
         "Example: Given 14 days of weather data (Outlook, Temp, Humidity, Wind) labeled PlayTennis=Yes/No, induce a rule like 'Play tennis if Outlook=Sunny AND Humidity=Normal'.\n"
         "Algorithms: ID3/C4.5 (decision trees), neural networks, rule induction (AQ algorithm).\n"
         "ID3 uses Information Gain = H(S) − Σ(|Sv|/|S|)×H(Sv) to select best splitting feature.\n"
         "Applications: Medical diagnosis, classification problems, game playing.\n\n"
         "4. LEARNING FROM INSTRUCTION (Deductive Learning):\n"
         "Directly told rules or facts by a teacher. The system deductively applies them to new situations.\n"
         "Example: A student reads a textbook. An expert system given rules directly by a knowledge engineer.\n"
         "Advantage: Fast, accurate for what's taught. Disadvantage: Cannot go beyond what was explicitly taught; no generalization.\n\n"
         "5. STATISTICAL LEARNING:\n"
         "Uses statistical models to identify patterns in data. Builds a probabilistic model of the relationship between inputs and outputs.\n"
         "Key algorithms:\n"
         "Linear Regression: Ŷ = β0 + Σβi×xi — predict continuous values.\n"
         "Logistic Regression: P(Y=1) = σ(Xβ) — predict probability of class.\n"
         "Naive Bayes: P(class|features) ∝ P(class)×ΠP(fi|class).\n"
         "SVM: Find maximum-margin hyperplane separating classes.\n"
         "Bias-Variance Tradeoff: Prediction Error = Bias² + Variance + Noise.\n"
         "Applications: Spam detection, medical prognosis, financial forecasting.\n\n"
         "6. REINFORCEMENT LEARNING:\n"
         "Learn by interacting with an environment through REWARDS and PENALTIES. No supervisor — only a scalar reward signal.\n"
         "Example: Teaching a robot to walk: good step → reward. Falling → penalty. After millions of trials, the robot learns an optimal walking policy.\n"
         "Key concepts: Agent, environment, state, action, reward, policy π: state→action, value function V(s).\n"
         "Algorithms: Q-learning, SARSA, Policy Gradient, Deep RL (DQN).\n"
         "Applications: Game playing (AlphaGo, Atari games), robotic control, autonomous driving, recommendation systems.\n\n"
         "7. EVOLUTIONARY LEARNING:\n"
         "Inspired by biological evolution. Maintains a population of candidate solutions, evolves them through selection, crossover, and mutation.\n"
         "Examples: Genetic Algorithms (GA), Genetic Programming (GP), Evolution Strategies.\n"
         "GA: Evolves fixed-length chromosomes. Fitness function evaluates quality. Best for combinatorial optimization.\n"
         "GP: Evolves variable-length program trees. Best for symbolic regression and automatic programming.\n"
         "Applications: Optimization problems, neural architecture search, strategy evolution.\n\n"
         "8. UNSUPERVISED LEARNING:\n"
         "No labels — discover hidden structure in unlabeled data.\n"
         "Clustering: Group similar examples (K-means, DBSCAN).\n"
         "Dimensionality Reduction: Compress features (PCA, t-SNE, Autoencoders).\n"
         "Generative Models: Learn data distribution (GANs, VAEs).\n"
         "Applications: Customer segmentation, anomaly detection, data compression, feature learning.\n\n"
         "COMPARISON TABLE:\n"
         "Rote: No generalization, exact recall, huge memory.\n"
         "Analogy: Transfers from similar problem, flexible but structure-matching required.\n"
         "Induction: From examples to rules, general but may be wrong (not guaranteed).\n"
         "Statistical: Data-driven, probabilistic, requires large datasets.\n"
         "Reinforcement: Trial and error, slow but learns complex behaviors.\n"
         "Evolutionary: Population-based, global search, good for complex optimization.\n\n"
         "CONCLUSION:\n"
         "No single learning strategy is universally best. Induction is best when labeled examples are plentiful. Statistical learning excels for pattern recognition in large datasets. Reinforcement learning handles sequential decision-making. Evolutionary methods solve complex optimization. Modern AI systems (like deep reinforcement learning in AlphaGo) combine multiple strategies to achieve superhuman performance.", C['cyan'], C['cl']),
    ]:
        for item in qa(q, marks, years, ans, c, bg): story.append(item)

    story.append(PageBreak())

    # ════════════════════ SECTION 13: LOGIC & INFERENCE ═══════════════════
    story.append(ban("SECTION 13 — LOGIC & INFERENCE: RESOLUTION, TABLEAUX, PROOF", C['dark']))
    story.append(Spacer(1,0.2*cm))

    for q,marks,years,ans,c,bg in [
        ("Show that (~W∨R) is a logical consequence of {~P∨Q, ~Q∨R, ~W∨P} using resolution refutation. (Asked 2022, 2025 — 5M)",
         "5 Marks — 500–800 words", "2022, 2025",
         "RESOLUTION REFUTATION PROOF\n\n"
         "GOAL: Prove (¬W ∨ R) from {¬P∨Q, ¬Q∨R, ¬W∨P}\n\n"
         "BACKGROUND — RESOLUTION METHOD:\n"
         "Resolution is a complete and sound inference rule for propositional and first-order logic. To prove that a formula G is a logical consequence of a set of premises S:\n"
         "1. NEGATE the goal G → ¬G.\n"
         "2. Add ¬G to the premise set S.\n"
         "3. Convert all formulas to CNF (Conjunctive Normal Form).\n"
         "4. Apply the resolution rule repeatedly: from (A∨B) and (¬A∨C), derive (B∨C).\n"
         "5. If we derive the EMPTY CLAUSE (□) — a contradiction — then ¬G is inconsistent with S, so G is provable. QED.\n\n"
         "STEP 1 — NEGATE THE GOAL:\n"
         "Goal: (¬W ∨ R)\n"
         "Negation: ¬(¬W ∨ R) = W ∧ ¬R   [De Morgan's law]\n"
         "This gives two unit clauses: {W} and {¬R}\n\n"
         "STEP 2 — COMPLETE CLAUSE SET:\n"
         "Clause 1: ¬P ∨ Q      [premise 1]\n"
         "Clause 2: ¬Q ∨ R      [premise 2]\n"
         "Clause 3: ¬W ∨ P      [premise 3]\n"
         "Clause 4: W            [from negated goal, part 1]\n"
         "Clause 5: ¬R           [from negated goal, part 2]\n\n"
         "STEP 3 — APPLY RESOLUTION RULE SYSTEMATICALLY:\n\n"
         "Resolution 1: Resolve Clause 3 (¬W ∨ P) with Clause 4 (W):\n"
         "   Complementary pair: W and ¬W\n"
         "   Resolvent: P\n"
         "   → New Clause 6: P\n\n"
         "Resolution 2: Resolve Clause 1 (¬P ∨ Q) with Clause 6 (P):\n"
         "   Complementary pair: P and ¬P\n"
         "   Resolvent: Q\n"
         "   → New Clause 7: Q\n\n"
         "Resolution 3: Resolve Clause 2 (¬Q ∨ R) with Clause 7 (Q):\n"
         "   Complementary pair: Q and ¬Q\n"
         "   Resolvent: R\n"
         "   → New Clause 8: R\n\n"
         "Resolution 4: Resolve Clause 8 (R) with Clause 5 (¬R):\n"
         "   Complementary pair: R and ¬R\n"
         "   Resolvent: □ (EMPTY CLAUSE)\n\n"
         "STEP 4 — CONCLUSION:\n"
         "We have derived the empty clause □.\n"
         "This represents a CONTRADICTION — our assumption that ¬(¬W∨R) is consistent with the premises is FALSE.\n"
         "Therefore: (¬W ∨ R) IS a logical consequence of {¬P∨Q, ¬Q∨R, ¬W∨P}. QED ✓\n\n"
         "PROOF CHAIN SUMMARY:\n"
         "Clause 3 + Clause 4 → Clause 6 (P)\n"
         "Clause 1 + Clause 6 → Clause 7 (Q)\n"
         "Clause 2 + Clause 7 → Clause 8 (R)\n"
         "Clause 8 + Clause 5 → □ CONTRADICTION\n\n"
         "INTUITIVE EXPLANATION:\n"
         "Starting from W (assumed from negated goal):\n"
         "W is true → (¬W∨P) forces P to be true.\n"
         "P is true → (¬P∨Q) forces Q to be true.\n"
         "Q is true → (¬Q∨R) forces R to be true.\n"
         "But we also assumed ¬R (from negated goal). Contradiction!\n"
         "So the negation of our goal is impossible → the goal (¬W∨R) must be true.", C['dark'], C['acc']),

        ("Consider {~(P∨Q), (Q∨R), ~(~P∧R)}. Show the set is inconsistent using semantic tableau. (Asked 2022 — 5M)",
         "5 Marks — 500–800 words", "2022",
         "SEMANTIC TABLEAU — INCONSISTENCY PROOF\n\n"
         "GOAL: Show that {¬(P∨Q), (Q∨R), ¬(¬P∧R)} is INCONSISTENT (all three cannot be simultaneously true).\n\n"
         "SEMANTIC TABLEAU METHOD:\n"
         "The semantic tableau (truth tree) method checks satisfiability by systematically analyzing cases. For inconsistency, we show that every possible assignment of truth values leads to a contradiction (closed branch).\n\n"
         "TABLEAU RULES:\n"
         "For conjunctive formulas (α-formulas): Both parts must hold (no branching).\n"
         "For disjunctive formulas (β-formulas): Create two branches (one for each disjunct).\n\n"
         "α-rules (no branching):\n"
         "¬(P∨Q) → ¬P AND ¬Q\n"
         "¬(¬P∧R) → ¬(¬P) OR ¬R = P OR ¬R\n\n"
         "β-rules (branching):\n"
         "Q∨R → branch on Q | branch on ¬Q with R\n"
         "P∨¬R → branch on P | branch on ¬R\n\n"
         "STEP-BY-STEP TABLEAU CONSTRUCTION:\n\n"
         "Start with all three formulas:\n"
         "(1) ¬(P∨Q)    [Premise 1]\n"
         "(2) Q∨R       [Premise 2]\n"
         "(3) ¬(¬P∧R)   [Premise 3]\n\n"
         "Apply α-rule to (1): ¬(P∨Q) decomposes to:\n"
         "(4) ¬P         [from 1]\n"
         "(5) ¬Q         [from 1]\n\n"
         "Now we have: ¬P, ¬Q on all branches.\n\n"
         "Apply β-rule to (2): Q∨R branches:\n"
         "LEFT BRANCH: Q\n"
         "RIGHT BRANCH: R (since ¬Q already forces R to make Q∨R true)\n\n"
         "LEFT BRANCH ANALYSIS:\n"
         "We have: ¬P, ¬Q, Q\n"
         "¬Q and Q are CONTRADICTORY. LEFT BRANCH CLOSES (✗)\n\n"
         "RIGHT BRANCH ANALYSIS:\n"
         "We have: ¬P, ¬Q, R\n\n"
         "Apply β-rule to (3): ¬(¬P∧R) = P ∨ ¬R. Branch on this:\n\n"
         "RIGHT-LEFT SUB-BRANCH: P\n"
         "We have: ¬P, ¬Q, R, P\n"
         "¬P and P are CONTRADICTORY. RIGHT-LEFT BRANCH CLOSES (✗)\n\n"
         "RIGHT-RIGHT SUB-BRANCH: ¬R\n"
         "We have: ¬P, ¬Q, R, ¬R\n"
         "R and ¬R are CONTRADICTORY. RIGHT-RIGHT BRANCH CLOSES (✗)\n\n"
         "CONCLUSION:\n"
         "ALL branches of the tableau are CLOSED (every branch has a contradiction).\n"
         "Therefore, there is NO truth assignment that satisfies all three formulas simultaneously.\n"
         "The set {¬(P∨Q), (Q∨R), ¬(¬P∧R)} is INCONSISTENT (unsatisfiable). QED ✓\n\n"
         "SUMMARY:\n"
         "Root: {¬(P∨Q), Q∨R, ¬(¬P∧R)}\n"
         "→ Decompose ¬(P∨Q): get ¬P, ¬Q\n"
         "→ Branch on Q∨R: Left=Q (closes with ¬Q), Right=R\n"
         "→ Right branch, branch on P∨¬R: Left=P (closes with ¬P), Right=¬R (closes with R)\n"
         "All 3 branches closed → INCONSISTENT ✓", C['dark'], C['acc']),

        ("What is Alpha-Beta Pruning? Explain. (Asked 2018 — 1.5M)",
         "1.5 Marks — 100 words", "2018",
         "Alpha-Beta Pruning is an optimization of the Minimax search algorithm for two-player game trees. It prunes branches that cannot possibly affect the final decision, dramatically reducing the number of nodes evaluated.\n\n"
         "Alpha (α): The BEST value that the MAXIMIZER can guarantee so far.\n"
         "Beta (β): The BEST value that the MINIMIZER can guarantee so far.\n\n"
         "Pruning rule:\n"
         "At MAX node: if α ≥ β → prune remaining children (they won't affect outcome).\n"
         "At MIN node: if β ≤ α → prune remaining children.\n\n"
         "Effect: Reduces complexity from O(b^m) to O(b^(m/2)) with perfect ordering — allows searching TWICE as deep in the same time. Used in chess, checkers, Go.", C['dark'], C['acc']),
    ]:
        for item in qa(q, marks, years, ans, c, bg): story.append(item)

    story.append(PageBreak())

    # ════════════════════ SECTION 14: MISCELLANEOUS ════════════════════════
    story.append(ban("SECTION 14 — MISCELLANEOUS: NLP, PLANNING, REASONING, THEMATIC FRAMES", C['brown']))
    story.append(Spacer(1,0.2*cm))

    for q,marks,years,ans,c,bg in [
        ("Represent statements using Thematic Role Frame. (Asked 2018, 2023 — 1.5M)",
         "1.5 Marks — 100 words", "2018, 2023",
         "Thematic Role Frames represent sentence structure by identifying SEMANTIC ROLES of each participant in an event.\n\n"
         "Statement 1: 'The cookies were eaten in the kitchen under the table by the baker.'\n"
         "EVENT: Eat\n"
         "AGENT (doer): Baker\n"
         "OBJECT (thing acted on): Cookies\n"
         "LOCATION: Kitchen\n"
         "POSITION: Under the table\n\n"
         "Statement 2: 'Seema is sitting on a wooden stool by a window.'\n"
         "EVENT: Sit\n"
         "AGENT: Seema\n"
         "LOCATION: On a wooden stool\n"
         "CO-LOCATION: By a window\n\n"
         "Statement 3: 'Suzie told Robbie to put wedge on the red block.'\n"
         "EVENT: Tell\n"
         "AGENT: Suzie | OBJECT: Robbie\n"
         "EMBEDDED EVENT: Put | AGENT: Robbie | OBJECT: Wedge | DESTINATION: On red block", C['brown'], C['bl']),

        ("What is NLP? Also explain Transformational Grammar. (Asked 2018 — 5M)",
         "5 Marks — 500–800 words", "2018",
         "NLP AND TRANSFORMATIONAL GRAMMAR\n\n"
         "WHAT IS NLP (Natural Language Processing):\n"
         "Natural Language Processing (NLP) is a branch of AI that deals with the interaction between computers and human language. It enables computers to understand, interpret, generate, and respond to human language (text and speech) in a way that is both meaningful and useful.\n\n"
         "NLP CHALLENGES:\n"
         "1. Ambiguity: 'I saw the man with the telescope' — Did I use the telescope to see him, or did he have a telescope?\n"
         "2. Context Dependence: 'Bank' means different things in different contexts.\n"
         "3. Informal Language: Slang, abbreviations, typos.\n"
         "4. Coreference: 'John fell. He cried.' — 'He' refers to John.\n"
         "5. Idioms: 'It's raining cats and dogs' has no literal meaning.\n\n"
         "NLP LEVELS OF ANALYSIS:\n"
         "1. Phonological Analysis: Analysis of sounds in language.\n"
         "2. Morphological Analysis: Structure of words (prefixes, suffixes, roots).\n"
         "3. Lexical Analysis: Word meanings (POS tagging, word sense disambiguation).\n"
         "4. Syntactic Analysis (Parsing): Grammatical structure of sentences.\n"
         "5. Semantic Analysis: Meaning of sentences.\n"
         "6. Pragmatic Analysis: Context and intent behind communication.\n"
         "7. Discourse Analysis: Meaning across multiple sentences.\n\n"
         "APPLICATIONS OF NLP:\n"
         "Machine translation (Google Translate), speech recognition (Siri), information extraction, question answering, text summarization, sentiment analysis, chatbots (ChatGPT), spell checking.\n\n"
         "TRANSFORMATIONAL GRAMMAR (Chomsky, 1957):\n"
         "Transformational-Generative Grammar is a theory of language structure proposed by Noam Chomsky. It proposes that sentences have two levels of structure:\n\n"
         "1. Deep Structure (D-Structure):\n"
         "The UNDERLYING, abstract logical/semantic meaning of a sentence — the 'idea' before words are chosen. Example: Both 'John loves Mary' and 'Mary is loved by John' have the SAME deep structure (John is the agent of loving Mary), but different surface structures.\n\n"
         "2. Surface Structure (S-Structure):\n"
         "The ACTUAL word sequence as spoken or written. The surface structure is derived from the deep structure by applying TRANSFORMATIONAL RULES.\n\n"
         "TRANSFORMATIONAL RULES:\n"
         "Rules that convert deep structure to surface structure by rearranging, adding, or deleting elements:\n\n"
         "a) Passive Transformation:\n"
         "Deep: 'John eats the apple'\n"
         "Surface (passive): 'The apple is eaten by John'\n"
         "Transformation: Move object to front, add 'is...by', change verb to past participle.\n\n"
         "b) Question Transformation:\n"
         "Deep: 'John is eating'\n"
         "Surface (question): 'Is John eating?'\n"
         "Transformation: Move auxiliary verb to front.\n\n"
         "c) Negation Transformation:\n"
         "Deep: 'John eats'\n"
         "Surface (negative): 'John does not eat'\n\n"
         "PHRASE STRUCTURE RULES (Context-Free Grammar):\n"
         "S → NP + VP\n"
         "NP → Det + N | NP + PP\n"
         "VP → V + NP | VP + PP\n"
         "PP → P + NP\n\n"
         "SIGNIFICANCE IN NLP:\n"
         "Transformational grammar provided the theoretical foundation for:\n"
         "1. Syntactic parsers in NLP systems.\n"
         "2. Machine translation (map deep structures across languages).\n"
         "3. Semantic analysis — deep structure reveals true meaning.\n"
         "4. Question-answering systems.\n\n"
         "CONCLUSION:\n"
         "NLP enables computers to process human language, which is inherently ambiguous and context-dependent. Transformational grammar provides a formal framework for understanding the relationship between sentence surface form and underlying meaning, which is crucial for building systems that can genuinely understand language rather than just pattern-match on words.", C['brown'], C['bl']),

        ("Differentiate between Database and Knowledge Base. (Asked 2024 — 1.5M)",
         "1.5 Marks — 100 words", "2024",
         "Database vs Knowledge Base:\n\n"
         "DATABASE: Organized collection of structured data (tables, records). Answers 'what are the facts?' — stores raw data. No reasoning capability. Uses SQL queries. Data is precise and well-defined. Example: Student records (ID, Name, Marks).\n\n"
         "KNOWLEDGE BASE: Stores both facts AND rules, relationships, and reasoning mechanisms. Answers 'what can be inferred?' — supports intelligent queries. Has inference capability. Uses logic/frames/rules. Knowledge may be uncertain or incomplete.\n\n"
         "Key distinction: Database retrieves stored data. Knowledge base DERIVES new information through reasoning. Example: KB can infer 'Socrates is mortal' from 'all humans are mortal' + 'Socrates is human'.", C['brown'], C['bl']),

        ("Define Stochastic Annealing (Simulated Annealing). (Asked 2023 — 1.5M)",
         "1.5 Marks — 100 words", "2023",
         "Stochastic/Simulated Annealing is a probabilistic optimization algorithm inspired by the metallurgical process of annealing (slowly cooling hot metal to find low-energy crystal structure). It extends hill climbing by allowing occasional DOWNHILL moves (worse solutions) to escape local optima.\n\n"
         "Key mechanism: Accept worse solution with probability P = e^(ΔE/T) where T is the 'temperature' parameter that decreases over time. High T → many bad moves accepted (exploration). Low T → few bad moves (exploitation).\n\n"
         "Cooling schedule: T = α×T at each step (geometric cooling, α≈0.95). As T→0, behavior approaches hill climbing. Theoretically finds global optimum with slow enough cooling.", C['brown'], C['bl']),
    ]:
        for item in qa(q, marks, years, ans, c, bg): story.append(item)

    story.append(PageBreak())

    # ════════════════════ FINAL REVISION ══════════════════════════════════
    story.append(ban("FINAL REVISION — HIGH-PROBABILITY QUESTIONS BY YEAR", C['navy']))
    story.append(Spacer(1,0.2*cm))
    story.append(ibox("Study these first — they have appeared in 3+ exam papers.",
                      C['gl'], C['green']))
    story.append(Spacer(1,0.2*cm))

    freq = ctab([
        ["QUESTION","APPEARED IN","MARKS","SECTION"],
        ["ANN vs Biological Neuron / ANN Architecture","2018,2022,2023,2024,2025","5-10M","Sec 2"],
        ["Backpropagation — algorithm, advantages, disadvantages","2022,2024,2025","10M","Sec 3"],
        ["A* Algorithm — explain, vs Hill Climbing, why optimal","2017,2018,2022,2023,2025","5-10M","Sec 7"],
        ["BFS, DFS, IDDFS — compare, explain, complexity","2017,2018,2022,2023,2024","5-15M","Sec 6"],
        ["Genetic Algorithm — steps, operators, applications","2017,2018,2022,2023,2024,2025","5-10M","Sec 10"],
        ["Bayesian Reasoning — Bayes theorem with example","2017,2018,2022,2023,2024","5-10M","Sec 11"],
        ["Expert System — architecture, forward/backward chaining","2017,2018,2022,2023,2024,2025","5-15M","Sec 9"],
        ["Semantic Nets + Frames — short notes","2018,2022,2023,2024,2025","5-15M","Sec 8"],
        ["Blackboard Architecture — diagram + components","2022,2023,2024,2025","5M","Sec 8"],
        ["Fuzzy Logic — operations, core, support, membership","2018,2022,2023,2024,2025","5-7M","Sec 5"],
        ["Dempster-Shafer Theory","2018,2023,2024,2025","5-10M","Sec 11"],
        ["Resolution Refutation — prove logical consequence","2018,2022,2025","5M","Sec 13"],
        ["Induction and Statistical Learning","2017,2022,2023,2024","5-10M","Sec 12"],
        ["RNN — preferred in AI, layers, disadvantages","2022,2024,2025","5-10M","Sec 4"],
        ["Semantic Tableaux — inconsistency/validity proof","2022,2025","5M","Sec 13"],
    ],[7*cm,4*cm,2.5*cm,W-2.8*cm-13.5*cm], C['navy'],
    [C['acc'],C['gl'],C['ol'],C['pl'],C['rl'],C['yl'],C['tl'],C['bl'],
     C['acc'],C['gl'],C['ol'],C['pl'],C['rl'],C['yl'],C['tl']])
    story.append(freq)
    story.append(Spacer(1,0.3*cm))
    story.append(ibox(
        "🎯  EXAM STRATEGY:\n"
        "Part A (1.5M each, 10 questions — ALL compulsory):\n"
        "Write 2-3 crisp sentences. Start with definition. Add one key fact/formula. One example if space allows.\n\n"
        "Part B (15M each, answer any 4 from 6):\n"
        "Choose questions you know completely. Write structured answers with: Introduction → Main Content → Examples → Conclusion.\n"
        "Safe choices: Q on ANN/Backprop + Q on Search (A*/BFS) + Q on KR (Sem Nets/Expert System) + Q on Uncertainty (Bayesian/DS).\n\n"
        "Time Management: Part A = 30 min. Each Part B question = 25-30 min. Total = 30 + 4×27 = 138 min out of 180 min.",
        C['gl'], C['teal']))

    return story

def main():
    out = "IS_All_PYQ_Complete_Answers.pdf"
    doc = SimpleDocTemplate(out, pagesize=A4,
        rightMargin=1.3*cm, leftMargin=1.3*cm,
        topMargin=1.3*cm, bottomMargin=1.3*cm,
        title="IS — All Previous Year Questions with Complete Answers")

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(HexColor('#9e9e9e'))
        canvas.drawString(1.3*cm, 0.6*cm, "IS PCC-CS-601 | Complete PYQ Answers | YMCA University")
        canvas.drawRightString(W-1.3*cm, 0.6*cm, f"Page {doc.page}")
        canvas.restoreState()

    doc.build(build(), onFirstPage=footer, onLaterPages=footer)
    print(f"Done: {out}")

if __name__ == "__main__":
    main()