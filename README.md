# ElevenLabs Batch Calling Data Processor

[![CI/CD Pipeline](https://github.com/ieiskyler/elevenlabs-batch-processor/actions/workflows/ci.yml/badge.svg)](https://github.com/ieiskyler/elevenlabs-batch-processor/actions/workflows/ci.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python toolkit for managing and processing ElevenLabs batch calling data, including batch retrieval, data conversion, and recipient analysis.

## ✨ Features

- **🔄 Batch Management**: Fetch batch calling data from ElevenLabs API
- **📊 Data Conversion**: Convert JSON batch data to CSV format
- **🚀 Bulk Processing**: Process multiple batches from a CSV list
- **📞 Recipient Analysis**: Extract and analyze recipient data with phone numbers
- **⚡ Rate Limiting**: Built-in API rate limiting to prevent quota exhaustion
- **🔒 Secure**: Environment-based configuration (no hard-coded API keys)
- **🧪 Tested**: Comprehensive test suite with 19 passing tests
- **📚 Documented**: Full documentation with type hints and examples

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/ieiskyler/elevenlabs-batch-processor.git
cd elevenlabs-batch-processor

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your ElevenLabs API key
ELEVENLABS_API_KEY=your_api_key_here
```

### Usage

```bash
# Run the demo
python demo.py

# Fetch batch history
python src/batch_history.py --output history.json

# Convert batch data to CSV
python src/batch_converter.py batch_data.json output.csv

# Process multiple batches
python src/batch_processor.py batch_list.csv recipients.csv
```

## Project Structure

```
eleven-labs/
├── src/
│   ├── __init__.py
│   ├── batch_history.py      # Fetch batch history from API
│   ├── batch_converter.py    # Convert single batch JSON to CSV
│   ├── batch_processor.py    # Process multiple batches
│   ├── batch_list_converter.py # Convert batch list JSON to CSV
│   └── config.py            # Configuration management
├── tests/
│   ├── __init__.py
│   ├── test_batch_converter.py
│   ├── test_batch_processor.py
│   └── test_config.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## API Reference

### BatchProcessor Class
- `fetch_batch(batch_id)`: Fetch a single batch from the API
- `extract_recipients(batch_data)`: Extract recipient data from batch
- `process_batch_list(csv_file, output_file)`: Process multiple batches

### BatchConverter Class
- `json_to_csv(json_file, csv_file)`: Convert JSON batch data to CSV
- `convert_batch_list(json_file, csv_file)`: Convert batch list to CSV

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run tests: `python -m pytest`
6. Submit a pull request

## License

MIT License - see LICENSE file for details
