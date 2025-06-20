#!/usr/bin/env python3
"""
Test-Skript für die Polygon-Visualisierung (Aufgabe 8)
Führt verschiedene Visualisierungen automatisch aus
"""

import sys
import os

# Polygon-Visualizer importieren
sys.path.append('/home/artur/schule/jahr_2/sem_2/m165_adrian')
from polygon_visualizer import PolygonVisualizer
import matplotlib.pyplot as plt

def test_polygon_visualizer():
    print("=== POLYGON VISUALISIERUNG TEST (Aufgabe 8) ===")
    print()
    
    # Visualizer initialisieren
    viz = PolygonVisualizer()
    
    print("1. Teste matplotlib Übersicht (10 Neighborhoods)...")
    try:
        fig, ax = viz.visualize_with_matplotlib(limit=10)
        if fig:
            plt.savefig('test_overview_10.png', dpi=150, bbox_inches='tight')
            print("✓ Übersicht gespeichert: test_overview_10.png")
            plt.close(fig)
        else:
            print("❌ Fehler bei Übersicht")
    except Exception as e:
        print(f"❌ Fehler: {e}")
    
    print("\n2. Teste einzelnes Neighborhood (Bedford)...")
    try:
        fig, axes = viz.visualize_single_detailed("Bedford")
        if fig:
            plt.savefig('test_bedford_detail.png', dpi=150, bbox_inches='tight')
            print("✓ Bedford Detail gespeichert: test_bedford_detail.png")
            plt.close(fig)
        else:
            print("❌ Fehler bei Bedford Visualisierung")
    except Exception as e:
        print(f"❌ Fehler: {e}")
    
    print("\n3. Teste Manhattan-spezifische Ansicht...")
    try:
        fig, ax = viz.visualize_with_matplotlib(limit=None, borough_filter="manhattan")
        if fig:
            plt.savefig('test_manhattan.png', dpi=150, bbox_inches='tight')
            print("✓ Manhattan Ansicht gespeichert: test_manhattan.png")
            plt.close(fig)
        else:
            print("❌ Fehler bei Manhattan Ansicht")
    except Exception as e:
        print(f"❌ Fehler: {e}")
    
    print("\n4. Teste Statistiken...")
    try:
        fig, axes = viz.create_statistics_plot()
        if fig:
            plt.savefig('test_statistics.png', dpi=150, bbox_inches='tight')
            print("✓ Statistiken gespeichert: test_statistics.png")
            plt.close(fig)
        else:
            print("❌ Fehler bei Statistiken")
    except Exception as e:
        print(f"❌ Fehler: {e}")
    
    print("\n5. Liste einige Neighborhoods auf...")
    try:
        neighborhoods = viz.list_neighborhoods()
        print(f"✓ Gefunden: {len(neighborhoods)} Neighborhoods")
        print("Erste 10:")
        for i, name in enumerate(neighborhoods[:10], 1):
            print(f"  {i:2d}. {name}")
    except Exception as e:
        print(f"❌ Fehler: {e}")
    
    print("\n=== TEST ABGESCHLOSSEN ===")
    print("Überprüfe die generierten PNG-Dateien für die Visualisierungen.")

if __name__ == "__main__":
    test_polygon_visualizer()
