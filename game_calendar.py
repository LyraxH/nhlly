import subprocess
from datetime import datetime, timedelta # Essential for date math
from api_client import get_data
from db import get_colors, colorize, RESET
from game_center import view_gamecenter

def get_schedule_for_date(date_str):
    """
    Fetches the schedule starting specifically at date_str
    """
    data = get_data(f"schedule/{date_str}")
    week = data.get('gameWeek', [])
    if not week:
        return None
    day_data = week[0] 
    return {
        'date': day_data.get('date'),
        'games': day_data.get('games', [])
    }

def calendar_tui():
    current_date = datetime.now()
    while True:
        date_str = current_date.strftime("%Y-%m-%d")
        schedule = get_schedule_for_date(date_str)
        subprocess.run(["clear"])
        if not schedule or not schedule['games']:
            print(f"--- No games scheduled for {date_str} ---")
        else:
            print(f"--- Games for {schedule['date']} ---")
            game_number = 0
            for game in schedule['games']:
                away_color_primary, away_color_secondary, away_color_accent, away_neutral_dark, away_neutral_light = get_colors(game['awayTeam']['abbrev'])
                home_color_primary, home_color_secondary, home_color_accent, home_neutral_dark, home_neutral_light = get_colors(game['homeTeam']['abbrev'])
                away = game['awayTeam']['abbrev']
                home = game['homeTeam']['abbrev']
                print(f"{game_number}.  {colorize(away_color_primary)}{away}{RESET} @ {colorize(home_color_primary)}{home}{RESET}")
                game_number += 1
        choice = input(f"{RESET}(y)esterday (t)omorrow (#)View Game (q)uit: ").lower()
        match choice:
            case 't':
                current_date += timedelta(days=1)
            case 'y':
                current_date -= timedelta(days=1)
            case 'q':
                break
            case x if x.isnumeric():
                view_gamecenter(x)
            case _:
                print("Invalid input")