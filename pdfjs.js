const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, HeadingLevel, BorderStyle, WidthType, ShadingType,
  LevelFormat, PageBreak, UnderlineType
} = require('docx');
const fs = require('fs');

// ─── Helpers ────────────────────────────────────────────────────────────────

const border = { style: BorderStyle.SINGLE, size: 1, color: "888888" };
const borders = { top: border, bottom: border, left: border, right: border };
const noBorder = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [new TextRun({ text, bold: true, size: 32, color: "1F3864", font: "Arial" })],
    spacing: { before: 360, after: 180 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "1F3864", space: 1 } }
  });
}

function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    children: [new TextRun({ text, bold: true, size: 26, color: "2E75B6", font: "Arial" })],
    spacing: { before: 280, after: 120 }
  });
}

function h3(text) {
  return new Paragraph({
    children: [new TextRun({ text, bold: true, size: 24, color: "C55A11", font: "Arial", underline: { type: UnderlineType.SINGLE } })],
    spacing: { before: 200, after: 80 }
  });
}

function topicBox(text) {
  return new Paragraph({
    children: [new TextRun({ text: "📚 Topics/Subtopics: " + text, italics: true, size: 20, color: "1F497D", font: "Arial" })],
    spacing: { before: 60, after: 100 },
    shading: { fill: "DCE6F1", type: ShadingType.CLEAR },
    indent: { left: 200 }
  });
}

function marksBox(text) {
  return new Paragraph({
    children: [new TextRun({ text, bold: true, size: 22, color: "FFFFFF", font: "Arial" })],
    spacing: { before: 80, after: 80 },
    shading: { fill: "2E75B6", type: ShadingType.CLEAR },
    indent: { left: 0 }
  });
}

function body(text) {
  return new Paragraph({
    children: [new TextRun({ text, size: 22, font: "Arial" })],
    spacing: { before: 60, after: 60 },
    alignment: AlignmentType.JUSTIFIED
  });
}

function bold_body(label, rest) {
  return new Paragraph({
    children: [
      new TextRun({ text: label, bold: true, size: 22, font: "Arial" }),
      new TextRun({ text: rest, size: 22, font: "Arial" })
    ],
    spacing: { before: 60, after: 60 },
    alignment: AlignmentType.JUSTIFIED
  });
}

function bullet(text, numbering_ref = "bullets") {
  return new Paragraph({
    numbering: { reference: numbering_ref, level: 0 },
    children: [new TextRun({ text, size: 22, font: "Arial" })],
    spacing: { before: 40, after: 40 }
  });
}

function formula(text) {
  return new Paragraph({
    children: [new TextRun({ text, bold: true, size: 22, font: "Courier New", color: "7030A0" })],
    spacing: { before: 80, after: 80 },
    alignment: AlignmentType.CENTER,
    shading: { fill: "F2EBF9", type: ShadingType.CLEAR }
  });
}

function spacer() {
  return new Paragraph({ children: [new TextRun("")], spacing: { before: 40, after: 40 } });
}

function pageBreak() {
  return new Paragraph({ children: [new PageBreak()] });
}

function simpleTable(headers, rows) {
  const colCount = headers.length;
  const totalWidth = 9000;
  const colW = Math.floor(totalWidth / colCount);
  const colWidths = Array(colCount).fill(colW);

  const headerRow = new TableRow({
    tableHeader: true,
    children: headers.map(h => new TableCell({
      borders,
      width: { size: colW, type: WidthType.DXA },
      shading: { fill: "1F3864", type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 120, right: 120 },
      children: [new Paragraph({ children: [new TextRun({ text: h, bold: true, size: 20, color: "FFFFFF", font: "Arial" })], alignment: AlignmentType.CENTER })]
    }))
  });

  const dataRows = rows.map((row, ri) => new TableRow({
    children: row.map(cell => new TableCell({
      borders,
      width: { size: colW, type: WidthType.DXA },
      shading: { fill: ri % 2 === 0 ? "DCE6F1" : "FFFFFF", type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 120, right: 120 },
      children: [new Paragraph({ children: [new TextRun({ text: cell, size: 20, font: "Arial" })], alignment: AlignmentType.JUSTIFIED })]
    }))
  }));

  return new Table({ width: { size: totalWidth, type: WidthType.DXA }, columnWidths: colWidths, rows: [headerRow, ...dataRows] });
}

// ─── Content ─────────────────────────────────────────────────────────────────

const children = [];

// TITLE PAGE
children.push(
  new Paragraph({
    children: [new TextRun({ text: "DATA MINING (PEC-CS-D601)", bold: true, size: 44, color: "1F3864", font: "Arial" })],
    alignment: AlignmentType.CENTER,
    spacing: { before: 400, after: 200 }
  }),
  new Paragraph({
    children: [new TextRun({ text: "B.Tech VI Semester — Complete PYQ Solutions", bold: true, size: 28, color: "2E75B6", font: "Arial" })],
    alignment: AlignmentType.CENTER,
    spacing: { before: 0, after: 200 }
  }),
  new Paragraph({
    children: [new TextRun({ text: "May 2024 & May 2025 | Detailed Answers with Topic Explanations", size: 22, italics: true, color: "666666", font: "Arial" })],
    alignment: AlignmentType.CENTER,
    spacing: { before: 0, after: 600 }
  }),
  pageBreak()
);

// ════════════════════════════════════════════════
//  MAY 2024 PAPER
// ════════════════════════════════════════════════
children.push(h1("MAY 2024 PAPER — Data Mining (PEC-CS-D601)"));
children.push(h1("PART A — Short Answer Questions (1.5 Marks Each)"));

// Q1a
children.push(h2("Q1(a): How can the confidence of an association rule X → Y be calculated?"));
children.push(marksBox("[1.5 Marks | ~100 words]"));
children.push(topicBox("Association Rule Mining → Confidence Measure → Apriori Algorithm | Subtopic: Support & Confidence metrics"));
children.push(body("Association rules are statements of the form X → Y, meaning if item-set X is bought, then item-set Y is also likely bought. The confidence of a rule X → Y measures how often items in Y appear in transactions that also contain X."));
children.push(formula("Confidence(X → Y) = Support(X ∪ Y) / Support(X)"));
children.push(body("= P(Y | X) = Number of transactions containing both X and Y / Number of transactions containing X"));
children.push(body("Example: If 4 out of 10 transactions contain {Bread, Butter} and 5 contain {Bread}, then Confidence(Bread → Butter) = 4/5 = 80%. A higher confidence means a stronger rule. Only rules exceeding the minimum confidence threshold are considered valid."));
children.push(spacer());

// Q1b
children.push(h2("Q1(b): Define classifier accuracy."));
children.push(marksBox("[1.5 Marks | ~100 words]"));
children.push(topicBox("Classification → Model Evaluation → Accuracy Metric | Subtopics: Confusion Matrix, Precision, Recall, F1-score"));
children.push(body("Classifier accuracy is a performance metric that measures the proportion of correctly classified instances out of the total instances in the test dataset. It is defined as:"));
children.push(formula("Accuracy = (TP + TN) / (TP + TN + FP + FN)"));
children.push(body("Where TP = True Positives, TN = True Negatives, FP = False Positives, FN = False Negatives. For example, if a classifier correctly identifies 90 out of 100 samples, its accuracy is 90%. However, accuracy alone can be misleading when classes are imbalanced; in such cases, precision, recall, and F1-score provide better evaluation. High classifier accuracy indicates a well-trained model with low generalization error."));
children.push(spacer());

// Q1c
children.push(h2("Q1(c): Explain any two methods for filling up the missing values during data preprocessing."));
children.push(marksBox("[1.5 Marks | ~100 words]"));
children.push(topicBox("Data Preprocessing → Missing Value Handling | Subtopics: Imputation techniques, Mean/Mode substitution, Regression imputation"));
children.push(body("1. Mean/Median/Mode Substitution: The missing value is replaced with the mean (for numerical), median (for skewed data), or mode (for categorical data) of the existing values in that attribute. Simple and widely used but may distort data distribution."));
children.push(body("2. Regression Imputation: A regression model is built using the non-missing attributes to predict the missing value. For example, if 'age' is missing, a model using salary, experience, and education predicts it. This is more accurate than mean substitution as it considers relationships between attributes but is computationally expensive."));
children.push(spacer());

// Q1d
children.push(h2("Q1(d): Differentiate between Classification and Clustering."));
children.push(marksBox("[1.5 Marks | ~100 words]"));
children.push(topicBox("Classification vs Clustering → Supervised vs Unsupervised Learning | Subtopics: Decision trees, K-means, Label usage"));
children.push(simpleTable(
  ["Basis", "Classification", "Clustering"],
  [
    ["Learning Type", "Supervised Learning", "Unsupervised Learning"],
    ["Labels", "Requires pre-labeled training data", "No pre-labeled data required"],
    ["Goal", "Predict class of new data", "Discover hidden natural groups"],
    ["Examples", "Decision Tree, SVM, Naïve Bayes", "K-Means, DBSCAN, Hierarchical"],
    ["Output", "Predefined classes/categories", "Groups (clusters) with no fixed labels"],
  ]
));
children.push(spacer());

// Q1e
children.push(h2("Q1(e): Explain the importance of Web Mining."));
children.push(marksBox("[1.5 Marks | ~100 words]"));
children.push(topicBox("Web Mining → Web Content Mining, Web Structure Mining, Web Usage Mining | Subtopics: Applications in E-commerce, Search engines, Personalization"));
children.push(body("Web Mining refers to the use of data mining techniques to automatically discover and extract useful information from the World Wide Web. Its importance includes:"));
children.push(bullet("Personalization: Recommends products/content based on user behavior (e.g., Amazon, Netflix)."));
children.push(bullet("Search Engine Optimization: Improves relevance ranking using link analysis (PageRank)."));
children.push(bullet("E-commerce Intelligence: Analyzes customer purchase patterns to improve business strategies."));
children.push(bullet("Fraud Detection: Detects fraudulent web transactions and spam pages."));
children.push(bullet("Trend Analysis: Identifies trending topics, public opinion from social media."));
children.push(body("Thus, web mining is crucial for business intelligence, cybersecurity, and knowledge discovery from internet data."));
children.push(spacer());

// Q1f
children.push(h2("Q1(f): Give the limitations of Hierarchical Clustering."));
children.push(marksBox("[1.5 Marks | ~100 words]"));
children.push(topicBox("Hierarchical Clustering → Agglomerative & Divisive Methods | Subtopics: Dendrogram, Linkage methods, Scalability issues"));
children.push(bullet("Computationally Expensive: Time complexity is O(n²) or O(n² log n), making it unsuitable for large datasets."));
children.push(bullet("No Backtracking: Once a merge/split is made, it cannot be undone—errors propagate through the hierarchy."));
children.push(bullet("Sensitive to Noise and Outliers: Outliers can significantly affect the cluster structure."));
children.push(bullet("Difficulty in Determining Cut Point: Deciding at which level to cut the dendrogram is subjective."));
children.push(bullet("Not Suitable for Large Data: Memory requirements grow quadratically with the size of the dataset."));
children.push(bullet("Linkage Method Sensitivity: Results vary significantly with single, complete, or average linkage."));
children.push(spacer());

// Q1g
children.push(h2("Q1(g): Define the term Outlier."));
children.push(marksBox("[1.5 Marks | ~100 words]"));
children.push(topicBox("Outlier Detection → Statistical outliers, Distance-based outliers | Subtopics: Box plots, Z-score, IQR method, DBSCAN for outlier detection"));
children.push(body("An Outlier (also called anomaly or noise) is a data point that deviates significantly from the majority of the data in a dataset. It lies far from the general distribution and does not conform to the expected pattern or behavior."));
children.push(formula("Outlier: A data point x such that |x - μ| > k·σ   (Z-score method, k usually = 3)"));
children.push(body("Types of Outliers: (1) Global Outliers – deviate from the entire dataset. (2) Contextual Outliers – abnormal in a specific context. (3) Collective Outliers – a group of data points that are anomalous together. Examples include: a temperature of 70°C in weather data, or a transaction of ₹10,00,000 in a set of small daily transactions. Outliers are important in fraud detection, network intrusion, and medical diagnosis."));
children.push(spacer());

// Q1h
children.push(h2("Q1(h): What is the basic idea behind Histogram method of sampling?"));
children.push(marksBox("[1.5 Marks | ~100 words]"));
children.push(topicBox("Data Sampling → Histogram-based Sampling | Subtopics: Data summarization, Bucket-based approximation, Frequency estimation"));
children.push(body("The Histogram Method of Sampling is a data summarization technique used to approximate the distribution of data values without storing all individual records. The basic idea is to:"));
children.push(bullet("Divide the data attribute's range into equal-width or equal-frequency buckets (bins)."));
children.push(bullet("Store the count (frequency) or aggregate statistics of values falling within each bucket."));
children.push(bullet("Use these aggregated buckets to estimate query answers or reconstruct the approximate distribution."));
children.push(body("For example, if age values range from 0–100, they can be divided into 10 buckets of width 10 each. This reduces storage while preserving approximate statistical information. Histograms are widely used in database query optimization and OLAP systems."));
children.push(spacer());

// Q1i
children.push(h2("Q1(i): Name any three properties of data streams."));
children.push(marksBox("[1.5 Marks | ~100 words]"));
children.push(topicBox("Data Streams → Stream Mining | Subtopics: Online processing, Concept drift, Sliding window models"));
children.push(body("Data Streams are continuous, rapidly arriving sequences of data that cannot be stored entirely in memory. Key properties include:"));
children.push(bullet("Continuous and Unbounded: Data arrives continuously and potentially infinitely—there is no defined end to the stream."));
children.push(bullet("High Speed & Real-Time: Data arrives at a very high rate, requiring real-time or near-real-time processing. Traditional batch processing is insufficient."));
children.push(bullet("Concept Drift: The underlying statistical properties of the data stream may change over time (e.g., user behavior shifts), making models trained on old data obsolete."));
children.push(body("Other properties include: non-revisitable (data cannot be stored/re-read), high volume, and order-sensitive nature."));
children.push(spacer());

