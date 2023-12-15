import pprint
from .parse import (
    quests,
    cutscenes,
    items,
    tripletriadcards,
    statuses,
    fates,
    fishes,
    mounts,
)

from .settings import OUTPUT_PATH

from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

SERIALIZERS = {
    quests.DATATYPE: quests.serialize,
    items.DATATYPE: items.serialize,
    cutscenes.DATATYPE: cutscenes.serialize,
    tripletriadcards.DATATYPE: tripletriadcards.serialize,
    statuses.DATATYPE: statuses.serialize,
    fates.DATATYPE: fates.serialize,
    fishes.DATATYPE: fishes.serialize,
    mounts.DATATYPE: mounts.serialize
}

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

def get_all_docs():
    
    docs = []
    docs = docs + [doc for doc in quests.QuestIterator()]
    docs = docs + [doc for doc in cutscenes.CutsceneIterator()]
    docs = docs + [doc for doc in items.ItemIterator()]
    docs = docs + [doc for doc in tripletriadcards.TripleTriadCardIterator()]
    docs = docs + [doc for doc in statuses.StatusIterator()]
    docs = docs + [doc for doc in fishes.FishIterator()]
    docs = docs + [doc for doc in mounts.MountIterator()]
    docs = docs + [doc for doc in fates.FatesIterator()]

    return docs

def upload_docs(docs):

    db = ClientManager.connect().tea
    collection = db.lore
    # collection.remove({})

    collection.insert_many(docs)

def dump_docs(docs):

    with open(f"{OUTPUT_PATH}\\dump.txt", "w+", encoding="UTF-8") as fh:    
        for doc in docs:
            fh.write(_serialize(doc))

def _serialize(doc):

    method = SERIALIZERS[doc["datatype"]]
    return method(doc)


def run():

    docs = get_all_docs()

    dump_docs(docs)


    # db = ClientManager.connect().tea
    # collection = db.lore

    # results = collection.aggregate(
    #     [
    #         {
    #             "$search": {
    #                 "index": "lore_text_search",
    #                 "text": {"query": "meracydia", "path": {"wildcard": "*"}},
    #             }
    #         },
    #         {"$limit": 20},
    #     ]
    # )

    # for i in results:
    #     pprint.pp(i)

    # quests.dump_text_file()
    # cutscenes.dump_text_file()
    # items.dump_text_file()
    # tripletriadcards.dump_text_file()
    # statuses.dump_text_file()
    # fates.dump_text_file()
    # fishes.dump_text_file()
    # mounts.dump_text_file()
