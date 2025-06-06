from buch import Buch
from pymongo import MongoClient

# MongoDB Verbindung
client = MongoClient("mongodb://localhost:27017/")
db = client['bib']['books']

# Bücher erstellen
buecher = [
    Buch("The subtle art of not giving a f*ck", "Mark Manson", "978-3-442-17722-0", 20.00),
    Buch("Atomic Habits", "James Clear", "978-3-442-17722-1", 25.00)
]

# In DB speichern
for buch in buecher:
    print(buch)
    db.insert_one(buch.__dict__)

print(f"Bücher gespeichert: {len(buecher)}")
