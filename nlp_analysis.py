from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from keyphrase_vectorizers import KeyphraseCountVectorizer
from typing import Dict, List, Tuple
import spacy
import re

class NLPAnalyzer:
    def __init__(self):
        """Initialize NLP components"""
        try:
            # Load sentiment analysis pipeline
            self.sentiment_pipeline = pipeline("sentiment-analysis")
            # Load VADER for additional sentiment analysis
            self.vader = SentimentIntensityAnalyzer()
            # Initialize keyword extractor
            self.keyword_extractor = KeyphraseCountVectorizer()
            # Load spaCy model for named entity recognition
            self.nlp = spacy.load("en_core_web_sm")
        except Exception as e:
            print(f"Warning: Could not initialize some NLP components: {e}")

    async def analyze(self, text: str) -> Dict:
        """Perform comprehensive NLP analysis on text"""
        try:
            sentiment = await self._analyze_sentiment(text)
            keywords = await self._extract_keywords(text)
            entities = await self._extract_entities(text)
            tone_flags = await self._check_tone(text)

            return {
                "sentiment": sentiment,
                "keywords": keywords,
                "entities": entities,
                "tone_flags": tone_flags,
                "extracted_info": self._extract_candidate_info(text)
            }

        except Exception as e:
            return {"error": str(e)}

    async def _analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment using both transformers and VADER"""
        try:
            # Get transformer-based sentiment
            transformer_sentiment = self.sentiment_pipeline(text)[0]
            
            # Get VADER sentiment
            vader_scores = self.vader.polarity_scores(text)
            
            # Combine both analyses
            compound_score = vader_scores['compound']
            
            if compound_score >= 0.5:
                return "Very Positive"
            elif compound_score > 0:
                return "Positive"
            elif compound_score == 0:
                return "Neutral"
            elif compound_score > -0.5:
                return "Negative"
            else:
                return "Very Negative"

        except Exception:
            # Fallback to basic sentiment analysis
            return self._basic_sentiment_analysis(text)

    async def _extract_keywords(self, text: str) -> List[str]:
        """Extract key phrases and important terms"""
        try:
            # Extract keyphrases
            keyphrases = self.keyword_extractor.fit([text]).get_feature_names_out()
            
            # Filter and clean keyphrases
            cleaned_keyphrases = [
                phrase.strip() for phrase in keyphrases
                if len(phrase.strip()) > 2  # Remove very short phrases
            ]
            
            return cleaned_keyphrases[:10]  # Return top 10 keyphrases

        except Exception:
            return self._basic_keyword_extraction(text)

    async def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities using spaCy"""
        try:
            doc = self.nlp(text)
            entities = {}
            
            for ent in doc.ents:
                if ent.label_ not in entities:
                    entities[ent.label_] = []
                entities[ent.label_].append(ent.text)

            return entities

        except Exception:
            return {}

    async def _check_tone(self, text: str) -> List[str]:
        """Check for potential tone issues or red flags"""
        flags = []
        
        # Check for negative patterns
        negative_patterns = [
            r'\b(never|no|not|cannot|won\'t)\b',
            r'\b(hate|dislike|awful|terrible)\b',
            r'\b(impossible|difficult|hard|problem)\b'
        ]

        for pattern in negative_patterns:
            if re.search(pattern, text.lower()):
                flags.append("Negative language detected")
                break

        # Check for vague responses
        vague_words = ['maybe', 'somewhat', 'kind of', 'sort of', 'i guess']
        if any(word in text.lower() for word in vague_words):
            flags.append("Vague response")

        # Check response length
        if len(text.split()) < 5:
            flags.append("Very short response")

        return flags

    def _extract_candidate_info(self, text: str) -> Dict:
        """Extract specific candidate information"""
        info = {
            "name": None,
            "experience": None,
            "location": None,
            "skills": []
        }

        try:
            doc = self.nlp(text)

            # Extract name (first PERSON entity)
            for ent in doc.ents:
                if ent.label_ == "PERSON" and not info["name"]:
                    info["name"] = ent.text
                elif ent.label_ == "GPE" and not info["location"]:
                    info["location"] = ent.text

            # Extract experience (looking for patterns like "X years")
            experience_pattern = r'\b(\d+)\s*(?:years?|yrs?)\b'
            experience_match = re.search(experience_pattern, text)
            if experience_match:
                info["experience"] = f"{experience_match.group(1)} years"

            # Extract skills (using keyword extraction)
            skills = self._basic_keyword_extraction(text)
            info["skills"] = skills[:5]  # Top 5 skills

            return info

        except Exception:
            return info

    def _basic_sentiment_analysis(self, text: str) -> str:
        """Basic sentiment analysis fallback"""
        positive_words = set(['good', 'great', 'excellent', 'happy', 'interested', 'positive'])
        negative_words = set(['bad', 'poor', 'terrible', 'unhappy', 'negative', 'not'])
        
        words = text.lower().split()
        pos_count = sum(1 for word in words if word in positive_words)
        neg_count = sum(1 for word in words if word in negative_words)
        
        if pos_count > neg_count:
            return "Positive"
        elif neg_count > pos_count:
            return "Negative"
        return "Neutral"

    def _basic_keyword_extraction(self, text: str) -> List[str]:
        """Basic keyword extraction fallback"""
        # Remove common stop words and punctuation
        stop_words = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 
                         'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself'])
        
        words = text.lower().split()
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Return unique keywords
        return list(set(keywords))[:10]