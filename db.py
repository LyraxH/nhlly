import sqlite3

RESET = "\033[0m"

def get_colors(tricode):
    """
    Fetches colors for a given team from attached SQL database
    """
    path = "nhlly_data.db"
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT color_primary, color_secondary, color_accent, neutral_dark, neutral_light FROM colors WHERE tricode = ?", (tricode,))
        row = cursor.fetchone()
        if row:
            primary, secondary, accent, neutral_dark, neutral_light = row
            return primary, secondary, accent, neutral_dark, neutral_light
        else:
            print(f"Error: No colors found for {tricode}")
            return None

def colorize(hex):
    """
    Converts a hex color to an RGB color for use in the terminal
    """
    hex = hex.lstrip("#").upper()
    r = int(hex[0:2], 16)
    g = int(hex[2:4], 16)
    b = int(hex[4:6], 16)
    return f"\033[38;2;{r};{g};{b}m"