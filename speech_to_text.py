import whisper
import requests
from typing import Dict, Optional
import tempfile
import os

class SpeechToText:
    def __init__(self, model_name: str = "base"):
        """Initialize Whisper model for speech recognition"""
        try:
            self.model = whisper.load_model(model_name)
        except Exception as e:
            print(f"Warning: Could not load Whisper model: {e}")
            self.model = None

    async def transcribe(self, audio_url: str) -> Dict[str, str]:
        """Transcribe audio from URL to text"""
        try:
            # Download audio file
            audio_data = await self._download_audio(audio_url)
            if not audio_data:
                return {"text": "", "error": "Failed to download audio"}

            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_file.write(audio_data)
                temp_path = temp_file.name

            try:
                # Transcribe using Whisper
                result = self.model.transcribe(temp_path)
                transcribed_text = result["text"]

                return {
                    "text": transcribed_text,
                    "language": result.get("language", "en")
                }

            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        except Exception as e:
            return {"text": "", "error": str(e)}

    async def _download_audio(self, url: str) -> Optional[bytes]:
        """Download audio file from URL"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.content
        except Exception as e:
            print(f"Error downloading audio: {e}")
            return None

    def mock_transcribe(self, mock_response: str) -> Dict[str, str]:
        """Mock transcription for testing without actual audio"""
        return {
            "text": mock_response,
            "language": "en"
        }

    async def transcribe_stream(self, audio_stream: bytes) -> Dict[str, str]:
        """Transcribe audio from a byte stream"""
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_file.write(audio_stream)
                temp_path = temp_file.name

            try:
                result = self.model.transcribe(temp_path)
                return {
                    "text": result["text"],
                    "language": result.get("language", "en")
                }
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        except Exception as e:
            return {"text": "", "error": str(e)}