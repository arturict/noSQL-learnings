#!/usr/bin/env python3
import os

def read_path_variable():
    print("Umgebungsvariablen Demo")
    print("=" * 25)
    
    path = os.environ.get('PATH')
    home = os.getenv('HOME', 'Nicht gesetzt')
    user = os.environ.get('USER', 'Unbekannt')
    
    print(f"HOME: {home}")
    print(f"USER: {user}")
    print(f"PATH Einträge: {len(path.split(':')) if path else 0}")

def demonstrate_mongodb_connection():
    print("\nMongoDB Verbindung")
    print("=" * 20)
    
    mongodb_uri = os.getenv('MONGODB_URI')
    
    if mongodb_uri:
        print("✓ MongoDB URI gefunden")
        from pymongo import MongoClient
        client = MongoClient(mongodb_uri)
        server_info = client.server_info()
        print(f"✓ Verbunden - Version: {server_info['version']}")
        return True
    else:
        print("✗ MONGODB_URI nicht gesetzt")
        print("Setze: export MONGODB_URI='mongodb://192.168.1.157:27017/'")
        return False

def main():
    read_path_variable()
    demonstrate_mongodb_connection()
    
    print("\nSicherheit:")
    print("- Keine Passwörter im Code")
    print("- Umgebungsvariablen verwenden")
    print("- .env Dateien zu .gitignore hinzufügen")

if __name__ == "__main__":
    main()
