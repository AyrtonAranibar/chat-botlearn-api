# app/core/config.py
import os
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()  # carga variables desde .env

class Settings:
    def __init__(self) -> None:
        self.VLLM_BASE_URL: str = os.getenv("VLLM_BASE_URL", "http://127.0.0.1:8000")
        self.VLLM_MODEL: str = os.getenv("VLLM_MODEL", "meta-llama/Llama-3.2-3B-Instruct")

@lru_cache
def get_settings() -> Settings:
    return Settings()