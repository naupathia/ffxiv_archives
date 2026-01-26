#!/usr/bin/env python3

import os
from pprint import pp
from dotenv import load_dotenv
from src.xivexport import adapter, search, xivclient, model
from itertools import batched
import json

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
OUTPUT_FILE_JSON = f"{OUTPUT_PATH}\\dump.json"

def delete_dump_file():        
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        print(f"File '{OUTPUT_FILE}' deleted successfully.")
    else:
        print(f"File '{OUTPUT_FILE}' does not exist.")

    if os.path.exists(OUTPUT_FILE_JSON):
        os.remove(OUTPUT_FILE_JSON)
        print(f"File '{OUTPUT_FILE_JSON}' deleted successfully.")
    else:
        print(f"File '{OUTPUT_FILE_JSON}' does not exist.")

def dump_docs(docs):
    """Outputs the search items as plaintext to a txt file. Mainly for debugging purposes."""

    print("Outputting text files...")
    with open(OUTPUT_FILE, "a", encoding="UTF-8") as fh:        
        for doc in docs:
            fh.write('\n')
            fh.write(doc.as_plain_text())
    
    data = []
    try :
        with open(OUTPUT_FILE_JSON, "r", encoding="UTF-8") as fh:
            data = json.load(fh)
    except Exception:
        data = []

    with open(OUTPUT_FILE_JSON, "w", encoding="UTF-8") as fh:
        json.dump(data + [x.model_dump() for x in docs], fh, indent=2)

def connect():
    search.ClientManager.connect(API_USER, API_SECRET)
    xivclient.XivApiClientManager.connect()

def close():
    search.ClientManager.close()
    xivclient.XivApiClientManager.close()

def save_batch(docs: list[model.SearchItem], remote_save=True):
    dump_docs(docs)
    print(f"inserting records...")
    if remote_save:
        search.ClientManager.upload_docs([d.model_dump() for d in docs])

def clear_data(is_test):
    # pass
    delete_dump_file()
    
    if not is_test:
        print("Truncating records...")
        search.ClientManager.truncate()

def main():
    """Entry point for the xivexport application."""
    debug = True
    debug_adapter = [adapter.AdventureAdapter]
    connect()

    clear_data(debug)

    batch_size = 10 if debug else 1000

    try:
        adapters = debug_adapter if debug and debug_adapter else adapter.__all__

        for adp in adapters:
            print(f"Loading docs for {adp.__name__}...")
            for docs in batched(adp.get_all(), batch_size):
                save_batch(docs, not debug)
                if debug:
                    break

            print(f"*******************************\nDone with {adp.__name__}!\n*******************************")

    finally:
        print("Done!")
        close()

if __name__ == "__main__":
    main()