"""
Utility functions for the AI-Powered Spoken Introduction Scoring Tool.
Handles model loading, data downloading, radar chart generation, and PDF report creation.
"""

import streamlit as st
import nltk
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

# --- Model Loading & Setup ---

def download_nltk_data():
    """Downloads necessary NLTK data for tokenization, tagging, and sentiment analysis."""
    resources = [
        ('tokenizers/punkt', 'punkt'),
        ('tokenizers/punkt_tab', 'punkt_tab'),
        ('corpora/brown', 'brown'),
        ('taggers/averaged_perceptron_tagger', 'averaged_perceptron_tagger'),
        ('sentiment/vader_lexicon.zip', 'vader_lexicon')
    ]
    
    for path, name in resources:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(name)

@st.cache_resource
def load_language_tool():
    """
    Loads the LanguageTool object for grammar checking.
    Returns None if Java is not installed or loading fails.
    """
    import language_tool_python
    try:
        tool = language_tool_python.LanguageTool('en-US')
        return tool
    except Exception as e:
        print(f"Warning: LanguageTool failed to load: {e}")
        return None

@st.cache_resource
def load_vader_analyzer():
    """Loads the VADER SentimentIntensityAnalyzer."""
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    return SentimentIntensityAnalyzer()

# --- Visualization & Reporting ---

def create_radar_chart(results):
    """
    Generates a radar chart for the 5 categories.
    Normalizes scores to a 0-10 scale for visualization.
    
    Args:
        results (dict): The scoring results dictionary.
        
    Returns:
        tuple: (matplotlib.figure.Figure, BytesIO buffer)
    """
    # Extract scores and normalize to 0-10
    # Content (40) -> /4
    # Speech (10) -> /1
    # Language (20) -> /2
    # Clarity (15) -> /1.5
    # Engagement (15) -> /1.5
    
    categories = ['Content', 'Speech Rate', 'Language', 'Clarity', 'Engagement']
    
    content_score = results['content_and_structure']['total'] / 4
    speech_score = results['speech_rate']['score']
    lang_score = results['language_and_grammar']['total'] / 2
    clarity_score = results['clarity']['score'] / 1.5
    eng_score = results['engagement']['score'] / 1.5
    
    values = [content_score, speech_score, lang_score, clarity_score, eng_score]
    
    # Close the loop for the radar chart
    values += [values[0]]
    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
    angles += [angles[0]]
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    
    # Draw the plot
    ax.plot(angles, values, color='#4CAF50', linewidth=2, linestyle='solid')
    ax.fill(angles, values, color='#4CAF50', alpha=0.25)
    
    # Fix axis to 0-10 range
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(['2', '4', '6', '8', '10'], color="grey", size=8)
    
    # Set category labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    
    # Save to buffer for PDF usage
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    buf.seek(0)
    
    return fig, buf

def create_pdf_report(transcript, results, radar_buf):
    """
    Generates a PDF report using ReportLab.
    
    Args:
        transcript (str): The input transcript text.
        results (dict): The scoring results dictionary.
        radar_buf (BytesIO): Buffer containing the radar chart image.
        
    Returns:
        BytesIO: Buffer containing the generated PDF.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = styles['Title']
    story.append(Paragraph("AI Spoken Introduction Evaluation Report", title_style))
    story.append(Spacer(1, 12))
    
    # Timestamp
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    story.append(Paragraph(f"Date: {date_str}", styles['Normal']))
    story.append(Spacer(1, 12))

    # Overall Score
    overall = results['overall_score']
    score_style = ParagraphStyle('Score', parent=styles['Heading2'], textColor=colors.darkblue)
    story.append(Paragraph(f"Overall Score: {overall}/100", score_style))
    story.append(Spacer(1, 12))

    # Radar Chart
    if radar_buf:
        img = Image(radar_buf, width=4*inch, height=4*inch)
        story.append(img)
        story.append(Spacer(1, 12))

    # Category Scores Table
    data = [
        ["Category", "Score", "Max"],
        ["Content & Structure", f"{results['content_and_structure']['total']:.1f}", "40"],
        ["Speech Rate", f"{results['speech_rate']['score']}", "10"],
        ["Language & Grammar", f"{results['language_and_grammar']['total']}", "20"],
        ["Clarity", f"{results['clarity']['score']}", "15"],
        ["Engagement", f"{results['engagement']['score']}", "15"]
    ]
    
    t = Table(data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(t)
    story.append(Spacer(1, 24))

    # Transcript Section
    story.append(Paragraph("Transcript:", styles['Heading3']))
    story.append(Paragraph(transcript, styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Summary & Feedback Section
    story.append(Paragraph("Summary & Feedback:", styles['Heading3']))
    
    # Construct dynamic feedback
    feedback = []
    if results['content_and_structure']['total'] < 20:
        feedback.append("Content needs improvement. Ensure you include all key details like name, age, family, and hobbies.")
    else:
        feedback.append("Good content coverage.")
        
    if results['speech_rate']['score'] < 6:
        feedback.append("Watch your speaking pace. Aim for ~130 words per minute.")
        
    if results['clarity']['score'] < 10:
        feedback.append("Try to reduce filler words (um, uh, like) to sound more confident.")
        
    if results['engagement']['score'] < 10:
        feedback.append("Try to sound more enthusiastic and positive.")
        
    for item in feedback:
        story.append(Paragraph(f"- {item}", styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    return buffer
