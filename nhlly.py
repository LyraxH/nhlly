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
        print(f"{"Division":<12} {"Team":<22} {"Points":<8} {"W":<4} {"L":<4}")
        print("-" * 60)
        for name, stats in sorted_list:
            print(f"{stats['div']:<12} {name:<22} {stats['points']:<8} {stats['wins']:<4} {stats['losses']:<4}")
        print("\n Sort By: (p)oints, (d)ivision, (t)eam, (q)uit")
        choice = input("\nChoose an option: ").lower()
        match choice:
            case 'p':
                sort_by = "points"
            case 'd':
                sort_by = "div"
            case 't':
                sort_by = "team"
            case 'q':
                break
            case _:
                print("Invalid input")

def main():
    """
    Main function for nhlly
    """
    while True:
        user_input = input("(s)tandings (g)ames (p)layoffs (q)uit \n what do: ").lower()
        match user_input:
            case 's':
                standings_tui()
            case 'g':
                get_games()
            case 'p':
                get_players()
            case 'q':
                break
            case _:
                print("Invalid input")

if __name__ == '__main__':
    main()