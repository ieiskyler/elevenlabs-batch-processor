"""
Batch processor for ElevenLabs batch calling data.

This module provides functionality to fetch batch data from the ElevenLabs API
and process recipients data from multiple batches.
"""

import csv
import requests
import time
import logging
import argparse
from typing import List, Dict, Generator, Optional
from pathlib import Path
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BatchProcessor:
    """Process ElevenLabs batch calling data."""
    
    def __init__(self, rate_limit_delay: float = 0.2):
        """
        Initialize the batch processor.
        
        Args:
            rate_limit_delay: Delay between API calls to avoid rate limiting
        """
        self.rate_limit_delay = rate_limit_delay
        self.api_base = config.api_base
        self.headers = config.headers
    
    def read_batch_ids_from_csv(self, csv_file: Path) -> List[str]:
        """
        Read batch IDs from a CSV file.
        
        Args:
            csv_file: Path to CSV file containing batch IDs in 'id' column
            
        Returns:
            List of batch IDs
            
        Raises:
            FileNotFoundError: If CSV file doesn't exist
            ValueError: If CSV file has invalid format
        """
        if not csv_file.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_file}")
        
        batch_ids = []
        try:
            with open(csv_file, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if 'id' not in reader.fieldnames:
                    raise ValueError("CSV file must contain 'id' column")
                
                for row in reader:
                    if 'id' in row and row['id']:
                        batch_ids.append(row['id'])
        except Exception as e:
            logger.error(f"Error reading CSV file {csv_file}: {e}")
            raise
        
        return batch_ids
    
    def fetch_batch(self, batch_id: str) -> Optional[Dict]:
        """
        Fetch batch data from ElevenLabs API.
        
        Args:
            batch_id: ID of the batch to fetch
            
        Returns:
            Batch data as dictionary, or None if failed
        """
        logger.info(f"Fetching batch {batch_id}...")
        
        try:
            response = requests.get(
                f"{self.api_base}/{batch_id}",
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch batch {batch_id}: {e}")
            return None
    
    def extract_recipients(self, batch_data: Dict) -> Generator[Dict, None, None]:
        """
        Extract recipient data from batch data.
        
        Args:
            batch_data: Batch data dictionary
            
        Yields:
            Dictionary containing recipient information
        """
        recipients = batch_data.get("recipients", [])
        
        for recipient in recipients:
            row = {
                "batch_id": batch_data.get("id"),
                "batch_name": batch_data.get("name"),
                "agent_id": batch_data.get("agent_id"),
                "agent_name": batch_data.get("agent_name"),
                "created_at_unix": batch_data.get("created_at_unix"),
                "scheduled_time_unix": batch_data.get("scheduled_time_unix"),
                "total_calls_dispatched": batch_data.get("total_calls_dispatched"),
                "total_calls_scheduled": batch_data.get("total_calls_scheduled"),
                "last_updated_at_unix": batch_data.get("last_updated_at_unix"),
                "status": batch_data.get("status"),
                "recipient_id": recipient.get("id"),
                "phone_number": recipient.get("phone_number"),
                "recipient_status": recipient.get("status"),
                "recipient_created_at_unix": recipient.get("created_at_unix"),
                "recipient_updated_at_unix": recipient.get("updated_at_unix"),
                "conversation_id": recipient.get("conversation_id"),
                "city": self._extract_city(recipient)
            }
            yield row
    
    def _extract_city(self, recipient: Dict) -> str:
        """
        Extract city from recipient data.
        
        Args:
            recipient: Recipient data dictionary
            
        Returns:
            City name or empty string if not found
        """
        try:
            return recipient["conversation_initiation_client_data"]["dynamic_variables"].get("city", "")
        except (KeyError, TypeError):
            return ""
    
    def process_batch_list(self, batch_list_csv: Path, output_csv: Path) -> None:
        """
        Process multiple batches and save recipients to CSV.
        
        Args:
            batch_list_csv: Path to CSV file containing batch IDs
            output_csv: Path to output CSV file for recipients
        """
        batch_ids = self.read_batch_ids_from_csv(batch_list_csv)
        logger.info(f"Read {len(batch_ids)} batch IDs from {batch_list_csv}")
        
        all_rows = []
        
        for batch_id in batch_ids:
            batch_data = self.fetch_batch(batch_id)
            if not batch_data:
                continue
                
            for row in self.extract_recipients(batch_data):
                all_rows.append(row)
            
            # Rate limiting
            time.sleep(self.rate_limit_delay)
        
        if all_rows:
            self._write_to_csv(all_rows, output_csv)
            logger.info(f"Wrote {len(all_rows)} recipient rows to {output_csv}")
        else:
            logger.warning("No recipient data found to write.")
    
    def _write_to_csv(self, rows: List[Dict], output_file: Path) -> None:
        """
        Write rows to CSV file.
        
        Args:
            rows: List of data rows
            output_file: Output CSV file path
        """
        if not rows:
            logger.warning("No data to write to CSV")
            return
        
        fieldnames = list(rows[0].keys())
        
        try:
            with open(output_file, "w", newline='', encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
        except Exception as e:
            logger.error(f"Error writing to CSV file {output_file}: {e}")
            raise


def main():
    """Command line interface for batch processing."""
    parser = argparse.ArgumentParser(
        description="Process ElevenLabs batch calling data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python batch_processor.py batch_list.csv recipients.csv
    python batch_processor.py --rate-limit 0.5 batch_list.csv recipients.csv
        """
    )
    
    parser.add_argument(
        "batch_list_csv",
        type=Path,
        help="CSV file with batch IDs in 'id' column"
    )
    parser.add_argument(
        "output_csv",
        type=Path,
        help="Output CSV file for all recipients"
    )
    parser.add_argument(
        "--rate-limit",
        type=float,
        default=0.2,
        help="Delay between API calls in seconds (default: 0.2)"
    )
    
    args = parser.parse_args()
    
    try:
        processor = BatchProcessor(rate_limit_delay=args.rate_limit)
        processor.process_batch_list(args.batch_list_csv, args.output_csv)
    except Exception as e:
        logger.error(f"Error processing batches: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
