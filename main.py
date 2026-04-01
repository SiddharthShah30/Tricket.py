import os
import random
import sys
import time
import json
import math
import shutil
import re
from typing import Any

# Colorama for colored CLI output
try:
    from colorama import init as colorama_init, Fore, Back, Style
    colorama_init(autoreset=True)
except ImportError:
    # Fallback if colorama is not installed
    class Dummy:
        RESET = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = BLACK = BRIGHT = DIM = NORMAL = ''
    Fore = Back = Style = Dummy()

def ctext(text, color=Fore.WHITE, style=Style.NORMAL):
    return f"{style}{color}{text}{Style.RESET_ALL}"

def highlight(text):
    return ctext(text, Fore.CYAN, Style.BRIGHT)

def error_text(text):
    return ctext(text, Fore.RED, Style.BRIGHT)

def success_text(text):
    return ctext(text, Fore.GREEN, Style.BRIGHT)

def info_text(text):
    return ctext(text, Fore.YELLOW, Style.BRIGHT)

def term_width():
    return max(60, shutil.get_terminal_size((108, 36)).columns)

def term_height():
    return max(20, shutil.get_terminal_size((108, 36)).lines)

THEME_ACCENT = Fore.RED
THEME_TEXT = Fore.WHITE

def ui_profile():
    cols = term_width()
    lines = term_height()
    compact = cols < 120 or lines < 34
    return {
        "cols": cols,
        "lines": lines,
        "compact": compact,
    }

