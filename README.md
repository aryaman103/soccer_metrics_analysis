# MatchMetrics Explorer

A tactical football analytics toolkit using [StatsBomb Open Data](https://github.com/statsbomb/open-data) with sample data from Real Madrid, Manchester United, and Spain.

## Features

- **Top Shot-Takers**: Identify prolific shooters with team filtering and xG(expected goals) analysis
- **Progressive Passers**: Find players and teams who drive play forward into the final third
- **Shot Maps**: Visualize shooting patterns for any player with interactive maps
- **Modern UI**: Dark theme with sidebar navigation and quick filters
- Also included: Conversion rates, shot count, end_location - start_location to filter distance of progessive passes, team and player rankings for all categories, top teams given quick filters on the top. 
- Can be used for tactical analysis, player comparisons, and scouting. 

- New functionality included player comparison and a single page dedicated to team metrics.
```
## 📁 Project Structure

```
matchmetrics-explorer/
├── dashboard.py              # Main Streamlit dashboard
├── scripts/
│   └── load_and_parse.py    # Data loading and processing
├── visualizations/
│   └── shot_map_visualizer.py # Shot map generation
├── data/                    # StatsBomb JSON files (optional)
├── generate_player_shot_map.py # Standalone shot map generator
└── requirements.txt         # Python dependencies

## Sample Data

Includes players from:
- **Real Madrid**: Benzema, Vinicius Jr., Modrić, Kroos, Valverde
- **Manchester United**: Rashford, Bruno Fernandes, Sancho, Martial
- **Spain**: Morata, Pedri, Gavi, Busquets, Ferran Torres

## Generate Shot Map

```bash
# List available players
python generate_player_shot_map.py --list-players

# Generate for specific player
python generate_player_shot_map.py --player "Karim Benzema"
```

## Data Source

[StatsBomb Open Data](https://github.com/statsbomb/open-data) - World Cup 2018, Women's World Cup 2019, Champions League matches. 