import sqlite3

def get_summary():
    conn = sqlite3.connect('ebola_outbreak.db')
    cursor = conn.cursor()

    query = '''
        SELECT 
            hc.country, 
            SUM(r.confirmed_cases) as total_cases, 
            SUM(r.confirmed_deaths) as total_deaths,
            SUM(r.recoveries) as total_recoveries
        FROM reports r
        JOIN health_centers hc ON r.health_center_id = hc.id
        GROUP BY hc.country
    '''
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    print(f"{'Country':<10} | {'Cases':<6} | {'Deaths':<6} | {'Recoveries':<10}")
    print("-" * 45)
    
    total_cases = 0
    total_deaths = 0
    for country, cases, deaths, recoveries in results:
        print(f"{country:<10} | {cases:<6} | {deaths:<6} | {recoveries:<10}")
        total_cases += cases
        total_deaths += deaths
        
    print("-" * 45)
    print(f"{'TOTAL':<10} | {total_cases:<6} | {total_deaths:<6}")

    conn.close()

if __name__ == "__main__":
    get_summary()
