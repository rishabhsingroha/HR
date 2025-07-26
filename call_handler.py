from typing import Dict, Optional
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
from text_to_speech import TextToSpeech
import os
from dotenv import load_dotenv

load_dotenv()

class CallHandler:
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.phone_number = os.getenv('TWILIO_PHONE_NUMBER')
        self.client = Client(self.account_sid, self.auth_token)
        self.tts = TextToSpeech()
        self.questions = [
            "Can you tell me about yourself?",
            "What are your key skills?",
            "How many years of experience do you have?",
            
        ]

    async def start_call(self, to_number: str) -> Dict:
        """Initiate a call to the candidate"""
        try:
            call = self.client.calls.create(
                to=to_number,
                from_=self.phone_number,
                url=self._get_webhook_url('/welcome'),
                status_callback=self._get_webhook_url('/call-status'),
                status_callback_event=['completed', 'failed']
            )
            return {"call_id": call.sid, "status": call.status}
        except Exception as e:
            raise Exception(f"Failed to initiate call: {str(e)}")

    def _get_webhook_url(self, endpoint: str) -> str:
        """Get the webhook URL for Twilio callbacks"""
        base_url = os.getenv('BASE_URL', 'http://localhost:8000')
        return f"{base_url}{endpoint}"

    async def handle_welcome(self) -> str:
        """Generate TwiML for welcome message"""
        response = VoiceResponse()
        response.say(
            "Hello, this is the HR team calling regarding your job application. "
            "We would like to ask you a few questions."
        )
        return self._ask_next_question(response, 0)

    async def handle_response(self, question_index: int, response_audio: bytes) -> Optional[str]:
        """Process candidate's response and ask next question"""
        if question_index >= len(self.questions):
            return self._generate_goodbye_twiml()

        # Here we would normally process the audio response
        # For now, we'll just continue with the next question
        response = VoiceResponse()
        return self._ask_next_question(response, question_index + 1)

    def _ask_next_question(self, response: VoiceResponse, index: int) -> str:
        """Add the next question to the TwiML response"""
        if index < len(self.questions):
            gather = Gather(
                input='speech',
                action=f'/handle-response?question={index}',
                method='POST',
                timeout=5,
                speech_timeout='auto'
            )
            gather.say(self.questions[index])
            response.append(gather)

            # If no input received
            response.redirect(f'/handle-response?question={index}')
        else:
            response.append(self._generate_goodbye_twiml())

        return str(response)

    def _generate_goodbye_twiml(self) -> str:
        """Generate TwiML for goodbye message"""
        response = VoiceResponse()
        response.say(
            "Thank you for your time. We will review your responses "
            "and get back to you soon. Have a great day!"
        )
        response.hangup()
        return str(response)

    async def handle_call_status(self, call_sid: str, status: str) -> None:
        """Handle call status updates"""
        # Log call status and take appropriate actions
        print(f"Call {call_sid} status: {status}")

    def mock_call(self) -> Dict:
        """Mock function for testing without actual Twilio integration"""
        return {
            "call_id": "mock_call_id",
            "status": "completed",
            "responses": [
                "I am John Doe with 5 years of software development experience.",
                "My key skills are Python, JavaScript, and Cloud Technologies.",
                "5 years",
                "New York",
                "Yes, I can join within 2 weeks"
            ]
        }