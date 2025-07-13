import json
import pandas as pd
from pathlib import Path

def convert_lists_to_tuples(df):
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, list)).any():
            df[col] = df[col].apply(lambda x: tuple(x) if isinstance(x, list) else x)
    return df

def add_sample_data(df_shots, df_passes):
    """Add sample data for Real Madrid, Manchester United, and Spain"""
    import random
    import uuid
    
    # Sample players for each team
    teams_players = {
        "Real Madrid": [
            "Karim Benzema", "Vinicius Jr.", "Luka Modric", "Toni Kroos", 
            "Federico Valverde", "Rodrygo", "Eduardo Camavinga", "Dani Carvajal"
        ],
        "Manchester United": [
            "Marcus Rashford", "Bruno Fernandes", "Jadon Sancho", "Anthony Martial",
            "Mason Greenwood", "Paul Pogba", "Luke Shaw", "Harry Maguire"
        ],
        "Spain": [
            "Alvaro Morata", "Pedri", "Gavi", "Sergio Busquets", 
            "Ferran Torres", "Dani Olmo", "Pau Torres", "Jordi Alba"
        ]
    }
    
    sample_shots = []
    sample_passes = []
    
    for team, players in teams_players.items():
        for player in players:
            # Generate shots for each player
            num_shots = random.randint(2, 8)
            for _ in range(num_shots):
                shot_data = {
                    'id': str(uuid.uuid4()),
                    'type.name': 'Shot',
                    'player.name': player,
                    'team.name': team,
                    'location': (random.uniform(90, 120), random.uniform(20, 60)),
                    'shot.outcome.name': 'Goal' if random.random() < 0.15 else 'Saved',
                    'shot.statsbomb_xg': random.uniform(0.02, 0.8),
                    'minute': random.randint(1, 90),
                    'second': random.randint(0, 59)
                }
                sample_shots.append(shot_data)
            
            # Generate passes for each player
            num_passes = random.randint(20, 50)
            for _ in range(num_passes):
                start_x = random.uniform(20, 100)
                end_x = start_x + random.uniform(-10, 25)
                pass_data = {
                    'id': str(uuid.uuid4()),
                    'type.name': 'Pass',
                    'player.name': player,
                    'team.name': team,
                    'location': (start_x, random.uniform(10, 70)),
                    'pass.end_location': (end_x, random.uniform(10, 70)),
                    'minute': random.randint(1, 90),
                    'second': random.randint(0, 59)
                }
                sample_passes.append(pass_data)
    
    # Convert to DataFrames
    if sample_shots:
        sample_shots_df = pd.DataFrame(sample_shots)
        sample_shots_df = convert_lists_to_tuples(sample_shots_df)
        df_shots = pd.concat([df_shots, sample_shots_df], ignore_index=True)
    
    if sample_passes:
        sample_passes_df = pd.DataFrame(sample_passes)
        sample_passes_df = convert_lists_to_tuples(sample_passes_df)
        df_passes = pd.concat([df_passes, sample_passes_df], ignore_index=True)
    
    return df_shots, df_passes

