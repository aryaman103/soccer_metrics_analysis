import streamlit as st
import pandas as pd
import sys
sys.path.append('scripts')
sys.path.append('visualizations')
from scripts.load_and_parse import load_statsbomb_data, get_top_shot_takers, get_top_progressive_passers
from visualizations.shot_map_visualizer import create_shot_map

st.set_page_config(page_title="MatchMetrics Explorer", page_icon="⚽", layout="wide", initial_sidebar_state="expanded")

# Enhanced custom dark theme styling
st.markdown(
    """
    <style>
    .stApp { background-color: #101014; }
    section[data-testid="stSidebar"] {
        background-color: #181a20 !important;
        border-right: 1.5px solid #23242a;
    }
    .sidebar-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #fff;
        margin-bottom: 1.2em;
        display: flex;
        align-items: center;
        gap: 0.5em;
    }
    .sidebar-radio {
        background: #23242a;
        border-radius: 12px;
        padding: 1em 0.5em 1em 0.5em;
        margin-bottom: 2em;
        box-shadow: 0 2px 8px #0002;
    }
    .stRadio > div { flex-direction: column; }
    .stRadio label {
        color: #f5f5f5 !important;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5em;
    }
    .stRadio [data-baseweb="radio"]:hover {
        background: #23242a33;
    }
    .stRadio [aria-checked="true"] {
        background: #2e2e38 !important;
        border-radius: 8px;
        box-shadow: 0 0 0 2px #ff3c6f;
    }
    .stMetric {
        background: #181a20;
        border-radius: 10px;
        padding: 1em;
        margin-bottom: 0.5em;
        color: #ff3c6f;
        font-weight: bold;
    }
    .section-card {
        background: #181a20;
        border-radius: 16px;
        padding: 2em 2em 1.5em 2em;
        margin-bottom: 2em;
        box-shadow: 0 4px 24px #0003;
    }
    .section-header {
        color: #ff3c6f;
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.5em;
    }
    .stDataFrame, .stTable {
        background: #23242a !important;
        color: #f5f5f5 !important;
        border-radius: 10px;
        box-shadow: 0 2px 8px #0002;
    }
    .footer {
        color: #888;
        font-size: 0.9em;
        text-align: right;
        margin-top: 2em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar title and radio
with st.sidebar:
    st.markdown('<div class="sidebar-title">📊 Statistics</div>', unsafe_allow_html=True)
    section = st.radio(
        "",
        ["Top Shot-Takers", "Top Progressive Passers", "Shot Maps"],
        index=0,
        key="sidebar-radio",
        help="Select a statistics section to explore."
    )
    st.markdown("<div class='footer'>MatchMetrics Explorer</div>", unsafe_allow_html=True)

@st.cache_data
def load_cached_data():
    df_shots, df_passes = load_statsbomb_data()
    return df_shots, df_passes

@st.cache_data
def get_cached_top_shot_takers(df_shots):
    return get_top_shot_takers(df_shots)

@st.cache_data
def get_cached_top_progressive_passers(df_passes):
    return get_top_progressive_passers(df_passes)


def main():
    st.title("⚽ MatchMetrics Explorer")
    st.markdown("Tactical Analysis Toolkit using StatsBomb Open Data")
    df_shots, df_passes = load_cached_data()
    if df_shots.empty or df_passes.empty:
        st.error("No data found! Please ensure you have StatsBomb JSON files in the `data/` directory.")
        return
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Events", len(df_shots) + len(df_passes))
    with col2:
        st.metric("Total Shots", len(df_shots))
    with col3:
        st.metric("Total Passes", len(df_passes))
    with col4:
        st.metric("Unique Players", df_shots['player.name'].nunique() + df_passes['player.name'].nunique())
    st.markdown("---")

    if section == "Top Shot-Takers":
        st.header("🎯 Top Shot-Takers")
        st.markdown("""
        - Across all matches or filtered by team/competition
        - Shots per 90 mins (not just raw count)
        - Optional: Include **xG per shot** for shot quality (if available)
        """)
        teams = sorted(df_shots['team.name'].dropna().unique())
        # Add quick filter buttons for Real Madrid, Spain, Man United
        st.subheader("Quick Filters:")
        col1, col2, col3 = st.columns(3)
        quick_selected = None
        with col1:
            if st.button("🇪🇸 Real Madrid", key="rm_btn"):
                st.session_state.selected_team = "Real Madrid"
        with col2:
            if st.button("🇪🇸 Spain", key="spain_btn"):
                st.session_state.selected_team = "Spain"
        with col3:
            if st.button("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Manchester United", key="mu_btn"):
                st.session_state.selected_team = "Manchester United"
        # Team dropdown
        default_team = getattr(st.session_state, 'selected_team', "All")
        if default_team not in ["All"] + teams:
            default_team = "All"
        selected_team = st.selectbox("Filter by team (optional):", ["All"] + teams, 
                                   index=0 if default_team == "All" else teams.index(default_team) + 1)
        filtered_shots = df_shots if selected_team == "All" else df_shots[df_shots['team.name'] == selected_team]
        shot_counts = get_cached_top_shot_takers(filtered_shots)
        st.subheader("Top 10 Shot Takers (by count)")
        st.dataframe(shot_counts)
        if 'shot.statsbomb_xg' in filtered_shots.columns:
            xg_stats = filtered_shots.groupby('player.name').agg(
                shots=('id', 'count'),
                avg_xg=('shot.statsbomb_xg', 'mean')
            ).sort_values('shots', ascending=False).head(10)
            st.subheader("xG per Shot (Top 10)")
            st.dataframe(xg_stats)
    elif section == "Top Progressive Passers":
        st.header("⚡ Top Progressive Passers")
        st.markdown("""
        - Per team and per player
        - Option to define **progressive pass** as:
            - A pass that moves the ball forward at least X meters and ends closer to goal
            - Or use `pass.end_location - pass.start_location` with thresholds
        """)
        threshold = st.slider("Minimum forward distance for progressive pass (meters):", 5, 30, 10)
        progressive_passes = df_passes.copy()
        progressive_passes['start_x'] = progressive_passes['location'].apply(lambda x: x[0] if isinstance(x, (list, tuple)) and len(x) >= 2 else None)
        progressive_passes['end_x'] = progressive_passes['pass.end_location'].apply(lambda x: x[0] if isinstance(x, (list, tuple)) and len(x) >= 2 else None)
        progressive_passes['forward_distance'] = progressive_passes['end_x'] - progressive_passes['start_x']
        progressive_passes = progressive_passes[(progressive_passes['forward_distance'] > threshold) & (progressive_passes['forward_distance'].notna())]
        top_players = progressive_passes.groupby('player.name').size().reset_index(name='progressive_pass_count').sort_values('progressive_pass_count', ascending=False).head(10)
        top_teams = progressive_passes.groupby('team.name').size().reset_index(name='progressive_pass_count').sort_values('progressive_pass_count', ascending=False).head(10)
        st.subheader("Top 10 Progressive Passers (Players)")
        st.dataframe(top_players)
        st.subheader("Top 10 Progressive Passers (Teams)")
        st.dataframe(top_teams)
    elif section == "Shot Maps":
        st.header("🗺️ Shot Maps")
        st.markdown("Select a player to view their shot map and stats.")
        players = sorted(df_shots['player.name'].unique())
        selected_player = st.selectbox("Select a player:", players)
        if selected_player:
            player_shots = df_shots[df_shots['player.name'] == selected_player]
            total_shots = len(player_shots)
            goals = len(player_shots[player_shots['shot.outcome.name'] == 'Goal'])
            conversion_rate = (goals / total_shots * 100) if total_shots > 0 else 0
            st.metric("Total Shots", total_shots)
            st.metric("Goals", goals)
            st.metric("Conversion Rate", f"{conversion_rate:.1f}%")
            st.metric("Team", player_shots['team.name'].iloc[0] if not player_shots.empty else "N/A")
            st.subheader(f"Shot Map: {selected_player}")
            fig = create_shot_map(df_shots, selected_player)
            if fig:
                st.pyplot(fig)

if __name__ == "__main__":
    main() 