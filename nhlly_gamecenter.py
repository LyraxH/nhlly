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
    player_stats = data.get('playerByGameStats', '')
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
        'period': data.get('periodDescriptor', {}).get('number', 0), #period
        'time_remaining': data.get('clock', {}).get('timeRemaining', '69:420'), #time remaining
        'pp_home': data.get('situation', {}).get('homeTeam', {}).get('strength', 0), #power play
        'pp_away': data.get('situation', {}).get('awayTeam', {}).get('strength', 0), #power play
        'home_pp_status': data.get('situation', {}).get('homeTeam', {}).get('situationDescriptions', 'N/A'),
        'away_pp_status': data.get('situation', {}).get('awayTeam', {}).get('situationDescriptions', 'N/A'),
        'venue': data.get('venue', {}).get('default', ''), #stadium name
        'venue_location': data.get('venueLocation', {}).get('default', ''), #stadium location

        'home': get_team_stats(player_stats.get('homeTeam', '')),
        'away': get_team_stats(player_stats.get('awayTeam', '')),
    }

def get_team_stats(team_stats):
    team = {'forwards': [], 'defense': [], 'goalies': []}
    for player in team_stats.get('forwards', []):
        team['forwards'].append(get_player_stats(player))
    for player in team_stats.get('defense', []):
        team['defense'].append(get_player_stats(player))
    for player in team_stats.get('goalies', []):
        team['goalies'].append(get_player_stats(player))
    return team

def get_player_stats(player):
    stats = {
        'player_id': player.get('playerId', ''),
        'number': player.get('sweaterNumber', 0),
        'name': player.get('name', {}).get('default', 'S. John'), #john smith lmao
        'position': player.get('position', ''),
    }
    if (player.get('positon', '') == 'G'):
        stats.update({
            'essa': player.get('evenStrengthShotsAgainst', 0),
            'ppsa': player.get('powerPlayShotsAgainst', 0),
            'shsa': player.get('shortHandedShotsAgainst', 0),
            'ssa': player.get('saveShotsAgainst', 0),
            'save_pctg': player.get('savePctg', 0),
            'esga': player.get('evenStrengthGoalsAgainst', 0),
            'ppga': player.get('powerPlayGoalsAgainst', 0),
            'shga': player.get('shortHandedGoalsAgainst', 0),
            'ga': player.get('goalsAgainst', 0),
            'saves': player.get('saves', 0)
        })
    else:
        stats.update({
            'goals': player.get('goals', 0),
            'assists': player.get('assists', 0),
            'points': player.get('points', 0),
            '+/-': player.get('plusMinus', 0),
            'pim': player.get('pim', 0),
            'hits': player.get('hits', 0),
            'ppg': player.get('powerPlayGoals', 0),
            'sog': player.get('sog', 0),
            'fow': player.get('faceoffWinPctg', 0),
            'toi': player.get('toi', 0),
            'blocks': player.get('blockedShots', 0),
            'shifts': player.get('shifts', 0),
            'giveaways': player.get('giveaways', 0),
            'takeaways': player.get('takeaways', 0),
        })
    return stats

    
def view_pbp(game_number):
    """
    Fetches play-by-play stats for a game, used for the most advanced set of plays
    """
    data = get_data(f"gamecenter/{game_number}/play-by-play")
    return {}

