import sqlite3
import json

def generate_js_data():
    conn = sqlite3.connect('ebola_outbreak.db')
    cursor = conn.cursor()

    # Get Health Zone Data
    query_zones = '''
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
    
    cursor.execute(query_zones)
    rows_zones = cursor.fetchall()
    
    zones_data = []
    for country, province, zone, lat, lon, cases, deaths, recov in rows_zones:
        cfr = (deaths / cases * 100) if cases > 0 else 0
        zones_data.append({
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

    # Get Health Center Data
    query_hc = '''
        SELECT name, type, latitude, longitude
        FROM health_centers
    '''
    cursor.execute(query_hc)
    rows_hc = cursor.fetchall()

    hc_data = []
    for name, hc_type, lat, lon in rows_hc:
        hc_data.append({
            "name": name,
            "type": hc_type,
            "lat": lat,
            "lon": lon
        })

    final_data = {
        "ebolaData": zones_data,
        "healthCenters": hc_data
    }

    with open('data.js', 'w') as f:
        f.write("var ebolaMapData = " + json.dumps(final_data, indent=4) + ";")

    conn.close()
    print("Map data generated in data.js")

if __name__ == "__main__":
    generate_js_data()