// Q1j
children.push(h2("Q1(j): Generate the Clustering Feature for point (3,5)."));
children.push(marksBox("[1.5 Marks | ~100 words]"));
children.push(topicBox("BIRCH Clustering → Clustering Feature (CF) | Subtopics: CF Triple (N, LS, SS), CF Tree construction"));
children.push(body("A Clustering Feature (CF) in the BIRCH algorithm is a compact summary of a cluster, represented as a triple:"));
children.push(formula("CF = (N, LS, SS)"));
children.push(body("Where: N = number of data points, LS = Linear Sum of data points (vector), SS = Sum of Squares of data points (scalar)."));
children.push(body("For a single point (3, 5):"));
children.push(bullet("N = 1  (only one data point)"));
children.push(bullet("LS = (3, 5)  (sum of coordinates)"));
children.push(bullet("SS = 3² + 5² = 9 + 25 = 34  (sum of squares)"));
children.push(body("Therefore, CF for point (3, 5) = (1, (3, 5), 34). The CF triple allows efficient merging of sub-clusters and computation of cluster statistics like centroid, radius, and diameter."));
children.push(spacer());

// ─── PART B ───
children.push(pageBreak());
children.push(h1("PART B — Detailed Answer Questions"));

// ─── Q2(a) FP Tree ───
children.push(h2("Q2(a): Create FP Tree and find Conditional Pattern Base for the given transaction dataset. [10 Marks]"));
children.push(topicBox("Frequent Pattern Mining → FP-Growth Algorithm | Subtopics: FP-Tree construction, Conditional Pattern Base, Conditional FP-Tree, Frequent itemsets without candidate generation"));

children.push(h3("Transaction Dataset"));
children.push(simpleTable(
  ["T_Id", "Items"],
  [
    ["T1", "{E, K, M, N, O, Y}"],
    ["T2", "{D, E, K, N, O, Y}"],
    ["T3", "{A, E, K, M}"],
    ["T4", "{C, K, M, U, Y}"],
    ["T5", "{C, E, I, K, O}"],
  ]
));
children.push(spacer());

children.push(h3("Step 1: Count Item Frequencies (min_sup = 2 assumed)"));
children.push(simpleTable(
  ["Item", "Frequency", "Include? (freq ≥ 2)"],
  [
    ["K", "5", "Yes"],
    ["E", "4", "Yes"],
    ["M", "3", "Yes"],
    ["Y", "3", "Yes"],
    ["O", "3", "Yes"],
    ["N", "2", "Yes"],
    ["C", "2", "Yes"],
    ["D", "1", "No (excluded)"],
    ["A", "1", "No (excluded)"],
    ["U", "1", "No (excluded)"],
    ["I", "1", "No (excluded)"],
  ]
));
children.push(spacer());

children.push(h3("Step 2: Reorder Items in Each Transaction by Decreasing Frequency"));
children.push(body("Frequency order (descending): K(5) > E(4) > M(3) > Y(3) > O(3) > N(2) > C(2)"));
children.push(simpleTable(
  ["T_Id", "Original Items", "Ordered Frequent Items"],
  [
    ["T1", "{E,K,M,N,O,Y}", "K, E, M, Y, O, N"],
    ["T2", "{D,E,K,N,O,Y}", "K, E, Y, O, N"],
    ["T3", "{A,E,K,M}", "K, E, M"],
    ["T4", "{C,K,M,U,Y}", "K, M, Y, C"],
    ["T5", "{C,E,I,K,O}", "K, E, O, C"],
  ]
));
children.push(spacer());

children.push(h3("Step 3: FP-Tree Construction"));
children.push(body("Starting with root node {}, insert each transaction:"));
children.push(bullet("Insert T1: root → K(1) → E(1) → M(1) → Y(1) → O(1) → N(1)"));
children.push(bullet("Insert T2: root → K(2) → E(2) → Y(1) → O(1) → N(1) [K,E shared; new branch at Y]"));
children.push(bullet("Insert T3: root → K(3) → E(3) → M(1 + existing M) = root→K(3)→E(3)→M(2)..."));
children.push(bullet("Insert T4: root → K(4) → M(1 new branch since E not in T4) → Y → C"));
children.push(bullet("Insert T5: root → K(5) → E(4) → O → C [new branch at O from E]"));

children.push(body("FP-Tree Structure (textual representation):"));
children.push(formula("root"));
children.push(formula("  └─ K:5"));
children.push(formula("       ├─ E:4"));
children.push(formula("       │    ├─ M:2 → Y:1 → O:1 → N:1"));
children.push(formula("       │    ├─ Y:1 → O:1 → N:1"));
children.push(formula("       │    └─ O:1 → C:1"));
children.push(formula("       └─ M:1 → Y:1 → C:1"));
children.push(spacer());

children.push(h3("Step 4: Conditional Pattern Base and Conditional FP-Trees"));
children.push(simpleTable(
  ["Item", "Conditional Pattern Base (CPB)", "Conditional FP-Tree", "Frequent Patterns Generated"],
  [
    ["N", "{K,E,M,Y,O:1}, {K,E,Y,O:1}", "K:2, E:2, Y:2, O:2", "KN, EN, YN, ON, KEN, KYN, KON, KEYN, KEYON, ..."],
    ["O", "{K,E,M,Y:1}, {K,E,Y:1}, {K,E:1}", "K:3, E:3, Y:2", "KO, EO, KO, YO, KEO, KYO, EYO, KEYO"],
    ["Y", "{K,E,M:1}, {K,E:1}, {K,M:1}", "K:3, E:2, M:2", "KY, EY, MY, KEY, KMY, EMY"],
    ["M", "{K,E:2}, {K:1}", "K:3, E:2", "KM, EM, KEM"],
    ["C", "{K,E,O:1}, {K,M,Y:1}", "K:2", "KC"],
    ["E", "{K:4}", "K:4", "KE"],
  ]
));
children.push(spacer());

children.push(h3("Step 5: All Frequent Itemsets (with support ≥ 2)"));
children.push(body("Single items: K(5), E(4), M(3), Y(3), O(3), N(2), C(2)"));
children.push(body("From E's CPB: {KE} = 4"));
children.push(body("From M's CPB: {KM} = 3, {EM} = 2, {KEM} = 2"));
children.push(body("From Y's CPB: {KY} = 3, {EY} = 2, {MY} = 2, {KEY} = 2, {KMY} = 2"));
children.push(body("From O's CPB: {KO} = 3, {EO} = 3, {KEO} = 3, {YO} = 2, {KYO} = 2, {EYO} = 2, {KEYO} = 2"));
children.push(body("From N's CPB: {KN} = 2, {EN} = 2, {YN} = 2, {ON} = 2, {KEN} = 2, {KYN} = 2, {KON} = 2, {EON} = 2, {YON} = 2"));
children.push(body("From C's CPB: {KC} = 2"));
children.push(spacer());

// ─── Q2(b) K-Means ───
children.push(h2("Q2(b): Write down the algorithm for K-means algorithm. [5 Marks]"));
children.push(topicBox("K-Means Clustering → Iterative Algorithm | Subtopics: Centroid computation, Distance metrics, Convergence criterion, Choosing K"));

children.push(h3("K-Means Algorithm"));
children.push(body("K-Means is an unsupervised clustering algorithm that partitions n data points into k clusters, where each point belongs to the cluster with the nearest centroid (mean). It minimizes within-cluster sum of squared distances (WCSS)."));
children.push(spacer());

children.push(h3("Algorithm (Step-by-Step)"));
children.push(bold_body("Input: ", "Dataset D with n points, number of clusters k, convergence criterion (e.g., no change in centroids)"));
children.push(bold_body("Output: ", "k clusters with their centroids"));
children.push(spacer());
children.push(bold_body("Step 1 — Initialize: ", "Randomly select k data points as initial cluster centroids μ₁, μ₂, ..., μk."));
children.push(bold_body("Step 2 — Assign: ", "For each data point xᵢ, compute its Euclidean distance to all k centroids and assign it to the cluster of the nearest centroid:"));
children.push(formula("Cluster(xᵢ) = argmin_j || xᵢ - μⱼ ||²     for j = 1 to k"));
children.push(bold_body("Step 3 — Update Centroids: ", "Recalculate the centroid of each cluster as the mean of all points assigned to it:"));
children.push(formula("μⱼ = (1/|Cⱼ|) × Σ xᵢ     for all xᵢ ∈ Cⱼ"));
children.push(bold_body("Step 4 — Check Convergence: ", "If the centroids do not change (or change is below a threshold), stop. Otherwise, go to Step 2."));
children.push(bold_body("Step 5 — Output: ", "Return the k cluster assignments and their final centroids."));
children.push(spacer());

children.push(h3("Pseudocode"));
children.push(formula("K-Means(D, k):"));
children.push(formula("  μ = randomly select k points from D"));
children.push(formula("  REPEAT"));
children.push(formula("    FOR each point x in D:"));
children.push(formula("      Assign x to cluster j* = argmin ||x - μⱼ||²"));
children.push(formula("    FOR each cluster j = 1 to k:"));
children.push(formula("      μⱼ = mean of all points assigned to cluster j"));
children.push(formula("  UNTIL centroids do not change"));
children.push(formula("  RETURN clusters C₁, C₂, ..., Cₖ"));
children.push(spacer());

children.push(h3("Key Properties"));
children.push(simpleTable(
  ["Property", "Detail"],
  [
    ["Time Complexity", "O(n·k·t·d) where t=iterations, d=dimensions"],
    ["Distance Metric", "Usually Euclidean Distance"],
    ["Convergence", "Guaranteed to converge but may reach local minimum"],
    ["Sensitivity", "Sensitive to initial centroid selection and outliers"],
    ["Selection of k", "Use Elbow Method or Silhouette Score"],
  ]
));
children.push(spacer());

children.push(h3("Advantages"));
children.push(bullet("Simple and easy to implement"));
children.push(bullet("Efficient for large datasets (linear time per iteration)"));
children.push(bullet("Works well when clusters are spherical and equal-sized"));
children.push(h3("Disadvantages"));
children.push(bullet("Must specify k in advance"));
children.push(bullet("Sensitive to outliers and initial centroid choice"));
children.push(bullet("Cannot handle non-convex or irregular shaped clusters"));
children.push(bullet("May converge to a local optimum"));
children.push(spacer());

// ─── Q3(a) Time Series ───
children.push(pageBreak());
children.push(h2("Q3(a): What is time series analysis? Explain four major components of Time Series Data. [5 Marks]"));
children.push(topicBox("Time Series Analysis → Temporal Data Mining | Subtopics: Trend, Seasonality, Cyclicity, Irregularity/Noise, Forecasting methods"));

children.push(h3("What is Time Series Analysis?"));
children.push(body("Time Series Analysis is a statistical and data mining technique used to analyze a sequence of data points collected or recorded at successive points in time, typically at uniform intervals. The goal is to identify patterns, trends, and relationships within the data to understand the past behavior and predict future values."));
children.push(body("Examples include: stock market prices, weather temperature recordings, annual sales figures, EEG signals, and sensor data from IoT devices."));
children.push(body("Applications: Stock forecasting, demand forecasting, anomaly detection in networks, weather prediction, and economic planning."));
children.push(spacer());

children.push(h3("Four Major Components of Time Series Data"));
children.push(spacer());
children.push(bold_body("1. Trend (T): ", "The long-term general movement or direction in the data over an extended period. A trend can be upward (e.g., increasing population), downward (e.g., declining landline users), or horizontal (stationary). It reflects the overall tendency of the series ignoring short-term fluctuations. Trend is identified using moving averages or regression analysis."));
children.push(formula("Example: Annual GDP growth showing an overall upward trend from 2000 to 2023."));
children.push(spacer());
children.push(bold_body("2. Seasonality (S): ", "Regular, periodic fluctuations in data that repeat over a fixed time period (daily, monthly, quarterly, or yearly). Seasonality occurs due to seasonal factors like weather, holidays, or festivals. Unlike trend, seasonality is predictable and repeats at known intervals."));
children.push(formula("Example: Retail sales spike every December due to Christmas shopping."));
children.push(formula("Example: Ice cream sales increase every summer and decrease in winter."));
children.push(spacer());
children.push(bold_body("3. Cyclical Component (C): ", "Wave-like fluctuations in the data that occur over longer, irregular time periods (typically more than one year). Unlike seasonality, cycles are not of fixed length and are caused by business cycles, economic expansions/recessions, or political changes. Cycles are harder to predict because their duration and amplitude vary."));
children.push(formula("Example: Economic boom and recession cycles over 5–10 year periods."));
children.push(spacer());
children.push(bold_body("4. Irregular/Random Component (I): ", "Also called 'noise' or 'residual', this represents unpredictable, random variations in the data that cannot be explained by trend, seasonality, or cyclicity. These occur due to sudden events such as natural disasters, strikes, pandemics, or random shocks."));
children.push(formula("Example: A sudden drop in airline traffic due to COVID-19 pandemic."));
children.push(spacer());
children.push(h3("Decomposition Model"));
children.push(formula("Additive Model:    Y = T + S + C + I"));
children.push(formula("Multiplicative Model: Y = T × S × C × I"));
children.push(body("The Additive model is used when seasonal variations are constant, while the Multiplicative model is used when they grow proportionally with the trend."));
children.push(spacer());

// ─── Q3(b) SVM ───
children.push(h2("Q3(b): Find the best fit line/hyperplane to classify given positive and negative points. [10 Marks]"));
children.push(topicBox("Support Vector Machine (SVM) → Maximal Margin Hyperplane | Subtopics: Support Vectors, Margin calculation, Hyperplane equation w·x + b = 0, Hard margin SVM"));

children.push(h3("Given Data"));
children.push(bold_body("Positive Labelled (+1): ", "{(4,0), (5,1), (5,-1), (6,0)}"));
children.push(bold_body("Negative Labelled (-1): ", "{(1,1), (1,-1), (2,1), (2,-1)}"));
children.push(spacer());

children.push(h3("Step 1: Understanding SVM"));
children.push(body("SVM finds a hyperplane w·x + b = 0 that maximally separates the two classes. The margin is the distance between the two parallel planes: w·x + b = +1 and w·x + b = -1. We want to maximize the margin = 2/||w||."));
children.push(spacer());

