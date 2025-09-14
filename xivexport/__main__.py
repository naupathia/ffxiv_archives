#!/usr/bin/env python3

from src.xivexport import app
import asyncio

def main():
    """Entry point for the xivexport application."""
    asyncio.run(app.run())


if __name__ == "__main__":
    main()