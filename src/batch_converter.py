"""
Batch data converter for ElevenLabs batch calling data.

This module provides functionality to convert JSON batch data to CSV format.
"""

import json
import csv
import argparse
import logging
from typing import List, Dict
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BatchConverter:
    """Convert ElevenLabs batch data between formats."""
    
    # Standard field names for batch data CSV
    BATCH_FIELDNAMES = [
        "batch_id",
        "batch_name",
        "agent_id",
        "agent_name",
        "created_at_unix",
        "scheduled_time_unix",
        "total_calls_dispatched",
        "total_calls_scheduled",
        "last_updated_at_unix",
        "status",
        "recipient_id",
        "phone_number",
        "recipient_status",
        "recipient_created_at_unix",
        "recipient_updated_at_unix",
        "conversation_id",
        "city"
    ]
    
    def json_to_csv(self, json_file: Path, csv_file: Path) -> None:
        """
        Convert single batch JSON data to CSV format.
        
        Args:
            json_file: Path to input JSON file
            csv_file: Path to output CSV file
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            ValueError: If JSON format is invalid
        """
        if not json_file.exists():
            raise FileNotFoundError(f"JSON file not found: {json_file}")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in {json_file}: {e}")
        
        # Extract recipients data
        recipients = data.get("recipients", [])
        if not recipients:
            logger.warning(f"No recipients found in {json_file}")
            return
        
        # Convert to CSV rows
        rows = []
        for recipient in recipients:
            row = self._create_recipient_row(data, recipient)
            rows.append(row)
        
        # Write to CSV
        self._write_to_csv(rows, csv_file, self.BATCH_FIELDNAMES)
        logger.info(f"Converted {len(rows)} recipients from {json_file} to {csv_file}")
    
    def _create_recipient_row(self, batch_data: Dict, recipient: Dict) -> Dict:
        """
        Create a CSV row for a recipient.
        
        Args:
            batch_data: Batch data dictionary
            recipient: Recipient data dictionary
            
        Returns:
            Dictionary containing recipient row data
        """
        # Extract city from dynamic variables
        city = self._extract_city(recipient)
        
        return {
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
            "city": city
        }
    
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
    
    def _write_to_csv(self, rows: List[Dict], output_file: Path, fieldnames: List[str]) -> None:
        """
        Write rows to CSV file.
        
        Args:
            rows: List of data rows
            output_file: Output CSV file path
            fieldnames: List of field names for CSV headers
        """
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
        except Exception as e:
            logger.error(f"Error writing to CSV file {output_file}: {e}")
            raise


def main():
    """Command line interface for batch conversion."""
    parser = argparse.ArgumentParser(
        description="Convert ElevenLabs batch JSON data to CSV format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python batch_converter.py batch_data.json batch_data.csv
    python batch_converter.py input/batch.json output/batch.csv
        """
    )
    
    parser.add_argument(
        "input_json",
        type=Path,
        help="Input JSON file containing batch data"
    )
    parser.add_argument(
        "output_csv",
        type=Path,
        help="Output CSV file for converted data"
    )
    
    args = parser.parse_args()
    
    try:
        converter = BatchConverter()
        converter.json_to_csv(args.input_json, args.output_csv)
    except Exception as e:
        logger.error(f"Error converting batch data: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
