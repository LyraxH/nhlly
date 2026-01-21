import subprocess
from nhlly_utils import get_data
from nhlly_db import get_colors, colorize, RESET

def get_standings() -> dict | None:
    """
    Fetches standings data from Official NHL API
    """
    data = get_data("standings/now")
    if not data or 'standings' not in data:
        return None
    return {
        team.get('teamName', {}).get('default', ''): {
            'team_abbrev': team.get('teamAbbrev', {}).get('default', ''),
            'points': team.get('points'),
            'wins': team.get('wins'),
            'losses': team.get('losses'),
            'otl': team.get('otLosses'),
            'conf': team.get('conferenceName'),
            'conf_abbrev': team.get('conferenceAbbrev'),
            'div': team.get('divisionName'),
            'div_abbrev': team.get('divisionAbbrev'),
            'abv': team.get('teamAbbrev', {}).get('default', ''),
            'wildcard': team.get('wildcardSequence', 0),
            'win_pctg': team.get('winPctg')
        }
        for team in data.get('standings', [])
    }

def standings_tui():
    sort_by = "points"
    color_by = "name"
    while True:
        subprocess.run(["clear"])
        standings = get_standings()
        standings_sorted = sorted(standings.items(), key=lambda x: x[1][sort_by], reverse = True)
        print(f"--- Standings ---\nSort By: {sort_by}")
        print(f"{"Conference":<12}{"Division":<15}{"Team":<28}{"P":<4}{"W":<4}{"L":<4}{"OTL":<4}{"PCT":<4}")
        print("-" * 80)
        for name, stats in standings_sorted:
            match color_by:
                case "name":
                    light, dark, accent = get_colors(stats['team_abbrev'], 3)
                case "div":
                    light, dark, accent = get_colors(stats['div_abbrev'], 3)
                case "conf":
                    light, dark, accent = get_colors(stats['conf_abbrev'], 3)
                case "playoffs":
                    light, dark, accent = get_colors("CLI", 3)
            print(f"{stats['conf']:<12}{stats['div']:<15}{colorize(light)}{stats['team_abbrev']:<6}{colorize(dark)}{name:<22}{colorize(light)}{stats['points']:<4}{stats['wins']:<4}{stats['losses']:<4}{stats['otl']:<4}{stats['win_pctg']:<4.2f}{RESET}")
        choice = input("Sort By: (p)oints, (c)onference, (d)ivision, (p)layoffs, (n)ame, (q)uit: ").lower()
        match choice:
            case 'p':
                sort_by = "points"
                color_by = "name"
            case 'd':
                sort_by = "div"
                color_by = "div"
            case 'c':
                sort_by = "conf"
                color_by = "conf"
            case 'pl':
                sort_by = "wildcard"
                color_by = "wildcard"
            case 'n':
                sort_by = "name"
                color_by = "name"
            case 'q':
                break
            case _:
                print("Invalid input")