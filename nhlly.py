import requests

def get_standings() -> dict | None:
    data = get_data("standings/now")
    if not data or 'standings' not in data:
        return None
    return {
        team['teamName']['default']: {
            "team_abbrev": team['teamAbbrev']['default'],
            "points": team['points'],
            "wins": team['wins'],
            "losses": team['losses'],
            "conf": team['conferenceName'],
            "conf_abbrev": team['conferenceAbbrev'],
            "div": team['divisionName'],
            "div_abbrev": team['divisionAbbrev'],
            "abv": team['teamAbbrev']['default']
        }
        for team in data.get('standings', [])
    }

def get_team():
    data = get_data("teams")
    
def get_data(endpoint) -> dict:
    url = "https://api-web.nhle.com/v1/"
    r = requests.get(f"{url}{endpoint}")
    
    if r.status_code == 200:
        return r.json()
    else:
        return {"error": "Could not retrieve data"}

def main():
    """
    Main function for nhlly
    """
    while True:
        user_input = input("(s)tandings (g)ames (p)layers (q)uit \n what do: ").lower()
        match user_input:
            case 's':
                standings = get_standings()
                if standings:
                    print(f"{'DIV':<6} {'ABV':<5} {'TEAM':<22} {'PTS':<5} {'W':<4} {'L'}")
                    print("-" * 55)
                    for name, stats in standings.items():
                        print(f"{stats['div_abbrev']:<6} "
                              f"{stats['team_abbrev']:<5} "
                              f"{name:<22}"
                              f"{stats['points']:<5} "
                              f"{stats['wins']:<4} "
                              f"{stats['losses']}")
                else:
                    print("No standings data")

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