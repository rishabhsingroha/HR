from typing import Dict, Optional, List
import json
import random

class MockTwilioService:
    def __init__(self):
        self.call_id = 0
        self.mock_responses = [
            "Hi, I'm John Smith. I have 5 years of experience in software development.",
            "My key skills are Python, React, and Cloud technologies.",
            "I have 5 years of experience.",
            "I'm based in New York.",
            "Yes, I can join within 2 weeks."
        ]

    async def make_call(self, phone_number: str) -> Dict:
        """Simulate making a phone call"""
        self.call_id += 1
        return {
            "call_id": f"mock_call_{self.call_id}",
            "status": "completed"
        }

    def get_response(self, question_index: int) -> str:
        """Get mock response for a question"""
        if 0 <= question_index < len(self.mock_responses):
            return self.mock_responses[question_index]
        return "I understand."

class MockTTSService:
    async def synthesize(self, text: str) -> bytes:
        """Mock text-to-speech conversion"""
        return b'mock_audio_data'

class MockSTTService:
    async def transcribe(self, audio: bytes) -> Dict[str, str]:
        """Mock speech-to-text conversion"""
        mock_responses = [
            "I have extensive experience in software development",
            "My skills include Python programming and web development",
            "I have been working in this field for 5 years",
            "I am currently located in San Francisco",
            "Yes, I am available to start immediately"
        ]
        return {
            "text": random.choice(mock_responses),
            "language": "en"
        }

class MockNLPService:
    def analyze_sentiment(self, text: str) -> str:
        """Mock sentiment analysis"""
        positive_words = ['good', 'great', 'excellent', 'yes', 'experience', 'skills']
        negative_words = ['no', 'not', 'never', 'bad']
        
        words = text.lower().split()
        pos_count = sum(1 for word in words if word in positive_words)
        neg_count = sum(1 for word in words if word in negative_words)
        
        if pos_count > neg_count:
            return "Positive"
        elif neg_count > pos_count:
            return "Negative"
        return "Neutral"

    def extract_keywords(self, text: str) -> List[str]:
        """Mock keyword extraction"""
        tech_skills = ['python', 'javascript', 'react', 'java', 'cloud', 'aws']
        soft_skills = ['communication', 'leadership', 'teamwork']
        
        words = text.lower().split()
        keywords = []
        
        for word in words:
            if word in tech_skills or word in soft_skills:
                keywords.append(word.title())
        
        return list(set(keywords))