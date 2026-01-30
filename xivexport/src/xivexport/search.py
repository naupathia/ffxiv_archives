from pymongo.mongo_client import MongoClient, Collection
from pymongo.server_api import ServerApi

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
    def connect(cls) -> MongoClient:
        """Connects to the mongodb"""
        if not cls._client:
            uri = f"mongodb+srv://{cls.API_USER}:{cls.API_SECRET}@cluster0.1buu3qz.mongodb.net/?retryWrites=true&w=majority"

            # Create a new client and connect to the server
            cls._client = MongoClient(uri, server_api=ServerApi("1"))

        cls._collection = cls._client.tea.lore

    @classmethod
    def ping(cls, api_user, api_secret):
        cls.API_USER = api_user
        cls.API_SECRET = api_secret
        try:
            cls.connect()
            cls._client.admin.command("ping")
            print("Pinged your deployment. You successfully connected to MongoDB!")

        except Exception as e:
            print(e)

        finally:
            cls.close()

    @classmethod
    def truncate(cls):
        """Clears out the current collection"""
        try:
            cls.connect()
            cls._collection.delete_many({})

        finally:
            cls.close()

    @classmethod
    def upload_docs(cls, docs):
        """Inserts the records to mongodb"""
        try:
            cls.connect()
            cls._collection.insert_many(docs, ordered=False)

        # except pymongo.errors.BulkWriteError as e:
        #     LOGGER.warning(e, exc_info=e)

        finally:
            cls.close()

    @classmethod
    def find_doc(cls, type, row, name):

        try:
            cls.connect()
            doc_id = cls.create_doc_key(type, row, name)
            return cls._collection.find_one(doc_id)

        finally:
            cls.close()

    @classmethod
    def close(cls):
        if cls._client:
            cls._collection = None
            cls._client.close()
            cls._client = None
