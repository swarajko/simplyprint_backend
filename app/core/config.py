"""
Configuration management for the application.
Uses Pydantic Settings to load environment variables.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    
    simplyprint_api_key: str = "key"
    simplyprint_company_id: str = "123"
    simplyprint_base_url: str = "https://api.simplyprint.io"
    
    # Database - for update later
    database_url: Optional[str] = None
    
    app_name: str = "PrintFarm Onground Backend"
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
