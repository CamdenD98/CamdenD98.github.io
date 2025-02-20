import sqlite3
import datetime
import random

# 1. Create or connect to a SQLite database and ensure the table exists.
def create_database(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id TEXT,
            reading REAL,
            timestamp TEXT
        )
    ''')
    conn.commit()
    return conn

# 2. Insert a new sensor reading into the database.
def insert_sensor_data(conn, sensor_id, reading):
    c = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    c.execute("INSERT INTO sensor_data (sensor_id, reading, timestamp) VALUES (?, ?, ?)", 
              (sensor_id, reading, timestamp))
    conn.commit()

# 3. Simulate readings for a list of sensors.
def simulate_sensor_readings(conn, sensors, num_readings=10):
    for _ in range(num_readings):
        for sensor in sensors:
            # Simulate a sensor reading (for example, between 20.0 and 100.0)
            reading = round(random.uniform(20.0, 100.0), 2)
            insert_sensor_data(conn, sensor, reading)
    print("Simulated sensor data inserted into database.")

# 4. Compute the average reading for each sensor.
def compute_average_readings(conn):
    c = conn.cursor()
    c.execute("SELECT sensor_id, AVG(reading) as avg_reading FROM sensor_data GROUP BY sensor_id")
    results = c.fetchall()
    return results

# 5. Generate a simple HTML dashboard to display the average readings.
def generate_html_report(averages, output_file='dashboard.html'):
    html_content = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sensor Data Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            table { border-collapse: collapse; width: 50%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h2>Sensor Data Dashboard</h2>
        <table>
            <tr>
                <th>Sensor ID</th>
                <th>Average Reading</th>
            </tr>
    '''
    for sensor_id, avg_reading in averages:
        html_content += f'''
            <tr>
                <td>{sensor_id}</td>
                <td>{avg_reading:.2f}</td>
            </tr>
        '''
    html_content += '''
        </table>
    </body>
    </html>
    '''
    with open(output_file, 'w') as f:
        f.write(html_content)
    print(f"Dashboard generated as {output_file}")

# 6. Main function to run the steps.
def main():
    db_name = 'sensor_data.db'
    conn = create_database(db_name)
    
    # List of sensor IDs (could correspond to actual hardware sensors)
    sensors = ['TempSensor1', 'PressureSensor1', 'HumiditySensor1']
    
    # Simulate and insert sensor readings into the database
    simulate_sensor_readings(conn, sensors, num_readings=10)
    
    # Compute and display the average reading for each sensor
    averages = compute_average_readings(conn)
    print("Average sensor readings:")
    for sensor, avg in averages:
        print(f"{sensor}: {avg:.2f}")
    
    # Generate a simple HTML dashboard to visualize the averages
    generate_html_report(averages)
    conn.close()

if __name__ == "__main__":
    main()