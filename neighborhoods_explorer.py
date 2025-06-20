#!/usr/bin/env python3
"""
Neighborhoods-Collection Explorer für Aufgabe 8
Analysiert die Struktur und den Inhalt der neighborhoods-Collection
"""

from pymongo import MongoClient
import os
import json
from pprint import pprint

def explore_neighborhoods():
    # MongoDB-Verbindung
    connection_string = os.getenv('MONGODB_URI', 'mongodb://192.168.1.157:27017/')
    client = MongoClient(connection_string)
    
    # Database und Collection auswählen
    db = client['restaurants']
    collection = db['neighborhoods']
    
    print("=== NEIGHBORHOODS COLLECTION EXPLORER ===")
    print()
    
    # 1. Anzahl der Dokumente
    doc_count = collection.count_documents({})
    print(f"Anzahl der Dokumente: {doc_count}")
    print()
    
    # 2. Ein Beispieldokument anzeigen
    print("=== BEISPIELDOKUMENT ===")
    sample_doc = collection.find_one()
    if sample_doc:
        pprint(sample_doc, width=80)
    print()
    
    # 3. Struktur-Analyse
    print("=== STRUKTUR-ANALYSE ===")
    if sample_doc:
        print("Feldnamen:")
        for key in sample_doc.keys():
            print(f"  - {key}: {type(sample_doc[key]).__name__}")
        print()
        
        # Geometrie-Details falls vorhanden
        if 'geometry' in sample_doc:
            geom = sample_doc['geometry']
            print("Geometrie-Details:")
            print(f"  Type: {geom.get('type', 'N/A')}")
            if 'coordinates' in geom:
                coords = geom['coordinates']
                print(f"  Koordinaten-Typ: {type(coords).__name__}")
                if isinstance(coords, list) and len(coords) > 0:
                    print(f"  Anzahl Koordinaten-Arrays: {len(coords)}")
                    if isinstance(coords[0], list) and len(coords[0]) > 0:
                        print(f"  Erstes Koordinaten-Array Länge: {len(coords[0])}")
                        print(f"  Beispiel-Koordinate: {coords[0][0] if coords[0] else 'N/A'}")
    
    # 4. Alle Neighborhood-Namen auflisten
    print("=== ALLE NEIGHBORHOODS ===")
    neighborhoods = collection.find({}, {'name': 1}).sort('name', 1)
    for i, neighborhood in enumerate(neighborhoods, 1):
        name = neighborhood.get('name', 'Unbekannt')
        print(f"{i:2d}. {name}")
    
    print()
    print("=== ANALYSE ABGESCHLOSSEN ===")
    
    client.close()
    return doc_count, sample_doc

if __name__ == "__main__":
    explore_neighborhoods()
