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
        print(f"{"Division":<12} {"Team":<22} {"Points":<8} {"W":<4} {"L":<4} {"OTL":<4}")
        print("-" * 69)
        for name, stats in sorted_list:
            print(f"{stats['div']:<12} {name:<22} {stats['points']:<8} {stats['wins']:<4} {stats['losses']:<4} {stats['otl']:<4}")
        choice = input("Sort By: (p)oints, (d)ivision, (t)eam, (q)uit").lower()
        match choice:
            case 'p':
                sort_by = "points"
            case 'd':
                sort_by = "div"
            case 't':
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
            'games': player['gamesPlayed'],
            'goals': player['goals'],
            'assists': player['assists'],
            'points': player['points'],
            '+/-': player['plusMinus'],
            'penalty_minutes': player['penaltyMinutes'],
            'toi': player['avgTimeOnIcePerGame'],
            'faceoffWinPctg': player['faceoffWinPctg']
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

def team_tui():
    team_abbrev = input("What team: ").upper()
    skaters = get_skaters(team_abbrev)
    goalies = get_goalies(team_abbrev)
    subprocess.run(["clear"])
    sorted_skaters = sorted(skaters.items(), key=lambda x: x[1]['first_name'], reverse=True)
    for name, stats in sorted_skaters:
        print(f"{stats['first_name']:<12} [{name}]: {stats['games']}")
    sorted_goalies = sorted(goalies.items(), key=lambda x: x[1]['first_name'], reverse=True)
    for name, stats in sorted_goalies:
        print(f"{stats['first_name']:<12} [{name}]: {stats['games']}")

def main():
    """
    Main function for nhlly
    """
    while True:
        user_input = input("(s)tandings (g)ames (t)eam (q)uit \n what do: ").lower()
        match user_input:
            case 's':
                standings_tui()
            case 'g':
                get_games()
            case 't':
                team_tui()
            case 'q':
                break
            case _:
                print("Invalid input")

if __name__ == '__main__':
    main()