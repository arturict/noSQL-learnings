# Aufgabe 1: 
from pymongo import MongoClient

connection_string = "mongodb://192.168.1.157:27017/"
client = MongoClient(connection_string)

print(client.server_info()) 

# Aufgabe 2:

Ausgabe:
<details>
<summary>Details anzeigen</summary>

**Datenbanken:**
- file_storage
- jokes_db
- jukebox
- restaurants
- system_monitoring
- test_database

**Ausgewählte Datenbank:** jukebox

**Collections:**
- songs

**Ausgewählte Collection:** songs

**Dokumente:**
- 6842b4dbe97494bfdb007b82
- 6842b4dbe97494bfdb007b83
- 6842b4dbe97494bfdb007b84

**Ausgewähltes Dokument:** 6842b4dbe97494bfdb007b82

- _id: 6842b4dbe97494bfdb007b82
- name: Bohemian Rhapsody
- artist: Queen
- album: A Night at the Opera
- genre: Rock
- year: 1975

</details>



Ausgabe 2. Fall:
<details>
<summary>Details anzeigen</summary>

**Datenbanken:**
- file_storage
- jokes_db
- jukebox
- restaurants
- system_monitoring
- test_database

**Datenbank auswählen:** hallo  
Datenbank 'hallo' nicht gefunden

**Datenbanken:**
- file_storage
- jokes_db
- jukebox
- restaurants
- system_monitoring
- test_database

**Datenbank auswählen:** 
</details>

# Aufgabe 3:

## Ausgabe:
<details>

==================================================
RESTAURANT DATENBANK OPERATIONEN
==================================================
1. Alle einzigartigen Stadtbezirke anzeigen
2. Top 3 bewertete Restaurants anzeigen
3. Nächstes Restaurant zu 'Le Perigord' finden
4. Restaurants suchen
5. Bewertung zu Restaurant hinzufügen
6. Beenden

Option wählen (1-6): 1

Einzigartige Stadtbezirke:
 - Bronx
 - Brooklyn
 - Manhattan
 - Missing
 - Queens
 - Staten Island

==================================================
RESTAURANT DATENBANK OPERATIONEN
==================================================
1. Alle einzigartigen Stadtbezirke anzeigen
2. Top 3 bewertete Restaurants anzeigen
3. Nächstes Restaurant zu 'Le Perigord' finden
4. Restaurants suchen
5. Bewertung zu Restaurant hinzufügen
6. Beenden

Option wählen (1-6): 2

Top 3 bewertete Restaurants:
1. Juice It Health Bar (Juice, Smoothies, Fruit Salads)
   Durchschnittsscore: 75.00
   Stadtbezirk: Brooklyn
2. Golden Dragon Cuisine (Chinese)
   Durchschnittsscore: 73.00
   Stadtbezirk: Bronx
3. Chelsea'S Juice Factory (Juice, Smoothies, Fruit Salads)
   Durchschnittsscore: 69.00
   Stadtbezirk: Brooklyn

==================================================
RESTAURANT DATENBANK OPERATIONEN
==================================================
1. Alle einzigartigen Stadtbezirke anzeigen
2. Top 3 bewertete Restaurants anzeigen
3. Nächstes Restaurant zu 'Le Perigord' finden
4. Restaurants suchen
5. Bewertung zu Restaurant hinzufügen
6. Beenden

Option wählen (1-6): 3

Nächstes Restaurant zu 'Le Perigord' finden...
Nächstes Restaurant: Subway
Küche: Sandwiches
Entfernung: 55.29977412262775 Meter
</details>

## Ausgabe 2:
<details>
==================================================
RESTAURANT DATENBANK OPERATIONEN
==================================================
1. Alle einzigartigen Stadtbezirke anzeigen
2. Top 3 bewertete Restaurants anzeigen
3. Nächstes Restaurant zu 'Le Perigord' finden
4. Restaurants suchen
5. Bewertung zu Restaurant hinzufügen
6. Beenden

Option wählen (1-6): 4

