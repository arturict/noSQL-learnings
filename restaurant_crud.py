#!/usr/bin/env python3
from pymongo import MongoClient
from datetime import datetime
import re
import os

class RestaurantManager:
    def __init__(self, connection_string, database_name="restaurants", collection_name="restaurants"):
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
        print(f"Verbunden mit {database_name}.{collection_name}")
    
    def get_unique_boroughs(self):
        boroughs = self.collection.distinct("borough")
        return sorted(boroughs)
    
    def get_top_rated_restaurants(self, limit=3):
        pipeline = [
            {"$unwind": "$grades"},
            {"$group": {
                "_id": "$_id",
                "name": {"$first": "$name"},
                "cuisine": {"$first": "$cuisine"},
                "borough": {"$first": "$borough"},
                "avg_score": {"$avg": "$grades.score"}
            }},
            {"$sort": {"avg_score": -1}},
            {"$limit": limit}
        ]
        
        return list(self.collection.aggregate(pipeline))
    
    def find_nearest_restaurant(self, target_restaurant_name):
        target = self.collection.find_one({"name": target_restaurant_name})
        
        if not target or "address" not in target or "coord" not in target["address"]:
            print(f"Restaurant '{target_restaurant_name}' nicht gefunden oder keine Koordinaten")
            return None
        
        target_coords = target["address"]["coord"]
        
        pipeline = [
            {
                "$geoNear": {
                    "near": {
                        "type": "Point",
                        "coordinates": target_coords
                    },
                    "distanceField": "distance",
                    "spherical": True,
                    "query": {"name": {"$ne": target_restaurant_name}}
                }
            },
            {"$limit": 1}
        ]
        
        result = list(self.collection.aggregate(pipeline))
        return result[0] if result else None
    
    def search_restaurants(self, name_query="", cuisine_query=""):
        query = {}
        
        if name_query.strip():
            query["name"] = {"$regex": re.escape(name_query), "$options": "i"}
        
        if cuisine_query.strip():
            query["cuisine"] = {"$regex": re.escape(cuisine_query), "$options": "i"}
        
        if not query:
            return []
        
        return list(self.collection.find(query))
    
    def add_rating(self, restaurant_id, score, grade="A"):
        new_grade = {
            "date": datetime.now(),
            "grade": grade,
            "score": score
        }
        
        result = self.collection.update_one(
            {"_id": restaurant_id},
            {"$push": {"grades": new_grade}}
        )
        
        return result.modified_count > 0

def main():
    connection_string = os.getenv('MONGODB_URI', 'mongodb://192.168.1.157:27017/')
    
    rm = RestaurantManager(connection_string)
    
    while True:
        print("\n" + "="*50)
        print("RESTAURANT DATENBANK OPERATIONEN")
        print("="*50)
        print("1. Alle einzigartigen Stadtbezirke anzeigen")
        print("2. Top 3 bewertete Restaurants anzeigen")
        print("3. Nächstes Restaurant zu 'Le Perigord' finden")
        print("4. Restaurants suchen")
        print("5. Bewertung zu Restaurant hinzufügen")
        print("6. Beenden")
        
        choice = input("\nOption wählen (1-6): ").strip()
        
        if choice == "1":
            print("\nEinzigartige Stadtbezirke:")
            boroughs = rm.get_unique_boroughs()
            for borough in boroughs:
                print(f" - {borough}")
        
        elif choice == "2":
            print("\nTop 3 bewertete Restaurants:")
            top_restaurants = rm.get_top_rated_restaurants()
            for i, restaurant in enumerate(top_restaurants, 1):
                print(f"{i}. {restaurant['name']} ({restaurant['cuisine']})")
                print(f"   Durchschnittsscore: {restaurant['avg_score']:.2f}")
                print(f"   Stadtbezirk: {restaurant['borough']}")
        
        elif choice == "3":
            print("\nNächstes Restaurant zu 'Le Perigord' finden...")
            nearest = rm.find_nearest_restaurant("Le Perigord")
            if nearest:
                print(f"Nächstes Restaurant: {nearest['name']}")
                print(f"Küche: {nearest['cuisine']}")
                print(f"Entfernung: {nearest.get('distance', 'N/A')} Meter")
            else:
                print("Nächstes Restaurant nicht gefunden")
        
        elif choice == "4":
            print("\nRestaurant Suche")
            name_query = input("Name eingeben (oder leer lassen): ").strip()
            cuisine_query = input("Küche eingeben (oder leer lassen): ").strip()
            
            if not name_query and not cuisine_query:
                print("Bitte mindestens ein Suchkriterium angeben")
                continue
            
            results = rm.search_restaurants(name_query, cuisine_query)
            
            print(f"\n{len(results)} Restaurant(s) gefunden:")
            for i, restaurant in enumerate(results, 1):
                print(f"{i}. {restaurant['name']} ({restaurant['cuisine']})")
                print(f"   Stadtbezirk: {restaurant['borough']}")
                print(f"   ID: {restaurant['_id']}")
            
            # Restaurant aus Suchergebnissen bewerten
            if results:
                choice = input("\nNummer eingeben um Restaurant zu bewerten (oder Enter um zu überspringen): ").strip()
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(results):
                        selected_restaurant = results[idx]
                        score = input("Score eingeben (0-100): ").strip()
                        if score.isdigit():
                            score = int(score)
                            if 0 <= score <= 100:
                                if rm.add_rating(selected_restaurant['_id'], score):
                                    print(f"Bewertung erfolgreich zu {selected_restaurant['name']} hinzugefügt")
                                else:
                                    print("Bewertung hinzufügen fehlgeschlagen")
        
        elif choice == "5":
            print("\nBewertung zu Restaurant hinzufügen")
            restaurant_id = input("Restaurant ID eingeben: ").strip()
            score = input("Score eingeben (0-100): ").strip()
            
            if score.isdigit():
                score = int(score)
                if 0 <= score <= 100:
                    if rm.add_rating(restaurant_id, score):
                        print("Bewertung erfolgreich hinzugefügt!")
                    else:
                        print("Bewertung hinzufügen fehlgeschlagen")
        
        elif choice == "6":
            print("Auf Wiedersehen!")
            break
        
        else:
            print("Ungültige Option. Bitte erneut versuchen.")

if __name__ == "__main__":
    main()
