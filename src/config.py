"""
Configuration management for ElevenLabs Batch Calling Data Processor.

This module handles environment variable loading and configuration settings.
"""

import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for managing API settings and environment variables."""
    
    def __init__(self):
        """Initialize configuration with environment variables."""
        try:
            self.api_key = self._get_required_env("ELEVENLABS_API_KEY")
        except ValueError:
            # Allow missing API key during testing
            if os.getenv("TESTING") == "true":
                self.api_key = "test_key"
            else:
                raise
        self.api_base = self._get_env("ELEVENLABS_API_BASE", 
                                     "https://api.elevenlabs.io/v1/convai/batch-calling")
        
    def _get_required_env(self, key: str) -> str:
        """Get a required environment variable or raise an error."""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable {key} is not set. "
                           f"Please check your .env file.")
        return value
    
    def _get_env(self, key: str, default: str = "") -> str:
        """Get an environment variable with a default value."""
        return os.getenv(key, default)
    
    @property
    def headers(self) -> dict:
        """Get HTTP headers for API requests."""
        return {"xi-api-key": self.api_key}


# Global configuration instance
config = Config()
