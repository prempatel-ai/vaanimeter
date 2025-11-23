"""
Main Streamlit Application for the AI-Powered Spoken Introduction Scoring Tool.
Handles UI rendering, user input, scoring execution, and report generation.
"""

import streamlit as st
from scorer import IntroductionScorer
from utils import create_radar_chart, create_pdf_report

# --- Page Configuration ---
st.set_page_config(
    page_title="VaaniMeter",
    page_icon="🎤",
    layout="wide"
)

# --- Custom CSS ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .score-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .score-value {
        font-size: 3em;
        font-weight: bold;
        color: #2c3e50;
    }
    .score-label {
        font-size: 1.2em;
        color: #7f8c8d;
    }
    .category-header {
        font-size: 1.1em;
        font-weight: bold;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    """Main function to run the Streamlit app."""
    
    st.title("🎤 AI-Powered Spoken Introduction Scoring Tool")
    st.markdown("Evaluate your self-introduction transcript against a strict professional rubric.")

    # --- Sidebar ---
    with st.sidebar:
        st.header("Instructions")
        st.markdown("""
        1. **Paste** your transcript or **Upload** a .txt file.
        2. Click **Score Introduction**.
        3. Review your **Overall Score** and **Detailed Breakdown**.
        """)
        st.info("This tool uses strict rule-based and NLP scoring.")

    # --- Input Section ---
    col1, col2 = st.columns([2, 1])
    
    with col1:
        input_method = st.radio("Input Method", ["Paste Transcript", "Upload .txt File"], horizontal=True)
        
        transcript_text = ""
        
        if input_method == "Paste Transcript":
            transcript_text = st.text_area("Enter Transcript", height=300, placeholder="Good morning, my name is...")
        else:
            uploaded_file = st.file_uploader("Upload Transcript (.txt)", type=["txt"])
            if uploaded_file is not None:
                transcript_text = uploaded_file.read().decode("utf-8")
                st.text_area("Preview", transcript_text, height=200, disabled=True)

    with col2:
        st.markdown("### Scoring Criteria")
        st.markdown("""
        - **Content (40)**: Salutation, Keywords, Flow
        - **Speech Rate (10)**: WPM (Target 111-140)
        - **Language (20)**: Grammar, Vocabulary
        - **Clarity (15)**: Filler Words
        - **Engagement (15)**: Sentiment
        """)
        
        if st.button("Score Introduction"):
            if not transcript_text.strip():
                st.error("Please provide a transcript first.")
            else:
                with st.spinner("Analyzing..."):
                    try:
                        scorer = IntroductionScorer()
                        results = scorer.calculate_final_score(transcript_text)
                        
                        st.session_state['results'] = results
                        st.session_state['transcript'] = transcript_text
                    except Exception as e:
                        st.error(f"An error occurred: {e}")

    # --- Results Section ---
    if 'results' in st.session_state:
        results = st.session_state['results']
        transcript = st.session_state['transcript']
        
        st.markdown("---")
        st.header("📊 Evaluation Results")
        
        # Overall Score
        overall = results['overall_score']
        color = "green" if overall >= 80 else "orange" if overall >= 60 else "red"
        
        col_score, col_radar = st.columns([1, 1])
        
        with col_score:
            st.markdown(f"""
            <div class="score-card" style="border-left: 5px solid {color};">
                <div class="score-label">Overall Score</div>
                <div class="score-value" style="color: {color};">{overall}/100</div>
            </div>
            """, unsafe_allow_html=True)
            
            # PDF Download
            fig, radar_buf = create_radar_chart(results)
            pdf_buf = create_pdf_report(transcript, results, radar_buf)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_buf,
                file_name="VaaniMeter_Report.pdf",
                mime="application/pdf"
            )

        with col_radar:
            st.pyplot(fig)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Score Breakdown Formula
        with st.expander("Score Breakdown Formula (How Your Score Was Calculated)", expanded=False):
            st.markdown("### 1. Content & Structure (Max 40)")
            c = results['content_and_structure']
            st.table({
                "Component": ["Salutation", "Must-Have Keywords", "Good-To-Have Keywords", "Flow", "TOTAL"],
                "Score": [c['salutation_score'], c['keyword_must_have_score'], c['keyword_good_to_have_score'], c['flow_score'], c['total']],
                "Max": [5, 20, 10, 5, 40]
            })
            
            st.markdown("### 2. Speech Rate (Max 10)")
            s = results['speech_rate']
            st.write(f"**Words Per Minute (WPM):** {s['wpm']}")
            st.table({
                "Component": ["Speech Rate Score"],
                "Score": [s['score']],
                "Max": [10]
            })
            
            st.markdown("### 3. Language & Grammar (Max 20)")
            l = results['language_and_grammar']
            st.table({
                "Component": ["Grammar", "Vocabulary (TTR)", "TOTAL"],
                "Score": [l['grammar_score'], l['vocabulary_richness_score'], l['total']],
                "Max": [10, 10, 20]
            })
            
            st.markdown("### 4. Clarity (Max 15)")
            cl = results['clarity']
            st.write(f"**Filler Word Rate:** {cl['filler_word_rate_percent']}%")
            st.table({
                "Component": ["Clarity Score"],
                "Score": [cl['score']],
                "Max": [15]
            })
            
            st.markdown("### 5. Engagement (Max 15)")
            e = results['engagement']
            st.write(f"**Positive Probability:** {e['sentiment_positive_probability']}")
            st.table({
                "Component": ["Engagement Score"],
                "Score": [e['score']],
                "Max": [15]
            })
            
            st.markdown(f"### Final Calculation")
            st.markdown(f"**{c['total']} (Content) + {s['score']} (Speech) + {l['total']} (Language) + {cl['score']} (Clarity) + {e['score']} (Engagement) = {overall}/100**")

        # Detailed Category Analysis
        st.subheader("📝 Detailed Category Analysis")
        
        c1, c2 = st.columns(2)
        
        with c1:
            # Content & Structure
            content = results['content_and_structure']
            with st.expander(f"Content & Structure ({content['total']}/40)", expanded=True):
                st.write(f"**Salutation:** {content['salutation_score']}/5")
                st.write(f"**Must-Have Keywords:** {content['keyword_must_have_score']}/20")
                st.write(f"**Good-To-Have Keywords:** {content['keyword_good_to_have_score']}/10")
                st.write(f"**Flow:** {content['flow_score']}/5")

            # Speech Rate
            speech = results['speech_rate']
            with st.expander(f"Speech Rate ({speech['score']}/10)", expanded=True):
                st.write(f"**WPM:** {speech['wpm']}")
                st.write(f"**Score:** {speech['score']}/10")

        with c2:
            # Language & Grammar
            lang = results['language_and_grammar']
            with st.expander(f"Language & Grammar ({lang['total']}/20)", expanded=True):
                st.write(f"**Grammar Score:** {lang['grammar_score']}/10")
                st.write(f"**Vocabulary Score:** {lang['vocabulary_richness_score']}/10")

            # Clarity
            clarity = results['clarity']
            with st.expander(f"Clarity ({clarity['score']}/15)", expanded=True):
                st.write(f"**Filler Count:** {clarity['filler_word_count']}")
                st.write(f"**Filler Rate:** {clarity['filler_word_rate_percent']}%")
                st.write(f"**Score:** {clarity['score']}/15")

            # Engagement
            eng = results['engagement']
            with st.expander(f"Engagement ({eng['score']}/15)", expanded=True):
                st.write(f"**Positive Probability:** {eng['sentiment_positive_probability']}")
                st.write(f"**Score:** {eng['score']}/15")

        # JSON Output
        st.subheader("💻 JSON Output")
        st.json(results)

if __name__ == "__main__":
    main()
