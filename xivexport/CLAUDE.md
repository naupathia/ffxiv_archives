# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Always use context7 when I need code generation, setup or configuration steps, or
library/API documentation. This means you should automatically use the Context7 MCP
tools to resolve library id and get library docs without me having to explicitly ask.

## Project Overview

This is the **XIV Export** tool - a Python application that extracts Final Fantasy XIV game data from various sources and uploads it to MongoDB for searchable indexing. The tool processes multiple types of game content including quests, items, cutscenes, mounts, fates, fish, Triple Triad cards, status effects, and custom text.

## Common Commands

### Development
```bash
# Install dependencies (using uv)
uv sync

# Run the main export tool
python __main__.py

# Alternative entry point
python -m xivexport

# Run tests
pytest

# Run specific test types
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m "not slow"    # Skip slow tests

# Run tests with coverage
pytest --cov=src/xivexport
```

### Environment Setup
The application requires a `.env` file with:
```
MONGO_USERNAME=your_username
MONGO_SECRET=your_password
```

## Architecture

### Core Components

- **`__main__.py`** - Main entry point that orchestrates the full data export process
- **`src/xivexport/adapter.py`** - Contains data adapters that map game data to search models:
  - `QuestAdapter`, `ItemAdapter`, `MountAdapter`, `FishAdapter`, `FateAdapter`
  - `TripleTriadCardAdapter`, `StatusAdapter`, `CutsceneAdapter`, `CustomTextAdapter`
- **`src/xivexport/model.py`** - Pydantic models for search items and their metadata
- **`src/xivexport/xivclient.py`** - Client for accessing XIV game data
- **`src/xivexport/search.py`** - MongoDB connection and upload functionality
- **`src/xivexport/_scrub.py`** - Data cleaning and text processing utilities
- **`src/xivexport/_tools.py`** - General utility functions

### Data Flow

1. **Connect**: Establish connections to MongoDB and XIV data sources
2. **Clear**: Truncate existing data and delete previous dump files
3. **Process**: For each adapter in `adapter.__all__`:
   - Load game data using the adapter's `DATA_CLASS`
   - Map data to `SearchItem` models via `map_model()`
   - Process in batches of 1000 items
   - Save to both text dump files and MongoDB
4. **Close**: Clean up connections

### Data Processing Pipeline

Each data type follows the same pattern:
- `DataAdapter.get_data()` → fetches raw game data via `xivclient.XivDataAccess`
- `DataAdapter.map_model()` → transforms to `model.SearchItem` subclass
- Items without text content are filtered out
- Results are batched and uploaded to MongoDB via `search.ClientManager`

### Testing

- Test configuration in `pytest.ini` with markers for `unit`, `integration`, and `slow` tests
- Async test support enabled with `asyncio_mode = auto`
- Tests located in `tests/` directory with fixtures in `conftest.py`
- Coverage reporting available via `pytest --cov`

## Development Notes

- The export process truncates and rebuilds the entire MongoDB collection on each run
- Hard-coded paths in `__main__.py` point to `_dumps/input` for game data
- Text output is saved to `_dumps/output/dump.txt` for debugging
- Uses Pydantic models for data validation and serialization
- Implements batched processing to handle large datasets efficiently
- Error handling logs failures but continues processing other items