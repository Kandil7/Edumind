from abc import ABC, abstractmethod


class EmbeddingService(ABC):
    @abstractmethod
    async def embed(self, text: str) -> list[float]: ...

    @abstractmethod
    async def embed_batch(self, texts: list[str]) -> list[list[float]]: ...


class LLMService(ABC):
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        max_tokens: int = 1024,
        temperature: float = 0.7,
    ) -> str: ...


class SpeechService(ABC):
    @abstractmethod
    async def text_to_speech(self, text: str, language: str = "ar") -> bytes: ...

    @abstractmethod
    async def speech_to_text(self, audio: bytes, language: str = "ar") -> str: ...
