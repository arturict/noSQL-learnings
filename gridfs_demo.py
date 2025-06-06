#!/usr/bin/env python3
from pymongo import MongoClient
import gridfs
import os

class FileManager:
    def __init__(self, connection_string=None):
        if connection_string is None:
            connection_string = os.getenv('MONGODB_URI', 'mongodb://192.168.1.157:27017/')
        
        self.client = MongoClient(connection_string)
        self.db = self.client['file_storage']
        self.fs = gridfs.GridFS(self.db)
        print("✓ GridFS File Manager bereit")
    
    def store_file(self, file_path, metadata=None):
        if not os.path.exists(file_path):
            print(f"Datei nicht gefunden: {file_path}")
            return None
        
        filename = os.path.basename(file_path)
        
        with open(file_path, 'rb') as f:
            file_id = self.fs.put(f, filename=filename, metadata=metadata)
        
        print(f"✓ Datei gespeichert: {filename} (ID: {file_id})")
        return file_id
    
    def retrieve_file(self, file_id, output_path):
        grid_out = self.fs.get(file_id)
        
        with open(output_path, 'wb') as f:
            f.write(grid_out.read())
        
        print(f"✓ Datei wiederhergestellt: {output_path}")
        return True
    
    def list_files(self):
        files = self.fs.find()
        for file in files:
            metadata = file.metadata or {}
            print(f"- {file.filename} (ID: {file._id}, Größe: {file.length} bytes)")
            if metadata:
                print(f"  Metadaten: {metadata}")
    
    def delete_file(self, file_id):
        self.fs.delete(file_id)
        print(f"✓ Datei gelöscht: {file_id}")

class PhotoAlbum:
    def __init__(self, connection_string=None):
        if connection_string is None:
            connection_string = os.getenv('MONGODB_URI', 'mongodb://192.168.1.157:27017/')
        
        self.client = MongoClient(connection_string)
        self.db = self.client['photo_album']
        self.fs = gridfs.GridFS(self.db)
        print("✓ Fotoalbum bereit")
    
    def add_photo(self, photo_path, album_name, description=""):
        if not os.path.exists(photo_path):
            print(f"Foto nicht gefunden: {photo_path}")
            return None
        
        filename = os.path.basename(photo_path)
        metadata = {
            'album': album_name,
            'description': description,
            'type': 'photo'
        }
        
        with open(photo_path, 'rb') as f:
            file_id = self.fs.put(f, filename=filename, metadata=metadata)
        
        print(f"✓ Foto zu Album '{album_name}' hinzugefügt: {filename}")
        return file_id
    
    def get_album_photos(self, album_name):
        photos = self.fs.find({'metadata.album': album_name})
        return list(photos)
    
    def download_album(self, album_name, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        photos = self.get_album_photos(album_name)
        
        for photo in photos:
            output_path = os.path.join(output_dir, photo.filename)
            with open(output_path, 'wb') as f:
                f.write(photo.read())
            print(f"✓ Heruntergeladen: {photo.filename}")
        
        print(f"Album '{album_name}' heruntergeladen nach {output_dir}")
    
    def list_albums(self):
        albums = self.fs.find().distinct('metadata.album')
        return albums
    
    def list_album_contents(self, album_name):
        photos = self.get_album_photos(album_name)
        print(f"\nAlbum '{album_name}':")
        for photo in photos:
            desc = photo.metadata.get('description', 'Keine Beschreibung')
            print(f"- {photo.filename}: {desc}")

def demo_file_storage():
    print("GridFS File Storage Demo")
    print("=" * 25)
    
    fm = FileManager()
    
    test_file = "/tmp/test.txt"
    with open(test_file, 'w') as f:
        f.write("Dies ist ein Test für GridFS!\nZweite Zeile des Tests.")
    
    file_id = fm.store_file(test_file, {'test': True, 'author': 'Demo'})
    
    restored_file = "/tmp/restored_test.txt"
    fm.retrieve_file(file_id, restored_file)
    
    print("\nGespeicherte Dateien:")
    fm.list_files()
    
    print("\nGridFS Collections:")
    collections = fm.db.list_collection_names()
    for col in collections:
        print(f"- {col}")
    
    print("\nfs.files Collection Struktur:")
    files_doc = fm.db['fs.files'].find_one()
    if files_doc:
        for key, value in files_doc.items():
            print(f"  {key}: {value}")
    
    print("\nDatei-Chunks (fs.chunks):")
    chunk = fm.db['fs.chunks'].find_one()
    if chunk:
        print(f"  data type: {type(chunk['data'])}")
        print(f"  data encoding: Base64 BSON Binary")

def demo_photo_album():
    print("\n\nFotoalbum Demo")
    print("=" * 15)
    
    album = PhotoAlbum()
    
    test_images = [
        ("/tmp/vacation1.jpg", "Urlaub 2025", "Strand bei Sonnenuntergang"),
        ("/tmp/vacation2.jpg", "Urlaub 2025", "Hotel am Meer"),
        ("/tmp/family1.jpg", "Familie", "Familienfeier"),
    ]
    
    for img_path, album_name, desc in test_images:
        with open(img_path, 'wb') as f:
            f.write(b"FAKE_IMAGE_DATA_" + desc.encode())
        album.add_photo(img_path, album_name, desc)
    
    print("\nVerfügbare Alben:")
    albums = album.list_albums()
    for album_name in albums:
        album.list_album_contents(album_name)

def main():
    print("GridFS und Fotoalbum")
    print("=" * 20)
    
    while True:
        print("\nOptionen:")
        print("1. File Storage Demo")
        print("2. Fotoalbum Demo")
        print("3. Beenden")
        
        choice = input("\nWählen (1-3): ").strip()
        
        if choice == "1":
            demo_file_storage()
        elif choice == "2":
            demo_photo_album()
        elif choice == "3":
            break
        else:
            print("Ungültige Option")

if __name__ == "__main__":
    main()
