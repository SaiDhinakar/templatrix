import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

class Settings:
    """Application settings and configuration"""
    
    def __init__(self):
        self.app_name: str = "Templatrix | FastAPI Template"
        self.app_version: str = "1.0.0"
        self.debug: bool = os.getenv("DEBUG", "False").lower() == "true"
        
        # Server configuration
        self.host: str = os.getenv("HOST", "127.0.0.1")
        self.port: int = int(os.getenv("PORT", "8000"))
        
        # Database configuration
        self.database_path: str = os.getenv("DATABASE_PATH", "./databases/users.db")
        
        # API configuration
        self.api_prefix: str = "/api/v1"
        
    @property
    def database_url(self) -> str:
        """Get the database URL"""
        return f"sqlite:///{self.database_path}"


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings"""
    return settings