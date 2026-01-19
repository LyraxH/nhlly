import subprocess
from db import get_colors, colorize
from standings import standings_tui
from rosters import roster_tui
from game_calendar import calendar_tui

def main():
    """
    Main function for nhlly
    """
    while True:
        user_input = input("(s)tandings (c)alendar (t)eam (r)oster (q)uit \n what do: ").lower()
        match user_input:
            case 's':
                standings_tui()
            case 'c':
                calendar_tui()
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