Restaurant Suche
Name eingeben (oder leer lassen): Mcdonald'S 
Küche eingeben (oder leer lassen): Burger

181 Restaurant(s) gefunden:
1. Mcdonald'S (Hamburgers)
   Stadtbezirk: Queens
   ID: 5eb3d668b31de5d588f429f9
2. Mcdonald'S (Hamburgers)
   Stadtbezirk: Brooklyn
   ID: 5eb3d668b31de5d588f42a07
3. Mcdonald'S (Hamburgers)
   Stadtbezirk: Brooklyn
   ID: 5eb3d668b31de5d588f42a2f
4. Mcdonald'S (Hamburgers)
   Stadtbezirk: Queens
   ID: 5eb3d668b31de5d588f42a3c
5. Mcdonald'S (Hamburgers)
   Stadtbezirk: Brooklyn
   ID: 5eb3d668b31de5d588f42a43
...
173. Mcdonald'S (Hamburgers)
   Stadtbezirk: Queens
   ID: 5eb3d669b31de5d588f479b0
174. Mcdonald'S (Hamburgers)
   Stadtbezirk: Queens
   ID: 5eb3d669b31de5d588f479b1
175. Mcdonald'S (Hamburgers)
   Stadtbezirk: Queens
   ID: 5eb3d669b31de5d588f47c7d
176. Mcdonald'S (Hamburgers)
   Stadtbezirk: Queens
   ID: 5eb3d669b31de5d588f47c83
177. Mcdonald'S (Hamburgers)
   Stadtbezirk: Queens
   ID: 5eb3d669b31de5d588f480dc
178. Mcdonald'S  (Hamburgers)
   Stadtbezirk: Queens
   ID: 5eb3d669b31de5d588f480f9
179. Mcdonald'S (Hamburgers)
   Stadtbezirk: Queens
   ID: 5eb3d669b31de5d588f488ac
180. Mcdonald'S (Hamburgers)
   Stadtbezirk: Brooklyn
   ID: 5eb3d669b31de5d588f488ad
181. Mcdonald'S (Hamburgers)
   Stadtbezirk: Queens
   ID: 5eb3d669b31de5d588f48b05

Nummer eingeben um Restaurant zu bewerten (oder Enter um zu überspringen): 181
Score eingeben (0-100): 69
Bewertung erfolgreich zu Mcdonald'S hinzugefügt

==================================================
RESTAURANT DATENBANK OPERATIONEN
==================================================
1. Alle einzigartigen Stadtbezirke anzeigen
2. Top 3 bewertete Restaurants anzeigen
3. Nächstes Restaurant zu 'Le Perigord' finden
4. Restaurants suchen
5. Bewertung zu Restaurant hinzufügen
6. Beenden

Option wählen (1-6): 5

Bewertung zu Restaurant hinzufügen
Methode wählen:
1. Restaurant ID eingeben
2. Restaurant suchen und bewerten
Methode (1-2): 1
Restaurant ID eingeben: 5eb3d669b31de5d588f480f9
Score eingeben (0-100): 70
Bewertung erfolgreich hinzugefügt!

==================================================
RESTAURANT DATENBANK OPERATIONEN
==================================================
1. Alle einzigartigen Stadtbezirke anzeigen
2. Top 3 bewertete Restaurants anzeigen
3. Nächstes Restaurant zu 'Le Perigord' finden
4. Restaurants suchen
5. Bewertung zu Restaurant hinzufügen
6. Beenden

Option wählen (1-6): 
</details>

# Aufgabe 4
[Quellcode zu Aufgabe 2 und Lösung zu Aufgabe 4: database_explorer.py](./database_explorer.py)


# Aufgabe 5
[Quellcode zu Aufgabe 5: power_monitor.py](./power_monitor.py)
<details>
Power Monitor
===============
✓ Verbunden mit MongoDB: system_monitoring.power_stats
CPU Kerne: 4
RAM: 15.6 GB
Logs: 40