children.push(h3("Step 2: Identify Support Vectors"));
children.push(body("Looking at the data, the boundary lies roughly at x₁ = 3.5 (midpoint between x₁ = 2 and x₁ = 4 in the first dimension)."));
children.push(body("Positive support vectors (closest to boundary): (4,0), (5,1), (5,-1)"));
children.push(body("Negative support vectors (closest to boundary): (2,1), (2,-1), (1,1)"));
children.push(spacer());

children.push(h3("Step 3: Find the Decision Boundary"));
children.push(body("Since the data is linearly separable along the x₁ axis, we can determine the hyperplane based on x₁ only:"));
children.push(body("The positive class has minimum x₁ = 4, negative class has maximum x₁ = 2."));
children.push(body("The optimal decision boundary is:"));
children.push(formula("x₁ = 3   →   x₁ - 3 = 0"));
children.push(body("This means the weight vector w = (1, 0) and bias b = -3."));
children.push(formula("Decision Boundary: w·x + b = 0  →  1·x₁ + 0·x₂ - 3 = 0  →  x₁ = 3"));
children.push(spacer());

children.push(h3("Step 4: Verify Margin"));
children.push(body("Positive margin plane: w·x + b = +1  →  x₁ - 3 = 1  →  x₁ = 4 ✓ (positive support vectors at x₁ = 4)"));
children.push(body("Negative margin plane: w·x + b = -1  →  x₁ - 3 = -1  →  x₁ = 2 ✓ (negative support vectors at x₁ = 2)"));
children.push(formula("Margin = 2 / ||w|| = 2 / ||(1,0)|| = 2 / 1 = 2"));
children.push(spacer());

children.push(h3("Step 5: Verify Classification"));
children.push(simpleTable(
  ["Point", "Class", "x₁ - 3", "Sign", "Correct?"],
  [
    ["(4,0)", "+1", "4-3 = +1", "+", "✓"],
    ["(5,1)", "+1", "5-3 = +2", "+", "✓"],
    ["(5,-1)", "+1", "5-3 = +2", "+", "✓"],
    ["(6,0)", "+1", "6-3 = +3", "+", "✓"],
    ["(1,1)", "-1", "1-3 = -2", "-", "✓"],
    ["(1,-1)", "-1", "1-3 = -2", "-", "✓"],
    ["(2,1)", "-1", "2-3 = -1", "-", "✓"],
    ["(2,-1)", "-1", "2-3 = -1", "-", "✓"],
  ]
));
children.push(spacer());

children.push(h3("Conclusion"));
children.push(body("The optimal separating hyperplane is: x₁ = 3, or equivalently:"));
children.push(formula("f(x) = x₁ - 3 = 0"));
children.push(body("Support Vectors: (4,0), (5,1), (5,-1) on the positive side and (2,1), (2,-1) on the negative side. The maximum margin is 2 units. Any new point with x₁ > 3 is classified as positive (+1) and with x₁ < 3 as negative (-1)."));
children.push(spacer());

// ─── Q4(a) Classification & Prediction Evaluation ───
children.push(pageBreak());
children.push(h2("Q4(a): What are the parameters on the basis of which Classification and Prediction methods can be evaluated? [5 Marks]"));
children.push(topicBox("Model Evaluation → Classification Metrics | Subtopics: Accuracy, Precision, Recall, F1-Score, ROC Curve, Confusion Matrix, Cross-validation, MSE for regression"));

children.push(h3("Evaluation Parameters for Classification"));
children.push(spacer());
children.push(bold_body("1. Accuracy: ", "The ratio of correctly predicted instances to the total instances. It is the most basic metric."));
children.push(formula("Accuracy = (TP + TN) / (TP + TN + FP + FN)"));
children.push(body("Limitation: Can be misleading for imbalanced datasets."));
children.push(spacer());
children.push(bold_body("2. Precision (Positive Predictive Value): ", "The proportion of positive predictions that are actually correct. Measures how 'precise' the classifier is."));
children.push(formula("Precision = TP / (TP + FP)"));
children.push(body("High precision: few false positives. Important in spam detection, medical diagnosis."));
children.push(spacer());
children.push(bold_body("3. Recall (Sensitivity / True Positive Rate): ", "The proportion of actual positives that are correctly identified."));
children.push(formula("Recall = TP / (TP + FN)"));
children.push(body("High recall: few false negatives. Critical in disease detection, fraud detection."));
children.push(spacer());
children.push(bold_body("4. F1-Score: ", "The harmonic mean of precision and recall. Best metric when there is class imbalance."));
children.push(formula("F1-Score = 2 × (Precision × Recall) / (Precision + Recall)"));
children.push(spacer());
children.push(bold_body("5. Confusion Matrix: ", "A table showing TP, TN, FP, FN for each class. It gives a complete picture of classifier performance."));
children.push(spacer());
children.push(bold_body("6. ROC Curve & AUC: ", "Receiver Operating Characteristic curve plots TPR vs FPR. Area Under Curve (AUC) = 1 is perfect; AUC = 0.5 is random. Used for binary classifiers."));
children.push(spacer());
children.push(bold_body("7. Cross-Validation: ", "Technique (e.g., k-fold) to estimate generalization error by training and testing on different data subsets. Reduces overfitting bias."));
children.push(spacer());

children.push(h3("Evaluation Parameters for Prediction (Regression)"));
children.push(simpleTable(
  ["Metric", "Formula", "Description"],
  [
    ["Mean Squared Error (MSE)", "MSE = (1/n) Σ(yᵢ - ŷᵢ)²", "Penalizes large errors more"],
    ["Root MSE (RMSE)", "RMSE = √MSE", "In same units as output"],
    ["Mean Absolute Error (MAE)", "MAE = (1/n) Σ|yᵢ - ŷᵢ|", "Robust to outliers"],
    ["R² Score", "1 - SS_res/SS_tot", "1 = perfect prediction, 0 = baseline"],
  ]
));
children.push(spacer());

children.push(h3("Other Parameters"));
children.push(bullet("Speed & Scalability: Time to train and test on large datasets."));
children.push(bullet("Interpretability: How easy is it to understand the model's decisions."));
children.push(bullet("Robustness: Performance under noisy or incomplete data."));
children.push(bullet("Overfitting/Underfitting: Training vs. test error comparison."));
children.push(spacer());

// ─── Q4(b) Decision Tree ───
children.push(h2("Q4(b): Explain Decision Tree induction algorithm for classification. Discuss the usage of information gain. [10 Marks]"));
children.push(topicBox("Decision Tree → ID3 / C4.5 Algorithm | Subtopics: Entropy, Information Gain, Attribute selection, Tree pruning, Overfitting, Gini Index"));

children.push(h3("What is a Decision Tree?"));
children.push(body("A Decision Tree is a flowchart-like tree structure used for classification and regression. It works by recursively splitting the dataset into subsets based on the most informative attribute (feature), ultimately creating a tree where:"));
children.push(bullet("Internal nodes represent tests on attributes/features"));
children.push(bullet("Branches represent outcomes of tests"));
children.push(bullet("Leaf nodes represent class labels (decisions)"));
children.push(spacer());

children.push(h3("Decision Tree Induction Algorithm (ID3)"));
children.push(bold_body("Input: ", "Training dataset D with attributes A₁, A₂, ..., Aₘ and class labels, minimum support threshold."));
children.push(bold_body("Output: ", "A decision tree T."));
children.push(spacer());
children.push(formula("ID3(D, Attributes):"));
children.push(formula("  IF all examples in D belong to the same class C:"));
children.push(formula("    Return leaf node labeled C"));
children.push(formula("  IF Attributes is empty:"));
children.push(formula("    Return leaf node labeled with majority class in D"));
children.push(formula("  A* = attribute with highest Information Gain in Attributes"));
children.push(formula("  Create internal node N labeled A*"));
children.push(formula("  FOR each value v of A*:"));
children.push(formula("    Dv = subset of D where A* = v"));
children.push(formula("    IF Dv is empty: add leaf with majority class"));
children.push(formula("    ELSE: add subtree ID3(Dv, Attributes - {A*})"));
children.push(formula("  Return tree rooted at N"));
children.push(spacer());

children.push(h3("Information Gain — The Core Measure"));
children.push(body("Information Gain measures the reduction in entropy (uncertainty) achieved by splitting the dataset on a particular attribute. ID3 always selects the attribute with the highest information gain."));
children.push(spacer());

children.push(bold_body("Step 1 — Entropy of Dataset D: ", "Measures the impurity/randomness of a dataset."));
children.push(formula("Entropy(D) = -Σ pᵢ × log₂(pᵢ)   for i = 1 to c classes"));
children.push(body("Where pᵢ is the proportion of class i in D. Entropy = 0 means pure (all same class); Entropy = 1 means maximum impurity (equal split)."));
children.push(spacer());

children.push(bold_body("Step 2 — Information Gain for Attribute A: "));
children.push(formula("IG(D, A) = Entropy(D) - Σ (|Dᵥ|/|D|) × Entropy(Dᵥ)"));
children.push(body("Where Dᵥ is the subset of D where attribute A = value v. The attribute with maximum IG is chosen for splitting."));
children.push(spacer());

children.push(h3("Worked Example: Play Tennis Dataset (Simplified)"));
children.push(body("Suppose we have 14 instances: 9 play (Yes) and 5 don't play (No)."));
children.push(formula("Entropy(D) = -(9/14)log₂(9/14) - (5/14)log₂(5/14)"));
children.push(formula("           = -(0.643 × (-0.637)) - (0.357 × (-1.485))"));
children.push(formula("           = 0.410 + 0.530 = 0.940 bits"));
children.push(spacer());
children.push(body("For attribute 'Outlook' with values {Sunny, Overcast, Rain}:"));
children.push(bullet("Sunny: 5 instances (2 Yes, 3 No) → Entropy = 0.971"));
children.push(bullet("Overcast: 4 instances (4 Yes, 0 No) → Entropy = 0.0 (pure)"));
children.push(bullet("Rain: 5 instances (3 Yes, 2 No) → Entropy = 0.971"));
children.push(formula("IG(Outlook) = 0.940 - [(5/14)×0.971 + (4/14)×0.0 + (5/14)×0.971]"));
children.push(formula("            = 0.940 - [0.347 + 0 + 0.347] = 0.940 - 0.694 = 0.246 bits"));
children.push(spacer());

children.push(h3("Advantages of Decision Trees"));
children.push(bullet("Easy to understand and interpret — produces human-readable rules"));
children.push(bullet("Works for both categorical and numerical data"));
children.push(bullet("No feature scaling required"));
children.push(bullet("Handles missing values effectively"));
children.push(bullet("Can capture non-linear relationships"));
children.push(spacer());

children.push(h3("Limitations and Solutions"));
children.push(simpleTable(
  ["Limitation", "Solution"],
  [
    ["Overfitting on noisy data", "Pruning (Pre-pruning, Post-pruning)"],
    ["Bias towards attributes with many values", "Use Gain Ratio (C4.5) or Gini Index (CART)"],
    ["Instability (small data changes = new tree)", "Use Random Forests (ensemble method)"],
    ["Cannot handle XOR relationships well", "Use kernel methods or deeper trees"],
  ]
));
children.push(spacer());

children.push(h3("Information Gain vs Other Splitting Criteria"));
children.push(simpleTable(
  ["Criterion", "Formula", "Used In", "Limitation"],
  [
    ["Information Gain", "IG = Entropy(D) - Σ weighted Entropy(Dᵥ)", "ID3", "Biased to many-valued attributes"],
    ["Gain Ratio", "GR = IG / SplitInfo(A)", "C4.5", "May prefer unbalanced splits"],
    ["Gini Index", "Gini = 1 - Σ pᵢ²", "CART", "Biased to equal-sized partitions"],
  ]
));
children.push(spacer());

// ─── Q5(a) Euclidean vs Manhattan ───
children.push(pageBreak());
children.push(h2("Q5(a): Explain the difference between Euclidian and Manhattan Distance. Generate the distance matrix for points [3, 5, 1, 10, 8] using Euclidian distance. [5 Marks]"));
children.push(topicBox("Distance Metrics in Data Mining | Subtopics: Euclidean Distance, Manhattan Distance, Minkowski Distance, Distance Matrix, Similarity measures"));

children.push(h3("Euclidean vs Manhattan Distance"));
children.push(simpleTable(
  ["Aspect", "Euclidean Distance", "Manhattan Distance"],
  [
    ["Definition", "Straight-line (as-the-crow-flies) distance", "Sum of absolute differences (city-block)"],
    ["Formula (2D)", "d = √[(x₂-x₁)² + (y₂-y₁)²]", "d = |x₂-x₁| + |y₂-y₁|"],
    ["Formula (nD)", "d = √[Σ(xᵢ-yᵢ)²]", "d = Σ|xᵢ-yᵢ|"],
    ["Geometry", "Diagonal movement allowed", "Only horizontal/vertical movement"],
    ["Sensitivity to Outliers", "High (squares the differences)", "Lower (uses absolute values)"],
    ["Use Case", "Continuous, low-dimensional data", "High-dimensional, sparse data, city navigation"],
    ["Minkowski p-value", "p = 2", "p = 1"],
  ]
));
children.push(spacer());

children.push(h3("Euclidean Distance Matrix for Points [3, 5, 1, 10, 8]"));
children.push(body("Given 1-D points: P₁ = 3, P₂ = 5, P₃ = 1, P₄ = 10, P₅ = 8"));
children.push(body("For 1-D points, Euclidean distance = |pᵢ - pⱼ| (absolute difference since squaring then square-rooting of one dimension)"));
children.push(spacer());
children.push(formula("d(Pᵢ, Pⱼ) = √(Pᵢ - Pⱼ)² = |Pᵢ - Pⱼ|"));
children.push(spacer());
children.push(simpleTable(
  ["", "P₁(3)", "P₂(5)", "P₃(1)", "P₄(10)", "P₅(8)"],
  [
    ["P₁(3)", "0", "|3-5|=2", "|3-1|=2", "|3-10|=7", "|3-8|=5"],
    ["P₂(5)", "2", "0", "|5-1|=4", "|5-10|=5", "|5-8|=3"],
    ["P₃(1)", "2", "4", "0", "|1-10|=9", "|1-8|=7"],
    ["P₄(10)", "7", "5", "9", "0", "|10-8|=2"],
    ["P₅(8)", "5", "3", "7", "2", "0"],
  ]
));
children.push(spacer());
children.push(body("The distance matrix is symmetric (d(i,j) = d(j,i)) and has zeros on the diagonal. Nearest pair: P₁ and P₂ (or P₄ and P₅) with distance = 2. Farthest pair: P₃(1) and P₄(10) with distance = 9."));
children.push(spacer());

