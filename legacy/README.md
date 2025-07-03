# Legacy Files

⚠️ **DEPRECATED**: These files are deprecated and maintained for backward compatibility only.

## Migration Guide

Please use the new modular structure in the `src/` directory:

### Old → New Mapping

- `bt-json-to-csv.py` → `src/batch_converter.py`
- `btid-json-to-csv.py` → `src/batch_list_converter.py`
- `cek-phonenumber-from-btid.py` → `src/batch_processor.py`
- `history-bt-id.py` → `src/batch_history.py`

### Key Improvements in New Version

1. **Security**: No hard-coded API keys
2. **Error Handling**: Better error handling and logging
3. **Documentation**: Full docstrings and type hints
4. **Testing**: Complete test coverage
5. **Modularity**: Reusable classes and functions
6. **CLI**: Better command-line interfaces

### Migration Steps

1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment: `cp .env.example .env` and add your API key
3. Use new modules from `src/` directory
4. Remove old files when migration is complete

## Support

For help migrating from legacy files, please refer to the main README.md or open an issue.
