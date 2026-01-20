import subprocess
from nhlly_api_client import get_data
from nhlly_db import get_colors, colorize, RESET

def get_skaters(team_abbrev) -> dict | None:
    """
    Fetches skater stats for a given team
    """
    data = get_data(f"club-stats/{team_abbrev}/now")
    if not data or 'skaters' not in data:
        return None
    return {
        player.get('lastName', {}).get('default', ''): {
            'first_name': player.get('firstName', {}).get('default', ''),
            'player_id': player.get('playerId'),
            'position': player.get('positionCode'),
            'games': player.get('gamesPlayed'),
            'goals': player.get('goals'),
            'assists': player.get('assists'),
            'points': player.get('points'),
            '+/-': player.get('plusMinus'),
            'pim': player.get('penaltyMinutes'),
            'toi': player.get('avgTimeOnIcePerGame'),
            'fow': player.get('faceoffWinPctg')
        }
        for player in data.get('skaters', [])
    }

def get_goalies(team_abbrev) -> dict | None:
    """
    Fetches goalie stats for a given team
    """
    data = get_data(f"club-stats/{team_abbrev}/now")
    if not data or 'goalies' not in data:
        return None
    return {
        player.get('lastName', {}).get('default', ''): {
            'first_name': player.get('firstName', {}).get('default', ''),
            'player_id': player.get('playerId'),
            'games': player.get('gamesPlayed'),
            'wins': player.get('wins'),
            'losses': player.get('losses'),
            'otl': player.get('overtimeLosses'),
            'shutouts': player.get('shutouts'),
            'save_pctg': player.get('savePercentage'),
            'gaa': player.get('goalsAgainstAverage')
        }
        for player in data.get('goalies', [])
    }

def roster_tui():
    team_abbrev = input("What team: ").upper()
    skater_sort_by = "first_name"
    goalie_sort_by = "first_name"
    while True:
        subprocess.run(["clear"])
        skaters = get_skaters(team_abbrev)
        goalies = get_goalies(team_abbrev)
        light, dark, accent = get_colors(team_abbrev, 3)
        print(f" --- team roster {team_abbrev} --- Sort By: {skater_sort_by}")
        print(f"{colorize(light)}-" * 79)
        print(f" {'Pos':<3} {'First Name':<10} {'Last Name':<13} {'GP':<4} {'G':<4} {'A':<4} {'P':<4} {'+/-':<5} {'PIM':<5} {'TOI':<5} {'FOW%':<10}")
        print(f"{colorize(accent)}-{colorize(light)}" * 79)
        sorted_skaters = sorted(skaters.items(), key=lambda x: x[1][skater_sort_by], reverse=True)
        for name, stats in sorted_skaters:
            print(f" {stats['position']:<3} {stats['first_name']:<10} {name:<13} {stats['games']:<4} {stats['goals']:<4} {stats['assists']:<4} {stats['points']:<4} {stats['+/-']:<5} {stats['pim']:<5} {(stats['toi']/60):<5.2f} {stats['fow']:<10}")
        sorted_goalies = sorted(goalies.items(), key=lambda x: x[1][goalie_sort_by], reverse=True)
        print(f"{colorize(light)}-" * 79)
        print(f" {'Pos':<3} {'First Name':<10} {'Last Name':<13} {'GP':<4} {'W':<4} {'L':<4} {'OTL':<4} {'SO':<4} {'SV%':<10} {'GAA':<10}")
        print(f"{colorize(accent)}-{colorize(light)}" * 79)
        for name, stats in sorted_goalies:
            print(f" {"G":<3} {stats['first_name']:<10} {name:<13} {stats['games']:<4} {stats['wins']:<4} {stats['losses']:<4} {stats['otl']:<4} {stats['shutouts']:<4} {stats['save_pctg']:<10} {stats['gaa']:<10}")
        choice = input(f"{RESET}Sort By: (f)irst name, (g)ames, (p)oints, (+/-), (pim), (toi), (fow), (q)uit: ").lower()
        match choice:
            case 'f':
                skater_sort_by = "first_name"
                goalie_sort_by = "first_name"
            case 'g':
                skater_sort_by = "games"
                goalie_sort_by = "games"
            case 'p':
                skater_sort_by = "points"
                goalie_sort_by = "shutouts"
            case '+':
                skater_sort_by = "+/-"
                goalie_sort_by = "sv"
            case 'pim':
                skater_sort_by = "pim"
            case 'toi':
                skater_sort_by = "toi"
                goalie_sort_by = "games"
            case 'fow':
                skater_sort_by = "fow"
                goalie_sort_by = "gaa"
            case 'q':
                break
            case _:
                print("Invalid input")