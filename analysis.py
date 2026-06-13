import sqlite3

def run_statistical_analysis():
    conn = sqlite3.connect('ebola_outbreak.db')
    cursor = conn.cursor()

    query = '''
        SELECT 
            l.country, 
            l.province_region, 
            l.health_zone_city, 
            r.confirmed_cases, 
            r.confirmed_deaths, 
            r.recoveries
        FROM reports r
        JOIN locations l ON r.location_id = l.id
    '''
    
    cursor.execute(query)
    rows = cursor.fetchall()

    print(f"{'Location':<30} | {'CFR %':<8} | {'Recov %':<8} | {'Active (Est)':<12}")
    print("-" * 65)

    grand_total_cases = 0
    grand_total_deaths = 0
    grand_total_recov = 0

    for country, province, zone, cases, deaths, recov in rows:
        cfr = (deaths / cases * 100) if cases > 0 else 0
        recov_rate = (recov / cases * 100) if cases > 0 else 0
        active = cases - deaths - recov
        
        loc_name = f"{zone} ({country})"
        print(f"{loc_name:<30} | {cfr:>7.1f}% | {recov_rate:>7.1f}% | {active:>12}")
        
        grand_total_cases += cases
        grand_total_deaths += deaths
        grand_total_recov += recov

    print("-" * 65)
    overall_cfr = (grand_total_deaths / grand_total_cases * 100) if grand_total_cases > 0 else 0
    overall_recov = (grand_total_recov / grand_total_cases * 100) if grand_total_cases > 0 else 0
    overall_active = grand_total_cases - grand_total_deaths - grand_total_recov
    
    print(f"{'OVERALL TOTAL':<30} | {overall_cfr:>7.1f}% | {overall_recov:>7.1f}% | {overall_active:>12}")

    conn.close()

if __name__ == "__main__":
    run_statistical_analysis()
