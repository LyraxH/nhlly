import subprocess
from nhlly_api_client import get_data
from nhlly_db import get_colors, colorize, RESET

def get_team_stats(team_stats):
    team = {'forwards': [], 'defense': [], 'goalies': []}
    for player in team_stats.get('skaters', {}):
        if player.get('positionCode', '') == 'D':
            team['defense'].append(get_skater_stats(player))
        else:
            team['forwards'].append(get_skater_stats(player))
    for player in team_stats.get('goalies', {}):
        team['goalies'].append(get_goalie_stats(player))
    return team

def get_skater_stats(player):
    return {
        'player_id': player.get('playerId', ''),
        'first_name': player.get('firstName', {}).get('default', ''),
        'last_name': player.get('lastName', {}).get('default', ''),
        'position': player.get('positionCode', ''),
        'gp': player.get('gamesPlayed', 0),
        'goals': player.get('goals', 0),
        'assists': player.get('assists', 0),
        'points': player.get('points', 0),
        '+/-': player.get('plusMinus', 0),
        'pim': player.get('pim', 0),
        'ppg': player.get('powerPlayGoals', 0),
        'shg': player.get('shortHandedGoals', 0),
        'gwg': player.get('gameWinningGoals', 0),
        'otg': player.get('overtimeGoals', 0),
        'sog': player.get('shotsOnGoal', 0),
        'toi': player.get('timeOnIce', 0),
        'fow': player.get('faceoffWinningPctg', 0),
    }

def get_goalie_stats(player):
    return {
        'player_id': player.get('playerId', ''),
        'first_name': player.get('firstName', {}).get('default', ''),
        'last_name': player.get('lastName', {}).get('default', ''),
        'gp': player.get('gamesPlayed', 0),
        'wins': player.get('wins', 0),
        'losses': player.get('losses', 0),
        'otl': player.get('otl', 0),
        'gaa': player.get('gaa', 0),
        'save_pctg': player.get('savePercentage', 0),
        'shutouts': player.get('shutouts', 0),
    }

def roster_tui():
    team_abbrev = input("What team: ").upper()
    team = get_team_stats(get_data(f"club-stats/{team_abbrev}/now"))
    skater_sort_by = "first_name"
    goalie_sort_by = "first_name"
    sorted_forwards = sorted(team['forwards'], key=lambda x: x[skater_sort_by], reverse=True)
    sorted_defense = sorted(team['defense'], key=lambda x: x[skater_sort_by], reverse=True)
    sorted_goalies = sorted(team['goalies'], key=lambda x: x[goalie_sort_by], reverse=True)
    while True:
        subprocess.run(["clear"])
        light, dark, accent = get_colors(team_abbrev, 3)
        print(f"{colorize(light)}------ {colorize(accent)} {team_abbrev} {colorize(light)} ------ {colorize(dark)}\nSort By: {skater_sort_by}{RESET}")      
        print(f"{colorize(dark)}{"-" * 79}{RESET}")
        print(f" {colorize(light)}{'Pos':<4}{'Name':<23}{'GP':<4}{'G':<4}{'A':<4}{'P':<4}{'+/-':<5}{'PIM':<5}{'TOI':<7}{'FOW%':<10}{RESET}")
        print(f"{colorize(dark)}{"-" * 79}{RESET}")
        for forward in sorted_forwards:
            print(f" {colorize(light)}{forward.get('position', ''):<4}{forward.get('first_name', ''):<10}{forward.get('last_name', ''):<13}{forward.get('gp', 0):<4}{forward.get('goals', 0):<4}{forward.get('assists', 0):<4}{forward.get('points', 0):<4}{forward.get('+/-', 0):<5}{forward.get('pim', 0):<5}{forward.get('toi', 0):<7}{forward.get('fow', 0):<10.2f}{RESET}")
        print(f"{colorize(dark)}{"-" * 79}{RESET}")
        for defense in sorted_defense:
            print(f" {colorize(light)}{defense.get('position', ''):<4}{defense.get('first_name', ''):<10}{defense.get('last_name', ''):<13}{defense.get('gp', 0):<4}{defense.get('goals', 0):<4}{defense.get('assists', 0):<4}{defense.get('points', 0):<4}{defense.get('+/-', 0):<5}{defense.get('pim', 0):<5}{defense.get('toi', 0):<7}{defense.get('fow', 0):<10.2f}{RESET}")
        print(f"{colorize(dark)}{"-" * 79}{RESET}")
        print(f" {colorize(light)}{'Pos':<4}{'Name':<23}{'GP':<4}{'W':<4}{'L':<4}{'OTL':<4}{'SO':<4}{'SV%':<7}{RESET}")
        print(f"{colorize(dark)}{"-" * 79}{RESET}")
        for goalie in sorted_goalies:
            print(f" {colorize(light)}{"G":<4}{goalie.get('first_name', ''):<10}{goalie.get('last_name', ''):<13}{goalie.get('gp', 0):<4}{goalie.get('wins', 0):<4}{goalie.get('losses', 0):<4}{goalie.get('otl', 0):<4}{goalie.get('shutouts', 0):<4}{goalie.get('save_pctg', 0):<7.3f}{RESET}")
        print(f"{colorize(dark)}{"-" * 79}{RESET}")
        choice = input(f"{RESET}Sort By: (f)irst name, (g)ames, (p)oints, (+/-), (pim), (toi), (fow), (q)uit: ").lower()
        match choice:
            case 'f':
                skater_sort_by = "first_name"
                goalie_sort_by = "first_name"
            case 'g':
                skater_sort_by = "gp"
                goalie_sort_by = "gp"
            case 'p':
                skater_sort_by = "points"
                goalie_sort_by = "shutouts"
            case '+':
                skater_sort_by = "+/-"
                goalie_sort_by = "save_pctg"
            case 'pim':
                skater_sort_by = "pim"
            case 'toi':
                skater_sort_by = "toi"
                goalie_sort_by = "gaa"
            case 'fow':
                skater_sort_by = "fow"
                goalie_sort_by = "save_pctg"
            case 'q':
                break
            case _:
                print("Invalid input")