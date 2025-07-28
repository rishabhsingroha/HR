from typing import Dict, List, Optional

class DecisionEngine:
    def __init__(self):
        """Initialize decision engine with evaluation criteria"""
        self.skill_keywords = {
            'technical': [
                'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node',
                'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'ml', 'ai'
            ],
            'soft_skills': [
                'leadership', 'communication', 'teamwork', 'problem-solving',
                'analytical', 'project management', 'agile', 'scrum'
            ]
        }
        
        self.red_flags = [
            'Negative language detected',
            'Very short response',
            'Vague response'
        ]

    async def evaluate(self, analysis: Dict) -> Dict:
        """Evaluate candidate based on NLP analysis results"""
        try:
            # Extract relevant information
            sentiment = analysis.get('sentiment', '')
            keywords = analysis.get('keywords', [])
            tone_flags = analysis.get('tone_flags', [])
            extracted_info = analysis.get('extracted_info', {})

            # Evaluate different aspects
            skill_score = self._evaluate_skills(keywords)
            tone_score = self._evaluate_tone(sentiment, tone_flags)
            experience_score = self._evaluate_experience(extracted_info.get('experience', ''))

            # Make decision
            decision, reason = self._make_decision(
                skill_score, tone_score, experience_score, tone_flags
            )

            return {
                'candidate_name': extracted_info.get('name', 'Unknown'),
                'skills': self._format_skills(keywords),
                'experience': extracted_info.get('experience', 'Not specified'),
                'location': extracted_info.get('location', 'Not specified'),
                'sentiment': sentiment,
                'decision': decision,
                'reason': reason
            }

        except Exception as e:
            return self._generate_error_response(str(e))

    def _evaluate_skills(self, keywords: List[str]) -> float:
        """Evaluate candidate's skills based on keywords"""
        if not keywords:
            return 0.0

        # Convert keywords to lowercase for matching
        keywords_lower = [k.lower() for k in keywords]
        
        # Count matches in both technical and soft skills
        technical_matches = sum(1 for skill in self.skill_keywords['technical'] 
                              if skill in keywords_lower)
        soft_skill_matches = sum(1 for skill in self.skill_keywords['soft_skills'] 
                                if skill in keywords_lower)
        
        # Calculate weighted score (technical skills weighted more)
        total_score = (technical_matches * 0.7 + soft_skill_matches * 0.3)
        max_possible = 5  # Normalize to a 0-1 scale
        
        return min(total_score / max_possible, 1.0)

    def _evaluate_tone(self, sentiment: str, tone_flags: List[str]) -> float:
        """Evaluate candidate's tone based on sentiment and flags"""
        # Base score from sentiment
        sentiment_scores = {
            'Very Positive': 1.0,
            'Positive': 0.8,
            'Neutral': 0.6,
            'Negative': 0.3,
            'Very Negative': 0.0
        }
        
        base_score = sentiment_scores.get(sentiment, 0.6)
        
        # Reduce score for each tone flag
        penalty_per_flag = 0.2
        total_penalty = len(tone_flags) * penalty_per_flag
        
        return max(base_score - total_penalty, 0.0)

    def _evaluate_experience(self, experience: str) -> float:
        """Evaluate candidate's experience"""
        if not experience:
            return 0.0

        try:
            # Extract years from experience string
            years = float(experience.split()[0])
            
            # Score based on years of experience (0-5 years scale)
            score = min(years / 5.0, 1.0)
            return score
            
        except (ValueError, IndexError):
            return 0.0

    def _make_decision(self, 
                      skill_score: float, 
                      tone_score: float, 
                      experience_score: float,
                      tone_flags: List[str]) -> tuple:
        """Make final decision based on all scores"""
        # Calculate weighted total score
        total_score = (
            skill_score * 0.4 +      # Skills are most important
            tone_score * 0.3 +        # Tone is second most important
            experience_score * 0.3    # Experience is equally important as tone
        )

        # Decision thresholds
        if total_score >= 0.8:
            decision = "Recommend"
            reason = "Strong candidate with good skills and positive interaction"
        elif total_score >= 0.6:
            decision = "Consider"
            reason = "Potential candidate but some areas need discussion"
        elif total_score >= 0.4:
            if tone_flags:
                decision = "Escalate"
                reason = f"Review needed due to: {', '.join(tone_flags)}"
            else:
                decision = "Consider with Reservations"
                reason = "Below average performance in key areas"
        else:
            decision = "Do Not Recommend"
            reason = "Does not meet minimum requirements"

        return decision, reason

    def _format_skills(self, keywords: List[str]) -> List[str]:
        """Format and filter relevant skills from keywords"""
        # Combine all skill keywords
        all_skills = set(self.skill_keywords['technical'] + 
                        self.skill_keywords['soft_skills'])
        
        # Filter and format relevant skills
        relevant_skills = [
            keyword.title() 
            for keyword in keywords 
            if keyword.lower() in all_skills
        ]
        
        return relevant_skills[:5]  # Return top 5 relevant skills

    def _generate_error_response(self, error_message: str) -> Dict:
        """Generate error response when evaluation fails"""
        return {
            'candidate_name': 'Error',
            'skills': [],
            'experience': 'N/A',
            'location': 'N/A',
            'sentiment': 'N/A',
            'decision': 'Error',
            'reason': f'Evaluation failed: {error_message}'
        }