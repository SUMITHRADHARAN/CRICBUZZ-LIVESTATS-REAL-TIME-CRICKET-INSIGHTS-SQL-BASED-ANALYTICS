import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# ----------------- Database Connection -----------------
def create_connection():
    load_dotenv()
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return conn
    except Error as e:
        st.error(f"❌ Connection Error: {e}")
        return None

def run_query(conn, query):
    try:
        return pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"❌ Query Error: {e}")
        return None

# ----------------- Helper for Rendering -----------------
def render_result(result: pd.DataFrame):
    if result is None or result.empty:
        st.warning("⚠️ No results found for this specific criteria.")
    else:
        st.success(f"✅ Analysis Complete: Found {len(result)} records.")
        st.dataframe(result, use_container_width=True)
        
        # Auto-draw chart if numeric columns exist
        numeric_cols = result.select_dtypes(include=["int64", "float64"]).columns
        if len(numeric_cols) > 0:
            st.write("📊 **Data Visualization**")
            st.bar_chart(result.set_index(result.columns[0])[numeric_cols])

# ----------------- Query Dictionary -----------------
# ----------------- All 25 Queries Categorized (Anti-Duplicate Version) -----------------
QUERIES = {
    # Beginner (Q1-Q8)
    "Q1: List all Indian players with full name, role, batting style, and bowling style": """
        SELECT DISTINCT full_name AS player_name, playing_role, batting_style, bowling_style
        FROM players
        WHERE country = 'India';
    """,
    "Q2: Matches played in the last 30 days (most recent first)": """
        SELECT DISTINCT match_desc AS match_description, team1, team2, venue, start_date
        FROM recent_matches
        WHERE start_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
        ORDER BY start_date DESC;
    """,
    "Q3: Top 10 ODI run scorers with total runs, average, centuries": """
        SELECT DISTINCT player_name, runs AS total_runs, average AS batting_avg
        FROM top_odi_runs
        ORDER BY total_runs DESC
        LIMIT 10;
    """,
    "Q4: Venues with capacity over 50,000 (largest first)": """
        SELECT DISTINCT venue_name AS stadium_name, city, country, capacity
        FROM venues
        WHERE capacity >= 50000
        ORDER BY capacity DESC;
    """,
    "Q5: Total matches won by each team (most wins first)": """
        SELECT match_winner AS team_name, COUNT(DISTINCT match_id) AS total_wins
        FROM combined_matches
        GROUP BY team_name
        ORDER BY total_wins DESC;
    """,
    "Q6: Count of players by playing role": """
        SELECT playing_role AS role, COUNT(DISTINCT player_id) AS total_players
        FROM players
        GROUP BY role;
    """,
    "Q7: Highest individual batting score by format": """
        SELECT c.format AS match_format, MAX(b.runs) AS highest_score
        FROM batting_data b
        JOIN combined_matches c ON b.match_id = c.match_id
        GROUP BY match_format;
    """,
    "Q8: Series that started in 2024": """
        SELECT DISTINCT series_name AS series, venue, match_format AS format, start_date AS match_date
        FROM series_matches
        WHERE YEAR(start_date) = 2024
        ORDER BY match_date;
    """,

    # Intermediate (Q9-Q16)
    "Q9: Show allrounders with 1000+ runs & 50+ wickets": """
        SELECT DISTINCT name AS player_name, total_runs AS runs_scored, total_wickets AS wickets_taken
        FROM players
        WHERE (playing_role LIKE '%Allrounder%' OR playing_role LIKE '%All-rounder%')
          AND total_runs > 1000
          AND total_wickets > 50;
    """,
    "Q10: Last 20 completed matches victory margin overview": """
        SELECT DISTINCT match_desc, team1, team2, status as result
        FROM recent_matches
        WHERE state = 'Complete'
        ORDER BY start_date DESC
        LIMIT 20;
    """,
    "Q11: Players in multi-formats: Overall average calculation": """
        SELECT DISTINCT player_name, test_runs, odi_runs, t20_runs,
               ROUND((test_runs + odi_runs + t20_runs) / 3, 2) AS overall_avg
        FROM players_stats
        WHERE test_runs > 0 AND odi_runs > 0;
    """,
    "Q12: Home vs Away team win distribution": """
        SELECT match_winner, venue_country, COUNT(DISTINCT match_id) as wins
        FROM combined_matches
        GROUP BY match_winner, venue_country
        ORDER BY wins DESC;
    """,
    "Q13: Batting partnerships with combined runs >= 100": """
        SELECT DISTINCT batter1_name, batter2_name, runs_partnership
        FROM players_partnerships_data
        WHERE runs_partnership >= 100
        ORDER BY runs_partnership DESC;
    """,
    "Q14: Bowling performance at venues (Avg Economy)": """
        SELECT DISTINCT r.venue, 
               COUNT(DISTINCT b.match_id) as matches_played, 
               ROUND(AVG(b.economy_rate), 2) AS avg_economy
        FROM bowling_data b
        JOIN recent_matches r ON b.match_id = r.match_id
        GROUP BY r.venue
        HAVING matches_played >= 1;
    """,
    "Q15: Players in close matches (margin <50 runs or <5 wkts)": """
        SELECT p.name AS player_name, 
       ROUND(AVG(b.runs), 2) AS avg_runs, 
       COUNT(DISTINCT b.match_id) as games
        FROM batting_data b
        JOIN combined_matches c ON b.match_id = c.match_id
        JOIN players p ON b.player_id = p.player_id
        WHERE (c.win_margin_runs <= 50 AND c.win_margin_runs > 0)
            OR (c.win_margin_wickets <= 5 AND c.win_margin_wickets > 0)
        GROUP BY p.name;
    """,
    "Q16: Yearly run totals per player since 2020": """
        SELECT player_name, YEAR(match_date) AS year, SUM(runs) as total_yearly_runs
        FROM batting_data
        WHERE match_date >= '2020-01-01'
        GROUP BY player_name, year
        ORDER BY year DESC, total_yearly_runs DESC;
    """,

    # Advanced (Q17-Q25)
    "Q17: Toss decision impact: win % by toss choice": """
        SELECT toss_decision, 
               COUNT(DISTINCT match_id) AS total_matches,
               ROUND(SUM(CASE WHEN toss_winner = match_winner THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT match_id), 2) AS win_percentage
        FROM combined_matches
        GROUP BY toss_decision;
    """,
    "Q18: Most economical bowlers (Min 10 Overs)": """
        SELECT player_name, SUM(overs) as total_overs, ROUND(AVG(economy_rate), 2) as economy
        FROM bowling_data
        GROUP BY player_name
        HAVING total_overs >= 1
        ORDER BY economy ASC;
    """,
    "Q19: Player consistency: Standard Deviation of runs": """
        SELECT player_name, ROUND(AVG(runs), 2) as avg_runs, ROUND(STDDEV(runs), 2) as run_stddev
        FROM batting_data
        GROUP BY player_name
        HAVING COUNT(DISTINCT match_id) >= 2
        ORDER BY run_stddev ASC;
    """,
    "Q20: Matches & batting avg by format": """
        SELECT player_name, format, COUNT(DISTINCT match_id) as matches, ROUND(AVG(runs), 2) as avg_score
        FROM batting_data
        GROUP BY player_name, format
        ORDER BY player_name;
    """,
    "Q21: Composite performance ranking (Runs & Wickets)": """
        SELECT DISTINCT name, (total_runs * 0.4 + total_wickets * 20) AS performance_score
        FROM players
        ORDER BY performance_score DESC;
    """,
    "Q22: Venue Country Advantage (Home Wins)": """
        SELECT venue_country, COUNT(DISTINCT match_id) as home_wins
        FROM combined_matches
        WHERE venue_country = team_country
        GROUP BY venue_country;
    """,
    "Q23: Impact Players: High Strike Rate (>150) in innings": """
        SELECT DISTINCT player_name, runs, strike_rate, match_date
        FROM batting_data
        WHERE strike_rate > 150 AND runs > 30;
    """,
    "Q24: Career partnership pair totals": """
        SELECT batter1_name, batter2_name, SUM(runs_partnership) as career_runs
        FROM players_partnerships_data
        GROUP BY batter1_name, batter2_name
        ORDER BY career_runs DESC;
    """,
    "Q25: Efficiency Metrics: Runs per wicket (Bowling Avg)": """
        SELECT player_name, ROUND(SUM(runs_conceded) / SUM(wickets), 2) as bowling_avg
        FROM bowling_data
        GROUP BY player_name
        HAVING SUM(wickets) > 0
        ORDER BY bowling_avg ASC;
    """
}


