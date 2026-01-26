from pymongo.mongo_client import MongoClient, Collection
from pymongo.server_api import ServerApi


class ClientManager:
    _client: MongoClient = None
    _collection: Collection = None

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
        cls._collection.insert_many(docs)

    @classmethod
    def close(cls):
        cls._collection = None
        cls._client.close()
        cls._client = None
