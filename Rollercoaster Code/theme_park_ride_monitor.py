from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import random
import datetime

app = Flask(__name__)
DATABASE = 'ride_data.db'

def init_db():
    """
    Initialize the SQLite database.
    Creates a table 'ride_data' if it doesn't already exist.
    The table stores an auto-incremented ID, timestamp, ride name, speed, g-force, and ride section.
    """
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS ride_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    ride_name TEXT,
                    speed REAL,
                    g_force REAL,
                    section TEXT
                )''')
    conn.commit()
    conn.close()

def simulate_ride_data():
    """
    Simulates performance data for the "ThunderBolt Coaster".
    Generates:
      - A random speed (in km/h) between 80 and 120.
      - A random g-force between 2.5 and 5.0.
      - A ride section randomly chosen from a list (e.g., "Ascent", "First Drop", "Loop", "Brake Run", "Mid-course Boost").
      - The current timestamp.
    Returns a tuple with these values.
    """
    ride_name = "ThunderBolt Coaster"  # Name of the ride
    speed = round(random.uniform(80.0, 120.0), 2)  # Speed in km/h
    g_force = round(random.uniform(2.5, 5.0), 2)     # G-force experienced
    sections = ["Ascent", "First Drop", "Loop", "Brake Run", "Mid-course Boost"]
    section = random.choice(sections)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return (timestamp, ride_name, speed, g_force, section)

def insert_ride_data(data):
    """
    Inserts a simulated ride data record into the 'ride_data' table.
    """
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('INSERT INTO ride_data (timestamp, ride_name, speed, g_force, section) VALUES (?, ?, ?, ?, ?)', data)
    conn.commit()
    conn.close()

def get_all_ride_data():
    """
    Retrieves all ride data records from the database, ordered by newest first.
    """
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM ride_data ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    return rows

@app.route('/')
def index():
    """
    Home route:
    - Generates a new simulated ride reading each time the page is loaded.
    - Inserts this data into the SQLite database.
    - Retrieves all stored ride data and passes it to the dashboard for display.
    """
    data = simulate_ride_data()
    insert_ride_data(data)
    ride_data = get_all_ride_data()
    return render_template('index.html', ride_data=ride_data)

@app.route('/clear', methods=['POST'])
def clear_data():
    """
    Clears all ride performance data from the database.
    Activated via a button on the dashboard.
    """
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('DELETE FROM ride_data')
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # Ensure the database and table are initialized.
    app.run(debug=True)