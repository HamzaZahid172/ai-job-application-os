import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "AI Job Application OS")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data/applications.db")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
    use_llm: bool = os.getenv("USE_LLM", "true").lower() == "true"

settings = Settings()
