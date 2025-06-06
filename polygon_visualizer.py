#!/usr/bin/env python3
from pymongo import MongoClient
from PIL import Image, ImageDraw
import os

class PolygonVisualizer:
    def __init__(self, connection_string=None):
        if connection_string is None:
            connection_string = os.getenv('MONGODB_URI', 'mongodb://192.168.1.157:27017/')
        
        self.client = MongoClient(connection_string)
        self.db = self.client['restaurants']
        self.collection = self.db['neighborhoods']
        print("✓ Verbunden mit neighborhoods Collection")
    
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
    print("Polygon Visualisierung")
    print("=" * 22)
    
    while True:
        print("\nOptionen:")
        print("1. Pillow Demo")
        print("2. Einzelnes Polygon zeichnen")
        print("3. Alle Polygone zeichnen")
        print("4. Neighborhoods auflisten")
        print("5. Beenden")
        
        choice = input("\nWählen (1-5): ").strip()
        
        if choice == "1":
            demo_pillow()
        
        elif choice == "2":
            viz = PolygonVisualizer()
            neighborhoods = viz.list_neighborhoods()
            
            print("\nVerfügbare Neighborhoods:")
            for name in neighborhoods[:10]:
                print(f"- {name}")
            
            polygon_name = input("\nPolygon Name eingeben: ").strip()
            viz.draw_single_polygon(polygon_name)
        
        elif choice == "3":
            viz = PolygonVisualizer()
            viz.draw_all_polygons()
        
        elif choice == "4":
            viz = PolygonVisualizer()
            neighborhoods = viz.list_neighborhoods()
            print(f"\n{len(neighborhoods)} Neighborhoods gefunden:")
            for name in neighborhoods:
                print(f"- {name}")
        
        elif choice == "5":
            break
        
        else:
            print("Ungültige Option")

if __name__ == "__main__":
    main()
