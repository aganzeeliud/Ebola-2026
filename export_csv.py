import sqlite3
import csv

def export_to_csv():
    conn = sqlite3.connect('ebola_outbreak.db')
    cursor = conn.cursor()

    query = '''
        SELECT 
            l.country, 
            l.province_region, 
            l.health_zone_city, 
            r.report_date, 
            r.confirmed_cases, 
            r.confirmed_deaths, 
            r.recoveries,
            o.name as outbreak_name,
            o.virus_strain
        FROM reports r
        JOIN locations l ON r.location_id = l.id
        JOIN outbreaks o ON r.outbreak_id = o.id
    '''
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    headers = [description[0] for description in cursor.description]
    
    with open('ebola_outbreak_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    conn.close()
    print("Data exported to ebola_outbreak_data.csv successfully.")

if __name__ == "__main__":
    export_to_csv()
