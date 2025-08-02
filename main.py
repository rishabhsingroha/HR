from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import uvicorn

# Import mock services instead of real ones
from mock_services import (
    MockTwilioService,
    MockTTSService,
    MockSTTService,
    MockNLPService
)

app = FastAPI(title="Voice AI HR Agent (Local Mock Version)")

# Initialize mock services
twilio_service = MockTwilioService()
tts_service = MockTTSService()
stt_service = MockSTTService()
nlp_service = MockNLPService()

class CandidateResponse(BaseModel):
    candidate_name: str
    skills: List[str]
    experience: str
    location: str
    sentiment: str
    decision: str
    reason: Optional[str]

@app.get("/")
async def root():
    return {"status": "Voice AI HR Agent Mock Service is running"}

@app.post("/initiate-call")
async def initiate_call(phone_number: str) -> Dict:
    try:
        # Use mock Twilio service
        call_status = await twilio_service.make_call(phone_number)
        return {"status": "success", "call_id": call_status["call_id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/simulate-interview")
async def simulate_interview() -> List[Dict]:
    """Endpoint to simulate entire interview process"""
    try:
        interview_results = []
        
        # Simulate responses for each question
        for i in range(5):  # 5 standard questions
            # Get mock response
            response = twilio_service.get_response(i)
            
            # Analyze response
            sentiment = nlp_service.analyze_sentiment(response)
            keywords = nlp_service.extract_keywords(response)
            
            result = {
                "question_index": i,
                "response": response,
                "analysis": {
                    "sentiment": sentiment,
                    "keywords": keywords
                }
            }
            interview_results.append(result)
        
        return interview_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-response")
async def process_response(audio_data: bytes = b'') -> CandidateResponse:
    try:
        # Use mock services for processing
        transcript = await stt_service.transcribe(audio_data)
        sentiment = nlp_service.analyze_sentiment(transcript["text"])
        keywords = nlp_service.extract_keywords(transcript["text"])
        
        # Mock decision logic
        decision = "Recommend" if sentiment == "Positive" else "Consider"
        
        return CandidateResponse(
            candidate_name="Mock Candidate",
            skills=keywords,
            experience="5 years",  # Mock data
            location="San Francisco",  # Mock data
            sentiment=sentiment,
            decision=decision,
            reason="Mock evaluation based on sentiment analysis"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "mode": "mock"}

if __name__ == "__main__":
    print("Starting Voice AI HR Agent in Mock Mode...")
    print("No external services or API keys required")
    print("Access the API documentation at http://localhost:8000/docs")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)