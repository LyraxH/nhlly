import sqlite3

RESET = "\033[0m"

def get_colors(code, color_num):
    """
    Fetches colors for a given team from attached SQL database
    """
    path = "nhlly_data.db"
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT light, dark, accent FROM colors WHERE code = ?", (code,))
        row = cursor.fetchone()
        if row:
            light, dark, accent= row
            match color_num:
                case 1:
                    return light
                case 2:
                    return light, dark
                case 3:
                    return light, dark, accent
        else:
            print(f"Error: No colors found for {code}")
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