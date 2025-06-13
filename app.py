import os
from pymongo import MongoClient

connection_string = os.getenv('MONGODB_URI', 'mongodb://192.168.1.157:27017/')
client = MongoClient(connection_string)

print(client.server_info()) 
