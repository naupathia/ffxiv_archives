#!/usr/bin/env python3

import os
from pprint import pp
from dotenv import load_dotenv
from src.xivexport import adapter, search, xivclient, model
from itertools import batched

# Load environment variables from .env file
load_dotenv()

API_USER = os.getenv("MONGO_USERNAME")
API_SECRET = os.getenv("MONGO_SECRET")

ROOT_PATH = 'C:\\Users\\naupa.LAURENPC2\\dev\\ffxiv_archives\\xivexport'
INPUT_PATH = f"{ROOT_PATH}\\_dumps\\input"

VERSION_NAME = os.listdir(INPUT_PATH)[-1]

DATA_PATH = f"{INPUT_PATH}\\{VERSION_NAME}\\exd"
OUTPUT_PATH = f"{ROOT_PATH}\\_dumps\\output"
OUTPUT_FILE = f"{OUTPUT_PATH}\\dump.txt"

def delete_dump_file():        
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        print(f"File '{OUTPUT_FILE}' deleted successfully.")
    else:
        print(f"File '{OUTPUT_FILE}' does not exist.")

def dump_docs(docs):
    """Outputs the search items as plaintext to a txt file. Mainly for debugging purposes."""

    print("Outputting text files...")
    with open(OUTPUT_FILE, "a", encoding="UTF-8") as fh:
        for doc in docs:
            fh.write(_serialize(doc))


def _serialize(doc: model.SearchItem):
    return doc.as_plain_text()

def connect():
    search.ClientManager.connect(API_USER, API_SECRET)
    xivclient.XivApiClientManager.connect()

def close():
    search.ClientManager.close()
    xivclient.XivApiClientManager.close()

def save_batch(docs: list[model.SearchItem]):
    dump_docs(docs)
    print(f"inserting records...")
    search.ClientManager.upload_docs([d.model_dump() for d in docs])

def clear_data():
    # pass
    delete_dump_file()
    print("Truncating records...")
    search.ClientManager.truncate()

def main():
    """Entry point for the xivexport application."""
    connect()
    clear_data()

    try:
        adapters = adapter.__all__

        for adp in adapters:
            print(f"Loading docs for {adp.__name__}...")
            for docs in batched(adp.get_all(), 1000):
                save_batch(docs)
            print(f"*******************************\nDone with {adp.__name__}!\n*******************************")
    finally:
        print("Done!")
        close()

if __name__ == "__main__":
    main()