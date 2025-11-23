Here is your updated, polished **README.md** with the GitHub clone instruction added at the perfect place and written professionally to impress reviewers.

I’ve placed the cloning section *right before* the local setup instructions — the best UX for developers.

---

# 🌟 **VaaniMeter**

### *AI-Powered Spoken Introduction Evaluation Tool*

---

## 📌 **Overview**

**VaaniMeter** is an AI-powered evaluation tool designed to score spoken self-introductions using a **strict, deterministic rubric**.
It provides instant feedback, transparent scoring, radar-chart visualization, and a downloadable professional PDF report.

The tool brings structure, clarity, and objectivity to communication assessment—making it ideal for academic evaluation, skill-building, and learning environments.

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

Shows **exactly how each score was calculated**, including:

* Keyword detection
* Grammar analysis
* Filler percentages
* Sentiment score
* WPM category mapping
* Flow structure quality

### 🔹 Radar Chart Visualization

A spider chart provides a visual overview of strengths and weaknesses.

### 🔹 PDF Report Generation

Download a clean, professional report containing:

* Input transcript
* Rubric category scores
* Radar chart
* Strengths & improvement insights
* Final summary

### 🔹 JSON Output (Optional)

Raw structured data for developers or advanced reviewers.

---

## 📁 **Project Structure**

| File               | Description                                                                    |
| ------------------ | ------------------------------------------------------------------------------ |
| `app.py`           | Streamlit UI: input handling, score display, chart visualizations, PDF export. |
| `scorer.py`        | Core scoring engine implementing strict rubric logic.                          |
| `utils.py`         | NLP utilities, radar chart functions, and PDF report generation tools.         |
| `requirements.txt` | Dependency list.                                                               |

---

## 🧠 **How the Scoring Engine Works**

### **1. Content & Structure (40 pts)**

Checks:

* Salutation quality
* Must-have keywords (*Name, Age, Class/School, Family, Hobbies*)
* Good-to-have details (fun fact, goal, strengths, achievements, etc.)
* Flow and logical order

### **2. Speech Rate (10 pts)**

Uses a fixed **52-second** duration assumption:

```
wpm = total_words / (52/60)
```

Ideal WPM: **111–140**

### **3. Language (20 pts)**

* Grammar: via **LanguageTool**
* Vocabulary: via **Type-Token Ratio (TTR)**

### **4. Clarity (15 pts)**

Detects filler words:
`"um", "uh", "like", "you know", "hmm", "kinda", "sort of"`
Scoring based on filler percentage.

### **5. Engagement (15 pts)**

Uses **VADER sentiment analysis** for positivity.

---

## 🔄 **End-to-End Data Flow**

1. **User Input** (textarea or txt file)
2. **Processing** → `app.py` sends transcript to `calculate_final_score()`
3. **Analysis** → `scorer.py` performs all NLP + scoring steps
4. **Visualization** → `utils.create_radar_chart()`
5. **PDF Report** → `utils.create_pdf_report()`
6. **Output** → scores, breakdowns, chart, and report in Streamlit

---

# 📥 **Clone This Repository**

To get started, first clone the project:

```
git clone https://github.com/prempatel-ai/vaanimeter.git
```

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

Currently not deployed.
Fully compatible with:

* Streamlit Cloud
* HuggingFace Spaces
* Render
* Railway

---

## 🧪 **Testing**

Evaluated using three categories of transcripts:

* High-quality → **>80**
* Average → **50–70**
* Poor → **<40**

The scoring strongly matches rubric expectations.

---

## ✨ **What Makes VaaniMeter Unique**

* Applies a **clear, strict rubric**, not vague NLP scoring
* Transparent and explainable output
* Professional PDF reporting
* Modern visual radar analysis
* Built for fairness and educational use

---

## ⚠️ **Known Limitations**

* Uses fixed 52s duration for WPM → may differ from real audio
* Semantic similarity intentionally removed as per task requirement
* Grammar detection may miss deep contextual issues

---

## 💙 **Acknowledgments**

Created as part of the **Nirmaan Education AI Internship Case Study**
to demonstrate product thinking, communication analysis design, and practical AI engineering through a clean, transparent scoring tool.

---