Überwachung gestartet (Strg+C zum Stoppen)
Power Überwachung gestartet (Intervall: 1s, max logs: 10000)
Strg+C zum Stoppen
[08:39:22] Power Stats [2025-06-20 08:39:22]: CPU: 1.2%, RAM: 1.8GB / 15.6GB (11.8%)
[08:39:24] Power Stats [2025-06-20 08:39:24]: CPU: 0.8%, RAM: 1.9GB / 15.6GB (11.9%)
[08:39:26] Power Stats [2025-06-20 08:39:26]: CPU: 0.5%, RAM: 1.8GB / 15.6GB (11.8%)
[08:39:28] Power Stats [2025-06-20 08:39:28]: CPU: 0.2%, RAM: 1.8GB / 15.6GB (11.8%)
^CTraceback (most recent call last):
  File "/home/artur/schule/jahr_2/sem_2/m165_adrian/power_monitor.py", line 130, in <module>
    main()
  File "/home/artur/schule/jahr_2/sem_2/m165_adrian/power_monitor.py", line 127, in main
    monitor.start_monitoring(interval=1)
  File "/home/artur/schule/jahr_2/sem_2/m165_adrian/power_monitor.py", line 94, in start_monitoring
    time.sleep(interval)
KeyboardInterrupt
</details>

# Aufgabe 6
[Quellcode zu Aufgabe 6: joke_dao.py](./joke_dao.py)

# Aufgabe 7
[Quellcode zu Aufgabe 7: gridfs_demo.py](./gridfs_demo.py)

## GridFS Demo Ausgabe:
<details>
<summary>Details anzeigen</summary>

```
GridFS File Storage Demo
=========================
✓ GridFS File Manager bereit
✓ Datei gespeichert: test.txt (ID: 685523409483863a15d1b0e3)
✓ Datei wiederhergestellt: /tmp/restored_test.txt

Gespeicherte Dateien:
- test.txt (ID: 685520890fcecc6118662f65, Größe: 54 bytes)
  Metadaten: {'test': True, 'author': 'Demo'}

GridFS Collections:
- fs.files
- fs.chunks

fs.files Collection Struktur:
  _id: 685520890fcecc6118662f65
  filename: test.txt
  metadata: {'test': True, 'author': 'Demo'}
  chunkSize: 261120
  length: 54
  uploadDate: 2025-06-20 08:49:13.964000
```
</details>

## Fotoalbum Demo Ausgabe:
<details>
<summary>Details anzeigen</summary>

```
Fotoalbum Demo
===============
✓ Fotoalbum bereit
✓ Foto zu Album 'Urlaub 2025' hinzugefügt: vacation1.jpg
✓ Foto zu Album 'Urlaub 2025' hinzugefügt: vacation2.jpg
✓ Foto zu Album 'Familie' hinzugefügt: family1.jpg

Verfügbare Alben:

Album 'Familie':
- family1.jpg: Familienfeier

Album 'Urlaub 2025':
- vacation1.jpg: Strand bei Sonnenuntergang
- vacation2.jpg: Hotel am Meer
```
</details>

# Aufgabe 8
[Quellcode zu Aufgabe 8: polygon_visualizer.py](./polygon_visualizer.py)

## Ausgabe:
<details>
<summary>Details anzeigen</summary>

```
=== NEIGHBORHOODS COLLECTION EXPLORER ===
Anzahl der Dokumente: 195

Beispiel Neighborhood:
Name: Bedford
Geometry Type: Polygon
Anzahl Eckpunkte: 123

Visualisierung von 10 Neighborhoods:
✓ Übersicht gespeichert: test_overview_10.png

Manhattan Neighborhoods (15 gefunden):
- Battery Park City-Lower Manhattan
- DUMBO-Vinegar Hill-Downtown Brooklyn-Boerum Hill
- Marble Hill-Inwood
- SoHo-TriBeCa-Civic Center-Little Italy
...

Statistiken:
Durchschnittliche Eckpunkte: 336.5
Min/Max Eckpunkte: 54 / 4649
Komplexestes Neighborhood: Hammels-Arverne-Edgemere (4649 Punkte)
```
</details>

