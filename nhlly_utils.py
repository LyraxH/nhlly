import requests
import subprocess
from nhlly_db import get_colors, colorize, RESET

def get_data(endpoint) -> dict:
    """
    Basic data fetching command
    Used in conjunction with endpoint to fetch data from Official NHL API
    """
    url = "https://api-web.nhle.com/v1/"
    r = requests.get(f"{url}{endpoint}")
    if r.status_code == 200:
        return r.json()
    else:
        return {"error": "Could not retrieve data"}


def draw_table(team_abbrev, skater_sort_by, goalie_sort_by, h_a_tag=None):
    #subprocess.run(["clear"])
    team_stats = get_team_stats(team_abbrev, h_a_tag)
    light, dark, accent = get_colors(team_abbrev, 3)
    sorted_forwards = sorted(team_stats.get('forwards', []), key=lambda x: x[skater_sort_by], reverse=True)
    sorted_defense = sorted(team_stats.get('defense', []), key=lambda x: x[skater_sort_by], reverse=True)
    sorted_goalies = sorted(team_stats.get('goalies', []), key=lambda x: x[goalie_sort_by], reverse=True)
    print(f"{colorize(light)}------ {colorize(accent)} {team_abbrev} {colorize(light)} ------ {colorize(dark)}\nSort By: {skater_sort_by}{RESET}")
    print(f"{colorize(dark)}{"-" * 79}{RESET}")
    print(f" {colorize(light)}{'Pos':<4}{'Name':<22}{'G':<4}{'A':<4}{'P':<4}{'+/-':<5}{'PIM':<5}{'TOI':<7}{'FOW%':<10}{RESET}")
    print(f"{colorize(dark)}{"-" * 79}{RESET}")
    for forward in sorted_forwards:
        print(f" {colorize(light)}{forward.get('position', ''):<4}{forward.get('name', ''):<22}{forward.get('goals', 0):<4}{forward.get('assists', 0):<4}{forward.get('points', 0):<4}{forward.get('+/-', 0):<5}{forward.get('pim', 0):<5}{forward.get('toi', 0):<7}{forward.get('fow', 0):<10.2f}{RESET}")
    print(f"{colorize(dark)}{"-" * 79}{RESET}")
    for defense in sorted_defense:
        print(f" {colorize(light)}{defense.get('position', ''):<4}{defense.get('name', ''):<22}{defense.get('goals', 0):<4}{defense.get('assists', 0):<4}{defense.get('points', 0):<4}{defense.get('+/-', 0):<5}{defense.get('pim', 0):<5}{defense.get('toi', 0):<7}{defense.get('fow', 0):<10.2f}{RESET}")
    print(f"{colorize(dark)}{"-" * 79}{RESET}")
    print(f" {colorize(light)}{'Pos':<4}{'Name':<22}{'SA':<4}{'GA':<4}{'SVS':<4}{'SV%':<7}{RESET}")
    print(f"{colorize(dark)}{"-" * 79}{RESET}")
    for goalie in sorted_goalies:
        print(f" {colorize(light)}{"G":<4}{goalie.get('name', ''):<22}{goalie.get('sa', 0):<4}{goalie.get('ga', 0):<4}{goalie.get('saves', 0):<4}{goalie.get('save_pctg', 0):<7.3f}{RESET}")
    print(f"{colorize(dark)}{"-" * 79}{RESET}")

def get_team_stats(code, h_a_tag=None):
    team = {'forwards': [], 'defense': [], 'goalies': []}
    if h_a_tag:
        data = get_data(f"game-center/{code}/boxscore").get('playerByGameStats', {})
        for player in data.get(h_a_tag, {}).get('forwards', []):
            team['forwards'].append(get_skater_stats(player, True))
        for player in data.get(h_a_tag, {}).get('defense', []):
            team['defense'].append(get_skater_stats(player, True))
        for player in data.get(h_a_tag, {}).get('goalies', []):
            team['goalies'].append(get_skater_stats(player, True))
    else:
        team_stats = get_data(f"club-stats/{code}/now")
        for player in team_stats.get('skaters', {}):
            if player.get('positionCode', '') == 'D':
                team['defense'].append(get_skater_stats(player, False))
            else:
                team['forwards'].append(get_skater_stats(player, False))
        for player in team_stats.get('goalies', {}):
            team['goalies'].append(get_skater_stats(player, False))
    return team

def get_skater_stats(player, isBoxscore=False):
    stats = {
        'player_id': player.get('playerId', ''),
        'name': player.get('firstName', {}).get('default', '') + ' ' + player.get('lastName', {}).get('default', ''),
        'position': player.get('positionCode', ''),
        'gp': player.get('gamesPlayed', 0),
        'goals': player.get('goals', 0),
        'assists': player.get('assists', 0),
        'points': player.get('points', 0),
        '+/-': player.get('plusMinus', 0),
        'pim': player.get('penaltyMinutes', 0),
        'ppg': player.get('powerPlayGoals', 0),
        'shg': player.get('shortHandedGoals', 0),
        'gwg': player.get('gameWinningGoals', 0),
        'otg': player.get('overtimeGoals', 0),
        'sog': player.get('shotsOnGoal', 0),
        'toi': player.get('avgTimeOnIcePerGame', 0),
        'fow': player.get('faceoffWinPctg', 0),
        'w': player.get('wins', 0),
        'l': player.get('losses', 0),
        'otl': player.get('overtimeLosses', 0),
        'sa': player.get('shotsAgainst', 0),
        'ga': player.get('goalsAgainst', 0),
        'saves': player.get('saves', 0),
        'save_pctg': player.get('savePercentage', 0),
        'gaa': player.get('goalsAgainstAverage', 0)
    }
    if isBoxscore:
        if (player.get('position', '') == "G"):
            stats.update({
                'essa': player.get('evenStrengthShotsAgainst', 0),
                'ppsa': player.get('powerPlayShotsAgainst', 0),
                'shsa': player.get('shortHandedShotsAgainst', 0),
                'ssa': player.get('saveShotsAgainst', 0),
                'save_pctg': player.get('savePctg', 0),
                'esga': player.get('evenStrengthGoalsAgainst', 0),
                'ppga': player.get('powerPlayGoalsAgainst', 0),
                'shga': player.get('shortHandedGoalsAgainst', 0),
                'sa': player.get('shotsAgainst', 0),
                'ga': player.get('goalsAgainst', 0),
                'saves': player.get('saves', 0)
            })
        else:
            stats.update({
                'name': player.get('name', {}).get('default', 'S. John'), #john smith lmao
                'number': player.get('sweaterNumber', 0),
                'position': player.get('position', ''),
                'blocks': player.get('blockedShots', 0),
                'shifts': player.get('shifts', 0),
                'giveaways': player.get('giveaways', 0),
                'takeaways': player.get('takeaways', 0),
                'pim': player.get('pim', 0),
                'hits': player.get('hits', 0),
                'ppg': player.get('powerPlayGoals', 0),
                'sog': player.get('sog', 0),
                'fow': player.get('faceoffWinningPctg', 0),
                'toi': player.get('toi', 0),
            })    
    return stats