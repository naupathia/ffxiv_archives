# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Always use context7 when I need code generation, setup or configuration steps, or
library/API documentation. This means you should automatically use the Context7 MCP
tools to resolve library id and get library docs without me having to explicitly ask.

## Project Overview

This is the **Lore Search App**, a Next.js 14 web application for searching through archived FFXIV (Final Fantasy XIV) game content. It provides full-text search capabilities across quests, cutscenes, items, and other game content stored in MongoDB.

## Common Commands

```bash
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

### Framework & Stack
- **Next.js 14** with TypeScript and App Router
- **Tailwind CSS** for styling
- **MongoDB** with Atlas Search for data storage and search
- **SWR** for client-side data fetching
- **Axios** for HTTP requests

### Key Directories
- `app/` - Next.js App Router pages and components
  - `api/` - API routes (search, lore-entries, synonyms)
  - `search/` - Main search interface
  - `item/[id]/` - Individual item detail pages
  - `bookmarks/` - Bookmark management pages
  - `lib/` - Shared utilities and data fetching functions
  - `ui/` - Reusable UI components
- `types/` - TypeScript type definitions
- `public/` - Static assets

### Core Components
- `app/lib/data.ts` - MongoDB data access layer using MongoDB Data API
- `app/api/search/route.ts` - Search API endpoint
- `app/search/page.tsx` - Main search page
- `types/objectTypes.ts` - Core type definitions (LoreEntry, SearchParams, etc.)

### Data Flow
1. User searches via the search interface
2. Client makes API request to `/api/search`
3. API calls `fetchSearchResults()` which uses MongoDB Data API
4. MongoDB Atlas Search indexes provide full-text search with synonyms
5. Results are paginated (100 items per page) and returned to client
6. SWR manages client-side caching and revalidation

### Database Schema
The app connects to MongoDB collection `tea.lore` with documents following the `LoreEntry` type:
- `_id` - MongoDB ObjectId
- `datatype` - Content category (quest, cutscene, item, etc.)
- `name` - Entry title
- `text` - Searchable content
- `expansion` - Game expansion (optional)
- `rank` - Search relevance rank (optional)
- `meta` - Additional metadata (patch, place_name, etc.)

### Search Features
- **Text Search**: Full-text search across name and text fields
- **Phrase Search**: Exact phrase matching with quotes
- **Synonyms**: Custom synonym mapping for better search results
- **Filtering**: Category and expansion filters
- **Sorting**: Default relevance or by category
- **Pagination**: 100 results per page

### Environment Setup
Requires `.env.local` file with:
- `API_KEY` - MongoDB Data API key
- `COLLECTION_NAME` - MongoDB collection name

### TypeScript Configuration
- Path alias `@/*` maps to root directory
- Strict mode enabled
- Uses Next.js TypeScript plugin