def load_statsbomb_data(data_dir='data'):
    data_path = Path(data_dir)
    events_files = list(data_path.glob('**/*events*.json'))
    if not events_files:
        print(f"No events JSON files found in {data_path}")
        return pd.DataFrame(), pd.DataFrame()
    all_events = []
    for file_path in events_files:
        try:
            print(f"Loading {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                df = pd.json_normalize(data)
                df = convert_lists_to_tuples(df)
                all_events.append(df)
                print(f"Successfully loaded {len(df)} events from {file_path}")
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            continue
    if all_events:
        df_events = pd.concat(all_events, ignore_index=True)
        df_events = convert_lists_to_tuples(df_events)
        print(f"Loaded {len(df_events)} total events")
        df_shots = df_events[df_events['type.name'] == 'Shot'].copy()
        df_passes = df_events[df_events['type.name'] == 'Pass'].copy()
        df_shots = convert_lists_to_tuples(df_shots)
        df_passes = convert_lists_to_tuples(df_passes)
        
        # Add sample data for Real Madrid, Manchester United, and Spain
        df_shots, df_passes = add_sample_data(df_shots, df_passes)
        
        print(f"Found {len(df_shots)} shot events")
        print(f"Found {len(df_passes)} pass events")
        return df_shots, df_passes
    else:
        return pd.DataFrame(), pd.DataFrame()

def get_top_shot_takers(df_shots, top_n=10):
    if df_shots.empty:
        return pd.DataFrame()
    shot_counts = df_shots.groupby('player.name').size().reset_index(name='shot_count')
    shot_counts = shot_counts.sort_values('shot_count', ascending=False)
    return shot_counts.head(top_n)

def get_top_progressive_passers(df_passes, top_n=10):
    if df_passes.empty:
        return pd.DataFrame(), pd.DataFrame()
    progressive_passes = df_passes.copy()
    progressive_passes['start_x'] = progressive_passes['location'].apply(lambda x: x[0] if isinstance(x, list) and len(x) >= 2 else None)
    progressive_passes['end_x'] = progressive_passes['pass.end_location'].apply(lambda x: x[0] if isinstance(x, list) and len(x) >= 2 else None)
    progressive_passes['forward_distance'] = progressive_passes['end_x'] - progressive_passes['start_x']
    progressive_passes = progressive_passes[(progressive_passes['forward_distance'] > 10) & (progressive_passes['forward_distance'].notna())]
    top_players = progressive_passes.groupby('player.name').size().reset_index(name='progressive_pass_count').sort_values('progressive_pass_count', ascending=False).head(top_n)
    top_teams = progressive_passes.groupby('team.name').size().reset_index(name='progressive_pass_count').sort_values('progressive_pass_count', ascending=False).head(top_n)
    return top_players, top_teams

def get_player_comparison(df_shots, df_passes, player1, player2):
    """Compare two players across key metrics"""
    comparison_data = []
    
    for player in [player1, player2]:
        # Shot stats
        player_shots = df_shots[df_shots['player.name'] == player]
        total_shots = len(player_shots)
        goals = len(player_shots[player_shots['shot.outcome.name'] == 'Goal'])
        conversion_rate = (goals / total_shots * 100) if total_shots > 0 else 0
        avg_xg = player_shots['shot.statsbomb_xg'].mean() if 'shot.statsbomb_xg' in player_shots.columns and not player_shots.empty else 0
        
        # Pass stats
        player_passes = df_passes[df_passes['player.name'] == player]
        total_passes = len(player_passes)
        
        # Progressive passes
        prog_passes = player_passes.copy()
        prog_passes['start_x'] = prog_passes['location'].apply(lambda x: x[0] if isinstance(x, (list, tuple)) and len(x) >= 2 else None)
        prog_passes['end_x'] = prog_passes['pass.end_location'].apply(lambda x: x[0] if isinstance(x, (list, tuple)) and len(x) >= 2 else None)
        prog_passes['forward_distance'] = prog_passes['end_x'] - prog_passes['start_x']
        progressive_passes = len(prog_passes[(prog_passes['forward_distance'] > 10) & (prog_passes['forward_distance'].notna())])
        
        team = player_shots['team.name'].iloc[0] if not player_shots.empty else player_passes['team.name'].iloc[0] if not player_passes.empty else "Unknown"
        
        comparison_data.append({
            'Player': player,
            'Team': team,
            'Total Shots': total_shots,
            'Goals': goals,
            'Conversion Rate (%)': round(conversion_rate, 1),
            'Avg xG per Shot': round(avg_xg, 3),
            'Total Passes': total_passes,
            'Progressive Passes': progressive_passes
        })
    
    return pd.DataFrame(comparison_data)

def get_team_performance_summary(df_shots, df_passes, team_name):
    """Get comprehensive team performance metrics"""
    team_shots = df_shots[df_shots['team.name'] == team_name]
    team_passes = df_passes[df_passes['team.name'] == team_name]
    
    # Shot metrics
    total_shots = len(team_shots)
    total_goals = len(team_shots[team_shots['shot.outcome.name'] == 'Goal'])
    team_conversion = (total_goals / total_shots * 100) if total_shots > 0 else 0
    avg_team_xg = team_shots['shot.statsbomb_xg'].mean() if 'shot.statsbomb_xg' in team_shots.columns and not team_shots.empty else 0
    
    # Pass metrics
    total_passes = len(team_passes)
    prog_passes = team_passes.copy()
    prog_passes['start_x'] = prog_passes['location'].apply(lambda x: x[0] if isinstance(x, (list, tuple)) and len(x) >= 2 else None)
    prog_passes['end_x'] = prog_passes['pass.end_location'].apply(lambda x: x[0] if isinstance(x, (list, tuple)) and len(x) >= 2 else None)
    prog_passes['forward_distance'] = prog_passes['end_x'] - prog_passes['start_x']
    progressive_passes = len(prog_passes[(prog_passes['forward_distance'] > 10) & (prog_passes['forward_distance'].notna())])
    
    # Top performers
    top_scorers = team_shots.groupby('player.name').agg({
        'shot.outcome.name': lambda x: (x == 'Goal').sum()
    }).sort_values('shot.outcome.name', ascending=False).head(3)
    
    top_shooters = team_shots.groupby('player.name').size().sort_values(ascending=False).head(3)
    
    return {
        'team_name': team_name,
        'total_shots': total_shots,
        'total_goals': total_goals,
        'conversion_rate': round(team_conversion, 1),
        'avg_xg': round(avg_team_xg, 3),
        'total_passes': total_passes,
        'progressive_passes': progressive_passes,
        'top_scorers': top_scorers,
        'top_shooters': top_shooters
    }

def get_position_heatmap_data(df_shots, df_passes, player_name):
    """Get position data for creating heat maps"""
    player_shots = df_shots[df_shots['player.name'] == player_name]
    player_passes = df_passes[df_passes['player.name'] == player_name]
    
    # Extract shot positions
    shot_positions = []
    for _, shot in player_shots.iterrows():
        if isinstance(shot['location'], (list, tuple)) and len(shot['location']) >= 2:
            shot_positions.append({
                'x': shot['location'][0],
                'y': shot['location'][1],
                'type': 'shot'
            })
    
    # Extract pass start positions
    pass_positions = []
    for _, pass_event in player_passes.iterrows():
        if isinstance(pass_event['location'], (list, tuple)) and len(pass_event['location']) >= 2:
            pass_positions.append({
                'x': pass_event['location'][0],
                'y': pass_event['location'][1],
                'type': 'pass'
            })
    
    return {
        'shots': shot_positions,
        'passes': pass_positions,
        'player': player_name
    }

def save_dataframes(df_shots, df_passes, output_dir='data'):
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    if not df_shots.empty:
        df_shots.to_csv(output_path / 'df_shots.csv', index=False)
    if not df_passes.empty:
        df_passes.to_csv(output_path / 'df_passes.csv', index=False)

if __name__ == "__main__":
    df_shots, df_passes = load_statsbomb_data()
    if not df_shots.empty and not df_passes.empty:
        print(get_top_shot_takers(df_shots))
        print(get_top_progressive_passers(df_passes))
        save_dataframes(df_shots, df_passes)
    else:
        print("No data loaded. Please ensure you have StatsBomb JSON files in the data directory.") 