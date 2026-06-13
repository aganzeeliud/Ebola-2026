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
            health_center_id INTEGER,
            report_date DATE,
            confirmed_cases INTEGER DEFAULT 0,
            confirmed_deaths INTEGER DEFAULT 0,
            recoveries INTEGER DEFAULT 0,
            probable_cases INTEGER DEFAULT 0,
            probable_deaths INTEGER DEFAULT 0,
            notes TEXT,
            FOREIGN KEY (outbreak_id) REFERENCES outbreaks (id),
            FOREIGN KEY (health_center_id) REFERENCES health_centers (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS health_centers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT,
            latitude REAL,
            longitude REAL,
            country TEXT,
            province TEXT,
            city_zone TEXT
        )
    ''')

    # Insert initial outbreak data
    cursor.execute('''
        INSERT INTO outbreaks (name, virus_strain, declaration_date, status)
        VALUES (?, ?, ?, ?)
    ''', ("2026 Bundibugyo Ebola Outbreak", "Bundibugyo virus (BDBV)", "2026-05-15", "Ongoing"))
    outbreak_id = cursor.lastrowid

    # Health Centers Data
    # Format: (name, type, lat, lon, country, province, zone)
    health_centers_data = [
        ("CME Nyakunde (Bunia)", "Ebola Treatment Center", 1.53867, 30.24895, "DRC", "Ituri", "Bunia"),
        ("Mongbwalu General Referral Hospital", "Ebola Treatment Center", 1.92930, 30.04919, "DRC", "Ituri", "Mongbwalu"),
        ("Rwampara General Referral Hospital", "Ebola Treatment Center", 1.54348, 30.17918, "DRC", "Ituri", "Rwampara"),
        ("Aru General Referral Hospital", "Ebola Treatment Center", 2.85902, 30.83841, "DRC", "Ituri", "Aru"),
        ("Kasenye Treatment Center", "Ebola Treatment Center", 1.39197, 30.44024, "DRC", "Ituri", "Other Health Zones"),
        ("Beni General Referral Hospital", "Ebola Treatment Center", 0.4911, 29.4731, "DRC", "North Kivu", "Beni"),
        ("Hôpital de l’Amitié Sino-Congolaise", "Isolation Center", -4.40334, 15.37416, "DRC", "Kinshasa", "Kinshasa"),
        ("Miti-Murhesa Health Center", "Isolation Center", -2.3667, 28.8000, "DRC", "South Kivu", "Miti-Murhesa"),
        ("Mulago National Referral Hospital", "Isolation Unit", 0.33779, 32.57555, "Uganda", "Central", "Kampala"),
        ("Entebbe Regional Referral Hospital", "Isolation Unit", 0.06387, 32.47166, "Uganda", "Wakiso", "Wakiso"),
        ("Bwera General Hospital", "Border Screening ETC", 0.0333, 29.7667, "Uganda", "Kasese", "Border Zones")
    ]

    hc_map = {}
    for name, hc_type, lat, lon, country, province, zone in health_centers_data:
        cursor.execute('''
            INSERT INTO health_centers (name, type, latitude, longitude, country, province, city_zone)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, hc_type, lat, lon, country, province, zone))
        hc_map[name] = cursor.lastrowid

    # Reports Data (Cases assigned to Health Centers)
    # Format: (hc_name, cases, deaths, recoveries)
    reports_data = [
        ("CME Nyakunde (Bunia)", 150, 30, 5),
        ("Mongbwalu General Referral Hospital", 120, 25, 3),
        ("Rwampara General Referral Hospital", 100, 20, 2),
        ("Aru General Referral Hospital", 80, 15, 1),
        ("Kasenye Treatment Center", 179, 39, 1),
        ("Beni General Referral Hospital", 44, 10, 0),
        ("Hôpital de l’Amitié Sino-Congolaise", 13, 0, 0),
        ("Miti-Murhesa Health Center", 3, 0, 0),
        ("Mulago National Referral Hospital", 8, 1, 3),
        ("Entebbe Regional Referral Hospital", 1, 0, 1),
        ("Bwera General Hospital", 10, 1, 1)
    ]

    report_date = "2026-06-12"

    for hc_name, cases, deaths, recoveries in reports_data:
        hc_id = hc_map.get(hc_name)
        cursor.execute('''
            INSERT INTO reports (outbreak_id, health_center_id, report_date, confirmed_cases, confirmed_deaths, recoveries)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (outbreak_id, hc_id, report_date, cases, deaths, recoveries))

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
