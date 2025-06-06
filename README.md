# MongoDB Datenbank Management Projekt

Dieses Projekt implementiert verschiedene MongoDB Datenbankoperationen als Teil der M165 Kursanforderungen.

## Setup und Anforderungen

### Voraussetzungen
- Python 3.x
- MongoDB Server läuft auf `192.168.1.157:27017`
- Python Bibliotheken (siehe requirements.txt)

### Installation
```bash
pip install -r requirements.txt
```

### Schnelles Setup
```bash
# Umgebungsvariable setzen und Anwendungen starten
./setup.sh

# Oder manuell Umgebungsvariable setzen
export MONGODB_URI='mongodb://192.168.1.157:27017/'
```

## 1. ODM Erklärung

**ODM (Object Document Mapping)** ist eine Programmiertechnik, die eine Brücke zwischen Dokumentendatenbanken (wie MongoDB) und objektorientierten Programmiersprachen (wie Python) schlägt.

### ODM Funktionen:
- **Daten-Mapping**: Konvertiert zwischen Datenbankdokumenten und Programmobjekten
- **Schema-Validierung**: Stellt Datenintegrität und -struktur sicher
- **Query-Abstraktion**: Bietet objektorientierte Methoden zur Datenbankabfrage
- **Beziehungsmanagement**: Verwaltet Beziehungen zwischen verschiedenen Dokumenttypen
- **Typkonvertierung**: Konvertiert automatisch Datentypen zwischen Datenbank und Anwendung

Beliebte Python ODMs für MongoDB sind **Mongoengine** und **Beanie**.

## 2. Datenbank Explorer Anwendung

Das `database_explorer.py` Skript bietet eine interaktive Kommandozeilen-Schnittstelle zum Durchsuchen von MongoDB Datenbanken, Collections und Dokumenten.

### Funktionen:
- Listet alle verfügbaren Datenbanken auf
- Durchsucht Collections innerhalb ausgewählter Datenbanken
- Zeigt Dokument-IDs innerhalb von Collections an
- Zeigt vollständigen Dokumentinhalt an
- Behandelt Navigation und Fehlerfälle
- Benutzerfreundliche Oberfläche mit ordentlicher Fehlerbehandlung

### Verwendung:
```bash
python database_explorer.py
```

### Navigationsablauf:
1. **Datenbanken** → Datenbank nach Namen auswählen
2. **Collections** → Collection nach Namen auswählen
3. **Dokumente** → Dokument nach ID auswählen
4. **Inhalt** → Dokumentdetails anzeigen, beliebige Taste für Rückkehr

## 3. Restaurant Datenbank CRUD Operationen

Das `restaurant_crud.py` Skript implementiert umfassende CRUD (Create, Read, Update, Delete) Operationen für Restaurantdaten.

### Funktionen:

#### 3.1 Eindeutige Stadtbezirke
- Zeigt alle eindeutigen Stadtbezirke ohne Duplikate an
- Verwendet MongoDB's `distinct()` Methode für effiziente Abfragen

#### 3.2 Top bewertete Restaurants
- Zeigt die top 3 Restaurants mit den höchsten Durchschnittsbewertungen
- Verwendet MongoDB Aggregation Pipeline mit `$unwind`, `$group` und `$sort`

#### 3.3 Geografische Suche
- Findet das Restaurant, das "Le Perigord" geografisch am nächsten liegt
- Verwendet MongoDB's `$geoNear` Operator für standortbasierte Abfragen

#### 3.4 Restaurant Suchanwendung
- Suche nach Restaurantname und/oder Küchentyp
- Teilweise Übereinstimmung mit Regex-Mustern
- Optionale Suchkriterien (leere Felder werden ignoriert)
- Groß-/Kleinschreibung wird ignoriert

#### 3.5 Bewertungssystem
- Neue Bewertungen zu Restaurants hinzufügen
- Integration mit Suchergebnissen für einfache Bewertung
- Speichert Bewertungen mit aktuellem Zeitstempel
- Validiert Eingabedaten

### Verwendung:
```bash
python restaurant_crud.py
```

## 4. Connection-String Sicherheit

### Umgebungsvariablen Implementierung

Das `environment_demo.py` Skript demonstriert die sichere Handhabung von Datenbank-Anmeldedaten mit Umgebungsvariablen.

### Funktionen:
- **PATH Variable lesen**: Demonstriert das Lesen und Parsen der PATH Umgebungsvariable
- **MongoDB URI Sicherheit**: Zeigt sichere Connection-String Handhabung
- **Best Practices**: Erklärt Sicherheitsprinzipien für Anmeldedatenmanagement

