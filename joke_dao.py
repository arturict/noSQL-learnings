#!/usr/bin/env python3
from pymongo import MongoClient
from bson import ObjectId
import os

class Joke:
    def __init__(self, text, category, author, _id=None):
        self._id = _id
        self.text = text
        self.category = category if isinstance(category, list) else [category]
        self.author = author
    
    def to_dict(self):
        doc = {
            'text': self.text,
            'category': self.category,
            'author': self.author
        }
        if self._id:
            doc['_id'] = self._id
        return doc
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            text=data['text'],
            category=data['category'],
            author=data['author'],
            _id=data.get('_id')
        )
    
    def __str__(self):
        return f"{self.text} - {self.author} ({', '.join(self.category)})"

class JokeDAO:
    def __init__(self, connection_string=None):
        if connection_string is None:
            connection_string = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        
        self.client = MongoClient(connection_string)
        self.db = self.client['jokes_db']
        self.collection = self.db['jokes']
        print("✓ Verbunden mit Jokes Datenbank")
    
    def insert(self, joke):
        result = self.collection.insert_one(joke.to_dict())
        return result.inserted_id
    
    def get_category(self, category):
        cursor = self.collection.find({'category': category})
        return [Joke.from_dict(doc) for doc in cursor]
    
    def delete(self, joke_id):
        if isinstance(joke_id, str):
            joke_id = ObjectId(joke_id)
        result = self.collection.delete_one({'_id': joke_id})
        return result.deleted_count > 0
    
    def update(self, joke_id, updated_joke):
        if isinstance(joke_id, str):
            joke_id = ObjectId(joke_id)
        result = self.collection.update_one(
            {'_id': joke_id},
            {'$set': updated_joke.to_dict()}
        )
        return result.modified_count > 0
    
    def get_all(self):
        cursor = self.collection.find()
        return [Joke.from_dict(doc) for doc in cursor]

def main():
    print("Joke DAO Test")
    print("=" * 15)
    
    dao = JokeDAO()
    
    jokes = [
        Joke("Warum nehmen Geister keine Drogen? Weil sie schon high sind!", ["Geister", "Wortspiel"], "Anonymous"),
        Joke("Was ist grün und klopft an der Tür? Ein Klopfsalat!", ["Wortspiel", "Essen"], "Dad"),
        Joke("Warum können Geister so schlecht lügen? Weil man durch sie hindurchsehen kann!", ["Geister"], "Anonymous")
    ]
    
    print("\nJokes einfügen...")
    for joke in jokes:
        joke_id = dao.insert(joke)
        print(f"✓ Eingefügt: {joke_id}")
    
    print("\nGeister-Jokes:")
    geister_jokes = dao.get_category("Geister")
    for joke in geister_jokes:
        print(f"- {joke}")
    
    print("\nAlle Jokes:")
    all_jokes = dao.get_all()
    for joke in all_jokes:
        print(f"- {joke} (ID: {joke._id})")

if __name__ == "__main__":
    main()
