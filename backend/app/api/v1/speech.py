from fastapi import APIRouter, Depends, UploadFile, File

from app.core.security import get_current_user
from app.api.schemas.speech import TTSRequest, ASRResponse, SpeechResponse

router = APIRouter(prefix="/speech", tags=["speech"])


@router.post("/tts", response_model=SpeechResponse)
async def text_to_speech(
    body: TTSRequest,
    user: dict = Depends(get_current_user),
):
    from app.application.speech.speech_service import SpeechServiceImpl

    service = SpeechServiceImpl()
    audio_bytes = await service.text_to_speech(body.text, body.language)
    # In production, store to S3/CDN and return URL
    return SpeechResponse(audio_url="/audio/temp_output.wav")


@router.post("/asr", response_model=ASRResponse)
async def speech_to_text(
    audio: UploadFile = File(...),
    language: str = "ar",
    user: dict = Depends(get_current_user),
):
    from app.application.speech.speech_service import SpeechServiceImpl

    service = SpeechServiceImpl()
    audio_bytes = await audio.read()
    transcript = await service.speech_to_text(audio_bytes, language)
    return ASRResponse(transcript=transcript, confidence=0.95)
