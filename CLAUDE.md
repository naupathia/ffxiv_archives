# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Always use context7 when I need code generation, setup or configuration steps, or
library/API documentation. This means you should automatically use the Context7 MCP
tools to resolve library id and get library docs without me having to explicitly ask.

## Project Overview

This repository contains a FFXIV (Final Fantasy XIV) archives system with two main components:

1. **Data Export Tool** (`xivexport/`) - Python application that extracts game data from various sources and uploads to MongoDB
2. **Lore Search App** (`lore-search-app/`) - Next.js web application for searching through the archived game content

## Common Commands

### XIV Data Export Tool (Python)
```bash
# Navigate to the xivexport directory first
cd xivexport

# Install dependencies using uv (preferred)
uv sync

# Run the data export tool to update records after patch
python __main__.py

# Alternative entry point
python -m xivexport

# Run tests
pytest

# Run specific test types
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m "not slow"    # Skip slow tests
```

### Lore Search App (Next.js)
```bash
# Navigate to the app directory first
cd lore-search-app

# Development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Lint code
npm run lint

# Install dependencies
npm install
```

## Architecture

### Data Export Tool (`xivexport/`)
- **Purpose**: Extracts and processes FFXIV game data, uploads to MongoDB
- **Main entry**: `__main__.py` orchestrates the full data export process
- **Core components**:
  - `src/xivexport/adapter.py` - Data adapters that map game data to search models
  - `src/xivexport/model.py` - Pydantic models for search items and metadata
  - `src/xivexport/xivclient.py` - Client for accessing XIV game data
  - `src/xivexport/search.py` - MongoDB connection and upload functionality
- **Data adapters**: Handle different content types (quests, cutscenes, items, tripletriadcards, fates, fishes, mounts, custom text, status effects)
- **Database**: Uses MongoDB Atlas with connection managed by `ClientManager` class
- **Environment**: Requires `.env` file with `MONGO_USERNAME` and `MONGO_SECRET`
- **Testing**: Uses pytest with markers for unit, integration, and slow tests

### Lore Search App (`lore-search-app/`)
- **Framework**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS
- **Database**: MongoDB for search data
- **Key features**:
  - Full-text search across all game content types
  - Category and expansion filtering
  - Pagination and sorting
- **Main routes**:
  - `/` - Redirects to `/search`
  - `/search` - Main search interface
  - `/api/search` - Search API endpoint
- **Environment**: Requires `.env.local` file for database configuration

### Data Flow
1. Data export tool parses game files and uploads structured data to MongoDB
2. Web app connects to same MongoDB instance for search functionality
3. Search uses MongoDB Atlas Search indexes for full-text search capabilities

## Development Notes

- Both components share the same MongoDB database (`tea.lore` collection)
- The data export tool truncates and rebuilds the entire collection on each run
- Web app uses SWR for client-side data fetching
- TypeScript path aliases configured with `@/*` pointing to root directory
- Export tool uses modern Python packaging with `pyproject.toml` and `uv` for dependency management
- Data processing follows a consistent pattern: fetch → map to SearchItem → batch upload to MongoDB
- Export tool processes data in batches of 1000 items for memory efficiency
