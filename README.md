# Ebola Outbreak Intelligence Dashboard (2026 & Historical)

An interactive geospatial and statistical platform for monitoring the 2026 Ebola outbreak in the Democratic Republic of the Congo (DRC) and Uganda, providing deep historical context dating back to 1976.

## 🚀 Live Dashboard
View the interactive map and analytics here:
**[https://aganzeeliud.github.io/Ebola-2026/map.html](https://aganzeeliud.github.io/Ebola-2026/map.html)**

## 📊 Project Overview
This project was developed to provide a centralized hub for Ebola outbreak intelligence. It combines a robust SQLite database back-end with a modern, responsive web dashboard built using Leaflet.js and Chart.js.

### Key Features:
- **Real-Time Outbreak Mapping:** Visualizes the 2026 Bundibugyo Ebola outbreak at the health-center level.
- **Historical Analysis:** Provides a longitudinal view of 25+ outbreaks across 50 years (1976–2026).
- **Interactive Data Visualization:** Includes bar charts for facility-level burden and line charts for historical trends.
- **Quick Stats Bar:** High-impact metrics for cases, deaths, recoveries, and Case Fatality Rate (CFR).
- **Comprehensive Data Ledger:** A searchable, dynamic table for granular data exploration.

## 🛠 Project Structure
- `ebola_outbreak.db`: SQLite database storing outbreak, location, and reporting data.
- `ebola_outbreak_data.csv`: Portable CSV export of the latest data.
- `init_db.py`: Python script to initialize the database and populate it with researched statistics.
- `generate_map_data.py`: Utility script to sync database data into `data.js` for the dashboard.
- `analysis.py`: Statistical analysis script calculating CFR and active cases.
- `queries.py`: Command-line utility for quick statistical summaries.
- `map.html`: The main interactive dashboard (HTML/CSS/JS).

## 🧪 Database Schema
The project uses a structured relational model:
- `outbreaks`: General info about the strain and status.
- `health_centers`: Detailed facility names and precise geocoordinates.
- `reports`: Daily/periodic statistics linked to specific facilities.
- `historical_outbreaks`: Archive of previous Ebola events (1976-2025).

## 📖 How to Use
1. **Initialize/Update Data:**
   ```bash
   python init_db.py
   ```
2. **Refresh Dashboard Data:**
   ```bash
   python generate_map_data.py
   ```
3. **Run Statistical Analysis:**
   ```bash
   python analysis.py
   ```
4. **View Map:** Open `map.html` in any modern web browser or host via GitHub Pages.

## 📚 Data Sources
- **2026 Outbreak:** World Health Organization (WHO), Africa CDC, Ministries of Health (DRC/Uganda).
- **Historical Archive:** CDC Ebola Distribution Map, WHO Global Health Observatory.
- **Geospatial:** OpenStreetMap contributors and IOM DTM.

## ⚖️ License
This project is for informational and educational purposes. Data is sourced from public domain health reports.
