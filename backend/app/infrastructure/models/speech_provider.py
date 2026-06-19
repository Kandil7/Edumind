"""Whisper-based ASR and TTS speech services."""
import io
import tempfile
import os
from abc import ABC, abstractmethod


class SpeechProvider(ABC):
    """Abstract speech provider interface."""

    @abstractmethod
    async def speech_to_text(self, audio: bytes, language: str = "ar") -> tuple[str, float]:
        """Transcribe audio to text. Returns (transcript, confidence)."""
        ...

    @abstractmethod
    async def text_to_speech(self, text: str, language: str = "ar") -> bytes:
        """Convert text to audio bytes (WAV format)."""
        ...


class WhisperSpeechProvider(SpeechProvider):
    """Real Whisper-based speech provider using OpenAI Whisper API or local model."""

    def __init__(self, model_size: str = "small", api_key: str | None = None):
        self.model_size = model_size
        self.api_key = api_key
        self._local_model = None

    def _get_local_model(self):
        if self._local_model is None:
            try:
                import whisper
                self._local_model = whisper.load_model(self.model_size)
            except ImportError:
                raise RuntimeError(
                    "whisper package not installed. Run: pip install openai-whisper"
                )
        return self._local_model

    async def speech_to_text(self, audio: bytes, language: str = "ar") -> tuple[str, float]:
        if self.api_key:
            return await self._api_transcribe(audio, language)
        return await self._local_transcribe(audio, language)

    async def _api_transcribe(self, audio: bytes, language: str) -> tuple[str, float]:
        """Use OpenAI Whisper API for transcription."""
        import httpx

        lang_map = {"ar": "ar", "en": "en", "fr": "fr", "es": "es"}
        whisper_lang = lang_map.get(language, "en")

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                files={"file": ("audio.wav", audio, "audio/wav")},
                data={"model": "whisper-1", "language": whisper_lang},
                timeout=30.0,
            )
            response.raise_for_status()
            result = response.json()
            return result.get("text", ""), 0.95

    async def _local_transcribe(self, audio: bytes, language: str) -> tuple[str, float]:
        """Use local Whisper model for transcription."""
        import asyncio

        model = self._get_local_model()

        # Write audio to temp file (Whisper needs a file path)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio)
            tmp_path = tmp.name

        try:
            result = await asyncio.to_thread(
                model.transcribe,
                tmp_path,
                language=language if language in ("ar", "en") else None,
            )
            return result.get("text", ""), 0.9
        finally:
            os.unlink(tmp_path)

    async def text_to_speech(self, text: str, language: str = "ar") -> bytes:
        """Convert text to speech using gTTS (Google TTS) or edge-tts."""
        try:
            return await self._edge_tts(text, language)
        except Exception:
            return await self._gtts_fallback(text, language)

    async def _edge_tts(self, text: str, language: str) -> bytes:
        """Use edge-tts for high-quality multilingual TTS."""
        import asyncio
        import edge_tts

        voice_map = {
            "ar": "ar-SA-ZariyahNeural",
            "en": "en-US-JennyNeural",
            "fr": "fr-FR-DeniseNeural",
            "es": "es-ES-ElviraNeural",
        }
        voice = voice_map.get(language, "en-US-JennyNeural")

        communicate = edge_tts.Communicate(text, voice)
        audio_chunks = []
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_chunks.append(chunk["data"])

        return b"".join(audio_chunks)

    async def _gtts_fallback(self, text: str, language: str) -> bytes:
        """Fallback TTS using gTTS."""
        from gtts import gTTS

        lang_map = {"ar": "ar", "en": "en", "fr": "fr", "es": "es"}
        tts_lang = lang_map.get(language, "en")

        tts = gTTS(text=text, lang=tts_lang)
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        return audio_bytes.getvalue()


class StubSpeechProvider(SpeechProvider):
    """Stub provider for when no speech library is installed."""

    async def speech_to_text(self, audio: bytes, language: str = "ar") -> tuple[str, float]:
        return f"[STUB] Transcription placeholder for {len(audio)} bytes audio", 0.0

    async def text_to_speech(self, text: str, language: str = "ar") -> bytes:
        return b"audio_stub"


def get_speech_provider() -> SpeechProvider:
    """Factory to get the best available speech provider."""
    api_key = os.environ.get("OPENAI_API_KEY", "")

    if api_key:
        return WhisperSpeechProvider(model_size="small", api_key=api_key)

    try:
        import whisper  # noqa: F401
        return WhisperSpeechProvider(model_size="small")
    except ImportError:
        pass

    try:
        import edge_tts  # noqa: F401
        return WhisperSpeechProvider(model_size="small")
    except ImportError:
        pass

    return StubSpeechProvider()
