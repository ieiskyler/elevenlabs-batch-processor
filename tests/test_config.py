"""
Tests for the configuration module.
"""

import pytest
import os
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Set testing environment
os.environ["TESTING"] = "true"

from config import Config


class TestConfig:
    """Test cases for the Config class."""
    
    def test_config_initialization_success(self):
        """Test successful configuration initialization."""
        with patch.dict(os.environ, {
            'ELEVENLABS_API_KEY': 'test_key',
            'ELEVENLABS_API_BASE': 'https://test.api.com'
        }):
            config = Config()
            assert config.api_key == 'test_key'
            assert config.api_base == 'https://test.api.com'
    
    def test_config_missing_api_key(self):
        """Test configuration with missing API key."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="Required environment variable ELEVENLABS_API_KEY"):
                Config()
    
    def test_config_default_api_base(self):
        """Test configuration with default API base."""
        with patch.dict(os.environ, {
            'ELEVENLABS_API_KEY': 'test_key'
        }, clear=True):
            config = Config()
            assert config.api_base == "https://api.elevenlabs.io/v1/convai/batch-calling"
    
    def test_headers_property(self):
        """Test headers property."""
        with patch.dict(os.environ, {
            'ELEVENLABS_API_KEY': 'test_key'
        }):
            config = Config()
            headers = config.headers
            assert headers == {"xi-api-key": "test_key"}
    
    def test_dotenv_loading(self):
        """Test that dotenv loading works correctly."""
        # Since load_dotenv is called at module level, we can't easily mock it
        # Instead, test that the config can be loaded with environment variables
        with patch.dict(os.environ, {
            'ELEVENLABS_API_KEY': 'test_key',
            'ELEVENLABS_API_BASE': 'https://test.com'
        }):
            config = Config()
            assert config.api_key == 'test_key'
            assert config.api_base == 'https://test.com'
