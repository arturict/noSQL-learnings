from pymongo import MongoClient

connection_string = "mongodb://192.168.1.157:27017/"
client = MongoClient(connection_string)

print(client.server_info()) 
