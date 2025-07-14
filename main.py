from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import uvicorn

# Import custom modules
from call_handler import CallHandler
from speech_to_text import SpeechToText
from text_to_speech import TextToSpeech
from nlp_analysis import NLPAnalyzer
from decision_engine import DecisionEngine

app = FastAPI(title="Voice AI HR Agent")

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
    return {"status": "Voice AI HR Agent is running"}

@app.post("/initiate-call")
async def initiate_call(phone_number: str) -> Dict:
    try:
        call_handler = CallHandler()
        call_status = await call_handler.start_call(phone_number)
        return {"status": "success", "call_id": call_status.call_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-response")
async def process_response(audio_url: str) -> CandidateResponse:
    try:
        # Initialize components
        stt = SpeechToText()
        nlp = NLPAnalyzer()
        decision = DecisionEngine()

        # Process the response
        transcript = await stt.transcribe(audio_url)
        analysis = await nlp.analyze(transcript)
        final_decision = await decision.evaluate(analysis)

        return CandidateResponse(**final_decision)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)