import subprocess
from nhlly_api_client import get_data
from nhlly_db import get_colors, colorize, RESET

def view_boxscore(game_number):
    """
    Fetches boxscore stats for a game, used for fetching more stats about a specific game
    """
    data = get_data(f"gamecenter/{game_number}/boxscore")
    home_team = data.get('homeTeam', {})
    away_team = data.get('awayTeam', {})
    return {
        'game_state': data.get('gameState'), #what happening
        'game_id': data.get('id'), #game id
        'season': data.get('season'), #season 2025 2026
        'game_date': data.get('gameDate'), #date of game
        'home_team_location': home_team.get('placeName', '').get('default', ''), #Winnipeg
        'away_team_location': away_team.get('placeName', '').get('default', ''), #Toronto
        'home_team_name': home_team.get('commonName', '').get('default', ''), #Jets
        'away_team_name': away_team.get('commonName', '').get('default', ''), #Maple Leafs
        'home_team_abbrev': home_team.get('abbrev', ''), #WPG
        'away_team_abbrev': away_team.get('abbrev', ''), #TOR
        'home_score': home_team.get('score', 0), #home score
        'away_score': away_team.get('score', 0), #away score
        'home_sog': home_team.get('sog', 0), #home shots on goal
        'away_sog': away_team.get('sog', 0), #away shots on goal
        'venue': data.get('venue', {}).get('default', ''),
        'venue_location': data.get('venueLocation', {}).get('default', '')
    }

def view_pbp(game_number):
    """
    Fetches play-by-play stats for a game, used for the most advanced set of plays
    """
    data = get_data(f"gamecenter/{game_number}/play-by-play")
    return {}

def game_view_tui(game_number):
    data = view_boxscore(game_number)
    while True:
        subprocess.run(["clear"])
        home_primary, home_secondary, home_accent, home_dark, home_light = get_colors(data.get('home_team_abbrev'), 5)
        away_primary, away_secondary, away_accent, away_dark, away_light = get_colors(data.get('away_team_abbrev'), 5)
        print(f"{colorize(away_primary)}{data.get('away_team_location'):^14}{RESET} {"@":^4} {colorize(home_primary)}{data.get('home_team_location'):^14}{RESET}")
        print(f"{colorize(away_secondary)}{data.get('away_team_name'):^14}{RESET} {" ":^4} {colorize(home_secondary)}{data.get('home_team_name'):^14}{RESET}")
        print(f"{colorize(away_accent)}{data.get('away_score'):^14}{RESET} {" ":^4} {colorize(home_accent)}{data.get('home_score'):^14}{RESET}")
        print(f"Venue: {data.get('venue')}, {data.get('venue_location')}")
        choice = input("(p)lay by play (s)tats (q)uit: ").lower()
        match choice:
            case 'q':
                break
            case 's':
                #pull some stats b'y
                print("")
            case 'p':
                data = view_pbp(game_number)
            case _:
                print("Invalid input")