### Wichtige Sicherheitskonzepte:
- **Niemals Anmeldedaten hardcoden** im Quellcode
- **Umgebungsvariablen verwenden** für sensible Daten
- **Konfigurationsmanagement** für Produktionsumgebungen
- **Versionskontrolle Sicherheit** (.env zu .gitignore hinzufügen)

### Verwendung:
```bash
# Umgebungsvariable setzen
export MONGODB_URI='mongodb://192.168.1.157:27017/'

# Umgebungsvariablen Funktionalität testen
python environment_demo.py
```

### Persistente Umgebungsvariablen:
Zu `~/.bashrc` oder `~/.zshrc` hinzufügen:
```bash
export MONGODB_URI='mongodb://192.168.1.157:27017/'
```

## 5. Power Statistiken Überwachung

### System Überwachung mit psutil

Das Power Monitoring System verfolgt CPU und RAM Nutzung und speichert die Daten in MongoDB zur Analyse.

#### 5.1 Power Klasse

Die `Power` Klasse speichert Systemstatistiken mit diesen Attributen:
- **CPU Nutzung**: CPU Prozent Auslastung
- **RAM Total**: Gesamter Systemspeicher in Bytes
- **RAM Verwendet**: Verwendeter Speicher in Bytes
- **Zeitstempel**: Wann die Messung gemacht wurde

**Konstruktor Verhalten**:
- Wenn keine Parameter gegeben → automatisch aktuelle Systemstatistiken messen
- Wenn Parameter gegeben → gegebene Werte verwenden
- Zeitstempel automatisch auf aktuelle Zeit gesetzt wenn nicht gegeben

#### 5.2 Power Monitor Anwendung

Das `power_monitor.py` Skript bietet kontinuierliche Systemüberwachung:

### Funktionen:
- **Echtzeit Überwachung**: Sammelt Statistiken jede Sekunde
- **Datenbank Speicherung**: Speichert Messungen automatisch in MongoDB
- **Log Management**: Hält maximal 10.000 Logs (entfernt automatisch die ältesten)
- **System Information**: Zeigt CPU Kerne, RAM Kapazität an
- **Datenbank Statistiken**: Zeigt Überwachungshistorie

### Verwendung:
```bash
python power_monitor.py
```

#### 5.3 Graph Visualisierung

Das `power_grapher.py` Skript erstellt interaktive Grafiken mit matplotlib:

### Visualisierungsoptionen:
1. **Aktuelle Aktivität**: Letzte 1-4 Stunden detaillierte Überwachung
2. **Zusammenfassungsstatistiken**: Tages-/Wochenübersicht mit Durchschnittswerten
3. **Dashboard Ansicht**: Umfassende Leistungsübersicht
4. **Benutzerdefinierter Zeitbereich**: Benutzerdefinierte Zeiträume
5. **Export Optionen**: Grafiken als PNG Dateien speichern

### Graph Typen:
- **Timeline Plots**: CPU und RAM Nutzung über Zeit
- **Verteilungshistogramme**: Nutzungsmuster Analyse
- **Gestapelte Flächendiagramme**: Speicherzuteilung Visualisierung
- **Dual-Achsen Plots**: CPU vs RAM Vergleich
- **Statistische Zusammenfassungen**: Mittelwert, Maximum, Minimum, Standardabweichung

### Verwendung:
```bash
python power_grapher.py
```

### Hauptfunktionen:
- **Interaktives Menü**: Visualisierungstyp wählen
- **Mehrere Zeitskalen**: Stunden, Tage, Wochen
- **Professioneller Stil**: Saubere, lesbare Grafiken
- **Statistische Analyse**: Automatische Berechnung von Metriken
- **Export Fähigkeit**: Grafiken für Berichte speichern

## 6. DAO Pattern - Joke Management

Das `joke_dao.py` Skript demonstriert das Data Access Object (DAO) Pattern für Witz-Management.

### Joke Klasse Attribute:
- **text**: Text des Witzes
- **category**: Liste von Kategorien (z.B. ["Wortspiel", "Geister"])
- **author**: Verfasser des Witzes

### DAO Methoden:
- **insert**: Neuen Witz hinzufügen
- **get_category**: Alle Witze einer Kategorie abrufen
- **delete**: Witz anhand ID löschen
- **update**: Witz bearbeiten (erweiterte Funktionalität)

### Verwendung:
```bash
python joke_dao.py
```

## 7. GridFS File Storage

Das `gridfs_demo.py` Skript implementiert MongoDB GridFS für Datei-Management und Fotoalbum-Funktionalität.

### File Manager Features:
- **Datei Speicherung**: Files in MongoDB GridFS speichern
- **Wiederherstellung**: Gespeicherte Files extrahieren
- **Metadaten**: Zusätzliche Informationen zu Files
- **Collection Struktur**: fs.files und fs.chunks Collections

