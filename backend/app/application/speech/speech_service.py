"""Speech service using pluggable provider."""
from app.infrastructure.models.speech_provider import get_speech_provider, SpeechProvider


class SpeechServiceImpl:
    """Speech service that delegates to the best available provider."""

    def __init__(self, provider: SpeechProvider | None = None):
        self._provider = provider or get_speech_provider()

    async def text_to_speech(self, text: str, language: str = "ar") -> bytes:
        return await self._provider.text_to_speech(text, language)

    async def speech_to_text(self, audio: bytes, language: str = "ar") -> str:
        transcript, confidence = await self._provider.speech_to_text(audio, language)
        return transcript
