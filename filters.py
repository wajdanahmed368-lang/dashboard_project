import os
import pandas as pd
import numpy as np

# Resolve file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MATCHES_PATH = os.path.join(DATA_DIR, 'matches.csv')
DELIVERIES_PATH = os.path.join(DATA_DIR, 'deliveries.csv')

# Cache for cleaned datasets
_matches_df = None
_deliveries_df = None

TEAM_STANDARDIZATION = {
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Rising Pune Supergiants": "Rising Pune Supergiant",
    "Royal Challengers Bengaluru": "Royal Challengers Bangalore"
}

SEASON_MAPPING = {
    "2007/08": "2008",
    "2009/10": "2010",
    "2020/21": "2020"
}

def load_and_clean_data():
    global _matches_df, _deliveries_df
    
    if _matches_df is not None and _deliveries_df is not None:
        return _matches_df, _deliveries_df

    # 1. Load matches dataset
    if not os.path.exists(MATCHES_PATH):
        raise FileNotFoundError(f"Matches CSV file not found at {MATCHES_PATH}")
    
    matches = pd.read_csv(MATCHES_PATH)
    
    # 2. Clean Matches
    # Standardize Season years to 4-digit strings for plotting and ordering
    matches['season'] = matches['season'].replace(SEASON_MAPPING)
    
    # Parse Date
    matches['date'] = pd.to_datetime(matches['date'], errors='coerce')
    
    # Handle missing cities by venue mapping
    venue_city_map = {
        "M.Chinnaswamy Stadium": "Bangalore",
        "M Chinnaswamy Stadium": "Bangalore",
        "Punjab Cricket Association Stadium, Mohali": "Chandigarh",
        "Punjab Cricket Association IS Bindra Stadium": "Chandigarh",
        "Punjab Cricket Association IS Bindra Stadium, Mohali": "Chandigarh",
        "Feroz Shah Kotla": "Delhi",
        "Arun Jaitley Stadium": "Delhi",
        "Arun Jaitley Stadium, Delhi": "Delhi",
        "Eden Gardens": "Kolkata",
        "Eden Gardens, Kolkata": "Kolkata",
        "Wankhede Stadium": "Mumbai",
        "Wankhede Stadium, Mumbai": "Mumbai",
        "Rajiv Gandhi International Stadium, Uppal": "Hyderabad",
        "MA Chidambaram Stadium, Chepauk": "Chennai",
        "MA Chidambaram Stadium": "Chennai",
        "MA Chidambaram Stadium, Chepauk, Chennai": "Chennai",
        "Dubai International Cricket Stadium": "Dubai",
        "Sharjah Cricket Stadium": "Sharjah",
        "Sheikh Zayed Stadium": "Abu Dhabi"
    }
    
    def fill_city(row):
        if pd.isna(row['city']):
            return venue_city_map.get(row['venue'], 'Other')
        return row['city']
        
    matches['city'] = matches.apply(fill_city, axis=1)
    
    # Standardize team names in matches
    for col in ['team1', 'team2', 'toss_winner', 'winner']:
        matches[col] = matches[col].replace(TEAM_STANDARDIZATION)
        
    # Handle winner missing values (matches with no result/tie)
    matches['winner'] = matches['winner'].fillna('No Result')
    matches['result_margin'] = matches['result_margin'].fillna(0)
    matches['result'] = matches['result'].fillna('no result')
    
    # Sort matches by date
    matches = matches.sort_values('date').reset_index(drop=True)
    
    # 3. Load deliveries dataset selectively (saving memory and load time)
    if not os.path.exists(DELIVERIES_PATH):
        raise FileNotFoundError(f"Deliveries CSV file not found at {DELIVERIES_PATH}")
        
    cols_to_use = [
        'match_id', 'inning', 'batting_team', 'bowling_team', 
        'total_runs', 'is_wicket', 'batter', 'batsman_runs', 
        'bowler', 'dismissal_kind'
    ]
    deliveries = pd.read_csv(DELIVERIES_PATH, usecols=cols_to_use)
    
    # Standardize team names in deliveries
    deliveries['batting_team'] = deliveries['batting_team'].replace(TEAM_STANDARDIZATION)
    deliveries['bowling_team'] = deliveries['bowling_team'].replace(TEAM_STANDARDIZATION)
    
    # Cache cleaned DataFrames
    _matches_df = matches
    _deliveries_df = deliveries
    
    return _matches_df, _deliveries_df