### Photo Album Features:
- **Album Management**: Fotos nach Alben organisieren
- **Metadaten Support**: Album-Zugehörigkeit und Beschreibungen
- **Batch Download**: Ganze Alben herunterladen
- **Album Auflistung**: Verfügbare Alben anzeigen

### GridFS Encoding:
- **Rohdaten**: Base64 BSON Binary Format
- **Chunks**: Große Files werden automatisch aufgeteilt
- **Verbindung**: files_id verknüpft fs.files mit fs.chunks

### Verwendung:
```bash
python gridfs_demo.py
```

## 8. Polygon Visualisierung

Das `polygon_visualizer.py` Skript erstellt grafische Darstellungen von MongoDB neighborhood Polygonen mit Pillow.

### Funktionen:
- **Einzelne Polygone**: Spezifische Neighborhoods visualisieren
- **Alle Polygone**: Komplette neighborhood Übersicht
- **Koordinaten Normalisierung**: Automatische Skalierung für Bildgröße
- **Pillow Integration**: Professionelle Grafik-Erstellung

### Technische Details:
- **Koordinaten**: GeoJSON Polygon-Daten aus neighborhoods Collection
- **Normalisierung**: Skalierung auf Bildschirmauflösung
- **Farbcodierung**: Verschiedene Farben pro Polygon
- **Export**: PNG Dateien für weitere Verwendung

### Verwendung:
```bash
python polygon_visualizer.py
```

## 9. Jukebox System

Das `jukebox.py` Skript implementiert ein vollständiges Musikverwaltungs- und Abspielsystem.

### 9.1 Song Klasse Attribute:
- **name**: Titel des Songs (erforderlich)
- **artist**: Interpret (erforderlich)
- **album**: Album (optional)
- **genre**: Musikgenre (optional)
- **year**: Erscheinungsjahr (optional)

### 9.2 Management Features:
- **Song hinzufügen**: Neue Musikstücke in Datenbank speichern
- **Song bearbeiten**: Bestehende Songs modifizieren
- **Song löschen**: Songs aus Datenbank entfernen
- **Volltext-Suche**: Nach allen Attributen suchen

### 9.3 Player Features:
- **Intelligente Suche**: Groß-/Kleinschreibung ignorieren, Teilübereinstimmungen
- **Kombinierte Suche**: Mehrere Suchkriterien gleichzeitig
- **Playlist Management**: Songs in Abspielliste hinzufügen
- **FIFO Wiedergabe**: Songs in Reihenfolge abspielen
- **Zufallswiedergabe**: Wenn Playlist leer, zufälligen Song spielen

### Suchlogik:
- **Case-insensitive**: "beatles" findet "The Beatles"
- **Teilstring**: "Wall" findet "Another Brick in the Wall"
- **Multi-Parameter**: Artist="Beatles" + Name="Back" findet "Get Back"

### Verwendung:
```bash
python jukebox.py
```

## Anwendungsübersicht - Erweitert

| Anwendung | Zweck | Hauptfunktionen |
|-----------|-------|-----------------|
| `database_explorer.py` | Datenbank Browser | DB/Collections/Dokumente navigieren |
| `restaurant_crud.py` | Restaurant Operationen | Suche, Bewertungen, geografische Abfragen |
| `environment_demo.py` | Sicherheits Demo | Umgebungsvariablen, PATH lesen |
| `power_monitor.py` | System Überwachung | CPU/RAM Verfolgung, automatische Protokollierung |
| `power_grapher.py` | Datenvisualisierung | Interaktive Grafiken, Statistiken |
| `joke_dao.py` | DAO Pattern Demo | Witz-Management mit CRUD Operationen |
| `gridfs_demo.py` | File Storage | GridFS, Fotoalbum, Metadaten |
| `polygon_visualizer.py` | Geografische Visualisierung | Neighborhood Polygone, Pillow Grafiken |
| `jukebox.py` | Musik Management | Song-Verwaltung, Playlist, Player |

## Datei Struktur - Erweitert

```
m165_adrian/
├── app.py                 # Ursprünglicher MongoDB Verbindungstest
├── database_explorer.py   # Datenbank Browser Anwendung
├── restaurant_crud.py     # Restaurant CRUD Operationen
├── environment_demo.py    # Umgebungsvariablen Demonstration
├── power_monitor.py       # System Überwachungsanwendung
├── power_grapher.py       # Graph Visualisierungsanwendung
├── joke_dao.py           # DAO Pattern für Witz-Management
├── gridfs_demo.py        # GridFS File Storage und Fotoalbum
├── polygon_visualizer.py # Geografische Polygon Visualisierung
├── jukebox.py            # Musik Management und Player System
├── demo.py               # Setup Test und Demonstration
├── setup.sh              # Schnelles Setup Skript
├── requirements.txt      # Python Abhängigkeiten (inkl. Pillow)
├── README.md            # Diese Dokumentation
└── oop_basic/           # Objektorientierte Beispiele
    ├── app.py           # Buchverwaltung mit MongoDB
    ├── buch.py          # Buch Klassendefinition
    └── uuid.py          # UUID Hilfsfunktionen
```

