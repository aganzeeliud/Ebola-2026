import sqlite3
import json

def generate_js_data():
    conn = sqlite3.connect('ebola_outbreak.db')
    cursor = conn.cursor()

    # Get Current Reports (2026)
    query_2026 = '''
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
    cursor.execute(query_2026)
    rows_2026 = cursor.fetchall()
    
    current_data = []
    for name, hc_type, lat, lon, country, province, zone, cases, deaths, recov, date in rows_2026:
        cfr = (deaths / cases * 100) if cases > 0 else 0
        current_data.append({
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

    # Get Historical Data
    query_hist = '''
        SELECT year, country, location, virus_strain, cases, deaths
        FROM historical_outbreaks
        ORDER BY year ASC
    '''
    cursor.execute(query_hist)
    rows_hist = cursor.fetchall()
    
    historical_data = []
    for year, country, loc, strain, cases, deaths in rows_hist:
        historical_data.append({
            "year": year,
            "country": country,
            "location": loc,
            "strain": strain,
            "cases": cases,
            "deaths": deaths
        })

    final_data = {
        "ebolaMapData": current_data,
        "historicalData": historical_data
    }

    with open('data.js', 'w') as f:
        f.write("var ebolaFullData = " + json.dumps(final_data, indent=4) + ";")

    conn.close()
    print("Map and Historical data generated in data.js")

if __name__ == "__main__":
    generate_js_data()
