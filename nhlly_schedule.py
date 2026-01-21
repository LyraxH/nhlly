import subprocess
from datetime import datetime, timedelta
from nhlly_utils import get_data
from nhlly_db import get_colors, colorize, RESET
from nhlly_gamecenter import game_ataglance_tui

def get_schedule(date_str):
    """
    Fetches the schedule starting specifically at date_str
    """
    week = get_data(f"schedule/{date_str}").get('gameWeek', [])
    if not week:
        return None
    day = week[0]
    game_id = day.get('games', [])[0].get('id')
    return {
        'date': day.get('date'),
        'dayAbbrev': day.get('dayAbbrev'),
        'games': day.get('games', []),
        'game_id': game_id,
    }

def schedule_tui():
    current_date = datetime.now()
    while True:
        date = current_date.strftime("%Y-%m-%d")
        schedule = get_schedule(date)
        subprocess.run(["clear"])
        if not schedule or not schedule['games']:
            print(f"--- No games scheduled for {date} ---")
        else:
            print(f"--- Games for {schedule['dayAbbrev']} {schedule['date']} ---")
            game_info = {}
            for i, game in enumerate(schedule['games'], start=1):
                game_id = game.get('id')
                state = game.get('gameState', '')
                game_info[str(i)] = game_id
                away = game.get('awayTeam', {}).get('abbrev', '')
                home = game.get('homeTeam', {}).get('abbrev', '')
                away_color_primary = get_colors(away, 1)
                home_color_primary = get_colors(home, 1)
                print(f"{i:>2}. {colorize(away_color_primary)}{away}{RESET} @ {colorize(home_color_primary)}{home}{RESET} - {state}")
        choice = input(f"{RESET}(y)esterday (t)omorrow (#)View Game (q)uit: ").lower()
        match choice:
            case 't':
                current_date += timedelta(days=1)
            case 'y':
                current_date -= timedelta(days=1)
            case 'q':
                break
            case x if x in game_info: #advanced stats
                game_ataglance_tui(game_info[x])
            case _:
                print("Invalid input")
