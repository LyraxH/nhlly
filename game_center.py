import subprocess
from api_client import get_data
from db import get_colors, colorize, RESET

def view_gamecenter(game_number):
    data = get_data(f"gamecenter/{game_number}/landing")
    home_team = data.get('homeTeam', {})
    away_team = data.get('awayTeam', {})
    return {
        'game_id': data.get('id'),
        'season': data.get('season'),
        'gameDate': data.get('gameDate'),
        'awayTeam': away_team.get('abbrev', ''),
        'homeTeam': home_team.get('abbrev', ''),
        'awayScore': away_team.get('score', 0),
        'homeScore': home_team.get('score', 0),
        'venue': data.get('venue', {}).get('default', ''),
        'venue_location': data.get('venueLocation', {}).get('default', '')
    }

def view_boxscore(game_number):
    game_data = get_data(f"gamecenter/{game_number}/boxscore")
    return {}

def view_pbp(game_number):
    game_data = get_data(f"gamecenter/{game_number}/play-by-play")
    return {}

def game_view_tui(game_number):
    data = view_gamecenter(game_number)
    while True:
        subprocess.run(["clear"])
        print(f"{data.get('awayTeam'):<7} {"@":<4} {data.get('homeTeam'):<5}")
        print(f"{"Away:":<5} {data.get('awayScore'):<5} {"Home:":<5} {data.get('homeScore'):<5}")
        print(f"Venue: {data.get('venue')}, {data.get('venue_location')}")
        choice = input("(p)lay by play (b)oxscore (q)uit ").lower()
        match choice:
            case 'q':
                break
            case 'p':
                data = view_pbp(game_number)
            case 'b':
                data = view_boxscore(game_number)
            case _:
                print("Invalid input")