def center_line(line):
    width = term_width()
    visible = len(ANSI_RE.sub("", str(line))) if "ANSI_RE" in globals() else len(str(line))
    pad = max(0, (width - visible) // 2)
    print(" " * pad + line)

def draw_center_box(lines, width=84, title=None):
    width = min(width, term_width() - 4)
    top = "╔" + "═" * width + "╗"
    bot = "╚" + "═" * width + "╝"
    center_line(ctext(top, Fore.BLUE, Style.BRIGHT))
    if title:
        t = f"[ {title} ]"
        center_line(ctext("║" + t.center(width) + "║", Fore.CYAN, Style.BRIGHT))
        center_line(ctext("╠" + "═" * width + "╣", Fore.BLUE, Style.BRIGHT))
    for line in lines:
        content = str(line)
        if visible_len(content) > width:
            raw = ANSI_RE.sub("", content)
            content = raw[:width]
        center_line(ctext("║" + pad_visible(content, width) + "║", Fore.WHITE))
    center_line(ctext(bot, Fore.BLUE, Style.BRIGHT))

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")

def visible_len(text):
    return len(ANSI_RE.sub("", str(text)))

def pad_visible(text, width):
    text = str(text)
    extra = max(0, width - visible_len(text))
    return text + (" " * extra)

def progress_bar(value, total=100, width=10):
    if total <= 0:
        total = 1
    ratio = max(0.0, min(1.0, value / total))
    filled = int(round(ratio * width))
    return "[" + ("█" * filled) + ("░" * (width - filled)) + "]"

def normalize_terminal_viewport(min_cols=110, min_lines=34):
    """Only enlarge very small Windows terminals; avoid hard-locking user size."""
    if os.name != "nt":
        return
    cols = shutil.get_terminal_size((108, 36)).columns
    lines = shutil.get_terminal_size((108, 36)).lines
    if cols < min_cols or lines < min_lines:
        os.system(f"mode con: cols={max(cols, min_cols)} lines={max(lines, min_lines)}")

def draw_dual_panels(left_title, left_lines, right_title, right_lines, panel_width=48, gap=4):
    rows = max(len(left_lines), len(right_lines))
    left = left_lines + [""] * (rows - len(left_lines))
    right = right_lines + [""] * (rows - len(right_lines))
    top = ctext("┏" + "━" * panel_width + "┓", Fore.CYAN, Style.BRIGHT)
    mid = ctext("┣" + "━" * panel_width + "┫", Fore.CYAN, Style.BRIGHT)
    bot = ctext("┗" + "━" * panel_width + "┛", Fore.CYAN, Style.BRIGHT)
    sep = " " * gap

    center_line(top + sep + top)
    ltitle = pad_visible(ctext(f" [ {left_title} ]", Fore.CYAN, Style.BRIGHT), panel_width)
    rtitle = pad_visible(ctext(f" [ {right_title} ]", Fore.CYAN, Style.BRIGHT), panel_width)
    center_line(
        ctext("┃", Fore.CYAN, Style.BRIGHT) + ltitle + ctext("┃", Fore.CYAN, Style.BRIGHT)
        + sep +
        ctext("┃", Fore.CYAN, Style.BRIGHT) + rtitle + ctext("┃", Fore.CYAN, Style.BRIGHT)
    )
    center_line(mid + sep + mid)

    for lrow, rrow in zip(left, right):
        ltxt = pad_visible(lrow, panel_width)
        rtxt = pad_visible(rrow, panel_width)
        center_line(
            ctext("┃", Fore.CYAN, Style.BRIGHT) + ltxt + ctext("┃", Fore.CYAN, Style.BRIGHT)
            + sep +
            ctext("┃", Fore.CYAN, Style.BRIGHT) + rtxt + ctext("┃", Fore.CYAN, Style.BRIGHT)
        )

    center_line(bot + sep + bot)

HEADER_BIG = [
    "████████╗██████╗ ██╗██╗  ██╗███████╗████████╗",
    "╚══██╔══╝██╔══██╗██║██║ ██╔╝██╔════╝╚══██╔══╝",
    "   ██║   ██████╔╝██║█████╔╝ █████╗     ██║   ",
    "   ██║   ██╔══██╗██║██╔═██╗ ██╔══╝     ██║   ",
    "   ██║   ██║  ██║██║██║  ██╗███████╗   ██║   ",
    "   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ",
]

def print_header(subtitle="RETRO ARCADE CRICKET"):
    clear()
    profile = ui_profile()
    if profile["compact"]:
        center_line(ctext("TRIKET", THEME_ACCENT, Style.BRIGHT))
    else:
        for line in HEADER_BIG:
            center_line(ctext(line, THEME_ACCENT, Style.BRIGHT))
    center_line(ctext(f"{subtitle}", THEME_ACCENT, Style.BRIGHT))
    print()

def draw_ladder_screen(title, options, selected_idx, accent=THEME_ACCENT,
                       subtitle="-- RETRO ARCADE CRICKET --",
                       footer="[W/S] NAVIGATE  |  [ENTER] SELECT  |  [ESC] BACK"):
    print_header(title)
    center_line(ctext(subtitle, accent, Style.BRIGHT))
    print()
    for i, opt in enumerate(options, 1):
        selected = (i - 1) == selected_idx
        if selected:
            line = ctext(f"[[ {i:02d} ]] {opt}", accent, Style.BRIGHT)
        else:
            line = ctext(f"   {i:02d}   {opt}", THEME_TEXT, Style.DIM)
        center_line(line)
    print()
    center_line(ctext(footer, accent, Style.BRIGHT))

def arrow_menu(title, options, hint="Use UP/DOWN and ENTER"):
    idx = 0
    while True:
        draw_ladder_screen(title, options, idx, accent=THEME_ACCENT,
                           subtitle="-- SELECTION --",
                           footer="[W/S] NAVIGATE  |  [ENTER] SELECT  |  [ESC] BACK")
        center_line(ctext(hint, THEME_TEXT, Style.DIM))
        k = get_key()
        if k in ("UP", "W"):
            idx = (idx - 1) % len(options)
        elif k in ("DOWN", "S"):
            idx = (idx + 1) % len(options)
        elif k in ("ENTER",):
            return idx

def draw_main_menu_screen(selected_idx, settings_preview=None):
    clear()
    profile = ui_profile()
    logo_lines = HEADER_BIG if not profile["compact"] else ["TRIKET"]

    content_lines = 1 + len(logo_lines) + 1 + 1 + 1 + 4 + 1 + (2 if settings_preview else 0) + 1
    top_pad = max(0, (profile["lines"] - content_lines) // 3)
    for _ in range(top_pad):
        print()

    print()
    for line in logo_lines:
        center_line(ctext(line, THEME_ACCENT, Style.BRIGHT))
    print()

    anchor = "──── RETRO ARCADE CRICKET ────"
    center_line(ctext(anchor, THEME_ACCENT, Style.BRIGHT))
    print("\n")

    options = ["QUICK MATCH", "RECORDS", "SETTINGS", "QUIT GAME"]
    for i, label in enumerate(options, 1):
        selected = (i - 1) == selected_idx
        if selected:
            item = ctext(f"[[ {i:02d} ]] {label}", THEME_ACCENT, Style.BRIGHT)
        else:
            item = ctext(f"   {i:02d}   {label}", THEME_TEXT, Style.DIM)
        center_line(item)

    print("\n")
    if settings_preview:
        center_line(ctext(f"CURRENT: {settings_preview}", THEME_TEXT, Style.DIM))
        print()

    footer = ctext("[W/S] NAVIGATE  |  [ENTER] EXECUTE  |  [ESC] SYSTEM", THEME_ACCENT, Style.BRIGHT)
    center_line(footer)

TEAM_SELECT_HEADER_LINES = [
    "████████╗███████╗ █████╗ ███╗   ███╗    ███████╗███████╗██╗     ███████╗ ██████╗████████╗",
    "╚══██╔══╝██╔════╝██╔══██╗████╗ ████║    ██╔════╝██╔════╝██║     ██╔════╝██╔════╝╚══██╔══╝",
    "   ██║   █████╗  ███████║██╔████╔██║    ███████╗█████╗  ██║     █████╗  ██║        ██║   ",
    "   ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║    ╚════██║██╔══╝  ██║     ██╔══╝  ██║        ██║   ",
    "   ██║   ███████╗██║  ██║██║ ╚═╝ ██║    ███████║███████╗███████╗███████╗╚██████╗   ██║   ",
    "   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝    ╚══════╝╚══════╝╚══════╝╚══════╝ ╚═════╝   ╚═╝   ",
]

def draw_ascii_header(lines, color=Fore.CYAN, fixed_height=6):
    padded = list(lines[:fixed_height]) + [""] * max(0, fixed_height - len(lines))
    for line in padded:
        center_line(ctext(line, color, Style.BRIGHT))

def draw_team_select_screen(selected_idx, teams):
    clear()
    profile = ui_profile()
    header_lines = TEAM_SELECT_HEADER_LINES if (not profile["compact"] and profile["cols"] >= 120) else ["TEAM SELECT"]
    content_lines = 1 + len(header_lines) + 1 + 1 + 1 + len(teams) + 1 + 1
    top_pad = max(0, (profile["lines"] - content_lines) // 3)
    for _ in range(top_pad):
        print()

    print()
    draw_ascii_header(header_lines, color=THEME_ACCENT, fixed_height=len(header_lines))

    print()
    center_line(ctext("── ASSEMBLE YOUR SQUAD ──", THEME_ACCENT, Style.BRIGHT))
    print("\n")

    for i, team in enumerate(teams, 1):
        selected = (i - 1) == selected_idx
        if selected:
            line = ctext(f"[[ {i:02d} ]] {team.upper()}", THEME_ACCENT, Style.BRIGHT)
        else:
            line = ctext(f"   {i:02d}   {team.upper()}", THEME_TEXT, Style.DIM)
        center_line(line)

    footer = ctext("[TRIKET // v2.6]  [W/S] NAVIGATE   |   [ENTER] SELECT   |   [ESC] BACK", THEME_ACCENT, Style.BRIGHT)
    print()
    center_line(footer)

ZONE_GRID = [
    ["1", "2", "3"],
    ["6", "5", "4"],
    ["7", "8", "9"],
]

ZONE_POS = {z: (r, c) for r, row in enumerate(ZONE_GRID) for c, z in enumerate(row)}

def move_zone(selected, key):
    r, c = ZONE_POS.get(selected, (1, 1))
    if key == "LEFT":
        c = max(0, c - 1)
    elif key == "RIGHT":
        c = min(2, c + 1)
    elif key == "UP":
        r = max(0, r - 1)
    elif key == "DOWN":
        r = min(2, r + 1)
    return ZONE_GRID[r][c]

def draw_modern_field(selected_zone=None):
    selected_zone = selected_zone or "5"

    def ztxt(z, name):
        if selected_zone == z:
            return ctext(f"▶{z}:{name}", Fore.YELLOW, Style.BRIGHT)
        return ctext(f" {z}:{name}", Fore.CYAN, Style.NORMAL)

    lines = [
        "",
        ctext("                 RETRO ARENA VIEW", Fore.GREEN, Style.BRIGHT),
        "",
        f"      {ztxt('1', '3rd')}         {ztxt('2', 'Cover')}       {ztxt('3', 'MidOff')}",
        "",
        "           . . . . . . . . . BOUNDARY . . . . . . . . .",
        "",
        f"      {ztxt('6', 'Fine')}         {ztxt('5', 'Straight')}   {ztxt('4', 'MidWkt')}",
        "",
        "                     [  P I T C H  ]",
        "",
        f"      {ztxt('7', 'MidOn')}       {ztxt('8', 'LongOn')}     {ztxt('9', 'LongOff')}",
        "",
        ctext("       Arrows move zone. Enter confirms. Number keys 1-9 also work.", Fore.MAGENTA),
    ]
    draw_center_box(lines, title="MATCH ARENA")

# =========================
# TEAMS
# =========================

TEAMS = {
    "India": [
        "Rohit Sharma", "Shubman Gill", "Virat Kohli",
        "Shreyas Iyer", "KL Rahul",
        "Hardik Pandya", "Ravindra Jadeja",
        "Jasprit Bumrah", "Mohammed Shami",
        "Mohammed Siraj", "Kuldeep Yadav"
    ],
    "Australia": [
        "David Warner", "Travis Head", "Steve Smith",
        "Marnus Labuschagne", "Glenn Maxwell",
        "Marcus Stoinis", "Alex Carey",
        "Pat Cummins", "Mitchell Starc",
        "Josh Hazlewood", "Adam Zampa"
    ],
    "England": [
        "Jason Roy", "Jonny Bairstow", "Joe Root",
        "Ben Stokes", "Jos Buttler",
        "Liam Livingstone", "Moeen Ali",
        "Mark Wood", "Jofra Archer",
        "Adil Rashid", "Reece Topley"
    ],
    "New Zealand": [
        "Devon Conway", "Will Young", "Kane Williamson",
        "Daryl Mitchell", "Glenn Phillips",
        "Tom Latham", "Mitchell Santner",
        "Trent Boult", "Tim Southee",
        "Matt Henry", "Ish Sodhi"
    ],
    "South Africa": [
        "Quinton de Kock", "Temba Bavuma", "Aiden Markram",
        "Rassie van der Dussen", "David Miller",
        "Marco Jansen", "Kagiso Rabada",
        "Anrich Nortje", "Lungi Ngidi",
        "Keshav Maharaj", "Tabraiz Shamsi"
    ],
    "Pakistan": [
        "Babar Azam", "Mohammad Rizwan", "Fakhar Zaman",
        "Imam-ul-Haq", "Saud Shakeel",
        "Shadab Khan", "Iftikhar Ahmed",
        "Shaheen Afridi", "Naseem Shah",
        "Haris Rauf", "Usama Mir"
    ],
    "Sri Lanka": [
        "Pathum Nissanka", "Kusal Mendis", "Charith Asalanka",
        "Dhananjaya de Silva", "Sadeera Samarawickrama",
        "Wanindu Hasaranga", "Dasun Shanaka",
        "Maheesh Theekshana", "Dilshan Madushanka",
        "Matheesha Pathirana", "Kasun Rajitha"
    ],
    "West Indies": [
        "Brandon King", "Shai Hope", "Nicholas Pooran",
        "Shimron Hetmyer", "Rovman Powell",
        "Jason Holder", "Andre Russell",
        "Alzarri Joseph", "Akeal Hosein",
        "Romario Shepherd", "Gudakesh Motie"
    ],
    "Bangladesh": [
        "Litton Das", "Najmul Hossain Shanto", "Shakib Al Hasan",
        "Mushfiqur Rahim", "Mehidy Hasan Miraz",
        "Mahmudullah", "Taskin Ahmed",
        "Mustafizur Rahman", "Nasum Ahmed",
        "Tanzim Hasan Sakib", "Rishad Hossain"
    ],
    "Afghanistan": [
        "Rahmanullah Gurbaz", "Ibrahim Zadran", "Hashmatullah Shahidi",
        "Azmatullah Omarzai", "Mohammad Nabi",
        "Rashid Khan", "Mujeeb Ur Rahman",
        "Fazalhaq Farooqi", "Naveen-ul-Haq",
        "Noor Ahmad", "Gulbadin Naib"
    ]
}

def short(name):
    parts = name.split()
    if len(parts) >= 2:
        return parts[0][0] + ". " + " ".join(parts[1:])
    return name

# =========================
# PLAYER ATTRIBUTES
# =========================

PLAYER_STATS = {
    "Rohit Sharma":           {"bat_skill": 88, "aggression": 90, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 80},
    "Shubman Gill":           {"bat_skill": 82, "aggression": 75, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 85},
    "Virat Kohli":            {"bat_skill": 95, "aggression": 80, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 90},
    "Shreyas Iyer":           {"bat_skill": 78, "aggression": 82, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 78},
    "KL Rahul":               {"bat_skill": 80, "aggression": 72, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 82},
    "Hardik Pandya":          {"bat_skill": 72, "aggression": 95, "bowl_skill": 72, "bowl_type": "medium", "stamina": 70},
    "Ravindra Jadeja":        {"bat_skill": 65, "aggression": 78, "bowl_skill": 78, "bowl_type": "spin",   "stamina": 85},
    "Jasprit Bumrah":         {"bat_skill": 10, "aggression": 50, "bowl_skill": 96, "bowl_type": "pace",   "stamina": 75},
    "Mohammed Shami":         {"bat_skill": 12, "aggression": 50, "bowl_skill": 88, "bowl_type": "pace",   "stamina": 72},
    "Mohammed Siraj":         {"bat_skill": 8,  "aggression": 45, "bowl_skill": 82, "bowl_type": "pace",   "stamina": 70},
    "Kuldeep Yadav":          {"bat_skill": 15, "aggression": 55, "bowl_skill": 85, "bowl_type": "spin",   "stamina": 80},
    "David Warner":           {"bat_skill": 85, "aggression": 95, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 80},
    "Travis Head":            {"bat_skill": 80, "aggression": 98, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 85},
    "Steve Smith":            {"bat_skill": 93, "aggression": 70, "bowl_skill": 30, "bowl_type": "spin",   "stamina": 88},
    "Marnus Labuschagne":     {"bat_skill": 82, "aggression": 68, "bowl_skill": 35, "bowl_type": "medium", "stamina": 85},
    "Glenn Maxwell":          {"bat_skill": 75, "aggression": 105,"bowl_skill": 60, "bowl_type": "spin",   "stamina": 72},
    "Marcus Stoinis":         {"bat_skill": 68, "aggression": 92, "bowl_skill": 58, "bowl_type": "medium", "stamina": 74},
    "Alex Carey":             {"bat_skill": 65, "aggression": 80, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 78},
    "Pat Cummins":            {"bat_skill": 35, "aggression": 70, "bowl_skill": 92, "bowl_type": "pace",   "stamina": 78},
    "Mitchell Starc":         {"bat_skill": 22, "aggression": 70, "bowl_skill": 88, "bowl_type": "pace",   "stamina": 72},
    "Josh Hazlewood":         {"bat_skill": 10, "aggression": 50, "bowl_skill": 87, "bowl_type": "pace",   "stamina": 75},
    "Adam Zampa":             {"bat_skill": 18, "aggression": 60, "bowl_skill": 83, "bowl_type": "spin",   "stamina": 80},
    "Jason Roy":              {"bat_skill": 78, "aggression": 100,"bowl_skill": 10, "bowl_type": "bat",    "stamina": 78},
    "Jonny Bairstow":         {"bat_skill": 80, "aggression": 95, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 80},
    "Joe Root":               {"bat_skill": 90, "aggression": 72, "bowl_skill": 45, "bowl_type": "spin",   "stamina": 88},
    "Ben Stokes":             {"bat_skill": 78, "aggression": 88, "bowl_skill": 75, "bowl_type": "medium", "stamina": 75},
    "Jos Buttler":            {"bat_skill": 83, "aggression": 103,"bowl_skill": 10, "bowl_type": "bat",    "stamina": 80},
    "Liam Livingstone":       {"bat_skill": 70, "aggression": 108,"bowl_skill": 52, "bowl_type": "spin",   "stamina": 76},
    "Moeen Ali":              {"bat_skill": 60, "aggression": 90, "bowl_skill": 70, "bowl_type": "spin",   "stamina": 78},
    "Mark Wood":              {"bat_skill": 20, "aggression": 68, "bowl_skill": 82, "bowl_type": "pace",   "stamina": 68},
    "Jofra Archer":           {"bat_skill": 18, "aggression": 65, "bowl_skill": 85, "bowl_type": "pace",   "stamina": 70},
    "Adil Rashid":            {"bat_skill": 25, "aggression": 60, "bowl_skill": 80, "bowl_type": "spin",   "stamina": 78},
    "Reece Topley":           {"bat_skill": 8,  "aggression": 45, "bowl_skill": 75, "bowl_type": "pace",   "stamina": 72},
    "Devon Conway":           {"bat_skill": 82, "aggression": 72, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 85},
    "Will Young":             {"bat_skill": 72, "aggression": 68, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 80},
    "Kane Williamson":        {"bat_skill": 93, "aggression": 70, "bowl_skill": 35, "bowl_type": "spin",   "stamina": 88},
    "Daryl Mitchell":         {"bat_skill": 75, "aggression": 85, "bowl_skill": 42, "bowl_type": "medium", "stamina": 78},
    "Glenn Phillips":         {"bat_skill": 72, "aggression": 95, "bowl_skill": 40, "bowl_type": "spin",   "stamina": 75},
    "Tom Latham":             {"bat_skill": 68, "aggression": 70, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 80},
    "Mitchell Santner":       {"bat_skill": 55, "aggression": 80, "bowl_skill": 75, "bowl_type": "spin",   "stamina": 82},
    "Trent Boult":            {"bat_skill": 15, "aggression": 55, "bowl_skill": 88, "bowl_type": "pace",   "stamina": 75},
    "Tim Southee":            {"bat_skill": 28, "aggression": 65, "bowl_skill": 82, "bowl_type": "pace",   "stamina": 72},
    "Matt Henry":             {"bat_skill": 18, "aggression": 60, "bowl_skill": 80, "bowl_type": "pace",   "stamina": 74},
    "Ish Sodhi":              {"bat_skill": 22, "aggression": 65, "bowl_skill": 78, "bowl_type": "spin",   "stamina": 78},
    "Quinton de Kock":        {"bat_skill": 83, "aggression": 95, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 82},
    "Temba Bavuma":           {"bat_skill": 75, "aggression": 68, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 78},
    "Aiden Markram":          {"bat_skill": 80, "aggression": 78, "bowl_skill": 45, "bowl_type": "spin",   "stamina": 80},
    "Rassie van der Dussen":  {"bat_skill": 78, "aggression": 75, "bowl_skill": 15, "bowl_type": "medium", "stamina": 80},
    "David Miller":           {"bat_skill": 72, "aggression": 100,"bowl_skill": 10, "bowl_type": "bat",    "stamina": 78},
    "Marco Jansen":           {"bat_skill": 45, "aggression": 80, "bowl_skill": 80, "bowl_type": "pace",   "stamina": 72},
    "Kagiso Rabada":          {"bat_skill": 30, "aggression": 72, "bowl_skill": 92, "bowl_type": "pace",   "stamina": 75},
    "Anrich Nortje":          {"bat_skill": 15, "aggression": 60, "bowl_skill": 88, "bowl_type": "pace",   "stamina": 70},
    "Lungi Ngidi":            {"bat_skill": 12, "aggression": 55, "bowl_skill": 82, "bowl_type": "pace",   "stamina": 72},
    "Keshav Maharaj":         {"bat_skill": 30, "aggression": 60, "bowl_skill": 83, "bowl_type": "spin",   "stamina": 80},
    "Tabraiz Shamsi":         {"bat_skill": 15, "aggression": 55, "bowl_skill": 85, "bowl_type": "spin",   "stamina": 78},
    "Babar Azam":             {"bat_skill": 94, "aggression": 78, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 90},
    "Mohammad Rizwan":        {"bat_skill": 85, "aggression": 80, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 85},
    "Fakhar Zaman":           {"bat_skill": 80, "aggression": 95, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 80},
    "Imam-ul-Haq":            {"bat_skill": 75, "aggression": 65, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 82},
    "Saud Shakeel":           {"bat_skill": 72, "aggression": 65, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 80},
    "Shadab Khan":            {"bat_skill": 60, "aggression": 85, "bowl_skill": 78, "bowl_type": "spin",   "stamina": 78},
    "Iftikhar Ahmed":         {"bat_skill": 65, "aggression": 92, "bowl_skill": 52, "bowl_type": "spin",   "stamina": 75},
    "Shaheen Afridi":         {"bat_skill": 25, "aggression": 65, "bowl_skill": 90, "bowl_type": "pace",   "stamina": 75},
    "Naseem Shah":            {"bat_skill": 18, "aggression": 58, "bowl_skill": 85, "bowl_type": "pace",   "stamina": 72},
    "Haris Rauf":             {"bat_skill": 15, "aggression": 55, "bowl_skill": 82, "bowl_type": "pace",   "stamina": 70},
    "Usama Mir":              {"bat_skill": 20, "aggression": 60, "bowl_skill": 78, "bowl_type": "spin",   "stamina": 78},
    "Pathum Nissanka":        {"bat_skill": 78, "aggression": 72, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 80},
    "Kusal Mendis":           {"bat_skill": 80, "aggression": 88, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 82},
    "Charith Asalanka":       {"bat_skill": 75, "aggression": 85, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 78},
    "Dhananjaya de Silva":    {"bat_skill": 72, "aggression": 78, "bowl_skill": 65, "bowl_type": "spin",   "stamina": 80},
    "Sadeera Samarawickrama": {"bat_skill": 70, "aggression": 82, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 78},
    "Wanindu Hasaranga":      {"bat_skill": 55, "aggression": 80, "bowl_skill": 85, "bowl_type": "spin",   "stamina": 80},
    "Dasun Shanaka":          {"bat_skill": 60, "aggression": 92, "bowl_skill": 55, "bowl_type": "medium", "stamina": 75},
    "Maheesh Theekshana":     {"bat_skill": 20, "aggression": 60, "bowl_skill": 82, "bowl_type": "spin",   "stamina": 78},
    "Dilshan Madushanka":     {"bat_skill": 15, "aggression": 55, "bowl_skill": 80, "bowl_type": "pace",   "stamina": 72},
    "Matheesha Pathirana":    {"bat_skill": 12, "aggression": 50, "bowl_skill": 83, "bowl_type": "pace",   "stamina": 70},
    "Kasun Rajitha":          {"bat_skill": 10, "aggression": 45, "bowl_skill": 78, "bowl_type": "pace",   "stamina": 72},
    "Brandon King":           {"bat_skill": 75, "aggression": 88, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 78},
    "Shai Hope":              {"bat_skill": 80, "aggression": 70, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 82},
    "Nicholas Pooran":        {"bat_skill": 78, "aggression": 100,"bowl_skill": 10, "bowl_type": "bat",    "stamina": 78},
    "Shimron Hetmyer":        {"bat_skill": 72, "aggression": 98, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 75},
    "Rovman Powell":          {"bat_skill": 68, "aggression": 95, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 76},
    "Jason Holder":           {"bat_skill": 60, "aggression": 80, "bowl_skill": 80, "bowl_type": "medium", "stamina": 78},
    "Andre Russell":          {"bat_skill": 70, "aggression": 108,"bowl_skill": 72, "bowl_type": "medium", "stamina": 70},
    "Alzarri Joseph":         {"bat_skill": 22, "aggression": 65, "bowl_skill": 82, "bowl_type": "pace",   "stamina": 72},
    "Akeal Hosein":           {"bat_skill": 30, "aggression": 68, "bowl_skill": 78, "bowl_type": "spin",   "stamina": 78},
    "Romario Shepherd":       {"bat_skill": 45, "aggression": 85, "bowl_skill": 75, "bowl_type": "medium", "stamina": 74},
    "Gudakesh Motie":         {"bat_skill": 20, "aggression": 58, "bowl_skill": 78, "bowl_type": "spin",   "stamina": 78},
    "Litton Das":             {"bat_skill": 78, "aggression": 88, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 80},
    "Najmul Hossain Shanto":  {"bat_skill": 75, "aggression": 72, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 82},
    "Shakib Al Hasan":        {"bat_skill": 72, "aggression": 82, "bowl_skill": 82, "bowl_type": "spin",   "stamina": 85},
    "Mushfiqur Rahim":        {"bat_skill": 75, "aggression": 75, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 80},
    "Mehidy Hasan Miraz":     {"bat_skill": 60, "aggression": 72, "bowl_skill": 80, "bowl_type": "spin",   "stamina": 80},
    "Mahmudullah":            {"bat_skill": 65, "aggression": 80, "bowl_skill": 55, "bowl_type": "spin",   "stamina": 78},
    "Taskin Ahmed":           {"bat_skill": 18, "aggression": 58, "bowl_skill": 82, "bowl_type": "pace",   "stamina": 72},
    "Mustafizur Rahman":      {"bat_skill": 15, "aggression": 55, "bowl_skill": 85, "bowl_type": "pace",   "stamina": 74},
    "Nasum Ahmed":            {"bat_skill": 18, "aggression": 55, "bowl_skill": 78, "bowl_type": "spin",   "stamina": 78},
    "Tanzim Hasan Sakib":     {"bat_skill": 12, "aggression": 50, "bowl_skill": 76, "bowl_type": "pace",   "stamina": 70},
    "Rishad Hossain":         {"bat_skill": 20, "aggression": 60, "bowl_skill": 78, "bowl_type": "spin",   "stamina": 78},
    "Rahmanullah Gurbaz":     {"bat_skill": 78, "aggression": 90, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 80},
    "Ibrahim Zadran":         {"bat_skill": 72, "aggression": 70, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 80},
    "Hashmatullah Shahidi":   {"bat_skill": 70, "aggression": 62, "bowl_skill": 10, "bowl_type": "bat",    "stamina": 80},
    "Azmatullah Omarzai":     {"bat_skill": 65, "aggression": 85, "bowl_skill": 60, "bowl_type": "medium", "stamina": 75},
    "Mohammad Nabi":          {"bat_skill": 65, "aggression": 80, "bowl_skill": 75, "bowl_type": "spin",   "stamina": 80},
    "Rashid Khan":            {"bat_skill": 48, "aggression": 85, "bowl_skill": 95, "bowl_type": "spin",   "stamina": 85},
    "Mujeeb Ur Rahman":       {"bat_skill": 15, "aggression": 55, "bowl_skill": 85, "bowl_type": "spin",   "stamina": 78},
    "Fazalhaq Farooqi":       {"bat_skill": 15, "aggression": 55, "bowl_skill": 83, "bowl_type": "pace",   "stamina": 72},
    "Naveen-ul-Haq":          {"bat_skill": 18, "aggression": 58, "bowl_skill": 80, "bowl_type": "pace",   "stamina": 70},
    "Noor Ahmad":             {"bat_skill": 15, "aggression": 52, "bowl_skill": 82, "bowl_type": "spin",   "stamina": 78},
    "Gulbadin Naib":          {"bat_skill": 52, "aggression": 78, "bowl_skill": 68, "bowl_type": "medium", "stamina": 75},
}

def get_stat(player: str, key: str, default: Any = 50) -> Any:
    return PLAYER_STATS.get(player, {}).get(key, default)

# =========================
# PITCH & WEATHER  (halved modifiers to reduce swing)
# =========================

PITCH_TYPES = {
    "Flat":      {"pace_mod": -0.05, "spin_mod": -0.08, "bat_mod": +0.10},
    "Green Top": {"pace_mod": +0.10, "spin_mod": -0.05, "bat_mod": -0.05},
    "Dusty":     {"pace_mod": -0.05, "spin_mod": +0.10, "bat_mod": -0.05},
    "Slow":      {"pace_mod": -0.03, "spin_mod": +0.05, "bat_mod": -0.03},
}
WEATHER_CONDITIONS = {
    "Sunny":    {"swing_mod": -0.05},
    "Overcast": {"swing_mod": +0.10},
    "Humid":    {"swing_mod": +0.06},
    "Windy":    {"swing_mod": +0.03},
}

DIFFICULTY_SETTINGS = {
    "Easy":   {"user_run_mod": 1.08, "user_wicket_mod": 0.90, "ai_review": 0.28, "ai_aggr": 0.92},
    "Normal": {"user_run_mod": 1.00, "user_wicket_mod": 1.00, "ai_review": 0.40, "ai_aggr": 1.00},
    "Hard":   {"user_run_mod": 0.92, "user_wicket_mod": 1.10, "ai_review": 0.50, "ai_aggr": 1.10},
}

AI_PERSONALITIES = {
    "Defensive": {"shot_aggr": 0.88, "risk_guard": 1.20, "death_yorker": 1.25},
    "Balanced":  {"shot_aggr": 1.00, "risk_guard": 1.00, "death_yorker": 1.00},
    "Aggressive":{"shot_aggr": 1.14, "risk_guard": 0.84, "death_yorker": 0.88},
}

DELIVERY_IMPACT = {
    "IN":       {"wicket": 0.08,  "run": -0.05, "boundary": -0.02},
    "OUT":      {"wicket": -0.03, "run": 0.06,  "boundary": 0.05},
    "YORKER":   {"wicket": 0.10,  "run": -0.12, "boundary": -0.08},
    "BOUNCER":  {"wicket": 0.03,  "run": -0.02, "boundary": 0.04},
    "OFF_SPIN": {"wicket": 0.03,  "run": -0.03, "boundary": -0.01},
    "LEG_SPIN": {"wicket": 0.04,  "run": 0.00,  "boundary": 0.03},
    "FLIPPER":  {"wicket": 0.09,  "run": -0.08, "boundary": -0.05},
    "GOOGLY":   {"wicket": 0.07,  "run": -0.04, "boundary": -0.02},
}

FIELD_ZONES = {
    "1": "Deep Third",
    "2": "Point",
    "3": "Extra Cover",
    "4": "Square Leg",
    "5": "Straight",
    "6": "Midwicket",
    "7": "Fine Leg",
    "8": "Long On",
    "9": "Long Off",
}

BOWLING_PLANS = {
    "1": {"name": "Normal", "hint": "Back of a good length"},
    "2": {"name": "Short",  "hint": "Chest-high pressure ball"},
    "3": {"name": "Full",   "hint": "Drive-inviting fuller ball"},
    "4": {"name": "Yorker", "hint": "Toe-crushing yorker lane"},
    "5": {"name": "Wide",   "hint": "Outside-off tight line"},
}

BOWL_ROWS = ["YORKER", "FULL", "GOOD", "SHORT"]
BOWL_COLS = ["WIDE", "STUMP", "BODY"]

ZONE_PROFILE = {
    "1": "off",
    "2": "off",
    "3": "off",
    "4": "leg",
    "5": "straight",
    "6": "leg",
    "7": "leg",
    "8": "straight",
    "9": "straight",
}

SHOT_ZONE_COMPAT = {
    "DEFEND": {"off": 1.0, "straight": 1.0, "leg": 0.9},
    "SWING":  {"off": 1.0, "straight": 1.0, "leg": 1.0},
    "LOFT":   {"off": 1.0, "straight": 1.1, "leg": 1.1},
    "LEAVE":  {"off": 1.0, "straight": 1.0, "leg": 1.0},
}

RADAR_LINKS = {
    "1": ("3", "2"),
    "2": ("3", "1"),
    "3": ("2", "1"),
    "4": ("7", "5"),
    "5": ("7", "4"),
    "6": ("8", "1"),
    "7": ("8", "4"),
    "8": ("7", "6"),
    "9": ("3", "4"),
}

def draw_divider(char="─"):
    center_line(ctext(char * min(term_width() - 2, 112), THEME_TEXT, Style.DIM))

def aim_from_input(first_key, second_key=None):
    if first_key == "UP":
        return "5"
    if first_key == "LEFT":
        return "4"
    if first_key == "RIGHT":
        return "2"
    if first_key == "DOWN":
        return "9"

    fk = (first_key or "").upper()
    sk = (second_key or "").upper()

    if fk == "W" and sk == "D":
        return "3"
    if fk == "W" and sk == "A":
        return "7"
    if fk == "S" and sk == "D":
        return "1"
    if fk == "S" and sk == "A":
        return "6"

    if fk == "W":
        return "5"
    if fk == "A":
        return "4"
    if fk == "D":
        return "2"
    if fk == "S":
        return "9"

    if fk in FIELD_ZONES:
        return fk
    return None

def zone_gap_state(field_setup, zone):
    if not field_setup:
        return True
    f = field_setup.get(zone, "ring")
    return f == "deep"

def move_pitch_cursor(cursor, key):
    r, c = cursor
    if key == "UP":
        r = max(0, r - 1)
    elif key == "DOWN":
        r = min(3, r + 1)
    elif key == "LEFT":
        c = max(0, c - 1)
    elif key == "RIGHT":
        c = min(2, c + 1)
    return (r, c)

def cursor_to_plan(cursor):
    r, c = cursor
    if c == 0:
        return "5"  # wide line intent
    if r == 0:
        return "4"
    if r == 1:
        return "3"
    if r == 2:
        return "1"
    return "2"

def delivery_from_type_and_bowler(bowler_type, type_key):
    if bowler_type == "spin":
        if type_key == "1":
            return "OFF_SPIN"
        if type_key == "2":
            return "GOOGLY"
        if type_key == "3":
            return random.choice(["OFF_SPIN", "LEG_SPIN"])
        return "FLIPPER"

    # pace / medium
    if type_key == "1":
        return random.choice(["IN", "OUT"])
    if type_key == "2":
        return "BOUNCER"
    if type_key == "3":
        return random.choice(["OUT", "IN"])
    return "YORKER"

# =========================
# COMMENTARY
# =========================

COMMENTARY = {
    0:   ["Dot ball. Nothing doing.",
          "Well bowled — beaten outside off!",
          "Defended solidly back to the bowler.",
          "Plays and misses! Lucky there.",
          "Tight line, no run offered."],
    1:   ["Nudged to mid-on, easy single.",
          "Pushed to covers, comes back for one.",
          "Dabbed fine for a single.",
          "Tucks it to leg, rotates the strike."],
    2:   ["Driven through the gap — two runs!",
          "Good running between the wickets, two!",
          "Punched through mid-off, they race back for two.",
          "Flicked off the hips — two more!"],
    4:   ["FOUR! Cracking drive through covers!",
          "FOUR! Slapped through mid-wicket!",
          "FOUR! Edged but flies to the boundary!",
          "FOUR! Swept hard — races away!",
          "FOUR! Full toss punished to the fence!"],
    6:   ["SIX! Right out of the ground!",
          "SIX! Massive hit over long-on!",
          "SIX! Slog sweep into the crowd!",
          "SIX! Launched effortlessly over extra cover!"],
    "W": ["OUT! Caught behind — walks off!",
          "OUT! Timber! Bowled him — stumps shattered!",
          "OUT! Plumb in front — LBW!",
          "OUT! Holed out to long-on — poor shot!",
          "OUT! Edge and taken at slip!"],
    "WD":["Wide! Down the leg side.",
          "Wide! Too far outside off."],
    "NB":["No Ball! Front foot over the line — FREE HIT!",
          "No ball — FREE HIT coming up!"],
}

TIPS = [
    "Timing is everything! Use [→] Swing for power and [←] Defend for survival.",
    "Pace bowlers thrive on Green Top pitches.",
    "Spinners love a Dusty track — dangerous in the death overs.",
    "A maiden over builds pressure. Bowl tight lines!",
    "Use DRS wisely — you only get one review per innings.",
    "Overcast conditions? Swing bowlers will be lethal.",
    "The longer a batter stays in, the harder they are to dismiss!",
    "Partnership building is key. Don't throw wickets away early.",
]

DATA_FILE = "records.json"


def default_game_data():
    return {
        "history": [],
        "stats": {
            "matches": 0,
            "ties": 0,
            "user_wins": 0,
            "user_losses": 0,
            "total_runs": 0,
            "total_wickets": 0,
            "highest_match_total": 0,
        }
    }


def load_game_data():
    if not os.path.exists(DATA_FILE):
        return default_game_data()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        base = default_game_data()
        base["history"] = data.get("history", [])[-100:]
        base_stats = base["stats"]
        in_stats = data.get("stats", {})
        for k in base_stats:
            if isinstance(in_stats, dict):
                base_stats[k] = in_stats.get(k, base_stats[k])
        return base
    except (OSError, ValueError, TypeError):
        return default_game_data()


def save_game_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except OSError:
        pass


def get_ai_field_setup(personality, balls, total_balls, wickets, target, score):
    base = {
        "1": "ring", "2": "ring", "3": "ring",
        "4": "ring", "5": "ring", "6": "ring",
        "7": "deep", "8": "deep", "9": "deep",
    }

    progress = balls / total_balls if total_balls else 0
    death_phase = progress >= 0.8
    pers = AI_PERSONALITIES.get(personality, AI_PERSONALITIES["Balanced"])

    if personality == "Defensive":
        for z in ["1", "6", "7", "8", "9"]:
            base[z] = "deep"
    elif personality == "Aggressive":
        for z in ["2", "3", "4", "5", "6"]:
            base[z] = "ring"
        base["8"] = "ring"
        base["9"] = "ring"

    if death_phase:
        for z in ["1", "6", "7", "8", "9"]:
            base[z] = "deep"

    if target is not None:
        balls_left = max(1, total_balls - balls)
        runs_left = max(0, target - score)
        req_rr = (runs_left / balls_left) * 6
        if req_rr > 10:
            # attacking chase: spread boundary riders
            for z in ["1", "6", "7", "8", "9"]:
                base[z] = "deep"
        elif req_rr < 6 and wickets >= 6:
            # squeeze singles
            for z in ["2", "3", "4", "5", "6"]:
                base[z] = "ring"

    # Personality fine-tune: higher risk_guard means defend boundaries more.
    if pers["risk_guard"] > 1.1:
        base["1"] = "deep"
        base["6"] = "deep"

    return base


def draw_field_map(field_setup, selected_zone=None):
    def zid(z):
        return f"*{z}*" if selected_zone == z else f"[{z}]"

    lines = [
    "",
    "                  ◯  CRICKET FIELD  ◯",
    "",
    "             OFF-SIDE      |      LEG-SIDE",
    "        ___________________|___________________",
    "       /           ( BOUNDARY LINE )           \\",
    f"      /     {zid('1')}                         {zid('6')}     \\",
    f"     /    Deep Off          {zid('5')}        Deep Leg  \\",
    "    |                    Straight                 |",
    "    |          .-------- 30-YD --------.          |",
    "    |         /                         \\         |",
    f"    |   {zid('2')}  |           [ P ]           |  {zid('4')}   |",
    f"    |  Cover |           PITCH           |  Mid-W |",
    "    |         \\                         /         |",
    f"    |          '---------{zid('8')}---------'          |",
    "    |                    Long-On                  |",
    f"     \\      {zid('3')}                         {zid('7')}      /",
    f"      \\    Mid-Off         {zid('9')}        Mid-On  /",
    "       \\_________________Straight______________/ ",
    "",
    "   KEY: *n* = selected zone, [n] = zone id",
    "",
]
    for ln in lines:
        print(ln)


def poll_key_nonblocking():
    if os.name == 'nt':
        import msvcrt
        if not msvcrt.kbhit():
            return None
        key = msvcrt.getch()
        if key == b'\xe0':
            k2 = msvcrt.getch()
            if k2 == b'K':
                return "LEFT"
            if k2 == b'M':
                return "RIGHT"
            if k2 == b'H':
                return "UP"
            if k2 == b'P':
                return "DOWN"
            return None
        if key == b'\r':
            return "ENTER"
        if key == b'\x1b':
            return "ESC"
        if key == b' ':
            return "SPACE"
        try:
            return key.decode().upper()
        except Exception:
            return None

    import select
    if select.select([sys.stdin], [], [], 0)[0]:
        ch = sys.stdin.read(1)
        if ch in ('\r', '\n'):
            return "ENTER"
        if ch == ' ':
            return "SPACE"
        return ch.upper()
    return None


def grade_timing(delta):
    ad = abs(delta)
    if ad <= 0.045:
        return "PERFECT"
    if ad <= 0.10:
        return "GOOD"
    if ad <= 0.20:
        return "LATE" if delta > 0 else "EARLY"
    return "MISS"


def run_timing_challenge(delivery, batter_skill, difficulty, bowler_pace_skill=75):
    # Faster balls tighten timing windows; better batters get slight assistance.
    speed_factor = {
        "YORKER": 1.20,
        "IN": 1.10,
        "OUT": 1.05,
        "BOUNCER": 1.12,
        "OFF_SPIN": 0.92,
        "LEG_SPIN": 0.95,
        "FLIPPER": 1.00,
        "GOOGLY": 0.96,
    }.get(delivery, 1.0)

    strictness = {
        "Easy": 0.86,
        "Normal": 1.00,
        "Hard": 1.18,
    }.get(difficulty, 1.0)

    perfect_th = 0.045 / strictness
    good_th = 0.10 / strictness
    late_th = 0.20 / strictness

    pace_factor = 1.0 + max(-0.15, min(0.20, (bowler_pace_skill - 75) * 0.004))
    travel_time = max(0.75, (1.25 / speed_factor) / pace_factor)
    ideal_t = travel_time * random.uniform(0.62, 0.75)
    assist = max(-0.02, min(0.02, (batter_skill - 75) * 0.0005))

    start = time.time()
    hit_time = None

    # Calculate ideal zone positions on a 50-char bar
    bar_length = 50
    perfect_start_idx = max(0, int((ideal_t - perfect_th) / travel_time * (bar_length - 1)))
    perfect_end_idx = min(bar_length - 1, int((ideal_t + perfect_th) / travel_time * (bar_length - 1)))
    good_start_idx = max(0, int((ideal_t - good_th) / travel_time * (bar_length - 1)))
    good_end_idx = min(bar_length - 1, int((ideal_t + good_th) / travel_time * (bar_length - 1)))

    # Print timing gauge header
    print("\n")
    print("  ╔════════════════════════════════════════════════════╗")
    print("  ║        TIMING GAUGE - PRESS SPACE TO HIT           ║")
    print("  ║─────────────────────────────────────────────────────║")

    while True:
        now = time.time()
        t = now - start
        if t >= travel_time:
            break

        prog = min(1.0, t / travel_time)
        pos = min(bar_length - 1, int(prog * (bar_length - 1)))

        # Build bar: show target zones and moving indicator
        bar = []
        for i in range(bar_length):
            if i == pos:
                bar.append("◆")  # Moving indicator
            elif perfect_start_idx <= i <= perfect_end_idx:
                bar.append("█")  # Perfect zone
            elif good_start_idx <= i <= good_end_idx:
                bar.append("▓")  # Good zone
            else:
                bar.append("░")  # Miss zone

        bar_str = "".join(bar)
        pct = int(prog * 100)
        print(f"  ║ {bar_str}  {pct:>3}% ║\r", end="", flush=True)

        k = poll_key_nonblocking()
        if k in ("SPACE", "ENTER", "H"):
            hit_time = t
            break
        if k == "ESC":
            print("\n  Paused. Press [ENTER] to resume...")
            while get_key() != "ENTER":
                pass

        time.sleep(0.01)
    
    print("\n  ╚════════════════════════════════════════════════════╝\n")

    if hit_time is None:
        return "MISS", 1.0

    delta = (hit_time - ideal_t) - assist
    ad = abs(delta)
    if ad <= perfect_th:
        grade = "PERFECT"
    elif ad <= good_th:
        grade = "GOOD"
    elif ad <= late_th:
        grade = "LATE" if delta > 0 else "EARLY"
    else:
        grade = "MISS"
    quality = max(0.0, 1.0 - abs(delta) / max(ideal_t, 0.01))
    return grade, quality


def run_release_meter(bowler_skill, difficulty):
    speed = max(0.006, 0.016 - (bowler_skill / 1000.0))
    strict = {"Easy": 1.2, "Normal": 1.0, "Hard": 0.85}.get(difficulty, 1.0)
    bar_len = 20
    sweet_start = int(0.78 * bar_len)
    sweet_end = int(0.90 * bar_len)
    sweet_mid = (sweet_start + sweet_end) // 2

    start = time.time()
    locked_pos = None

    center_line(ctext("RELEASE: Press [SPACE] again to lock", THEME_TEXT, Style.BRIGHT))
    while True:
        elapsed = time.time() - start
        pos = min(bar_len - 1, int((elapsed / (1.2 / strict)) * (bar_len - 1)))
        chars = []
        for i in range(bar_len):
            if i == pos:
                chars.append("▌")
            elif sweet_start <= i <= sweet_end:
                chars.append("█")
            else:
                chars.append("░")
        center_line(ctext(f"[{''.join(chars)}]", THEME_TEXT, Style.BRIGHT))

        k = poll_key_nonblocking()
        if k == "SPACE":
            locked_pos = pos
            break
        if pos >= bar_len - 1:
            break
        time.sleep(speed)

    if locked_pos is None:
        return "MISS", 0.0, (1, 1)

    delta = locked_pos - sweet_mid
    ad = abs(delta)
    if ad <= 1:
        grade = "PERFECT"
    elif ad <= 3:
        grade = "GOOD"
    else:
        grade = "EARLY" if delta < 0 else "LATE"

    quality = max(0.0, 1.0 - (ad / max(1, bar_len - 1)))
    # early => tends shorter/wider, late => fuller/body-side
    if grade == "PERFECT":
        # Short visual feedback flash for a perfect lock-in.
        for _ in range(2):
            center_line(ctext("RELEASE LOCKED: PERFECT", Fore.GREEN, Style.BRIGHT))
            time.sleep(0.12)
        drift = (0, 0)
    elif grade == "GOOD":
        drift = (random.choice([0, 0, 1, -1]), random.choice([0, 0, 1, -1]))
    elif grade == "EARLY":
        drift = (1, -1)
    else:
        drift = (-1, 1)
    return grade, quality, drift


def apply_timing_and_zone(result, shot, timing_grade, timing_quality,
                          zone, field_setup, batter, delivery,
                          balls, total_balls):
    # Leave is mostly a non-contact option.
    if shot == "LEAVE":
        return result

    zone_kind = ZONE_PROFILE.get(zone, "straight")
    compat = SHOT_ZONE_COMPAT.get(shot, {}).get(zone_kind, 1.0)
    field_type = field_setup.get(zone, "ring")
    bat_skill = get_stat(batter, "bat_skill", 50)
    death_phase = (balls / total_balls) >= 0.8 if total_balls else False

    # Hard miss can still survive, but wicket chance is high.
    if timing_grade == "MISS":
        if random.random() < 0.38 + (0.08 if delivery in ("YORKER", "FLIPPER") else 0):
            return "W"
        return 0

    # Timing layers; tune boundaries and wicket risk.
    if timing_grade == "PERFECT":
        if result == "W" and random.random() < 0.55:
            result = 1
        elif isinstance(result, int):
            if result <= 1 and random.random() < 0.55 * compat:
                result = 2
            if result == 2 and random.random() < 0.45 * compat:
                result = 4
            if result == 4 and random.random() < 0.30 * compat:
                result = 6

            # Extra reward for cleanly timed lofted shots.
            if shot == "LOFT":
                if result <= 2 and random.random() < 0.60 * compat:
                    result = 4
                if result == 4 and random.random() < 0.42 * compat:
                    result = 6
    elif timing_grade == "GOOD":
        if result == "W" and random.random() < 0.28:
            result = 0
        elif isinstance(result, int) and result == 0 and random.random() < 0.45 * compat:
            result = 1
    else:  # EARLY / LATE
        if isinstance(result, int):
            if result >= 4 and random.random() < 0.65:
                result = 2
            elif result == 2 and random.random() < 0.50:
                result = 1
        if random.random() < 0.12 and timing_quality < 0.35:
            result = "W"

    # Field placement effects.
    if isinstance(result, int) and result >= 4:
        deep_cut = 0.55 + (0.18 if death_phase else 0.0)
        if field_type == "deep" and random.random() < deep_cut:
            result = 2 if result == 4 else 4
        # In death overs, miscued lofts to deep field can bring wickets.
        if death_phase and field_type == "deep" and shot == "LOFT" and timing_grade in ("EARLY", "LATE"):
            if random.random() < 0.20:
                return "W"
    elif isinstance(result, int) and result in (1, 2):
        if field_type == "ring" and random.random() < 0.35:
            result = 0
        elif field_type == "deep" and random.random() < 0.35 and bat_skill > 70:
            result = min(2, result + 1)

    return result

# Dismissal types grouped by whether DRS is allowed and who gets the wicket credit
# DRS_ELIGIBLE: only LBW and caught-behind (edge) can be reviewed by batting team
DISMISSAL_DRS = [
    ("lbw b. {bowler}",           "bowler",  True),   # LBW — DRS allowed
    ("c. {wk} b. {bowler}",       "bowler",  True),   # caught behind/edge — DRS allowed
]
DISMISSAL_NO_DRS = [
    ("b. {bowler}",               "bowler",  False),  # bowled — umpire's call, no DRS
    ("c. {fielder} b. {bowler}",  "bowler",  False),  # caught in field — no DRS
    ("c. {fielder} b. {bowler}",  "bowler",  False),  # caught in field — no DRS
    ("st. {wk} b. {bowler}",      "bowler",  False),  # stumped — no DRS
    ("run out ({fielder})",       "fielder", False),  # run out — no bowler credit, no DRS
]

def pick_dismissal(delivery):
    """
    Pick a dismissal type appropriate to the delivery.
    Returns (dis_template, credit, drs_eligible).
    credit = 'bowler' or 'fielder'.
    """
    # Deliveries that favour edge/LBW chances
    if delivery in ("OUT", "IN", "LEG_SPIN", "OFF_SPIN"):
        # Higher chance of LBW or edge
        pool = DISMISSAL_DRS + DISMISSAL_NO_DRS[:3]
    elif delivery in ("BOUNCER",):
        # Short ball — mostly caught in the deep, no edge/LBW
        pool = [DISMISSAL_NO_DRS[1], DISMISSAL_NO_DRS[2]]
    elif delivery in ("YORKER", "FLIPPER"):
        # Yorker/flipper — mostly bowled
        pool = [("b. {bowler}", "bowler", False)] * 3 + DISMISSAL_DRS[:1]
    else:
        pool = DISMISSAL_DRS + DISMISSAL_NO_DRS
    return random.choice(pool)

# Delivery bias → [DEFEND, SWING, LOFT, LEAVE] for computer batter
PACE_SHOT_BIAS = {
    "IN":      [55, 20,  5, 20],   # cramps batter on the pads
    "OUT":     [15, 50, 20, 15],   # full, invites the drive
    "YORKER":  [40, 30,  5, 25],   # hard to score, lots of dots
    "BOUNCER": [10, 20, 55, 15],   # short ball, tempts the pull
}
SPIN_SHOT_BIAS = {
    "OFF_SPIN": [45, 25, 15, 15],  # turns in, batter defends or drives
    "LEG_SPIN": [30, 35, 20, 15],  # more temptation to drive
    "FLIPPER":  [50, 20, 10, 20],  # skids through, hard to score
    "GOOGLY":   [25, 20, 20, 35],  # mystery ball, batter often leaves
}

def get_shot_bias(delivery):
    if delivery in PACE_SHOT_BIAS:
        return PACE_SHOT_BIAS[delivery]
    return SPIN_SHOT_BIAS.get(delivery, [40, 25, 15, 20])


def choose_ai_shot(delivery, target, score, balls, total_balls, wickets, difficulty, personality):
    base = list(get_shot_bias(delivery))
    sett = DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS["Normal"])
    pers = AI_PERSONALITIES.get(personality, AI_PERSONALITIES["Balanced"])

    if target is not None:
        balls_left = max(1, total_balls - balls)
        req_rr = (max(0, target - score) / balls_left) * 6
        if req_rr > 11:
            base[2] += 18
            base[1] += 8
            base[0] = max(5, base[0] - 10)
            base[3] = max(2, base[3] - 8)
        elif req_rr < 6:
            base[0] += 10
            base[3] += 6
            base[2] = max(8, base[2] - 8)

    if wickets >= 7:
        base[0] += 14
        base[3] += 8
        base[2] = max(6, base[2] - 10)

    if pers["risk_guard"] > 1.0:
        base[0] += int(6 * (pers["risk_guard"] - 1.0))
        base[3] += int(5 * (pers["risk_guard"] - 1.0))
        base[2] = max(4, base[2] - int(8 * (pers["risk_guard"] - 1.0)))

    aggr = sett["ai_aggr"] * pers["shot_aggr"]
    base[1] = max(1, int(base[1] * aggr))
    base[2] = max(1, int(base[2] * aggr))

    return random.choices(["DEFEND", "SWING", "LOFT", "LEAVE"], base)[0]


def choose_ai_delivery(bowler_type, balls, total_balls, target, score, personality):
    progress = balls / total_balls if total_balls else 0
    death_phase = progress >= 0.8
    pers = AI_PERSONALITIES.get(personality, AI_PERSONALITIES["Balanced"])

    if bowler_type == "spin":
        if death_phase:
            return random.choices(
                ["OFF_SPIN", "LEG_SPIN", "FLIPPER", "GOOGLY"],
                [20, 20, 40, 20]
            )[0]
        return random.choices(
            ["OFF_SPIN", "LEG_SPIN", "FLIPPER", "GOOGLY"],
            [30, 30, 20, 20]
        )[0]

    yorker_boost = pers["death_yorker"]
    if target is not None and (target - score) <= 25 and death_phase:
        return random.choices(["IN", "OUT", "YORKER", "BOUNCER"],
                              [15, 15, int(55 * yorker_boost), 15])[0]
    if death_phase:
        return random.choices(["IN", "OUT", "YORKER", "BOUNCER"],
                              [20, 15, int(45 * yorker_boost), 20])[0]
    return random.choices(["IN", "OUT", "YORKER", "BOUNCER"], [30, 30, 20, 20])[0]


def choose_ai_bowling_plan(balls, total_balls, target, score):
    progress = balls / total_balls if total_balls else 0.0
    death_phase = progress >= 0.8

    if death_phase:
        weights = [18, 15, 15, 40, 12]  # normal, short, full, yorker, wide
    else:
        weights = [38, 18, 24, 10, 10]

    if target is not None:
        balls_left = max(1, total_balls - balls)
        runs_left = max(0, target - score)
        req_rr = (runs_left * 6) / balls_left
        if req_rr > 10:
            # defend boundary more
            weights = [20, 22, 14, 26, 18]
        elif req_rr < 7:
            # hunt wickets with fuller/yorker
            weights = [24, 14, 28, 24, 10]

    return random.choices(["1", "2", "3", "4", "5"], weights)[0]


def tactical_insight(score, wickets, balls, total_balls, target, partnership_runs, over_log):
    progress = balls / total_balls if total_balls else 0
    if progress <= 0.33:
        phase = "Powerplay"
    elif progress <= 0.8:
        phase = "Middle Overs"
    else:
        phase = "Death Overs"

    over_runs = 0
    for s in over_log:
        if s.isdigit():
            over_runs += int(s)
        elif s in ("wd", "nb"):
            over_runs += 1

    momentum = "Steady"
    if over_runs >= 10:
        momentum = "Batting Surge"
    elif over_runs <= 2 and len(over_log) >= 4:
        momentum = "Bowling Pressure"

    def win_prob_first_innings(crr, wkts, prog):
        # Rough first-innings projection confidence (not match result probability).
        base = 45 + (crr - 7.0) * 7 - wkts * 2.4 + prog * 12
        return max(5, min(95, int(round(base))))

    def win_prob_chase(req_rr, crr_now, wkts, balls_left, runs_left):
        if balls_left <= 0:
            return 100 if runs_left <= 0 else 0
        gap = req_rr - crr_now
        resource = (10 - wkts) * 4 + (balls_left / 6) * 2
        base = 58 - gap * 9 + resource * 0.9
        return max(1, min(99, int(round(base))))

    if target is None:
        crr = (score * 6 / balls) if balls else 0.0
        proj = int(round(crr * (total_balls / 6))) if balls else 0
        wp = win_prob_first_innings(crr, wickets, progress)
        line2 = f"Phase: {phase} | Momentum: {momentum} | Projected Total: {proj} | Win%: {wp}"
    else:
        balls_left = max(0, total_balls - balls)
        runs_left = max(0, target - score)
        req_rr = (runs_left * 6 / balls_left) if balls_left else 0.0
        pressure = "Low" if req_rr <= 7 else ("Medium" if req_rr <= 10 else "High")
        crr_now = (score * 6 / balls) if balls else 0.0
        wp = win_prob_chase(req_rr, crr_now, wickets, balls_left, runs_left)
        line2 = f"Phase: {phase} | Pressure: {pressure} | Need {runs_left} off {balls_left} | Win%: {wp}"

    line1 = f"Tactical: Wkts {wickets}/10 | Partnership {partnership_runs} | Last over runs {over_runs}"
    return [line1, line2]

# ── REBALANCED BASE WEIGHTS — lower wicket base rates ─────────────────────
SHOT_OUTCOMES = {
    "DEFEND": ([0, 1, "W"],        [65, 32,  3]),
    "SWING":  ([0, 1, 2, 4, "W"], [22, 28, 24, 20,  6]),
    "LOFT":   ([0, 4, 6, "W"],    [18, 38, 32, 12]),
    "LEAVE":  ([0, "W"],           [92,  8]),
}

# =========================
# UTILITIES
# =========================

def clear():
    os.system("cls" if os.name == 'nt' else 'clear')

def animate(text, delay=0.022):
    for c in text:
        print(c, end='', flush=True)
        time.sleep(delay)
    print()

def pause(sec=1.0):
    time.sleep(sec)


def pause_game():
    print("\n  === GAME PAUSED ===")
    print("  Press [ENTER] to resume...")
    while get_key() != "ENTER":
        pass


def choose_target_zone(field_setup):
    selected = "5"
    while True:
        print_header("BATTING TARGET")
        draw_modern_field(selected_zone=selected)
        k = get_key()
        if k in ("LEFT", "RIGHT", "UP", "DOWN"):
            selected = move_zone(selected, k)
            continue
        if k in FIELD_ZONES:
            selected = k
            continue
        if k == "ENTER":
            return selected
        if k == "ESC":
            pause_game()


def choose_bowling_zone():
    selected = "1"
    while True:
        print_header("BOWLING PLAN")
        opts = []
        for key, info in BOWLING_PLANS.items():
            pref = "[[" if key == selected else "  "
            suff = "]]" if key == selected else "  "
            opts.append(ctext(f"{pref} {key} {suff} {info['name']:<7} - {info['hint']}", THEME_ACCENT if key == selected else THEME_TEXT, Style.BRIGHT if key == selected else Style.DIM))
        draw_center_box(opts, width=min(96, term_width() - 6), title="CHOOSE LENGTH")
        k = get_key()
        if k in ("UP", "W"):
            selected = str(max(1, int(selected) - 1))
            continue
        if k in ("DOWN", "S"):
            selected = str(min(5, int(selected) + 1))
            continue
        if k in BOWLING_PLANS:
            selected = k
            continue
        if k == "ENTER":
            return selected
        if k == "ESC":
            pause_game()


def timing_feedback(grade, quality):
    if grade == "PERFECT":
        return "PERFECT", "Elite contact"
    if grade == "GOOD":
        return "GOOD", "Solid timing"
    if grade in ("EARLY", "LATE"):
        if quality >= 0.45:
            return "AVERAGE", "Slight mistime"
        return "BAD", "Poor contact"
    return "MISS", "No clean contact"


def apply_bowling_zone_effect(result, delivery, zone, balls, total_balls):
    if not isinstance(result, (int, str)):
        return result
    plan = zone if zone in BOWLING_PLANS else "1"
    death_phase = (balls / total_balls) >= 0.8 if total_balls else False

    # 1 Normal: balanced discipline
    if plan == "1":
        if isinstance(result, int) and result in (1, 2) and random.random() < 0.15:
            result = 0

    # 2 Short: extra wicket chance, but pulls can score
    elif plan == "2":
        if result != "W" and random.random() < 0.08:
            result = "W"
        elif isinstance(result, int) and result == 0 and random.random() < 0.18:
            result = 1

    # 3 Full: can induce drives and edges
    elif plan == "3":
        if result != "W" and random.random() < 0.07:
            result = "W"
        elif isinstance(result, int) and result == 2 and random.random() < 0.22:
            result = 4

    # 4 Yorker: strongest in death, suppresses runs
    elif plan == "4":
        if result != "W" and random.random() < (0.12 if death_phase else 0.08):
            result = "W"
        elif isinstance(result, int) and result >= 2 and random.random() < 0.45:
            result = 1

    # 5 Wide line: cuts boundaries, higher single/dot pattern
    else:
        if isinstance(result, int) and result >= 4 and random.random() < 0.42:
            result = 2
        elif isinstance(result, int) and result == 1 and random.random() < 0.25:
            result = 0

    return result

def safe_input(prompt, default=""):
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        return default

def draw_box(lines, width=76):
    draw_center_box(lines, width=width)

# =========================
# KEY READER
# =========================

def get_key():
    if os.name == 'nt':
        import msvcrt
        while True:
            key = msvcrt.getch()
            if key == b'\xe0':
                k2 = msvcrt.getch()
                if k2 == b'K': return "LEFT"
                if k2 == b'M': return "RIGHT"
                if k2 == b'H': return "UP"
                if k2 == b'P': return "DOWN"
            elif key == b'\r': return "ENTER"
            elif key == b'\x1b': return "ESC"
            elif key == b' ': return "SPACE"
            else:
                try: return key.decode().upper()
                except: pass
    else:
        import tty, termios
        fd  = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    if ch3 == 'A': return "UP"
                    if ch3 == 'B': return "DOWN"
                    if ch3 == 'C': return "RIGHT"
                    if ch3 == 'D': return "LEFT"
                return "ESC"
            elif ch in ('\r', '\n'): return "ENTER"
            elif ch == ' ': return "SPACE"
            return ch.upper()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

# =========================
# MAIN MENU
# =========================

def main_menu(settings_preview="5 OVERS | NORMAL | BALANCED"):
    idx = 0
    while True:
        draw_main_menu_screen(idx, settings_preview=settings_preview)
        k = get_key()
        if k in ("UP", "W"):
            idx = (idx - 1) % 4
        elif k in ("DOWN", "S"):
            idx = (idx + 1) % 4
        elif k == "ENTER":
            if idx == 0:
                return "play"
            if idx == 1:
                return "records"
            if idx == 2:
                return "settings"
            print(success_text("\nGG! Thanks for playing.\n"))
            sys.exit(0)
        elif k == "ESC":
            print(success_text("\nGG! Thanks for playing.\n"))
            sys.exit(0)

# =========================
# RECORDS
# =========================

def show_records(history, stats):
    print_header("RECORDS")
    center_line(ctext("-- CAREER LOGBOOK --", THEME_ACCENT, Style.BRIGHT))
    print()
    if history:
        center_line(ctext("RECENT MATCHES", THEME_ACCENT, Style.BRIGHT))
        for i, rec in enumerate(history[-10:], 1):
            center_line(ctext(f"{i:>2}. {rec}", THEME_TEXT))
    else:
        center_line(ctext("No match records yet. Play a game first!", Fore.RED, Style.BRIGHT))

    print()
    center_line(ctext("CAREER SNAPSHOT", THEME_ACCENT, Style.BRIGHT))
    center_line(ctext(f"Matches {stats.get('matches', 0)} | Wins {stats.get('user_wins', 0)} | Losses {stats.get('user_losses', 0)} | Ties {stats.get('ties', 0)}", THEME_TEXT))
    center_line(ctext(f"Total Runs {stats.get('total_runs', 0)} | Total Wickets {stats.get('total_wickets', 0)} | Highest Match Total {stats.get('highest_match_total', 0)}", THEME_TEXT))
    print()
    center_line(ctext("[TRIKET // v2.6]  [ENTER] BACK", THEME_ACCENT, Style.BRIGHT))
    safe_input("", "")


def choose_match_settings():
    while True:
        try:
            print_header("MATCH SETTINGS")
            center_line(ctext("Type total overs for the innings (1 to 50)", THEME_ACCENT, Style.BRIGHT))
            center_line(ctext("Recommended: 5, 10, 20", THEME_TEXT, Style.DIM))
            print()
            overs = int(safe_input(ctext("  >> OVERS: ", THEME_ACCENT, Style.BRIGHT), "5"))
            if 1 <= overs <= 50:
                break
            center_line(error_text("Choose a value from 1 to 50."))
            pause(1.0)
        except ValueError:
            center_line(error_text("Invalid input. Type a number."))
            pause(1.0)

    d_idx = arrow_menu(
        "DIFFICULTY",
        [
            "Easy   - More forgiving batting outcomes",
            "Normal - Balanced simulation",
            "Hard   - Tougher AI and tighter outcomes",
        ],
    )
    difficulty = ["Easy", "Normal", "Hard"][d_idx]

    p_idx = arrow_menu(
        "AI PERSONALITY",
        [
            "Defensive - Protects wickets, calmer chasing",
            "Balanced  - Mixed tactics",
            "Aggressive - Boundary hunting, higher risk",
        ],
    )
    personality = ["Defensive", "Balanced", "Aggressive"][p_idx]

    return overs, difficulty, personality

# =========================
# TEAM SELECTION
# =========================

def choose_team():
    teams = list(TEAMS.keys())
    idx = 0
    while True:
        draw_team_select_screen(idx, teams)
        k = get_key()
        if k in ("UP", "W"):
            idx = (idx - 1) % len(teams)
        elif k in ("DOWN", "S"):
            idx = (idx + 1) % len(teams)
        elif k == "ENTER":
            break
        elif k == "ESC":
            return None, None

    player = teams[idx]
    computer = random.choice([t for t in teams if t != player])
    print_header("MATCHUP")
    draw_center_box([
        ctext(f"  Your team  : {player}", Fore.GREEN, Style.BRIGHT),
        ctext(f"  Opponent   : {computer}", Fore.YELLOW, Style.BRIGHT),
    ], title="TEAMS")
    pause(1.5)
    return player, computer

# =========================
# CONDITIONS
# =========================

def setup_conditions():
    pitch   = random.choice(list(PITCH_TYPES.keys()))
    weather = random.choice(list(WEATHER_CONDITIONS.keys()))
    desc = {
        "Flat": "Great for batting.",
        "Green Top": "Pace bowlers will dominate!",
        "Dusty": "Spinners in paradise!",
        "Slow": "Hard to time the ball.",
        "Sunny": "Clear skies.",
        "Overcast": "Swing bowlers will be dangerous!",
        "Humid": "Some extra movement expected.",
        "Windy": "Gusty conditions at the ground.",
    }
    print_header("MATCH CONDITIONS")
    spin_tag = int(round(PITCH_TYPES.get(pitch, {}).get("spin_mod", 0) * 20))
    swing_tag = int(round(WEATHER_CONDITIONS.get(weather, {}).get("swing_mod", 0) * 10))
    center_line(ctext("-- PRE-MATCH REPORT --", THEME_ACCENT, Style.BRIGHT))
    print()
    center_line(ctext(f"PITCH   : {pitch.upper()} (SPIN {spin_tag:+d})", THEME_TEXT, Style.BRIGHT))
    center_line(ctext(desc.get(pitch, ''), THEME_TEXT, Style.DIM))
    print()
    center_line(ctext(f"WEATHER : {weather.upper()} (SWING {swing_tag:+d})", THEME_TEXT, Style.BRIGHT))
    center_line(ctext(desc.get(weather, ''), THEME_TEXT, Style.DIM))
    print()
    center_line(ctext("[TRIKET // v2.6]", THEME_ACCENT, Style.BRIGHT))
    pause(1.5)
    return pitch, weather

# =========================
# TOSS
# =========================

def toss(player, computer):
    print_header("TOSS")
    call_idx = arrow_menu("CALL THE TOSS", ["Heads", "Tails"], hint="UP/DOWN and ENTER")
    user_call = "heads" if call_idx == 0 else "tails"
    result = random.choice(["heads","tails"])
    print_header("TOSS")
    center_line(ctext("COIN FLIPS...", THEME_TEXT, Style.BRIGHT))
    center_line(ctext(f"RESULT: {result.upper()}!", THEME_ACCENT, Style.BRIGHT))
    pause(0.8)
    if user_call == result:
        pick = arrow_menu("YOU WON THE TOSS", ["Bat First", "Bowl First"], hint="Choose innings plan")
        if pick == 0:
            print_header("TOSS RESULT")
            center_line(ctext(f"{player.upper()} WILL BAT FIRST", THEME_ACCENT, Style.BRIGHT))
            safe_input("\n>> PRESS [ENTER] TO CONTINUE...", "")
            return True
        print_header("TOSS RESULT")
        center_line(ctext(f"{player.upper()} WILL BOWL FIRST", THEME_ACCENT, Style.BRIGHT))
        safe_input("\n>> PRESS [ENTER] TO CONTINUE...", "")
        return False
    else:
        comp = random.choice(["bat","bowl"])
        print_header("TOSS RESULT")
        center_line(ctext(f"{computer.upper()} WON THE TOSS AND CHOSE TO {comp.upper()}", THEME_ACCENT, Style.BRIGHT))
        safe_input("\n>> PRESS [ENTER] TO CONTINUE...", "")
        return comp != "bat"

# =========================
# BOWLER SELECTION
# =========================

def pick_bowler(bowling_team, bowler_overs, max_quota, last_bowler=None):
    lineup   = TEAMS[bowling_team]
    eligible = [p for p in lineup
                if get_stat(p,"bowl_type") != "bat"
                and bowler_overs.get(p,0) < max_quota
                and p != last_bowler]
    if not eligible:
        eligible = [p for p in lineup
                    if bowler_overs.get(p,0) < max_quota and p != last_bowler]
    if not eligible:
        eligible = [p for p in lineup if p != last_bowler]
    if not eligible:
        eligible = lineup
    skills = [get_stat(p,"bowl_skill",50) for p in eligible]
    return random.choices(eligible, skills)[0]

# =========================
# USER BOWLER SELECTION SCREEN
# =========================

def user_pick_bowler(bowling_team, bowler_overs, bowler_stats, max_quota,
                     last_bowler, over_num):
    """Show a selection screen so the user chooses who bowls the next over."""
    lineup = TEAMS[bowling_team]

    # Build candidate list respecting quota and consecutive-over rule
    candidates = []
    for p in lineup:
        btype    = get_stat(p, "bowl_type", "bat")
        ov_done  = bowler_overs.get(p, 0)
        if btype == "bat":         continue   # pure batters can't bowl
        if p == last_bowler:       continue   # can't bowl two overs in a row
        if ov_done >= max_quota:   continue   # quota reached
        candidates.append(p)

    # Safety fallbacks
    if not candidates:
        candidates = [p for p in lineup
                      if get_stat(p,"bowl_type") != "bat" and p != last_bowler]
    if not candidates:
        candidates = [p for p in lineup if p != last_bowler]
    if not candidates:
        candidates = lineup[:]

    type_icon = {"pace": "PACE", "spin": "SPIN", "medium": "MED", "bat": "BAT"}
    idx = 0
    while True:
        print_header(f"OVER {over_num} - CHOOSE BOWLER")
        rows = []
        for i, p in enumerate(candidates):
            btype = get_stat(p, "bowl_type", "bat")
            ov_done = bowler_overs.get(p, 0)
            remaining = max_quota - ov_done
            bst = bowler_stats.get(p, {"balls": 0, "runs": 0, "wickets": 0})
            ov_str = f"{bst['balls']//6}.{bst['balls']%6}"
            spell = f"{bst['runs']}-{bst['wickets']} ({ov_str})"
            marker = "▶" if i == idx else " "
            color = Fore.GREEN if i == idx else Fore.WHITE
            rows.append(ctext(
                f" {marker} {short(p):<20} {type_icon.get(btype, btype.upper()):<5}  {ov_done}/{max_quota}  left:{remaining:<2}  {spell}",
                color,
                Style.BRIGHT if i == idx else Style.NORMAL,
            ))
        rows.append("")
        rows.append(ctext("Use UP/DOWN and ENTER", Fore.MAGENTA, Style.BRIGHT))
        draw_center_box(rows, title="BOWLING ROTATION")
        k = get_key()
        if k in ("UP", "W"):
            idx = (idx - 1) % len(candidates)
        elif k in ("DOWN", "S"):
            idx = (idx + 1) % len(candidates)
        elif k == "ENTER":
            chosen = candidates[idx]
            animate(f"\n  {short(chosen)} will bowl over {over_num}.")
            pause(0.5)
            return chosen


# =========================
# OUTCOME ENGINE
# ─────────────────────────
# CONFIDENCE MECHANIC
# Every ball a batter faces builds their confidence.
#   0–5 balls  : danger zone — extra wicket risk, subdued scoring
#   6–15 balls : settling in — nervousness fading
#   16–30 balls: set batter — scoring freely, hard to dismiss
#   31+ balls  : dominant — very hard to dismiss, scoring prolifically
# =========================

def compute_outcome(shot, batter, bowler, delivery, pitch, weather,
                    bat_balls_faced, bowl_balls, difficulty,
                    batting_is_user=False):
    outcomes, base_w = SHOT_OUTCOMES[shot]
    weights = [float(w) for w in base_w]
    sett = DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS["Normal"])

    bat_skill  = get_stat(batter, "bat_skill",  50) / 100.0
    aggression = min(get_stat(batter, "aggression", 80), 108) / 100.0
    bowl_skill = get_stat(bowler,  "bowl_skill", 50) / 100.0
    # Derive bowl_type from the actual delivery chosen (pace vs spin)
    if delivery in PACE_SHOT_BIAS:
        bowl_type = "pace"
    elif delivery in SPIN_SHOT_BIAS:
        bowl_type = "spin"
    else:
        bowl_type = get_stat(bowler, "bowl_type", "medium")

    pm       = PITCH_TYPES.get(pitch, {})
    pace_mod = pm.get("pace_mod", 0)
    spin_mod = pm.get("spin_mod", 0)
    bat_mod  = pm.get("bat_mod",  0)
    swing_m  = WEATHER_CONDITIONS.get(weather, {}).get("swing_mod", 0)
    delivery_mod = DELIVERY_IMPACT.get(delivery, {"wicket": 0.0, "run": 0.0, "boundary": 0.0})

    # Softer fatigue — only kicks in after 30 balls
    stamina = get_stat(bowler, "stamina", 80) / 100.0
    fatigue = min(0.08, max(0, (bowl_balls - 30) * 0.003 / stamina)) \
              if bowl_balls > 30 else 0

    # ── CONFIDENCE MECHANIC ───────────────────────────────────────────
    if bat_balls_faced < 6:
        # New batter: nervous, wicket danger up, scoring down
        confidence_w_mod   = 1.0 + (6 - bat_balls_faced) * 0.08   # max +48%
        confidence_run_mod = max(0.65, 1.0 - (6 - bat_balls_faced) * 0.05)
    elif bat_balls_faced < 16:
        # Settling: linearly reducing wicket danger back to baseline
        confidence_w_mod   = max(0.75, 1.0 - (bat_balls_faced - 6) * 0.025)
        confidence_run_mod = 1.0
    elif bat_balls_faced < 31:
        # Set batter: noticeably harder to dismiss, scores more freely
        confidence_w_mod   = max(0.45, 0.75 - (bat_balls_faced - 16) * 0.02)
        confidence_run_mod = 1.0 + (bat_balls_faced - 16) * 0.012
    else:
        # Dominant: very hard to remove, scoring prolifically
        confidence_w_mod   = max(0.25, 0.45 - (bat_balls_faced - 31) * 0.004)
        confidence_run_mod = min(1.45, 1.22 + (bat_balls_faced - 31) * 0.005)

    # ── APPLY WEIGHTS ─────────────────────────────────────────────────
    for i, o in enumerate(outcomes):
        if o == "W":
            pitch_bonus = pace_mod if bowl_type == "pace" else spin_mod
            weights[i] *= (1 + bowl_skill * 0.25 + pitch_bonus
                           + swing_m - fatigue + delivery_mod["wicket"]) * confidence_w_mod
        elif isinstance(o, int) and o >= 4:
            weights[i] *= max(0.4,
                (aggression * bat_skill + bat_mod)
                * (1 - bowl_skill * 0.20)
                * (1 + delivery_mod["boundary"])
                * confidence_run_mod)
        elif isinstance(o, int) and o > 0:
            weights[i] *= (bat_skill * 0.75 + bat_mod * 0.4) * (1 + delivery_mod["run"]) * confidence_run_mod
        elif o == 0:
            weights[i] *= max(0.5, 1 + bowl_skill * 0.20 - bat_skill * 0.15)

    user_run_mod = sett["user_run_mod"]
    user_wicket_mod = sett["user_wicket_mod"]
    ai_run_mod = max(0.75, 2.0 - user_run_mod)
    ai_wicket_mod = max(0.75, 2.0 - user_wicket_mod)

    for i, o in enumerate(outcomes):
        if o == "W":
            weights[i] *= user_wicket_mod if batting_is_user else ai_wicket_mod
        elif isinstance(o, int) and o > 0:
            weights[i] *= user_run_mod if batting_is_user else ai_run_mod

    return random.choices(outcomes, [max(0.01, w) for w in weights])[0]

# =========================
# PLAY SCREEN
# =========================

def render_play_screen(batting_team, bowling_team, score, wickets, overs,
                       balls, innings_num, lineup, striker, non_striker,
                       batter_runs, batter_balls, current_bowler,
                       bowler_stats, over_log, partnership_runs,
                       pitch, weather, difficulty, personality,
                       field_setup=None, selected_zone=None,
                       timing_grade="-", timing_quality=1.0,
                       bowling_zone="1", target=None, free_hit=False,
                       user_is_batting=True, aggression_level=3, loft_mode=False,
                       bowling_cursor=(2, 1), bowling_type="1", release_grade="-"):
    cur_ov = balls // 6
    cur_bl = balls % 6
    crr = round((score / balls) * 6, 2) if balls > 0 else 0.00
    total = overs * 6

    clear()
    draw_divider("─")
    if target is not None:
        balls_left = max(0, total - balls)
        runs_left = max(0, target - score)
        req_rr = (runs_left * 6 / balls_left) if balls_left else 0.0
        win_pred = max(1, min(99, int(round(58 - (req_rr - crr) * 9 + ((10 - wickets) * 4 + (balls_left / 6) * 2) * 0.9))))
        head = f"{batting_team[:3].upper()} {score}-{wickets} ({cur_ov}.{cur_bl}) • RR {crr:.2f} • NEED {runs_left} OFF {balls_left} • OVS LEFT {(balls_left // 6)}.{(balls_left % 6)} • WIN% {win_pred}"
    else:
        phase = "POWERPLAY" if (balls / total if total else 0) <= 0.33 else "MIDDLE"
        proj = int(round(crr * overs)) if balls else 0
        win_pred = max(5, min(95, int(round(45 + (crr - 7.0) * 7 - wickets * 2.4 + (balls / total if total else 0) * 12))))
        head = f"{batting_team[:3].upper()} {score}-{wickets} ({cur_ov}.{cur_bl}) • RR {crr:.2f} • OVS LEFT {max(0, overs - cur_ov - (1 if cur_bl else 0))}.{(6 - cur_bl) % 6} • PROJ {proj} • PHASE {phase} • WIN% {win_pred}"
    center_line(ctext(head, Fore.CYAN, Style.BRIGHT))
    draw_divider("─")

    s_r = batter_runs.get(striker, 0)
    s_b = batter_balls.get(striker, 0)
    ns_r = batter_runs.get(non_striker, 0)
    ns_b = batter_balls.get(non_striker, 0)
    bst = bowler_stats.get(current_bowler, {"balls": 0, "runs": 0, "wickets": 0})
    bow_balls = bst.get("balls", 0)
    bow_runs = bst.get("runs", 0)
    bow_wkts = bst.get("wickets", 0)
    bow_ov = f"{bow_balls // 6}.{bow_balls % 6}"
    eco = round((bow_runs * 6 / bow_balls), 2) if bow_balls else 0.0

    # Over history formatting (last 5)
    hist = over_log[-5:]
    hist_fmt = []
    for token in hist:
        if token == "W":
            hist_fmt.append(ctext("W", Fore.RED, Style.BRIGHT))
        elif token in ("•", "0"):
            hist_fmt.append(ctext(".", THEME_TEXT, Style.DIM))
        elif token in ("4", "6"):
            hist_fmt.append(ctext(token, Fore.YELLOW, Style.BRIGHT))
        else:
            hist_fmt.append(ctext(str(token), THEME_TEXT))
    hist_line = " ".join(hist_fmt) if hist_fmt else ". . . . ."

    # Tier 2: left and right modules
    if user_is_batting:
        left_lines = [
            ctext(f"{short(lineup[striker])}* {s_r} ({s_b:02d})", THEME_TEXT, Style.BRIGHT),
            ctext(f"{short(lineup[non_striker])}  {ns_r} ({ns_b:02d})", THEME_TEXT, Style.DIM),
            "",
            ctext(f"PARTNER: {partnership_runs}", THEME_TEXT),
            ctext(f"LAST OVR: {hist_line}", THEME_TEXT),
        ]
        focus_zone = selected_zone if selected_zone in FIELD_ZONES else "5"
        def zfmt(z):
            return ctext(f"▶[ {z} ]◀", Fore.CYAN, Style.BRIGHT) if z == focus_zone else ctext(f"({z})", THEME_TEXT, Style.DIM)
        right_lines = [
            "   " + zfmt("3") + "    \\   /    " + zfmt("1"),
            "   " + zfmt("9") + "     \\ /     " + zfmt("2"),
            "   " + zfmt("8") + " ─── [ PITCH ] ─── " + zfmt("6"),
            "   " + zfmt("7") + "     / \\     " + zfmt("4"),
            "            " + zfmt("5"),
        ]
        left_title, right_title = "BATSMAN", "FIELD RADAR"
    else:
        left_lines = [
            ctext(f"{short(current_bowler)}* {bow_ov}-{bow_runs}-{bow_wkts}", THEME_TEXT, Style.BRIGHT),
            ctext(f"ECONOMY: {eco:.2f}", THEME_TEXT, Style.DIM),
            "",
            ctext(f"STRIKER: {short(lineup[striker])} ({s_r})", THEME_TEXT),
            ctext(f"OVER: {hist_line}", THEME_TEXT),
        ]
        right_lines = [
            ctext("SET: ATTACKING", THEME_TEXT),
            ctext("BIAS: OFF-SIDE", THEME_TEXT),
            "",
            ctext("[1] SLIP   [6] FINE", THEME_TEXT),
            ctext("[2] COVER  [7] MID-ON", THEME_TEXT),
        ]
        left_title, right_title = "BOWLER", "FIELD TACTICS"

    draw_dual_panels(left_title, left_lines, right_title, right_lines,
                     panel_width=min(44, max(34, (term_width() - 8) // 2)))
    draw_divider("─")

    # Tier 3: action module
    timing_label, _ = timing_feedback(timing_grade, timing_quality)
    if user_is_batting:
        focus_zone = selected_zone if selected_zone in FIELD_ZONES else "5"
        gap_open = zone_gap_state(field_setup, focus_zone)
        gap_text = ctext("WIDELY OPEN (+15% RUNS)", Fore.GREEN, Style.BRIGHT) if gap_open else ctext("GUARDED", Fore.RED, Style.BRIGHT)
        facing = ZONE_PROFILE.get(focus_zone, "straight").upper()
        action_left = [
            ctext(f"POWER: {progress_bar(aggression_level, 5, 12)} {'AGGRESSIVE' if aggression_level >= 4 else 'CONTROLLED'}", THEME_TEXT),
            ctext(f"TYPE:  {'LOFT' if loft_mode else 'FRONT-FOOT'}", THEME_TEXT),
        ]
        action_right = [
            ctext(f"AIM: ({focus_zone}) {FIELD_ZONES.get(focus_zone, 'STRAIGHT').upper()}", THEME_TEXT),
            ctext(f"BATTER FACING: {facing}", Fore.CYAN, Style.BRIGHT),
            ctext(f"GAP: {gap_text}", THEME_TEXT),
        ]
    else:
        r, c = bowling_cursor
        row_name = BOWL_ROWS[r]
        col_name = BOWL_COLS[c]
        row_labels = [ctext(f"({name})", Fore.CYAN if i == r else THEME_TEXT, Style.BRIGHT if i == r else Style.DIM) for i, name in enumerate(BOWL_ROWS)]
        col_labels = [ctext(f"({name})", Fore.CYAN if i == c else THEME_TEXT, Style.BRIGHT if i == c else Style.DIM) for i, name in enumerate(BOWL_COLS)]

        grid = [
            f"      {pad_visible(col_labels[0], 10)}  {pad_visible(col_labels[1], 10)}  {pad_visible(col_labels[2], 10)}",
            f"{pad_visible(row_labels[0], 9)} |{' ' * (2 + c * 12)}{ctext('⊙', Fore.CYAN, Style.BRIGHT) if r == 0 else ' '}|",
            f"{pad_visible(row_labels[1], 9)} |{' ' * (2 + c * 12)}{ctext('⊙', Fore.CYAN, Style.BRIGHT) if r == 1 else ' '}|",
            f"{pad_visible(row_labels[2], 9)} |{' ' * (2 + c * 12)}{ctext('⊙', Fore.CYAN, Style.BRIGHT) if r == 2 else ' '}|",
            f"{pad_visible(row_labels[3], 9)} |{' ' * (2 + c * 12)}{ctext('⊙', Fore.CYAN, Style.BRIGHT) if r == 3 else ' '}|",
        ]
        action_left = grid
        action_right = [
            ctext(f"TYPE [{bowling_type}]: {BOWLING_PLANS.get(bowling_type, BOWLING_PLANS['1'])['name']}", THEME_TEXT),
            ctext(f"TARGET: {row_name} / {col_name}", Fore.CYAN, Style.BRIGHT),
            ctext(f"RELEASE: {progress_bar(int(max(1, min(10, timing_quality * 10))), 10, 10)}", THEME_TEXT),
            ctext(f"> {release_grade} <", Fore.GREEN if release_grade == "PERFECT" else (Fore.CYAN if release_grade == "GOOD" else Fore.YELLOW), Style.BRIGHT),
        ]

    draw_dual_panels("SHOT SELECT" if user_is_batting else "LINE & LENGTH",
                     action_left,
                     "EXECUTION",
                     action_right,
                     panel_width=min(44, max(34, (term_width() - 8) // 2)))

    if user_is_batting:
        center_line(ctext("RADAR: PRESS [1-9] TO PICK SHOT DIRECTION. THEN [SPACE/ENTER] TO PLAY.", THEME_TEXT, Style.DIM))

    # Tier 4: footer
    draw_divider("─")
    if user_is_batting:
        center_line(ctext("[1-9] AIM | [Q/E] POWER | [L] LOFT | [SPACE/ENTER] HIT | [ESC]", THEME_TEXT, Style.BRIGHT))
        if timing_label == "PERFECT":
            center_line(ctext("> PERFECT <", Fore.CYAN, Style.BRIGHT))
        else:
            center_line(ctext(f"> {timing_label} <", THEME_TEXT, Style.DIM))
    else:
        center_line(ctext("[1-4] BALL TYPE | [ARROWS] TARGET | [SPACE/ENTER] RELEASE | [ESC]", THEME_TEXT, Style.BRIGHT))
        if release_grade == "PERFECT":
            center_line(ctext("RELEASE PERFECT", Fore.GREEN, Style.BRIGHT))
        elif release_grade in ("EARLY", "LATE"):
            center_line(ctext(f"RELEASE {release_grade}", Fore.YELLOW, Style.BRIGHT))

    if free_hit:
        center_line(ctext("ALERT: FREE HIT", Fore.RED, Style.BRIGHT))

# =========================
# INNINGS SUMMARY
# Called immediately when an innings ends — before returning to main().
# For innings 1: shows the chase target box and waits for Enter.
# For innings 2: shows "PRESS ENTER TO SEE FINAL RESULT" and waits.
# =========================

def show_innings_summary(batting_team, score, wickets, balls,
                         overs, extras_detail, batter_runs, batter_balls,
                         batter_fours, batter_sixes, batter_dismissal,
                         bowler_stats, lineup, is_first_innings, first_innings_score=0):
    print_header("INNINGS SUMMARY")

    crr     = round((score / balls) * 6, 2) if balls > 0 else 0.00
    ov_str  = f"{balls // 6}.{balls % 6}"
    w_cnt   = extras_detail.get("w",  0)
    lb_cnt  = extras_detail.get("lb", 0)
    nb_cnt  = extras_detail.get("nb", 0)
    total_x = w_cnt + lb_cnt + nb_cnt

    center_line(ctext(f"INNINGS COMPLETE: {batting_team.upper()}", THEME_ACCENT, Style.BRIGHT))
    center_line(ctext(f"TOTAL: {score}/{wickets} ({ov_str} overs) | RUN RATE: {crr:.2f}", THEME_TEXT, Style.BRIGHT))
    center_line(ctext(f"EXTRAS: {total_x} (w{w_cnt}, lb{lb_cnt}, nb{nb_cnt})", THEME_TEXT))
    print()

    bat_rows = []
    shown = 0
    for i, name in enumerate(lineup):
        r = batter_runs.get(i, 0)
        b = batter_balls.get(i, 0)
        if b == 0 and i > wickets:
            continue
        sr   = round((r / b) * 100, 1) if b > 0 else 0.0
        dis  = batter_dismissal.get(i, "not out")
        f4   = batter_fours.get(i, 0)
        s6   = batter_sixes.get(i, 0)
        bdry = f"[4x{f4}, 6x{s6}]"
        bat_rows.append(f"{short(name):<16} {dis:<20} {r:>3} ({b:02d}) {bdry:<10} SR {sr:>5.1f}")
        shown += 1
    if shown == 0:
        bat_rows.append("(no batters recorded)")

    bowl_rows = []
    for bname, bst in bowler_stats.items():
        if bst["balls"] == 0:
            continue
        ov  = f"{bst['balls'] // 6}.{bst['balls'] % 6}"
        eco = round((bst["runs"] / bst["balls"]) * 6, 2) \
              if bst["balls"] > 0 else 0.00
        bowl_rows.append(f"{short(bname):<18} O:{ov:>4} M:{bst['maidens']:>2} R:{bst['runs']:>3} W:{bst['wickets']:>2} ECO:{eco:>4.2f}")
    if not bowl_rows:
        bowl_rows.append("(no bowling figures)")

    max_rows = 6 if term_height() < 34 else 10
    center_line(ctext("BATTING SUMMARY", THEME_ACCENT, Style.BRIGHT))
    for row in bat_rows[:max_rows]:
        center_line(ctext(row, THEME_TEXT))
    print()
    center_line(ctext("BOWLING SUMMARY", THEME_ACCENT, Style.BRIGHT))
    for row in bowl_rows[:max_rows]:
        center_line(ctext(row, THEME_TEXT))
    print()

    if is_first_innings:
        # Show the target the chasing team needs
        target = score + 1
        rrr    = round((target / (overs * 6)) * 6, 2)
        draw_box(["",
                  f"   TARGET: {target} RUNS TO WIN  (REQUIRED RATE: {rrr:.2f})",
                  ""])
        print()
        safe_input(">> PRESS [ENTER] TO START THE CHASE...", "")
    else:
        print()
        safe_input(">> PRESS [ENTER] TO SEE FINAL RESULT...", "")

# =========================
# INNINGS ENGINE
# =========================

def play_innings(overs, batting_team, bowling_team, user_is_batting,
                 pitch, weather, innings_num, difficulty, personality, target=None):
    lineup      = TEAMS[batting_team]
    striker     = 0
    non_striker = 1
    score       = 0
    wickets     = 0
    balls       = 0
    total_balls = overs * 6
    over_log    = []

    batter_runs      = {i: 0 for i in range(11)}
    batter_balls     = {i: 0 for i in range(11)}
    batter_fours     = {i: 0 for i in range(11)}
    batter_sixes     = {i: 0 for i in range(11)}
    batter_dismissal = {}

    bowler_stats   = {}
    bowler_overs   = {}
    last_bowler    = None
    max_quota      = max(1, math.ceil(overs / 5))
    if not user_is_batting:
        current_bowler = user_pick_bowler(bowling_team, bowler_overs, {},
                                          max_quota, None, 1)
    else:
        current_bowler = pick_bowler(bowling_team, bowler_overs, max_quota)

    extras_detail    = {"w": 0, "lb": 0, "nb": 0}
    partnership_runs = 0
    free_hit         = False
    user_drs         = 1
    play_innings._comp_drs = 1
    selected_zone    = "5"
    timing_grade     = "-"
    timing_quality   = 1.0
    bowling_zone     = "1"
    aggression_level = 3
    loft_mode        = False
    bowling_cursor   = (2, 1)
    bowling_type     = "1"
    release_grade    = "-"

    def ensure_bowler(name):
        if name not in bowler_stats:
            bowler_stats[name] = {
                "balls": 0, "runs": 0, "wickets": 0,
                "maidens": 0, "over_runs": []
            }

    ensure_bowler(current_bowler)

    while balls < total_balls and wickets < 10:
        if target is not None and score >= target:
            break

        bst = bowler_stats[current_bowler]
        if user_is_batting:
            bowling_zone = choose_ai_bowling_plan(balls, total_balls, target, score)
        field_setup = (get_ai_field_setup(personality, balls, total_balls, wickets, target, score)
                   if user_is_batting else None)

        render_play_screen(
            batting_team, bowling_team, score, wickets, overs, balls,
            innings_num, lineup, striker, non_striker,
            batter_runs, batter_balls, current_bowler, bowler_stats,
            over_log, partnership_runs, pitch, weather, difficulty, personality,
            field_setup, selected_zone, timing_grade, timing_quality,
            bowling_zone, target, free_hit, user_is_batting, aggression_level, loft_mode,
            bowling_cursor, bowling_type, release_grade
        )

        # Show correct commands based on current bowler type
        b_type = get_stat(current_bowler, "bowl_type", "medium")
        center_line(ctext("━" * min(term_width() - 2, 112), Fore.CYAN, Style.BRIGHT))
        if user_is_batting:
            center_line(ctext("BATTING: [1-9] AIM ZONE | [Q/E] POWER | [L] LOFT | [SPACE/ENTER] PLAY", Fore.WHITE, Style.BRIGHT))
            center_line(ctext(f"BOWLER PLAN: {BOWLING_PLANS.get(bowling_zone, BOWLING_PLANS['1'])['name']}", Fore.CYAN, Style.BRIGHT))
        else:
            if b_type == "spin":
                center_line(ctext("SPIN CONTROL: [1] NORMAL [2] SHORT [3] FULL [4] YORKER", Fore.WHITE, Style.BRIGHT))
            else:
                center_line(ctext("PACE CONTROL: [1] NORMAL [2] SHORT [3] FULL [4] YORKER", Fore.WHITE, Style.BRIGHT))
            center_line(ctext("BOWLING: ARROWS MOVE TARGET, SPACE/ENTER LOCK RELEASE", Fore.WHITE))
        center_line(ctext("SYSTEM: [ESC] Pause / Resume", Fore.WHITE))
        center_line(ctext("═" * min(term_width() - 2, 112), Fore.CYAN, Style.BRIGHT))

        # Input
        shot = delivery = None
        timing_quality = 1.0
        timing_grade = "-"
        release_grade = "-"
        if user_is_batting:
            while shot is None:
                k = get_key()
                if k == "ESC":
                    pause_game()
                    continue
                if k == "Q":
                    aggression_level = max(1, aggression_level - 1)
                    render_play_screen(
                        batting_team, bowling_team, score, wickets, overs, balls,
                        innings_num, lineup, striker, non_striker,
                        batter_runs, batter_balls, current_bowler, bowler_stats,
                        over_log, partnership_runs, pitch, weather, difficulty, personality,
                        field_setup, selected_zone, timing_grade, timing_quality,
                        bowling_zone, target, free_hit, user_is_batting, aggression_level, loft_mode
                    )
                    continue
                if k == "E":
                    aggression_level = min(5, aggression_level + 1)
                    render_play_screen(
                        batting_team, bowling_team, score, wickets, overs, balls,
                        innings_num, lineup, striker, non_striker,
                        batter_runs, batter_balls, current_bowler, bowler_stats,
                        over_log, partnership_runs, pitch, weather, difficulty, personality,
                        field_setup, selected_zone, timing_grade, timing_quality,
                        bowling_zone, target, free_hit, user_is_batting, aggression_level, loft_mode
                    )
                    continue
                if k in ("L",):
                    loft_mode = not loft_mode
                    render_play_screen(
                        batting_team, bowling_team, score, wickets, overs, balls,
                        innings_num, lineup, striker, non_striker,
                        batter_runs, batter_balls, current_bowler, bowler_stats,
                        over_log, partnership_runs, pitch, weather, difficulty, personality,
                        field_setup, selected_zone, timing_grade, timing_quality,
                        bowling_zone, target, free_hit, user_is_batting, aggression_level, loft_mode
                    )
                    continue

                if k in ("SPACE", "ENTER"):
                    shot = "LOFT" if loft_mode else ("SWING" if aggression_level >= 4 else "DEFEND")
                elif k in FIELD_ZONES:
                    selected_zone = k
                    render_play_screen(
                        batting_team, bowling_team, score, wickets, overs, balls,
                        innings_num, lineup, striker, non_striker,
                        batter_runs, batter_balls, current_bowler, bowler_stats,
                        over_log, partnership_runs, pitch, weather, difficulty, personality,
                        field_setup, selected_zone, timing_grade, timing_quality,
                        bowling_zone, target, free_hit, user_is_batting, aggression_level, loft_mode,
                        bowling_cursor, bowling_type, release_grade
                    )

            # Computer bowler picks delivery based on their type
            delivery = choose_ai_delivery(b_type, balls, total_balls, target, score, personality)
        else:
            while delivery is None:
                k = get_key()
                if k == "ESC":
                    pause_game()
                    continue
                if k in ("1", "2", "3", "4"):
                    bowling_type = k
                    render_play_screen(
                        batting_team, bowling_team, score, wickets, overs, balls,
                        innings_num, lineup, striker, non_striker,
                        batter_runs, batter_balls, current_bowler, bowler_stats,
                        over_log, partnership_runs, pitch, weather, difficulty, personality,
                        field_setup, selected_zone, timing_grade, timing_quality,
                        bowling_zone, target, free_hit, user_is_batting, aggression_level, loft_mode,
                        bowling_cursor, bowling_type, release_grade
                    )
                    continue
                if k in ("UP", "DOWN", "LEFT", "RIGHT"):
                    bowling_cursor = move_pitch_cursor(bowling_cursor, k)
                    render_play_screen(
                        batting_team, bowling_team, score, wickets, overs, balls,
                        innings_num, lineup, striker, non_striker,
                        batter_runs, batter_balls, current_bowler, bowler_stats,
                        over_log, partnership_runs, pitch, weather, difficulty, personality,
                        field_setup, selected_zone, timing_grade, timing_quality,
                        bowling_zone, target, free_hit, user_is_batting, aggression_level, loft_mode,
                        bowling_cursor, bowling_type, release_grade
                    )
                    continue
                if k in ("SPACE", "ENTER"):
                    release_grade, timing_quality, drift = run_release_meter(get_stat(current_bowler, "bowl_skill", 75), difficulty)
                    dr, dc = drift
                    r, c = bowling_cursor
                    effective_cursor = (max(0, min(3, r + dr)), max(0, min(2, c + dc)))
                    bowling_zone = cursor_to_plan(effective_cursor)
                    timing_grade = release_grade
                    delivery = delivery_from_type_and_bowler(b_type, bowling_type)
            shot = choose_ai_shot(delivery, target, score, balls, total_balls, wickets, difficulty, personality)

        print()
        animate("  Bowler runs in...", delay=0.02)
        pause(0.35)

        if user_is_batting:
            timing_grade, timing_quality = run_timing_challenge(
                delivery,
                get_stat(lineup[striker], "bat_skill", 50),
                difficulty,
                get_stat(current_bowler, "bowl_skill", 75),
            )
            animate(f"  Timing: {timing_grade}")

        # No-ball
        if (not free_hit) and random.random() < 0.04:
            animate(f"  {random.choice(COMMENTARY['NB'])}")
            score += 1; extras_detail["nb"] += 1
            bst["runs"] += 1; bst["over_runs"].append("NB"); over_log.append("nb")
            free_hit = True; pause(0.9); continue

        # Wide — pace: IN/BOUNCER can go wide; spin: GOOGLY/FLIPPER can
        wide_types = ["IN", "BOUNCER"] if b_type != "spin" else ["GOOGLY", "FLIPPER"]
        if delivery in wide_types and random.random() < 0.04:
            animate(f"  {random.choice(COMMENTARY['WD'])}")
            score += 1; extras_detail["w"] += 1
            bst["runs"] += 1; bst["over_runs"].append("WD"); over_log.append("wd")
            pause(0.9); continue

        # Outcome
        result = compute_outcome(
            shot, lineup[striker], current_bowler,
            delivery, pitch, weather,
            batter_balls[striker], bst["balls"],
            difficulty, batting_is_user=user_is_batting
        )

        if user_is_batting:
            result = apply_timing_and_zone(
                result, shot, timing_grade, timing_quality,
                selected_zone, field_setup, lineup[striker], delivery,
                balls, total_balls
            )
            gap_open = zone_gap_state(field_setup, selected_zone)
            if isinstance(result, int) and result > 0:
                # Aggression affects conversion potential.
                if aggression_level >= 4 and random.random() < 0.18:
                    result = min(6, result + 1)
                # Open gap reward
                if gap_open and random.random() < 0.30:
                    if result in (1, 2):
                        result = min(4, result + 2)
                # Guarded zones increase dismissal risk on mistimed attacks
                if (not gap_open) and shot in ("SWING", "LOFT") and timing_grade in ("EARLY", "LATE", "MISS"):
                    if random.random() < 0.16:
                        result = "W"
        else:
            result = apply_bowling_zone_effect(result, delivery, bowling_zone, balls, total_balls)

        # Free hit
        if free_hit and result == "W":
            animate("  FREE HIT saves him — cannot be dismissed!")
            result = 0
        free_hit = False

        # Wicket
        if result == "W":
            animate(f"  {random.choice(COMMENTARY['W'])}")

            # ── Pick dismissal type BEFORE DRS ────────────────────────
            fielders = [p for p in TEAMS[bowling_team] if p != current_bowler]
            fielder  = short(random.choice(fielders)) if fielders else "sub"
            wk       = short(TEAMS[bowling_team][min(6, len(TEAMS[bowling_team]) - 1)])
            dis_tmpl, credit, drs_eligible = pick_dismissal(delivery)
            dis_str  = dis_tmpl.format(
                bowler=short(current_bowler), fielder=fielder, wk=wk)

            # ── DRS — only offered for LBW and edge/caught-behind ─────
            overturned = False
            if drs_eligible:
                if user_is_batting:
                    # User's batter got out — user can review
                    if user_drs > 0:
                        yn = safe_input("  Challenge with DRS? (Y/N): ", "N").strip().upper()
                        if yn == "Y":
                            user_drs -= 1
                            if random.random() < 0.35:
                                animate("  DRS: Replays show it's missing — NOT OUT!")
                                overturned = True
                            else:
                                animate("  DRS: Ball-tracking confirms — OUT stands!")
                else:
                    # Computer's batter got out — computer may review
                    comp_drs = getattr(play_innings, '_comp_drs', 1)
                    ai_review_chance = DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS["Normal"])["ai_review"]
                    if comp_drs > 0 and random.random() < ai_review_chance:
                        animate("  Computer reviews the decision...")
                        pause(0.8)
                        play_innings._comp_drs = comp_drs - 1
                        if random.random() < 0.35:
                            animate("  DRS: Replays show it's missing — NOT OUT!")
                            overturned = True
                        else:
                            animate("  DRS: Ball-tracking confirms — OUT stands!")
            else:
                # No DRS available — show reason for clarity
                if dis_tmpl.startswith("run out"):
                    animate("  Run out — no DRS available for run outs.")
                # For bowled/caught/stumped, umpire's finger is final — silent

            if overturned:
                result = 0
                animate("  Batter survives!")
            else:
                batter_dismissal[striker] = dis_str
                batter_balls[striker] += 1

                print(f"\n  {lineup[striker]}: {batter_runs[striker]}"
                      f"({batter_balls[striker]}b) — {dis_str}")
                pause(1.5)

                # Only credit the bowler if it's a bowler dismissal (not run out)
                if credit == "bowler":
                    bst["wickets"] += 1
                bst["balls"]          += 1
                bst["over_runs"].append("W")
                over_log.append("W")
                balls                 += 1
                wickets               += 1
                partnership_runs       = 0

                if wickets >= 10:
                    break

                striker = wickets + 1
                batter_runs.setdefault(striker, 0)
                batter_balls.setdefault(striker, 0)

                if balls % 6 == 0 and balls > 0:
                    striker, non_striker = non_striker, striker
                    _close_over(current_bowler, bowler_stats, bowler_overs)
                    last_bowler = current_bowler
                    next_ov = balls // 6 + 1
                    if not user_is_batting:
                        current_bowler = user_pick_bowler(
                            bowling_team, bowler_overs, bowler_stats,
                            max_quota, last_bowler, next_ov)
                    else:
                        current_bowler = pick_bowler(bowling_team, bowler_overs,
                                                     max_quota, last_bowler)
                    ensure_bowler(current_bowler)
                    over_log = []
                    animate(f"\n  --- END OF OVER {balls // 6} ---")
                    pause(1.2)
                continue

        # Runs
        if isinstance(result, int):
            animate(f"  {random.choice(COMMENTARY.get(result, [str(result)+' run(s).']))}")
            score                 += result
            bst["runs"]           += result
            bst["over_runs"].append(str(result))
            over_log.append("•" if result == 0 else str(result))
            batter_runs[striker]  += result
            batter_balls[striker] += 1
            bst["balls"]          += 1
            balls                 += 1
            partnership_runs      += result
            if result == 4: batter_fours[striker] += 1
            if result == 6: batter_sixes[striker] += 1
            if result % 2 == 1:
                striker, non_striker = non_striker, striker
            pause(0.85)

        # End of over
        if balls % 6 == 0 and balls > 0:
            striker, non_striker = non_striker, striker
            _close_over(current_bowler, bowler_stats, bowler_overs)
            last_bowler = current_bowler
            next_ov = balls // 6 + 1
            if not user_is_batting:
                current_bowler = user_pick_bowler(
                    bowling_team, bowler_overs, bowler_stats,
                    max_quota, last_bowler, next_ov)
            else:
                current_bowler = pick_bowler(bowling_team, bowler_overs,
                                             max_quota, last_bowler)
            ensure_bowler(current_bowler)
            over_log = []
            animate(f"\n  --- END OF OVER {balls // 6} ---")
            pause(1.2)

        if target is not None and score >= target:
            break

    # ── INNINGS SUMMARY shown immediately here, before returning ──────
    # is_first_innings=True  → shows chase target box + "START THE CHASE"
    # is_first_innings=False → shows "SEE FINAL RESULT"
    show_innings_summary(
        batting_team, score, wickets, balls, overs,
        extras_detail, batter_runs, batter_balls,
        batter_fours, batter_sixes, batter_dismissal,
        bowler_stats, lineup,
        is_first_innings=(innings_num == 1)
    )

    return score, wickets, balls, bowler_stats, batter_runs, batter_balls


def _close_over(bowler, bowler_stats, bowler_overs):
    if bowler not in bowler_stats:
        return
    bst = bowler_stats[bowler]
    if bst["over_runs"] and all(r in ["0", "W", "•"] for r in bst["over_runs"]):
        bst["maidens"] += 1
    bst["over_runs"] = []
    bowler_overs[bowler] = bowler_overs.get(bowler, 0) + 1

# =========================
# PLAYER OF THE MATCH
# =========================

def pick_potm(t1, t2, br1, bb1, bs1, br2, bb2, bs2):
    candidates = []
    for i, name in enumerate(TEAMS[t1]):
        sc = br1.get(i, 0) + bs1.get(name, {}).get("wickets", 0) * 25
        candidates.append((sc, name, t1, bs1))
    for i, name in enumerate(TEAMS[t2]):
        sc = br2.get(i, 0) + bs2.get(name, {}).get("wickets", 0) * 25
        candidates.append((sc, name, t2, bs2))
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0] if candidates else (0, "Unknown", "", {})

# =========================
# FINAL RESULT SCREEN
# =========================

def show_final_result(player_team, t1, s1, w1, b1,
                      t2, s2, w2, b2, overs,
                      bs1, br1, bb1, bs2, br2, bb2, history):
    print_header("MATCH RESULT")

    target = s1 + 1

    if s2 >= target:
        wkts_left = 10 - w2
        balls_rem  = overs * 6 - b2
        ovs_rem    = f"{balls_rem // 6}.{balls_rem % 6}"
        msg    = f"{t2} WIN BY {wkts_left} WICKET(S) ({ovs_rem} OVERS REMAINING)"
        winner = t2
    elif s2 == s1:
        msg    = "IT IS A TIE! WHAT A MATCH!"
        winner = "Tie"
    else:
        margin = s1 - s2
        msg    = f"{t1} WIN BY {margin} RUN(S)"
        winner = t1

    center_line(ctext("-- FINAL VERDICT --", THEME_ACCENT, Style.BRIGHT))
    center_line(ctext(msg, THEME_ACCENT, Style.BRIGHT))

    rr1 = round((s1 / (b1 if b1 else 1)) * 6, 2)
    rr2 = round((s2 / (b2 if b2 else 1)) * 6, 2)
    ov1 = f"{b1 // 6}.{b1 % 6}"
    ov2 = f"{b2 // 6}.{b2 % 6}"

    recap_l = [
        f"1ST INNINGS ({t1}): {s1}/{w1} ({ov1}) | RR: {rr1}",
        f"2ND INNINGS ({t2}): {s2}/{w2} ({ov2}) | RR: {rr2}",
    ]

    potm_sc, potm_name, potm_team, potm_bst_dict = pick_potm(
        t1, t2, br1, bb1, bs1, br2, bb2, bs2)
    potm_bst   = potm_bst_dict.get(potm_name, {})
    potm_idx   = (TEAMS.get(potm_team, []).index(potm_name)
                  if potm_name in TEAMS.get(potm_team, []) else 0)
    potm_runs  = (br1 if potm_team == t1 else br2).get(potm_idx, 0)
    potm_bals  = (bb1 if potm_team == t1 else bb2).get(potm_idx, 0)
    potm_wkts  = potm_bst.get("wickets", 0)

    potm_lines = [f"{short(potm_name)} ({potm_team})"]
    if potm_bst.get("balls", 0) > 0:
        ov_s = f"{potm_bst['balls'] // 6}.{potm_bst['balls'] % 6}"
        potm_lines.append(f"Performance: {ov_s} - {potm_bst.get('maidens',0)} - {potm_bst.get('runs',0)} - {potm_wkts}")
    else:
        potm_lines.append(f"Performance: {potm_runs} runs ({potm_bals} balls)")

    all_bat = []
    for i, name in enumerate(TEAMS[t1]):
        all_bat.append((br1.get(i, 0), bb1.get(i, 0), name))
    for i, name in enumerate(TEAMS[t2]):
        all_bat.append((br2.get(i, 0), bb2.get(i, 0), name))
    all_bat.sort(key=lambda x: x[0], reverse=True)

    all_bowl = []
    for name, bst in {**bs1, **bs2}.items():
        if bst.get("balls", 0) > 0:
            all_bowl.append((bst["wickets"], bst["runs"], bst["balls"], name))
    all_bowl.sort(key=lambda x: (-x[0], x[1]))

    left_rows  = []
    right_rows = []
    for r, b, name in all_bat[:3]:
        left_rows.append(f"  {short(name):<18}  {r} ({b})")
    for wk, rns, bls, name in all_bowl[:3]:
        right_rows.append(f"  {short(name):<18}  {wk}/{rns}")

    print()
    center_line(ctext("FINAL RECAP", THEME_ACCENT, Style.BRIGHT))
    for ln in recap_l:
        center_line(ctext(ln, THEME_TEXT))
    print()
    center_line(ctext("PLAYER OF THE MATCH", THEME_ACCENT, Style.BRIGHT))
    for ln in potm_lines:
        center_line(ctext(ln, THEME_TEXT))
    print()
    center_line(ctext("BATTING LEADERS", THEME_ACCENT, Style.BRIGHT))
    for ln in left_rows[:3]:
        center_line(ctext(ln.strip(), THEME_TEXT))
    print()
    center_line(ctext("BOWLING LEADERS", THEME_ACCENT, Style.BRIGHT))
    for ln in right_rows[:3]:
        center_line(ctext(ln.strip(), THEME_TEXT))
    print()
    center_line(ctext("[R] REPLAY  |  [Q] MENU", THEME_ACCENT, Style.BRIGHT))

    history_result = "Match tied" if winner == "Tie" else f"{winner} won"
    history.append(
        f"{t1} {s1}/{w1}  vs  {t2} {s2}/{w2}  —  {history_result}")

    while True:
        choice = safe_input(">> SELECT OPTION: ", "Q").strip().upper()
        if choice == "R":
            return "replay"
        elif choice == "Q":
            return "menu"
        else:
            print("  Type R to replay or Q to quit to menu.")

# =========================
# MAIN
# =========================

def main():
    normalize_terminal_viewport()
    game_data = load_game_data()
    history = game_data["history"]
    stats = game_data["stats"]
    menu_overs = 5
    menu_difficulty = "Normal"
    menu_personality = "Balanced"
    while True:
        preview = f"{menu_overs} OVERS | {menu_difficulty.upper()} | {menu_personality.upper()}"
        action = main_menu(settings_preview=preview)

        if action == "records":
            show_records(history, stats)
            continue

        if action == "settings":
            menu_overs, menu_difficulty, menu_personality = choose_match_settings()
            continue

        # Quick Match should always allow changing overs/difficulty/personality before start.
        menu_overs, menu_difficulty, menu_personality = choose_match_settings()
        overs, difficulty, personality = menu_overs, menu_difficulty, menu_personality

        player, computer = choose_team()
        if not player:
            continue
        pitch, weather   = setup_conditions()
        user_bats_first  = toss(player, computer)

        t1 = player   if user_bats_first else computer
        t2 = computer if user_bats_first else player

        # Innings 1 — summary shown inside play_innings, user presses Enter
        print_header("MATCH START")
        center_line(ctext(f"{t1} WILL BAT FIRST", Fore.YELLOW, Style.BRIGHT))
        center_line(ctext(f"Difficulty: {difficulty} | AI: {personality}", Fore.WHITE, Style.DIM))
        print()
        safe_input(">> PRESS [ENTER] TO START THE INNINGS...", "")
        s1, w1, b1, bs1, br1, bb1 = play_innings(
            overs, t1, t2, t1 == player, pitch, weather, 1, difficulty, personality)

        # Innings 2 — starts right after user pressed Enter on innings 1 summary
        s2, w2, b2, bs2, br2, bb2 = play_innings(
            overs, t2, t1, t2 == player, pitch, weather, 2, difficulty, personality, s1 + 1)

        # Final result
        action = show_final_result(
            player, t1, s1, w1, b1,
                    t2, s2, w2, b2, overs,
            bs1, br1, bb1, bs2, br2, bb2, history
        )

        stats["matches"] += 1
        stats["total_runs"] += s1 + s2
        stats["total_wickets"] += w1 + w2
        stats["highest_match_total"] = max(stats["highest_match_total"], s1 + s2)

        if s2 == s1:
            stats["ties"] += 1
        else:
            user_won = (t1 == player and s1 > s2) or (t2 == player and s2 > s1)
            if user_won:
                stats["user_wins"] += 1
            else:
                stats["user_losses"] += 1

        game_data["history"] = history[-100:]
        game_data["stats"] = stats
        save_game_data(game_data)

        if action == "menu":
            continue

if __name__ == "__main__":
    main()