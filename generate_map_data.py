import sqlite3
import json

def generate_js_data():
    conn = sqlite3.connect('ebola_outbreak.db')
    cursor = conn.cursor()

    # Get Reports linked to Health Centers
    query = '''
        SELECT 
            hc.name, 
            hc.type, 
            hc.latitude, 
            hc.longitude, 
            hc.country, 
            hc.province, 
            hc.city_zone,
            r.confirmed_cases, 
            r.confirmed_deaths, 
            r.recoveries,
            r.report_date
        FROM reports r
        JOIN health_centers hc ON r.health_center_id = hc.id
    '''
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    map_data = []
    for name, hc_type, lat, lon, country, province, zone, cases, deaths, recov, date in rows:
        cfr = (deaths / cases * 100) if cases > 0 else 0
        map_data.append({
            "hc_name": name,
            "hc_type": hc_type,
            "country": country,
            "province": province,
            "zone": zone,
            "lat": lat,
            "lon": lon,
            "cases": cases,
            "deaths": deaths,
            "recoveries": recov,
            "cfr": round(cfr, 1),
            "date": date
        })

    with open('data.js', 'w') as f:
        f.write("var ebolaMapData = " + json.dumps(map_data, indent=4) + ";")

    conn.close()
    print("Map data generated in data.js")

if __name__ == "__main__":
    generate_js_data()
