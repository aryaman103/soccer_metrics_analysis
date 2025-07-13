#!/usr/bin/env python3
"""
Comprehensive script to generate shot maps for any player using StatsBomb data.
"""

import sys
import os
import argparse
sys.path.append('scripts')
sys.path.append('visualizations')

from scripts.load_and_parse import load_statsbomb_data
from visualizations.shot_map_visualizer import create_shot_map
import pandas as pd

def list_available_players(df_shots):
    """List all available players with their shot counts."""
    if df_shots.empty:
        print("No shot data available.")
        return
    
    player_stats = df_shots.groupby('player.name').agg({
        'id': 'count',
        'shot.outcome.name': lambda x: (x == 'Goal').sum()
    }).rename(columns={'id': 'total_shots', 'shot.outcome.name': 'goals'})
    
    player_stats['conversion_rate'] = (player_stats['goals'] / player_stats['total_shots'] * 100).round(1)
    player_stats = player_stats.sort_values('total_shots', ascending=False)
    
    print(f"\n📊 Available Players ({len(player_stats)} total):")
    print("=" * 80)
    print(f"{'Rank':<4} {'Player Name':<30} {'Shots':<6} {'Goals':<6} {'Conv%':<6}")
    print("-" * 80)
    
    for i, (player, stats) in enumerate(player_stats.head(20).iterrows(), 1):
        print(f"{i:<4} {player:<30} {stats['total_shots']:<6} {stats['goals']:<6} {stats['conversion_rate']:<6.1f}")
    
    if len(player_stats) > 20:
        print(f"... and {len(player_stats) - 20} more players")

def generate_shot_map_for_player(df_shots, player_name, save_path=None):
    """Generate shot map for a specific player."""
    print(f"\n🎯 Generating shot map for: {player_name}")
    
    # Check if player exists
    if player_name not in df_shots['player.name'].values:
        print(f"❌ Player '{player_name}' not found in the data.")
        print("Use --list-players to see available players.")
        return False
    
    # Get player stats
    player_shots = df_shots[df_shots['player.name'] == player_name]
    total_shots = len(player_shots)
    goals = len(player_shots[player_shots['shot.outcome.name'] == 'Goal'])
    conversion_rate = (goals / total_shots * 100) if total_shots > 0 else 0
    
    print(f"📊 Player Statistics:")
    print(f"   Total shots: {total_shots}")
    print(f"   Goals: {goals}")
    print(f"   Conversion rate: {conversion_rate:.1f}%")
    print(f"   Team: {player_shots['team.name'].iloc[0] if not player_shots.empty else 'N/A'}")
    
    if total_shots == 0:
        print("❌ No shots found for this player.")
        return False
    
    # Generate shot map
    fig = create_shot_map(df_shots, player_name, save_path=save_path)
    
    if fig:
        print(f"✅ Shot map generated successfully!")
        if save_path:
            print(f"💾 Saved to: {save_path}")
        return True
    else:
        print("❌ Failed to generate shot map.")
        return False

def main():
    parser = argparse.ArgumentParser(description='Generate shot maps for football players using StatsBomb data')
    parser.add_argument('--player', '-p', type=str, help='Player name to generate shot map for')
    parser.add_argument('--list-players', '-l', action='store_true', help='List all available players')
    parser.add_argument('--output', '-o', type=str, default='visualizations/shot_map.png', 
                       help='Output file path for the shot map')
    parser.add_argument('--data-dir', '-d', type=str, default='data', help='Directory containing StatsBomb JSON files')
    
    args = parser.parse_args()
    
    print("Loading StatsBomb data...")
    df_shots, df_passes = load_statsbomb_data(args.data_dir)
    
    if df_shots.empty:
        print("❌ No shot data found. Please ensure you have StatsBomb JSON files in the data/ directory.")
        return
    
    print(f"✅ Loaded {len(df_shots)} shots and {len(df_passes)} passes")
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    if args.list_players:
        list_available_players(df_shots)
        return
    
    if args.player:
        success = generate_shot_map_for_player(df_shots, args.player, args.output)
        if success:
            print(f"\n🎉 Shot map for {args.player} has been generated!")
        else:
            print(f"\n❌ Failed to generate shot map for {args.player}")
    else:
        print("\nUsage examples:")
        print("  python generate_player_shot_map.py --list-players")
        print("  python generate_player_shot_map.py --player 'Antoine Griezmann'")
        print("  python generate_player_shot_map.py --player 'Eden Hazard' --output 'hazard_shot_map.png'")
        print("\nUse --help for more options.")

if __name__ == "__main__":
    main() 