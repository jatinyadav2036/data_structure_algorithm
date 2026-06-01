from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, HRFlowable)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

W, H = A4

C = {
    'navy': HexColor('#0d1b2a'), 'dark': HexColor('#1a237e'),
    'blue': HexColor('#283593'), 'teal': HexColor('#004d40'),
    'tl':   HexColor('#e0f2f1'), 'green': HexColor('#1b5e20'),
    'gl':   HexColor('#e8f5e9'), 'purple': HexColor('#4a148c'),
    'pl':   HexColor('#f3e5f5'), 'orange': HexColor('#e65100'),
    'ol':   HexColor('#fff3e0'), 'red': HexColor('#b71c1c'),
    'rl':   HexColor('#fce4ec'), 'maroon': HexColor('#880e4f'),
    'ml':   HexColor('#fce4ec'), 'brown': HexColor('#4e342e'),
    'bl':   HexColor('#efebe9'), 'yl':  HexColor('#fffde7'),
    'gy':   HexColor('#f5f5f5'), 'dk':  HexColor('#212121'),
    'md':   HexColor('#424242'), 'acc': HexColor('#e8eaf6'),
    'cyan': HexColor('#006064'), 'cl':  HexColor('#e0f7fa'),
}

def mk():
    s = {}
    def p(n, **kw):
        d = dict(fontName='Helvetica', fontSize=10.5, textColor=C['dk'],
                 leading=16, spaceAfter=5, alignment=TA_JUSTIFY)
        d.update(kw); s[n] = ParagraphStyle(n, **d)
    p('ct', fontName='Helvetica-Bold', fontSize=22, textColor=white,
      alignment=TA_CENTER, leading=30, spaceAfter=8)
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
    p('note', fontName='Helvetica-Oblique', fontSize=10, textColor=C['purple'],
      leading=14, spaceAfter=5, leftIndent=8)
    p('form', fontName='Helvetica-Bold', fontSize=11, textColor=C['purple'],
      alignment=TA_CENTER, leading=18, spaceAfter=5, spaceBefore=4)
    p('qm',  fontName='Helvetica-Bold', fontSize=10, textColor=white,
      alignment=TA_LEFT, leading=14, leftIndent=6)
    p('th',  fontName='Helvetica-Bold', fontSize=9.5, textColor=white,
      alignment=TA_CENTER, leading=13)
    p('td',  fontSize=9.5, leading=14, spaceAfter=3, alignment=TA_JUSTIFY)
    return s

S = mk()

def ban(t, c):
    x = Table([[Paragraph(t, S['ban'])]], colWidths=[W-2.8*cm])
    x.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),c),
        ('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9),
        ('LEFTPADDING',(0,0),(-1,-1),14)]))
    return x

def fbox(t, bg=None, bd=None):
    bg = bg or C['pl']; bd = bd or C['purple']
    x = Table([[Paragraph(t, S['form'])]], colWidths=[W-2.8*cm])
    x.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),bg),
        ('BOX',(0,0),(-1,-1),1.5,bd),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
    return x

def ibox(t, bg=None, bd=None):
    bg = bg or C['ol']; bd = bd or C['orange']
    x = Table([[Paragraph(t, S['body'])]], colWidths=[W-2.8*cm])
    x.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),bg),
        ('BOX',(0,0),(-1,-1),1.2,bd),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12)]))
    return x

def ctab(rows, widths, hc, rbgs=None):
    built = []
    for i, row in enumerate(rows):
        sty = S['th'] if i == 0 else S['td']
        built.append([Paragraph(str(c), sty) for c in row])
    t = Table(built, colWidths=widths)
    cmds = [('BACKGROUND',(0,0),(-1,0),hc),
            ('GRID',(0,0),(-1,-1),0.5,HexColor('#bdbdbd')),
            ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
            ('LEFTPADDING',(0,0),(-1,-1),7),('VALIGN',(0,0),(-1,-1),'MIDDLE')]
    if rbgs:
        for i, bg in enumerate(rbgs, 1):
            if i < len(built): cmds.append(('BACKGROUND',(0,i),(-1,i),bg))
    t.setStyle(TableStyle(cmds)); return t

def qa(q_text, marks, years, answer, color, topic_bg=None):
    items = []
    topic_bg = topic_bg or C['gy']
    qs = ParagraphStyle('qsh', fontName='Helvetica-Bold', fontSize=11,
                        textColor=white, leading=15, spaceAfter=0,
                        spaceBefore=0, leftIndent=8, backColor=color)
    items.append(Spacer(1, 0.15*cm))
    qh = Table([[Paragraph(f"Q  [{marks}]  {q_text}", qs)]], colWidths=[W-2.8*cm])
    qh.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),color),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',(0,0),(-1,-1),10)]))
    items.append(qh)
    yt = Table([[Paragraph(f"  📅 Asked in: {years}  |  Word limit: {marks}",
                           ParagraphStyle('yt', fontName='Helvetica-Oblique', fontSize=9,
                           textColor=C['maroon'], leading=12, leftIndent=6))]],
               colWidths=[W-2.8*cm])
    yt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),C['yl']),
        ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
        ('LEFTPADDING',(0,0),(-1,-1),8)]))
    items.append(yt)
    as_ = ParagraphStyle('ans_', fontName='Helvetica', fontSize=10.3,
                         textColor=C['dk'], leading=16, spaceAfter=4,
                         leftIndent=10, alignment=TA_JUSTIFY, backColor=topic_bg)
    items.append(Paragraph("<b>✍ Answer:</b>", ParagraphStyle('ah',
        fontName='Helvetica-Bold', fontSize=10, textColor=C['teal'],
        leading=13, spaceBefore=4, spaceAfter=2, leftIndent=10, backColor=topic_bg)))
    items.append(Paragraph(answer.replace('\n', '<br/>'), as_))
    items.append(HRFlowable(width="100%", thickness=0.8, color=HexColor('#e0e0e0'), spaceAfter=3))
    return items