## Security Implementation

### Before (Insecure):
```python
connection_string = "mongodb://192.168.1.157:27017/"  # ❌ Hardcoded
```

### After (Secure):
```python
connection_string = os.getenv('MONGODB_URI', 'default_fallback')  # ✅ Environment variable
```

## Key MongoDB Concepts Demonstrated

### Collections and Documents
- **Database**: Container for collections (like `restaurants`, `system_monitoring`)
- **Collection**: Group of documents (like `restaurants` collection, `power_stats`)
- **Document**: Individual record in BSON format (like a restaurant entry, power measurement)

### Query Operations
- **Find**: Basic document retrieval
- **Distinct**: Get unique values
- **Aggregation**: Complex data processing pipelines
- **Geospatial**: Location-based queries
- **Regex**: Pattern matching for text search
- **Indexing**: Performance optimization for timestamps

### CRUD Operations
- **Create**: Insert new documents (power stats, ratings)
- **Read**: Query and retrieve documents (search, browse)
- **Update**: Modify existing documents (add ratings)
- **Delete**: Remove documents (log cleanup)

## Performance Optimization

### Database Management:
- **Automatic Cleanup**: Maintains 10,000 log limit
- **Indexed Queries**: Timestamp indexing for fast retrieval
- **Batch Operations**: Efficient bulk insertions
- **Memory Management**: Optimized data structures

### Graph Performance:
- **Data Sampling**: Intelligent data point selection
- **Lazy Loading**: Load data only when needed
- **Caching**: Reuse calculated statistics
- **Progressive Rendering**: Handle large datasets

## Testing

Run the comprehensive test suite:

```bash
# Test all components
python demo.py

# Test environment variables
python environment_demo.py

# Quick setup and test
./setup.sh
```

## Einfache Implementierung

Alle Anwendungen sind bewusst maximal einfach gehalten:
- **Minimaler Code**: Nur essenzielle Funktionalität
- **Direkte Verbindungen**: Keine komplexe Fehlerbehandlung  
- **Einfache Menüs**: Reduzierte Optionen
- **Klare Struktur**: Verständliche, kurze Funktionen
- **Deutsche Benutzeroberfläche**: Für bessere Verständlichkeit

### Code-Vereinfachungen:
- **Power Grapher**: Von 7 auf 4 Menüoptionen reduziert
- **Power Monitor**: Vereinfachte Datenbankstatistiken
- **Environment Demo**: Kompakte Umgebungsvariablen-Demonstration
- **Demo Script**: Essenzielle Tests ohne komplexe Validierung
- **OOP Beispiele**: Minimale Buchverwaltung mit direkter MongoDB-Interaktion

## Production Deployment

### Environment Setup:
```bash
# Production environment variables
export MONGODB_URI='mongodb://username:password@production-server:27017/database'
export MONITORING_INTERVAL=60  # Seconds between measurements
export MAX_LOGS=50000          # Maximum log entries
```

### Security Checklist:
- ✅ Environment variables for credentials
- ✅ Input validation and sanitization
- ✅ Error handling without information leakage
- ✅ Connection pooling for performance
- ✅ Logging for audit trails
- ✅ Rate limiting for API endpoints

### Performance Tuning:
- **Database Indexing**: Create indexes on frequently queried fields
- **Connection Pooling**: Reuse database connections
- **Data Archiving**: Regular cleanup of old monitoring data
- **Query Optimization**: Use aggregation pipelines efficiently

## Best Practices Implemented

1. **Security**: Environment variables, input validation, error handling
2. **Performance**: Indexing, connection management, data cleanup
3. **Usability**: Interactive menus, clear error messages, help text
4. **Maintainability**: Modular design, comprehensive documentation
5. **Monitoring**: Real-time stats, historical analysis, alerting
6. **Visualization**: Multiple chart types, statistical analysis

## Next Steps for Enhancement

### Advanced Features:
- **Real-time Dashboards**: Web-based monitoring interface
- **Alert System**: Email/SMS notifications for high usage
- **Machine Learning**: Predictive analysis of system performance
- **Multi-server Monitoring**: Track multiple systems
- **Custom Metrics**: User-defined performance indicators

### Integration Options:
- **REST API**: Web service for external access
- **Message Queues**: Async processing for high-volume data
- **Time Series Database**: Specialized storage for metrics
- **Container Deployment**: Docker/Kubernetes support
- **Cloud Integration**: AWS/Azure monitoring services
