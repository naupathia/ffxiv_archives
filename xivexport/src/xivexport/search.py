from pymongo.mongo_client import MongoClient, Collection
from pymongo.server_api import ServerApi
import pymongo

import logging

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.StreamHandler())
LOGGER.setLevel(logging.CRITICAL)

class ClientManager:
    _client: MongoClient = None
    _collection: Collection = None

    @classmethod
    def create_doc_key(cls, type, row_id, key):
        return f"{type}{row_id}-{key}"

    @classmethod
    def connect(cls, api_user, api_secret) -> MongoClient:
        """Connects to the mongodb"""
        if not cls._client:
            uri = f"mongodb+srv://{api_user}:{api_secret}@cluster0.1buu3qz.mongodb.net/?retryWrites=true&w=majority"

            # Create a new client and connect to the server
            cls._client = MongoClient(uri, server_api=ServerApi("1"))

            # Send a ping to confirm a successful connection
            try:
                cls._client.admin.command("ping")
                print("Pinged your deployment. You successfully connected to MongoDB!")
            except Exception as e:
                print(e)

        cls._collection = cls._client.tea.lore_v2

    @classmethod
    def truncate(cls):
        """Clears out the current collection"""
        cls._collection.delete_many({})

    @classmethod
    def upload_docs(cls, docs):
        """Inserts the records to mongodb"""
        # try:
        cls._collection.insert_many(docs)
        
        # except pymongo.errors.BulkWriteError as e:
        #     LOGGER.warning(e, exc_info=e)
            
    @classmethod
    def find_doc(cls, type, row, name):
        doc_id = cls.create_doc_key(type, row, name)

        return cls._collection.find_one(doc_id)

    @classmethod
    def close(cls):
        cls._collection = None
        cls._client.close()
        cls._client = None
