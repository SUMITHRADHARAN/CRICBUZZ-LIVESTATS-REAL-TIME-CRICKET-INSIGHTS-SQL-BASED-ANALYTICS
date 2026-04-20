# 🏏 Cricbuzz LiveStats: Real-Time Cricket Insights & SQL Analytics

Cricbuzz LiveStats is a high-performance sports analytics platform that harmonizes real-time data acquisition with deep-dive historical analysis. Developed using **Python**, **Streamlit**, and **SQL**, the platform serves as a unified ecosystem where users can track live match momentum, explore detailed player profiles, and execute complex analytical queries.

---

## 🚀 Features

*   **📊 Live Cricket Updates** – Fetches real-time match details, including scores, status, and venues.
*   **📝 Scorecards & Player Insights** – View batting, bowling, and player statistics at a glance.
*   **🎯 Interactive Streamlit Dashboard** – A clean, responsive UI with multi-dimensional filtering options.
*   **🗄️ Database Support** – A MySQL backend for robust data persistence.
*   **🔎 SQL Query Playground** – Write and execute custom SQL queries directly inside the app.
*   **🛠 CRUD Operations** – Add, update, delete, and view cricket data in real time.

---

## 🛠 Tech Stack

*   **Python** → Data fetching & processing.
*   **Streamlit** → Interactive web dashboard.
*   **MySQL** → Database storage & SQL analytics.
*   **REST API** (Cricbuzz via RapidAPI) → Source for live cricket data.
*   **Pandas** → Data manipulation and table rendering.

---

## 🗄️ Database Schema

The project integrates API data into a structured MySQL database (`cricket_db`) with the following tables:

*   **teams**: `team_id`, `team_name`, `short_name`.
*   **players**: `id`, `name`, `batting_style`, `bowling_style`, `country`, `team_id`.
*   **matches**: `id`, `series`, `format`, `teams`, `venue`, `status`.
*   **scores**: `runs`, `wickets`, `overs`, `innings`.
*   **venues**: `name`, `location`, `capacity`, `profile`.
*   **series**: `series_id`, `name`, `type`, `start_date`, `end_date`.
*   **player_stats**: `matches`, `innings`, `runs`, `average`, `type`.

---

## 🎯 Key Features Walkthrough

### 📊 Live Matches Dashboard
*   **Auto-Refresh:** The dashboard updates every 30 seconds for live scores.
*   **Filters:** Sift through data based on Match Format (Test, ODI, T20), specific Series, or Teams.
*   **Match Details:** Drill down into specific match events and ball-by-ball information.

### 📈 Top Stats & Analytics
*   **Leaderboards:** View batting leaders (runs, averages, strike rates) and bowling leaders (wickets, economy).
*   **Data Management:** Quickly refresh, clear, or regenerate data directly from the UI.

### 🖥️ SQL Query Playground
*   **Pre-Built Queries:** Instant access to common stats like "Venue Consistency" or "Clutch Performance."
*   **Custom Builder:** A dedicated space for users to write and execute their own SQL logic.
*   **Schema Explorer:** Interactive browser to visualize the database structure.

### ⚙️ CRUD Operations
*   **Governance:** An administrative interface to manage player profiles, match schedules, and performance records without requiring raw SQL access.

---

## 🔍 Analytical Insights

*   **International Dominance:** Top-tier international players consistently anchor the leaderboards across all formats.
*   **Infrastructure Hotspots:** High-capacity venues are geographically concentrated in India and Australia.
*   **Offensive Correlation:** Data shows a direct link between deep batting lineups and higher overall match win counts.
*   **Venue Advantage:** Historical analysis suggests specific teams maintain a statistically significant "home-ground" win rate.
*   **Strike Rate Trends:** Modern T20 players prioritize high strike rates over batting averages, visible in recent API datasets.
*   **Bowling Efficiency:** Spinners show better economy in subcontinental venues, while pacers dominate in conditions like Perth or London.

---

## 📌 Conclusion

The **Cricbuzz LiveStats System** demonstrates how fragmented sports data can be successfully consolidated into a unified environment. By bridging the gap between live REST API streams and relational database management, it provides a comprehensive toolkit for modern cricket analytics and data governance.

---

## 📂 Project Structure

```text
cricbuzz_livestats/
├── app.py              # Main entry point for the Streamlit app
├── requirements.txt    # Required Python packages
├── pages/              # Individual Streamlit pages
│   ├── home.py         # Overview and About
│   ├── live_matches.py # Live match data
│   ├── top_stats.py    # Batting/Bowling statistics
│   ├── sql_queries.py  # SQL analytics interface
│   └── crud_operations.py # Administrative data management
└── utils/
    └── db_connection.py # SQL database connection logic
