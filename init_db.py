import sqlite3
import datetime

def init_db():
    conn = sqlite3.connect('ebola_outbreak.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS outbreaks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            virus_strain TEXT,
            declaration_date DATE,
            status TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country TEXT NOT NULL,
            province_region TEXT,
            health_zone_city TEXT,
            latitude REAL,
            longitude REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            outbreak_id INTEGER,
            location_id INTEGER,
            report_date DATE,
            confirmed_cases INTEGER DEFAULT 0,
            confirmed_deaths INTEGER DEFAULT 0,
            recoveries INTEGER DEFAULT 0,
            probable_cases INTEGER DEFAULT 0,
            probable_deaths INTEGER DEFAULT 0,
            notes TEXT,
            FOREIGN KEY (outbreak_id) REFERENCES outbreaks (id),
            FOREIGN KEY (location_id) REFERENCES locations (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS health_centers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT,
            latitude REAL,
            longitude REAL,
            location_id INTEGER,
            FOREIGN KEY (location_id) REFERENCES locations (id)
        )
    ''')

    # Insert initial outbreak data
    cursor.execute('''
        INSERT INTO outbreaks (name, virus_strain, declaration_date, status)
        VALUES (?, ?, ?, ?)
    ''', ("2026 Bundibugyo Ebola Outbreak", "Bundibugyo virus (BDBV)", "2026-05-15", "Ongoing"))
    outbreak_id = cursor.lastrowid

    # Locations and Reports (Data as of June 12, 2026)
    # Format: (country, province, zone, lat, lon, cases, deaths, recoveries)
    data = [
        # DRC - Ituri
        ("DRC", "Ituri", "Bunia", 1.5670, 30.2500, 150, 30, 5),
        ("DRC", "Ituri", "Mongbwalu", 1.9352, 30.0462, 120, 25, 3),
        ("DRC", "Ituri", "Rwampara", 1.5167, 30.2167, 100, 20, 2),
        ("DRC", "Ituri", "Aru", 2.8617, 30.8333, 80, 15, 1),
        ("DRC", "Ituri", "Other Health Zones (15)", 1.5000, 30.0000, 179, 39, 1),
        # DRC - North Kivu
        ("DRC", "North Kivu", "Beni", 0.4911, 29.4731, 44, 10, 0),
        # DRC - South Kivu
        ("DRC", "South Kivu", "Miti-Murhesa", -2.3667, 28.8000, 3, 0, 0),
        # DRC - Kinshasa
        ("DRC", "Kinshasa", "Kinshasa", -4.3222, 15.3119, 13, 0, 0),
        # Uganda
        ("Uganda", "Central", "Kampala", 0.3476, 32.5825, 8, 1, 3),
        ("Uganda", "Central", "Wakiso", 0.4000, 32.4825, 1, 0, 1),
        ("Uganda", "Border/Imported", "DRC Border Zones", 0.5000, 31.0000, 10, 1, 1)
    ]

    report_date = "2026-06-12"

    location_map = {} # Store zone -> id for health center linking

    for country, province, zone, lat, lon, cases, deaths, recoveries in data:
        cursor.execute('''
            INSERT INTO locations (country, province_region, health_zone_city, latitude, longitude)
            VALUES (?, ?, ?, ?, ?)
        ''', (country, province, zone, lat, lon))
        location_id = cursor.lastrowid
        location_map[zone] = location_id

        cursor.execute('''
            INSERT INTO reports (outbreak_id, location_id, report_date, confirmed_cases, confirmed_deaths, recoveries)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (outbreak_id, location_id, report_date, cases, deaths, recoveries))

    # Insert Health Centers
    health_centers = [
        ("CME Nyakunde (Bunia)", "Ebola Treatment Center", 1.53867, 30.24895, "Bunia"),
        ("Beni General Referral Hospital", "Ebola Treatment Center", 0.4911, 29.4731, "Beni"),
        ("Mongbwalu General Referral Hospital", "Ebola Treatment Center", 1.92930, 30.04919, "Mongbwalu"),
        ("Aru General Referral Hospital", "Ebola Treatment Center", 2.85902, 30.83841, "Aru"),
        ("Kasenye Treatment Center", "Ebola Treatment Center", 1.39197, 30.44024, "Other Health Zones (15)"),
        ("Mulago National Referral Hospital", "Isolation Unit", 0.33779, 32.57555, "Kampala")
    ]

    for name, hc_type, lat, lon, zone in health_centers:
        cursor.execute('''
            INSERT INTO health_centers (name, type, latitude, longitude, location_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, hc_type, lat, lon, location_map.get(zone)))

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
