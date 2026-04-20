import streamlit as st
import sys
import os

# 1. Page Configuration
st.set_page_config(
    page_title="🏏 Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Optimized CSS for Full Visibility
st.markdown("""
<style>
    /* 1. App Background & Global Text visibility */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #fffaf0 !important;
        color: #333333 !important;
    }

    /* 2. Main Header Banner with WHITE text */
    .main-header {
        text-align: center;
        padding: 2.5rem;
        background: linear-gradient(135deg, #800000, #B22222);
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.25);
        margin-bottom: 2rem;
    }
    .main-header h1 { 
        color: #ffffff !important; /* Title to White */
        margin: 0 !important; 
    }
    .main-header p { 
        color: #ffffff !important; /* Subtitle to White */
        font-size: 1.2rem !important;
        opacity: 1 !important;
    }

    /* 3. Sidebar Visibility Fixes */
    [data-testid="stSidebar"] {
        background-color: #fffaf0 !important; /* Match app background */
        border-right: 2px solid #B22222;
    }
    /* Force "Navigate to:" and Sidebar titles to Deep Maroon */
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] h2 {
        color: #800000 !important;
        font-weight: bold !important;
    }
    /* Dropdown text visibility */
    [data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 1px solid #B22222;
    }

    /* 4. Page Content Titles (Update Role, Delete, etc.) */
    h1, h2, h3, h4, label, .stMarkdown p {
        color: #4B0000 !important; /* Deep Maroon for visibility */
        font-weight: 600 !important;
    }

    /* 5. Input Fields (No more invisible typing) */
    input {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* 6. Buttons Styling - Maroon with Gold Text */
    div.stButton > button {
        background: linear-gradient(135deg, #B22222, #800000) !important;
        color: #FFD700 !important; /* Gold text */
        border-radius: 25px;
        border: 1px solid #FFD700 !important;
        font-weight: bold !important;
        width: 100%;
        padding: 0.6rem;
    }
    div.stButton > button:hover {
        color: #ffffff !important;
        background: #800000 !important;
    }

    /* 7. Cards & Metrics */
    .feature-card, .metric-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        text-align: center;
        border: 1px solid #f0e6d2;
    }

    /* Hide standard nav */
    [data-testid="stSidebarNav"] { display: none; }
</style>
""", unsafe_allow_html=True)

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    st.markdown("""
    <div class="main-header">
        <h1>🏏 Cricbuzz LiveStats</h1>
        <p>Real-Time Cricket Insights & SQL-Based Analytics</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar navigation
    with st.sidebar:
        st.markdown("<h2 style='text-align: center; color:#B22222;'>🏏 Menu</h2>", unsafe_allow_html=True)
        st.markdown("---")
        page = st.selectbox(
            "🧭 Navigate to:",
            ["🏠 Home", "⚡ Live Matches", "📊 Top Stats", "🔍 SQL Analytics", "🛠️ CRUD Operations"]
        )

    try:
        if page == "🏠 Home":
            show_home()
        elif page == "⚡ Live Matches":
            from pages.live_matches import show_live_matches
            show_live_matches()
        elif page == "📊 Top Stats":
            from pages.top_stats import show_top_stats
            show_top_stats()
        elif page == "🔍 SQL Analytics":
            from pages.sql_queries import show_sql_queries
            show_sql_queries()
        elif page == "🛠️ CRUD Operations":
            from pages.crud_operations import show_crud_operations
            show_crud_operations()
    except ImportError as e:
        st.error(f"Page file not found: {e}")
        st.warning("Create a corresponding file in the `pages` directory.")

def show_home():
    # --- Project Overview ---
    st.markdown("""
        ## 📖 Project Overview
        **Cricbuzz LiveStats** is a premier sports analytics platform designed to provide a 360-degree view of the cricketing world. 
        By harmonizing real-time data from the **Cricbuzz API** with the structured power of **SQL databases**, this dashboard 
        transforms complex statistics into actionable insights for fans, analysts, and sports media teams.
    """)

    st.markdown("---")
    
    # --- Tools & Tech Stack ---
    st.subheader("🛠️ Technology Stack")
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        st.info("**Frontend**  \nStreamlit (Python)")
    with t2:
        st.info("**Backend**  \nPython 3.x")
    with t3:
        st.info("**Database**  \nSQL (MySQL)")
    with t4:
        st.info("**Data Source**  \nCricbuzz REST API")

    st.markdown("---")

    # Feature cards section
    st.subheader("✨ Explore the Dashboard's Key Features")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<div class="feature-card"><div class="feature-icon">⚡</div><h4>Live Matches</h4><p>Real-time scores, updates, and commentary.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="feature-card"><div class="feature-icon">📊</div><h4>Top Stats</h4><p>Leaderboards for top batsmen and bowlers.</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="feature-card"><div class="feature-icon">🔍</div><h4>SQL Analytics</h4><p>Run custom queries on the database for deep insights.</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="feature-card"><div class="feature-icon">🛠️</div><h4>CRUD Operations</h4><p>Add, update, and manage your own data.</p></div>', unsafe_allow_html=True)

    st.markdown("---")

    # --- User Instructions & Navigation ---
    st.subheader("🧭 How to Navigate the Dashboard")
    nav_col1, nav_col2 = st.columns(2)
    
    with nav_col1:
        st.markdown("""
        #### **1. Tracking Live Games**
        *   **Go to:** `⚡ Live Matches`
        *   **Action:** Select a live series from the dropdown to see real-time scores.
        *   **Detail:** Click "View Scorecard" for full batting and bowling analysis.

        #### **2. Exploring Player Profiles**
        *   **Go to:** `📊 Top Stats`
        *   **Action:** Type a player's name (e.g., "Kohli") to see their ICC rankings and career history.
        """)

    with nav_col2:
        st.markdown("""
        #### **3. Running Data Analytics**
        *   **Go to:** `🔍 SQL Analytics`
        *   **Action:** Choose from 25 pre-built SQL questions to analyze consistency and team performance.
        
        #### **4. Managing Data (Admin)**
        *   **Go to:** `🛠️ CRUD Operations`
        *   **Action:** Use the forms to manually Add, Update, or Delete records in the local database.
        """)

    st.markdown("---")

    
    # System Architecture Section
    st.subheader("🖼️ System Architecture at a Glance")
    with st.expander("🔌 API Integration"):
        st.code("""
import requests
import json

url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"
response = requests.get(url, headers=headers)
data = response.json()
        """, language="python")

    with st.expander("🗄️ Database Schema"):
        st.code("""
CREATE TABLE players (
    player_id INT PRIMARY KEY,
    name VARCHAR(100),
    team_id INT,
    playing_role VARCHAR(50)
);

CREATE TABLE matches (
    match_id INT PRIMARY KEY,
    series_id INT,
    venue VARCHAR(200)
);
        """, language="sql")

    st.markdown("---")

    # Project Statistics
    st.subheader("📊 Project Statistics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><div class="metric-value">12</div><div class="metric-label">📁 Total Files</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><div class="metric-value">7</div><div class="metric-label">🐍 Python Libraries</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><div class="metric-value">25</div><div class="metric-label">🔍 SQL Queries</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><div class="metric-value">14</div><div class="metric-label">🗄️ Database Tables</div></div>', unsafe_allow_html=True)
    

if __name__ == "__main__":
    main()