// ─── Q5(b) OLAP vs OLTP and Web Mining vs Data Mining ───
children.push(h2("Q5(b): Differentiate between (i) OLAP vs OLTP (ii) Web Mining vs Data Mining [10 Marks]"));
children.push(topicBox("Data Warehousing → OLAP & OLTP | Web Mining vs Data Mining | Subtopics: Multidimensional analysis, Transaction processing, ETL, ROLAP, MOLAP, Web content/structure/usage mining"));

children.push(h3("(i) OLAP vs OLTP"));
children.push(simpleTable(
  ["Parameter", "OLAP (Online Analytical Processing)", "OLTP (Online Transaction Processing)"],
  [
    ["Purpose", "Data analysis and decision support", "Day-to-day transaction management"],
    ["Data Type", "Historical, aggregated, multidimensional", "Current, detailed, operational"],
    ["Database Size", "Terabytes to Petabytes", "Megabytes to Gigabytes"],
    ["Operations", "Complex queries, aggregations, drill-down, roll-up", "Insert, Update, Delete, simple reads"],
    ["Users", "Analysts, managers, executives", "Clerks, customers, tellers"],
    ["Schema", "Star/Snowflake/Galaxy schema (denormalized)", "Normalized (3NF) schema"],
    ["Query Complexity", "Complex, few queries at a time", "Simple, many queries per second"],
    ["Response Time", "Seconds to minutes", "Milliseconds"],
    ["Optimization", "Optimized for reading and aggregation", "Optimized for writing and fast lookups"],
    ["Examples", "Business reports, dashboards, SSAS", "Banking, e-commerce, ATM, ERP"],
    ["Backup", "Periodic (can afford downtime)", "Continuous, critical (no data loss)"],
  ]
));
children.push(spacer());

children.push(h3("(ii) Web Mining vs Data Mining"));
children.push(simpleTable(
  ["Parameter", "Web Mining", "Data Mining"],
  [
    ["Definition", "Mining knowledge from web data (pages, links, logs)", "Mining patterns from structured datasets"],
    ["Data Source", "Web pages, hyperlinks, server logs, social media", "Databases, data warehouses, spreadsheets"],
    ["Data Type", "Unstructured/semi-structured (HTML, XML, logs)", "Structured and semi-structured data"],
    ["Subtypes", "Web Content, Web Structure, Web Usage Mining", "Association, Classification, Clustering, Regression"],
    ["Tools", "Web crawlers, parsers, PageRank, NLP tools", "Weka, RapidMiner, Python (sklearn), R"],
    ["Goal", "Understand web user behavior and web content", "Discover hidden patterns and relationships in data"],
    ["Challenges", "Noise in web data, link spam, heterogeneity", "High dimensionality, missing data, scalability"],
    ["Examples", "Google PageRank, Amazon recommendations", "Customer churn prediction, fraud detection"],
  ]
));
children.push(body("Web Mining is a subfield of Data Mining — it applies data mining techniques specifically to web data. Data Mining is broader and encompasses any type of data, while Web Mining focuses exclusively on web-generated data."));
children.push(spacer());

// ─── Q6(a) GSP ───
children.push(pageBreak());
children.push(h2("Q6(a): Find all frequent sub-sequences using GSP approach (min_sup = 2). [15 Marks]"));
children.push(topicBox("Sequential Pattern Mining → GSP Algorithm | Subtopics: Sequences, Subsequences, Support counting, Level-wise approach, Candidate generation and pruning, AprioriAll"));

children.push(h3("Given Transaction Sequences"));
children.push(simpleTable(
  ["SNo", "SID", "Items_bought"],
  [
    ["01", "S1", "<a {a,b} {a,c} d {c,e,f}>"],
    ["02", "S2", "<{a,d} c {b,c,d} {a,b,e}>"],
    ["03", "S3", "<{e,f} {a,b} {d,e,f} c b>"],
    ["04", "S4", "<e g {a,d,f} c b>"],
  ]
));
children.push(body("min_sup = 2 (sequence is frequent if it appears in ≥ 2 sequences)"));
children.push(spacer());

children.push(h3("Step 1: Find Frequent 1-Sequences (Large 1-itemsets)"));
children.push(body("Count occurrence of each item across all sequences (an item counts once per sequence even if repeated):"));
children.push(simpleTable(
  ["Item", "Appears in Sequences", "Support Count", "Frequent?"],
  [
    ["a", "S1, S2, S3, S4", "4", "Yes"],
    ["b", "S1, S2, S3, S4", "4", "Yes"],
    ["c", "S1, S2, S3, S4", "4", "Yes"],
    ["d", "S1, S2, S3, S4", "4", "Yes"],
    ["e", "S1, S2, S3, S4", "4", "Yes"],
    ["f", "S1, S2, S3, S4", "4", "Yes"],
    ["g", "S4", "1", "No"],
  ]
));
children.push(body("Large 1-sequences (L₁): <a>, <b>, <c>, <d>, <e>, <f>  (all with support ≥ 2)"));
children.push(spacer());

children.push(h3("Step 2: Generate Candidate 2-Sequences (C₂)"));
children.push(body("Using apriori-based generation: combine pairs from L₁. For each pair of frequent 1-itemsets, generate 2-sequences. For items within same itemset: {a,b}, {a,c}, etc. For items across consecutive elements: <a b>, <a c>, etc."));
children.push(body("Check support for key 2-sequences:"));
children.push(simpleTable(
  ["2-Sequence", "Appears In", "Support"],
  [
    ["<a b>", "S1(a→{a,b}), S2({a,d}→{a,b,e}), S3({a,b}), S4({a,d,f}→b)", "4"],
    ["<a c>", "S1,S2,S3,S4", "4"],
    ["<a d>", "S1,S2,S3,S4", "4"],
    ["<a e>", "S1,S2,S3,S4", "4"],
    ["<a f>", "S1,S2,S3,S4", "3"],
    ["<b c>", "S1,S2,S3,S4", "4"],
    ["<b d>", "S1,S2,S3,S4", "3"],
    ["<b e>", "S1,S2,S3,S4", "3"],
    ["<b f>", "S1,S2,S3,S4", "3"],
    ["<c d>", "S1,S2,S3,S4", "3"],
    ["<c e>", "S1,S2,S3,S4", "3"],
    ["<c f>", "S1,S2,S3,S4", "3"],
    ["<d e>", "S1,S2,S3,S4", "4"],
    ["<d f>", "S1,S2,S3,S4", "4"],
    ["<e f>", "S1,S2,S3,S4", "4"],
    ["{a,b}", "S1({a,b}), S2({a,b,e}), S3({a,b})", "3"],
    ["{a,c}", "S1({a,c})", "1 - drop"],
    ["{a,d}", "S2({a,d}), S4({a,d,f})", "2"],
    ["{a,e}", "S2({a,b,e})", "1 - drop"],
    ["{b,c}", "S2({b,c,d})", "1 - drop"],
    ["{c,e}", "S1({c,e,f}), S3({d,e,f}→c)", "1 - check"],
    ["{d,f}", "S2({b,c,d})→no, S3({d,e,f}), S4({a,d,f})", "2"],
    ["{e,f}", "S1({c,e,f}), S3({e,f},{d,e,f})", "2"],
    ["{a,b,e}", "S2({a,b,e})", "1 - drop"],
    ["{a,d,f}", "S4({a,d,f})", "1 - drop"],
  ]
));
children.push(spacer());

children.push(h3("Large 2-Sequences (L₂) — All with support ≥ 2"));
children.push(body("From the above analysis, the frequent 2-sequences include (representative list):"));
children.push(bullet("<a b>: sup=4, <a c>: sup=4, <a d>: sup=4, <a e>: sup=4, <a f>: sup=3"));
children.push(bullet("<b c>: sup=4, <b d>: sup=3, <b e>: sup=3, <b f>: sup=3"));
children.push(bullet("<c d>: sup=3, <c e>: sup=3, <c f>: sup=3"));
children.push(bullet("<d e>: sup=4, <d f>: sup=4, <e f>: sup=4"));
children.push(bullet("{a,b}: sup=3, {a,d}: sup=2, {d,f}: sup=2, {e,f}: sup=2"));
children.push(spacer());

children.push(h3("Step 3: Generate Candidate 3-Sequences (C₃) and Find L₃"));
children.push(body("Join L₂ with itself: A 3-sequence is generated by joining two 2-sequences sharing a common prefix. Then prune any candidate whose 2-subsequence is not in L₂."));
children.push(body("Key frequent 3-sequences (support ≥ 2):"));
children.push(bullet("<a b c>: Appears in S1, S2, S3, S4 → sup=4"));
children.push(bullet("<a b d>: Appears in S1, S2, S3, S4 → sup=4"));
children.push(bullet("<a b e>: Appears in S1, S2, S3 → sup=3"));
children.push(bullet("<a c d>: Appears in S1, S2, S3, S4 → sup=4"));
children.push(bullet("<a d e>: Appears in S1, S2, S3, S4 → sup=3"));
children.push(bullet("<a d f>: Appears in S1, S3, S4 → sup=3"));
children.push(bullet("<b c d>: Appears in S1, S2, S3, S4 → sup=4"));
children.push(bullet("<c d e>: S1, S2, S3, S4 → sup=3"));
children.push(bullet("<d e f>: S1, S3 → sup=2"));
children.push(bullet("<a b c d>: Appears in multiple sequences → sup≥2"));
children.push(spacer());

children.push(h3("Step 4: Continue Until No More Candidates"));
children.push(body("The GSP algorithm continues generating longer candidate sequences by joining previous frequent sequences and pruning those that contain an infrequent subsequence (apriori property). The process terminates when no new frequent sequences can be found."));
children.push(spacer());

children.push(h3("GSP Algorithm Summary"));
children.push(simpleTable(
  ["Step", "Action"],
  [
    ["1", "Scan DB, find all frequent 1-sequences (L₁)"],
    ["2", "Generate candidate k-sequences (Cₖ) from L_{k-1}"],
    ["3", "Prune candidates whose (k-1)-subsequences are not frequent"],
    ["4", "Scan DB to count support for each candidate in Cₖ"],
    ["5", "Remove candidates with support < min_sup → get Lₖ"],
    ["6", "Repeat steps 2–5 with k=k+1 until Lₖ is empty"],
  ]
));
children.push(spacer());
children.push(body("Key Insight (Apriori Property for Sequences): If a sequence is infrequent, then all its super-sequences are also infrequent. This allows early pruning of candidate sequences and dramatically reduces computational overhead."));
children.push(spacer());

// ─────────────────────────────────────────────────
//  MAY 2025 PAPER
// ─────────────────────────────────────────────────
children.push(pageBreak());
children.push(h1("MAY 2025 PAPER — Data Mining (PEC-CS-D601)"));
children.push(h1("PART A — Short Answer Questions (1.5 Marks Each)"));

// 1a Data Warehousing features
children.push(h2("1(a): List some features of Data Warehousing which make it different from Information Processing. [1.5 Marks]"));
children.push(marksBox("[1.5 Marks | ~100 words]"));
children.push(topicBox("Data Warehousing → Features & Architecture | Subtopics: Subject-oriented, Integrated, Non-volatile, Time-variant, OLAP vs traditional DB"));
children.push(body("A Data Warehouse is a subject-oriented, integrated, time-variant, and non-volatile collection of data supporting management decision-making. Features distinguishing it from traditional Information Processing:"));
children.push(bullet("Subject-Oriented: Organized around major subjects (sales, customers) not day-to-day operations."));
children.push(bullet("Integrated: Consolidates data from multiple heterogeneous sources with consistent naming, encoding, and format."));
children.push(bullet("Time-Variant: Stores historical data (years/decades) vs. only current operational data."));
children.push(bullet("Non-Volatile: Data is loaded once and never deleted — used only for query/analysis, not frequent updates."));
children.push(bullet("Supports OLAP: Enables multidimensional analysis unlike row-based OLTP processing."));
children.push(spacer());

// 1b supervised vs unsupervised
children.push(h2("1(b): What is the difference between supervised and unsupervised learning in data mining? [1.5 Marks]"));
children.push(marksBox("[1.5 Marks | ~100 words]"));
children.push(topicBox("Machine Learning Paradigms | Subtopics: Labeled data, Training, Classification vs Clustering"));
children.push(simpleTable(
  ["Aspect", "Supervised Learning", "Unsupervised Learning"],
  [
    ["Labels", "Uses labeled training data", "No labels — discovers structure autonomously"],
    ["Goal", "Learn a mapping from input to known output", "Discover hidden patterns or groupings"],
    ["Examples", "Classification, Regression (SVM, DT, ANN)", "Clustering, Association (K-Means, Apriori)"],
    ["Evaluation", "Accuracy, Precision, Recall (easy to measure)", "Silhouette score, Dunn index (harder to evaluate)"],
  ]
));
children.push(body("Example: Classifying email as spam/not-spam is supervised (labels known). Grouping customers by shopping behavior is unsupervised (no predefined groups)."));
children.push(spacer());

// 1c bitmap indexing
children.push(h2("1(c): Discuss bitmap indexing in data warehouse. [1.5 Marks]"));
children.push(marksBox("[1.5 Marks | ~100 words]"));
children.push(topicBox("Data Warehouse Indexing | Subtopics: Bitmap Index, B-Tree Index, Join Index, Low-cardinality attributes"));
children.push(body("Bitmap Indexing is an efficient indexing technique in data warehouses used for attributes with low cardinality (few distinct values). A separate bit vector (bitmap) is created for each distinct value of the indexed attribute. Each bit in the vector corresponds to one row in the table:"));
children.push(bullet("If the row has that attribute value → bit = 1"));
children.push(bullet("Otherwise → bit = 0"));
children.push(body("Example: For attribute 'Gender' with values {Male, Female}: Male bitmap = [1,0,1,1,0] and Female = [0,1,0,0,1]. Boolean operations (AND, OR, NOT) on bitmaps are very fast, making bitmap indexes ideal for OLAP queries with multiple WHERE conditions on low-cardinality columns."));
children.push(spacer());

