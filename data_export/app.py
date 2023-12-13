from .parse import quests, cutscenes, items, tripletriadcards, statuses, fates, fishes, mounts

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def run():
    uri = "mongodb+srv://tea_app:GQzBeQxpwlW3t4mV@cluster0.1buu3qz.mongodb.net/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    # quests.dump_text_file()
    # cutscenes.dump_text_file()
    # items.dump_text_file()
    # tripletriadcards.dump_text_file()
    # statuses.dump_text_file()
    # fates.dump_text_file()
    # fishes.dump_text_file()
    # mounts.dump_text_file()

