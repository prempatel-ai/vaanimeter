"""
Scoring engine for the AI-Powered Spoken Introduction Scoring Tool.
Implements strict rubric logic for Content, Speech Rate, Language, Clarity, and Engagement.
"""

from utils import load_language_tool, download_nltk_data, load_vader_analyzer

# Ensure NLTK data is available
download_nltk_data()

class IntroductionScorer:
    """
    Evaluates a self-introduction transcript based on a predefined rubric.
    """
    def __init__(self):
        self.grammar_tool = load_language_tool()
        self.vader_analyzer = load_vader_analyzer()

    def evaluate_content_structure(self, text):
        """
        Evaluates Content & Structure (Max 40 points).
        
        Criteria:
        - Salutation (0-5)
        - Must-Have Keywords (0-20)
        - Good-To-Have Keywords (0-10)
        - Flow (0-5)
        """
        lower_text = text.lower()
        
        # 1.1 Salutation
        salutation_score = 0
        strong_salutations = [
            "i am excited to introduce myself", 
            "i'm very happy to introduce myself", 
            "i am very happy to introduce myself"
        ]
        good_salutations = [
            "good morning", "good afternoon", "good evening", 
            "good day", "hello everyone"
        ]
        basic_salutations = ["hi", "hello"]
        
        if any(x in lower_text for x in strong_salutations):
            salutation_score = 5
        elif any(x in lower_text for x in good_salutations):
            salutation_score = 4
        elif any(x in lower_text for x in basic_salutations):
            salutation_score = 2
        else:
            salutation_score = 0

        # 1.2 Must-Have Keywords (4 points each, max 20)
        must_haves = {
            "Name": ["name is", "i am", "my name"],
            "Age": ["years old", "age is", "i am 1", "i am 2", "i am 3", "i am 4", "i am 5", "i am 6", "i am 7", "i am 8", "i am 9"],
            "School/Class": ["study in", "class", "grade", "school", "student at"],
            "Family": ["family", "parents", "brother", "sister", "mother", "father", "live with"],
            "Hobbies": ["hobby", "hobbies", "like to", "enjoy", "love to", "playing", "reading"]
        }
        
        must_have_score = 0
        for _, patterns in must_haves.items():
            if any(p in lower_text for p in patterns):
                must_have_score += 4
        must_have_score = min(20, must_have_score)

        # 1.3 Good-To-Have Keywords (2 points each, max 10)
        good_to_haves = {
            "Family Details": ["father is", "mother is", "sister is", "brother is", "parents are"],
            "Origin": ["i am from", "parents are from", "born in", "native"],
            "Ambition": ["want to become", "goal", "future", "aim to", "dream"],
            "Unique": ["interesting", "unique", "fact about me", "special"],
            "Strengths": ["strength", "good at", "achievement", "proud of"]
        }
        
        good_to_have_score = 0
        for _, patterns in good_to_haves.items():
            if any(p in lower_text for p in patterns):
                good_to_have_score += 2
        good_to_have_score = min(10, good_to_have_score)

        # 1.4 Flow (0-5)
        # Heuristic: Check relative positions of key sections
        indices = {}
        for k, patterns in must_haves.items():
            indices[k] = -1
            for p in patterns:
                idx = lower_text.find(p)
                if idx != -1:
                    indices[k] = idx
                    break
        
        salutation_idx = -1
        for s in good_salutations + basic_salutations:
            idx = lower_text.find(s)
            if idx != -1:
                salutation_idx = idx
                break
                
        closing_idx = -1
        for c in ["thank you", "thanks", "that's all"]:
            idx = lower_text.find(c)
            if idx != -1:
                closing_idx = idx
                break
        
        flow_score = 5
        
        # Penalize if Name appears before Salutation
        if salutation_idx != -1 and indices["Name"] != -1 and indices["Name"] < salutation_idx:
            flow_score -= 2
        
        # Penalize if Closing appears before Name
        if closing_idx != -1 and indices["Name"] != -1 and closing_idx < indices["Name"]:
            flow_score -= 3
            
        # Penalize if Hobbies appear before Name
        if indices["Hobbies"] != -1 and indices["Name"] != -1 and indices["Hobbies"] < indices["Name"]:
            flow_score -= 1
            
        flow_score = max(0, flow_score)

        total = salutation_score + must_have_score + good_to_have_score + flow_score
        
        return {
            "salutation_score": salutation_score,
            "keyword_must_have_score": must_have_score,
            "keyword_good_to_have_score": good_to_have_score,
            "flow_score": flow_score,
            "total": total
        }

    def evaluate_speech_rate(self, text):
        """
        Evaluates Speech Rate (Max 10 points).
        Assumes a fixed duration of 52 seconds.
        """
        words = text.split()
        word_count = len(words)
        duration_min = 52 / 60
        wpm = word_count / duration_min if duration_min > 0 else 0
        
        if wpm > 161:
            score = 2
        elif 141 <= wpm <= 160:
            score = 6
        elif 111 <= wpm <= 140:
            score = 10
        elif 81 <= wpm <= 110:
            score = 6
        else: # < 80
            score = 2
            
        return {
            "wpm": int(wpm),
            "score": score
        }

    def evaluate_language_grammar(self, text):
        """
        Evaluates Language & Grammar (Max 20 points).
        Criteria:
        - Grammar Error Ratio (0-10)
        - Vocabulary Richness / TTR (0-10)
        """
        words = text.split()
        word_count = len(words)
        if word_count == 0:
            return {"grammar_score": 0, "vocabulary_richness_score": 0, "total": 0}

        # 3.1 Grammar
        errors = 0
        if self.grammar_tool:
            matches = self.grammar_tool.check(text)
            errors = len(matches)
        
        errors_per_100 = (errors / word_count) * 100
        g_ratio = 1 - min(errors_per_100 / 10, 1)
        
        if g_ratio >= 0.9:
            grammar_score = 10
        elif 0.7 <= g_ratio < 0.9:
            grammar_score = 8
        elif 0.5 <= g_ratio < 0.7:
            grammar_score = 6
        elif 0.3 <= g_ratio < 0.5:
            grammar_score = 4
        else:
            grammar_score = 2
            
        # 3.2 Vocabulary (Type-Token Ratio)
        tokens = [w.lower() for w in words]
        unique_tokens = set(tokens)
        ttr = len(unique_tokens) / len(tokens) if len(tokens) > 0 else 0
        
        if ttr >= 0.9:
            vocab_score = 10
        elif 0.7 <= ttr < 0.9:
            vocab_score = 8
        elif 0.5 <= ttr < 0.7:
            vocab_score = 6
        elif 0.3 <= ttr < 0.5:
            vocab_score = 4
        else:
            vocab_score = 2
            
        return {
            "grammar_score": grammar_score,
            "vocabulary_richness_score": vocab_score,
            "total": grammar_score + vocab_score
        }

    def evaluate_clarity(self, text):
        """
        Evaluates Clarity (Max 15 points).
        Based on filler word percentage.
        """
        fillers = [
            "um", "uh", "like", "you know", "so", "actually", 
            "basically", "right", "i mean", "well", "kinda", 
            "sort of", "okay", "hmm", "ah"
        ]
        lower_text = text.lower()
        words = lower_text.split()
        word_count = len(words)
        
        if word_count == 0:
            return {"filler_word_count": 0, "filler_word_rate_percent": 0, "score": 15}

        filler_count = 0
        # Check single word fillers
        for w in words:
            if w in fillers:
                filler_count += 1
        
        # Check multi-word fillers
        multi_word_fillers = [f for f in fillers if " " in f]
        for f in multi_word_fillers:
            filler_count += lower_text.count(f)
            
        rate_percent = (filler_count / word_count) * 100
        
        if rate_percent <= 3:
            score = 15
        elif 4 <= rate_percent <= 6:
            score = 12
        elif 7 <= rate_percent <= 9:
            score = 9
        elif 10 <= rate_percent <= 12:
            score = 6
        else:
            score = 3
            
        return {
            "filler_word_count": filler_count,
            "filler_word_rate_percent": round(rate_percent, 2),
            "score": score
        }

    def evaluate_engagement(self, text):
        """
        Evaluates Engagement (Max 15 points).
        Based on VADER sentiment positive probability.
        """
        if not text.strip():
            return {"sentiment_positive_probability": 0, "score": 3}
            
        scores = self.vader_analyzer.polarity_scores(text)
        
        # Map compound score to a 0-1 probability-like scale
        p_pos = (scores['compound'] + 1) / 2
        
        if p_pos >= 0.9:
            score = 15
        elif 0.7 <= p_pos < 0.9:
            score = 12
        elif 0.5 <= p_pos < 0.7:
            score = 9
        elif 0.3 <= p_pos < 0.5:
            score = 6
        else:
            score = 3
            
        return {
            "sentiment_positive_probability": round(p_pos, 2),
            "score": score
        }

    def calculate_final_score(self, text):
        """
        Aggregates scores from all categories.
        Returns a detailed dictionary with scores and breakdowns.
        """
        if not text or not text.strip():
            return {
                "overall_score": 0,
                "content_and_structure": {"salutation_score": 0, "keyword_must_have_score": 0, "keyword_good_to_have_score": 0, "flow_score": 0, "total": 0},
                "speech_rate": {"wpm": 0, "score": 0},
                "language_and_grammar": {"grammar_score": 0, "vocabulary_richness_score": 0, "total": 0},
                "clarity": {"filler_word_count": 0, "filler_word_rate_percent": 0, "score": 0},
                "engagement": {"sentiment_positive_probability": 0, "score": 0}
            }

        content = self.evaluate_content_structure(text)
        speech = self.evaluate_speech_rate(text)
        language = self.evaluate_language_grammar(text)
        clarity = self.evaluate_clarity(text)
        engagement = self.evaluate_engagement(text)
        
        overall = (
            content['total'] +
            speech['score'] +
            language['total'] +
            clarity['score'] +
            engagement['score']
        )
        
        overall = max(0, min(100, overall))
        
        return {
            "overall_score": overall,
            "content_and_structure": content,
            "speech_rate": speech,
            "language_and_grammar": language,
            "clarity": clarity,
            "engagement": engagement
        }
