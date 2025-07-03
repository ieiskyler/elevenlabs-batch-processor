"""
Tests for the batch processor module.
"""

import pytest
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

from batch_processor import BatchProcessor


class TestBatchProcessor:
    """Test cases for the BatchProcessor class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.processor = BatchProcessor(rate_limit_delay=0.1)
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
                }
            ]
        }
    
    def test_read_batch_ids_from_csv_success(self):
        """Test successful reading of batch IDs from CSV."""
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_file = Path(temp_dir) / "batches.csv"
            
            # Create test CSV
            with open(csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'name'])
                writer.writerow(['batch_1', 'First Batch'])
                writer.writerow(['batch_2', 'Second Batch'])
            
            batch_ids = self.processor.read_batch_ids_from_csv(csv_file)
            
            assert batch_ids == ['batch_1', 'batch_2']
    
    def test_read_batch_ids_from_csv_file_not_found(self):
        """Test reading batch IDs from non-existent CSV file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_file = Path(temp_dir) / "missing.csv"
            
            with pytest.raises(FileNotFoundError):
                self.processor.read_batch_ids_from_csv(csv_file)
    
    def test_read_batch_ids_from_csv_missing_id_column(self):
        """Test reading batch IDs from CSV without 'id' column."""
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_file = Path(temp_dir) / "batches.csv"
            
            # Create CSV without 'id' column
            with open(csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['name', 'description'])
                writer.writerow(['First Batch', 'Description'])
            
            with pytest.raises(ValueError, match="CSV file must contain 'id' column"):
                self.processor.read_batch_ids_from_csv(csv_file)
    
    @patch('batch_processor.requests.get')
    def test_fetch_batch_success(self, mock_get):
        """Test successful batch fetching."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.sample_batch_data
        mock_get.return_value = mock_response
        
        result = self.processor.fetch_batch("batch_123")
        
        assert result == self.sample_batch_data
        mock_get.assert_called_once()
    
    @patch('batch_processor.requests.get')
    def test_fetch_batch_http_error(self, mock_get):
        """Test batch fetching with HTTP error."""
        import requests
        mock_get.side_effect = requests.exceptions.RequestException("HTTP Error")
        
        result = self.processor.fetch_batch("batch_123")
        
        assert result is None
    
    def test_extract_recipients(self):
        """Test recipient extraction from batch data."""
        recipients = list(self.processor.extract_recipients(self.sample_batch_data))
        
        assert len(recipients) == 1
        recipient = recipients[0]
        
        assert recipient["batch_id"] == "batch_123"
        assert recipient["batch_name"] == "Test Batch"
        assert recipient["recipient_id"] == "recipient_1"
        assert recipient["phone_number"] == "+1234567890"
        assert recipient["city"] == "New York"
    
    def test_extract_city_success(self):
        """Test city extraction from recipient data."""
        recipient = {
            "conversation_initiation_client_data": {
                "dynamic_variables": {
                    "city": "Boston"
                }
            }
        }
        
        city = self.processor._extract_city(recipient)
        assert city == "Boston"
    
    def test_extract_city_missing_data(self):
        """Test city extraction with missing data."""
        recipient = {}
        
        city = self.processor._extract_city(recipient)
        assert city == ""
