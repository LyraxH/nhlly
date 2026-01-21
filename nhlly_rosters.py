import subprocess
from nhlly_db import get_colors, colorize, RESET
from nhlly_utils import draw_table

def roster_tui():
    team_abbrev = input("What team: ").upper()
    skater_sort_by = "name"
    goalie_sort_by = "name"
    while True:
        draw_table(team_abbrev, skater_sort_by, goalie_sort_by)
        choice = input(f"{RESET}Sort By: (n)ame, (g)ames, (p)oints, (+/-), (pim), (toi), (fow), (q)uit: ").lower()
        match choice:
            case 'n':
                skater_sort_by = "name"
                goalie_sort_by = "name"
            case 'g':
                skater_sort_by = "gp"
                goalie_sort_by = "gp"
            case 'p':
                skater_sort_by = "points"
                goalie_sort_by = "shutouts"
            case '+':
                skater_sort_by = "+/-"
                goalie_sort_by = "save_pctg"
            case 'pim':
                skater_sort_by = "pim"
            case 'toi':
                skater_sort_by = "toi"
                goalie_sort_by = "gaa"
            case 'fow':
                skater_sort_by = "fow"
                goalie_sort_by = "save_pctg"
            case 'q':
                break
            case _:
                print("Invalid input")