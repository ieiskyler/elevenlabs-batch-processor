"""
Batch history fetcher for ElevenLabs batch calling data.

This module provides functionality to fetch and save batch history from the ElevenLabs API.
"""

import json
import requests
import argparse
import logging
from pathlib import Path
from typing import Dict, Optional
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


class BatchHistoryFetcher:
    """Fetch batch history from ElevenLabs API."""
    
    def __init__(self):
        """Initialize the batch history fetcher."""
        self.api_base = config.api_base
        self.headers = config.headers
    
    def fetch_workspace_batches(self, output_file: Path = None) -> Optional[Dict]:
        """
        Fetch batch history from workspace.
        
        Args:
            output_file: Optional path to save the JSON data
            
        Returns:
            Dictionary containing batch history data, or None if failed
        """
        logger.info("Fetching batch history from workspace...")
        
        try:
            # Remove the specific batch ID from the URL to get workspace batches
            workspace_url = f"{self.api_base}/workspace"
            
            response = requests.get(
                workspace_url,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Save to file if specified
            if output_file:
                self._save_to_file(data, output_file)
                logger.info(f"Batch history saved to {output_file}")
            
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch batch history: {e}")
            return None
    
    def _save_to_file(self, data: Dict, output_file: Path) -> None:
        """
        Save data to JSON file.
        
        Args:
            data: Data to save
            output_file: Output file path
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving to file {output_file}: {e}")
            raise


def main():
    """Command line interface for batch history fetching."""
    parser = argparse.ArgumentParser(
        description="Fetch ElevenLabs batch history from workspace",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python batch_history.py
    python batch_history.py --output history.json
    python batch_history.py -o data/batch_history.json
        """
    )
    
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default="batch_history.json",
        help="Output JSON file (default: batch_history.json)"
    )
    
    args = parser.parse_args()
    
    try:
        fetcher = BatchHistoryFetcher()
        data = fetcher.fetch_workspace_batches(args.output)
        
        if data:
            batch_count = len(data.get("batch_calls", []))
            logger.info(f"Successfully fetched {batch_count} batches")
        else:
            logger.error("Failed to fetch batch history")
            return 1
            
    except Exception as e:
        logger.error(f"Error fetching batch history: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
