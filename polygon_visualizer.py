#!/usr/bin/env python3
"""
Erweiterte Polygon-Visualisierung für NYC Neighborhoods (Aufgabe 8)
Unterstützt sowohl PIL/Pillow als auch matplotlib für verschiedene Visualisierungen
"""
from pymongo import MongoClient
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

class PolygonVisualizer:
    def __init__(self, connection_string=None):
        if connection_string is None:
            connection_string = os.getenv('MONGODB_URI', 'mongodb://192.168.1.157:27017/')
        
        self.client = MongoClient(connection_string)
        self.db = self.client['restaurants']
        self.collection = self.db['neighborhoods']
        print("✓ Verbunden mit neighborhoods Collection")
        
        # Statistiken laden
        self.doc_count = self.collection.count_documents({})
        print(f"✓ {self.doc_count} Neighborhoods verfügbar")
    
    def normalize_coordinates(self, coords, img_width=800, img_height=600):
        if not coords:
            return []
        
        all_x = [coord[0] for coord in coords]
        all_y = [coord[1] for coord in coords]
        
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        
        range_x = max_x - min_x
        range_y = max_y - min_y
        
        normalized = []
        for x, y in coords:
            norm_x = int(((x - min_x) / range_x) * (img_width - 100) + 50)
            norm_y = int(((y - min_y) / range_y) * (img_height - 100) + 50)
            normalized.append((norm_x, norm_y))
        
        return normalized
    
    def draw_single_polygon(self, polygon_name):
        neighborhood = self.collection.find_one({'name': polygon_name})
        
        if not neighborhood or 'geometry' not in neighborhood:
            print(f"Polygon '{polygon_name}' nicht gefunden")
            return
        
        coords = neighborhood['geometry']['coordinates'][0]
        
        im = Image.new(mode="RGB", size=(800, 600), color="white")
        draw = ImageDraw.Draw(im)
        
        normalized_coords = self.normalize_coordinates(coords)
        
        if len(normalized_coords) > 2:
            draw.polygon(normalized_coords, outline="blue", fill="lightblue", width=2)
        
        draw.text((10, 10), f"Polygon: {polygon_name}", fill="black")
        
        filename = f"polygon_{polygon_name.replace(' ', '_')}.png"
        im.save(filename)
        print(f"✓ Polygon gespeichert: {filename}")
        im.show()
    
    def draw_all_polygons(self):
        neighborhoods = list(self.collection.find({}))
        
        if not neighborhoods:
            print("Keine Polygone gefunden")
            return
        
        im = Image.new(mode="RGB", size=(1200, 800), color="white")
        draw = ImageDraw.Draw(im)
        
        all_coords = []
        for neighborhood in neighborhoods:
            if 'geometry' in neighborhood and neighborhood['geometry']['coordinates']:
                coords = neighborhood['geometry']['coordinates'][0]
                all_coords.extend(coords)
        
        colors = ["red", "blue", "green", "orange", "purple", "brown", "pink"]
        
        for i, neighborhood in enumerate(neighborhoods):
            if 'geometry' not in neighborhood:
                continue
            
            coords = neighborhood['geometry']['coordinates'][0]
            normalized_coords = self.normalize_coordinates(coords, 1200, 800)
            
            color = colors[i % len(colors)]
            
            if len(normalized_coords) > 2:
                draw.polygon(normalized_coords, outline=color, width=2)
            
            if normalized_coords:
                center_x = sum(x for x, y in normalized_coords) // len(normalized_coords)
                center_y = sum(y for x, y in normalized_coords) // len(normalized_coords)
                name = neighborhood.get('name', f'Polygon {i}')
                draw.text((center_x, center_y), name[:10], fill=color)
        
        draw.text((10, 10), f"Alle Polygone ({len(neighborhoods)} total)", fill="black")
        
        filename = "all_polygons.png"
        im.save(filename)
        print(f"✓ Alle Polygone gespeichert: {filename}")
        im.show()
    
    def list_neighborhoods(self):
        neighborhoods = self.collection.find({}, {'name': 1})
        names = [n.get('name', 'Unbekannt') for n in neighborhoods]
        return names
    
    # === NEUE MATPLOTLIB-METHODEN ===
    
    def get_neighborhood_data(self, limit=None, borough_filter=None):
        """Lädt Neighborhood-Daten aus der MongoDB mit optionalen Filtern"""
        query = {}
        if borough_filter:
            # Filtere nach Borough-spezifischen Neighborhoods
            borough_patterns = {
                'manhattan': ['Manhattan', 'Harlem', 'Village', 'Midtown', 'SoHo', 'TriBeCa'],
                'brooklyn': ['Brooklyn', 'Bushwick', 'Crown', 'Park Slope', 'Williamsburg'],
                'queens': ['Queens', 'Astoria', 'Flushing', 'Jamaica', 'Corona'],
                'bronx': ['Bronx', 'Fordham', 'Morrisania', 'Tremont'],
                'staten island': ['Staten', 'Richmond', 'Tottenville']
            }
            if borough_filter.lower() in borough_patterns:
                patterns = borough_patterns[borough_filter.lower()]
                query['name'] = {'$regex': '|'.join(patterns), '$options': 'i'}
        
        cursor = self.collection.find(query, {'name': 1, 'geometry': 1})
        
        if limit:
            cursor = cursor.limit(limit)
            
        neighborhoods = []
        for doc in cursor:
            if 'geometry' in doc and doc['geometry']['type'] == 'Polygon':
                neighborhoods.append({
                    'name': doc['name'],
                    'coordinates': doc['geometry']['coordinates'][0]  # Erstes (äußeres) Polygon
                })
        
        return neighborhoods
    
    def calculate_bounds(self, neighborhoods):
        """Berechnet die Bounding Box aller Polygone"""
        all_lons = []
        all_lats = []
        
        for neighborhood in neighborhoods:
            for coord in neighborhood['coordinates']:
                all_lons.append(coord[0])  # Longitude
                all_lats.append(coord[1])  # Latitude
        
        return {
            'min_lon': min(all_lons),
            'max_lon': max(all_lons),
            'min_lat': min(all_lats),
            'max_lat': max(all_lats)
        }
    
    def visualize_with_matplotlib(self, limit=20, borough_filter=None, figsize=(15, 12)):
        """Moderne Visualisierung mit matplotlib"""
        print(f"Lade {limit if limit else 'alle'} Neighborhoods{f' ({borough_filter})' if borough_filter else ''}...")
        neighborhoods = self.get_neighborhood_data(limit, borough_filter)
        
        if not neighborhoods:
            print("Keine Neighborhoods gefunden!")
            return None, None
        
        print(f"Gefunden: {len(neighborhoods)} Neighborhoods")
        
        # Bounds berechnen
        bounds = self.calculate_bounds(neighborhoods)
        print(f"Bounds: Lon [{bounds['min_lon']:.4f}, {bounds['max_lon']:.4f}], "
              f"Lat [{bounds['min_lat']:.4f}, {bounds['max_lat']:.4f}]")
        
        # Plot erstellen
        fig, ax = plt.subplots(figsize=figsize)
        
        # Verschiedene Farben für die Polygone
        colors = plt.cm.Set3(np.linspace(0, 1, len(neighborhoods)))
        
        for i, neighborhood in enumerate(neighborhoods):
            coords = neighborhood['coordinates']
            
            # Koordinaten in separate Listen aufteilen
            lons = [coord[0] for coord in coords]
            lats = [coord[1] for coord in coords]
            
            # Polygon zeichnen
            polygon = patches.Polygon(
                list(zip(lons, lats)),
                closed=True,
                facecolor=colors[i],
                edgecolor='black',
                linewidth=0.5,
                alpha=0.7
            )
            ax.add_patch(polygon)
            
            # Label in der Mitte des Polygons
            center_lon = sum(lons) / len(lons)
            center_lat = sum(lats) / len(lats)
            
            ax.text(center_lon, center_lat, neighborhood['name'], 
                   fontsize=8, ha='center', va='center',
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
        
        # Plot-Einstellungen
        ax.set_xlim(bounds['min_lon'] - 0.01, bounds['max_lon'] + 0.01)
        ax.set_ylim(bounds['min_lat'] - 0.01, bounds['max_lat'] + 0.01)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        title = f'NYC Neighborhoods ({len(neighborhoods)} Neighborhoods)'
        if borough_filter:
            title += f' - {borough_filter.title()}'
        ax.set_title(title)
        
        plt.tight_layout()
        return fig, ax
    
    def visualize_single_detailed(self, neighborhood_name):
        """Detaillierte Visualisierung eines einzelnen Neighborhoods"""
        doc = self.collection.find_one({'name': neighborhood_name})
        
        if not doc:
            print(f"Neighborhood '{neighborhood_name}' nicht gefunden!")
            available = [n['name'] for n in self.collection.find({}, {'name': 1}).limit(5)]
            print(f"Verfügbare (erste 5): {', '.join(available)}")
            return None, None
        
        if doc['geometry']['type'] != 'Polygon':
            print(f"'{neighborhood_name}' ist kein Polygon!")
            return None, None
        
        coords = doc['geometry']['coordinates'][0]
        
        # Plot erstellen
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Koordinaten aufteilen
        lons = [coord[0] for coord in coords]
        lats = [coord[1] for coord in coords]
        
        # Linkes Plot: Gefülltes Polygon
        polygon1 = patches.Polygon(
            list(zip(lons, lats)),
            closed=True,
            facecolor='lightblue',
            edgecolor='navy',
            linewidth=2,
            alpha=0.7
        )
        ax1.add_patch(polygon1)
        
        # Rechtes Plot: Nur Umriss mit Punkten
        ax2.plot(lons + [lons[0]], lats + [lats[0]], 'b-', linewidth=2, label='Polygon-Umriss')
        ax2.plot(lons, lats, 'ro', markersize=4, alpha=0.7, label='Eckpunkte')
        
        # Startpunkt markieren
        ax2.plot(lons[0], lats[0], 'go', markersize=8, label='Startpunkt')
        
        # Bounds für dieses Polygon
        min_lon, max_lon = min(lons), max(lons)
        min_lat, max_lat = min(lats), max(lats)
        
        # Plot-Einstellungen für beide Plots
        margin = 0.005
        for ax in [ax1, ax2]:
            ax.set_xlim(min_lon - margin, max_lon + margin)
            ax.set_ylim(min_lat - margin, max_lat + margin)
            ax.set_aspect('equal')
            ax.grid(True, alpha=0.3)
            ax.set_xlabel('Longitude')
            ax.set_ylabel('Latitude')
        
        ax1.set_title(f"{neighborhood_name} - Gefülltes Polygon")
        ax2.set_title(f"{neighborhood_name} - Umriss & Punkte")
        ax2.legend()
        
        # Statistiken anzeigen
        print(f"\n=== {neighborhood_name} ===")
        print(f"Anzahl Eckpunkte: {len(coords)}")
        print(f"Longitude: {min_lon:.6f} bis {max_lon:.6f}")
        print(f"Latitude: {min_lat:.6f} bis {max_lat:.6f}")
        print(f"Erste Koordinate: [{coords[0][0]:.6f}, {coords[0][1]:.6f}]")
        print(f"Letzte Koordinate: [{coords[-1][0]:.6f}, {coords[-1][1]:.6f}]")
        
        plt.tight_layout()
        return fig, (ax1, ax2)
    
    def create_statistics_plot(self):
        """Erstellt ein Statistik-Plot über alle Neighborhoods"""
        neighborhoods = self.get_neighborhood_data()
        
        # Statistiken sammeln
        point_counts = []
        area_estimates = []
        borough_data = {'Manhattan': 0, 'Brooklyn': 0, 'Queens': 0, 'Bronx': 0, 'Staten Island': 0, 'Other': 0}
        
        for neighborhood in neighborhoods:
            coords = neighborhood['coordinates']
            point_counts.append(len(coords))
            
            # Grobe Flächenschätzung (Bounding Box)
            lons = [c[0] for c in coords]
            lats = [c[1] for c in coords]
            area = (max(lons) - min(lons)) * (max(lats) - min(lats))
            area_estimates.append(area)
            
            # Borough-Zuordnung
            name = neighborhood['name'].lower()
            if any(keyword in name for keyword in ['manhattan', 'harlem', 'village', 'midtown', 'soho', 'tribeca']):
                borough_data['Manhattan'] += 1
            elif any(keyword in name for keyword in ['brooklyn', 'bushwick', 'crown', 'park slope', 'williamsburg']):
                borough_data['Brooklyn'] += 1
            elif any(keyword in name for keyword in ['queens', 'astoria', 'flushing', 'jamaica', 'corona']):
                borough_data['Queens'] += 1
            elif any(keyword in name for keyword in ['bronx', 'fordham', 'morrisania', 'tremont']):
                borough_data['Bronx'] += 1
            elif any(keyword in name for keyword in ['staten', 'richmond', 'tottenville']):
                borough_data['Staten Island'] += 1
            else:
                borough_data['Other'] += 1
        
        # Statistik-Plot erstellen
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Histogramm der Punktanzahl
        ax1.hist(point_counts, bins=20, color='skyblue', alpha=0.7, edgecolor='black')
        ax1.set_xlabel('Anzahl Eckpunkte')
        ax1.set_ylabel('Anzahl Neighborhoods')
        ax1.set_title('Verteilung der Eckpunkte pro Neighborhood')
        ax1.grid(True, alpha=0.3)
        
        # 2. Scatterplot Punkte vs. geschätzte Fläche
        ax2.scatter(point_counts, area_estimates, alpha=0.6, color='orange')
        ax2.set_xlabel('Anzahl Eckpunkte')
        ax2.set_ylabel('Geschätzte Fläche (Bounding Box)')
        ax2.set_title('Eckpunkte vs. Fläche')
        ax2.grid(True, alpha=0.3)
        
        # 3. Borough-Verteilung
        boroughs = list(borough_data.keys())
        counts = list(borough_data.values())
        colors_borough = ['red', 'blue', 'green', 'orange', 'purple', 'gray']
        ax3.pie(counts, labels=boroughs, autopct='%1.1f%%', colors=colors_borough)
        ax3.set_title('Neighborhood-Verteilung nach Borough (geschätzt)')
        
        # 4. Top 10 Neighborhoods nach Eckpunkten
        neighborhood_points = [(n['name'], len(n['coordinates'])) for n in neighborhoods]
        neighborhood_points.sort(key=lambda x: x[1], reverse=True)
        top_10 = neighborhood_points[:10]
        
        names = [item[0][:20] for item in top_10]  # Namen kürzen
        points = [item[1] for item in top_10]
        
        ax4.barh(range(len(names)), points, color='lightcoral')
        ax4.set_yticks(range(len(names)))
        ax4.set_yticklabels(names)
        ax4.set_xlabel('Anzahl Eckpunkte')
        ax4.set_title('Top 10 Neighborhoods nach Eckpunkten')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Statistiken ausgeben
        print(f"\n=== NEIGHBORHOOD STATISTIKEN ===")
        print(f"Gesamt Neighborhoods: {len(neighborhoods)}")
        print(f"Durchschnittliche Eckpunkte: {np.mean(point_counts):.1f}")
        print(f"Min/Max Eckpunkte: {min(point_counts)} / {max(point_counts)}")
        print(f"Neighborhood mit meisten Punkten: {top_10[0][0]} ({top_10[0][1]} Punkte)")
        
        return fig, ((ax1, ax2), (ax3, ax4))
    
    # === BESTEHENDE PIL-METHODEN (verbessert) ===
def demo_pillow():
    print("Pillow Drawing Demo")
    print("=" * 20)
    
    im = Image.new(mode="RGB", size=(200, 200), color="white")
    draw = ImageDraw.Draw(im)
    
    draw.line((100, 200, 150, 180), fill=0x00ffff, width=3)
    draw.polygon([(50, 50), (150, 50), (100, 150)], outline="red", fill="yellow")
    draw.text((10, 10), "Demo", fill="black")
    
    im.save("pillow_demo.png")
    print("✓ Demo Bild erstellt: pillow_demo.png")
    im.show()

def main():
    print("=== ERWEITERTE POLYGON VISUALISIERUNG (Aufgabe 8) ===")
    print("=" * 55)
    
    while True:
        print("\nVisualisierungs-Optionen:")
        print("1. Pillow Demo (Original)")
        print("2. Einzelnes Polygon (PIL)")
        print("3. Alle Polygone (PIL)")
        print("4. Matplotlib Übersicht")
        print("5. Einzelnes Polygon detailliert (matplotlib)")
        print("6. Borough-spezifische Ansicht")
        print("7. Statistiken und Analyse")
        print("8. Neighborhoods auflisten")
        print("9. Interaktiver Explorer")
        print("0. Beenden")
        
        choice = input("\nWählen (0-9): ").strip()
        
        if choice == "0":
            break
            
        elif choice == "1":
            demo_pillow()
        
        elif choice == "2":
            viz = PolygonVisualizer()
            neighborhoods = viz.list_neighborhoods()
            
            print(f"\nVerfügbare Neighborhoods (erste 10 von {len(neighborhoods)}):")
            for name in neighborhoods[:10]:
                print(f"- {name}")
            
            polygon_name = input("\nPolygon Name eingeben: ").strip()
            viz.draw_single_polygon(polygon_name)
        
        elif choice == "3":
            viz = PolygonVisualizer()
            viz.draw_all_polygons()
        
        elif choice == "4":
            viz = PolygonVisualizer()
            try:
                limit = int(input("Anzahl Neighborhoods (Enter für 20): ").strip() or "20")
            except ValueError:
                limit = 20
            
            fig, ax = viz.visualize_with_matplotlib(limit=limit)
            if fig:
                plt.show()
        
        elif choice == "5":
            viz = PolygonVisualizer()
            neighborhoods = viz.list_neighborhoods()
            
            print(f"\nVerfügbare Neighborhoods (erste 10 von {len(neighborhoods)}):")
            for name in neighborhoods[:10]:
                print(f"- {name}")
            
            polygon_name = input("\nNeighborhood Name eingeben: ").strip()
            fig, axes = viz.visualize_single_detailed(polygon_name)
            if fig:
                plt.show()
        
        elif choice == "6":
            viz = PolygonVisualizer()
            print("\nVerfügbare Borough-Filter:")
            print("- manhattan")
            print("- brooklyn") 
            print("- queens")
            print("- bronx")
            print("- staten island")
            
            borough = input("\nBorough eingeben: ").strip()
            if borough:
                fig, ax = viz.visualize_with_matplotlib(limit=None, borough_filter=borough)
                if fig:
                    plt.show()
        
        elif choice == "7":
            viz = PolygonVisualizer()
            print("Erstelle Statistiken... (kann einen Moment dauern)")
            fig, axes = viz.create_statistics_plot()
            plt.show()
        
        elif choice == "8":
            viz = PolygonVisualizer()
            neighborhoods = viz.list_neighborhoods()
            print(f"\n{len(neighborhoods)} Neighborhoods gefunden:")
            for i, name in enumerate(neighborhoods, 1):
                print(f"{i:3d}. {name}")
        
        elif choice == "9":
            viz = PolygonVisualizer()
            interactive_explorer(viz)
        
        else:
            print("Ungültige Option")

def interactive_explorer(viz):
    """Erweiterte interaktive Kommandozeile"""
    print("\n=== INTERAKTIVER POLYGON-EXPLORER ===")
    print("Befehle:")
    print("  list [anzahl] - Neighborhoods auflisten")
    print("  show <name> - Einzelnes Neighborhood (matplotlib)")
    print("  overview [anzahl] [borough] - Übersicht")
    print("  stats - Statistiken anzeigen")
    print("  search <text> - Nach Namen suchen")
    print("  save <dateiname> - Letzte Visualisierung speichern")
    print("  help - Hilfe anzeigen")
    print("  quit - Beenden")
    
    neighborhoods = viz.list_neighborhoods()
    last_fig = None
    
    while True:
        command = input("\nexplorer> ").strip().split()
        
        if not command:
            continue
            
        cmd = command[0].lower()
        
        if cmd == "quit":
            break
            
        elif cmd == "help":
            print("\nVerfügbare Befehle:")
            print("  list [anzahl] - Zeige Neighborhoods")
            print("  show <name> - Detailansicht eines Neighborhoods")
            print("  overview [anzahl] [borough] - Übersicht mehrerer Neighborhoods")
            print("  stats - Zeige Statistiken")
            print("  search <text> - Suche nach Neighborhood-Namen")
            print("  save <dateiname> - Speichere aktuelle Visualisierung")
            
        elif cmd == "list":
            limit = int(command[1]) if len(command) > 1 and command[1].isdigit() else len(neighborhoods)
            print(f"\nNeighborhoods (erste {min(limit, len(neighborhoods))}):")
            for i, name in enumerate(neighborhoods[:limit], 1):
                print(f"{i:3d}. {name}")
                
        elif cmd == "show" and len(command) > 1:
            name = " ".join(command[1:])
            last_fig, _ = viz.visualize_single_detailed(name)
            if last_fig:
                plt.show()
                
        elif cmd == "overview":
            limit = int(command[1]) if len(command) > 1 and command[1].isdigit() else 20
            borough = command[2] if len(command) > 2 else None
            last_fig, _ = viz.visualize_with_matplotlib(limit=limit, borough_filter=borough)
            if last_fig:
                plt.show()
                
        elif cmd == "stats":
            last_fig, _ = viz.create_statistics_plot()
            plt.show()
            
        elif cmd == "search" and len(command) > 1:
            search_term = " ".join(command[1:]).lower()
            matches = [name for name in neighborhoods if search_term in name.lower()]
            print(f"\nGefunden {len(matches)} Matches für '{search_term}':")
            for match in matches[:20]:  # Erste 20 anzeigen
                print(f"  - {match}")
                
        elif cmd == "save" and len(command) > 1:
            filename = command[1]
            if last_fig:
                last_fig.savefig(filename, dpi=300, bbox_inches='tight')
                print(f"✓ Visualisierung gespeichert: {filename}")
            else:
                print("❌ Keine aktuelle Visualisierung zum Speichern!")
                
        else:
            print(f"❌ Unbekannter Befehl: {cmd}. Verwende 'help' für Hilfe.")

if __name__ == "__main__":
    main()
