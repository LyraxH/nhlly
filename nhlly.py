import os
import requests
import subprocess

def get_data(endpoint) -> dict:
    url = "https://api-web.nhle.com/v1/"
    r = requests.get(f"{url}{endpoint}")
    if r.status_code == 200:
        return r.json()
    else:
        return {"error": "Could not retrieve data"}

def get_standings() -> dict | None:
    data = get_data("standings/now")
    if not data or 'standings' not in data:
        return None
    return {
        team['teamName']['default']: {
            'team_abbrev': team['teamAbbrev']['default'],
            'points': team['points'],
            'wins': team['wins'],
            'losses': team['losses'],
            'otl': team['otLosses'],
            'conf': team['conferenceName'],
            'conf_abbrev': team['conferenceAbbrev'],
            'div': team['divisionName'],
            'div_abbrev': team['divisionAbbrev'],
            'abv': team['teamAbbrev']['default']
        }
        for team in data.get('standings', [])
    }

def standings_tui():
    sort_by = "points"
    while True:
        subprocess.run(["clear"])
        standings = get_standings()
        sorted_list = sorted(
            standings.items(),
            key=lambda x: x[1][sort_by] if sort_by != "name" else x[0],
            reverse = (sort_by != "name")
        )
        print(f"--- Standings --- Sort By: {sort_by}")
        print(f"{"Division":<14} {"":<4} {"Team":<22} {"Points":<8} {"W":<4} {"L":<4} {"OTL":<4}")
        print("-" * 69)
        for name, stats in sorted_list:
            print(f"{stats['div']:<14} {stats['team_abbrev']:<4} {name:<22} {stats['points']:<8} {stats['wins']:<4} {stats['losses']:<4} {stats['otl']:<4}")
        choice = input("Sort By: (p)oints, (d)ivision, (p)layoffs, (n)ame, (q)uit: ").lower()
        match choice:
            case 'p':
                sort_by = "points"
            case 'd':
                sort_by = "div"
            case 'p':
                sort_by = "playoffs"
            case 'n':
                sort_by = "name"
            case 'q':
                break
            case _:
                print("Invalid input")

def get_skaters(team_abbrev):
    data = get_data(f"club-stats/{team_abbrev}/now")
    if not data or 'skaters' not in data:
        return None
    return {
        player['lastName']['default']: {
            'first_name': player['firstName']['default'],
            'player_id': player['playerId'],
            'position': player['positionCode'],
            'games': player['gamesPlayed'],
            'goals': player['goals'],
            'assists': player['assists'],
            'points': player['points'],
            '+/-': player['plusMinus'],
            'pim': player['penaltyMinutes'],
            'toi': player['avgTimeOnIcePerGame'],
            'fow': player['faceoffWinPctg']
        }
        for player in data.get('skaters', [])
    }

def get_goalies(team_abbrev):
    data = get_data(f"club-stats/{team_abbrev}/now")
    if not data or 'goalies' not in data:
        return None
    return {
        player['lastName']['default']: {
            'first_name': player['firstName']['default'],
            'player_id': player['playerId'],
            'games': player['gamesPlayed'],
            'wins': player['wins'],
            'losses': player['losses'],
            'otl': player['overtimeLosses'],
            'shutouts': player['shutouts'],
            'sv': player['savePercentage'],
            'gaa': player['goalsAgainstAverage']
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
        print(f" --- team roster {team_abbrev} --- Sort By: {skater_sort_by}")
        print("-" * 79)
        print(f" {'Pos':<3} {'First Name':<10} {'Last Name':<13} {'GP':<4} {'G':<4} {'A':<4} {'P':<4} {'+/-':<5} {'PIM':<5} {'TOI':<5} {'FOW%':<10}")
        print("-" * 79)
        sorted_skaters = sorted(skaters.items(), key=lambda x: x[1][skater_sort_by], reverse=True)
        for name, stats in sorted_skaters:
            print(f" {stats['position']:<3} {stats['first_name']:<10} {name:<13} {stats['games']:<4} {stats['goals']:<4} {stats['assists']:<4} {stats['points']:<4} {stats['+/-']:<5} {stats['pim']:<5} {(stats['toi']/60):<5.2f} {stats['fow']:<10}")
        sorted_goalies = sorted(goalies.items(), key=lambda x: x[1][goalie_sort_by], reverse=True)
        print("-" * 79)
        print(f" {'Pos':<3} {'First Name':<10} {'Last Name':<13} {'GP':<4} {'W':<4} {'L':<4} {'OTL':<4} {'SO':<4} {'SV%':<10} {'GAA':<10}")
        print("-" * 79)
        for name, stats in sorted_goalies:
            print(f" {"G":<3} {stats['first_name']:<10} {name:<13} {stats['games']:<4} {stats['wins']:<4} {stats['losses']:<4} {stats['otl']:<4} {stats['shutouts']:<4} {stats['sv']:<10} {stats['gaa']:<10}")
        choice = input("Sort By: (f)irst name, (g)ames, (p)oints, (+/-), (pim), (toi), (fow), (q)uit: ").lower()
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
                skater_sort_by = "faceoffWinPctg"
                goalie_sort_by = "gaa"
            case 'q':
                break
            case _:
                print("Invalid input")
                

def main():
    """
    Main function for nhlly
    """
    while True:
        user_input = input("(s)tandings (g)ames (t)eam (r)oster (q)uit \n what do: ").lower()
        match user_input:
            case 's':
                standings_tui()
            case 'g':
                get_games()
            case 'r':
                roster_tui()
            case 't':
                team_tui()
            case 'q':
                break
            case _:
                print("Invalid input")

if __name__ == '__main__':
    main()