def stats_tui(home, away):
    toggle_team = home
    forward_sort_by = "name"
    defense_sort_by = "name"
    goalie_sort_by = "name"
    while True:
        subprocess.run(["clear"])
        print(f" --- team roster --- Sort By: {forward_sort_by}")

        sorted_forwards = sorted(toggle_team.get('forwards', []), key=lambda x: x[forward_sort_by], reverse=True)
        sorted_defense = sorted(toggle_team.get('defense', []), key=lambda x: x[defense_sort_by], reverse=True)
        sorted_goalies = sorted(toggle_team.get('goalies', []), key=lambda x: x[goalie_sort_by], reverse=True)

        print(f"{'Pos':<3} {'Name':<16} {'G':<4} {'A':<4} {'P':<4} {'+/-':<5} {'PIM':<5} {'TOI':<5} {'FOW%':<10}")
        print(f"{'-'}" * 79)
        for forward in sorted_forwards:
            print(f" {forward.get('position', ''):<3} {forward.get('name', ''):<16} {forward.get('goals', 0):<4} {forward.get('assists', 0):<4} {forward.get('points', 0):<4} {forward.get('+/-', 0):<5} {forward.get('pim', 0):<5} {forward.get('toi', 0):<5} {forward.get('fow', 0):<10}")
        print(f"{'-'}" * 79)
        for defense in sorted_defense:
            print(f" {defense.get('position', ''):<3} {defense.get('name', ''):<16} {defense.get('goals', 0):<4} {defense.get('assists', 0):<4} {defense.get('points', 0):<4} {defense.get('+/-', 0):<5} {defense.get('pim', 0):<5} {defense.get('toi', 0):<5} {defense.get('fow', 0):<10}")
        print(f"{'-'}" * 79)
        print(f"{'Pos':<3} {'Name':<16} {'SV%':<10} {'GAA':<10}")
        print(f"{'-'}" * 79)
        for goalie in sorted_goalies:
            print(f" {goalie.get('position', ''):<3} {goalie.get('name', ''):<16} {goalie.get('save_pctg', 0):<10} {goalie.get('gaa', 0):<10}")
        print(f"{'-'}" * 79)
        choice = input(f"Sort By: (n)ame, (g)ames, (p)oints, (+/-), (pim), (toi), (fow), (x)toggle team (q)uit: ").lower()
        match choice:
            case 'n':
                forward_sort_by = 'name'
                goalie_sort_by = 'name'
            case '+':
                forward_sort_by = '+/-'
                defense_sort_by = '+/-'
                goalie_sort_by = 'save_pctg'
            case 'pim':
                forward_sort_by = 'pim'
            case 'toi':
                forward_sort_by = 'toi'
                goalie_sort_by = 'toi'
            case 'fow':
                forward_sort_by = 'fow'
                defense_sort_by = 'fow'
                goalie_sort_by = 'gaa'
            case 'x':
                if toggle_team == home:
                    toggle_team = away
                else:
                    toggle_team = home
            case 'q':
                break
            case _:
                print("Invalid input")

def game_view_tui(game_number):
    data = view_boxscore(game_number)
    while True:
        subprocess.run(["clear"])
        home_primary, home_secondary, home_accent, home_dark, home_light = get_colors(data.get('home_team_abbrev'), 5)
        away_primary, away_secondary, away_accent, away_dark, away_light = get_colors(data.get('away_team_abbrev'), 5)
        print(f"{data.get('game_date')} | {data.get('game_state')} | ID: {data.get('game_id')}")
        print(f"{colorize(away_primary)}{data.get('away_team_location'):^14}{RESET} {"@":^4} {colorize(home_primary)}{data.get('home_team_location'):^14}{RESET}")
        print(f"{colorize(away_secondary)}{data.get('away_team_name'):^14}{RESET} {" ":^4} {colorize(home_secondary)}{data.get('home_team_name'):^14}{RESET}")
        print(f"{colorize(away_accent)}{data.get('away_score'):^14}{RESET} {" ":^4} {colorize(home_accent)}{data.get('home_score'):^14}{RESET}")
        print(f"SOG: {data.get('home_sog'):^4} {" ":^9} {data.get('away_sog'):^14}")
        print(f"Period: {data.get('period')} | {data.get('time_remaining')} | {data.get('home_pp_status')} | {data.get('away_pp_status')}")
        print(f"Venue: {data.get('venue')}, {data.get('venue_location')}")
        choice = input("(p)lay by play (s)tats (q)uit: ").lower()
        match choice:
            case 'q':
                break
            case 's':
                #pull some stats b'y
                stats_tui(data.get('home', {}), data.get('away', {}))
            case 'p':
                data = view_pbp(game_number)
            case _:
                print("Invalid input")