# ----------------- Streamlit UI -----------------
def show_sql_queries():
    """
    Displays the SQL Analytics page with stylized query blocks and categorized Tabs.
    """
    # Stylized CSS for the UI, Buttons, and Transparent Expander
    st.markdown("""
        <style>
        /* General text colors */
        .stApp [data-testid="stVerticalBlock"] p, h1, h2, h3, span, label { 
            color: #1a1a2e !important; 
        }
        
        /* Stylized 'Run Query' Button */
        div.stButton > button {
            background: linear-gradient(135deg, #800000, #B22222) !important;
            color: #FFD700 !important;
            border-radius: 30px !important;
            border: none !important;
            padding: 10px 25px !important;
            font-weight: bold !important;
            width: auto !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
            transition: 0.3s;
        }
        div.stButton > button:hover {
            transform: scale(1.05) !important;
            color: #fffaf0 !important;
        }

        /* Query Title Box */
        .query-title {
            background-color: #1a1a2e;
            color: white;
            padding: 12px 18px;
            border-radius: 10px 10px 0 0;
            font-weight: bold;
            border-left: 6px solid #800000;
            margin-top: 15px;
        }

        /* SQL Code Box */
        .query-code {
            background-color: #262730;
            color: #dcdcdc;
            padding: 20px;
            border-radius: 0 0 10px 10px;
            font-family: 'Courier New', monospace;
            margin-bottom: 20px;
            line-height: 1.6;
            white-space: pre-wrap;
            border: 1px solid #444;
        }

        /* Fix for Expander: Keep background transparent all the time */
        [data-testid="stExpander"] summary {
            background-color: transparent !important;
            transition: none !important;
        }
        [data-testid="stExpander"] summary:hover, 
        [data-testid="stExpander"] summary:focus, 
        [data-testid="stExpander"] summary:active {
            background-color: transparent !important;
            outline: none !important;
            box-shadow: none !important;
        }
        [data-testid="stExpander"] summary p {
            color: #1a1a2e !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🔍 SQL Analytics & Insights")
    st.info("💡 Select a research question to view its SQL logic and run analysis.")

    conn = create_connection()
    if conn is None:
        st.warning("⚠️ Database connection offline. Please check your MySQL service.")
        return

    # --- TABBED INTERFACE ---
    tab1, tab2, tab3, tab4 = st.tabs(["🌱 Beginner", "⚡ Intermediate", "🚀 Advanced", "🛠️ SQL Playground"])

    def display_query_preview(label, sql):
        st.markdown(f'<div class="query-title">{label}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="query-code">{sql}</div>', unsafe_allow_html=True)

    def get_queries_by_range(start, end):
        return [k for k in QUERIES.keys() if any(f"Q{i}:" in k for i in range(start, end+1))]

    with tab1:
        st.subheader("Beginner Research Questions")
        choice = st.selectbox("🎯 Pick a Beginner Query", get_queries_by_range(1, 8), key="beg_sel")
        display_query_preview(choice, QUERIES[choice])
        if st.button("Run Query", key="beg_btn"):
            render_result(run_query(conn, QUERIES[choice]))

    with tab2:
        st.subheader("Intermediate Research Questions")
        choice = st.selectbox("🎯 Pick an Intermediate Query", get_queries_by_range(9, 16), key="int_sel")
        display_query_preview(choice, QUERIES[choice])
        if st.button("Run Query", key="int_btn"):
            render_result(run_query(conn, QUERIES[choice]))

    with tab3:
        st.subheader("Advanced Research Questions")
        choice = st.selectbox("🎯 Pick an Advanced Query", get_queries_by_range(17, 25), key="adv_sel")
        display_query_preview(choice, QUERIES[choice])
        if st.button("Run Query", key="adv_btn"):
            render_result(run_query(conn, QUERIES[choice]))

    with tab4:
        st.subheader("🛠️ Custom SQL Query")
        query_input = st.text_area("Enter your SQL query below:", height=150, placeholder="SELECT * FROM players LIMIT 10;")
        if st.button("Run Query", key="custom_btn"):
            if query_input.strip():
                render_result(run_query(conn, query_input))
            else:
                st.warning("Please enter a query to run.")

    conn.close()

    # --- DOCUMENTATION ---
    with st.expander("📖 View Available Tables & Documentation"):
        st.markdown("""

        | Table Name | Description |
        | :--- | :--- |
        | `players` | Contains player information. |
        | `recent_matches` | Contains details of recent matches. |
        | `top_odi_runs` | Contains top ODI run scorers. |
        | `venues` | Contains venue and stadium information. |
        | `combined_matches` | A unified view of all matches. |
        | `batting_data` | Contains detailed batting performance data. |
        | `series_matches` | Contains information about different series. |
        | `players_stats` | Contains player statistics. |
        | `players_partnerships_data` | Contains batting partnerships data. |
        | `bowlers_bowling_venue_data` | Contains bowling stats at specific venues. |
        | `batters_batting_data` | Contains detailed batting stats for batters. |
        | `bowling_data` | Contains bowling data. |
        | `fielding_data` | Contains fielding data. |
        """)


