# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Always use context7 when I need code generation, setup or configuration steps, or
library/API documentation. This means you should automatically use the Context7 MCP
tools to resolve library id and get library docs without me having to explicitly ask.

## Project Overview

This repository contains a FFXIV (Final Fantasy XIV) archives system with two main components:

1. **Data Export Tool** (`data_export/`) - Python application that extracts game data from various sources and uploads to MongoDB
2. **Lore Search App** (`lore-search-app/`) - Next.js web application for searching through the archived game content

## Common Commands

### XIV Data Export Tool (Python)
```bash
# Run the data export tool to update records after patch
python -m xivexport.__main__

# Install Python dependencies
pip install -r xivexport/requirement.txt
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
- **Main entry**: `__main__.py` calls `app.run()`
- **Data parsers**: Located in `parse/` directory, each handles different content types:
  - `quests.py` - Quest data
  - `cutscenes.py` - Cutscene dialogues
  - `items.py` - Game items
  - `tripletriadcards.py` - Triple Triad cards
  - `fates.py` - FATE events
  - `fishes.py` - Fishing data
  - `mounts.py` - Mount data
  - `custom.py` - Custom content
- **Database**: Uses MongoDB Atlas with connection managed by `ClientManager` class
- **Environment**: Requires `.env` file with `MONGO_USERNAME` and `MONGO_SECRET`

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

- Both components share the same MongoDB database (`tea.lore2` collection)
- The data export tool truncates and rebuilds the entire collection on each run
- Web app uses SWR for client-side data fetching
- TypeScript path aliases configured with `@/*` pointing to root directory
