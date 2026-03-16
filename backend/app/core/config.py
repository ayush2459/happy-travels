from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    # =====================================================
    # DATABASE
    # =====================================================

    DATABASE_URL: str = "sqlite:///./travel.db"


    # =====================================================
    # JWT
    # =====================================================

    SECRET_KEY: str = "super-secret-key"

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440


    # =====================================================
    # RAZORPAY (SAFE DEFAULTS)
    # =====================================================

    RAZORPAY_KEY_ID: str = ""

    RAZORPAY_SECRET: str = ""

    RAZORPAY_WEBHOOK_SECRET: str = ""


    # =====================================================
    # OPTIONAL
    # =====================================================

    env: str | None = None

    frontend_url: str | None = None


settings = Settings()