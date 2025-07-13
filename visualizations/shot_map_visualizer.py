import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch

def create_shot_map(df_shots, player_name, save_path=None):
    player_shots = df_shots[df_shots['player.name'] == player_name].copy()
    if player_shots.empty:
        print(f"No shots found for player: {player_name}")
        return None
    player_shots['x'] = player_shots['location'].apply(lambda x: x[0] if isinstance(x, (list, tuple)) and len(x) >= 2 else None)
    player_shots['y'] = player_shots['location'].apply(lambda x: x[1] if isinstance(x, (list, tuple)) and len(x) >= 2 else None)
    player_shots = player_shots.dropna(subset=['x', 'y'])
    if player_shots.empty:
        print(f"No valid shot locations found for player: {player_name}")
        return None
    pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='white')
    fig, ax = pitch.draw(figsize=(12, 8))
    x_coords = player_shots['x'].values
    y_coords = player_shots['y'].values
    colors = ['red' if outcome == 'Goal' else 'blue' for outcome in player_shots['shot.outcome.name']]
    pitch.scatter(x_coords, y_coords, c=colors, s=100, alpha=0.7, ax=ax)
    total_shots = len(player_shots)
    goals = len(player_shots[player_shots['shot.outcome.name'] == 'Goal'])
    conversion_rate = (goals / total_shots * 100) if total_shots > 0 else 0
    title = f"Shot Map: {player_name}\nTotal Shots: {total_shots} | Goals: {goals} | Conversion Rate: {conversion_rate:.1f}%"
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='red', alpha=0.7, label='Goals'), Patch(facecolor='blue', alpha=0.7, label='Other Shots')]
    ax.legend(handles=legend_elements, loc='upper right')
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    return fig 