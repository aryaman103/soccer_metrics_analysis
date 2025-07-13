# MatchMetrics Explorer

A tactical football analytics toolkit using [StatsBomb Open Data](https://github.com/statsbomb/open-data).

## Features

- Identify top 10 shot takers across all matches
- Find players and teams with the most progressive passes
- Visualize shot maps for any player (with `mplsoccer`)
- Interactive Streamlit dashboard for live exploration

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Download StatsBomb event JSON files into `data/` (see [StatsBomb Open Data](https://github.com/statsbomb/open-data)).
2. Run the dashboard:

```bash
streamlit run dashboard.py
```

## Example

![Shot Map Example](visualizations/shot_map_kroos.png)

## Data Source

- [StatsBomb Open Data](https://github.com/statsbomb/open-data) 