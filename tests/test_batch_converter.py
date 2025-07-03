"""
Tests for the batch converter module.
"""

import pytest
import json
import csv
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Set testing environment
os.environ["TESTING"] = "true"

from batch_converter import BatchConverter


class TestBatchConverter:
    """Test cases for the BatchConverter class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.converter = BatchConverter()
        self.sample_batch_data = {
            "id": "batch_123",
            "name": "Test Batch",
            "agent_id": "agent_456",
            "agent_name": "Test Agent",
            "created_at_unix": 1609459200,
            "scheduled_time_unix": 1609462800,
            "total_calls_dispatched": 5,
            "total_calls_scheduled": 10,
            "last_updated_at_unix": 1609466400,
            "status": "completed",
            "recipients": [
                {
                    "id": "recipient_1",
                    "phone_number": "+1234567890",
                    "status": "called",
                    "created_at_unix": 1609459200,
                    "updated_at_unix": 1609466400,
                    "conversation_id": "conv_1",
                    "conversation_initiation_client_data": {
                        "dynamic_variables": {
                            "city": "New York"
                        }
                    }
                },
                {
                    "id": "recipient_2",
                    "phone_number": "+0987654321",
                    "status": "pending",
                    "created_at_unix": 1609459200,
                    "updated_at_unix": 1609466400,
                    "conversation_id": "conv_2"
                }
            ]
        }
    
    def test_json_to_csv_success(self):
        """Test successful JSON to CSV conversion."""
        with tempfile.TemporaryDirectory() as temp_dir:
            json_file = Path(temp_dir) / "test.json"
            csv_file = Path(temp_dir) / "test.csv"
            
            # Write test JSON data
            with open(json_file, 'w') as f:
                json.dump(self.sample_batch_data, f)
            
            # Convert to CSV
            self.converter.json_to_csv(json_file, csv_file)
            
            # Verify CSV was created and has correct data
            assert csv_file.exists()
            
            with open(csv_file, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                
                assert len(rows) == 2
                assert rows[0]["batch_id"] == "batch_123"
                assert rows[0]["phone_number"] == "+1234567890"
                assert rows[0]["city"] == "New York"
                assert rows[1]["phone_number"] == "+0987654321"
                assert rows[1]["city"] == ""
    
    def test_json_to_csv_file_not_found(self):
        """Test JSON to CSV conversion with missing file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            json_file = Path(temp_dir) / "missing.json"
            csv_file = Path(temp_dir) / "output.csv"
            
            with pytest.raises(FileNotFoundError):
                self.converter.json_to_csv(json_file, csv_file)
    
    def test_json_to_csv_invalid_json(self):
        """Test JSON to CSV conversion with invalid JSON."""
        with tempfile.TemporaryDirectory() as temp_dir:
            json_file = Path(temp_dir) / "invalid.json"
            csv_file = Path(temp_dir) / "output.csv"
            
            # Write invalid JSON
            with open(json_file, 'w') as f:
                f.write("invalid json content")
            
            with pytest.raises(ValueError, match="Invalid JSON format"):
                self.converter.json_to_csv(json_file, csv_file)
    
    def test_extract_city_success(self):
        """Test city extraction from recipient data."""
        recipient = {
            "conversation_initiation_client_data": {
                "dynamic_variables": {
                    "city": "Los Angeles"
                }
            }
        }
        
        city = self.converter._extract_city(recipient)
        assert city == "Los Angeles"
    
    def test_extract_city_missing_data(self):
        """Test city extraction with missing data."""
        recipient = {}
        
        city = self.converter._extract_city(recipient)
        assert city == ""
    
    def test_create_recipient_row(self):
        """Test recipient row creation."""
        recipient = self.sample_batch_data["recipients"][0]
        
        row = self.converter._create_recipient_row(self.sample_batch_data, recipient)
        
        assert row["batch_id"] == "batch_123"
        assert row["batch_name"] == "Test Batch"
        assert row["recipient_id"] == "recipient_1"
        assert row["phone_number"] == "+1234567890"
        assert row["city"] == "New York"
