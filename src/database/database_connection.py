from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os


from bson import ObjectId

load_dotenv()
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

uri = f"mongodb+srv://Wcasa:{DATABASE_PASSWORD}@waqas.simtf.mongodb.net/?retryWrites=true&w=majority&appName=Waqas"

client = MongoClient(uri, server_api=ServerApi("1"))

collection = client.OnlineStore.Products


#! check webscraping results
if __name__ == "__main__":
    total = 0
    for product in collection.find():
        total += len(list(product.get("Variants")))
    print(total)
