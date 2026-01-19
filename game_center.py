import subprocess
from api_client import get_data
from db import get_colors, colorize, RESET

def view_gamecenter(game_number):
    subprocess.run(["clear"])
    