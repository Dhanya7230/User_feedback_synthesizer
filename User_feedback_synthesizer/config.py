"""
Configuration module for the User Feedback Synthesizer agent.
Handles environment variables, paths, and Hindsight memory bank configuration.
"""

import os
from pathlib import Path
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load local environment variables if present
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

class AppConfig(BaseModel):
    # App metadata
    app_name: str = "User Feedback Synthesizer"
    version: str = "1.0.0"
    hackathon: str = "HackwithHyderabad 3.0"
    
    # Hindsight Configuration
    hindsight_mode: str = Field(
        default=os.getenv("HINDSIGHT_MODE", "embedded"),
        description="'embedded' for built-in high-fidelity Hindsight engine, 'server' for external Hindsight daemon."
    )
    hindsight_base_url: str = Field(
        default=os.getenv("HINDSIGHT_BASE_URL", "http://localhost:8888"),
        description="Base URL for remote or local Hindsight server"
    )
    hindsight_api_key: str = Field(
        default=os.getenv("HINDSIGHT_API_KEY", ""),
        description="Optional API key for Hindsight Cloud"
    )
    hindsight_bank_id: str = Field(
        default=os.getenv("HINDSIGHT_BANK_ID", "flowpilot-product-bank"),
        description="Memory bank identifier for FlowPilot user feedback"
    )

    # LLM Settings (optional live provider, defaults to rule-augmented neuro-symbolic engine)
    gemini_api_key: str = Field(
        default=os.getenv("GEMINI_API_KEY", ""),
        description="Gemini API Key if available"
    )
    openai_api_key: str = Field(
        default=os.getenv("OPENAI_API_KEY", ""),
        description="OpenAI API Key if available"
    )
    llm_provider: str = Field(
        default=os.getenv("LLM_PROVIDER", "gemini"),
        description="LLM provider: 'gemini', 'openai', or 'mock'"
    )

    # Data file paths
    data_dir: Path = DATA_DIR
    feedback_file: Path = DATA_DIR / "synthetic_feedback.json"
    changelog_file: Path = DATA_DIR / "changelog.json"
    personas_file: Path = DATA_DIR / "user_personas.json"
    memory_store_dir: Path = BASE_DIR / "storage" / "memory_store"

    # Analytics & Synthesis Thresholds
    sentiment_anomaly_drop_threshold: float = -0.40
    min_cluster_size: int = 3
    temporal_decay_half_life_days: float = 14.0

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"

config = AppConfig()

# Ensure directories exist
config.memory_store_dir.mkdir(parents=True, exist_ok=True)

