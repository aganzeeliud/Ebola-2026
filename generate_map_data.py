import sqlite3
import json

def generate_js_data():
    conn = sqlite3.connect('ebola_outbreak.db')
    cursor = conn.cursor()

    query = '''
        SELECT 
            l.country, 
            l.province_region, 
            l.health_zone_city, 
            l.latitude, 
            l.longitude,
            r.confirmed_cases, 
            r.confirmed_deaths, 
            r.recoveries
        FROM reports r
        JOIN locations l ON r.location_id = l.id
    '''
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    map_data = []
    for country, province, zone, lat, lon, cases, deaths, recov in rows:
        cfr = (deaths / cases * 100) if cases > 0 else 0
        map_data.append({
            "country": country,
            "province": province,
            "city": zone,
            "lat": lat,
            "lon": lon,
            "cases": cases,
            "deaths": deaths,
            "recoveries": recov,
            "cfr": round(cfr, 1)
        })

    with open('data.js', 'w') as f:
        f.write("var ebolaData = " + json.dumps(map_data, indent=4) + ";")

    conn.close()
    print("Map data generated in data.js")

if __name__ == "__main__":
    generate_js_data()
