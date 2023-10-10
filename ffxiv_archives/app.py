from ffxiv_archives import quests, cut_scenes

from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://tea_admin:BC5AOSNbRuhJPge4@cluster0.1buu3qz.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

quests.output_quests()
cut_scenes.output_cutscenes()
