import subprocess
from nhlly_db import get_colors, colorize
from nhlly_standings import standings_tui
from nhlly_rosters import roster_tui
from nhlly_schedule import schedule_tui

def main():
    """
    Main function for nhlly
    """
    while True:
        subprocess.run(["clear"])
        user_input = input("(st)andings (sc)hedule (t)eam (r)oster (q)uit \n what do: ").lower()
        match user_input:
            case 'st':
                standings_tui()
            case 'sc':
                schedule_tui()
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