def get_filter_options():
    matches, _ = load_and_clean_data()
    
    # Get sorted list of seasons
    seasons = sorted(matches['season'].dropna().unique().tolist())
    
    # Get sorted list of teams (excluding "No Result")
    teams = sorted(list(set(matches['team1'].dropna().unique().tolist() + matches['team2'].dropna().unique().tolist())))
    
    # Get sorted list of cities
    cities = sorted(matches['city'].dropna().unique().tolist())
    
    # Get sorted list of players
    players = sorted(matches['player_of_match'].dropna().unique().tolist())
    
    # Get min/max margins and target runs
    margin_max = int(matches['result_margin'].max())
    target_max = int(matches['target_runs'].max())
    
    # Date limits
    min_date = matches['date'].min().strftime('%Y-%m-%d') if not matches['date'].isnull().all() else '2008-01-01'
    max_date = matches['date'].max().strftime('%Y-%m-%d') if not matches['date'].isnull().all() else '2026-06-01'
    
    return {
        "seasons": seasons,
        "teams": teams,
        "cities": cities,
        "players": players,
        "margin_max": margin_max,
        "target_max": target_max,
        "min_date": min_date,
        "max_date": max_date
    }

def filter_data(filters):
    matches, deliveries = load_and_clean_data()
    
    filtered_matches = matches.copy()
    
    # Apply Season Filter
    if 'seasons' in filters and filters['seasons'] and 'all' not in filters['seasons']:
        filtered_matches = filtered_matches[filtered_matches['season'].isin(filters['seasons'])]
        
    # Apply City Filter
    if 'cities' in filters and filters['cities'] and 'all' not in filters['cities']:
        filtered_matches = filtered_matches[filtered_matches['city'].isin(filters['cities'])]
        
    # Apply Teams Filter (matches involving any of the selected teams)
    if 'teams' in filters and filters['teams'] and 'all' not in filters['teams']:
        selected_teams = filters['teams']
        filtered_matches = filtered_matches[
            filtered_matches['team1'].isin(selected_teams) | 
            filtered_matches['team2'].isin(selected_teams)
        ]
        
    # Apply Player of Match Filter
    if 'player' in filters and filters['player'] and filters['player'] != 'all':
        filtered_matches = filtered_matches[filtered_matches['player_of_match'] == filters['player']]
        
    # Apply Margin Filter (numerical slider)
    if 'min_margin' in filters and filters['min_margin'] is not None:
        filtered_matches = filtered_matches[filtered_matches['result_margin'] >= float(filters['min_margin'])]
        
    # Apply Date Range Filter
    if 'start_date' in filters and filters['start_date']:
        start_dt = pd.to_datetime(filters['start_date'])
        filtered_matches = filtered_matches[filtered_matches['date'] >= start_dt]
    if 'end_date' in filters and filters['end_date']:
        end_dt = pd.to_datetime(filters['end_date'])
        filtered_matches = filtered_matches[filtered_matches['date'] <= end_dt]
        
    # Apply Search Filter (Search Venue or POTM)
    if 'search' in filters and filters['search']:
        query = str(filters['search']).lower().strip()
        filtered_matches = filtered_matches[
            filtered_matches['venue'].str.lower().fillna('').str.contains(query) |
            filtered_matches['player_of_match'].str.lower().fillna('').str.contains(query) |
            filtered_matches['winner'].str.lower().fillna('').str.contains(query)
        ]
        
    # Filter deliveries to match the remaining matches
    filtered_deliveries = deliveries[deliveries['match_id'].isin(filtered_matches['id'])]
    
    return filtered_matches, filtered_deliveries

def calculate_kpis(filtered_matches, filtered_deliveries):
    total_matches = len(filtered_matches)
    
    if total_matches == 0:
        return {
            "total_matches": 0,
            "total_runs": 0,
            "avg_target": 0.0,
            "highest_margin": 0,
            "toss_impact": 0.0,
            "top_player": "N/A"
        }
        
    total_runs = int(filtered_deliveries['total_runs'].sum()) if len(filtered_deliveries) > 0 else 0
    avg_target = float(round(filtered_matches['target_runs'].mean(), 1)) if 'target_runs' in filtered_matches.columns else 0.0
    highest_margin = int(filtered_matches['result_margin'].max())
    
    # Calculate toss impact: % of matches won by the toss winner
    toss_winners = filtered_matches[filtered_matches['toss_winner'] == filtered_matches['winner']]
    toss_impact = float(round((len(toss_winners) / total_matches) * 100, 1))
    
    # Top Player of Match
    top_player_str = "N/A"
    if 'player_of_match' in filtered_matches.columns:
        potm_counts = filtered_matches['player_of_match'].dropna().value_counts()
        if len(potm_counts) > 0:
            top_player = potm_counts.index[0]
            top_player_count = int(potm_counts.iloc[0])
            top_player_str = f"{top_player} ({top_player_count}x)"
            
    return {
        "total_matches": total_matches,
        "total_runs": total_runs,
        "avg_target": avg_target,
        "highest_margin": highest_margin,
        "toss_impact": toss_impact,
        "top_player": top_player_str
    }
