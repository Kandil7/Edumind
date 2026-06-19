class SpeechServiceImpl:
    """Speech service with stub implementations for MVP."""

    async def text_to_speech(self, text: str, language: str = "ar") -> bytes:
        # Stub: In production, use Whisper/TTS API
        return b"audio_stub"

    async def speech_to_text(self, audio: bytes, language: str = "ar") -> str:
        # Stub: In production, use Whisper API
        return "[transcription stub - integrate Whisper API]"
