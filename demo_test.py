#!/usr/bin/env python3
"""
Demo Test für Database Explorer und Restaurant CRUD Funktionen
Dieser Test zeigt die Funktionen in der Konsole und erstellt Output zum Kopieren
"""

import os
import sys
from database_explorer import DatabaseExplorer
from restaurant_crud import RestaurantManager

def test_database_explorer():
    print("=" * 60)
    print("DATABASE EXPLORER DEMO")
    print("=" * 60)
    
    connection_string = os.getenv('MONGODB_URI', 'mongodb://192.168.1.157:27017/')
    
    try:
        explorer = DatabaseExplorer(connection_string)
        
        # Liste alle Datenbanken
        print("\n1. DATENBANKEN AUFLISTEN:")
        print("-" * 30)
        databases = explorer.list_databases()
        print("Databases")
        for db in databases:
            print(f" - {db}")
        
        # Zeige Collections für die erste verfügbare DB
        if databases:
            test_db = databases[0]  # Nimm die erste DB
            print(f"\n2. COLLECTIONS IN '{test_db}':")
            print("-" * 30)
            collections = explorer.list_collections(test_db)
            print(f"{test_db}")
            print("\nCollections")
            for col in collections:
                print(f" - {col}")
            
            # Zeige Documents für die erste Collection
            if collections:
                test_col = collections[0]  # Nimm die erste Collection
                print(f"\n3. DOCUMENTS IN '{test_db}.{test_col}':")
                print("-" * 30)
                documents = explorer.list_documents(test_db, test_col)
                print(f"{test_db}.{test_col}")
                print("\nDocuments")
                for doc_id in documents[:5]:  # Zeige nur erste 5 Documents
                    print(f" - {doc_id}")
                
                # Zeige Inhalt des ersten Documents
                if documents:
                    test_doc = documents[0]
                    print(f"\n4. DOCUMENT INHALT '{test_db}.{test_col}.{test_doc}':")
                    print("-" * 30)
                    document = explorer.get_document(test_db, test_col, test_doc)
                    print(f"{test_db}.{test_col}.{test_doc}")
                    print()
                    if document:
                        for key, value in document.items():
                            # Begrenze die Ausgabe für bessere Lesbarkeit
                            if isinstance(value, str) and len(value) > 100:
                                value = value[:100] + "..."
                            print(f"{key}: {value}")
                    print("\nPress any button to return")
        
    except Exception as e:
        print(f"Fehler beim Database Explorer Test: {e}")

def test_restaurant_crud():
    print("\n\n" + "=" * 60)
    print("RESTAURANT CRUD DEMO")
    print("=" * 60)
    
    connection_string = os.getenv('MONGODB_URI', 'mongodb://192.168.1.157:27017/')
    
    try:
        rm = RestaurantManager(connection_string)
        
        # 1. Stadtbezirke anzeigen
        print("\n1. EINZIGARTIGE STADTBEZIRKE:")
        print("-" * 30)
        boroughs = rm.get_unique_boroughs()
        print("Alle Stadtbezirke:")
        for borough in boroughs:
            print(f" - {borough}")
        
        # 2. Top 3 Restaurants
        print("\n2. TOP 3 BEWERTETE RESTAURANTS:")
        print("-" * 30)
        top_restaurants = rm.get_top_rated_restaurants()
        for i, restaurant in enumerate(top_restaurants, 1):
            print(f"{i}. {restaurant['name']} ({restaurant['cuisine']})")
            print(f"   Durchschnittsscore: {restaurant['avg_score']:.2f}")
            print(f"   Stadtbezirk: {restaurant['borough']}")
        
        # 3. Nächstes Restaurant zu Le Perigord
        print("\n3. NÄCHSTES RESTAURANT ZU 'Le Perigord':")
        print("-" * 30)
        nearest = rm.find_nearest_restaurant("Le Perigord")
        if nearest:
            print(f"Nächstes Restaurant: {nearest['name']}")
            print(f"Küche: {nearest['cuisine']}")
            print(f"Stadtbezirk: {nearest['borough']}")
            if 'distance' in nearest:
                print(f"Entfernung: {nearest['distance']} Meter")
        else:
            print("Nächstes Restaurant nicht gefunden")
        
        # 4. Restaurant Suche Demo
        print("\n4. RESTAURANT SUCHE DEMO:")
        print("-" * 30)
        
        # Suche nach "Pizza"
        print("Suche nach Küche 'Pizza':")
        pizza_results = rm.search_restaurants("", "Pizza")
        print(f"{len(pizza_results)} Restaurant(s) gefunden:")
        for i, restaurant in enumerate(pizza_results[:3], 1):  # Zeige nur erste 3
            print(f"{i}. {restaurant['name']} ({restaurant['cuisine']})")
            print(f"   Stadtbezirk: {restaurant['borough']}")
            print(f"   ID: {restaurant['_id']}")
        
        # Suche nach "Steak"
        print("\nSuche nach Name 'Steak':")
        steak_results = rm.search_restaurants("Steak", "")
        print(f"{len(steak_results)} Restaurant(s) gefunden:")
        for i, restaurant in enumerate(steak_results[:3], 1):  # Zeige nur erste 3
            print(f"{i}. {restaurant['name']} ({restaurant['cuisine']})")
            print(f"   Stadtbezirk: {restaurant['borough']}")
            print(f"   ID: {restaurant['_id']}")
        
        # 5. Demo einer Bewertung (ohne tatsächlich zu ändern)
        print("\n5. BEWERTUNG DEMO:")
        print("-" * 30)
        if pizza_results:
            demo_restaurant = pizza_results[0]
            print(f"Demo: Bewertung für '{demo_restaurant['name']}' würde hinzugefügt werden")
            print(f"Restaurant ID: {demo_restaurant['_id']}")
            print("Score: 85 (Demo-Wert)")
            print("Datum: Aktuelles Datum")
            print("Status: Demo-Modus - keine tatsächliche Änderung")
        
    except Exception as e:
        print(f"Fehler beim Restaurant CRUD Test: {e}")

def main():
    print("MONGODB FUNKTIONEN DEMO TEST")
    print("Dieser Test zeigt die implementierten Funktionen")
    print("Output kann kopiert werden für Dokumentation")
    
    # Database Explorer Test
    test_database_explorer()
    
    # Restaurant CRUD Test  
    test_restaurant_crud()
    
    print("\n\n" + "=" * 60)
    print("DEMO BEENDET")
    print("=" * 60)
    print("Alle Funktionen wurden demonstriert.")
    print("Output kann jetzt kopiert werden.")

if __name__ == "__main__":
    main()