# Aufgabe 9
[Quellcode zu Aufgabe 9: jukebox.py](./jukebox.py)

## Ausgabe:
<details>
<summary>Details anzeigen</summary>

```
=== JUKEBOX DEMO ===
✓ Jukebox Management bereit
✓ 7 Demo Songs hinzugefügt

Alle Songs:
1. Bohemian Rhapsody - Queen | Album: A Night at the Opera | Genre: Rock | Jahr: 1975
2. Hotel California - Eagles | Album: Hotel California | Genre: Rock | Jahr: 1976
3. Imagine - John Lennon | Album: Imagine | Genre: Pop | Jahr: 1971
4. Another Brick in the Wall - Pink Floyd | Album: The Wall | Genre: Rock | Jahr: 1979
5. Get Back - The Beatles | Album: Let It Be | Genre: Rock | Jahr: 1970

Suche nach "Brick":
- Another Brick in the Wall - Pink Floyd | Album: The Wall | Genre: Rock | Jahr: 1979

Player Demo:
✓ Jukebox Player bereit

Suche nach "Beatles":
- Get Back - The Beatles | Album: Let It Be | Genre: Rock | Jahr: 1970
✓ Zur Playlist hinzugefügt: Get Back
- I'll Be Back - The Beatles | Album: A Hard Day's Night | Genre: Pop | Jahr: 1964
✓ Zur Playlist hinzugefügt: I'll Be Back

Songs abspielen:
♪ Spielt: Get Back - The Beatles | Album: Let It Be | Genre: Rock | Jahr: 1970
♪ Spielt: I'll Be Back - The Beatles | Album: A Hard Day's Night | Genre: Pop | Jahr: 1964
♪ Zufällig gespielt: Hotel California - Eagles | Album: Hotel California | Genre: Rock | Jahr: 1976
```
</details>

---
### 8. Download-Test
<details>
<summary>Album Download Demo</summary>

```
✓ Fotoalbum bereit
Verfügbare Alben:
- Familie
- Urlaub 2025

Album 'Familie':
- family1.jpg: Familienfeier

Album 'Urlaub 2025':
- vacation1.jpg: Strand bei Sonnenuntergang
- vacation2.jpg: Hotel am Meer

Download Test: Album 'Urlaub 2025' nach /tmp/downloaded_albums
✓ Heruntergeladen: vacation1.jpg
✓ Heruntergeladen: vacation2.jpg
Album 'Urlaub 2025' heruntergeladen nach /tmp/downloaded_albums

Downloaded Dateien:
- vacation1.jpg (42 bytes)
- vacation2.jpg (29 bytes)
```
</details>

---

# Aufgabe 8: Neighborhoods Polygon-Visualisierung ⭐
[Quellcode zu Aufgabe 8: polygon_visualizer.py](./polygon_visualizer.py)

## Übersicht
Untersuchung der neighborhoods-Collection der Restaurant-Datenbank und Erstellung einer umfassenden Polygon-Visualisierungs-Applikation.

## 1. Collection-Analyse

**Durchgeführt mit:** `neighborhoods_explorer.py`

### Erkenntnisse:
- **195 Neighborhoods** in der Collection
- **Polygon-Geometrien** mit Koordinaten im [Longitude, Latitude] Format
- **Komplexe Formen** mit 54-4649 Eckpunkten pro Neighborhood
- **Vollständige NYC-Abdeckung** aller 5 Boroughs

### Beispiel-Struktur:
```json
{
  "_id": ObjectId("55cb9c666c522cafdb053a1a"),
  "name": "Bedford",
  "geometry": {
    "type": "Polygon", 
    "coordinates": [[
      [-73.94193078816193, 40.70072523469547],
      [-73.9443878859649, 40.70042452378256],
      // ... 121 weitere Koordinaten
    ]]
  }
}
```

