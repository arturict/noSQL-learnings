#!/usr/bin/env python3
from pymongo import MongoClient
from bson import ObjectId
import os
import re
import random

class Song:
    def __init__(self, name, artist, album=None, genre=None, year=None, _id=None):
        self._id = _id
        self.name = name
        self.artist = artist
        self.album = album
        self.genre = genre
        self.year = year
    
    def to_dict(self):
        doc = {
            'name': self.name,
            'artist': self.artist,
            'album': self.album,
            'genre': self.genre,
            'year': self.year
        }
        if self._id:
            doc['_id'] = self._id
        return doc
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            artist=data['artist'],
            album=data.get('album'),
            genre=data.get('genre'),
            year=data.get('year'),
            _id=data.get('_id')
        )
    
    def __str__(self):
        parts = [f"{self.name} - {self.artist}"]
        if self.album:
            parts.append(f"Album: {self.album}")
        if self.genre:
            parts.append(f"Genre: {self.genre}")
        if self.year:
            parts.append(f"Jahr: {self.year}")
        return " | ".join(parts)

class JukeboxManager:
    def __init__(self, connection_string=None):
        if connection_string is None:
            connection_string = os.getenv('MONGODB_URI', 'mongodb://192.168.1.157:27017/')
        
        self.client = MongoClient(connection_string)
        self.db = self.client['jukebox']
        self.collection = self.db['songs']
        print("✓ Jukebox Management bereit")
    
    def add_song(self, song):
        result = self.collection.insert_one(song.to_dict())
        print(f"✓ Song hinzugefügt: {song.name}")
        return result.inserted_id
    
    def search_songs(self, name=None, artist=None, album=None, genre=None):
        query = {}
        
        if name:
            query['name'] = {'$regex': re.escape(name), '$options': 'i'}
        if artist:
            query['artist'] = {'$regex': re.escape(artist), '$options': 'i'}
        if album:
            query['album'] = {'$regex': re.escape(album), '$options': 'i'}
        if genre:
            query['genre'] = {'$regex': re.escape(genre), '$options': 'i'}
        
        cursor = self.collection.find(query)
        return [Song.from_dict(doc) for doc in cursor]
    
    def update_song(self, song_id, updated_song):
        if isinstance(song_id, str):
            song_id = ObjectId(song_id)
        
        result = self.collection.update_one(
            {'_id': song_id},
            {'$set': updated_song.to_dict()}
        )
        return result.modified_count > 0
    
    def delete_song(self, song_id):
        if isinstance(song_id, str):
            song_id = ObjectId(song_id)
        
        result = self.collection.delete_one({'_id': song_id})
        return result.deleted_count > 0
    
    def get_all_songs(self):
        cursor = self.collection.find()
        return [Song.from_dict(doc) for doc in cursor]

class JukeboxPlayer:
    def __init__(self, connection_string=None):
        if connection_string is None:
            connection_string = os.getenv('MONGODB_URI', 'mongodb://192.168.1.157:27017/')
        
        self.client = MongoClient(connection_string)
        self.db = self.client['jukebox']
        self.collection = self.db['songs']
        self.playlist = []
        print("✓ Jukebox Player bereit")
    
    def search_songs(self, name=None, artist=None, album=None, genre=None):
        query = {}
        
        if name:
            query['name'] = {'$regex': re.escape(name), '$options': 'i'}
        if artist:
            query['artist'] = {'$regex': re.escape(artist), '$options': 'i'}
        if album:
            query['album'] = {'$regex': re.escape(album), '$options': 'i'}
        if genre:
            query['genre'] = {'$regex': re.escape(genre), '$options': 'i'}
        
        cursor = self.collection.find(query)
        return [Song.from_dict(doc) for doc in cursor]
    
    def add_to_playlist(self, song):
        self.playlist.append(song)
        print(f"✓ Zur Playlist hinzugefügt: {song.name}")
    
    def play_next(self):
        if self.playlist:
            song = self.playlist.pop(0)
            print(f"♪ Spielt: {song}")
            return song
        else:
            random_song = self.get_random_song()
            if random_song:
                print(f"♪ Zufällig gespielt: {random_song}")
                return random_song
            else:
                print("Keine Songs verfügbar")
                return None
    
    def get_random_song(self):
        count = self.collection.count_documents({})
        if count == 0:
            return None
        
        random_skip = random.randint(0, count - 1)
        cursor = self.collection.find().skip(random_skip).limit(1)
        doc = next(cursor, None)
        return Song.from_dict(doc) if doc else None
    
    def show_playlist(self):
        if not self.playlist:
            print("Playlist ist leer")
            return
        
        print(f"\nPlaylist ({len(self.playlist)} Songs):")
        for i, song in enumerate(self.playlist, 1):
            print(f"{i}. {song}")

