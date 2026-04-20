# pages/5_CRUD.py
import os
import streamlit as st
from utils.db_connection import run_query, execute_query

def show_crud_operations():
    

    # 1. READ: show existing players
    try:
        players = run_query("SELECT * FROM players;")
        st.subheader("Existing players")
        st.dataframe(players, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading database: {e}")
        return

    # 2. CREATE: Add / Upsert Player
    st.markdown("### ➕ Add / Upsert Player")
    with st.form("add_player"):
        pid = st.text_input("Player ID")
        mid = st.text_input("Match ID")
        team = st.text_input("Team Name")
        pname = st.text_input("Player Name")
        role = st.text_input("Role")
        sub = st.form_submit_button("Add / Update Player")
        
        if sub:
            q = "REPLACE INTO players (player_id, match_id, team_name, player_name, role) VALUES (%s, %s, %s, %s, %s)"
            ok = execute_query(q, (pid, mid, team, pname, role))
            if ok:
                st.success("Player added/updated.")
                st.rerun()
            else:
                st.error("Failed to add/update player.")

    # 3. UPDATE: Update Player Role
    st.markdown("### ✏️ Update Player Role")
    if not players.empty:
        sel = st.selectbox("Select player id", players["player_id"].unique().tolist())
        new_role = st.text_input("New role")
        if st.button("Update role"):
            # Filtering match_id to ensure specific record update
            m_id = players[players["player_id"]==sel].iloc[0]["match_id"]
            q_update = "UPDATE players SET role=%s WHERE player_id=%s AND match_id=%s"
            ok = execute_query(q_update, (new_role, sel, m_id))
            if ok:
                st.success("Role updated.")
                st.rerun()
            else:
                st.error("Update failed.")

    # 4. DELETE: Delete Player
    st.markdown("### 🗑️ Delete Player")
    del_id = st.text_input("Player ID to delete")
    if st.button("Delete player"):
        ok = execute_query("DELETE FROM players WHERE player_id=%s", (del_id,))
        if ok:
            st.success("Player deleted.")
            st.rerun()
        else:
            st.error("Delete failed.")