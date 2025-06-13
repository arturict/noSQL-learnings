#!/usr/bin/env python3
from pymongo import MongoClient
from bson import ObjectId
import os

class DatabaseExplorer:
    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        print("MongoDB verbunden!")
    
    def list_databases(self):
        db_names = self.client.list_database_names()
        return [db for db in db_names if db not in ['admin', 'local', 'config']]
    
    def list_collections(self, database_name):
        db = self.client[database_name]
        return db.list_collection_names()
    
    def list_documents(self, database_name, collection_name):
        db = self.client[database_name]
        collection = db[collection_name]
        documents = collection.find({}, {"_id": 1})
        return [str(doc["_id"]) for doc in documents]
    
    def get_document(self, database_name, collection_name, document_id):
        db = self.client[database_name]
        collection = db[collection_name]
        
        if len(document_id) == 24:
            query_id = ObjectId(document_id)
        else:
            query_id = document_id
        
        return collection.find_one({"_id": query_id})
    
    def display_document(self, document):
        if document:
            for key, value in document.items():
                print(f"{key}: {value}")
    
    def run(self):
        while True:
            databases = self.list_databases()
            
            if not databases:
                print("No Database")
                input("Press any button to return")
                continue
            
            print("Databases")
            for db in databases:
                print(f" - {db}")
            
            db_name = input("\nSelect Database: ").strip()
            
            if db_name not in databases:
                print(f"Database '{db_name}' not found")
                continue
            
            collections = self.list_collections(db_name)
            
            if not collections:
                print("No Collections")
                input("Press any button to return")
                continue
            
            print(f"\n{db_name}")
            print("\nCollections")
            for col in collections:
                print(f" - {col}")
            
            col_name = input("\nSelect Collection: ").strip()
            
            if col_name not in collections:
                print(f"Collection '{col_name}' not found")
                continue
            
            documents = self.list_documents(db_name, col_name)
            
            if not documents:
                print("No Documents")
                input("Press any button to return")
                continue
            
            print(f"\n{db_name}.{col_name}")
            print("\nDocuments")
            for doc_id in documents:
                print(f" - {doc_id}")
            
            doc_id = input("\nSelect Document: ").strip()
            
            if doc_id not in documents:
                print(f"Document '{doc_id}' not found")
                continue
            
            document = self.get_document(db_name, col_name, doc_id)
            
            print(f"\n{db_name}.{col_name}.{doc_id}")
            print()
            self.display_document(document)
            
            print("\nPress any button to return")
            input()

def main():
    connection_string = os.getenv('MONGODB_URI', 'mongodb://192.168.1.157:27017/')
    
    explorer = DatabaseExplorer(connection_string)
    explorer.run()

if __name__ == "__main__":
    main()
