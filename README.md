 

# 🌟 **VaaniMeter**

### *AI-Powered Spoken Introduction Evaluation Tool*

---

## 📌 **Overview**

**VaaniMeter** is an AI-powered evaluation tool designed to score spoken self-introductions using a **strict, deterministic rubric**.
It provides instant feedback, transparent scoring, radar-chart visualization, and a downloadable professional PDF report.

The tool brings structure, clarity, and objectivity to communication assessment—making it ideal for academic evaluation, skill-building, and training environments.

---

## 🚀 **Features**

### 🔹 Dual Input Support

* Paste transcript directly
* Upload `.txt` files

### 🔹 Strict Rubric-Based Scoring (0–100)

Scores are computed across five categories:

* **Content & Structure (40 pts)**
* **Speech Rate (10 pts)**
* **Language & Grammar (20 pts)**
* **Clarity (15 pts)**
* **Engagement (15 pts)**

### 🔹 Transparent Score Breakdown

Users can view **how each point was calculated**, including:

* Keyword matches
* Grammar analysis
* Filler rate
* Sentiment score
* WPM category mapping
* Flow structure rating

### 🔹 Radar Chart Visualization

A spider chart helps users visually understand their performance across categories.

### 🔹 PDF Report Generation

Download a professional report containing:

* Input transcript
* All scoring components
* Radar chart visualization
* Strengths & improvement areas
* Final score summary

### 🔹 JSON Output (Optional)

Advanced users can view raw JSON scoring data.

---

## 📁 **Project Structure**

| File               | Description                                                                           |
| ------------------ | ------------------------------------------------------------------------------------- |
| `app.py`           | Main Streamlit interface: input handling, UI components, chart rendering, PDF export. |
| `scorer.py`        | Core scoring engine implementing the strict rubric evaluation logic.                  |
| `utils.py`         | Helper utilities for NLP tools, radar chart rendering, and PDF report generation.     |
| `requirements.txt` | Python dependency list.                                                               |

---

## 🧠 **How the Scoring Engine Works**

### **1. Content & Structure (40 pts)**

Checks:

* Quality of salutation
* Presence of must-have keywords: *Name, Age, Class/School, Family, Hobbies*
* Presence of good-to-have details: fun fact, goal, strengths, etc.
* Flow and natural ordering of introduction sections

### **2. Speech Rate (10 pts)**

Assumes a fixed **52-second** speaking duration
Computes WPM:

```
wpm = total_words / (52/60)
```

Ideal score range: **111–140 WPM**

### **3. Language (20 pts)**

* Grammar scoring using **LanguageTool**
* Vocabulary quality measured by **Type-Token Ratio (TTR)**

### **4. Clarity (15 pts)**

Detects filler words:
`"um, uh, like, you know, hmm, kinda, sort of"`
Score based on filler percentage.

### **5. Engagement (15 pts)**

Uses **VADER sentiment analysis** to measure positivity and overall tone.

---

## 🔄 **End-to-End Data Flow**

1. **User Input**
   Text is pasted or uploaded.

2. **Processing**
   `app.py` sends transcript to `IntroductionScorer.calculate_final_score()`.

3. **Analysis**
   `scorer.py`:

   * cleans text
   * runs NLP tools
   * computes all category scores
   * generates JSON output

4. **Visualization**
   `create_radar_chart()` renders a spider chart.

5. **Report Generation**
   `create_pdf_report()` generates a downloadable report using ReportLab.

6. **Output**
   Streamlit displays all scores, breakdowns, and visualizations.

---

## 🛠 **How to Run Locally**

1. Install dependencies:

```
pip install -r requirements.txt
```

2. Launch the app:

```
streamlit run app.py
```

3. Open in your browser:
   👉 [http://localhost:8501](http://localhost:8501)

---

## 🌐 **Deployment**

Not yet deployed.
The project is fully compatible with:

* Streamlit Cloud
* HuggingFace Spaces
* Render
* Railway

---

## 🧪 **Testing**

Testing was done on:

* High-quality transcripts (expected: **>80**)
* Average transcripts (**50–70**)
* Poor transcripts (**<40**)

Old testing scripts are removed after cleanup.
The final scoring matches rubric expectations consistently.

---

## ✨ **What Makes VaaniMeter Unique**

* Uses a **strict professional rubric**, not generic NLP heuristics
* Transparent and explainable scoring
* Professional-grade PDF reporting
* Visual feedback through radar chart
* Designed with clarity, fairness, and educational use-cases in mind

---

## ⚠️ **Known Limitations**

* Assumes fixed 52-second audio duration; actual speaking speed may differ
* Semantic similarity has been intentionally removed per task requirement
* Grammar scoring relies on automated tools which may not catch all context-based errors

---

## 💙 **Acknowledgments**

This project was created as part of the Nirmaan Education AI Internship Case Study
— to demonstrate product thinking, communication assessment design, and practical AI engineering.

---