// 1d Manhattan vs Euclidean
children.push(h2("1(d): What is the difference between Manhattan Distance and Euclidean Distance? [1.5 Marks]"));
children.push(marksBox("[1.5 Marks | ~100 words]"));
children.push(topicBox("Distance Metrics → Similarity and Dissimilarity Measures | Subtopics: Minkowski Distance, L1 vs L2 norm"));
children.push(body("Euclidean Distance measures the straight-line distance between two points in n-dimensional space:"));
children.push(formula("Euclidean: d = √[Σ(xᵢ - yᵢ)²]"));
children.push(body("Manhattan Distance (City Block Distance) measures the sum of absolute differences:"));
children.push(formula("Manhattan: d = Σ|xᵢ - yᵢ|"));
children.push(body("Key differences: Euclidean allows diagonal movement (shortest path) while Manhattan only allows horizontal/vertical moves (like navigating a grid city). Euclidean is more sensitive to large outliers due to squaring; Manhattan is more robust. Euclidean is preferred for continuous low-dimensional data; Manhattan for high-dimensional or sparse data (e.g., text mining)."));
children.push(spacer());

// 1e support and confidence
children.push(h2("1(e): Discuss the importance of support and confidence. [1.5 Marks]"));
children.push(marksBox("[1.5 Marks | ~100 words]"));
children.push(topicBox("Association Rule Mining → Interestingness Measures | Subtopics: Support threshold, Confidence threshold, Lift, Apriori principle"));
children.push(formula("Support(X → Y) = P(X ∪ Y) = transactions containing both X and Y / total transactions"));
children.push(formula("Confidence(X → Y) = P(Y|X) = Support(X ∪ Y) / Support(X)"));
children.push(body("Importance of Support: Ensures that a rule is statistically significant — not just based on a few rare transactions. Rules below minimum support threshold (min_sup) are pruned early."));
children.push(body("Importance of Confidence: Measures the reliability/strength of the rule. A rule with 90% confidence means: whenever X is bought, Y is bought 90% of the time. Together, support and confidence filter out weak and uninteresting rules, ensuring only actionable patterns are retained in market basket analysis, recommendation systems, and medical diagnosis."));
children.push(spacer());

// 1f concept hierarchy
children.push(h2("1(f): What is meant by concept hierarchy? Explain its need. [1.5 Marks]"));
children.push(marksBox("[1.5 Marks | ~100 words]"));
children.push(topicBox("Data Cube & OLAP → Concept Hierarchy | Subtopics: Roll-up, Drill-down operations, Dimension hierarchies"));
children.push(body("A Concept Hierarchy defines a sequence of mappings from a set of low-level concepts to higher-level, more general concepts. It organizes data attributes at multiple levels of abstraction."));
children.push(body("Example: Location hierarchy: Street → City → State → Country → Continent"));
children.push(body("Another example: Time hierarchy: Hour → Day → Month → Quarter → Year"));
children.push(body("Need for Concept Hierarchies: (1) Enable Roll-up operations — aggregate data to higher levels (city → country). (2) Enable Drill-down — go from summary to detail (year → quarter → month). (3) Support data generalization and specialization in OLAP queries. (4) Reduce complexity of data and improve query performance in data warehouses."));
children.push(spacer());

// 1g Prior, Conditional, Posterior
children.push(h2("1(g): Define Prior Probability, Conditional Probability and Posterior Probability in context of Bayes theorem. [1.5 Marks]"));
children.push(marksBox("[1.5 Marks | ~100 words]"));
children.push(topicBox("Bayesian Classification → Naïve Bayes Classifier | Subtopics: Bayes Theorem, Prior/Likelihood/Posterior, MAP hypothesis"));
children.push(formula("Bayes Theorem: P(H|E) = P(E|H) × P(H) / P(E)"));
children.push(bold_body("Prior Probability P(H): ", "Probability of hypothesis H before observing any evidence. Example: P(Disease) = 0.01 (1% of population has disease)."));
children.push(bold_body("Conditional Probability P(E|H): ", "Probability of observing evidence E given that hypothesis H is true (also called Likelihood). Example: P(Fever|Disease) = 0.9."));
children.push(bold_body("Posterior Probability P(H|E): ", "Updated probability of H after observing evidence E. This is what we want to compute. Example: P(Disease|Fever) — probability of disease given patient has fever. It combines prior knowledge with observed evidence to give the most probable hypothesis."));
children.push(spacer());

// 1h Clustering Feature CF
children.push(h2("1(h): Calculate the Clustering Feature (CF) for points P1=(2,3), P2=(4,5), P3=(6,7). [1.5 Marks]"));
children.push(marksBox("[1.5 Marks | ~100 words]"));
children.push(topicBox("BIRCH Algorithm → Clustering Feature Tree | Subtopics: CF Triple (N, LS, SS), Cluster Centroid, Radius"));
children.push(formula("CF = (N, LS, SS)"));
children.push(body("Given: P1 = (2,3), P2 = (4,5), P3 = (6,7)"));
children.push(bullet("N = 3   (number of data points)"));
children.push(bullet("LS = (2+4+6, 3+5+7) = (12, 15)   (Linear Sum)"));
children.push(bullet("SS = (2²+4²+6²) + (3²+5²+7²) = (4+16+36) + (9+25+49) = 56 + 83 = 139   (Sum of Squares)"));
children.push(formula("CF = (3, (12, 15), 139)"));
children.push(body("Centroid = LS/N = (12/3, 15/3) = (4, 5). The CF triple is sufficient to derive all cluster statistics including centroid, radius, and diameter, enabling efficient merging of sub-clusters in the CF tree."));
children.push(spacer());

// 1i Crossover and Mutation
children.push(h2("1(i): Explain the process of Crossover and Mutation in Genetic algorithms. [1.5 Marks]"));
children.push(marksBox("[1.5 Marks | ~100 words]"));
children.push(topicBox("Genetic Algorithms → Evolutionary Computation | Subtopics: Chromosome representation, Selection, Crossover, Mutation, Fitness function"));
children.push(bold_body("Crossover (Recombination): ", "Two parent chromosomes (solutions) are combined to produce offspring. A crossover point is selected randomly, and the genetic material (bits) after that point is swapped between parents."));
children.push(formula("Parent 1: [1 0 1 | 1 0 0] → Child 1: [1 0 1 | 0 1 1]"));
children.push(formula("Parent 2: [0 1 0 | 0 1 1] → Child 2: [0 1 0 | 1 0 0]"));
children.push(bold_body("Mutation: ", "A random bit in the chromosome is flipped (0→1 or 1→0) with a small probability. Mutation introduces new genetic material and prevents premature convergence to local optima. It maintains population diversity."));
children.push(formula("Before mutation: [1 0 1 1 0]  →  After (bit 3 flips): [1 0 0 1 0]"));
children.push(spacer());

// 1j Data stream challenges
children.push(h2("1(j): List some challenges in mining data streams. [1.5 Marks]"));
children.push(marksBox("[1.5 Marks | ~100 words]"));
children.push(topicBox("Data Stream Mining → Real-time Analytics | Subtopics: Sliding window, Concept drift, Reservoir sampling, Sketches"));
children.push(bullet("Single-Pass Constraint: Data can be read only once; must be processed immediately or summarized in limited memory."));
children.push(bullet("Concept Drift: Statistical properties of the stream change over time, requiring adaptive models that can detect and respond to drift."));
children.push(bullet("High Data Volume and Speed: Streams arrive at extremely high rates (millions per second) leaving little processing time per record."));
children.push(bullet("Unbounded Nature: Data is potentially infinite — traditional batch algorithms and storage are infeasible."));
children.push(bullet("Real-Time Requirements: Results must be produced with minimal latency for time-critical applications like stock trading or network monitoring."));
children.push(spacer());

// ─── PART B 2025 ───
children.push(pageBreak());
children.push(h1("MAY 2025 — PART B — Detailed Questions"));

// Q2(a) Three-tier Data Warehouse Architecture
children.push(h2("Q2(a): Explain in detail the three-tier architecture of Data Warehouse. [7 Marks]"));
children.push(topicBox("Data Warehousing → Three-Tier Architecture | Subtopics: Data sources, ETL process, Data warehouse server, OLAP engine, Front-end tools, Metadata repository"));
children.push(body("A Data Warehouse (DW) follows a three-tier client-server architecture that provides a structured framework for storing, processing, and analyzing large volumes of historical data for decision support."));
children.push(spacer());

children.push(h3("Three-Tier Architecture"));
children.push(spacer());
children.push(bold_body("Tier 1 — Bottom Tier (Data Source / ETL Tier): ", "This is the data warehouse server itself (usually a relational database). It contains:"));
children.push(bullet("Multiple heterogeneous data sources: operational databases, flat files, external web sources, legacy systems, IoT sensors."));
children.push(bullet("ETL Process (Extract, Transform, Load): Data is extracted from sources, cleaned and transformed into a consistent format, and loaded into the data warehouse."));
children.push(bullet("Data cleaning resolves inconsistencies; transformation converts data types, units, and naming conventions; loading populates the warehouse."));
children.push(bullet("Tools: Informatica, Talend, Microsoft SSIS."));
children.push(spacer());

children.push(bold_body("Tier 2 — Middle Tier (OLAP Server): ", "This tier provides an abstraction layer for multidimensional data analysis:"));
children.push(bullet("ROLAP (Relational OLAP): Uses relational databases with star/snowflake schemas to simulate multidimensional processing."));
children.push(bullet("MOLAP (Multidimensional OLAP): Stores data in multidimensional cubes (array-based), offering fast query performance."));
children.push(bullet("HOLAP (Hybrid OLAP): Combines ROLAP and MOLAP — detailed data in relational, aggregates in MOLAP."));
children.push(bullet("Operations supported: Roll-up (aggregation), Drill-down (disaggregation), Slice, Dice, Pivot."));
children.push(bullet("Metadata Repository: Stores data about data — schema definitions, transformation rules, source-to-target mappings."));
children.push(spacer());

children.push(bold_body("Tier 3 — Top Tier (Front-End / Client Tier): ", "This is the user-facing layer where business users access and analyze data:"));
children.push(bullet("Query and Reporting Tools: Business Intelligence tools (Tableau, Power BI, Crystal Reports) generate reports and dashboards."));
children.push(bullet("Data Analysis Tools: Statistical analysis tools (R, SAS, SPSS) for advanced analytics."));
children.push(bullet("Data Mining Tools: Tools like Weka or Python sklearn for discovering patterns."));
children.push(bullet("OLAP Tools: Interactive exploration of multidimensional cubes."));
children.push(spacer());

children.push(h3("Architecture Diagram (Textual)"));
children.push(formula("[Data Sources] → (ETL) → [Data Warehouse DB] → [OLAP Server] → [Front-End Tools]"));
children.push(formula("   Tier 1                        Tier 1 (storage)       Tier 2               Tier 3"));
children.push(spacer());

children.push(h3("Benefits of Three-Tier Architecture"));
children.push(simpleTable(
  ["Benefit", "Description"],
  [
    ["Separation of Concerns", "Each tier handles specific tasks — ETL, analysis, presentation"],
    ["Scalability", "Each tier can be scaled independently"],
    ["Performance", "OLAP tier caches aggregates for fast query response"],
    ["Security", "Data access can be controlled at each tier"],
    ["Flexibility", "Different front-end tools can connect to same middle tier"],
  ]
));
children.push(spacer());

// Q2(b) Data Warehouse Schemas
children.push(h2("Q2(b): What are different schemas supported by a data warehouse? Explain in detail with an example scenario. [8 Marks]"));
children.push(topicBox("Data Warehouse Schema Design | Subtopics: Star Schema, Snowflake Schema, Galaxy/Fact Constellation Schema, Dimension tables, Fact tables, Normalization"));
children.push(body("A schema in a data warehouse defines the logical structure — how fact tables and dimension tables are organized and related. The main schemas are:"));
children.push(spacer());

children.push(h3("1. Star Schema"));
children.push(body("The most common data warehouse schema. A central Fact Table is directly connected to multiple Dimension Tables in a star-like pattern. Dimension tables are denormalized (flat)."));
children.push(formula("Fact Table (Sales_Fact): SalesID, ProductID, CustomerID, TimeID, StoreID, SalesAmount, Quantity"));
children.push(formula("Dimension Tables: Product_Dim, Customer_Dim, Time_Dim, Store_Dim"));
children.push(bullet("Advantages: Simple structure, easy to understand and query, fewer joins, faster query performance."));
children.push(bullet("Disadvantages: Data redundancy in dimension tables, higher storage requirement."));
children.push(spacer());

children.push(h3("2. Snowflake Schema"));
children.push(body("An extension of the star schema where dimension tables are normalized — split into multiple related tables forming a snowflake shape."));
children.push(formula("Product_Dim → Category_Dim → Department_Dim  (normalized hierarchy)"));
children.push(bullet("Advantages: Reduced data redundancy, saves storage space, easier maintenance."));
children.push(bullet("Disadvantages: More complex queries, more joins required, potentially slower performance."));
children.push(spacer());

children.push(h3("3. Galaxy Schema (Fact Constellation)"));
children.push(body("Multiple fact tables share dimension tables. Used when a data warehouse contains multiple subject areas."));
children.push(formula("Fact Table 1: Sales_Fact (ProductID, CustomerID, TimeID, SalesAmount)"));
children.push(formula("Fact Table 2: Inventory_Fact (ProductID, StoreID, TimeID, StockLevel)"));
children.push(formula("Shared Dimensions: Product_Dim, Time_Dim"));
children.push(bullet("Advantages: Can model complex business scenarios, shared dimensions ensure consistency."));
children.push(bullet("Disadvantages: Complex to design and manage."));
children.push(spacer());

