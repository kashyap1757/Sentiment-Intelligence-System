from dataclasses import dataclass
import os

@dataclass
class Settings:
    app_name: str = "Sentiment Intelligence System"
    model_path: str = os.getenv("MODEL_PATH", "models/model.pkl")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

settings = Settings()
