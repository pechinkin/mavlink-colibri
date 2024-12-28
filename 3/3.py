import sqlite3
import json
from datetime import datetime


class DroneChecker:
    def __init__(self, db_name="drones.db"):
        self.db_name = db_name
        self._initialize_database()

    def _initialize_database(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS drones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    drone_id TEXT NOT NULL,
                    battery_level INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def log_drone_data(self, drone_data):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO drones (drone_id, battery_level, status, timestamp)
                VALUES (?, ?, ?, ?)
            """, (drone_data["drone_id"], drone_data["battery_level"], drone_data["status"], timestamp))
            conn.commit()

    def process_drone_data(self, drone_data):
        self.log_drone_data(drone_data)
        print(f"уровень заряда батареи дрона {drone_data['drone_id']} = {drone_data['battery_level']}%")

        if drone_data['battery_level'] < 30:
            print("дрон стоит зарядить")
        else:
            print("дрон готов к запуску")


monitor = DroneChecker()

input_data = json.dumps({
    "drone_id": "drone_01",
    "battery_level": 75,
    "status": "ready"
})

drone_data = json.loads(input_data)
monitor.process_drone_data(drone_data)