children.push(h3("Example Scenario: Retail Supermarket Data Warehouse"));
children.push(simpleTable(
  ["Table", "Type", "Key Attributes"],
  [
    ["Sales_Fact", "Fact Table", "ProductID, CustomerID, TimeID, StoreID, Amount, Qty"],
    ["Product_Dim", "Dimension", "ProductID, Name, Brand, Category, Price"],
    ["Customer_Dim", "Dimension", "CustomerID, Name, City, Segment, Age_Group"],
    ["Time_Dim", "Dimension", "TimeID, Day, Month, Quarter, Year, IsHoliday"],
    ["Store_Dim", "Dimension", "StoreID, StoreName, City, Region, Size"],
  ]
));
children.push(body("This star schema enables queries like: 'Total sales by product category in Q3 2024 across all North India stores' — achievable with a single join between the fact table and dimension tables."));
children.push(spacer());

// Q3(a) Association Rules FP-Growth
children.push(pageBreak());
children.push(h2("Q3(a): Find frequent itemsets and generate association rules (min_sup=2, min_conf=60%) using A-Priori or FP-Growth. [10 Marks]"));
children.push(topicBox("Association Rule Mining → Apriori Algorithm | Subtopics: Support counting, Frequent itemsets, Confidence calculation, Rule generation, Apriori principle"));

children.push(h3("Transaction Database"));
children.push(simpleTable(
  ["Transaction ID", "Items"],
  [
    ["T1", "Hot Dogs, Buns, Ketchup"],
    ["T2", "Hot Dogs, Buns"],
    ["T3", "Hot Dogs, Coke, Chips"],
    ["T4", "Chips, Coke"],
    ["T5", "Chips, Ketchup"],
    ["T6", "Hot Dogs, Coke, Chips"],
  ]
));
children.push(body("min_sup = 2 (count-based), min_conf = 60%"));
children.push(spacer());

children.push(h3("Step 1: Count 1-itemset Frequencies"));
children.push(simpleTable(
  ["Item", "Transactions Containing It", "Support Count", "Frequent?"],
  [
    ["Hot Dogs", "T1,T2,T3,T6", "4", "Yes"],
    ["Buns", "T1,T2", "2", "Yes"],
    ["Ketchup", "T1,T5", "2", "Yes"],
    ["Coke", "T3,T4,T6", "3", "Yes"],
    ["Chips", "T3,T4,T5,T6", "4", "Yes"],
  ]
));
children.push(body("L₁ = {Hot Dogs, Buns, Ketchup, Coke, Chips} — all have support ≥ 2"));
children.push(spacer());

children.push(h3("Step 2: Generate C₂ and Find L₂"));
children.push(simpleTable(
  ["2-Itemset", "Transactions", "Support Count", "Frequent?"],
  [
    ["{Hot Dogs, Buns}", "T1,T2", "2", "Yes"],
    ["{Hot Dogs, Ketchup}", "T1", "1", "No"],
    ["{Hot Dogs, Coke}", "T3,T6", "2", "Yes"],
    ["{Hot Dogs, Chips}", "T3,T6", "2", "Yes"],
    ["{Buns, Ketchup}", "T1", "1", "No"],
    ["{Buns, Coke}", "None", "0", "No"],
    ["{Buns, Chips}", "None", "0", "No"],
    ["{Ketchup, Coke}", "None", "0", "No"],
    ["{Ketchup, Chips}", "T5", "1", "No"],
    ["{Coke, Chips}", "T3,T4,T6", "3", "Yes"],
  ]
));
children.push(body("L₂ = {{Hot Dogs, Buns}, {Hot Dogs, Coke}, {Hot Dogs, Chips}, {Coke, Chips}}"));
children.push(spacer());

children.push(h3("Step 3: Generate C₃ and Find L₃"));
children.push(simpleTable(
  ["3-Itemset", "Transactions", "Support Count", "Frequent?"],
  [
    ["{Hot Dogs, Coke, Chips}", "T3,T6", "2", "Yes"],
    ["{Hot Dogs, Buns, Ketchup}", "pruned — {Buns,Ketchup} not in L₂", "—", "Pruned"],
  ]
));
children.push(body("L₃ = {{Hot Dogs, Coke, Chips}}"));
children.push(spacer());

children.push(h3("Step 4: Generate Association Rules (min_conf = 60%)"));
children.push(body("For each frequent itemset, generate all non-empty subsets and compute confidence:"));
children.push(spacer());

children.push(h3("Rules from {Hot Dogs, Buns} (sup=2)"));
children.push(simpleTable(
  ["Rule", "Confidence Calculation", "Confidence", "Accepted?"],
  [
    ["Hot Dogs → Buns", "sup{HD,B}/sup{HD} = 2/4 = 50%", "50%", "No (<60%)"],
    ["Buns → Hot Dogs", "sup{HD,B}/sup{B} = 2/2 = 100%", "100%", "Yes ✓"],
  ]
));

children.push(h3("Rules from {Hot Dogs, Coke} (sup=2)"));
children.push(simpleTable(
  ["Rule", "Confidence", "Accepted?"],
  [
    ["Hot Dogs → Coke", "2/4 = 50%", "No"],
    ["Coke → Hot Dogs", "2/3 = 66.7%", "Yes ✓"],
  ]
));

children.push(h3("Rules from {Hot Dogs, Chips} (sup=2)"));
children.push(simpleTable(
  ["Rule", "Confidence", "Accepted?"],
  [
    ["Hot Dogs → Chips", "2/4 = 50%", "No"],
    ["Chips → Hot Dogs", "2/4 = 50%", "No"],
  ]
));

children.push(h3("Rules from {Coke, Chips} (sup=3)"));
children.push(simpleTable(
  ["Rule", "Confidence", "Accepted?"],
  [
    ["Coke → Chips", "3/3 = 100%", "Yes ✓"],
    ["Chips → Coke", "3/4 = 75%", "Yes ✓"],
  ]
));

children.push(h3("Rules from {Hot Dogs, Coke, Chips} (sup=2)"));
children.push(simpleTable(
  ["Rule", "Confidence", "Accepted?"],
  [
    ["Hot Dogs, Coke → Chips", "2/2 = 100%", "Yes ✓"],
    ["Hot Dogs, Chips → Coke", "2/2 = 100%", "Yes ✓"],
    ["Coke, Chips → Hot Dogs", "2/3 = 66.7%", "Yes ✓"],
    ["Hot Dogs → Coke, Chips", "2/4 = 50%", "No"],
    ["Coke → Hot Dogs, Chips", "2/3 = 66.7%", "Yes ✓"],
    ["Chips → Hot Dogs, Coke", "2/4 = 50%", "No"],
  ]
));

children.push(h3("Final Strong Association Rules (min_sup=2, min_conf≥60%)"));
children.push(bullet("Buns → Hot Dogs  (sup=2, conf=100%)"));
children.push(bullet("Coke → Hot Dogs  (sup=2, conf=66.7%)"));
children.push(bullet("Coke → Chips  (sup=3, conf=100%)"));
children.push(bullet("Chips → Coke  (sup=3, conf=75%)"));
children.push(bullet("Hot Dogs, Coke → Chips  (sup=2, conf=100%)"));
children.push(bullet("Hot Dogs, Chips → Coke  (sup=2, conf=100%)"));
children.push(bullet("Coke, Chips → Hot Dogs  (sup=2, conf=66.7%)"));
children.push(bullet("Coke → Hot Dogs, Chips  (sup=2, conf=66.7%)"));
children.push(spacer());

// Q3(b) ROLAP MOLAP HOLAP
children.push(h2("Q3(b): Differentiate between ROLAP, MOLAP and HOLAP servers. [5 Marks]"));
children.push(topicBox("OLAP Servers → Types of OLAP | Subtopics: Data cube storage, Relational vs Multidimensional, Query performance, Storage efficiency"));
children.push(simpleTable(
  ["Aspect", "ROLAP", "MOLAP", "HOLAP"],
  [
    ["Full Name", "Relational OLAP", "Multidimensional OLAP", "Hybrid OLAP"],
    ["Storage", "Relational Database (RDBMS)", "Multidimensional data cubes (arrays)", "Combination of RDBMS and cubes"],
    ["Query Speed", "Slower (SQL joins needed)", "Fastest (direct array access)", "Fast for aggregates, moderate for detail"],
    ["Scalability", "High — scales to TBs of data", "Limited — cube size grows exponentially", "Balanced scalability"],
    ["Data Volume", "Best for very large datasets", "Best for smaller, pre-aggregated data", "Moderate to large datasets"],
    ["Flexibility", "High — full SQL power", "Limited — fixed cube dimensions", "Flexible — best of both"],
    ["Storage Efficiency", "High (no pre-aggregation needed)", "Low (stores all possible aggregates)", "Moderate"],
    ["Examples", "Microsoft SQL Server Analysis Services (ROLAP mode)", "Essbase, SSAS MOLAP", "SSAS HOLAP mode"],
    ["Use Case", "Ad-hoc complex queries on large data", "Fast dashboard queries, fixed dimensions", "Mix of detail and summary queries"],
  ]
));
children.push(body("Summary: ROLAP provides flexibility and scalability, MOLAP provides speed, and HOLAP tries to balance both by storing summaries in cubes and detailed data in relational databases."));
children.push(spacer());

// Q4(a) Decision Trees with Information Gain
children.push(pageBreak());
children.push(h2("Q4(a): Decision Trees, Information Gain for Weather and Temperature attributes using Play dataset. [10 Marks]"));
children.push(topicBox("Decision Tree → ID3 Algorithm with Information Gain | Subtopics: Entropy calculation, Gain calculation for each attribute, Building the tree, Selecting root node"));

children.push(h3("Dataset: Play Tennis"));
children.push(simpleTable(
  ["Weather", "Temperature", "Play"],
  [
    ["Sunny", "Hot", "No"],
    ["Sunny", "Hot", "No"],
    ["Overcast", "Hot", "Yes"],
    ["Rainy", "Mild", "Yes"],
    ["Rainy", "Cool", "Yes"],
    ["Rainy", "Cool", "No"],
    ["Overcast", "Cool", "Yes"],
    ["Sunny", "Mild", "No"],
  ]
));
children.push(body("Total: 8 instances — 4 Yes, 4 No"));
children.push(spacer());

children.push(h3("Step 1: Calculate Entropy of Entire Dataset"));
children.push(formula("Entropy(D) = -(4/8)×log₂(4/8) - (4/8)×log₂(4/8)"));
children.push(formula("           = -(0.5×(-1)) - (0.5×(-1)) = 0.5 + 0.5 = 1.0 bit"));
children.push(spacer());

children.push(h3("Step 2: Information Gain for 'Weather' Attribute"));
children.push(body("Weather values and their distributions:"));
children.push(simpleTable(
  ["Weather Value", "Yes", "No", "Total", "Entropy"],
  [
    ["Sunny", "0", "3", "3", "-(0/3)log(0/3)-(3/3)log(3/3) = 0"],
    ["Overcast", "2", "0", "2", "-(2/2)log(2/2)-(0/2)log(0/2) = 0"],
    ["Rainy", "2", "1", "3", "-(2/3)log(2/3)-(1/3)log(1/3) = 0.918"],
  ]
));
children.push(formula("IG(Weather) = 1.0 - [(3/8)×0 + (2/8)×0 + (3/8)×0.918]"));
children.push(formula("           = 1.0 - [0 + 0 + 0.3443]"));
children.push(formula("           = 1.0 - 0.3443 = 0.6557 bits"));
children.push(spacer());

children.push(h3("Step 3: Information Gain for 'Temperature' Attribute"));
children.push(simpleTable(
  ["Temperature Value", "Yes", "No", "Total", "Entropy"],
  [
    ["Hot", "1", "2", "3", "-(1/3)log(1/3)-(2/3)log(2/3) = 0.918"],
    ["Mild", "1", "1", "2", "-(1/2)log(1/2)-(1/2)log(1/2) = 1.0"],
    ["Cool", "2", "1", "3", "-(2/3)log(2/3)-(1/3)log(1/3) = 0.918"],
  ]
));
children.push(formula("IG(Temperature) = 1.0 - [(3/8)×0.918 + (2/8)×1.0 + (3/8)×0.918]"));
children.push(formula("               = 1.0 - [0.3443 + 0.25 + 0.3443]"));
children.push(formula("               = 1.0 - 0.9386 = 0.0614 bits"));
children.push(spacer());

children.push(h3("Step 4: Select Root Node"));
children.push(simpleTable(
  ["Attribute", "Information Gain"],
  [
    ["Weather", "0.6557 bits  ← HIGHEST"],
    ["Temperature", "0.0614 bits"],
  ]
));
children.push(body("Weather has the highest Information Gain, so it is selected as the root node."));
children.push(spacer());

children.push(h3("Step 5: Build the Decision Tree"));
children.push(formula("           Weather"));
children.push(formula("         /    |    \\"));
children.push(formula("     Sunny  Overcast  Rainy"));
children.push(formula("       |      |        |"));
children.push(formula("      NO    YES   (Temperature?)"));
children.push(formula("                  /    |    \\"));
children.push(formula("               Hot   Mild   Cool"));
children.push(formula("               No    Yes    ?"));
children.push(spacer());
children.push(body("Note: For Rainy → Cool (2 Yes, 1 No): majority is Yes, so classify as Yes. The tree classifies all sunny days as No and all overcast days as Yes. For rainy days, Temperature is used as the next splitting attribute."));
children.push(spacer());

// Q4(b) Sequential Pattern Mining
children.push(h2("Q4(b): What is sequential pattern mining? Explain in brief. [5 Marks]"));
children.push(topicBox("Sequential Pattern Mining | Subtopics: Sequences, Subsequences, AprioriAll, GSP, FreeSpan, PrefixSpan algorithms, Applications"));
children.push(body("Sequential Pattern Mining (SPM) is a data mining technique that discovers frequently occurring ordered sequences of events or items in a database of sequences. Unlike association rule mining which ignores order, SPM considers the temporal or positional ordering of items."));
children.push(spacer());

