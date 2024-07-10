
from .parse import (
    quests,
    cutscenes,
    items,
    tripletriadcards,
    statuses,
    fates,
    fishes,
    mounts,
    custom
)

from .settings import OUTPUT_PATH

# import meilisearch
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
    mounts.DATATYPE: mounts.serialize,
    custom.DATATYPE: custom.serialize
    
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

    # @classmethod
    # def search_client(cls):
    #     return meilisearch.Client('https://ms-fe1609dcce38-6766.nyc.meilisearch.io', os.getenv('API_KEY'))
        

def get_all_docs():
    
    print("gathering records...")
    docs = []
    docs = docs + list(quests.QuestIterator())
    docs = docs + list(cutscenes.CutsceneIterator())
    docs = docs + list(items.ItemIterator())
    docs = docs + list(tripletriadcards.TripleTriadCardIterator())
    docs = docs + list(custom.CustomDirIterator())
    docs = docs + list(fishes.FishIterator())
    docs = docs + list(mounts.MountIterator())
    docs = docs + list(fates.FatesIterator())

    return docs

def upload_docs(docs):

    db = ClientManager.connect().tea
    collection = db.lore
    
    print("truncating collection...")
    collection.delete_many({})

    print("inserting records...")
    collection.insert_many(docs)

    # client = ClientManager.search_client()

    # print('truncating collection...')
    # task = client.index('lore').delete_all_documents()

    # while task.status in ('enqueued', 'processing'):
    #     time.sleep(0.5)
    #     task = client.get_task(task.task_uid)    

    # print('uploading documents...')
    # client.index('lore').add_documents_in_batches(docs, primary_key="id")

def dump_docs(docs):

    print('outputting text files...')
    with open(f"{OUTPUT_PATH}\\dump.txt", "w+", encoding="UTF-8") as fh:    
        for doc in docs:
            fh.write(_serialize(doc))

def _serialize(doc):

    method = SERIALIZERS[doc["datatype"]]
    return method(doc)


def run():

    docs = get_all_docs()

    dump_docs(docs)
    upload_docs(docs)


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
