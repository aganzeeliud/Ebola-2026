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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historical_outbreaks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER,
            country TEXT,
            location TEXT,
            virus_strain TEXT,
            cases INTEGER,
            deaths INTEGER
        )
    ''')

    # Insert Historical Data
    historical_data = [
        # DRC
        (1976, "DRC", "Yambuku", "Zaire (EBOV)", 318, 280),
        (1977, "DRC", "Tandala", "Zaire (EBOV)", 1, 1),
        (1995, "DRC", "Kikwit", "Zaire (EBOV)", 315, 254),
        (2007, "DRC", "Kasai Occidental", "Zaire (EBOV)", 264, 187),
        (2008, "DRC", "Kasai Occidental", "Zaire (EBOV)", 32, 14),
        (2012, "DRC", "Isiro", "Bundibugyo (BDBV)", 77, 36),
        (2014, "DRC", "Boende", "Zaire (EBOV)", 66, 49),
        (2017, "DRC", "Likati", "Zaire (EBOV)", 8, 4),
        (2018, "DRC", "Équateur (Bikoro)", "Zaire (EBOV)", 54, 33),
        (2018, "DRC", "North Kivu/Ituri", "Zaire (EBOV)", 3470, 2287),
        (2020, "DRC", "Équateur (Mbandaka)", "Zaire (EBOV)", 130, 55),
        (2021, "DRC", "North Kivu (Biena)", "Zaire (EBOV)", 12, 6),
        (2021, "DRC", "North Kivu (Beni)", "Zaire (EBOV)", 11, 9),
        (2022, "DRC", "Équateur (Mbandaka)", "Zaire (EBOV)", 5, 5),
        (2022, "DRC", "North Kivu (Beni)", "Zaire (EBOV)", 1, 1),
        (2025, "DRC", "Kasai (Bulape)", "Zaire (EBOV)", 64, 45),
        # Uganda
        (2000, "Uganda", "Gulu, Masindi, Mbarara", "Sudan (SUDV)", 425, 224),
        (2007, "Uganda", "Bundibugyo", "Bundibugyo (BDBV)", 149, 37),
        (2011, "Uganda", "Luwero", "Sudan (SUDV)", 1, 1),
        (2012, "Uganda", "Kibaale", "Sudan (SUDV)", 24, 17),
        (2012, "Uganda", "Luwero", "Sudan (SUDV)", 7, 4),
        (2019, "Uganda", "Kasese", "Zaire (EBOV)", 3, 3),
        (2022, "Uganda", "Mubende, Kassanda", "Sudan (SUDV)", 164, 77),
        (2025, "Uganda", "Kampala", "Sudan (SUDV)", 14, 4)
    ]

    for year, country, loc, strain, cases, deaths in historical_data:
        cursor.execute('''
            INSERT INTO historical_outbreaks (year, country, location, virus_strain, cases, deaths)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (year, country, loc, strain, cases, deaths))

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
