import subprocess
from nhlly_utils import get_data, draw_table
from nhlly_db import get_colors, colorize, RESET
    
def view_pbp(game_number):
    """
    Fetches play-by-play stats for a game, used for the most advanced set of plays
    """
    data = get_data(f"gamecenter/{game_number}/play-by-play")
    return {}

def game_ataglance_tui(game_number):
    data = get_data(f"gamecenter/{game_number}/landing")
    home_team = data.get('homeTeam', {})
    away_team = data.get('awayTeam', {})
    game_data = {
        'game_id': data.get('id'), #game id
        'season': data.get('season'), #season 2025 2026
        'game_date': data.get('gameDate'), #date of game
        'venue': data.get('venue', {}).get('default', ''), #stadium name
        'venue_location': data.get('venueLocation', {}).get('default', ''), #stadium location
        'game_state': data.get('gameState'), #what happening
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
        'period': data.get('periodDescriptor', {}).get('number', 0), #period
        'period_type': data.get('periodDescriptor', {}).get('periodType', 'N/A'),
        'time_remaining': data.get('clock', {}).get('timeRemaining', '69:420'), #time remaining
        'pp_home': data.get('situation', {}).get('homeTeam', {}).get('strength', 0), #power play
        'pp_away': data.get('situation', {}).get('awayTeam', {}).get('strength', 0), #power play
        'home_pp_status': data.get('situation', {}).get('homeTeam', {}).get('situationDescriptions', 'N/A'),
        'away_pp_status': data.get('situation', {}).get('awayTeam', {}).get('situationDescriptions', 'N/A'),
    }
    while True:
        subprocess.run(["clear"])
        home_light, home_dark, home_accent = get_colors(game_data.get('home_team_abbrev'), 3)
        away_light, away_dark, away_accent = get_colors(game_data.get('away_team_abbrev'), 3)
        print(f"{game_data.get('game_date')} | {game_data.get('game_state')} | ID: {game_data.get('game_id')}")
        print(f"{colorize(away_light)}{game_data.get('away_team_location'):^14}{RESET} {"@":^4} {colorize(home_light)}{game_data.get('home_team_location'):^14}{RESET}")
        print(f"{colorize(away_dark)}{game_data.get('away_team_name'):^14}{RESET} {" ":^4} {colorize(home_dark)}{game_data.get('home_team_name'):^14}{RESET}")
        print(f"{colorize(away_accent)}{game_data.get('away_score'):^14}{RESET} {" ":^4} {colorize(home_accent)}{game_data.get('home_score'):^14}{RESET}")
        print(f"SOG: {game_data.get('away_sog'):^4} {" ":^9} {game_data.get('home_sog'):^14}")
        print(f"Period: {game_data.get('period')} | {game_data.get('time_remaining')} | {game_data.get('away_pp_status')} | {game_data.get('home_pp_status')}")
        print(f"Venue: {game_data.get('venue')}, {game_data.get('venue_location')}")
        choice = input("(p)lay by play (s)tats (q)uit: ").lower()
        match choice:
            case 'q':
                break
            case 's': #pull some stats b'y
                stats_tui(game_data.get('home_team_abbrev'), game_data.get('away_team_abbrev'), game_data.get('game_id'))
            case 'p':
                data = view_pbp(game_data.get('game_id'))
            case _:
                print("Invalid input")

def stats_tui(h_tag, a_tag, code=None):
    toggle_tag = h_tag
    skater_sort_by = "name"
    goalie_sort_by = "name"
    print(code)
    while True:
        if toggle_tag == h_tag:
            draw_table(code, skater_sort_by, goalie_sort_by, 'homeTeam')
        else:
            draw_table(code, skater_sort_by, goalie_sort_by, 'awayTeam')
        choice = input(f"Sort By: (n)ame, (g)oals, (a)ssists, (p)oints, (+/-), (pim), (toi), (fow), (s)hots, (x)toggle team (q)uit: ").lower()
        match choice:
            case 'n':
                forward_sort_by = 'name'
                defense_sort_by = 'name'
            case 'g':
                forward_sort_by = 'goals'
                defense_sort_by = 'goals'
            case 'a':
                forward_sort_by = 'assists'
                defense_sort_by = 'assists'
            case 'p':
                forward_sort_by = 'points'
                defense_sort_by = 'points'
            case '+':
                forward_sort_by = '+/-'
                defense_sort_by = '+/-'
            case 'pim':
                forward_sort_by = 'pim'
                defense_sort_by = 'pim'
            case 'toi':
                forward_sort_by = 'toi'
                defense_sort_by = 'toi'
            case 'fow':
                forward_sort_by = 'fow'
                defense_sort_by = 'fow'
            case 's':
                forward_sort_by = 'sog'
                defense_sort_by = 'sog'
            case 'x':
                if toggle_team == home:
                    toggle_team = away
                    toggle_tag = a_tag
                else:
                    toggle_team = home
                    toggle_tag = h_tag
            case 'q':
                break
            case _:
                print("Invalid input")