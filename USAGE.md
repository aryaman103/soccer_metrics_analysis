# MatchMetrics Explorer - Usage Guide

## Quick Start

### 1. Generate Shot Maps

**List all available players:**
```bash
python generate_player_shot_map.py --list-players
```

**Generate shot map for a specific player:**
```bash
python generate_player_shot_map.py --player "Paul Pogba"
```

**Generate shot map with custom output path:**
```bash
python generate_player_shot_map.py --player "Francesca Kirby" --output "kirby_shot_map.png"
```

### 2. Run the Dashboard

**Launch the interactive Streamlit dashboard:**
```bash
streamlit run dashboard.py
```

### 3. Generate Example Shot Map (Kroos)

**Generate the default Kroos shot map:**
```bash
python generate_shot_map.py
```

## Available Players in Current Data

Based on the downloaded StatsBomb data, here are some notable players:

- **Francesca Kirby** (7 shots, 0 goals) - Chelsea FCW
- **Ramona Bachmann** (6 shots, 0 goals) - Chelsea FCW  
- **Ante Rebić** (3 shots, 0 goals) - Croatia
- **Paul Pogba** (2 shots, 1 goal, 50% conversion) - France
- **Kylian Mbappé** (2 shots, 1 goal, 50% conversion) - France
- **Antoine Griezmann** (2 shots, 1 goal, 50% conversion) - France

## Data Source

The shot maps are generated using [StatsBomb Open Data](https://github.com/statsbomb/open-data), which includes:

- World Cup 2018 matches
- Women's World Cup 2019 matches
- Champions League matches

## Generated Files

- `visualizations/shot_map_kroos.png` - Default example shot map
- `visualizations/kirby_shot_map.png` - Francesca Kirby shot map
- `visualizations/pogba_shot_map.png` - Paul Pogba shot map

## Features

- **Shot Maps**: Visualize shot locations on a football pitch
- **Player Statistics**: Total shots, goals, and conversion rates
- **Interactive Dashboard**: Explore data with Streamlit
- **Progressive Pass Analysis**: Identify forward-moving passes
- **Top Performers**: Find players with most shots and progressive passes 