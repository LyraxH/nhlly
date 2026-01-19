import subprocess
from api_client import get_data
from db import get_colors, colorize, RESET

def view_gamecenter(game_number):
    game_data = get_data(f"gamecenter/{game_number}/landing")
    while True:
        subprocess.run(["clear"])
        print(game_data)
        choice = input("\n What Do: ").lower()
        match choice:
            case 'q':
                break
            case _:
                print("Invalid input")
    

def view_boxscore(game_number):
    game_data = get_data(f"gamecenter/{game_number}/boxscore")
    while True:
        subprocess.run(["clear"])
        print(game_data)
        choice = input("\n What Do: ").lower()
        match choice:
            case 'q':
                break
            case _:
                print("Invalid input")

def view_pbp(game_number):
    game_data = get_data(f"gamecenter/{game_number}/play-by-play")
    while True:
        subprocess.run(["clear"])
        print(game_data)
        choice = input("\n What Do: ").lower()
        match choice:
            case 'q':
                break
            case _:
                print("Invalid input")