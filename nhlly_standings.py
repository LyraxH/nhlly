import subprocess
from nhlly_api_client import get_data
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
        print(f"--- Standings --- Sort By: {sort_by}")
        print(f"{"Conference":<12}{"Division":<15}{"Team":<28}{"P":<4}{"W":<4}{"L":<4}{"OTL":<4}{"PCT":<4}")
        print("-" * 80)
        for name, stats in standings_sorted:
            match color_by:
                case "name":
                    color_primary, color_secondary, color_accent, neutral_dark, neutral_light = get_colors(stats['team_abbrev'], 5)
                case "div":
                    color_primary, color_secondary, color_accent, neutral_dark, neutral_light = get_colors(stats['div_abbrev'], 5)
                case "conf":
                    color_primary, color_secondary, color_accent, neutral_dark, neutral_light = get_colors(stats['conf_abbrev'], 5)
                case "playoffs":
                    color_primary, color_secondary, color_accent, neutral_dark, neutral_light = get_colors("CLI", 5)
            print(f"{stats['conf']:<12}{stats['div']:<15}{colorize(color_primary)}{stats['team_abbrev']:<6}{RESET}{colorize(color_secondary)}{name:<22}{RESET}{stats['points']:<4}{stats['wins']:<4}{stats['losses']:<4}{stats['otl']:<4}{stats['win_pctg']:<4.2f}")
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