children.push(h3("Formal Definition"));
children.push(body("A sequence S = <s₁, s₂, ..., sₙ> where each sᵢ is an itemset (called an event). A sequence α is a subsequence of β if all events in α appear in β in the same order. A sequential pattern is a subsequence with support ≥ min_sup."));
children.push(formula("Example: <{Laptop} {Mouse} {Monitor}> means: a customer first bought a Laptop, then a Mouse, then a Monitor."));
children.push(spacer());

children.push(h3("Applications"));
children.push(bullet("E-commerce: 'Customers who bought X, then Y, often buy Z next' — useful for targeted marketing."));
children.push(bullet("Healthcare: Finding disease progression patterns — 'Patients with A, then B, develop C'."));
children.push(bullet("Web Usage Mining: Discovering frequent URL access patterns to optimize website design."));
children.push(bullet("Bioinformatics: Finding frequent subsequences in DNA, protein, or RNA sequences."));
children.push(bullet("Network Security: Identifying attack patterns in log files."));
children.push(spacer());

children.push(h3("Main Algorithms for Sequential Pattern Mining"));
children.push(simpleTable(
  ["Algorithm", "Approach", "Key Feature"],
  [
    ["AprioriAll", "Level-wise Apriori-based", "First SPM algorithm; slow due to candidate generation"],
    ["GSP (Generalized SP)", "Level-wise with time constraints", "Supports time gaps, sliding windows, taxonomies"],
    ["FreeSpan", "Pattern-fragment growth", "Avoids explicit candidate generation"],
    ["PrefixSpan", "Prefix-projection based", "Highly efficient; projects DB into smaller sub-databases"],
    ["SPADE", "Equivalence class", "Uses vertical data format for fast intersection"],
  ]
));
children.push(spacer());

// Q5(a) Backpropagation
children.push(h2("Q5(a): What is backpropagation in neural networks? Explain classification by backpropagation with mathematical formulation. [7 Marks]"));
children.push(topicBox("Artificial Neural Networks → Backpropagation Algorithm | Subtopics: Forward propagation, Loss function, Gradient descent, Weight updates, Sigmoid activation, Chain rule"));

children.push(h3("What is Backpropagation?"));
children.push(body("Backpropagation (Backward Propagation of Errors) is the fundamental algorithm for training multi-layer neural networks (MLPs). It efficiently computes the gradient of the loss function with respect to each weight using the chain rule of calculus, then uses gradient descent to update the weights to minimize the loss."));
children.push(spacer());

children.push(h3("Neural Network Architecture for Classification"));
children.push(body("A typical network has: Input Layer (d features) → Hidden Layer(s) → Output Layer (c classes with Softmax activation)."));
children.push(spacer());

children.push(h3("Step 1: Forward Propagation"));
children.push(body("Compute activations layer by layer from input to output:"));
children.push(formula("Net input at hidden neuron j: net_j = Σᵢ wᵢⱼ × xᵢ + bⱼ"));
children.push(formula("Activation (Sigmoid): O_j = f(net_j) = 1 / (1 + e^(-net_j))"));
children.push(formula("Net input at output neuron k: net_k = Σⱼ wⱼₖ × O_j + bₖ"));
children.push(formula("Output activation: O_k = f(net_k)   (sigmoid or softmax for classification)"));
children.push(spacer());

children.push(h3("Step 2: Loss Calculation"));
children.push(formula("Mean Squared Error: L = (1/2) × Σₖ (tₖ - O_k)²"));
children.push(body("Where tₖ is the true class label and O_k is the predicted output. For multi-class: Cross-Entropy Loss = -Σₖ tₖ × log(O_k)"));
children.push(spacer());

children.push(h3("Step 3: Backward Propagation — Output Layer"));
children.push(body("Compute the error gradient at output layer using chain rule:"));
children.push(formula("δₖ = (∂L/∂O_k) × f'(net_k)"));
children.push(formula("For MSE: ∂L/∂O_k = -(tₖ - O_k)"));
children.push(formula("Derivative of sigmoid: f'(net_k) = O_k × (1 - O_k)"));
children.push(formula("Therefore: δₖ = (tₖ - O_k) × O_k × (1 - O_k)"));
children.push(spacer());

children.push(h3("Step 4: Backward Propagation — Hidden Layer"));
children.push(body("Propagate error backwards to hidden layer:"));
children.push(formula("δⱼ = f'(net_j) × Σₖ (δₖ × wⱼₖ)"));
children.push(formula("   = O_j × (1 - O_j) × Σₖ (δₖ × wⱼₖ)"));
children.push(spacer());

children.push(h3("Step 5: Weight Updates (Gradient Descent)"));
children.push(formula("Δwⱼₖ = η × δₖ × O_j   (for output layer weights)"));
children.push(formula("Δwᵢⱼ = η × δⱼ × xᵢ    (for hidden layer weights)"));
children.push(formula("New weight: w ← w + Δw"));
children.push(body("Where η (eta) is the learning rate (typically 0.01 to 0.1). This update moves weights in the direction that reduces the loss."));
children.push(spacer());

children.push(h3("Complete Backpropagation Algorithm"));
children.push(formula("Initialize weights wᵢⱼ, wⱼₖ randomly (small values)"));
children.push(formula("REPEAT until convergence:"));
children.push(formula("  FOR each training sample (x, t):"));
children.push(formula("    1. Forward pass: compute O_j, O_k"));
children.push(formula("    2. Compute loss L = (1/2)Σ(tₖ - O_k)²"));
children.push(formula("    3. Compute δₖ for output layer"));
children.push(formula("    4. Compute δⱼ for hidden layer"));
children.push(formula("    5. Update wⱼₖ = wⱼₖ + η×δₖ×O_j"));
children.push(formula("    6. Update wᵢⱼ = wᵢⱼ + η×δⱼ×xᵢ"));
children.push(formula("UNTIL (loss < threshold or max_epochs reached)"));
children.push(spacer());

children.push(h3("Key Properties"));
children.push(simpleTable(
  ["Property", "Details"],
  [
    ["Learning Rate η", "Too high → oscillates; Too low → slow convergence. Adaptive methods: Adam, RMSprop"],
    ["Activation Functions", "Sigmoid, ReLU, Tanh — ReLU most common in deep networks (avoids vanishing gradient)"],
    ["Vanishing Gradient Problem", "In deep networks, gradients become tiny → use ReLU, Batch Normalization, ResNet"],
    ["Overfitting", "Regularization (L1, L2, Dropout) to prevent memorization of training data"],
  ]
));
children.push(spacer());

// Q5(b) K-means with 7 points
children.push(h2("Q5(b): Compute 2 clusters using K-means for 7 points in 2D space. Initial centers (1,1) and (5,7). Execute 2 iterations. [8 Marks]"));
children.push(topicBox("K-Means Clustering → Iterative Algorithm | Subtopics: Distance calculation, Centroid update, Convergence, Euclidean distance"));

children.push(h3("Given Data"));
children.push(simpleTable(
  ["Point", "A (x₁)", "B (x₂)"],
  [
    ["R1", "1.0", "1.0"],
    ["R2", "1.5", "2.0"],
    ["R3", "3.0", "4.0"],
    ["R4", "5.0", "7.0"],
    ["R5", "3.5", "5.0"],
    ["R6", "4.5", "5.0"],
    ["R7", "3.5", "4.5"],
  ]
));
children.push(body("Initial Centroids: C₁ = (1.0, 1.0),  C₂ = (5.0, 7.0)"));
children.push(spacer());

children.push(h3("ITERATION 1 — Step 1: Assign Points to Nearest Centroid"));
children.push(body("Euclidean distance formula: d = √[(x₁-cx₁)² + (x₂-cx₂)²]"));
children.push(simpleTable(
  ["Point", "d(P, C₁=(1,1))", "d(P, C₂=(5,7))", "Assigned Cluster"],
  [
    ["R1(1,1)", "√[(1-1)²+(1-1)²] = 0", "√[(1-5)²+(1-7)²] = √(16+36) = 7.21", "C₁"],
    ["R2(1.5,2)", "√[(0.5)²+(1)²] = √1.25 = 1.12", "√[(3.5)²+(5)²] = √37.25 = 6.10", "C₁"],
    ["R3(3,4)", "√[(2)²+(3)²] = √13 = 3.61", "√[(2)²+(3)²] = √13 = 3.61", "C₁ (tie→C₁)"],
    ["R4(5,7)", "√[(4)²+(6)²] = √52 = 7.21", "√[(0)²+(0)²] = 0", "C₂"],
    ["R5(3.5,5)", "√[(2.5)²+(4)²] = √22.25 = 4.72", "√[(1.5)²+(2)²] = √6.25 = 2.50", "C₂"],
    ["R6(4.5,5)", "√[(3.5)²+(4)²] = √28.25 = 5.32", "√[(0.5)²+(2)²] = √4.25 = 2.06", "C₂"],
    ["R7(3.5,4.5)", "√[(2.5)²+(3.5)²] = √18.5 = 4.30", "√[(1.5)²+(2.5)²] = √8.5 = 2.92", "C₂"],
  ]
));
children.push(body("After Iteration 1 Assignment:"));
children.push(bullet("Cluster 1 (C₁): R1(1,1), R2(1.5,2), R3(3,4)"));
children.push(bullet("Cluster 2 (C₂): R4(5,7), R5(3.5,5), R6(4.5,5), R7(3.5,4.5)"));
children.push(spacer());

children.push(h3("ITERATION 1 — Step 2: Update Centroids"));
children.push(formula("New C₁ = ((1+1.5+3)/3, (1+2+4)/3) = (5.5/3, 7/3) = (1.833, 2.333)"));
children.push(formula("New C₂ = ((5+3.5+4.5+3.5)/4, (7+5+5+4.5)/4) = (16.5/4, 21.5/4) = (4.125, 5.375)"));
children.push(spacer());

children.push(h3("ITERATION 2 — Step 1: Re-assign Points"));
children.push(body("New centroids: C₁ = (1.833, 2.333),  C₂ = (4.125, 5.375)"));
children.push(simpleTable(
  ["Point", "d(P, C₁=(1.833,2.333))", "d(P, C₂=(4.125,5.375))", "Cluster"],
  [
    ["R1(1,1)", "√[(0.833)²+(1.333)²]=√2.47=1.57", "√[(3.125)²+(4.375)²]=√28.90=5.38", "C₁"],
    ["R2(1.5,2)", "√[(0.333)²+(0.333)²]=√0.22=0.47", "√[(2.625)²+(3.375)²]=√18.29=4.28", "C₁"],
    ["R3(3,4)", "√[(1.167)²+(1.667)²]=√4.14=2.03", "√[(1.125)²+(1.375)²]=√3.16=1.78", "C₂"],
    ["R4(5,7)", "√[(3.167)²+(4.667)²]=√31.78=5.64", "√[(0.875)²+(1.625)²]=√3.41=1.85", "C₂"],
    ["R5(3.5,5)", "√[(1.667)²+(2.667)²]=√9.90=3.15", "√[(0.625)²+(0.375)²]=√0.53=0.73", "C₂"],
    ["R6(4.5,5)", "√[(2.667)²+(2.667)²]=√14.22=3.77", "√[(0.375)²+(0.375)²]=√0.28=0.53", "C₂"],
    ["R7(3.5,4.5)", "√[(1.667)²+(2.167)²]=√7.47=2.73", "√[(0.625)²+(0.875)²]=√1.16=1.08", "C₂"],
  ]
));
children.push(spacer());
children.push(body("After Iteration 2 Assignment:"));
children.push(bullet("Cluster 1 (C₁): R1(1,1), R2(1.5,2)"));
children.push(bullet("Cluster 2 (C₂): R3(3,4), R4(5,7), R5(3.5,5), R6(4.5,5), R7(3.5,4.5)"));
children.push(spacer());

children.push(h3("Update Centroids After Iteration 2"));
children.push(formula("Next C₁ = ((1+1.5)/2, (1+2)/2) = (1.25, 1.5)"));
children.push(formula("Next C₂ = ((3+5+3.5+4.5+3.5)/5, (4+7+5+5+4.5)/5) = (19.5/5, 25.5/5) = (3.9, 5.1)"));
children.push(spacer());
children.push(h3("Final Result After 2 Iterations"));
children.push(simpleTable(
  ["Cluster", "Points", "Next Centroid"],
  [
    ["C₁", "R1(1,1), R2(1.5,2)", "(1.25, 1.5)"],
    ["C₂", "R3(3,4), R4(5,7), R5(3.5,5), R6(4.5,5), R7(3.5,4.5)", "(3.9, 5.1)"],
  ]
));
children.push(spacer());

// Q6(a) Trend Analysis
children.push(pageBreak());
children.push(h2("Q6(a): Explain Trend Analysis in time-series data with all its components. [7 Marks]"));
children.push(topicBox("Time Series Mining → Trend Analysis | Subtopics: Long-term trend, Linear/Non-linear trends, Moving averages, Trend decomposition, Forecasting"));

children.push(h3("What is Trend Analysis?"));
children.push(body("Trend Analysis in time series is the process of identifying and modeling the long-term direction of movement in a dataset over time. A trend represents the overall tendency of a variable to increase, decrease, or remain stable across an extended period, after filtering out short-term fluctuations (seasonal and cyclical effects)."));
children.push(spacer());

children.push(h3("Types of Trends"));
children.push(bullet("Upward (Positive) Trend: The variable consistently increases over time. Example: India's GDP growth from 1990 to 2023."));
children.push(bullet("Downward (Negative) Trend: The variable consistently decreases. Example: Landline telephone subscriptions declining from 2000 onwards."));
children.push(bullet("Horizontal (Stationary) Trend: No significant long-term change. The series fluctuates around a constant mean."));
children.push(bullet("Non-linear Trend: Exponential, logarithmic, or polynomial growth/decline. Example: Internet user growth (S-curve)."));
children.push(spacer());

children.push(h3("Components of Time Series (Detailed)"));
children.push(spacer());
children.push(bold_body("1. Trend (T): ", "Long-term movement in data. Identified by fitting a trend line (linear regression) or using moving averages. Formula for linear trend: Ŷₜ = a + b×t, where a is intercept and b is slope."));
children.push(bold_body("2. Seasonal Component (S): ", "Regular repeating fluctuations within a fixed period. Measured by seasonal indices: SI = (Actual value / Trend value) × 100. Period is known and fixed (e.g., quarterly, monthly)."));
children.push(bold_body("3. Cyclical Component (C): ", "Long-wave fluctuations of period > 1 year with variable length. Caused by economic/business cycles. Harder to isolate than seasonality."));
children.push(bold_body("4. Irregular Component (I): ", "Random, unpredictable residual after removing T, S, C. Represents noise, random shocks, and one-time events."));
children.push(spacer());

