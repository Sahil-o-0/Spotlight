from pymongo import MongoClient
from pymongo.server_api import ServerApi

class Config:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://admin:admin@cluster0.xb5x6kl.mongodb.net/Spotlight", server_api=ServerApi('1'))
        self.db = self.client["Spotlight"]
        


config = Config()
