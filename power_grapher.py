#!/usr/bin/env python3
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
        
        timestamps = [stat.timestamp for stat in stats]
        cpu_data = [stat.cpu_percent for stat in stats]
        ram_data = [(stat.ram_used / stat.ram_total) * 100 for stat in stats]
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
        fig.suptitle(f'Power Stats - {hours}h', fontsize=14)
        
        ax1.plot(timestamps, cpu_data, 'r-', label='CPU %')
        ax1.set_title('CPU')
        ax1.set_ylim(0, 100)
        
        ax2.plot(timestamps, ram_data, 'b-', label='RAM %')
        ax2.set_title('RAM')
        ax2.set_ylim(0, 100)
        
        plt.tight_layout()
        
        if save_file:
            plt.savefig(save_file)
            print(f"Grafik gespeichert: {save_file}")
        else:
            plt.show()
    
    def create_dashboard(self, save_file=None):
        stats = self.monitor.get_recent_stats(limit=100)
        
        cpu_values = [stat.cpu_percent for stat in stats]
        ram_values = [(stat.ram_used / stat.ram_total) * 100 for stat in stats]
        timestamps = [stat.timestamp for stat in stats]
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle('System Dashboard', fontsize=14)
        
        ax1.plot(timestamps, cpu_values, 'r-', label='CPU')
        ax1.plot(timestamps, ram_values, 'b-', label='RAM')
        ax1.set_title('Timeline')
        ax1.legend()
        
        ax2.hist(cpu_values, bins=10, color='red', alpha=0.7)
        ax2.set_title('CPU Verteilung')
        
        ax3.hist(ram_values, bins=10, color='blue', alpha=0.7)
        ax3.set_title('RAM Verteilung')
        
        ax4.axis('off')
        stats_text = f"""
        CPU: {np.mean(cpu_values):.1f}% avg
        RAM: {np.mean(ram_values):.1f}% avg
        Datenpunkte: {len(stats)}
        """
        ax4.text(0.1, 0.5, stats_text, fontsize=12)
        
        plt.tight_layout()
        
        if save_file:
            plt.savefig(save_file)
            print(f"Dashboard gespeichert: {save_file}")
        else:
            plt.show()

def main():
    print("Power Grafiken")
    print("=" * 20)
    
    grapher = PowerGrapher()
    
    while True:
        print("\nOptionen:")
        print("1. Letzte Stunde")
        print("2. Letzte 4 Stunden") 
        print("3. Dashboard")
        print("4. Beenden")
        
        choice = input("\nWählen (1-4): ").strip()
        
        if choice == "1":
            grapher.plot_recent_stats(hours=1)
        elif choice == "2":
            grapher.plot_recent_stats(hours=4)
        elif choice == "3":
            grapher.create_dashboard()
        elif choice == "4":
            print("Tschüss!")
            break
        else:
            print("Ungültige Option")

if __name__ == "__main__":
    main()