children.push(h3("Methods for Trend Detection"));
children.push(simpleTable(
  ["Method", "Description", "Best For"],
  [
    ["Moving Average", "Smooth data by averaging over a sliding window of size n", "Short-term trend visualization"],
    ["Least Squares Regression", "Fit a linear line Y = a + bX minimizing Σ(Y - Ŷ)²", "Long-term linear trend estimation"],
    ["Exponential Smoothing", "Weighted average giving more weight to recent observations: Sₜ = α×Yₜ + (1-α)×Sₜ₋₁", "Adaptive short-term forecasting"],
    ["Decomposition", "Separate time series into T, S, C, I using STL or classical decomposition", "Multi-component analysis"],
  ]
));
children.push(spacer());

children.push(h3("Decomposition Models"));
children.push(formula("Additive Model:    Yₜ = Tₜ + Sₜ + Cₜ + Iₜ"));
children.push(formula("Multiplicative Model: Yₜ = Tₜ × Sₜ × Cₜ × Iₜ"));
children.push(body("Additive model: seasonal variations are constant in magnitude (absolute). Multiplicative model: seasonal variations are proportional to trend level (percentage). In practice, additive is used when seasonal amplitude is stable; multiplicative when it grows/shrinks with the trend."));
children.push(spacer());

// Q6(b) Hierarchical Clustering
children.push(h2("Q6(b): What is Hierarchical Clustering and its types? Describe single linkage, complete linkage and average linkage. [8 Marks]"));
children.push(topicBox("Hierarchical Clustering → Agglomerative & Divisive | Subtopics: Dendrogram, Single/Complete/Average Linkage, Ward's method, Cophenetic distance"));

children.push(h3("What is Hierarchical Clustering?"));
children.push(body("Hierarchical Clustering is a clustering technique that creates a tree-like hierarchy of clusters called a dendrogram. Unlike K-means, it does not require specifying k in advance. The dendrogram can be cut at any level to obtain the desired number of clusters."));
children.push(spacer());

children.push(h3("Two Types of Hierarchical Clustering"));
children.push(bold_body("1. Agglomerative (Bottom-Up): ", "Start with each point as its own cluster. Iteratively merge the two closest clusters until only one cluster remains (or a stopping criterion is met). Most commonly used."));
children.push(formula("Algorithm: Start with n clusters → merge 2 closest → n-1 clusters → ... → 1 cluster"));
children.push(spacer());
children.push(bold_body("2. Divisive (Top-Down): ", "Start with all data in one cluster. Iteratively split the cluster into smaller groups until each point is its own cluster. Less common due to high computational cost."));
children.push(formula("Algorithm: Start with 1 cluster → split → 2 clusters → ... → n clusters"));
children.push(spacer());

children.push(h3("Linkage Criteria — How to Measure Distance Between Clusters"));
children.push(spacer());

children.push(bold_body("1. Single Linkage (MIN Linkage): ", "Distance between two clusters is defined as the minimum distance between any pair of points, one from each cluster."));
children.push(formula("d(Cᵢ, Cⱼ) = min {dist(x, y) : x ∈ Cᵢ, y ∈ Cⱼ}"));
children.push(bullet("Characteristics: Can form long chain-like clusters (chaining effect). Good for detecting non-elliptical shapes."));
children.push(bullet("Problem: Sensitive to noise and outliers; can produce very unbalanced clusters."));
children.push(spacer());

children.push(bold_body("2. Complete Linkage (MAX Linkage): ", "Distance between clusters is the maximum distance between any pair of points from each cluster."));
children.push(formula("d(Cᵢ, Cⱼ) = max {dist(x, y) : x ∈ Cᵢ, y ∈ Cⱼ}"));
children.push(bullet("Characteristics: Tends to produce compact, spherical clusters of similar diameter."));
children.push(bullet("Problem: Also sensitive to outliers since outlier-to-outlier distance may dominate."));
children.push(spacer());

children.push(bold_body("3. Average Linkage (UPGMA): ", "Distance between clusters is the average distance between all pairs of points, one from each cluster."));
children.push(formula("d(Cᵢ, Cⱼ) = (1/|Cᵢ||Cⱼ|) × Σ Σ dist(x, y)   x∈Cᵢ, y∈Cⱼ"));
children.push(bullet("Characteristics: A compromise between single and complete linkage. Less sensitive to outliers than either."));
children.push(bullet("Produces clusters with moderate compactness; most widely used in practice."));
children.push(spacer());

children.push(h3("Comparison of Linkage Methods"));
children.push(simpleTable(
  ["Criterion", "Single Linkage", "Complete Linkage", "Average Linkage"],
  [
    ["Definition", "Min inter-cluster distance", "Max inter-cluster distance", "Mean inter-cluster distance"],
    ["Cluster Shape", "Elongated, chained clusters", "Compact, spherical clusters", "Intermediate/balanced"],
    ["Outlier Sensitivity", "High", "High", "Moderate"],
    ["Chaining Effect", "Prone", "Not prone", "Somewhat prone"],
    ["Use Case", "Non-convex shapes", "Tight compact clusters", "General-purpose"],
  ]
));
children.push(spacer());

// Q7(a) Class Imbalance
children.push(h2("Q7(a): Describe class imbalance problem and its solutions. [5 Marks]"));
children.push(topicBox("Class Imbalance → Imbalanced Classification | Subtopics: Oversampling, Undersampling, SMOTE, Cost-sensitive learning, Ensemble methods"));

children.push(h3("The Class Imbalance Problem"));
children.push(body("Class imbalance occurs when one class (majority class) has significantly more instances than another class (minority class) in the training dataset. A classifier trained on such data tends to be biased toward the majority class, often predicting everything as the majority class and achieving high accuracy while completely ignoring the minority class."));
children.push(formula("Example: Fraud Detection — 99% legitimate transactions (majority), 1% fraudulent (minority)."));
children.push(body("A classifier that labels all transactions as 'legitimate' gets 99% accuracy but detects zero fraud — completely useless."));
children.push(spacer());

children.push(h3("Solutions to Class Imbalance"));
children.push(bold_body("1. Oversampling (Increase Minority Class): "));
children.push(bullet("Random Oversampling: Duplicate random minority class samples. Simple but leads to overfitting."));
children.push(bullet("SMOTE (Synthetic Minority Oversampling Technique): Generate synthetic minority samples by interpolating between existing minority samples using k-nearest neighbors. Creates new, realistic samples that are not exact duplicates."));
children.push(formula("New sample: x_new = x_i + λ × (x_j - x_i)   where λ ∈ [0,1]"));
children.push(spacer());

children.push(bold_body("2. Undersampling (Reduce Majority Class): "));
children.push(bullet("Random Undersampling: Randomly remove majority class samples. Simple but causes information loss."));
children.push(bullet("Tomek Links: Remove borderline majority class samples that are too close to minority samples. Cleans the decision boundary."));
children.push(bullet("Cluster Centroids: Replace clusters of majority class samples with their centroids."));
children.push(spacer());

children.push(bold_body("3. Cost-Sensitive Learning: "));
children.push(body("Assign higher misclassification cost to the minority class. The classifier is penalized more for misclassifying minority samples, forcing it to pay attention to them."));
children.push(formula("Cost matrix: cost(FN) >> cost(FP) for minority class"));
children.push(spacer());

children.push(bold_body("4. Algorithmic Approaches: "));
children.push(bullet("Ensemble Methods: Balanced Random Forest, EasyEnsemble — combine multiple classifiers trained on balanced subsets."));
children.push(bullet("Threshold Adjustment: Lower the decision threshold for the minority class prediction."));
children.push(bullet("Use appropriate metrics: F1-Score, ROC-AUC, Matthews Correlation Coefficient (MCC) instead of accuracy."));
children.push(spacer());

// Q7(b) Web Mining
children.push(h2("Q7(b): What is web mining? What are its categories? [5 Marks]"));
children.push(topicBox("Web Mining → Types and Applications | Subtopics: Web Content Mining, Web Structure Mining, Web Usage Mining, PageRank, Log file analysis"));

children.push(h3("What is Web Mining?"));
children.push(body("Web Mining is the application of data mining techniques to automatically discover and extract useful information and knowledge from World Wide Web data including web content, hyperlink structure, and user access patterns. It combines techniques from data mining, NLP, information retrieval, and machine learning."));
children.push(spacer());

children.push(h3("Three Categories of Web Mining"));
children.push(spacer());

children.push(bold_body("1. Web Content Mining: ", "Extracting useful information from the actual content of web documents (text, images, audio, video, hyperlinks on the page)."));
children.push(bullet("Text mining: Document classification, clustering, information extraction, summarization."));
children.push(bullet("Image/video mining: Visual content extraction."));
children.push(bullet("Applications: Search engines (indexing), spam detection, news aggregation, sentiment analysis."));
children.push(bullet("Tools: Web scrapers (Scrapy, BeautifulSoup), NLP libraries."));
children.push(spacer());

children.push(bold_body("2. Web Structure Mining: ", "Analyzing the hyperlink structure of the web to discover authority and hub pages."));
children.push(bullet("PageRank Algorithm (Google): Assigns rank to pages based on number and quality of inbound links. A page linked by many high-rank pages gets a higher PageRank."));
children.push(bullet("HITS Algorithm (Hyperlink-Induced Topic Search): Identifies 'hubs' (pages with many good outgoing links) and 'authorities' (pages with many incoming links)."));
children.push(bullet("Applications: Search engine ranking, identifying influential pages/people in social networks."));
children.push(spacer());

children.push(bold_body("3. Web Usage Mining: ", "Analyzing web server logs, browser logs, and user click-streams to understand user behavior and navigation patterns."));
children.push(bullet("Web log analysis: IP addresses, timestamps, URLs, sessions from server access logs."));
children.push(bullet("Sequential pattern mining on sessions: Find frequent navigation paths."));
children.push(bullet("Applications: Website personalization (recommending next page), improving website layout, understanding user segments, targeted advertising."));
children.push(spacer());

children.push(simpleTable(
  ["Category", "Data Source", "Techniques Used", "Application"],
  [
    ["Web Content Mining", "Web page text, images, HTML", "NLP, Text classification, Clustering", "Search engines, Spam detection"],
    ["Web Structure Mining", "Hyperlinks between pages", "Graph algorithms, PageRank, HITS", "Page ranking, Influencer detection"],
    ["Web Usage Mining", "Server logs, clickstreams", "Sequential pattern mining, Clustering", "Personalization, UX optimization"],
  ]
));
children.push(spacer());

// Q7(c) Social Network Analysis
children.push(h2("Q7(c): Write a short note on Social Network Analysis. [5 Marks]"));
children.push(topicBox("Social Network Analysis (SNA) → Graph-based Mining | Subtopics: Nodes, Edges, Centrality measures, Community detection, Influence propagation"));

children.push(h3("Social Network Analysis (SNA)"));
children.push(body("Social Network Analysis (SNA) is the study of social structures using network and graph theory. It models individuals (users, organizations) as nodes and their relationships (friendships, collaborations, communications) as edges in a graph."));
children.push(formula("G = (V, E)   where V = nodes (entities), E = edges (relationships)"));
children.push(spacer());

children.push(h3("Key Metrics in SNA"));
children.push(simpleTable(
  ["Metric", "Definition", "Application"],
  [
    ["Degree Centrality", "Number of direct connections a node has", "Identify most connected users"],
    ["Betweenness Centrality", "How often a node lies on shortest paths between other nodes", "Identify information brokers/bridges"],
    ["Closeness Centrality", "How quickly a node can reach all other nodes", "Identify nodes with global influence"],
    ["PageRank", "Importance based on quality of incoming links", "Web page ranking, Twitter influence"],
    ["Clustering Coefficient", "Measure of how interconnected a node's neighbors are", "Detect tightly-knit communities"],
  ]
));
children.push(spacer());

children.push(h3("Community Detection"));
children.push(body("One of the primary tasks in SNA is finding communities — groups of nodes that are more densely connected to each other than to the rest of the network. Algorithms include:"));
children.push(bullet("Girvan-Newman Algorithm: Iteratively removes edges with highest betweenness centrality."));
children.push(bullet("Louvain Method: Maximizes modularity (Q) — the fraction of edges within communities minus expected fraction."));
children.push(bullet("Spectral Clustering: Uses eigenvectors of graph Laplacian matrix."));
children.push(spacer());

children.push(h3("Applications of SNA"));
children.push(bullet("Viral Marketing: Identify key influencers to maximize information spread."));
children.push(bullet("Fraud Detection: Unusual connection patterns may indicate fraudulent rings."));
children.push(bullet("Epidemiology: Model how diseases spread through social contacts."));
children.push(bullet("Recommendation Systems: Friends' preferences inform recommendations."));
children.push(bullet("Organizational Analysis: Identify informal leaders and communication bottlenecks in companies."));
children.push(bullet("Counter-Terrorism: Identifying key members and structure of terrorist networks."));
children.push(spacer());

children.push(body("SNA has become critical in the era of Facebook, Twitter, LinkedIn, and WhatsApp where billions of relationships generate massive graph data that can be mined for insights about human behavior, information diffusion, and social influence."));

// ─── CREATE DOC ──────────────────────────────────────────────────────────────

const doc = new Document({
  styles: {
    default: {
      document: { run: { font: "Arial", size: 22 } }
    },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, font: "Arial", color: "1F3864" },
        paragraph: { spacing: { before: 360, after: 180 }, outlineLevel: 0 }
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Arial", color: "2E75B6" },
        paragraph: { spacing: { before: 280, after: 120 }, outlineLevel: 1 }
      },
    ]
  },
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      }
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 }
      }
    },
    children
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("Data_Mining_Complete_PYQ_Answers.docx", buf);
  console.log("Done! File written.");
});