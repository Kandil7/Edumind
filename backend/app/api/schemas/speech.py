from pydantic import BaseModel


class TTSRequest(BaseModel):
    text: str
    language: str = "ar"


class ASRRequest(BaseModel):
    language: str = "ar"


class ASRResponse(BaseModel):
    transcript: str
    confidence: float | None = None


class SpeechResponse(BaseModel):
    audio_url: str
