
from pymongo.mongo_client import MongoClient
import certifi
uri = "mongodb+srv://username:password@netflix.s0ikh66.mongodb.net/?retryWrites=true&w=majority"


# mongoimport --uri "mongodb+srv://nagasuresh:LTOJzMBRshCukNcm@netflix.s0ikh66.mongodb.net/?retryWrites=true&w=majority" --type csv --headerline --db database  --collection netflix --file netflix.csv

def main():
    # Create a new client and connect to the server
    client = MongoClient(uri,tlsCAFile=certifi.where())
    try:
        client.admin.command('ping')
        print("You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)


