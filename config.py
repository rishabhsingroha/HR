import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twilio Configuration
TWILIO_CONFIG = {
    'account_sid': os.getenv('TWILIO_ACCOUNT_SID'),
    'auth_token': os.getenv('TWILIO_AUTH_TOKEN'),
    'phone_number': os.getenv('TWILIO_PHONE_NUMBER')
}

# Google Cloud Configuration
GOOGLE_CLOUD_CONFIG = {
    'project_id': os.getenv('GOOGLE_CLOUD_PROJECT_ID'),
    'credentials_path': os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
}

# Application Configuration
APP_CONFIG = {
    'host': os.getenv('APP_HOST', '0.0.0.0'),
    'port': int(os.getenv('APP_PORT', 8000)),
    'debug': os.getenv('DEBUG', 'False').lower() == 'true',
    'base_url': os.getenv('BASE_URL', 'http://localhost:8000')
}

# NLP Configuration
NLP_CONFIG = {
    'sentiment_threshold': 0.5,
    'keyword_min_length': 3,
    'max_keywords': 10
}

# Interview Questions
INTERVIEW_QUESTIONS = [
    {
        'id': 'intro',
        'text': 'Can you tell me about yourself?',
        'type': 'open_ended',
        'weight': 1.0
    },
    {
        'id': 'skills',
        'text': 'What are your key skills?',
        'type': 'skills',
        'weight': 1.5
    },
    {
        'id': 'experience',
        'text': 'How many years of experience do you have?',
        'type': 'numeric',
        'weight': 1.2
    },
    {
        'id': 'location',
        'text': 'What is your current location?',
        'type': 'location',
        'weight': 0.8
    },
    {
        'id': 'availability',
        'text': 'Are you available to join immediately?',
        'type': 'boolean',
        'weight': 0.5
    }
]

# Decision Engine Configuration
DECISION_CONFIG = {
    'score_weights': {
        'skills': 0.4,
        'experience': 0.3,
        'communication': 0.3
    },
    'thresholds': {
        'recommend': 0.8,
        'consider': 0.6,
        'escalate': 0.4
    }
}

# Error Messages
ERROR_MESSAGES = {
    'twilio_error': 'Failed to initiate call',
    'transcription_error': 'Failed to transcribe audio',
    'tts_error': 'Failed to convert text to speech',
    'nlp_error': 'Failed to analyze response',
    'general_error': 'An unexpected error occurred'
}