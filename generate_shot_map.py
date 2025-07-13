#!/usr/bin/env python3
"""
Standalone script to generate shot map for Toni Kroos using StatsBomb data.
"""

import sys
import os
sys.path.append('scripts')
sys.path.append('visualizations')

from scripts.load_and_parse import load_statsbomb_data
from visualizations.shot_map_visualizer import create_shot_map
import pandas as pd

def main():
    print("Loading StatsBomb data...")
    df_shots, df_passes = load_statsbomb_data('data')
    
    if df_shots.empty:
        print("No shot data found. Please ensure you have StatsBomb JSON files in the data/ directory.")
        return
    
    print(f"Loaded {len(df_shots)} shots and {len(df_passes)} passes")
    
    # Check available players
    players = sorted(df_shots['player.name'].unique())
    print(f"\nAvailable players with shots: {len(players)}")
    
    # Look for Toni Kroos or similar names
    kroos_variations = ['Toni Kroos', 'T. Kroos', 'Kroos', 'Toni']
    kroos_found = None
    
    for variation in kroos_variations:
        matching_players = [p for p in players if variation.lower() in p.lower()]
        if matching_players:
            kroos_found = matching_players[0]
            print(f"Found player: {kroos_found}")
            break
    
    if not kroos_found:
        print("Toni Kroos not found in the data.")
        print("Available players (first 10):")
        for i, player in enumerate(players[:10]):
            print(f"  {i+1}. {player}")
        
        # Use the first available player as example
        if players:
            kroos_found = players[0]
            print(f"\nUsing {kroos_found} as example instead.")
        else:
            print("No players found in the data.")
            return
    
    # Generate shot map
    print(f"\nGenerating shot map for {kroos_found}...")
    save_path = "visualizations/shot_map_kroos.png"
    
    # Ensure visualizations directory exists
    os.makedirs("visualizations", exist_ok=True)
    
    fig = create_shot_map(df_shots, kroos_found, save_path=save_path)
    
    if fig:
        print(f"✅ Shot map saved to {save_path}")
        print(f"📊 Player stats:")
        player_shots = df_shots[df_shots['player.name'] == kroos_found]
        total_shots = len(player_shots)
        goals = len(player_shots[player_shots['shot.outcome.name'] == 'Goal'])
        conversion_rate = (goals / total_shots * 100) if total_shots > 0 else 0
        print(f"   Total shots: {total_shots}")
        print(f"   Goals: {goals}")
        print(f"   Conversion rate: {conversion_rate:.1f}%")
    else:
        print("❌ Failed to create shot map")

if __name__ == "__main__":
    main() 