from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """
    Centraliza todas as configurações da aplicação.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    APP_NAME: str = "MixMind AI"
    APP_VERSION: str = "1.0.0"

    # ==========================================================
    # Paths
    # ==========================================================

    UPLOAD_DIR: str = "uploads"
    PROCESSED_DIR: str = "processed"
    TEMP_DIR: str = "temp"

    MAX_UPLOAD_SIZE: int = Field(
        default=100,
        description="Maximum upload size in MB",
    )

    BASE_URL: str = Field(
        default="http://localhost:8000",
        description="Public base URL used to generate file URLs.",
    )

    # ==========================================================
    # LLM
    # ==========================================================

    OPENROUTER_API_KEY: str = Field(
        default="",
        description="OpenRouter API key.",
    )

    OPENROUTER_BASE_URL: str = Field(
        default="https://openrouter.ai/api/v1",
        description="OpenRouter API endpoint.",
    )

    OPENROUTER_MODEL: str = Field(
        default="openai/gpt-oss-20b:free",
        description="Primary model.",
    )

    OPENROUTER_MODELS: list[str] = Field(
        default_factory=lambda: [
            "qwen/qwen3-next-80b-a3b-instruct",
            "google/gemma-4-31b-it:free",
            "google/gemma-4-26b-a4b-it:free",
            "tencent/hy3:free",
            "nvidia/nemotron-3-ultra-550b-a55b:free",
            "poolside/laguna-m.1:free",
            "qwen/qwen3-next-80b-a3b-instruct:free",
            "qwen/qwen3-coder:free",
            "nvidia/nemotron-3.5-content-safety:free",
            "meta-llama/llama-3.3-70b-instruct:free",
            "meta-llama/llama-3.2-3b-instruct:free",
            "nvidia/nemotron-3-super-120b-a12b:free",
            "nvidia/nemotron-3-nano-30b-a3b:free",
            "mistralai/mistral-medium-3.5-128b",
            "mistralai/mistral-small-4-119b-2603",
            "nvidia/nemotron-mini-4b-instruct",
        ],
        description="Fallback models in priority order.",
    )

    LLM_TIMEOUT: int = Field(
        default=30,
        ge=5,
        le=120,
    )

    LLM_MAX_RETRIES: int = Field(
        default=2,
        ge=0,
        le=5,
    )

    LLM_RETRY_BACKOFF_BASE: float = Field(
        default=1.0,
        ge=0.5,
        le=10.0,
    )

    LLM_MAX_TOKENS: int = Field(
        default=1500,
        ge=256,
        le=4096,
    )

    LLM_TEMPERATURE: float = Field(
        default=0.0,
        ge=0.0,
        le=2.0,
    )

    LLM_LOG_RAW_RESPONSES: bool = Field(
        default=False,
    )

    # ==========================================================
    # Computed Paths
    # ==========================================================

    @property
    def upload_path(self) -> Path:
        return BASE_DIR / self.UPLOAD_DIR

    @property
    def processed_path(self) -> Path:
        return BASE_DIR / self.PROCESSED_DIR

    @property
    def temp_path(self) -> Path:
        return BASE_DIR / self.TEMP_DIR

    @property
    def analysis_path(self) -> Path:
        return self.processed_path / "analysis"


settings = Settings()
