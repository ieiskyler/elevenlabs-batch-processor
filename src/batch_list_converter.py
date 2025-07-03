"""
Batch list converter for ElevenLabs batch calling data.

This module provides functionality to convert JSON batch lists to CSV format.
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


class BatchListConverter:
    """Convert ElevenLabs batch list data between formats."""
    
    # Standard field names for batch list CSV
    BATCH_LIST_FIELDNAMES = [
        "id",
        "phone_number_id",
        "phone_provider",
        "name",
        "agent_id",
        "agent_name",
        "created_at_unix",
        "scheduled_time_unix",
        "total_calls_dispatched",
        "total_calls_scheduled",
        "last_updated_at_unix",
        "status"
    ]
    
    def convert_batch_list(self, json_file: Path, csv_file: Path) -> None:
        """
        Convert batch list JSON data to CSV format.
        
        Args:
            json_file: Path to input JSON file containing batch list
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
        
        # Extract batch calls data
        batch_calls = data.get("batch_calls", [])
        if not batch_calls:
            logger.warning(f"No batch_calls found in {json_file}")
            return
        
        # Convert to CSV rows
        rows = []
        for batch in batch_calls:
            row = self._create_batch_row(batch)
            rows.append(row)
        
        # Write to CSV
        self._write_to_csv(rows, csv_file, self.BATCH_LIST_FIELDNAMES)
        logger.info(f"Converted {len(rows)} batches from {json_file} to {csv_file}")
    
    def _create_batch_row(self, batch: Dict) -> Dict:
        """
        Create a CSV row for a batch.
        
        Args:
            batch: Batch data dictionary
            
        Returns:
            Dictionary containing batch row data
        """
        return {field: batch.get(field, "") for field in self.BATCH_LIST_FIELDNAMES}
    
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
    """Command line interface for batch list conversion."""
    parser = argparse.ArgumentParser(
        description="Convert ElevenLabs batch list JSON data to CSV format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python batch_list_converter.py batch_list.json batch_list.csv
    python batch_list_converter.py input/batches.json output/batches.csv
        """
    )
    
    parser.add_argument(
        "input_json",
        type=Path,
        help="Input JSON file containing batch list data"
    )
    parser.add_argument(
        "output_csv",
        type=Path,
        help="Output CSV file for converted data"
    )
    
    args = parser.parse_args()
    
    try:
        converter = BatchListConverter()
        converter.convert_batch_list(args.input_json, args.output_csv)
    except Exception as e:
        logger.error(f"Error converting batch list data: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
