from pprint import pp
from . import adapter, model
from .settings import OUTPUT_PATH

import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class ClientManager:
    _client: MongoClient = None

    @classmethod
    def connect(cls) -> MongoClient:
        if not cls._client:
            api_user = os.getenv("MONGO_USERNAME")
            api_secret = os.getenv("MONGO_SECRET")
            uri = f"mongodb+srv://{api_user}:{api_secret}@cluster0.1buu3qz.mongodb.net/?retryWrites=true&w=majority"

            # Create a new client and connect to the server
            cls._client = MongoClient(uri, server_api=ServerApi("1"))

            # Send a ping to confirm a successful connection
            try:
                cls._client.admin.command("ping")
                print("Pinged your deployment. You successfully connected to MongoDB!")
            except Exception as e:
                print(e)

        return cls._client

def upload_docs(docs):

    db = ClientManager.connect().tea
    collection = db.lore

    # print("truncating collection...")
    # collection.delete_many({})

    print("inserting records...")
    collection.insert_many(docs)


def dump_docs(docs):
    """Outputs the search items as plaintext to a txt file. Mainly for debugging purposes."""

    print("outputting text files...")
    with open(f"{OUTPUT_PATH}\\dump.txt", "w+", encoding="UTF-8") as fh:
        for doc in docs:
            fh.write(_serialize(doc))


def _serialize(doc: model.SearchItem):

    return doc.as_plain_text()


async def run():

    sheets = await adapter.CustomTextAdapter.get_all(1)

    pp(sheets[0])

    pp(sheets[0].as_plain_text())
