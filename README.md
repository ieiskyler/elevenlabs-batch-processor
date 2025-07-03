# ElevenLabs Batch Calling Data Processor

A Python toolkit for managing and processing ElevenLabs batch calling data, including batch retrieval, data conversion, and recipient analysis.

## Features

- **Batch Management**: Fetch batch calling data from ElevenLabs API
- **Data Conversion**: Convert JSON batch data to CSV format
- **Bulk Processing**: Process multiple batches from a CSV list
- **Recipient Analysis**: Extract and analyze recipient data with phone numbers
- **Rate Limiting**: Built-in API rate limiting to prevent quota exhaustion

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your ElevenLabs API key
   ```

## Configuration

Create a `.env` file in the project root:
```
ELEVENLABS_API_KEY=your_api_key_here
ELEVENLABS_API_BASE=https://api.elevenlabs.io/v1/convai/batch-calling
```

## Usage

### 1. Fetch Batch History
```bash
python src/batch_history.py
```

### 2. Convert Single Batch JSON to CSV
```bash
python src/batch_converter.py input.json output.csv
```

### 3. Process Multiple Batches
```bash
python src/batch_processor.py batch_list.csv recipients_output.csv
```

### 4. Convert Batch List JSON to CSV
```bash
python src/batch_list_converter.py batch_list.json batch_list.csv
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
