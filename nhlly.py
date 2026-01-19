import subprocess
from db import get_colors, colorize
from standings import standings_tui
from rosters import roster_tui
from api_client import get_data

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