#!/usr/bin/env python3
import os
from pymongo import MongoClient

def test_connection():
    connection_string = os.getenv('MONGODB_URI', 'mongodb://192.168.1.157:27017/')
    
    client = MongoClient(connection_string)
    server_info = client.server_info()
    print("✓ MongoDB verbunden!")
    print(f"  Version: {server_info['version']}")
    
    databases = client.list_database_names()
    print(f"  Datenbanken: {len(databases)}")
    return True

def test_basic_operations():
    connection_string = os.getenv('MONGODB_URI', 'mongodb://192.168.1.157:27017/')
    
    client = MongoClient(connection_string)
    test_db = client['test_database']
    test_collection = test_db['test_collection']
    
    test_doc = {"name": "Test", "type": "Demo", "date": "2025-06-06"}
    result = test_collection.insert_one(test_doc)
    print(f"✓ Dokument eingefügt: {result.inserted_id}")
    
    found_doc = test_collection.find_one({"_id": result.inserted_id})
    print(f"✓ Dokument gefunden: {found_doc['name']}")
    
    test_collection.delete_one({"_id": result.inserted_id})
    print("✓ Test Dokument gelöscht")
    return True

def main():
    print("MongoDB Setup Test")
    print("=" * 20)
    
    print("\n1. Verbindung testen...")
    test_connection()
    
    print("\n2. Operationen testen...")
    test_basic_operations()
    
    print("\n3. Setup komplett!")
    print("\nJetzt verfügbar:")
    print("  python database_explorer.py")
    print("  python restaurant_crud.py")
    print("  python power_monitor.py")
    
    print("\nODM Info:")
    print("ODM = Object Document Mapping")
    print("- Dokumente <-> Python Objekte")
    print("- Datenvalidierung")
    print("- Schema Management")

if __name__ == "__main__":
    main()
