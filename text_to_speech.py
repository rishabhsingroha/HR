from google.cloud import texttospeech
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class TextToSpeech:
    def __init__(self):
        """Initialize Google Cloud Text-to-Speech client"""
        try:
            self.client = texttospeech.TextToSpeechClient()
            self.voice = texttospeech.VoiceSelectionParams(
                language_code="en-US",
                name="en-US-Standard-I",
                ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
            )
            self.audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=0.9,  # Slightly slower for clarity
                pitch=0.0
            )
        except Exception as e:
            print(f"Warning: Could not initialize TTS client: {e}")
            self.client = None

    async def synthesize(self, text: str) -> Optional[bytes]:
        """Convert text to speech"""
        try:
            if not self.client:
                return self.mock_synthesize()

            synthesis_input = texttospeech.SynthesisInput(text=text)

            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=self.voice,
                audio_config=self.audio_config
            )

            return response.audio_content

        except Exception as e:
            print(f"Error in text-to-speech synthesis: {e}")
            return self.mock_synthesize()

    async def synthesize_ssml(self, ssml: str) -> Optional[bytes]:
        """Convert SSML to speech for more natural pronunciation"""
        try:
            if not self.client:
                return self.mock_synthesize()

            synthesis_input = texttospeech.SynthesisInput(ssml=ssml)

            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=self.voice,
                audio_config=self.audio_config
            )

            return response.audio_content

        except Exception as e:
            print(f"Error in SSML synthesis: {e}")
            return self.mock_synthesize()

    def mock_synthesize(self) -> bytes:
        """Return mock audio data for testing"""
        # Return a minimal valid MP3 file
        return b'ID3\x03\x00\x00\x00\x00\x00\x00'

    def customize_voice(self, 
                       language_code: str = "en-US",
                       voice_name: str = "en-US-Standard-I",
                       gender: str = "FEMALE",
                       speaking_rate: float = 0.9,
                       pitch: float = 0.0) -> None:
        """Customize the voice parameters"""
        gender_map = {
            "FEMALE": texttospeech.SsmlVoiceGender.FEMALE,
            "MALE": texttospeech.SsmlVoiceGender.MALE,
            "NEUTRAL": texttospeech.SsmlVoiceGender.NEUTRAL
        }

        self.voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name,
            ssml_gender=gender_map.get(gender, texttospeech.SsmlVoiceGender.FEMALE)
        )

        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=speaking_rate,
            pitch=pitch
        )

    def get_available_voices(self) -> list:
        """Get list of available voices"""
        try:
            if not self.client:
                return []

            voices = self.client.list_voices().voices
            return [
                {
                    "name": voice.name,
                    "language_codes": voice.language_codes,
                    "gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name
                }
                for voice in voices
            ]
        except Exception as e:
            print(f"Error getting available voices: {e}")
            return []