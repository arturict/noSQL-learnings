import psutil
import time
import os
from datetime import datetime
from pymongo import MongoClient

class Power:
    def __init__(self, cpu_percent=None, ram_total=None, ram_used=None, timestamp=None):
        if cpu_percent is None or ram_total is None or ram_used is None or timestamp is None:
            self.cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            self.ram_total = memory.total
            self.ram_used = memory.used
            self.timestamp = datetime.now()
        else:
            self.cpu_percent = cpu_percent
            self.ram_total = ram_total
            self.ram_used = ram_used
            self.timestamp = timestamp
    
    def to_dict(self):
        return {
            'cpu_percent': self.cpu_percent,
            'ram_total': self.ram_total,
            'ram_used': self.ram_used,
            'ram_percent': (self.ram_used / self.ram_total) * 100,
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            cpu_percent=data['cpu_percent'],
            ram_total=data['ram_total'],
            ram_used=data['ram_used'],
            timestamp=data['timestamp']
        )
    
    def __str__(self):
        ram_percent = (self.ram_used / self.ram_total) * 100
        return (f"Power Stats [{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}]: "
                f"CPU: {self.cpu_percent:.1f}%, "
                f"RAM: {self.ram_used / (1024**3):.1f}GB / {self.ram_total / (1024**3):.1f}GB "
                f"({ram_percent:.1f}%)")

class PowerMonitor:
    def __init__(self, connection_string=None, database_name="system_monitoring", 
                 collection_name="power_stats", max_logs=10000):
        if connection_string is None:
            connection_string = os.getenv('MONGODB_URI', 'mongodb://192.168.1.157:27017/')
        
        self.max_logs = max_logs
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
        
        print(f"✓ Verbunden mit MongoDB: {database_name}.{collection_name}")
        
        self.collection.create_index("timestamp")
    
    def collect_stats(self):
        return Power()
    
    def store_stats(self, power_stats):
        result = self.collection.insert_one(power_stats.to_dict())
        return result.inserted_id
    
    def cleanup_old_logs(self):
        count = self.collection.count_documents({})
        
        if count > self.max_logs:
            to_delete = count - self.max_logs
            
            oldest_docs = self.collection.find().sort("timestamp", 1).limit(to_delete)
            oldest_ids = [doc["_id"] for doc in oldest_docs]
            
            result = self.collection.delete_many({"_id": {"$in": oldest_ids}})
            print(f"Aufräumen: {result.deleted_count} alte Logs gelöscht (behalten: {self.max_logs})")
    
    def start_monitoring(self, interval=1):
        print(f"Power Überwachung gestartet (Intervall: {interval}s, max logs: {self.max_logs})")
        print("Strg+C zum Stoppen")
        
        while True:
            stats = self.collect_stats()
            doc_id = self.store_stats(stats)
            
            if doc_id:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {stats}")
                
                if self.collection.count_documents({}) % 100 == 0:
                    self.cleanup_old_logs()
            
            time.sleep(interval)
    
    def get_recent_stats(self, limit=100):
        cursor = self.collection.find().sort("timestamp", -1).limit(limit)
        return [Power.from_dict(doc) for doc in cursor]
    
    def get_stats_in_range(self, start_time, end_time):
        cursor = self.collection.find({
            "timestamp": {
                "$gte": start_time,
                "$lte": end_time
            }
        }).sort("timestamp", 1)
        return [Power.from_dict(doc) for doc in cursor]
    
    def get_database_stats(self):
        count = self.collection.count_documents({})
        return {'total_logs': count}

def main():
    print("Power Monitor")
    print("=" * 15)
    
    monitor = PowerMonitor()
    
    print(f"CPU Kerne: {psutil.cpu_count()}")
    memory = psutil.virtual_memory()
    print(f"RAM: {memory.total / (1024**3):.1f} GB")
    
    stats = monitor.get_database_stats()
    print(f"Logs: {stats['total_logs']}")
    
    print("\nÜberwachung gestartet (Strg+C zum Stoppen)")
    monitor.start_monitoring(interval=1)

if __name__ == "__main__":
    main()
