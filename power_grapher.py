#!/usr/bin/env python3
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os
from pymongo import MongoClient
import numpy as np
from power_monitor import PowerMonitor, Power

class PowerGrapher:
    def __init__(self, connection_string=None):
        self.monitor = PowerMonitor(connection_string)
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (10, 6)
    
    def plot_recent_stats(self, hours=1, save_file=None):
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)
        stats = self.monitor.get_stats_in_range(start_time, end_time)
        
        if not stats:
            print(f"⚠ Keine Daten für die letzten {hours} Stunden gefunden")
            return
        
        timestamps = [stat.timestamp for stat in stats]
        cpu_data = [stat.cpu_percent for stat in stats]
        ram_data = [(stat.ram_used / stat.ram_total) * 100 for stat in stats]
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
        fig.suptitle(f'Power Stats - {hours}h ({len(stats)} Datenpunkte)', fontsize=14)
        
        ax1.plot(timestamps, cpu_data, 'r-', label='CPU %')
        ax1.set_title('CPU')
        ax1.set_ylim(0, 100)
        ax1.grid(True, alpha=0.3)
        
        ax2.plot(timestamps, ram_data, 'b-', label='RAM %')
        ax2.set_title('RAM')
        ax2.set_ylim(0, 100)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Always save to file since we can't display
        if not save_file:
            save_file = f"power_stats_{hours}h_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        plt.savefig(save_file, dpi=150, bbox_inches='tight')
        plt.close()  # Close to free memory
        print(f"✓ Grafik gespeichert: {save_file}")
        
        # Print some stats
        if stats:
            avg_cpu = np.mean(cpu_data)
            avg_ram = np.mean(ram_data)
            print(f"  CPU: {avg_cpu:.1f}% Durchschnitt")
            print(f"  RAM: {avg_ram:.1f}% Durchschnitt")
    
    def create_dashboard(self, save_file=None):
        stats = self.monitor.get_recent_stats(limit=100)
        
        if not stats:
            print("⚠ Keine Daten für Dashboard gefunden")
            return
        
        cpu_values = [stat.cpu_percent for stat in stats]
        ram_values = [(stat.ram_used / stat.ram_total) * 100 for stat in stats]
        timestamps = [stat.timestamp for stat in stats]
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle(f'System Dashboard ({len(stats)} Datenpunkte)', fontsize=14)
        
        # Timeline
        ax1.plot(timestamps, cpu_values, 'r-', label='CPU %', linewidth=2)
        ax1.plot(timestamps, ram_values, 'b-', label='RAM %', linewidth=2)
        ax1.set_title('Timeline')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(0, 100)
        
        # CPU distribution
        ax2.hist(cpu_values, bins=10, color='red', alpha=0.7, edgecolor='black')
        ax2.set_title('CPU Verteilung')
        ax2.set_xlabel('CPU %')
        ax2.set_ylabel('Häufigkeit')
        
        # RAM distribution
        ax3.hist(ram_values, bins=10, color='blue', alpha=0.7, edgecolor='black')
        ax3.set_title('RAM Verteilung')
        ax3.set_xlabel('RAM %')
        ax3.set_ylabel('Häufigkeit')
        
        # Statistics text
        ax4.axis('off')
        cpu_avg = np.mean(cpu_values)
        ram_avg = np.mean(ram_values)
        cpu_max = np.max(cpu_values)
        ram_max = np.max(ram_values)
        
        stats_text = f"""Statistiken:

CPU:
  • Durchschnitt: {cpu_avg:.1f}%
  • Maximum: {cpu_max:.1f}%

RAM:
  • Durchschnitt: {ram_avg:.1f}%
  • Maximum: {ram_max:.1f}%

Datenpunkte: {len(stats)}
Zeitraum: {timestamps[0].strftime('%H:%M')} - {timestamps[-1].strftime('%H:%M')}"""
        
        ax4.text(0.1, 0.5, stats_text, fontsize=11, verticalalignment='center')
        
        plt.tight_layout()
        
        # Always save to file
        if not save_file:
            save_file = f"dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        plt.savefig(save_file, dpi=150, bbox_inches='tight')
        plt.close()  # Close to free memory
        print(f"✓ Dashboard gespeichert: {save_file}")
        print(f"  CPU: {cpu_avg:.1f}% Durchschnitt, {cpu_max:.1f}% Maximum")
        print(f"  RAM: {ram_avg:.1f}% Durchschnitt, {ram_max:.1f}% Maximum")

def main():
    print("Power Grafiken")
    print("=" * 20)
    
    try:
        grapher = PowerGrapher()
        print("✓ Verbunden mit MongoDB: system_monitoring.power_stats")
    except Exception as e:
        print(f"❌ Fehler beim Verbinden: {e}")
        return
    
    print("\nHinweis: Grafiken werden als PNG-Dateien gespeichert")
    
    while True:
        print("\nOptionen:")
        print("1. Letzte Stunde")
        print("2. Letzte 4 Stunden") 
        print("3. Dashboard")
        print("4. Beenden")
        
        choice = input("\nWählen (1-4): ").strip()
        
        if choice == "1":
            print("Erstelle Grafik für letzte Stunde...")
            grapher.plot_recent_stats(hours=1)
        elif choice == "2":
            print("Erstelle Grafik für letzte 4 Stunden...")
            grapher.plot_recent_stats(hours=4)
        elif choice == "3":
            print("Erstelle Dashboard...")
            grapher.create_dashboard()
        elif choice == "4":
            print("Tschüss!")
            break
        else:
            print("Ungültige Option")

if __name__ == "__main__":
    main()