# ════════════════════════════════════════════════════════════════════════════
def build():
    story = []

    # COVER
    cov = Table([
        [Paragraph("INTELLIGENT SYSTEMS — PCC-CS-601", S['ct'])],
        [Paragraph("YMCA University Faridabad | B.Tech 6th Semester", S['cs'])],
        [Spacer(1, 0.3*cm)],
        [Paragraph("COMPLETE PYQ ANSWER BOOK — PART 2", ParagraphStyle('cm',
            fontName='Helvetica-Bold', fontSize=18, textColor=HexColor('#ffd54f'),
            alignment=TA_CENTER, leading=24))],
        [Paragraph("2023  •  2024  •  2025  — ALL Questions with Full Answers", S['cs'])],
        [Spacer(1, 0.3*cm)],
        [Paragraph("Every Part-A (1.5M) and Part-B (5M/10M/15M) question answered in full",
                   ParagraphStyle('wl', fontName='Helvetica-Oblique', fontSize=10,
                   textColor=HexColor('#90a4ae'), alignment=TA_CENTER, leading=15))],
        [Paragraph("Word Limits: 1.5M=100 words | 5M=500-800 | 10M=800-1200 | 15M=1200-1500",
                   ParagraphStyle('wl2', fontName='Helvetica-Oblique', fontSize=10,
                   textColor=HexColor('#80cbc4'), alignment=TA_CENTER, leading=15))],
    ], colWidths=[W-2*cm])
    cov.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),C['navy']),
        ('TOPPADDING',(0,0),(-1,-1),18),('BOTTOMPADDING',(0,0),(-1,-1),18),
        ('BOX',(0,0),(-1,-1),3,HexColor('#546e7a'))]))
    story += [Spacer(1, 0.8*cm), cov, Spacer(1, 0.5*cm)]

    # ════════════════ 2025 EXAM ════════════════════════════════════════════
    story.append(ban("MAY 2025 EXAM — COMPLETE PAPER WITH ALL ANSWERS", C['dark']))
    story.append(Spacer(1, 0.2*cm))
    story.append(ibox("Paper Code: 003601 | May 2025 | B.Tech 6th Sem | Max Marks: 75 | Time: 3 Hrs\n"
                      "Part A: All 10 questions compulsory (1.5 marks each) | Part B: Any 4 from 6",
                      C['acc'], C['dark']))
    story.append(Spacer(1, 0.2*cm))

    story.append(ban("2025 — PART A (1.5 Marks Each — 100 Words)", C['teal']))
    story.append(Spacer(1, 0.1*cm))

    for q, years, c, ans in [
        ("(a) What are the application areas of an intelligent system?",
         "2025 Part A", C['teal'],
         "Application areas of Intelligent Systems:\n"
         "1. Medical Diagnosis: Disease detection, drug discovery, patient monitoring (MYCIN, Watson Health).\n"
         "2. Natural Language Processing: Machine translation, speech recognition, chatbots (Siri, Alexa).\n"
         "3. Robotics: Industrial automation, surgical robots, autonomous vehicles (Tesla, Boston Dynamics).\n"
         "4. Expert Systems: Legal advisory, financial planning, fault diagnosis.\n"
         "5. Computer Vision: Face recognition, object detection, medical imaging.\n"
         "6. Game Playing: Chess (Deep Blue), Go (AlphaGo), video game AI.\n"
         "7. Education: Intelligent tutoring systems, personalized learning.\n"
         "8. Finance: Fraud detection, stock prediction, algorithmic trading.\n"
         "9. Manufacturing: Quality control, predictive maintenance.\n"
         "10. Smart Home: IoT devices, home automation, energy management."),

        ("(b) What are the different types of learning in ANN?",
         "2025 Part A", C['teal'],
         "Types of Learning in ANN:\n\n"
         "1. Supervised Learning: Network trained with labeled input-output pairs. Error = target − output. Adjust weights using backpropagation. Used for classification and regression. Example: Digit recognition.\n\n"
         "2. Unsupervised Learning: No labels — network discovers hidden patterns in data. Used for clustering and feature extraction. Example: Self-Organizing Maps (SOM), Autoencoders.\n\n"
         "3. Reinforcement Learning: Agent learns through trial and error — receives rewards for correct actions, penalties for wrong ones. Learns optimal policy. Example: Robot learning to walk.\n\n"
         "4. Hebbian Learning: 'Neurons that fire together, wire together.' Strengthens connections between simultaneously active neurons.\n\n"
         "5. Competitive Learning: Neurons compete — only the winner (most activated) updates its weights."),

        ("(c) Explain the terms Core and Height of a fuzzy set.",
         "2025 Part A", C['teal'],
         "Core and Height of a Fuzzy Set:\n\n"
         "For fuzzy set A on universe X with membership function μ_A(x):\n\n"
         "CORE: The set of ALL elements that have FULL membership (μ = 1).\n"
         "Core(A) = {x ∈ X | μ_A(x) = 1}\n"
         "Example: For fuzzy set TALL, Core = {all heights ≥ 6'4\"} where μ = 1.0.\n\n"
         "HEIGHT: The MAXIMUM membership value of any element in the fuzzy set.\n"
         "Height(A) = max{μ_A(x) | x ∈ X}\n"
         "Example: If maximum membership in set A is 0.9, then Height(A) = 0.9.\n\n"
         "NORMAL fuzzy set: Height = 1 (at least one element has full membership).\n"
         "SUBNORMAL fuzzy set: Height < 1 (no element reaches full membership)."),

        ("(d) Explain how IDDFS is better than BFS or DFS.",
         "2025 Part A", C['teal'],
         "IDDFS combines the BEST of BFS and DFS:\n\n"
         "BFS Problems: Complete + Optimal but needs O(b^d) memory — exponential! For b=10, d=10: stores 10 billion nodes.\n\n"
         "DFS Problems: Only O(b·m) memory but NOT complete (can loop) and NOT optimal (finds deepest, not shortest solution).\n\n"
         "IDDFS Solution: Runs DFS with increasing depth limits L=0,1,2,...\n"
         "Complete: YES (like BFS) | Optimal: YES (like BFS) | Space: O(b·d) (like DFS!)\n"
         "Time: O(b^d) — same as BFS asymptotically, with only ~11% overhead from re-expansion.\n\n"
         "IDDFS is the BEST general-purpose uninformed search: complete, optimal, and memory-efficient."),

        ("(e) Explain the Water-Jug Problem.",
         "2025 Part A", C['teal'],
         "Water-Jug Problem:\n\n"
         "Setup: Two jugs — 4-liter (J1) and 3-liter (J2). Neither has markings. Goal: Measure exactly 2 liters in J1.\n\n"
         "State representation: (x, y) where x = water in J1 (0-4), y = water in J2 (0-3).\n"
         "Initial state: (0, 0). Goal state: (2, y) for any y.\n\n"
         "Operators: Fill J1, Fill J2, Empty J1, Empty J2, Pour J1→J2, Pour J2→J1.\n\n"
         "Solution path:\n"
         "(0,0) → Fill J2 → (0,3) → Pour J2→J1 → (3,0) → Fill J2 → (3,3) → Pour J2→J1 → (4,2) → Empty J1 → (0,2) → Pour J2→J1 → (2,0) ✓\n\n"
         "This is a STATE SPACE SEARCH problem — BFS or DFS finds the optimal solution path."),

        ("(f) Discuss the various ways of knowledge representation.",
         "2025 Part A", C['teal'],
         "Ways of Knowledge Representation in AI:\n\n"
         "1. Logical Representation: Propositional Logic (TRUE/FALSE propositions) and FOPL (predicates, quantifiers ∀, ∃, variables). Example: ∀x[Human(x)→Mortal(x)].\n\n"
         "2. Semantic Networks: Directed labeled graph. Nodes=concepts, Arcs=relationships (IS-A, HAS-A, CAN). Supports inheritance.\n\n"
         "3. Frames: Slot-value structures for stereotyped objects. Supports defaults, inheritance, demons.\n\n"
         "4. Production Rules: IF-THEN rules. Example: IF fever AND cough THEN flu.\n\n"
         "5. Scripts: Event sequence templates. Example: Restaurant script.\n\n"
         "6. Conceptual Graphs: Formal extension of semantic nets with logic semantics."),

        ("(g) Explain induction learning.",
         "2025 Part A", C['teal'],
         "Induction Learning derives general rules/hypotheses from specific examples. It is the reverse of deduction.\n\n"
         "Process: Given positive (+) and negative (−) examples of a concept, find a general hypothesis that covers ALL positives and excludes ALL negatives.\n\n"
         "Example: Given 14 days of weather data labeled PlayTennis=Yes/No, learn rule: 'IF Outlook=Sunny AND Humidity=Normal THEN Play=Yes'.\n\n"
         "Key algorithm — ID3: Builds decision tree by splitting on feature with highest Information Gain.\n"
         "Entropy: H(S) = −Σpi·log2(pi)\n"
         "Info Gain: IG(S,A) = H(S) − Σ(|Sv|/|S|)·H(Sv)\n\n"
         "Induction is NOT logically guaranteed — the rule may be wrong on unseen data."),

        ("(h) What are Evolutionary Algorithms? Give an example.",
         "2025 Part A", C['teal'],
         "Evolutionary Algorithms (EAs) are population-based optimization and search methods inspired by biological evolution (Darwinian natural selection). They maintain a POPULATION of candidate solutions and evolve them through selection, crossover, and mutation.\n\n"
         "Common framework: Initialize population → Evaluate fitness → Select better solutions → Apply crossover + mutation → Replace → Repeat.\n\n"
         "Types:\n"
         "1. Genetic Algorithm (GA): Fixed-length string chromosomes. Best for combinatorial optimization.\n"
         "2. Genetic Programming (GP): Evolves program trees. Best for symbolic regression.\n"
         "3. Evolution Strategies: Real-valued vectors with Gaussian mutation. Best for continuous optimization.\n"
         "4. Particle Swarm Optimization: Swarm-inspired velocity updates.\n\n"
         "Example: GA solving Travelling Salesman Problem — evolves city-visit orderings to minimize total distance."),

        ("(i) Discuss why a backpropagation network is required.",
         "2025 Part A", C['teal'],
         "Backpropagation is required for the following reasons:\n\n"
         "1. Single-layer perceptrons can only solve LINEARLY SEPARABLE problems — they CANNOT solve XOR. Multi-layer networks are needed.\n\n"
         "2. For multi-layer networks, we need a way to compute how each hidden-layer weight contributed to the output error. Backpropagation uses the CHAIN RULE to propagate error backward from output to input.\n\n"
         "3. Weight update rule: Δwij = η × δj × yi, where δ is computed by backpropagating error.\n\n"
         "4. Without backpropagation, training deep networks would be computationally impossible — there was no known way to attribute error to hidden layers before 1986.\n\n"
         "5. It enabled the DEEP LEARNING revolution — CNN, RNN, Transformers all rely on it."),

        ("(j) What do you mean by problem reduction in AI?",
         "2025 Part A", C['teal'],
         "Problem Reduction in AI is the approach of decomposing a COMPLEX problem into simpler sub-problems. If all sub-problems are solved, the original problem is solved.\n\n"
         "Represented using AND-OR Graphs/Trees:\n"
         "OR node: Multiple alternative solutions — solve ANY ONE.\n"
         "AND node: ALL sub-problems must be solved for parent to be solved.\n\n"
         "Example: Prove theorem T.\n"
         "Method A: Prove Lemma L1 AND Lemma L2 (AND node).\n"
         "Method B: Prove directly (alternative OR node).\n\n"
         "Algorithm: AO* — finds optimal solution tree in AND-OR graphs.\n\n"
         "Applications: Robot planning, theorem proving, game strategy decomposition."),
    ]:
        for item in qa(q, "1.5 Marks — 100 words", years, ans, c, C['acc']):
            story.append(item)

    story.append(Spacer(1, 0.3*cm))
    story.append(ban("2025 — PART B (Detailed Answers)", C['dark']))
    story.append(Spacer(1, 0.1*cm))

    # Q2 2025
    for q, marks, years, ans, c,bg in [
        ("Q2(a) Differentiate between BNN and ANN. [2025]",
         "5 Marks — 500–800 words", "2025",
         "BNN VS ANN — DETAILED DIFFERENTIATION\n\n"
         "BIOLOGICAL NEURAL NETWORK (BNN) — Structure:\n"
         "The human brain has ~100 billion neurons. Each biological neuron has:\n"
         "• Dendrites: Receive electrochemical signals from other neurons.\n"
         "• Cell Body (Soma): Integrates incoming signals. If total exceeds threshold → fires.\n"
         "• Axon: Transmits output signal (action potential) to other neurons.\n"
         "• Synapse: Junction between neurons. Strength modified by learning.\n\n"
         "ARTIFICIAL NEURAL NETWORK (ANN) — Structure:\n"
         "Each artificial neuron computes:\n"
         "net = Σ(wi × xi) + bias\n"
         "output y = f(net) where f is activation function (sigmoid, ReLU, tanh).\n\n"
         "DETAILED DIFFERENCES:\n\n"
         "1. SCALE:\n"
         "BNN: 100 billion neurons, 100 trillion synapses.\n"
         "ANN: Thousands to millions of neurons, millions to billions of connections.\n\n"
         "2. SIGNAL TYPE:\n"
         "BNN: Electrochemical pulses (action potentials) — binary fire/no-fire with variable timing.\n"
         "ANN: Continuous numerical values (real numbers between -∞ and +∞).\n\n"
         "3. LEARNING MECHANISM:\n"
         "BNN: Synaptic plasticity (LTP/LTD) — biochemical modification of synapse strength. Governed by neurotransmitters, ion channels, neuromodulators.\n"
         "ANN: Backpropagation + gradient descent — mathematical adjustment of numerical weights.\n\n"
         "4. ENERGY EFFICIENCY:\n"
         "BNN: ~20 Watts — extraordinarily energy efficient.\n"
         "ANN: Training requires thousands of watts (GPU clusters).\n\n"
         "5. SPEED:\n"
         "BNN: Neurons fire at 100-200 Hz — slow biochemical signals.\n"
         "ANN: Computations run at GHz on silicon processors.\n\n"
         "6. PARALLELISM:\n"
         "BNN: True massively parallel — billions of neurons process simultaneously in real time.\n"
         "ANN: Simulated parallelism on GPU — far less than biological brains.\n\n"
         "7. FAULT TOLERANCE:\n"
         "BNN: Extremely robust — losing millions of neurons causes minimal effect. Knowledge is distributed across the entire network.\n"
         "ANN: Some distribution, moderate fault tolerance, but not as robust.\n\n"
         "8. LEARNING FROM FEW EXAMPLES:\n"
         "BNN: Humans can learn from 1-2 examples (one-shot learning).\n"
         "ANN: Typically requires thousands to millions of training examples.\n\n"
         "9. GENERAL INTELLIGENCE:\n"
         "BNN: General intelligence — creativity, consciousness, emotion, common sense reasoning.\n"
         "ANN: Narrow intelligence — excellent at specific tasks but cannot generalize across domains.\n\n"
         "10. MEMORY:\n"
         "BNN: Associative memory — pattern completion from partial cues. Holographic/distributed.\n"
         "ANN: Weight matrices store learned patterns. Catastrophic forgetting is a known limitation.\n\n"
         "COMPARISON TABLE:\n"
         "Neurons: BNN=100 billion | ANN=thousands to millions.\n"
         "Connections: BNN=100 trillion | ANN=millions to billions.\n"
         "Signal: BNN=electrochemical | ANN=real-valued numbers.\n"
         "Learning: BNN=synaptic plasticity | ANN=gradient descent.\n"
         "Energy: BNN=20W | ANN=kilowatts.\n"
         "Intelligence: BNN=general | ANN=narrow.\n\n"
         "CONCLUSION:\n"
         "ANN is a mathematical abstraction of BNN, capturing only the most essential computational principle (weighted summation + threshold). Despite vast differences in scale, mechanism, and capability, ANNs have proven remarkably powerful for specific tasks. The gap between biological and artificial intelligence continues to motivate research in neuromorphic computing, spiking neural networks, and AGI.", C['teal'], C['tl']),

        ("Q2(b) Why is RNN preferred in AI? How many layers? Write disadvantages. [2025 — 10M]",
         "10 Marks — 800–1200 words", "2025",
         "RECURRENT NEURAL NETWORKS — COMPLETE ANSWER\n\n"
         "INTRODUCTION:\n"
         "A Recurrent Neural Network (RNN) is a neural network with FEEDBACK connections — the output of a layer at time step t feeds back as input at time step t+1. This gives RNN a form of MEMORY — it can remember past inputs through its hidden state.\n\n"
         "Equations:\n"
         "h(t) = f(Wx·x(t) + Wh·h(t−1) + b)   [hidden state update]\n"
         "y(t) = g(Wy·h(t) + by)                [output at each time step]\n\n"
         "Unlike feedforward networks (process each input independently), RNNs maintain context across a sequence — crucial for language, speech, and time-series data.\n\n"
         "WHY RNN IS PREFERRED IN AI:\n\n"
         "1. SEQUENTIAL DATA PROCESSING:\n"
         "Real-world data is often sequential — text, speech, music, video, sensor readings. Feedforward networks require fixed input size and have no sense of time or order. RNNs naturally handle variable-length sequences while maintaining temporal context.\n\n"
         "2. MEMORY OF PREVIOUS CONTEXT:\n"
         "The hidden state h(t) encodes information from ALL previous time steps. This allows RNN to understand dependencies: 'The bank was steep' vs 'The bank approved the loan' — the word 'bank' changes meaning based on context that came before it.\n\n"
         "3. WEIGHT SHARING ACROSS TIME:\n"
         "The SAME weights (Wx, Wh, Wy) are reused at every time step. This means:\n"
         "a) Far fewer parameters than having separate weights per time step.\n"
         "b) Generalizes across different sequence positions — the network learns temporal patterns.\n"
         "c) Can handle variable-length sequences with fixed parameter count.\n\n"
         "4. FLEXIBLE INPUT-OUTPUT CONFIGURATIONS:\n"
         "RNNs support multiple sequence-to-sequence patterns:\n"
         "One-to-many: Single image → descriptive caption (Image Captioning).\n"
         "Many-to-one: Review text → sentiment score (Sentiment Analysis).\n"
         "Many-to-many (sync): Video frames → frame-level labels.\n"
         "Many-to-many (async): English sentence → French translation (Seq2Seq).\n\n"
         "5. REAL-TIME STREAMING:\n"
         "RNNs update their hidden state as each new token arrives — ideal for real-time applications like speech recognition (Siri, Google Voice), live translation, and stock market analysis.\n\n"
         "LAYERS IN AN RNN:\n\n"
         "RNNs can have ANY number of recurrent layers. Common configurations:\n\n"
         "1. Single-Layer RNN: One recurrent layer. Sufficient for simple tasks like character-level prediction. Processes input sequence with one set of recurrent weights.\n\n"
         "2. Stacked/Deep RNN (Multiple Recurrent Layers): 2-4 recurrent layers stacked vertically. Each layer takes hidden states of the layer below as input. Learns hierarchical representations — lower layers capture local patterns, higher layers capture long-range dependencies. Most modern NLP systems use 2-4 layers.\n\n"
         "3. Bidirectional RNN (Bi-RNN): Processes the sequence in BOTH forward (left to right) and backward (right to left) directions. Each position gets context from both past and future. Doubles effective information. Used in NLP where full sentence context is available.\n\n"
         "4. Encoder-Decoder RNN (Seq2Seq): Two-stage architecture. Encoder RNN reads entire input sequence, compresses to context vector c. Decoder RNN generates output sequence from c. Foundation of neural machine translation.\n\n"
         "DISADVANTAGES OF RNN:\n\n"
         "1. VANISHING GRADIENT PROBLEM (Critical):\n"
         "During Backpropagation Through Time (BPTT), error gradients must flow backward through many time steps. Each step multiplies by the recurrent weight matrix and activation derivative. For sigmoid/tanh activations, derivatives are < 1. After many steps: gradient → 0 exponentially. Early time steps receive nearly ZERO gradient — they cannot learn. The RNN cannot capture LONG-RANGE DEPENDENCIES.\n"
         "Example: 'I was born in France... [50 words later]... I speak French.' The relationship between 'France' and 'French' is 50 steps apart — standard RNN cannot learn this dependency.\n\n"
         "2. EXPLODING GRADIENT PROBLEM:\n"
         "Conversely, large recurrent weights cause gradients to grow exponentially — causing unstable, exploding weight updates. The network oscillates wildly and cannot converge.\n"
         "Partial solution: Gradient clipping — if ||gradient|| > threshold, scale it down.\n\n"
         "3. SEQUENTIAL COMPUTATION — NO PARALLELIZATION:\n"
         "Each time step DEPENDS on the previous one (through hidden state h(t-1)). The entire sequence must be computed sequentially — no parallel processing. This makes training SLOW on modern GPUs, which excel at parallel computation.\n"
         "Transformers (attention-based) process all positions simultaneously — this is why they've largely replaced RNNs for NLP despite being less memory-efficient.\n\n"
         "4. DIFFICULTY WITH LONG-TERM DEPENDENCIES:\n"
         "Standard RNN's memory degrades exponentially with sequence length. Information from many steps ago gets diluted. Effectively has a short memory window.\n\n"
         "5. HIGH COMPUTATIONAL COST:\n"
         "Unrolling through T time steps creates a depth-T network for BPTT — expensive in both time and memory.\n\n"
         "SOLUTIONS TO RNN PROBLEMS:\n\n"
         "1. LSTM (Long Short-Term Memory, Hochreiter & Schmidhuber 1997):\n"
         "Adds a separate CELL STATE C(t) — a 'highway' for gradients:\n"
         "Forget Gate: f(t) = σ(Wf·[h(t-1),x(t)]+bf) — what to forget from cell state.\n"
         "Input Gate: i(t) = σ(Wi·[h(t-1),x(t)]+bi) — what new info to store.\n"
         "Cell Update: C(t) = f(t)⊗C(t-1) + i(t)⊗tanh(Wc·[h(t-1),x(t)]+bc)\n"
         "Output Gate: o(t) = σ(Wo·[h(t-1),x(t)]+bo)\n"
         "Hidden state: h(t) = o(t)⊗tanh(C(t))\n"
         "Cell state gradients can flow unchanged across many steps — SOLVES VANISHING GRADIENT.\n\n"
         "2. GRU (Gated Recurrent Unit, Cho et al. 2014): Simplified LSTM with two gates (Reset, Update). Fewer parameters, comparable performance.\n\n"
         "APPLICATIONS:\n"
         "NLP (sentiment, translation), Speech Recognition (Siri, Google Voice), Music Generation, Time-Series Prediction, Video Analysis, Handwriting Recognition.\n\n"
         "CONCLUSION:\n"
         "RNNs revolutionized sequential data processing. Despite their limitations (vanishing gradient, no parallelism), LSTM/GRU solved the most critical issues. While Transformers now dominate NLP tasks, RNNs remain valuable for real-time streaming, low-memory systems, and inherently sequential domains.", C['teal'], C['tl']),

        ("Q3(a) Why was fuzzy logic introduced? Design a fuzzy set for the human age. [2025 — 5M]",
         "5 Marks — 500–800 words", "2025",
         "FUZZY LOGIC — INTRODUCTION AND FUZZY SET DESIGN FOR HUMAN AGE\n\n"
         "WHY FUZZY LOGIC WAS INTRODUCED:\n\n"
         "Classical (Boolean/Crisp) logic operates on BINARY truth values — a statement is either completely TRUE (1) or completely FALSE (0). This works well for mathematical theorems and digital circuits but FAILS for the imprecise, vague concepts humans use daily.\n\n"
         "Problems with Crisp Logic:\n"
         "1. 'Is a 5'9\" person TALL?' — Binary answer (Yes/No) is inadequate. They are SOMEWHAT tall.\n"
         "2. 'Is water at 29°C HOT?' — Not really, not really cold either. It's lukewarm.\n"
         "3. Medical reasoning: 'Mild fever' cannot be binary. 99.5°F and 101°F are both 'mild' but differ.\n"
         "4. Control systems: An air conditioner controlled by sharp 'HOT/NOT-HOT' threshold gives abrupt on/off behavior — uncomfortable and energy-wasteful.\n\n"
         "Fuzzy Logic was introduced by Lotfi A. Zadeh (1965) to handle this VAGUENESS and PARTIAL TRUTH by allowing membership values between 0 and 1.\n\n"
         "Key reasons for introduction:\n"
         "1. Models human reasoning — humans naturally think in approximations.\n"
         "2. Handles real-world imprecision and uncertainty.\n"
         "3. Enables smooth, gradual system responses instead of abrupt switching.\n"
         "4. No precise mathematical model of the system needed.\n"
         "5. Simple IF-THEN rules can control complex systems.\n\n"
         "DESIGNING A FUZZY SET FOR HUMAN AGE:\n\n"
         "Universe of discourse X = [0, 100] years.\n"
         "We define three overlapping fuzzy sets: YOUNG, MIDDLE-AGED, OLD.\n\n"
         "FUZZY SET 1 — YOUNG (Triangular):\n"
         "μ_YOUNG(x) = 1              if x ≤ 20 years\n"
         "μ_YOUNG(x) = (40-x)/20      if 20 < x < 40 years\n"
         "μ_YOUNG(x) = 0              if x ≥ 40 years\n"
         "Example values: μ(10)=1.0, μ(25)=0.75, μ(30)=0.5, μ(35)=0.25, μ(40)=0.0\n\n"
         "FUZZY SET 2 — MIDDLE-AGED (Trapezoidal):\n"
         "μ_MID(x) = 0              if x ≤ 30\n"
         "μ_MID(x) = (x-30)/15      if 30 < x < 45 (rising edge)\n"
         "μ_MID(x) = 1              if 45 ≤ x ≤ 55 (flat top — fully middle-aged)\n"
         "μ_MID(x) = (70-x)/15      if 55 < x < 70 (falling edge)\n"
         "μ_MID(x) = 0              if x ≥ 70\n"
         "Example values: μ(35)=0.33, μ(50)=1.0, μ(60)=0.67\n\n"
         "FUZZY SET 3 — OLD (Ramp/Triangular):\n"
         "μ_OLD(x) = 0              if x ≤ 60\n"
         "μ_OLD(x) = (x-60)/20      if 60 < x < 80 (rising edge)\n"
         "μ_OLD(x) = 1              if x ≥ 80\n"
         "Example values: μ(65)=0.25, μ(70)=0.5, μ(75)=0.75, μ(85)=1.0\n\n"
         "INTERPRETATION FOR SPECIFIC AGES:\n"
         "Age 25: YOUNG=0.75, MID=0, OLD=0 → Mostly young.\n"
         "Age 35: YOUNG=0.25, MID=0.33, OLD=0 → Young declining, slightly middle-aged.\n"
         "Age 50: YOUNG=0, MID=1.0, OLD=0 → Fully middle-aged.\n"
         "Age 65: YOUNG=0, MID=0.33, OLD=0.25 → Transitioning to old.\n"
         "Age 80: YOUNG=0, MID=0, OLD=1.0 → Fully old.\n\n"
         "This overlapping design reflects how people naturally transition between age categories — just as humans intuitively describe age using approximate terms rather than sharp boundaries.", C['teal'], C['tl']),

        ("Q3(b) What is a Genetic Algorithm and why is it used? Explain the various Genetic Operations. [2025 — 10M]",
         "10 Marks — 800–1200 words", "2025",
         "GENETIC ALGORITHM — COMPLETE ANSWER\n\n"
         "INTRODUCTION:\n"
         "A Genetic Algorithm (GA) is a population-based optimization and search technique inspired by Charles Darwin's theory of natural evolution — 'Survival of the Fittest'. Developed by John Holland (1975), GA maintains a POPULATION of candidate solutions (chromosomes) and evolves them over multiple GENERATIONS through biologically-inspired operators.\n\n"
         "Core principle: Better solutions (higher fitness) are more likely to survive and reproduce. Their offspring inherit favorable characteristics, with occasional random mutations introducing new diversity. Over many generations, the population evolves toward increasingly better solutions.\n\n"
         "WHY GENETIC ALGORITHM IS USED:\n\n"
         "1. NO GRADIENT REQUIRED: GA only needs a fitness function — no mathematical derivation needed. Works for non-differentiable, discontinuous, or noisy objective functions.\n\n"
         "2. GLOBAL SEARCH: Unlike hill climbing (gets stuck at local optima), GA maintains a POPULATION exploring MULTIPLE areas simultaneously — much less likely to get permanently stuck.\n\n"
         "3. COMPLEX SEARCH SPACES: For combinatorial problems (TSP, scheduling) with factorial-sized search spaces, GA finds near-optimal solutions in polynomial time.\n\n"
         "4. MULTI-OBJECTIVE: Can optimize multiple objectives simultaneously using Pareto fronts.\n\n"
         "5. PARALLELIZABLE: Each chromosome can be evaluated independently — naturally suited for parallel computation.\n\n"
         "6. NO DOMAIN KNOWLEDGE: Works as a black-box optimizer — only the fitness function needs to encode domain knowledge.\n\n"
         "WHEN TO USE GA: Large combinatorial search spaces, no closed-form solution, multiple local optima, problems where slight improvement matters. NOT ideal when exact optimal is required or classical methods work efficiently.\n\n"
         "COMPLETE GA ALGORITHM:\n\n"
         "Step 1 — ENCODING/REPRESENTATION:\n"
         "Convert each candidate solution into a CHROMOSOME (a string representation).\n"
         "Binary encoding: 10110101 (most common, simple genetic operations).\n"
         "Integer encoding: [3,1,4,2,5] for ordering/scheduling problems.\n"
         "Real-valued: [1.5, 0.3, 2.7] for continuous optimization.\n"
         "Permutation: [C,A,D,B,E] for TSP (order of city visits).\n\n"
         "Step 2 — INITIALIZE POPULATION:\n"
         "Generate N random chromosomes. N = 50 to 500 typically. Larger N = better exploration but slower.\n\n"
         "Step 3 — EVALUATE FITNESS:\n"
         "Compute fitness f(chromosome) for each individual using the fitness function. Higher fitness = better solution.\n\n"
         "Step 4 — TERMINATION CHECK:\n"
         "Stop if: (a) max generations reached, (b) fitness threshold achieved, (c) population has converged. Otherwise continue.\n\n"
         "Step 5 — SELECTION, Step 6 — CROSSOVER, Step 7 — MUTATION, Step 8 — REPLACE AND REPEAT.\n\n"
         "GENETIC OPERATIONS — DETAILED EXPLANATION:\n\n"
         "OPERATION 1 — SELECTION:\n"
         "Select which chromosomes become PARENTS for next generation. Better fitness = higher selection probability.\n\n"
         "a) Roulette Wheel (Fitness Proportionate) Selection:\n"
         "P(i) = f(i) / Σf(j) — each chromosome gets a slice proportional to fitness.\n"
         "Spin virtual roulette wheel — large slice = high chance of being selected.\n"
         "Problem: If one chromosome has very high fitness, it dominates — premature convergence.\n\n"
         "b) Tournament Selection:\n"
         "Randomly select k individuals (k=2 to 5 typically). Best among them wins.\n"
         "More control over selection pressure. k=2 is most common.\n\n"
         "c) Rank Selection:\n"
         "Sort by fitness, assign selection probability based on RANK not raw fitness value.\n"
         "Avoids super-individual domination. More stable selection pressure.\n\n"
         "d) Elitism:\n"
         "ALWAYS copy the best 1-2 individuals unchanged to next generation.\n"
         "Ensures best solution found is never lost.\n\n"
         "OPERATION 2 — CROSSOVER (Recombination):\n"
         "Combines genetic material of two parents to create offspring.\n"
         "Applied with probability Pc (crossover rate) ≈ 0.6 to 0.9.\n\n"
         "a) Single-Point Crossover:\n"
         "Choose random cut point k. Swap tails of parents.\n"
         "P1: 1011|0101   P2: 1100|1110\n"
         "C1: 1011|1110   C2: 1100|0101\n\n"
         "b) Two-Point Crossover:\n"
         "Choose two cut points k1, k2. Swap middle segment.\n"
         "P1: 10|110|01   P2: 11|001|10\n"
         "C1: 10|001|01   C2: 11|110|10\n\n"
         "c) Uniform Crossover:\n"
         "For each gene position, randomly choose from P1 or P2 with 50% probability.\n"
         "More disruptive — good for diverse populations.\n\n"
         "d) Order Crossover (OX) for Permutations (TSP):\n"
         "Copy middle segment from P1 to C1. Fill remaining positions from P2 in order, skipping already-present cities. Preserves valid permutations.\n\n"
         "e) Arithmetic Crossover (Real-valued):\n"
         "C1 = α·P1 + (1-α)·P2   C2 = (1-α)·P1 + α·P2\n\n"
         "OPERATION 3 — MUTATION:\n"
         "Randomly alters one or more genes. Applied with probability Pm ≈ 0.001 to 0.01 (very small!).\n"
         "Purpose: Maintains genetic diversity. Prevents premature convergence. Introduces new alleles not in initial population. Allows exploration of regions unreachable by crossover alone.\n\n"
         "a) Bit-Flip Mutation (Binary): Flip a randomly selected bit: 0→1 or 1→0.\n"
         "Before: 10110101   After: 10100101 (bit 4 flipped)\n\n"
         "b) Swap Mutation (Permutation): Swap two randomly selected genes.\n"
         "[3,1,4,2,5] → [3,1,2,4,5] (positions 3 and 4 swapped)\n\n"
         "c) Inversion Mutation: Reverse a randomly selected sub-sequence.\n"
         "[3,1,4,2,5] → [3,2,4,1,5] (sub-sequence [1,4,2] reversed to [2,4,1])\n\n"
         "d) Gaussian Mutation (Real-valued): Add small random Gaussian noise to a gene.\n"
         "x'i = xi + N(0, σ²)   where σ controls mutation step size.\n\n"
         "Too much mutation → RANDOM SEARCH. Too little → PREMATURE CONVERGENCE.\n\n"
         "OPERATION 4 — REPLACEMENT:\n"
         "Form new generation from offspring.\n"
         "Generational: All offspring replace all parents.\n"
         "Steady-State: Only worst individuals replaced by new offspring.\n"
         "Elitist: Keep best k parents + add offspring (ensures no regression).\n\n"
         "WORKED EXAMPLE — Maximize f(x) = x² for 5-bit binary chromosomes:\n"
         "Population: [01101=13, 11000=24, 01000=8, 10011=19]\n"
         "Fitness: [169, 576, 64, 361]. Total=1170.\n"
         "Selection: 11000 most likely selected (576/1170 = 49% chance).\n"
         "After crossover+mutation over generations → solution converges to 11111=31, f=961.\n\n"
         "CONCLUSION:\n"
         "GA is a powerful, general-purpose optimization framework. The combination of selection (exploitation of good solutions), crossover (mixing of promising building blocks), and mutation (exploration) enables GA to navigate complex fitness landscapes and find near-optimal solutions where classical methods fail.", C['teal'], C['tl']),

        ("Q4(a) Show that P→S is provable from {P→Q, Q→R, R→S} using Semantic Tableaux. [2025 — 5M]",
         "5 Marks — 500–800 words", "2025",
         "SEMANTIC TABLEAUX PROOF — P→S is provable\n\n"
         "GOAL: Prove that P → S follows logically from premises {P→Q, Q→R, R→S}.\n\n"
         "SEMANTIC TABLEAUX METHOD OVERVIEW:\n"
         "The semantic tableau (truth tree) is a proof system that checks VALIDITY by assuming the NEGATION of what we want to prove and showing this leads to contradiction. If ALL branches close (each reaches a contradiction), then the assumption of negation is impossible — the original statement is valid/provable.\n\n"
         "SETUP:\n"
         "We want to prove: {P→Q, Q→R, R→S} ⊢ (P→S)\n"
         "Method: Assume the argument is INVALID:\n"
         "Assume all PREMISES are TRUE AND conclusion (P→S) is FALSE.\n\n"
         "Given:\n"
         "Premise 1: P → Q   [TRUE]\n"
         "Premise 2: Q → R   [TRUE]\n"
         "Premise 3: R → S   [TRUE]\n"
         "Negated Conclusion: ¬(P→S) which means P=TRUE AND S=FALSE.\n\n"
         "TABLEAU RULES:\n"
         "For A→B (TRUE): BRANCH — Left branch: ¬A, Right branch: B.\n"
         "For ¬(A→B) (TRUE): No branching — A=TRUE AND B=FALSE.\n\n"
         "STEP-BY-STEP CONSTRUCTION:\n\n"
         "Starting state:\n"
         "P→Q [T], Q→R [T], R→S [T], ¬(P→S) [T]\n\n"
         "Decompose ¬(P→S): Gives us P=TRUE and S=FALSE (no branching)\n"
         "Now have: P=T, S=F, P→Q [T], Q→R [T], R→S [T]\n\n"
         "Apply P→Q (TRUE) — since P=TRUE, for P→Q to be TRUE, Q must be TRUE:\n"
         "Branch rule: Left=¬P (CLOSED — contradicts P=TRUE), Right=Q\n"
         "Left branch closes immediately. On right branch: Q=TRUE.\n\n"
         "Apply Q→R (TRUE) — since Q=TRUE, R must be TRUE:\n"
         "Branch: Left=¬Q (CLOSED — contradicts Q=TRUE), Right=R.\n"
         "Left closes. On right branch: R=TRUE.\n\n"
         "Apply R→S (TRUE) — since R=TRUE, S must be TRUE:\n"
         "Branch: Left=¬R (CLOSED — contradicts R=TRUE), Right=S=TRUE.\n"
         "Left closes. On right: S=TRUE.\n\n"
         "CONTRADICTION FOUND:\n"
         "From ¬(P→S): S=FALSE.\n"
         "From R→S with R=TRUE: S=TRUE.\n"
         "S is simultaneously TRUE and FALSE → CONTRADICTION! Branch CLOSES (✗).\n\n"
         "CONCLUSION:\n"
         "Every single branch of the tableau CLOSES (contains a contradiction).\n"
         "Therefore: The assumption that {P→Q, Q→R, R→S} are TRUE but P→S is FALSE is IMPOSSIBLE.\n"
         "Therefore: P→S is a VALID LOGICAL CONSEQUENCE of {P→Q, Q→R, R→S}. QED ✓\n\n"
         "INTUITIVE EXPLANATION:\n"
         "P forces Q (via P→Q).\n"
         "Q forces R (via Q→R).\n"
         "R forces S (via R→S).\n"
         "Therefore P forces S — which is exactly P→S.\n"
         "This is Hypothetical Syllogism applied twice:\n"
         "P→Q AND Q→R → P→R (Hyp. Syllogism)\n"
         "P→R AND R→S → P→S (Hyp. Syllogism) ✓", C['dark'], C['acc']),

        ("Q4(b) Explain the A* algorithm. How different from Hill Climbing? Why called optimized? [2025 — 10M]",
         "10 Marks — 800–1200 words", "2025",
         "A* ALGORITHM — COMPLETE ANSWER\n\n"
         "INTRODUCTION:\n"
         "A* (A-Star) is the most widely used and arguably the most important heuristic search algorithm in AI. Developed by Peter Hart, Nils Nilsson, and Bertram Raphael (1968), A* finds the OPTIMAL (minimum cost) path from start to goal in a weighted graph. It achieves this by combining actual path cost with an estimated remaining cost.\n\n"
         "THE CORE EVALUATION FUNCTION:\n"
         "f(n) = g(n) + h(n)\n\n"
         "g(n): ACTUAL cost from start node S to current node n. Known exactly from the search process.\n"
         "h(n): HEURISTIC — estimated cost from n to goal G. Problem-specific approximation.\n"
         "f(n): Total estimated cost of the cheapest path through n to goal.\n\n"
         "A* always expands the node with the LOWEST f(n) from its OPEN list.\n\n"
         "ADMISSIBILITY CONDITION (Key to optimality):\n"
         "h(n) is ADMISSIBLE if h(n) ≤ h*(n) for all nodes n.\n"
         "h*(n) = true optimal cost from n to goal.\n"
         "If h never OVERESTIMATES, A* is GUARANTEED to find the optimal path.\n\n"
         "A* ALGORITHM — STEP BY STEP:\n\n"
         "STEP 1 — INITIALIZATION:\n"
         "OPEN = {start_node}. OPEN is a priority queue ordered by f(n).\n"
         "CLOSED = {} (explored set).\n"
         "g(start) = 0. f(start) = 0 + h(start). parent(start) = None.\n\n"
         "STEP 2 — SELECT:\n"
         "n = node in OPEN with minimum f(n).\n"
         "If OPEN is empty → No solution exists. Return FAILURE.\n\n"
         "STEP 3 — GOAL CHECK:\n"
         "If n is the GOAL node:\n"
         "Reconstruct path by following parent pointers from goal to start. RETURN optimal path.\n\n"
         "STEP 4 — EXPAND:\n"
         "Move n from OPEN to CLOSED.\n"
         "For each successor s of n:\n"
         "   new_g = g(n) + cost(n, s)   [actual cost to reach s via n]\n"
         "   new_f = new_g + h(s)         [total estimated cost via s]\n"
         "   If s in CLOSED and new_g ≥ g(s): SKIP (already have better path)\n"
         "   If s in OPEN and new_g ≥ g(s): SKIP (current path is better)\n"
         "   Otherwise: Update parent(s)=n, g(s)=new_g, f(s)=new_f. Add to OPEN.\n\n"
         "STEP 5 — LOOP:\n"
         "Go to Step 2.\n\n"
         "WORKED EXAMPLE — 8-PUZZLE:\n"
         "Initial state: {2,8,3,1,_,4,7,6,5}. Goal: {1,2,3,8,_,4,7,6,5}.\n"
         "Heuristic h = Manhattan distance (sum of distances of each tile from goal).\n"
         "h is admissible — each tile needs at least d(Manhattan) moves to reach its goal.\n"
         "A* expands nodes in order of f=g+h, always finding the optimal (minimum moves) solution.\n\n"
         "EXAMPLE — Romania Map (Travel from Arad to Bucharest):\n"
         "h(n) = straight-line distance to Bucharest.\n"
         "A* evaluates: f(Arad)=0+366=366, explores Sibiu: g=140, h=253, f=393.\n"
         "Continues expanding minimum f nodes until Bucharest is reached with optimal path cost.\n\n"
         "HOW A* DIFFERS FROM HILL CLIMBING:\n\n"
         "1. SEARCH TYPE:\n"
         "A*: GLOBAL search — maintains OPEN list of all generated nodes. Explores multiple paths simultaneously. Can jump to any node in the frontier.\n"
         "HC: LOCAL search — only considers current node and immediate neighbors. No global view.\n\n"
         "2. EVALUATION FUNCTION:\n"
         "A*: f(n) = g(n) + h(n) — considers BOTH path cost paid AND estimated remaining cost.\n"
         "HC: f(n) = h(n) only — considers only estimated remaining cost. Ignores path cost.\n\n"
         "3. BACKTRACKING CAPABILITY:\n"
         "A*: CAN backtrack — via OPEN list, can return to any previously generated node.\n"
         "HC: CANNOT backtrack — once it moves to a neighbor, the old state is abandoned.\n\n"
         "4. COMPLETENESS:\n"
         "A*: COMPLETE — will always find a solution if one exists (in finite graphs).\n"
         "HC: NOT complete — permanently stuck at local optima, plateaux, or ridges.\n\n"
         "5. OPTIMALITY:\n"
         "A*: OPTIMAL — finds minimum cost path when h is admissible.\n"
         "HC: NOT optimal — finds only local optimum, not necessarily global.\n\n"
         "6. MEMORY:\n"
         "A*: HIGH — stores all nodes in OPEN and CLOSED lists.\n"
         "HC: VERY LOW — only stores current state.\n\n"
         "WHY A* IS CALLED OPTIMIZED (ADMISSIBLE) ALGORITHM:\n\n"
         "A* is called optimized because when the heuristic h(n) is ADMISSIBLE, A* is GUARANTEED to find the OPTIMAL solution. Here is the formal proof:\n\n"
         "Theorem: If h is admissible, A* finds the optimal solution.\n\n"
         "Proof by contradiction:\n"
         "Suppose A* returns a non-optimal goal G2 with cost f(G2) = g(G2) > C* [true optimal cost].\n"
         "Then the optimal goal G* has NOT been expanded yet.\n"
         "On the optimal path to G*, some node n is in OPEN (not yet expanded).\n"
         "f(n) = g(n) + h(n) ≤ g(n) + h*(n) = C*   [since h(n) ≤ h*(n) — admissible]\n"
         "So f(n) ≤ C* < g(G2) = f(G2).\n"
         "Therefore A* would choose n before G2 — CONTRADICTION with our assumption that G2 was chosen first.\n"
         "Therefore: A* NEVER expands a suboptimal goal before the optimal one. A* finds optimal solution. QED.\n\n"
         "HEURISTIC QUALITY:\n"
         "Admissibility: h(n) ≤ h*(n) [never overestimate].\n"
         "Consistency: h(n) ≤ c(n,a,n') + h(n') [satisfies triangle inequality].\n"
         "Dominance: h2 dominates h1 if h2(n) ≥ h1(n) for all n (h2 is more informed — A* expands fewer nodes).\n\n"
         "For 8-puzzle: h1 = misplaced tiles (admissible). h2 = Manhattan distance (admissible). h2 dominates h1.\n\n"
         "APPLICATIONS:\n"
         "GPS navigation (Google Maps), game AI (pathfinding in all video games), robot motion planning, puzzle solving, network routing, VLSI routing.\n\n"
         "CONCLUSION:\n"
         "A* elegantly balances EXPLORATION (via h — looking toward the goal) and EXPLOITATION (via g — using knowledge of path cost). Its admissibility guarantee makes it the gold standard for heuristic search. While it can be memory-intensive for large spaces (variants like IDA* and SMA* address this), its correctness, completeness, and optimality make it indispensable in AI.", C['dark'], C['acc']),

        ("Q5(b) What is Expert System? Explain architecture with inferencing techniques. [2025 — 10M]",
         "10 Marks — 800–1200 words", "2025",
         "EXPERT SYSTEM — COMPLETE ANSWER\n\n"
         "INTRODUCTION:\n"
         "An Expert System (ES) is a computer program that emulates the decision-making ability of a human expert in a specialized domain. It captures expert knowledge in a formal structure and uses automated reasoning to solve complex problems. The first expert systems appeared in the 1970s and represented a major milestone in AI.\n\n"
         "Famous examples:\n"
         "MYCIN (1974): Diagnosed bacterial blood infections and recommended antibiotics. Performance matched specialist physicians.\n"
         "DENDRAL (1965): Identified unknown organic molecules from mass spectrometry data.\n"
         "XCON (1980): Configured DEC computer systems — saved millions in errors.\n"
         "PROSPECTOR: Identified mineral deposits for geological surveys.\n\n"
         "ARCHITECTURE — SIX KEY COMPONENTS:\n\n"
         "1. KNOWLEDGE BASE (KB):\n"
         "The CORE of the expert system. Stores all domain-specific knowledge:\n"
         "a) Factual Knowledge: Established truths about the domain.\n"
         "   Example: 'Fever above 101°F indicates significant infection risk.'\n"
         "b) Heuristic Knowledge: Rules of thumb, expert experience.\n"
         "   Example: 'Gram-negative bacteria are more likely in burn wound infections.'\n"
         "c) Production Rules: IF-THEN rules encoding expert reasoning.\n"
         "   R1: IF organism is gram-negative AND shape is rod THEN pseudomonas-likely (CF=0.6)\n"
         "   R2: IF patient has burn-wound THEN pseudomonas-likely (CF=0.4)\n"
         "   R3: IF pseudomonas-likely AND WBC-elevated THEN diagnose-pseudomonas (CF=0.7)\n"
         "   R4: IF diagnose-pseudomonas THEN recommend-gentamicin (CF=0.9)\n\n"
         "The KB is SEPARATE from the inference engine. This separation is fundamental — it allows domain experts to update knowledge without changing the reasoning mechanism. Adding a new rule doesn't require reprogramming the system.\n\n"
         "2. WORKING MEMORY (WM) / GLOBAL DATABASE:\n"
         "Stores the CURRENT PROBLEM STATE — facts about the specific case being solved.\n"
         "Contains: User-provided facts, system-gathered data, intermediate inferences, current goals.\n"
         "Dynamically updated: As new facts are derived or obtained, WM grows.\n"
         "Example: WM = {Patient=John, Age=45, Fever=102, Gram-Stain=Negative, Shape=Rod, ...}\n\n"
         "3. INFERENCE ENGINE:\n"
         "The REASONING COMPONENT — applies KB rules to WM facts.\n\n"
         "a) FORWARD CHAINING (Data-Driven):\n"
         "Start with KNOWN FACTS in WM. Find rules whose IF conditions MATCH current WM facts. Fire matching rules — add their THEN conclusions to WM. Repeat until goal reached or no more rules fire.\n\n"
         "Algorithm (RETE-based):\n"
         "1. Match: Pattern-match all rule LHS against WM facts.\n"
         "2. Conflict Set: All rules whose conditions are satisfied.\n"
         "3. Select: Choose one rule using conflict resolution strategy.\n"
         "4. Execute: Fire the selected rule — add THEN part to WM.\n"
         "5. Repeat until goal found or no more rules fire.\n\n"
         "Conflict Resolution Strategies:\n"
         "Specificity: More specific rule wins (fewer matching rules).\n"
         "Recency: Rule matching most recently added fact wins.\n"
         "Priority: Manually assigned priority number.\n"
         "Refractoriness: Don't fire the same rule twice on same data.\n\n"
         "Used for: Medical screening (check all possibilities), monitoring systems, planning.\n\n"
         "b) BACKWARD CHAINING (Goal-Driven):\n"
         "Start with a HYPOTHESIS (goal) we want to prove.\n"
         "Find rules whose THEN part matches the goal.\n"
         "Their IF conditions become NEW SUB-GOALS.\n"
         "Recursively prove each sub-goal — either from WM (known facts) or by asking user.\n\n"
         "Example: Goal: 'Diagnose = Pseudomonas?'\n"
         "→ Find R3: IF pseudomonas-likely AND WBC-elevated THEN diagnose-pseudomonas\n"
         "→ Sub-goals: pseudomonas-likely? AND WBC-elevated?\n"
         "→ For pseudomonas-likely: Find R1: IF gram-negative AND rod-shaped\n"
         "→ Sub-goals: gram-negative? AND rod-shaped? → Ask user.\n"
         "→ User confirms: Gram-negative=YES, Rod=YES → R1 fires → pseudomonas-likely=YES\n"
         "→ WBC: Ask user → WBC=elevated=YES → R3 fires → Diagnose = Pseudomonas ✓\n\n"
         "Used for: Specific hypothesis testing, diagnosis, question-answering.\n\n"
         "c) MIXED CHAINING: Some systems use both — forward chaining to gather available facts, backward chaining to test specific hypotheses.\n\n"
         "4. EXPLANATION FACILITY:\n"
         "One of the most important components — builds USER TRUST.\n"
         "WHY Module: 'Why are you asking me this question?' Shows which rule triggered the question.\n"
         "HOW Module: 'How did you reach this conclusion?' Shows the complete rule chain fired.\n"
         "Example interaction:\n"
         "System: 'Is the patient gram-negative?'\n"
         "User: 'Why?'\n"
         "System: 'Because RULE R1 requires this to determine if pseudomonas is likely.'\n"
         "System: 'Diagnosis: Pseudomonas (CF=0.7)'\n"
         "User: 'How?'\n"
         "System: 'Fired R1 (gram-negative+rod→likely), then R3 (likely+WBC-high→diagnose)'\n\n"
         "5. KNOWLEDGE ACQUISITION FACILITY:\n"
         "Interface for KNOWLEDGE ENGINEERS to encode domain expert knowledge into KB.\n"
         "May include rule editors, consistency checkers, conflict detectors.\n"
         "Modern systems: Machine learning to extract rules from historical case data.\n\n"
         "6. USER INTERFACE:\n"
         "Collects problem information from user (text, menus, forms).\n"
         "Presents conclusions with confidence levels.\n"
         "Shows explanations when requested.\n"
         "Should be usable by non-programmers (doctors, engineers, etc.).\n\n"
         "ARCHITECTURE DIAGRAM (textual):\n"
         "[User] ↔ [User Interface] ↔ [Inference Engine] ↔ [Knowledge Base]\n"
         "                              ↕                          ↕\n"
         "                       [Working Memory]    [Explanation Facility]\n"
         "                                          [Knowledge Acquisition]\n\n"
         "CHARACTERISTICS OF EXPERT SYSTEMS:\n"
         "High performance: Expert-level accuracy in the domain.\n"
         "Reliability: Consistent — same inputs always give same outputs.\n"
         "Explainability: Can always explain how it reached a conclusion.\n"
         "Availability: 24/7, unlimited replications, no fatigue.\n\n"
         "LIMITATIONS:\n"
         "Knowledge acquisition bottleneck: Extracting knowledge from experts is slow and expensive.\n"
         "Brittleness: Fails gracefully outside its narrow domain.\n"
         "No common sense: Cannot handle unexpected situations.\n"
         "Static: Cannot learn from new cases (unless updated manually).\n\n"
         "CONCLUSION:\n"
         "Expert systems demonstrated that AI could achieve human-expert performance in narrow domains, laying the groundwork for modern AI. The separation of knowledge from reasoning, the explanation facility, and uncertainty handling through certainty factors were landmark contributions. While modern ML/DL systems have surpassed rule-based expert systems in many areas, expert systems remain valuable for well-defined, rule-governed domains requiring explainability.", C['green'], C['gl']),

        ("Q6(a) What is Reasoning? Types? Explain inductive and deductive reasoning. [2025 — 5M]",
         "5 Marks — 500–800 words", "2025",
         "REASONING IN AI — TYPES AND INDUCTIVE vs DEDUCTIVE\n\n"
         "WHAT IS REASONING:\n"
         "Reasoning in AI is the cognitive process of drawing conclusions, making inferences, or solving problems from known facts, observations, and rules. It is a fundamental component of intelligence — without reasoning, a system can only retrieve stored facts but cannot derive new knowledge.\n\n"
         "TYPES OF REASONING:\n\n"
         "1. DEDUCTIVE REASONING (Top-Down / Certain):\n"
         "Moves from GENERAL premises to SPECIFIC conclusions. If the premises are true and the argument is logically valid, the conclusion is GUARANTEED.\n\n"
         "Structure: Major Premise + Minor Premise → Certain Conclusion\n\n"
         "Classic example:\n"
         "Major: All humans are mortal.     [General rule]\n"
         "Minor: Socrates is a human.       [Specific fact]\n"
         "Conclusion: Socrates is mortal.   [GUARANTEED - logically certain]\n\n"
         "Inference rules used: Modus Ponens (P, P→Q ⊢ Q), Modus Tollens (¬Q, P→Q ⊢ ¬P), Hypothetical Syllogism.\n\n"
         "In AI: Expert systems use deductive reasoning — given rules and patient facts, DEDUCE diagnosis. Logic theorem provers, Prolog programming.\n\n"
         "Strength: Logically GUARANTEED. If premises true → conclusion necessarily true.\n"
         "Weakness: Cannot generate truly NEW knowledge beyond what's already in premises. Cannot handle uncertainty.\n\n"
         "2. INDUCTIVE REASONING (Bottom-Up / Probable):\n"
         "Moves from SPECIFIC observations to GENERAL rules. The conclusion is a PROBABLE generalization — not logically guaranteed.\n\n"
         "Structure: Multiple observations → Generalized Rule (with uncertainty)\n\n"
         "Example:\n"
         "Observation 1: The sun rose in the east today.\n"
         "Observation 2: The sun rose in the east yesterday.\n"
         "Observation 3: ...and every recorded day in history.\n"
         "Inductive conclusion: The sun always rises in the east. [Probable — but not guaranteed!]\n\n"
         "Hume's Problem of Induction: No matter how many white swans you observe, you cannot PROVE all swans are white (a black swan was eventually found in Australia).\n\n"
         "In AI/ML: Machine learning IS applied induction. Given training examples, induce hypothesis:\n"
         "ID3 decision tree: Sees 14 days of weather data → induces classification rules.\n"
         "Neural networks: See millions of images → induce pattern recognition rules.\n"
         "Naive Bayes: See spam/ham emails → induces classification model.\n\n"
         "Strength: Generates NEW general rules from data. Enables learning from experience.\n"
         "Weakness: Conclusion is PROBABLE not certain. Susceptible to overfitting (rule too specific to training data).\n\n"
         "3. ABDUCTIVE REASONING:\n"
         "Inference to the BEST EXPLANATION. Given observations, find the most likely cause.\n"
         "Example: Wet ground (observation) → Best explanation: It rained (abduction).\n"
         "Used in: Medical diagnosis, fault diagnosis, crime investigation.\n\n"
         "4. ANALOGICAL REASONING:\n"
         "Solves new problems by analogy with similar known problems.\n"
         "Example: Knowing how to drive a car helps learn to drive a truck.\n"
         "Used in: Case-based reasoning, NLP metaphor understanding.\n\n"
         "5. NON-MONOTONIC REASONING:\n"
         "Handles DEFAULT assumptions that can be overridden by new information.\n"
         "Example: 'Birds normally fly' → Tweety flies (default). New info: Tweety is penguin. Retract: Tweety cannot fly.\n"
         "Classical (monotonic) logic cannot retract conclusions — NM reasoning is needed for default reasoning.\n\n"
         "INDUCTION vs DEDUCTION — KEY COMPARISON:\n"
         "Direction: Induction=specific→general | Deduction=general→specific.\n"
         "Certainty: Induction=probable | Deduction=logically guaranteed.\n"
         "New knowledge: Induction=YES (generates new rules) | Deduction=NO (only derives what's in premises).\n"
         "Used in AI: Induction=ML, learning systems | Deduction=expert systems, logic programming.\n\n"
         "CONCLUSION:\n"
         "Both reasoning types are essential in AI. Expert systems primarily use deductive reasoning; machine learning primarily uses inductive reasoning. Modern intelligent systems combine both: learn rules inductively from data, then reason deductively from those rules to make decisions.", C['maroon'], C['ml']),

        ("Q7 Write short notes: (a) Blackboard Architecture (b) Semantic Nets and Frames (c) AO* Algorithm. [2025 — 15M]",
         "15 Marks — 1200–1500 words", "2025",
         "SHORT NOTE (a): BLACKBOARD ARCHITECTURE\n\n"
         "INTRODUCTION:\n"
         "Blackboard Architecture is a cooperative AI problem-solving model developed for the HEARSAY-II speech recognition system at Carnegie Mellon University (Erman et al., 1980). It provides a framework where multiple independent knowledge sources collaborate to solve problems too complex for any single module.\n\n"
         "ANALOGY: Imagine a group of experts (doctors, lab technicians, pharmacists) working around a shared physical blackboard. Each expert reads what others have written, adds their specialized contribution, and gradually the full diagnosis emerges. No expert communicates directly with another — all coordination happens through the blackboard.\n\n"
         "THREE COMPONENTS:\n\n"
         "1. THE BLACKBOARD (Central Shared Memory):\n"
         "A hierarchically structured global data structure — the SOLE communication medium. All knowledge sources read from and write to the blackboard. Organized into LEVELS representing different abstraction layers:\n"
         "In HEARSAY-II: Level 1=Acoustic signals, Level 2=Phonemes, Level 3=Syllables, Level 4=Words, Level 5=Phrases, Level 6=Sentences.\n"
         "The initial problem input appears at the lowest level. As KSes process and interpret the data, higher-level hypotheses appear on upper levels. The complete solution appears at the highest level.\n"
         "Contents: Raw input, partial solutions, hypotheses with confidence values, current best partial solution tree.\n\n"
         "2. KNOWLEDGE SOURCES (KSes):\n"
         "Independent, self-contained specialist modules. Each KS is an expert in one specific aspect of the problem.\n"
         "Each KS has TWO parts:\n"
         "a) Trigger/Precondition: Specifies WHEN this KS is applicable — what patterns on the blackboard activate it.\n"
         "b) Action: What the KS does when triggered — reads relevant blackboard data, performs specialized computation, writes result to higher-level blackboard space.\n"
         "CRITICAL: KSes NEVER communicate directly — only through the blackboard.\n"
         "Different KSes may use entirely different knowledge representations (rules, neural networks, fuzzy systems, statistical models).\n"
         "Examples in HEARSAY-II: Acoustic KS (converts raw audio to phoneme hypotheses), Lexical KS (matches phonemes to words), Syntax KS (checks grammatical validity), Semantic KS (checks meaningfulness).\n\n"
         "3. CONTROL COMPONENT (Scheduler/Monitor):\n"
         "The 'manager' coordinating the KSes. It:\n"
         "• Continuously monitors the blackboard for new data or changes.\n"
         "• Identifies which KSes are triggered by current blackboard state.\n"
         "• Evaluates and SELECTS which KS to activate next using a scheduling strategy.\n"
         "Scheduling strategies: Opportunistic/Best-First (activate KS that will contribute most), Priority-Based (fixed priority ranks), Breadth-First (all triggered KSes at current level), Depth-First (develop one hypothesis fully).\n\n"
         "WORKING CYCLE:\n"
         "1. Problem input placed on blackboard at Level 1.\n"
         "2. Control identifies triggered KSes.\n"
         "3. Best KS selected and activated.\n"
         "4. KS reads relevant data, computes, writes result to higher level.\n"
         "5. New data may trigger other KSes. Control updates agenda.\n"
         "6. Cycle repeats until complete solution at highest level.\n\n"
         "Advantages: Modular (easy to add/remove KSes), flexible, handles uncertainty, supports parallelism.\n"
         "Disadvantages: Complex control design, communication overhead, hard to debug.\n"
         "Applications: HEARSAY-II (speech), HASP (sonar), PROTEAN (protein structure), autonomous vehicle sensor fusion.\n\n"
         "---\n\n"
         "SHORT NOTE (b): SEMANTIC NETS AND FRAMES\n\n"
         "SEMANTIC NETWORKS (Quillian, 1968):\n"
         "Directed labeled graph. Nodes=concepts/objects. Arcs=labeled relationships.\n\n"
         "Key relationship types:\n"
         "IS-A: Class membership — Dog IS-A Animal. Penguin IS-A Bird.\n"
         "HAS-A: Property possession — Dog HAS-A Tail. Car HAS-A Engine.\n"
         "HAS-PART: Component — Car HAS-PART Wheel.\n"
         "CAN: Capability — Bird CAN Fly. Dog CAN Bark.\n"
         "IS-INSTANCE-OF: Fido IS-INSTANCE-OF Dog.\n\n"
         "INHERITANCE: Properties flow DOWNWARD through IS-A links.\n"
         "Animal CAN Breathe. Dog IS-A Animal. Therefore Dog CAN Breathe.\n"
         "Fido IS-A Dog. Therefore Fido CAN Breathe AND Fido HAS-A Tail.\n"
         "Child node overrides parent: Bird CAN Fly. Penguin IS-A Bird. Penguin CANNOT Fly (override).\n\n"
         "PARTITIONED NETWORKS (Extension):\n"
         "Adds SPACES to handle quantifier scope:\n"
         "G-space (Generic): For universal quantifiers (∀ — for all)\n"
         "I-space (Individual): For existential quantifiers (∃ — there exists)\n"
         "'Every lunatic hit a doctor': G-space(L) → I-space(D), L-hit-D. D depends on L.\n"
         "'The lunatic hit the door': Two I-spaces, no nesting.\n"
         "'Every lunatic hit every doctor': Nested G-spaces — outer G(L), inner G(D), L-hit-D.\n\n"
         "Advantages of Semantic Nets: Visual, intuitive, inheritance, no redundancy.\n"
         "Disadvantages: Cannot represent quantifiers (in basic form), negation, procedural knowledge.\n\n"
         "FRAMES (Minsky, 1975):\n"
         "Slot-value data structure representing stereotyped objects/situations.\n\n"
         "Components:\n"
         "Frame Name: Identifier (Car, Person, Restaurant)\n"
         "Slots: Attributes (Color, Weight, Speed)\n"
         "Fillers: Actual values (Color=Red, Speed=120kmh)\n"
         "Default Values: Used when no specific value given (Wheels=4 for Car)\n"
         "Value Restrictions: Constraints on slot values (Age must be 0-120)\n"
         "Demons: IF-NEEDED (compute when accessed), IF-ADDED (trigger on insertion)\n"
         "IS-A Link: For inheritance from parent frame\n\n"
         "Example Frame Hierarchy:\n"
         "FRAME: Vehicle | Wheels=4(default) | Engine=Yes | Can=Transport\n"
         "FRAME: Car IS-A Vehicle | Doors=4(default) | Fuel=(Petrol/Diesel/Electric)\n"
         "FRAME: ElectricCar IS-A Car | Fuel=Electric | Battery=integer(kWh)\n"
         "FRAME: MyTesla IS-A ElectricCar | Color=Red | Battery=100kWh\n"
         "MyTesla inherits: Wheels=4, Engine=Yes, Doors=4. Overrides nothing.\n\n"
         "Advantages: Natural for objects, defaults, inheritance, combines declarative+procedural.\n"
         "Disadvantages: Rigid, multiple inheritance conflicts, no formal semantics.\n\n"
         "---\n\n"
         "SHORT NOTE (c): AO* ALGORITHM\n\n"
         "INTRODUCTION:\n"
         "AO* (AO-Star) is an extension of A* for AND-OR graphs. While A* finds an optimal PATH in a regular graph, AO* finds an optimal SOLUTION TREE in an AND-OR graph where some nodes require all sub-problems to be solved (AND) and others require only one alternative (OR).\n\n"
         "AND-OR GRAPH CONCEPTS:\n"
         "OR node: Multiple alternative ways to solve — choose the CHEAPEST alternative.\n"
         "AND node: ALL children must be solved for the parent to be solved.\n"
         "Terminal node: Has a known solution (cost = 0).\n"
         "h(n): Estimated cost to solve node n.\n\n"
         "COST CALCULATION:\n"
         "For OR node: f(n) = min over alternatives (arc_cost + f(child))\n"
         "For AND node: f(n) = sum over ALL children (arc_cost + f(child))\n\n"
         "AO* ALGORITHM:\n"
         "Step 1: Initialize root node. Compute h(root).\n"
         "Step 2: Select the most promising (lowest cost) unexpanded node in current best partial solution tree.\n"
         "Step 3: Expand selected node. Generate successor nodes.\n"
         "Step 4: For each successor:\n"
         "   If terminal → mark SOLVED, cost = 0.\n"
         "   Otherwise → compute h, add to graph.\n"
         "Step 5: Back-propagate cost updates through the tree.\n"
         "   Update parent costs using OR/AND cost formulas.\n"
         "   Update best child pointers.\n"
         "Step 6: If root node is SOLVED → return solution tree.\n"
         "   Else go to Step 2.\n\n"
         "WORKED EXAMPLE:\n"
         "Problem: Solve A.\n"
         "A can be solved by B alone (OR) or by C AND D together (AND).\n"
         "h values: h(A)=5, h(B)=4, h(C)=3, h(D)=2. All arc costs=1.\n\n"
         "Iteration 1: Expand A. Two options:\n"
         "OR path A→B: f = 1 + h(B) = 1 + 4 = 5\n"
         "AND path A→{C,D}: f = (1+h(C)) + (1+h(D)) = 4 + 3 = 7\n"
         "Best partial tree: A→B (cost=5). Select B to expand.\n\n"
         "Iteration 2: Expand B. B has terminal child E (cost 0).\n"
         "B→E: f = 1+0 = 1. B is SOLVED (cost = 1).\n"
         "Back-propagate: A's best = A→B. f(A) = 1+f(B) = 1+1 = 2. A is SOLVED.\n\n"
         "Solution tree: A→B→E with total cost 2. This is optimal!\n\n"
         "KEY DIFFERENCE FROM A*:\n"
         "A*: Finds optimal PATH in regular OR-graphs.\n"
         "AO*: Finds optimal SOLUTION TREE in AND-OR graphs.\n"
         "AO* used for: Problem decomposition, theorem proving, planning with compound goals.\n\n"
         "Advantages: Optimal solution, handles both AND and OR decompositions, systematic exploration.\n"
         "Disadvantages: More complex than A*, back-propagation adds overhead.", C['purple'], C['pl']),
    ]:
        for item in qa(q, marks, years, ans, c, bg if 'purple' in str(c) else (C['gl'] if 'green' in str(c) else (C['tl'] if 'teal' in str(c) else C['acc']))):
            story.append(item)

    story.append(PageBreak())

    # ════════════════════ 2024 SPECIFIC QUESTIONS ═════════════════════════
    story.append(ban("MAY 2024 EXAM — COMPLETE PAPER WITH ALL ANSWERS", C['purple']))
    story.append(Spacer(1, 0.2*cm))
    story.append(ibox("Sr. 003601 | May 2024 | B.Tech 6th Sem | Max Marks: 75 | Time: 3 Hrs",
                      C['pl'], C['purple']))
    story.append(Spacer(1, 0.2*cm))
    story.append(ban("2024 — PART A (1.5 Marks Each — 100 Words)", C['purple']))

    for q, years, c,ans in [
        ("(a) What are the various uses of the intelligent system?", "2024 Part A", C['purple'],
         "Uses of Intelligent Systems:\n"
         "1. Medical Diagnosis: Disease detection, drug interaction checking, surgical assistance.\n"
         "2. Manufacturing: Quality control, predictive maintenance, process optimization.\n"
         "3. Finance: Fraud detection, algorithmic trading, credit risk assessment.\n"
         "4. Transportation: Autonomous vehicles, traffic optimization, airline scheduling.\n"
         "5. Education: Intelligent tutoring systems, adaptive learning, essay grading.\n"
         "6. Customer Service: Chatbots, recommendation engines (Netflix, Amazon).\n"
         "7. Agriculture: Crop disease detection, yield prediction, precision farming.\n"
         "8. Security: Intrusion detection, biometric authentication, threat analysis.\n"
         "9. Gaming: NPC behavior, game difficulty adjustment, procedural content generation.\n"
         "10. Scientific Research: Protein folding (AlphaFold), climate modeling, drug discovery."),

        ("(b) What do you mean by Perceptron?", "2024 Part A", C['purple'],
         "A Perceptron is the simplest artificial neural network unit, proposed by Frank Rosenblatt (1957). It models a single biological neuron: takes multiple inputs x1,...,xn, multiplies each by its weight wi, sums them, adds a bias b, and applies a step activation function.\n\n"
         "Output: y = 1 if Σ(wi·xi) + b ≥ 0, else y = 0.\n\n"
         "Learning Rule (Delta Rule): Δwi = η × (target − output) × xi. Adjusts weights to minimize error.\n\n"
         "Limitation: Only solves linearly separable problems. Cannot solve XOR. This limitation (proved by Minsky & Papert, 1969) triggered the first 'AI Winter'. Solution: Multi-layer perceptrons (MLP) with backpropagation."),

        ("(c) List applications of Genetic Algorithm.", "2024 Part A", C['purple'],
         "Applications of Genetic Algorithm:\n"
         "1. Travelling Salesman Problem (TSP): Find minimum-distance route visiting all cities.\n"
         "2. Job Scheduling: Optimal task assignment to minimize time/cost.\n"
         "3. VLSI Circuit Design: Optimize chip layout for minimum area and power.\n"
         "4. Neural Network Optimization: Evolve network architecture and weights.\n"
         "5. Feature Selection: Choose best features for ML models.\n"
         "6. Financial Portfolio Optimization: Maximize return for given risk.\n"
         "7. Robot Path Planning: Find obstacle-free minimum-distance paths.\n"
         "8. Game Playing: Evolve game strategies (checkers, Pac-Man).\n"
         "9. Bioinformatics: Protein structure prediction, DNA sequence alignment.\n"
         "10. Engineering Design: Optimize structural designs (bridges, aerodynamics)."),

        ("(d) Differentiate between crisp logic and fuzzy logic.", "2024 Part A", C['purple'],
         "Crisp Logic vs Fuzzy Logic:\n\n"
         "Crisp Logic: Membership is strictly 0 (not member) or 1 (full member). Sharp, well-defined boundaries. Example: 'Height > 180cm is TALL' (binary yes/no).\n\n"
         "Fuzzy Logic: Membership ranges continuously from 0 to 1. Gradual, overlapping boundaries. Example: 'Height 170cm is TALL with degree 0.6'.\n\n"
         "Key differences:\n"
         "Membership: Crisp=binary | Fuzzy=continuous [0,1].\n"
         "Boundaries: Crisp=sharp | Fuzzy=gradual.\n"
         "Handles vagueness: Crisp=NO | Fuzzy=YES.\n"
         "Truth values: Crisp=TRUE/FALSE | Fuzzy=degree of truth.\n"
         "Models human reasoning: Crisp=poorly | Fuzzy=well.\n"
         "Applications: Crisp=digital circuits | Fuzzy=control systems, AI."),

        ("(e) What is heuristic search? Explain with example.", "2024 Part A", C['purple'],
         "Heuristic Search uses problem-specific knowledge (a heuristic function h(n)) to guide the search toward the goal more efficiently, avoiding blind exploration of all possible states.\n\n"
         "h(n) = estimated cost from current node n to the goal. Good heuristics are:\n"
         "Admissible: h(n) ≤ h*(n) — never overestimate true cost.\n"
         "Informative: h(n) is close to actual cost h*(n).\n\n"
         "Example — 8-Puzzle:\n"
         "h1 = Number of misplaced tiles (admissible: each needs ≥1 move).\n"
         "h2 = Manhattan distance = sum of |row_curr − row_goal| + |col_curr − col_goal|.\n"
         "h2 is more informed than h1 — A* with h2 expands fewer nodes.\n\n"
         "A* uses f(n)=g(n)+h(n): balances actual cost g and estimated remaining cost h."),

        ("(f) What are applications of iterative deepening search?", "2024 Part A", C['purple'],
         "Applications of Iterative Deepening Search (IDDFS):\n\n"
         "IDDFS is the preferred uninformed search when: solution depth is unknown, memory is limited, and optimal solution is needed.\n\n"
         "Applications:\n"
         "1. Game Playing: Chess and puzzle solving where search depth is variable.\n"
         "2. Web Crawling: Memory-efficient exploration of large web graphs.\n"
         "3. Theorem Proving: Depth-bounded proof search.\n"
         "4. Robot Path Planning: Finding paths in large state spaces.\n"
         "5. Database Query Optimization: Finding optimal query execution plans.\n"
         "6. Software Model Checking: Systematic state space exploration.\n"
         "7. Natural Language Parsing: Exploring parse trees with limited memory.\n"
         "8. AI Planning: Finding action sequences in large planning domains."),

        ("(g) Differentiate between database and knowledge base.", "2024 Part A", C['purple'],
         "Database vs Knowledge Base:\n\n"
         "DATABASE:\n"
         "Stores structured DATA (tables, records). Supports exact retrieval queries (SQL). Data is precise, well-structured. No reasoning capability. Answers: 'What ARE the facts?' Example: Student table (ID, Name, Marks, CGPA).\n\n"
         "KNOWLEDGE BASE:\n"
         "Stores KNOWLEDGE — facts + rules + relationships + uncertainty. Supports reasoning and inference. Can derive NEW information not explicitly stored. Handles incomplete/uncertain knowledge. Answers: 'What can be INFERRED from the facts?'\n\n"
         "Example: KB can infer 'Rahul should study more' from rules about GPA thresholds + Rahul's GPA stored as a fact. Database can only retrieve Rahul's GPA — it cannot apply rules to derive recommendations."),

        ("(h) What is the semantic net?", "2024 Part A", C['purple'],
         "A Semantic Network is a directed labeled graph for knowledge representation, proposed by Quillian (1968). Nodes represent objects, concepts, or events. Labeled directed arcs represent typed relationships between nodes.\n\n"
         "Key arc types: IS-A (class membership: Dog IS-A Animal), HAS-A (property: Dog HAS-A Tail), CAN (capability: Dog CAN Bark), HAS-PART (component: Car HAS-PART Engine).\n\n"
         "Property Inheritance: Via IS-A links, properties propagate downward. Fido IS-A Dog IS-A Animal → Fido inherits all Dog and Animal properties.\n\n"
         "Advantages: Visual, intuitive, supports inheritance, reduces redundancy.\n"
         "Disadvantages: Cannot represent quantifiers, negation, or procedural knowledge in basic form."),

        ("(i) State Dempster-Shafer's Theory.", "2024 Part A", C['purple'],
         "Dempster-Shafer (DS) Theory (Dempster 1967, Shafer 1976) is a mathematical framework for evidential reasoning under uncertainty — a generalization of Bayesian probability.\n\n"
         "Key concepts:\n"
         "Frame of Discernment Θ: Complete set of mutually exclusive hypotheses.\n"
         "Mass function m: m(A) = belief specifically committed to subset A of Θ. Σm(A)=1, m(∅)=0.\n"
         "m(Θ) = ignorance — unassigned belief.\n"
         "Belief Bel(A) = Σm(B) for B⊆A [lower bound on probability].\n"
         "Plausibility Pl(A) = 1-Bel(¬A) [upper bound on probability].\n"
         "Interval [Bel(A), Pl(A)] = range of possible probability.\n\n"
         "Unlike probability, DS explicitly models IGNORANCE and assigns belief to SETS of hypotheses."),

        ("(j) What is Bayesian reasoning?", "2024 Part A", C['purple'],
         "Bayesian reasoning uses Bayes' Theorem to update the probability of a hypothesis when new evidence is observed:\n\n"
         "P(H|E) = [P(E|H) × P(H)] / P(E)\n\n"
         "P(H) = Prior — probability of hypothesis BEFORE evidence.\n"
         "P(E|H) = Likelihood — probability of evidence IF hypothesis is true.\n"
         "P(H|E) = Posterior — UPDATED probability AFTER observing evidence.\n"
         "P(E) = Marginal = P(E|H)·P(H) + P(E|¬H)·P(¬H).\n\n"
         "Example: P(Disease)=0.01, P(Test+|Disease)=0.95, P(Test+|NoDisease)=0.10.\n"
         "P(Disease|Test+) = (0.95×0.01)/[(0.95×0.01)+(0.10×0.99)] = 0.0875.\n\n"
         "Applications: Medical diagnosis, spam filtering, fault detection, speech recognition."),
    ]:
        for item in qa(q, "1.5 Marks — 100 words", years, ans, c, C['pl']):
            story.append(item)

    story.append(Spacer(1, 0.3*cm))
    story.append(ban("2024 — PART B (Detailed Answers)", C['purple']))

    for q, marks, years, ans, c,bg in [
        ("Q2(a) Advantages and disadvantages of backpropagation network. [2024 — 10M]",
         "10 Marks — 800–1200 words", "2024",
         "BACKPROPAGATION — ADVANTAGES AND DISADVANTAGES (COMPLETE)\n\n"
         "INTRODUCTION:\n"
         "Backpropagation (error back-propagation) is the primary algorithm for training multi-layer feedforward neural networks. It uses the chain rule of calculus to compute gradients of a loss function with respect to all network weights, then applies gradient descent to minimize the loss. Popularized by Rumelhart, Hinton, Williams (1986), it enabled the deep learning revolution.\n\n"
         "HOW IT WORKS (Brief):\n"
         "Forward Pass: Input → weighted sums → activations → output → loss L = (1/2)Σ(target − output)².\n"
         "Backward Pass: Compute δ for each neuron using chain rule:\n"
         "Output layer: δk = (tk − yk) × f'(net_k)\n"
         "Hidden layer: δj = f'(net_j) × Σ(δk × wjk)\n"
         "Weight update: Δwij = η × δj × yi   (η = learning rate)\n\n"
         "ADVANTAGES OF BACKPROPAGATION:\n\n"
         "1. SOLVES XOR AND NON-LINEAR PROBLEMS:\n"
         "The most important advantage. Single-layer perceptrons can ONLY solve linearly separable problems. Backpropagation enables multi-layer networks that can approximate ANY continuous function (Universal Approximation Theorem). XOR, which was impossible for single-layer networks, is trivially solved with one hidden layer.\n\n"
         "2. GENERAL-PURPOSE LEARNING:\n"
         "Works for classification, regression, function approximation, feature learning, and generative tasks. The same algorithm applies regardless of the specific problem domain — only the loss function and architecture change.\n\n"
         "3. SCALES TO DEEP NETWORKS:\n"
         "Can train networks with dozens or hundreds of layers (with modern improvements). Deep networks learn hierarchical representations — early layers detect edges, middle layers detect shapes, deep layers detect objects. This hierarchical learning is key to performance in vision and NLP.\n\n"
         "4. AUTOMATIC FEATURE EXTRACTION:\n"
         "Unlike classical ML (which requires manual feature engineering), backpropagation automatically discovers the most discriminative features from raw data. Deep networks have replaced hand-crafted features in virtually every domain.\n\n"
         "5. MATHEMATICALLY PRINCIPLED:\n"
         "Grounded in calculus (chain rule) and optimization theory (gradient descent). Convergence properties are well-studied. Many variants (Adam, RMSprop, Adagrad) optimize the basic gradient descent.\n\n"
         "6. WIDELY IMPLEMENTED:\n"
         "Automatic differentiation in PyTorch (autograd) and TensorFlow (GradientTape) implements backpropagation automatically. Engineers focus on architecture design; backprop handles training automatically.\n\n"
         "7. SUPPORTS ALL ARCHITECTURES:\n"
         "Applies to feedforward networks, CNNs, RNNs (as BPTT), and Transformers. It is the universal training method for neural networks.\n\n"
         "8. ONLINE, MINI-BATCH, AND BATCH VARIANTS:\n"
         "Can be applied one example at a time (online), in small batches (mini-batch, most common), or on entire dataset (batch). Mini-batch training (32-256 examples) provides excellent balance of speed, stability, and generalization.\n\n"
         "DISADVANTAGES OF BACKPROPAGATION:\n\n"
         "1. VANISHING GRADIENT PROBLEM:\n"
         "Most critical limitation. As error propagates backward through deep layers, gradients are multiplied by activation derivatives. For sigmoid/tanh: f'(x) ≤ 0.25. After 10 layers: gradient shrinks by (0.25)^10 ≈ 10^(-6). Early layers receive essentially zero gradient — they CANNOT LEARN. This prevented training deep networks until ReLU and batch normalization were introduced.\n"
         "Solution: ReLU activation (f'(x) = 1 for x>0 — no saturation), residual connections (ResNet — gradients bypass layers), batch normalization (keeps activations in non-saturating range).\n\n"
         "2. EXPLODING GRADIENT PROBLEM:\n"
         "Opposite of vanishing gradient — gradients grow exponentially in very deep networks or RNNs. Causes unstable, diverging training. Solution: Gradient clipping (scale down gradient when its norm exceeds threshold).\n\n"
         "3. LOCAL MINIMA AND SADDLE POINTS:\n"
         "Gradient descent may converge to a local minimum — a solution worse than the global optimum. In high-dimensional spaces, saddle points (gradient=0 but not minimum) are common. Modern networks have many local minima but most are near the global minimum (empirical observation). Solutions: Momentum, Adam optimizer, stochastic gradients (noise helps escape).\n\n"
         "4. REQUIRES LARGE TRAINING DATASETS:\n"
         "Deep networks have millions of parameters — require millions of training examples to avoid overfitting. Data collection and labeling is expensive. Solutions: Data augmentation, transfer learning, semi-supervised learning.\n\n"
         "5. SLOW CONVERGENCE:\n"
         "May require millions of iterations (epochs) across large datasets for complex problems. Training large models (GPT-3) takes weeks on GPU clusters. Solution: Adam optimizer, learning rate schedules, better initialization.\n\n"
         "6. LEARNING RATE SENSITIVITY:\n"
         "Too large learning rate η → oscillation, divergence. Too small → impractically slow convergence. Solution: Adaptive learning rates (Adam, RMSprop automatically adjust η per parameter).\n\n"
         "7. BLACK BOX / LACK OF INTERPRETABILITY:\n"
         "The learned weights in millions of neurons are not interpretable. It is impossible to know WHY the network makes a specific decision — critical problem for medical and legal AI systems. Active research in explainable AI (XAI) attempts to address this.\n\n"
         "8. COMPUTATIONALLY EXPENSIVE:\n"
         "Training GPT-3 (175B parameters) cost ~$12 million in GPU compute. Requires specialized hardware (GPUs, TPUs). Not practical for edge devices or real-time training.\n\n"
         "9. CATASTROPHIC FORGETTING:\n"
         "When trained sequentially on multiple tasks, learning new tasks overwrites knowledge from old tasks. The network 'forgets' previous knowledge when backpropagation updates all weights. Solution: Elastic Weight Consolidation (EWC), progressive networks.\n\n"
         "CONCLUSION:\n"
         "Backpropagation remains the cornerstone algorithm of modern AI despite its limitations. The combination of ReLU activations, batch normalization, residual connections, and Adam optimizer has addressed the most critical issues (vanishing gradient, slow convergence). Without backpropagation, the deep learning revolution — which transformed computer vision, NLP, and virtually every AI application — would not have been possible.", C['purple'], C['pl']),

        ("Q2(b) Compare recurrent and feed-forward neural networks. [2024 — 5M]",
         "5 Marks — 500–800 words", "2024",
         "RECURRENT vs FEEDFORWARD NEURAL NETWORKS — COMPARISON\n\n"
         "FEEDFORWARD NEURAL NETWORK (FFNN):\n"
         "Information flows in ONE DIRECTION only — from input layer through hidden layers to output layer. No cycles, no feedback connections. Each layer's output becomes the next layer's input.\n\n"
         "Architecture: Input → Hidden1 → Hidden2 → ... → Output\n"
         "Computation: y = f(W2 · f(W1 · x + b1) + b2)\n\n"
         "Training: Standard backpropagation on fixed-size inputs.\n"
         "Input requirement: FIXED size — must always receive the same number of features.\n"
         "Memory: NONE — processes each input independently. No memory of past inputs.\n\n"
         "RECURRENT NEURAL NETWORK (RNN):\n"
         "Has FEEDBACK connections — output at time t feeds back as input at time t+1.\n\n"
         "Architecture: Input → [Hidden + Feedback] → Output (at each time step)\n"
         "Computation: h(t) = f(Wx·x(t) + Wh·h(t-1) + b), y(t) = g(Wy·h(t) + by)\n\n"
         "Training: Backpropagation Through Time (BPTT) — unroll through T time steps then backpropagate.\n"
         "Input requirement: VARIABLE length sequences — handles sequences of any length.\n"
         "Memory: YES — hidden state h(t) carries information from past time steps.\n\n"
         "DETAILED COMPARISON:\n\n"
         "1. INFORMATION FLOW:\n"
         "FFNN: Unidirectional — input → output, no loops.\n"
         "RNN: Has cycles — output feeds back as future input.\n\n"
         "2. TEMPORAL CAPABILITY:\n"
         "FFNN: No temporal understanding. Treats each sample independently.\n"
         "RNN: Inherent temporal processing. Remembers past context.\n\n"
         "3. INPUT/OUTPUT TYPE:\n"
         "FFNN: Fixed-size input → fixed-size output.\n"
         "RNN: Variable-length sequences (one-to-many, many-to-one, many-to-many).\n\n"
         "4. PARAMETERS:\n"
         "FFNN: Different weights for each layer.\n"
         "RNN: Same weights Wx, Wh SHARED across all time steps.\n\n"
         "5. TRAINING COMPLEXITY:\n"
         "FFNN: Standard backpropagation — relatively simple.\n"
         "RNN: BPTT — more complex, suffers from vanishing/exploding gradients.\n\n"
         "6. BEST APPLICATIONS:\n"
         "FFNN: Image classification, tabular data, regression — where temporal order doesn't matter.\n"
         "RNN: Text processing, speech recognition, time-series, machine translation — sequential data.\n\n"
         "7. EXAMPLES:\n"
         "FFNN: MLP, CNN (for images), Perceptron.\n"
         "RNN: LSTM, GRU, Vanilla RNN, Bidirectional RNN.\n\n"
         "8. GRADIENT ISSUES:\n"
         "FFNN: Standard vanishing gradient — addressed by ReLU.\n"
         "RNN: Severe vanishing gradient through time — requires LSTM/GRU gating mechanisms.\n\n"
         "CONCLUSION:\n"
         "FFNN is the workhorse for non-sequential tasks — simpler, faster, more stable training. RNN is essential for sequential tasks where temporal context matters. In practice, LSTM/GRU (improved RNNs) are used for sequential data, while Transformers now dominate NLP but are computationally heavier.", C['purple'], C['pl']),

        ("Q3(a) Explain every step of the Genetic Algorithm in detail. [2024 — 10M]",
         "10 Marks — 800–1200 words", "2024",
         "GENETIC ALGORITHM — EVERY STEP IN COMPLETE DETAIL\n\n"
         "INTRODUCTION:\n"
         "A Genetic Algorithm is a population-based optimization technique inspired by biological evolution. It maintains a population of candidate solutions (chromosomes) and evolves them through biologically-inspired operators over multiple generations.\n\n"
         "STEP 1 — PROBLEM REPRESENTATION (ENCODING):\n"
         "Before running GA, each potential solution must be encoded as a CHROMOSOME.\n\n"
         "Binary Encoding: Each gene is 0 or 1. Most common.\n"
         "Example: Chromosome '10110' represents integer 22 (binary to decimal).\n"
         "Integer Encoding: Genes are integers. Example: [3,1,4,2,5] for city visit order in TSP.\n"
         "Real-Valued: Genes are real numbers. Example: [1.5, 2.3, 0.7] for optimization parameters.\n"
         "Permutation: Each gene is a position. Used when order matters (TSP, scheduling).\n\n"
         "STEP 2 — INITIALIZE POPULATION:\n"
         "Randomly generate N chromosomes as the initial population. N = 50 to 500 (problem-dependent).\n"
         "Each chromosome is created by randomly assigning values to each gene.\n"
         "Example (Binary, 6-bit, N=4):\n"
         "Population = {110101, 011010, 100111, 001101}\n"
         "= {53, 26, 39, 13} as decimal values.\n"
         "Population diversity is crucial — too uniform → premature convergence.\n\n"
         "STEP 3 — EVALUATE FITNESS:\n"
         "Compute the FITNESS VALUE f(chromosome) for each individual using the FITNESS FUNCTION.\n"
         "The fitness function defines the objective — what we're optimizing.\n\n"
         "Example (Maximize f(x) = x², 6-bit binary):\n"
         "110101 → x=53 → f=2809\n"
         "011010 → x=26 → f=676\n"
         "100111 → x=39 → f=1521\n"
         "001101 → x=13 → f=169\n"
         "Total fitness = 5175.\n\n"
         "STEP 4 — CHECK TERMINATION CONDITION:\n"
         "Stop if any of these conditions are met:\n"
         "a) Maximum number of generations reached (e.g., 1000 generations).\n"
         "b) Best fitness exceeds a threshold (e.g., fitness > 3500).\n"
         "c) Population has converged (all chromosomes nearly identical).\n"
         "d) Fitness has not improved for K consecutive generations (stagnation).\n"
         "If not terminated → proceed to selection.\n\n"
         "STEP 5 — SELECTION:\n"
         "Select which chromosomes become PARENTS for the next generation.\n"
         "Better fitness = higher probability of being selected.\n\n"
         "a) Roulette Wheel Selection:\n"
         "P(i) = f(i) / Σf(j)\n"
         "P(110101) = 2809/5175 = 0.543 → 54.3% chance of selection\n"
         "P(011010) = 676/5175 = 0.131 → 13.1% chance\n"
         "P(100111) = 1521/5175 = 0.294 → 29.4% chance\n"
         "P(001101) = 169/5175 = 0.033 → 3.3% chance\n"
         "Spin virtual roulette wheel N times to get N parents.\n\n"
         "b) Tournament Selection (alternative):\n"
         "Pick k random chromosomes, select the best among them. Repeat N times.\n\n"
         "c) Elitism: ALWAYS copy best individual(s) unchanged to next generation.\n\n"
         "STEP 6 — CROSSOVER (RECOMBINATION):\n"
         "Combine two parent chromosomes to create offspring.\n"
         "Applied with probability Pc (crossover rate) ≈ 0.6 to 0.9.\n\n"
         "Single-Point Crossover:\n"
         "Choose random crossover point k (e.g., k=3).\n"
         "Parent 1: 110 | 101 → Offspring 1: 110 + 010 = 110010\n"
         "Parent 2: 011 | 010 → Offspring 2: 011 + 101 = 011101\n\n"
         "Two-Point Crossover:\n"
         "Two cut points k1=2, k2=4:\n"
         "P1: 11|0101|10 → C1: 11|1001|10\n"
         "P2: 00|1001|01 → C2: 00|0101|01\n\n"
         "If random number > Pc → offspring = copies of parents (no crossover).\n\n"
         "STEP 7 — MUTATION:\n"
         "Randomly alter one or more genes in the offspring.\n"
         "Applied with very small probability Pm ≈ 0.001 to 0.01.\n\n"
         "Bit-Flip Mutation: For each gene, flip with probability Pm.\n"
         "Before: 110010\n"
         "After: 110110 (bit 4 flipped from 0→1)\n\n"
         "Why so small? Too much mutation → random search (loses good solutions).\n"
         "Too little → population converges, cannot escape local optima.\n"
         "Purpose: Maintains genetic diversity. Introduces new genetic material.\n\n"
         "STEP 8 — FORM NEW GENERATION (REPLACEMENT):\n"
         "Create the new population from offspring.\n\n"
         "Generational Replacement: All N offspring replace all N parents completely.\n"
         "Elitist Strategy: Best k individuals from parents survive + (N-k) offspring.\n"
         "Steady-State: Only the worst k parents are replaced by best k offspring.\n\n"
         "STEP 9 — GO TO STEP 3 (Iterate):\n"
         "With new population, evaluate fitness again. Check termination. Continue cycle.\n\n"
         "Each complete cycle (Steps 3-8) = one GENERATION.\n"
         "Over many generations, average fitness INCREASES as better chromosomes reproduce more.\n\n"
         "EXAMPLE TRACE (f(x)=x², 6-bit binary, after 2 generations):\n"
         "Gen 0: Best=110101=53, f=2809, Avg f=1294.\n"
         "Gen 1: After selection+crossover+mutation: Best≈111001=57, f=3249, Avg f≈2100.\n"
         "Gen 10: Best≈111111=63, f=3969 (near maximum!), Avg f≈3500.\n\n"
         "PARAMETERS AND THEIR EFFECTS:\n"
         "Population size N: Larger=better diversity+exploration but slower. 50-500 typical.\n"
         "Crossover rate Pc: 0.6-0.9. Higher=more recombination.\n"
         "Mutation rate Pm: 0.001-0.01. Too high=random search. Too low=premature convergence.\n"
         "Elitism: Prevents losing best solution found. Always recommended.\n\n"
         "CONCLUSION:\n"
         "The GA cycle — Initialize → Evaluate → Select → Crossover → Mutate → Replace — elegantly mimics biological evolution. The interplay of selection (exploitation of good solutions), crossover (combination of building blocks), and mutation (exploration of new solutions) allows GA to efficiently navigate complex fitness landscapes.", C['purple'], C['pl']),

        ("Q3(b) Main difference between probability and fuzzy logic. [2024 — 5M]",
         "5 Marks — 500–800 words", "2024",
         "PROBABILITY vs FUZZY LOGIC — COMPLETE COMPARISON\n\n"
         "INTRODUCTION:\n"
         "Both probability theory and fuzzy logic deal with UNCERTAINTY — situations where we don't have complete, perfect knowledge. However, they address FUNDAMENTALLY DIFFERENT TYPES of uncertainty:\n"
         "Probability handles STATISTICAL uncertainty — events that may or may not occur.\n"
         "Fuzzy logic handles LINGUISTIC uncertainty — vagueness in the meaning of words and concepts.\n\n"
         "CORE DISTINCTION:\n\n"
         "PROBABILITY:\n"
         "Answers: 'How LIKELY is this event to occur?'\n"
         "The event either OCCURS (becomes 1) or DOESN'T OCCUR (stays 0) — we just don't know which.\n"
         "P(Rain) = 0.7 means: There is a 70% CHANCE it will rain. Either it rains (1) or it doesn't (0). The uncertainty is about what WILL HAPPEN.\n\n"
         "FUZZY LOGIC:\n"
         "Answers: 'To what DEGREE does this element belong to this concept?'\n"
         "The element permanently belongs with a certain degree — there's no further resolution.\n"
         "μ_HOT(30°C) = 0.7 means: 30°C IS 'hot' with degree 0.7. The temperature IS 30°C. The uncertainty is about the MEANING of the word 'hot', not about the temperature value itself.\n\n"
         "DETAILED DIFFERENCES:\n\n"
         "1. NATURE OF UNCERTAINTY:\n"
         "Probability: Random/stochastic — future events, outcomes of experiments.\n"
         "Fuzzy: Linguistic/vague — imprecision in human language and concepts.\n\n"
         "2. MEMBERSHIP VALUES:\n"
         "Probability: P(A) measures likelihood of event A occurring. Sum P(A)+P(¬A)=1.\n"
         "Fuzzy: μ_A(x) measures degree of membership of x in fuzzy set A. μ_A(x)+μ_Ā(x)=1 too, BUT they can BOTH be non-zero (partial membership).\n\n"
         "3. COMPLEMENT INTERPRETATION:\n"
         "Probability: P(A) + P(not A) = 1. If P(Rain)=0.7, P(No-Rain)=0.3. These are DISJOINT outcomes.\n"
         "Fuzzy: μ_A(x) + μ_Ā(x) = 1. But both can reflect partial truth simultaneously.\n"
         "Example: 30°C can be 70% HOT and 30% NOT-HOT — both are 'true' simultaneously.\n\n"
         "4. MATHEMATICAL FRAMEWORK:\n"
         "Probability: Based on Kolmogorov axioms. Requires statistical experiments, frequency data, or prior knowledge.\n"
         "Fuzzy: Based on fuzzy set theory. Membership functions designed by domain experts to capture human perception.\n\n"
         "5. OPERATIONS:\n"
         "Probability: P(A∩B) = P(A)·P(B) [independence]. P(A∪B) = P(A)+P(B)-P(A∩B).\n"
         "Fuzzy: μ_(A∩B)(x) = min(μ_A(x), μ_B(x)). μ_(A∪B)(x) = max(μ_A(x), μ_B(x)).\n\n"
         "6. EXAMPLES:\n"
         "Probability example: 'What is the probability a randomly selected person has flu?'\n"
         "→ P(Flu) = 0.05 (5% prevalence rate). Person either has flu or doesn't.\n\n"
         "Fuzzy example: 'To what degree is this person's temperature a fever?'\n"
         "→ μ_FEVER(38.5°C) = 0.6. The temperature is 38.5°C — we're not uncertain about it.\n"
         "The fuzziness is in the DEFINITION of 'fever', not in the temperature measurement.\n\n"
         "7. UPDATING:\n"
         "Probability: Can be updated with new evidence using Bayes' theorem.\n"
         "Fuzzy: Membership function doesn't update — it's a fixed definition.\n\n"
         "KEY ANALOGY:\n"
         "Probability: A glass is 50% likely to be filled (it either is or isn't, we're uncertain which).\n"
         "Fuzzy: A glass is 50% 'full' (it's partially full — this IS its state, no uncertainty).\n\n"
         "WHERE THEY COMBINE:\n"
         "Fuzzy Probability: Assigns probability to fuzzy events. 'What is the probability it will be very hot tomorrow?' combines both.\n"
         "Probabilistic Fuzzy Systems: Use probability distributions over fuzzy membership values.\n\n"
         "CONCLUSION:\n"
         "Probability and fuzzy logic are complementary, not competing. Probability handles random events and statistical uncertainty. Fuzzy logic handles imprecise concepts and vague language. Modern intelligent systems often use BOTH — fuzzy logic to model imprecise concepts and probability to model random uncertainty. Understanding the distinction is critical for choosing the right tool for a given problem.", C['purple'], C['pl']),

        ("Q4(a) Explain AO* Algorithm with example. [2024 — 10M]",
         "10 Marks — 800–1200 words", "2024",
         "AO* ALGORITHM — COMPLETE ANSWER WITH EXAMPLE\n\n"
         "INTRODUCTION:\n"
         "AO* (A O-Star) is a heuristic search algorithm for AND-OR graphs. While A* finds the optimal path in a standard state-space graph (where each node has alternative successor states — OR nodes), AO* handles AND-OR graphs where some nodes represent problems that MUST be decomposed into multiple sub-problems that ALL need to be solved (AND nodes).\n\n"
         "WHEN IS AO* USED?\n"
         "Problems naturally decompose into sub-problems. Example: To prove theorem T, you must prove BOTH Lemma L1 AND Lemma L2 (AND node). But T could also be proved by Method A OR Method B (OR node).\n\n"
         "TERMINOLOGY:\n"
         "OR node: Node with multiple alternative solutions — choose the CHEAPEST one.\n"
         "AND node: Node requiring ALL children to be solved. Cost = sum of all children's costs.\n"
         "Terminal node: Has a known solution. Cost = 0.\n"
         "h(n): Heuristic estimate of cost to solve node n.\n"
         "Solved node: A node with a complete solution.\n"
         "Solution tree: The tree of nodes that represents the complete solution.\n\n"
         "COST COMPUTATION:\n"
         "For OR node n with children c1, c2, c3 via arcs of cost k1, k2, k3:\n"
         "f(n) = min_i (ki + f(ci))   [choose cheapest alternative]\n\n"
         "For AND node n with children c1, c2, c3 via arcs of cost k1, k2, k3:\n"
         "f(n) = Σ_i (ki + f(ci))   [must pay for ALL children]\n\n"
         "AO* ALGORITHM — COMPLETE STEPS:\n\n"
         "Step 1 — INITIALIZE:\n"
         "Create the root node. Compute h(root). Set root as the current best partial solution tree (BPST).\n\n"
         "Step 2 — SELECT:\n"
         "From the current BPST, select the MOST PROMISING UNEXPANDED LEAF node (lowest estimated cost along the current best path).\n\n"
         "Step 3 — EXPAND:\n"
         "Expand the selected node — generate all its successors.\n"
         "For each successor:\n"
         "• If it's terminal (known solution): mark SOLVED, set cost = 0.\n"
         "• If it's a new node: compute h, add to graph.\n"
         "• If already in graph: may need to update if new path is cheaper.\n\n"
         "Step 4 — BACK-PROPAGATE:\n"
         "Update cost estimates backward from the expanded node to the root:\n"
         "For each OR node on path: f(n) = min_i (ki + f(ci)) → update best child pointer.\n"
         "For each AND node on path: f(n) = Σ_i (ki + f(ci)) → must recompute all.\n"
         "If all children of an AND node are SOLVED → mark AND node as SOLVED.\n"
         "If the chosen alternative of an OR node is SOLVED → mark OR node as SOLVED.\n\n"
         "Step 5 — CHECK:\n"
         "If root is SOLVED → return the marked solution tree. DONE.\n"
         "Else → go to Step 2 (select next node to expand from updated BPST).\n\n"
         "WORKED EXAMPLE:\n\n"
         "Problem Graph:\n"
         "A (root, OR node): can be solved by:\n"
         "  Option 1: B alone (arc cost 1)\n"
         "  Option 2: C AND D together (arc costs 1 each)\n"
         "B (OR node): can be solved by:\n"
         "  Option 1: E alone (arc cost 1) — E is terminal, cost=0\n"
         "  Option 2: F alone (arc cost 1) — F is terminal, cost=0\n"
         "C (terminal): cost = 0\n"
         "D (terminal): cost = 0\n\n"
         "Initial h values: h(A)=4, h(B)=3, h(C)=1, h(D)=2\n\n"
         "ITERATION 1 — Initialize:\n"
         "Graph: A with h=4. A is unexpanded. Select A.\n\n"
         "ITERATION 2 — Expand A:\n"
         "Generate children:\n"
         "Option 1: A → B (arc cost=1). Cost via B: 1 + h(B) = 1 + 3 = 4.\n"
         "Option 2: A → {C AND D} (arc costs=1 each). Cost: (1+h(C)) + (1+h(D)) = (1+1) + (1+2) = 5.\n"
         "f(A) = min(4, 5) = 4. Best choice: A → B. Mark A's pointer → B.\n\n"
         "BPST: A → B. Select B (most promising unexpanded leaf).\n\n"
         "ITERATION 3 — Expand B:\n"
         "B is OR node with options:\n"
         "Option 1: B → E (arc cost=1). E is terminal. Cost: 1 + 0 = 1.\n"
         "Option 2: B → F (arc cost=1). F is terminal. Cost: 1 + 0 = 1.\n"
         "f(B) = min(1, 1) = 1. B is SOLVED (E and F are both terminal, pick E).\n"
         "Mark B as SOLVED with cost 1.\n\n"
         "BACK-PROPAGATE to A:\n"
         "f(A) via B = 1 (arc cost) + 1 (f(B)) = 2.\n"
         "f(A) via {C,D} = 2 + 3 = 5.\n"
         "f(A) = min(2, 5) = 2. Best: A → B. Since B is SOLVED, A is SOLVED.\n\n"
         "SOLUTION TREE: A → B → E with total cost 2.\n\n"
         "ANOTHER EXAMPLE — Proving theorem:\n"
         "Goal: Prove T. T can be proved by: Method A (cost 3) OR (Method B AND Method C).\n"
         "Method B has cost 2. Method C has cost 4. Method A has cost 3.\n"
         "Cost via A: 3.\n"
         "Cost via B∧C: 2+4=6.\n"
         "AO* chooses Method A (cost 3) as optimal.\n\n"
         "DIFFERENCE FROM A*:\n"
         "A*: Only OR nodes — find optimal PATH.\n"
         "AO*: Both AND and OR nodes — find optimal SOLUTION TREE.\n"
         "A*: Single goal node — one terminal state.\n"
         "AO*: Multiple terminal nodes may all need to be solved.\n\n"
         "COMPLETENESS AND OPTIMALITY:\n"
         "AO* is COMPLETE (finds solution if one exists) and OPTIMAL (finds minimum-cost solution tree) when heuristic h is admissible (h(n) ≤ h*(n)).\n\n"
         "APPLICATIONS:\n"
         "Theorem proving (proving theorem by sub-lemmas), robot planning (achieve goal by AND of sub-goals), game tree search with AND-OR structure, problem decomposition in expert systems.\n\n"
         "CONCLUSION:\n"
         "AO* elegantly extends heuristic search to the richer AND-OR graph formalism, enabling AI systems to solve decomposable problems optimally. The combination of AND-OR structure with admissible heuristics and backward cost propagation makes it a powerful and theoretically sound algorithm for complex planning and reasoning tasks.", C['purple'], C['pl']),

        ("Q7 Draw and describe architecture of Expert System. [2024 — 15M]",
         "15 Marks — 1200–1500 words", "2024",
         "EXPERT SYSTEM ARCHITECTURE — COMPLETE 15-MARK ANSWER\n\n"
         "INTRODUCTION TO EXPERT SYSTEMS:\n"
         "An Expert System (ES) is a Knowledge-Based AI system that captures the specialized knowledge of human experts in a particular domain and applies automated reasoning to solve complex problems at expert level. The concept emerged from the Stanford Heuristic Programming Project in the late 1960s and 1970s.\n\n"
         "The fundamental insight behind expert systems: Human experts solve problems by applying domain-specific knowledge (facts + rules + heuristics) through systematic reasoning. If we can capture this knowledge formally and implement a reasoning engine, a computer can replicate expert-level performance.\n\n"
         "Historical Examples:\n"
         "DENDRAL (1965): Determined chemical molecular structure from mass spectrometry.\n"
         "MYCIN (1974): Diagnosed bacterial infections and recommended antibiotics. Matched specialist physicians.\n"
         "XCON (1982): Configured DEC computer systems — saved $40M annually.\n"
         "PROSPECTOR: Discovered a $100M molybdenum deposit.\n\n"
         "COMPLETE ARCHITECTURE — SIX COMPONENTS:\n\n"
         "COMPONENT 1: KNOWLEDGE BASE (KB)\n"
         "The CORE and HEART of the expert system. Contains all domain knowledge in formalized structures.\n\n"
         "Types of knowledge stored:\n"
         "a) Factual Knowledge: Established, objectively true facts about the domain.\n"
         "   'Gram-negative bacteria are resistant to penicillin-based antibiotics.'\n"
         "   'Body temperature > 38°C (100.4°F) constitutes fever in adults.'\n\n"
         "b) Heuristic Knowledge: Rules of thumb, experiential knowledge, best practices.\n"
         "   'If a patient has not improved after 48 hours on antibiotic A, switch to antibiotic B.'\n"
         "   'Fever without cough in elderly patients — consider UTI before respiratory infection.'\n\n"
         "c) Production Rules (IF-THEN Rules): The primary knowledge representation format.\n"
         "   Rule R1: IF (organism-type = gram-negative) AND (morphology = rod-shaped)\n"
         "            THEN (pseudomonas-suspected = TRUE) [CF = 0.6]\n"
         "   Rule R2: IF (patient-has = burn-wound)\n"
         "            THEN (pseudomonas-suspected = TRUE) [CF = 0.4]\n"
         "   Rule R3: IF (pseudomonas-suspected = TRUE) AND (WBC-count = elevated)\n"
         "            THEN (diagnosis = pseudomonas-aeruginosa) [CF = 0.7]\n"
         "   Rule R4: IF (diagnosis = pseudomonas-aeruginosa)\n"
         "            THEN (recommend = gentamicin + carbenicillin) [CF = 0.85]\n\n"
         "d) Control Knowledge: Knowledge about when and how to use other knowledge.\n"
         "   Priority levels for rules, conflict resolution strategies.\n\n"
         "The KB is SEPARATE from the inference engine. This modularity allows:\n"
         "• Domain experts to update rules without programming knowledge.\n"
         "• Adding new rules without disrupting existing ones.\n"
         "• Different KBs with the same inference engine for different domains.\n\n"
         "COMPONENT 2: WORKING MEMORY (WM) / GLOBAL DATABASE\n"
         "Stores the CURRENT STATE of the specific problem being solved.\n"
         "Contents: User-provided patient data, laboratory results, derived facts, intermediate conclusions, current goals.\n"
         "Dynamically updated: As new information arrives (user answers, derived facts), WM grows.\n"
         "Example WM state:\n"
         "{Patient=Smith, Age=52, Diagnosis=?, Organism-type=gram-negative,\n"
         "  Morphology=rod-shaped, Burn-wound=YES, WBC-count=elevated, Temperature=103°F}\n\n"
         "COMPONENT 3: INFERENCE ENGINE (The Reasoning Core)\n"
         "Applies knowledge from KB to facts in WM to derive new conclusions.\n\n"
         "FORWARD CHAINING (Data-Driven Inference):\n"
         "Algorithm:\n"
         "1. Scan ALL rules in KB. Find rules whose IF conditions match current WM facts. These form the CONFLICT SET.\n"
         "2. Apply CONFLICT RESOLUTION to select which rule to fire:\n"
         "   • Specificity: Most specific rule (most conditions) wins.\n"
         "   • Recency: Rule matching most recently added fact wins.\n"
         "   • Priority: Manually assigned numerical priority.\n"
         "   • Refractoriness: Never fire same rule on same data twice.\n"
         "3. FIRE selected rule: Add THEN conclusion to WM.\n"
         "4. Repeat until: goal found, no more rules fire, or max iterations.\n\n"
         "Trace example with above KB and WM:\n"
         "Initial WM: {gram-negative=T, rod-shaped=T, burn-wound=T, WBC-elevated=T}\n"
         "Round 1: R1 matches (gram-negative∧rod-shaped→pseudomonas-suspected). Fire R1. WM: +{pseudomonas-suspected=T, CF=0.6}\n"
         "Round 1: R2 matches (burn-wound→pseudomonas-suspected). Fire R2. WM: CF updated using combination: 0.6+0.4×(1-0.6)=0.76.\n"
         "Round 2: R3 matches (pseudomonas-suspected∧WBC-elevated→diagnosis). Fire R3. WM: +{diagnosis=pseudomonas, CF=0.7×0.76=0.53}\n"
         "Round 3: R4 matches. Fire R4. WM: +{recommend=gentamicin, CF=0.85×0.53=0.45}\n"
         "Forward chaining reveals ALL possible conclusions from given data.\n\n"
         "BACKWARD CHAINING (Goal-Driven Inference):\n"
         "Algorithm:\n"
         "1. Start with specific GOAL (hypothesis to prove). Example: Goal = 'Is diagnosis=pseudomonas?'\n"
         "2. Find rules whose THEN part matches the goal. Example: R3.\n"
         "3. R3's IF conditions become SUB-GOALS: pseudomonas-suspected=T AND WBC=elevated.\n"
         "4. Recursively prove each sub-goal:\n"
         "   For pseudomonas-suspected: find R1, R2. Their conditions → sub-sub-goals.\n"
         "   If conditions are directly in WM → satisfied.\n"
         "   If not in WM → ASK USER: 'Is organism gram-negative?'\n"
         "5. If all sub-goals satisfied → original goal proven.\n"
         "Used for diagnosis, question-answering, hypothesis testing.\n\n"
         "COMPONENT 4: EXPLANATION FACILITY\n"
         "Critical for user trust and system validation.\n\n"
         "WHY module:\n"
         "User: 'Why are you asking if organism is gram-negative?'\n"
         "System: 'Because Rule R1 requires gram-negative AND rod-shaped to conclude pseudomonas is suspected, which is needed to prove the current goal: diagnose pseudomonas.'\n\n"
         "HOW module:\n"
         "User: 'How did you conclude pseudomonas?'\n"
         "System: 'Fired R1 (gram-negative+rod→pseudomonas-suspected, CF=0.6). Fired R2 (burn-wound→pseudomonas-suspected, CF=0.4). Combined CF=0.76. Fired R3 (suspected+WBC-high→diagnose, CF=0.7). Final diagnosis CF=0.53.'\n\n"
         "The explanation facility logs all rule firings and produces human-readable explanations.\n\n"
         "COMPONENT 5: KNOWLEDGE ACQUISITION FACILITY\n"
         "The interface for DOMAIN EXPERTS to enter and maintain knowledge.\n"
         "Features: Rule editor with syntax checking, consistency detector (conflicting rules), completeness checker (missing rule coverage).\n"
         "Modern systems: Machine learning from historical cases to semi-automatically derive rules.\n"
         "Challenge: KNOWLEDGE ACQUISITION BOTTLENECK — extracting knowledge from experts is slow, expensive, and difficult (experts often don't know HOW they know things — tacit knowledge).\n\n"
         "COMPONENT 6: USER INTERFACE\n"
         "Provides user-friendly interaction:\n"
         "• Presents questions in natural language (not code).\n"
         "• Accepts answers as text, menus, or structured forms.\n"
         "• Displays conclusions with confidence levels and evidence.\n"
         "• Provides WHY/HOW explanations on request.\n"
         "• Designed for domain professionals (doctors, engineers) — not programmers.\n\n"
         "ARCHITECTURE DIAGRAM:\n"
         "[Domain Expert] → [Knowledge Acquisition Facility] → [Knowledge Base]\n"
         "                                                              ↕\n"
         "[User] ↔ [User Interface] ↔ [Inference Engine] ↔ [Working Memory]\n"
         "                                    ↕\n"
         "                         [Explanation Facility]\n\n"
         "CHARACTERISTICS OF EXPERT SYSTEMS:\n"
         "1. High Performance: Expert-level accuracy in the domain.\n"
         "2. Reliability: Consistent — same inputs always produce same outputs.\n"
         "3. Explainability: Always explains HOW and WHY.\n"
         "4. Availability: 24/7, unlimited copies, no fatigue, no emotional bias.\n"
         "5. Transparency: Knowledge is explicit and inspectable.\n\n"
         "LIMITATIONS:\n"
         "1. Knowledge Acquisition Bottleneck: Extracting expert knowledge is slow and expensive.\n"
         "2. Brittleness: Fails outside its narrow domain.\n"
         "3. No Common Sense: Cannot reason about unexpected situations.\n"
         "4. Cannot Learn: Rules must be manually updated — no automatic learning from new cases.\n"
         "5. Narrow Scope: Each system is expert in one domain only.\n\n"
         "CONCLUSION:\n"
         "Expert systems demonstrated that AI could achieve human-expert performance in specific domains, establishing knowledge representation, reasoning, and explanation as core AI capabilities. While modern machine learning often achieves higher accuracy, expert systems remain valuable where EXPLAINABILITY is mandatory (medical regulations, legal systems, financial compliance) — domains where 'black box' ML predictions are insufficient.", C['purple'], C['pl']),
    ]:
        for item in qa(q, marks, years, ans, c, bg):
            story.append(item)

    story.append(PageBreak())

    # ════════════════════ 2023 SPECIFIC QUESTIONS ══════════════════════════
    story.append(ban("MAY 2023 EXAM — COMPLETE PAPER WITH ALL ANSWERS", C['maroon']))
    story.append(Spacer(1, 0.2*cm))
    story.append(ibox("003601 | May 2023 | B.Tech CE/IT 6th Sem | Max Marks: 75 | Time: 3 Hrs",
                      C['ml'], C['maroon']))
    story.append(Spacer(1, 0.2*cm))
    story.append(ban("2023 — PART A (1.5 Marks Each — 100 Words)", C['maroon']))

    for q, years, c,ans in [
        ("(e) Semantic Net for: 'Cycle is a two-wheeler and a moving vehicle. Vehicle needs engine, fuel system, electric system, also used by children for racing.'",
         "2023 Part A", C['maroon'],
         "Semantic Network for Cycle:\n\n"
         "Nodes: Cycle, Vehicle, Two-Wheeler, Engine, FuelSystem, ElectricSystem, Lights, Horn, Brakes, Children, Racing\n\n"
         "Arcs:\n"
         "Cycle ──IS-A──► Two-Wheeler\n"
         "Cycle ──IS-A──► Vehicle\n"
         "Cycle ──IS-A──► Moving-Vehicle\n"
         "Vehicle ──NEEDS──► Engine\n"
         "Vehicle ──NEEDS──► FuelSystem [sustains engine]\n"
         "Vehicle ──HAS──► ElectricSystem [for lights, horn, brakes]\n"
         "ElectricSystem ──PROVIDES──► Lights\n"
         "ElectricSystem ──PROVIDES──► Horn\n"
         "ElectricSystem ──PROVIDES──► Brakes\n"
         "Cycle ──USED-BY──► Children\n"
         "Children ──USE-FOR──► Racing\n"
         "Children ──USE-FOR──► Enjoying\n\n"
         "By inheritance: Cycle (IS-A Vehicle) NEEDS Engine, FuelSystem, HAS ElectricSystem."),

        ("(i) Represent: 'The cookies were eaten in the kitchen under the table by the baker' using Thematic Role Frame.",
         "2023 Part A", C['maroon'],
         "Thematic Role Frame Representation:\n\n"
         "EVENT: Eating\n"
         "AGENT (doer of action): Baker\n"
         "OBJECT/THEME (thing affected): Cookies\n"
         "LOCATION (where action occurred): Kitchen\n"
         "POSITION (specific location detail): Under the table\n"
         "TENSE: Past (were eaten — passive voice)\n\n"
         "Frame notation:\n"
         "FRAME: EatingEvent\n"
         "| Slot: Agent = Baker\n"
         "| Slot: Object = Cookies\n"
         "| Slot: Action = Eat\n"
         "| Slot: Location = Kitchen\n"
         "| Slot: Position = Under the table\n"
         "| Slot: Tense = Past\n\n"
         "Note: Passive voice 'were eaten by the baker' = Active 'baker ate cookies'. Thematic roles remain the same regardless of grammatical voice."),

        ("(j) Differentiate between Supervised and Unsupervised Learning.",
         "2023 Part A", C['maroon'],
         "Supervised vs Unsupervised Learning:\n\n"
         "SUPERVISED LEARNING:\n"
         "Training data has INPUT-OUTPUT pairs (labeled). Algorithm learns mapping f: X→Y.\n"
         "Regression: Continuous output (predict salary, temperature).\n"
         "Classification: Categorical output (spam/ham, disease type).\n"
         "Examples: Linear Regression, Decision Trees, SVM, Neural Networks.\n"
         "Applications: Medical diagnosis, image classification, speech recognition.\n\n"
         "UNSUPERVISED LEARNING:\n"
         "Training data has INPUTS ONLY — no labels. Algorithm discovers hidden structure.\n"
         "Clustering: Group similar data (K-means, DBSCAN).\n"
         "Dimensionality Reduction: Compress features (PCA, t-SNE).\n"
         "Examples: K-means, Autoencoders, GANs.\n"
         "Applications: Customer segmentation, anomaly detection, data compression.\n\n"
         "Key difference: Supervised needs labels (expensive); Unsupervised doesn't (cheap but harder to evaluate)."),
    ]:
        for item in qa(q, "1.5 Marks — 100 words", years, ans, c, C['ml']):
            story.append(item)

    story.append(Spacer(1, 0.2*cm))
    story.append(ban("2023 — PART B Specific Questions", C['maroon']))

    for q, marks, years, ans, c,bg in [
        ("Q7(a)(b)(c) Explain: Bayesian Reasoning & Bayesian Network, Dempster-Shafer Theory with derivation, Induction Learning. [2023 — 15M = 5+5+5]",
         "15 Marks — 1200–1500 words", "2023",
         "PART (a): BAYESIAN REASONING AND BAYESIAN NETWORK\n\n"
         "BAYESIAN REASONING:\n"
         "Bayesian reasoning is a probabilistic framework for updating beliefs about hypotheses when new evidence is observed. Based on Bayes' Theorem (Thomas Bayes, 1763):\n\n"
         "P(H|E) = [P(E|H) × P(H)] / P(E)\n\n"
         "P(H) = Prior: initial belief in hypothesis.\n"
         "P(E|H) = Likelihood: how well hypothesis explains evidence.\n"
         "P(H|E) = Posterior: updated belief after seeing evidence.\n"
         "P(E) = Marginal = P(E|H)·P(H) + P(E|¬H)·P(¬H).\n\n"
         "Example:\n"
         "P(Disease)=0.02, P(Test+|Disease)=0.95, P(Test+|No-Disease)=0.05.\n"
         "P(Test+) = 0.95×0.02 + 0.05×0.98 = 0.019+0.049 = 0.068.\n"
         "P(Disease|Test+) = (0.95×0.02)/0.068 = 0.019/0.068 = 0.279 = 27.9%.\n"
         "Even with positive test, only 27.9% chance — LOW prior dominates!\n\n"
         "Sequential updating: P(H|E1,E2) ∝ P(E2|H)×P(E1|H)×P(H) [if independent].\n"
         "Each new evidence refines belief. Posterior becomes new prior.\n\n"
         "BAYESIAN NETWORKS:\n"
         "A Directed Acyclic Graph (DAG) where:\n"
         "Nodes = random variables (events, features, hypotheses).\n"
         "Edges = direct probabilistic causal dependencies.\n"
         "Each node has Conditional Probability Table (CPT): P(node | parent states).\n\n"
         "Classic Example — Burglary Alarm Network:\n"
         "Structure: Burglary(B) → Alarm(A) ← Earthquake(E); Alarm → JohnCalls(J); Alarm → MaryCalls(M)\n"
         "P(B)=0.001; P(E)=0.002\n"
         "CPT for Alarm: P(A|B,E)=0.95, P(A|B,¬E)=0.94, P(A|¬B,E)=0.29, P(A|¬B,¬E)=0.001\n"
         "P(J|A)=0.90, P(M|A)=0.70\n\n"
         "Query: P(Burglary|JohnCalls=T, MaryCalls=T) — computed by belief propagation.\n\n"
         "Advantages: Compact (O(n·2^k) vs O(2^n)), supports diagnostic+predictive reasoning, handles missing data.\n\n"
         "---\n\n"
         "PART (b): DEMPSTER-SHAFER THEORY WITH DERIVATION\n\n"
         "MOTIVATION:\n"
         "Probability theory forces us to distribute probability even when we have NO information about some hypotheses. DS Theory explicitly models IGNORANCE.\n\n"
         "MATHEMATICAL FRAMEWORK:\n\n"
         "Frame of Discernment Θ: Complete set of mutually exclusive hypotheses.\n"
         "Θ = {H1, H2, H3, ...Hn}\n\n"
         "Power Set 2^Θ: All possible subsets. For Θ={A,B}: 2^Θ = {∅,{A},{B},{A,B}}.\n\n"
         "Mass Function m (Basic Probability Assignment):\n"
         "m: 2^Θ → [0,1] satisfying:\n"
         "1. m(∅) = 0\n"
         "2. Σ{A⊆Θ} m(A) = 1\n\n"
         "Interpretation: m(A) = degree of evidence SPECIFICALLY supporting set A and NOTHING smaller.\n"
         "m(Θ) = IGNORANCE — evidence doesn't specify which subset.\n\n"
         "BELIEF AND PLAUSIBILITY:\n"
         "Bel(A) = Σ{B⊆A} m(B) = total belief committed to A.\n"
         "Pl(A) = Σ{B:B∩A≠∅} m(B) = 1 - Bel(¬A) = maximum possible belief in A.\n"
         "Interval [Bel(A), Pl(A)] = range of possible probability of A.\n\n"
         "DEMPSTER'S COMBINATION RULE (Derivation):\n"
         "Given two INDEPENDENT sources with mass functions m1, m2:\n\n"
         "For non-empty A:\n"
         "(m1⊕m2)(A) = Σ{B∩C=A} m1(B)·m2(C) / (1-K)\n\n"
         "K = Σ{B∩C=∅} m1(B)·m2(C) = conflict between sources.\n\n"
         "Derivation: Unnormalized combined mass for set A = sum of all product pairs (m1(B), m2(C)) where their intersection equals A. Normalize by dividing by (1-K) to exclude contradicting evidence (where B∩C=∅ contributes to conflict K).\n\n"
         "Example:\n"
         "Θ = {Disease(D), NoDis(N)}.\n"
         "Doctor 1: m1({D})=0.7, m1(Θ)=0.3.\n"
         "Doctor 2: m2({N})=0.6, m2(Θ)=0.4.\n\n"
         "Products:\n"
         "m1({D})×m2({N}) = 0.7×0.6=0.42 → {D}∩{N}=∅ → K=0.42\n"
         "m1({D})×m2(Θ) = 0.7×0.4=0.28 → {D}∩Θ={D} → m({D})+=0.28\n"
         "m1(Θ)×m2({N}) = 0.3×0.6=0.18 → Θ∩{N}={N} → m({N})+=0.18\n"
         "m1(Θ)×m2(Θ) = 0.3×0.4=0.12 → m(Θ)+=0.12\n\n"
         "K=0.42, (1-K)=0.58.\n"
         "m({D})=0.28/0.58≈0.483, m({N})=0.18/0.58≈0.310, m(Θ)=0.12/0.58≈0.207.\n\n"
         "Advantages: Models ignorance, assigns belief to sets, no priors needed.\n"
         "Disadvantages: O(2^n) complexity, counter-intuitive with high conflict.\n\n"
         "---\n\n"
         "PART (c): INDUCTION LEARNING\n\n"
         "DEFINITION:\n"
         "Induction learning (Inductive Machine Learning) is the process of deriving GENERAL rules or hypotheses from SPECIFIC training examples. It is the primary mechanism by which AI systems learn from data.\n\n"
         "Induction vs Deduction:\n"
         "Deduction: General rule → Specific conclusion. Logically guaranteed.\n"
         "Induction: Specific examples → General rule. Probable, not guaranteed.\n\n"
         "CONCEPT LEARNING:\n"
         "Given positive (+) and negative (−) examples, find a hypothesis H that covers all positives and none of the negatives.\n"
         "Example: PlayTennis learning — 14 weather examples → decision tree rules.\n\n"
         "ID3 ALGORITHM (Most Important Induction Algorithm):\n"
         "Builds decision tree by recursively selecting best splitting feature.\n\n"
         "Key formulas:\n"
         "Entropy: H(S) = −Σpi·log2(pi)\n"
         "H=0: Pure node (all one class — best!)\n"
         "H=1: Equal split (worst — no information)\n\n"
         "Information Gain: IG(S,A) = H(S) − Σ(|Sv|/|S|)·H(Sv)\n"
         "= How much does feature A reduce uncertainty?\n"
         "Select feature with MAXIMUM IG at each node.\n\n"
         "ID3 Trace (PlayTennis, 14 examples, 9 YES, 5 NO):\n"
         "H(root) = -(9/14)log(9/14) - (5/14)log(5/14) = 0.940 bits\n"
         "IG(Outlook) = 0.940 - (5/14)·0.971 - (4/14)·0 - (5/14)·0.971 = 0.246 bits\n"
         "IG(Humidity) = 0.151, IG(Wind) = 0.048, IG(Temp) = 0.029\n"
         "Outlook has HIGHEST IG → split on Outlook first!\n"
         "Overcast branch → all YES → leaf node: PlayTennis=YES.\n"
         "Sunny and Rain branches → recurse with remaining features.\n\n"
         "VERSION SPACE LEARNING (Candidate Elimination):\n"
         "Maintains ALL consistent hypotheses bounded by:\n"
         "S-boundary: Most specific hypotheses.\n"
         "G-boundary: Most general hypotheses.\n"
         "Positive example → Generalize S, restrict G.\n"
         "Negative example → Specialize G, restrict S.\n"
         "Converges when S=G → unique hypothesis found.\n\n"
         "APPLICATIONS:\n"
         "Medical diagnosis (learn from patient cases), fraud detection, spam filtering, recommendation systems, game playing (learn strategies from game records).\n\n"
         "CONCLUSION:\n"
         "Induction learning is the foundation of machine learning. ID3 demonstrated that computers can automatically discover decision rules from examples without explicit programming. Version Space showed that learning can be viewed as constraint satisfaction over hypothesis spaces. Together these ideas catalyzed the ML revolution.", C['maroon'], C['ml']),
    ]:
        for item in qa(q, marks, years, ans, c, bg):
            story.append(item)

    story.append(PageBreak())

    # FINAL REVISION
    story.append(ban("FINAL QUICK REVISION — ALL KEY FORMULAS", C['navy']))
    story.append(Spacer(1, 0.2*cm))
    story.append(ibox("📌 KEY FORMULAS TO MEMORIZE BEFORE EXAM", C['yl'], C['orange']))
    story.append(Spacer(1, 0.2*cm))

    rev = ctab([
        ["FORMULA / CONCEPT", "EXPRESSION", "TOPIC"],
        ["Bayes Theorem", "P(H|E) = P(E|H)·P(H) / P(E)", "Bayesian"],
        ["Total Probability", "P(E) = P(E|H)·P(H) + P(E|¬H)·P(¬H)", "Bayesian"],
        ["Naive Bayes", "P(C|f1..fn) ∝ P(C)·ΠP(fi|C)", "Bayesian"],
        ["CF Formula", "CF = MB − MD  |  Range: -1 to +1", "CF"],
        ["CF Both Positive", "CF = CF1 + CF2·(1−CF1)", "CF"],
        ["CF Chained", "CF_concl = CF_ante × CF_rule", "CF"],
        ["DS Belief", "Bel(A) = Σ m(B) for B⊆A", "DS Theory"],
        ["DS Plausibility", "Pl(A) = 1 − Bel(¬A)", "DS Theory"],
        ["DS Combination", "(m1⊕m2)(A) = Σm1(B)·m2(C) for B∩C=A / (1−K)", "DS Theory"],
        ["A* Evaluation", "f(n) = g(n) + h(n)", "A*"],
        ["Admissibility", "h(n) ≤ h*(n) — never overestimate", "A*"],
        ["AO* OR node", "f(n) = min_i(arc_i + f(child_i))", "AO*"],
        ["AO* AND node", "f(n) = Σ_i(arc_i + f(child_i))", "AO*"],
        ["BFS Complexity", "Time=O(b^d) Space=O(b^d) — HIGH memory", "BFS"],
        ["DFS Complexity", "Time=O(b^m) Space=O(b·m) — LOW memory", "DFS"],
        ["IDDFS", "Complete+Optimal+O(b·d) space — BEST choice", "IDDFS"],
        ["Entropy (ID3)", "H(S) = −Σpi·log2(pi)", "Induction"],
        ["Info Gain", "IG(S,A) = H(S) − Σ(|Sv|/|S|)·H(Sv)", "Induction"],
        ["Perceptron", "y=1 if Σ(wi·xi)+b≥0 else 0 | Δwi=η·(t−y)·xi", "ANN"],
        ["Backprop Output δ", "δk = (tk−yk)·f'(net_k)", "Backprop"],
        ["Backprop Hidden δ", "δj = f'(net_j)·Σ(δk·wjk)", "Backprop"],
        ["Weight Update", "Δwij = η·δj·yi", "Backprop"],
        ["Sigmoid", "σ(x) = 1/(1+e^(−x)) | σ'=σ·(1−σ)", "Activation"],
        ["RBF Hidden", "φ(x) = exp(−||x−μ||²/(2σ²))", "RBFNN"],
        ["Fuzzy Core", "Core(A) = {x | μ_A(x) = 1}", "Fuzzy"],
        ["Fuzzy Height", "Height(A) = max{μ_A(x)}", "Fuzzy"],
        ["Fuzzy Union", "μ_(A∪B)(x) = max(μ_A(x), μ_B(x))", "Fuzzy"],
        ["Fuzzy Intersection", "μ_(A∩B)(x) = min(μ_A(x), μ_B(x))", "Fuzzy"],
        ["Fuzzy Complement", "μ_Ā(x) = 1 − μ_A(x)", "Fuzzy"],
        ["GA Roulette", "P(i) = f(i) / Σf(j)", "GA"],
        ["GA Crossover Rate", "Pc = 0.6−0.9 | Mutation Pm = 0.001−0.01", "GA"],
        ["RNN Hidden State", "h(t) = f(Wx·x(t) + Wh·h(t-1) + b)", "RNN"],
        ["FOPL Universal", "∀x[Human(x)→Mortal(x)] = All humans mortal", "FOPL"],
        ["Resolution Rule", "(A∨B)+(¬A∨C) → (B∨C)", "Resolution"],
        ["Empty Clause □", "Derived empty clause = contradiction = goal proved", "Resolution"],
    ], [5*cm, 6.5*cm, W-2.8*cm-11.5*cm], C['navy'],
    [C['acc'],C['gl'],C['ol'],C['pl'],C['yl'],C['rl'],C['tl'],C['bl'],
     C['acc'],C['gl'],C['ol'],C['pl'],C['yl'],C['rl'],C['tl'],C['bl'],
     C['acc'],C['gl'],C['ol'],C['pl'],C['yl'],C['rl'],C['tl'],C['bl'],
     C['acc'],C['gl'],C['ol'],C['pl'],C['yl'],C['rl'],C['tl'],C['bl'],
     C['acc'],C['gl'],C['ol']])
    story.append(rev)

    story.append(Spacer(1, 0.3*cm))
    story.append(ibox(
        "🎯 EXAM STRATEGY FOR 2025/2026:\n\n"
        "PART A (10×1.5M=15M — ALL COMPULSORY):\n"
        "• Write 2-3 precise sentences. Start with definition, add formula/key fact, give example.\n"
        "• Never skip — even 50% answer gets partial marks.\n\n"
        "PART B (6 questions, answer ANY 4 — 60M total):\n"
        "Based on pattern analysis, SAFEST 4 choices:\n"
        "Q2: ANN/RNN/Backprop (appears EVERY year)\n"
        "Q3: Fuzzy Logic + GA (appears EVERY year)\n"
        "Q4/5: A*/AO*/Resolution/Expert System (appears EVERY year)\n"
        "Q6/7: Uncertainty (Bayesian/DS) + KR/Blackboard (appears EVERY year)\n\n"
        "AVOID if weak: IDDFS 15-mark question (needs precise complexity analysis)\n\n"
        "TIME MANAGEMENT: Part A=25min | Each Part B=30min | Review=5min | Total=180min",
        C['gl'], C['teal']))

    return story


def main():
    out = "IS_PYQ_2023_2024_2025_Complete.pdf"
    doc = SimpleDocTemplate(out, pagesize=A4,
                            rightMargin=1.3*cm, leftMargin=1.3*cm,
                            topMargin=1.3*cm, bottomMargin=1.3*cm,
                            title="IS PYQ 2023-2024-2025 Complete Answers")

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(HexColor('#9e9e9e'))
        canvas.drawString(1.3*cm, 0.6*cm, "IS PCC-CS-601 | 2023-2024-2025 PYQ Answers | YMCA University")
        canvas.drawRightString(W - 1.3*cm, 0.6*cm, f"Page {doc.page}")
        canvas.restoreState()

    doc.build(build(), onFirstPage=footer, onLaterPages=footer)
    print(f"Done: {out}")


if __name__ == "__main__":
    main()