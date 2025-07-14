# Voice AI HR Agent

An automated voice-based AI system for conducting initial candidate screening interviews. The system uses natural language processing and speech recognition to evaluate candidates' responses and provide structured feedback.

## Features

- **Automated Phone Interviews**: Conducts phone interviews using AI-generated voice
- **Real-time Transcription**: Converts candidate responses to text using OpenAI Whisper
- **Sentiment Analysis**: Evaluates candidate's tone and sentiment
- **Keyword Extraction**: Identifies key skills and qualifications
- **Decision Engine**: Provides structured recommendations based on responses

## Technology Stack

- **Backend Framework**: FastAPI
- **Voice Calls**: Twilio
- **Speech-to-Text**: OpenAI Whisper
- **Text-to-Speech**: Google Cloud TTS
- **NLP**: HuggingFace Transformers, spaCy
- **Sentiment Analysis**: VADER

## Prerequisites

1. Python 3.8 or higher
2. Twilio Account (for voice calls)
3. Google Cloud Account (for Text-to-Speech)
4. OpenAI API key (for Whisper, optional if using local model)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd voice-ai-hr-agent
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install spaCy English model:
```bash
python -m spacy download en_core_web_sm
```

## Configuration

1. Create a `.env` file in the project root with the following variables:
```env
# Twilio Configuration
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number

# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT_ID=your_project_id
GOOGLE_APPLICATION_CREDENTIALS=path_to_credentials.json

# Application Configuration
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=True
BASE_URL=http://localhost:8000
```

## Running the Application

1. Start the FastAPI server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /`: Health check endpoint
- `POST /initiate-call`: Start a new interview call
- `POST /process-response`: Process candidate's audio response
- `GET /health`: Application health check

## Usage Example

1. Initiate a call:
```python
import requests

response = requests.post(
    'http://localhost:8000/initiate-call',
    json={'phone_number': '+1234567890'}
)
print(response.json())
```

2. The system will:
   - Call the candidate
   - Ask screening questions
   - Process responses in real-time
   - Generate a structured evaluation

## Sample Output

```json
{
  "candidate_name": "John Doe",
  "skills": ["Python", "React", "AWS"],
  "experience": "5 years",
  "location": "New York",
  "sentiment": "Positive",
  "decision": "Recommend",
  "reason": "Strong candidate with good skills and positive interaction"
}
```

## Testing

The system includes mock functions for testing without external API dependencies:

```python
# Mock a call without Twilio
call_handler = CallHandler()
result = call_handler.mock_call()

# Mock transcription without Whisper
stt = SpeechToText()
result = stt.mock_transcribe("Sample response")
```

## Error Handling

The system includes comprehensive error handling for:
- Failed API calls
- Audio processing issues
- NLP analysis errors
- Decision engine failures

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.