def management_interface():
    print("\nJukebox Management")
    print("=" * 18)
    
    manager = JukeboxManager()
    
    while True:
        print("\nManagement Optionen:")
        print("1. Song hinzufügen")
        print("2. Songs suchen")
        print("3. Song bearbeiten")
        print("4. Song löschen")
        print("5. Alle Songs anzeigen")
        print("6. Zurück")
        
        choice = input("\nWählen (1-6): ").strip()
        
        if choice == "1":
            name = input("Song Name: ").strip()
            artist = input("Interpret: ").strip()
            
            if not name or not artist:
                print("Name und Interpret sind erforderlich")
                continue
            
            album = input("Album (optional): ").strip() or None
            genre = input("Genre (optional): ").strip() or None
            year_input = input("Jahr (optional): ").strip()
            year = int(year_input) if year_input.isdigit() else None
            
            song = Song(name, artist, album, genre, year)
            manager.add_song(song)
        
        elif choice == "2":
            name = input("Name suchen (optional): ").strip() or None
            artist = input("Interpret suchen (optional): ").strip() or None
            album = input("Album suchen (optional): ").strip() or None
            genre = input("Genre suchen (optional): ").strip() or None
            
            results = manager.search_songs(name, artist, album, genre)
            
            print(f"\n{len(results)} Song(s) gefunden:")
            for i, song in enumerate(results, 1):
                print(f"{i}. {song} (ID: {song._id})")
        
        elif choice == "3":
            song_id = input("Song ID eingeben: ").strip()
            songs = manager.search_songs()
            song = next((s for s in songs if str(s._id) == song_id), None)
            
            if not song:
                print("Song nicht gefunden")
                continue
            
            print(f"Aktueller Song: {song}")
            
            name = input(f"Neuer Name ({song.name}): ").strip() or song.name
            artist = input(f"Neuer Interpret ({song.artist}): ").strip() or song.artist
            album = input(f"Neues Album ({song.album}): ").strip() or song.album
            genre = input(f"Neues Genre ({song.genre}): ").strip() or song.genre
            year_input = input(f"Neues Jahr ({song.year}): ").strip()
            year = int(year_input) if year_input.isdigit() else song.year
            
            updated_song = Song(name, artist, album, genre, year)
            
            if manager.update_song(song_id, updated_song):
                print("✓ Song aktualisiert")
            else:
                print("Fehler beim Aktualisieren")
        
        elif choice == "4":
            song_id = input("Song ID zum Löschen: ").strip()
            
            if manager.delete_song(song_id):
                print("✓ Song gelöscht")
            else:
                print("Fehler beim Löschen")
        
        elif choice == "5":
            songs = manager.get_all_songs()
            print(f"\nAlle Songs ({len(songs)} total):")
            for song in songs:
                print(f"- {song} (ID: {song._id})")
        
        elif choice == "6":
            break

def player_interface():
    print("\nJukebox Player")
    print("=" * 14)
    
    player = JukeboxPlayer()
    
    while True:
        print("\nPlayer Optionen:")
        print("1. Songs suchen")
        print("2. Zur Playlist hinzufügen")
        print("3. Nächsten Song spielen")
        print("4. Playlist anzeigen")
        print("5. Zufälligen Song spielen")
        print("6. Zurück")
        
        choice = input("\nWählen (1-6): ").strip()
        
        if choice == "1":
            name = input("Name suchen (optional): ").strip() or None
            artist = input("Interpret suchen (optional): ").strip() or None
            album = input("Album suchen (optional): ").strip() or None
            genre = input("Genre suchen (optional): ").strip() or None
            
            results = player.search_songs(name, artist, album, genre)
            
            print(f"\n{len(results)} Song(s) gefunden:")
            for i, song in enumerate(results, 1):
                print(f"{i}. {song}")
            
            if results:
                choice = input("\nNummer zur Playlist hinzufügen (oder Enter): ").strip()
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(results):
                        player.add_to_playlist(results[idx])
        
        elif choice == "2":
            songs = player.search_songs()
            print(f"\nAlle Songs ({len(songs)} verfügbar):")
            for i, song in enumerate(songs[:20], 1):
                print(f"{i}. {song}")
            
            choice = input("\nNummer zur Playlist hinzufügen: ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(songs):
                    player.add_to_playlist(songs[idx])
        
        elif choice == "3":
            player.play_next()
        
        elif choice == "4":
            player.show_playlist()
        
        elif choice == "5":
            song = player.get_random_song()
            if song:
                print(f"♪ Zufälliger Song: {song}")
        
        elif choice == "6":
            break

def setup_demo_data():
    print("Demo Daten einrichten...")
    
    manager = JukeboxManager()
    
    demo_songs = [
        Song("Another Brick in the Wall", "Pink Floyd", "The Wall", "Rock", 1979),
        Song("Get Back", "The Beatles", "Let It Be", "Rock", 1970),
        Song("I'll Be Back", "The Beatles", "A Hard Day's Night", "Pop", 1964),
        Song("Bohemian Rhapsody", "Queen", "A Night at the Opera", "Rock", 1975),
        Song("Hotel California", "Eagles", "Hotel California", "Rock", 1976),
        Song("Imagine", "John Lennon", "Imagine", "Pop", 1971),
        Song("Stairway to Heaven", "Led Zeppelin", "Led Zeppelin IV", "Rock", 1971),
    ]
    
    for song in demo_songs:
        manager.add_song(song)
    
    print(f"✓ {len(demo_songs)} Demo Songs hinzugefügt")

def main():
    print("Jukebox System")
    print("=" * 14)
    
    while True:
        print("\nHauptmenü:")
        print("1. Management")
        print("2. Player")
        print("3. Demo Daten einrichten")
        print("4. Beenden")
        
        choice = input("\nWählen (1-4): ").strip()
        
        if choice == "1":
            management_interface()
        elif choice == "2":
            player_interface()
        elif choice == "3":
            setup_demo_data()
        elif choice == "4":
            print("Tschüss!")
            break
        else:
            print("Ungültige Option")

if __name__ == "__main__":
    main()
