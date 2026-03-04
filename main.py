import os
import random
import sys
import time

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
    """V. Kohli style short name."""
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

def get_stat(player, key, default=50):
    return PLAYER_STATS.get(player, {}).get(key, default)

# =========================
# PITCH & WEATHER
# =========================

PITCH_TYPES = {
    "Flat":      {"pace_mod": -0.10, "spin_mod": -0.15, "bat_mod": +0.15},
    "Green Top": {"pace_mod": +0.20, "spin_mod": -0.10, "bat_mod": -0.10},
    "Dusty":     {"pace_mod": -0.10, "spin_mod": +0.20, "bat_mod": -0.10},
    "Slow":      {"pace_mod": -0.05, "spin_mod": +0.10, "bat_mod": -0.05},
}
WEATHER_CONDITIONS = {
    "Sunny":    {"swing_mod": -0.10},
    "Overcast": {"swing_mod": +0.20},
    "Humid":    {"swing_mod": +0.10},
    "Windy":    {"swing_mod": +0.05},
}

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
    "Timing is everything! Use [S]wing for power and [D]efend for survival.",
    "Pace bowlers thrive on Green Top pitches.",
    "Spinners love a Dusty track — dangerous in the death overs.",
    "A maiden over builds pressure. Bowl tight lines!",
    "Use DRS wisely — you only get one review per innings.",
    "Overcast conditions? Swing bowlers will be lethal.",
    "The first 6 balls for a new batter are the most dangerous.",
    "Partnership building is key. Don't throw wickets away early.",
]

DISMISSAL_METHODS = [
    "c. {fielder} b. {bowler}",
    "lbw b. {bowler}",
    "b. {bowler}",
    "c. {fielder} b. {bowler}",
    "run out ({fielder})",
    "st. {wk} b. {bowler}",
]

BOWL_SHOT_BIAS = {
    "IN":      [55, 20,  5, 20],
    "OUT":     [15, 50, 20, 15],
    "REVERSE": [20, 15, 10, 55],
    "BOUNCER": [10, 20, 55, 15],
}
SHOT_OUTCOMES = {
    "DEFEND": ([0, 1, "W"],        [60, 30, 10]),
    "SWING":  ([0, 1, 2, 4, "W"], [20, 25, 25, 20, 10]),
    "LOFT":   ([0, 4, 6, "W"],    [15, 40, 30, 15]),
    "LEAVE":  ([0, "W"],           [85, 15]),
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

def draw_box(lines, width=76):
    print("+" + "-" * width + "+")
    for line in lines:
        print("| " + line.ljust(width - 2) + " |")
    print("+" + "-" * width + "+")

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
            return ch.upper()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

# =========================
# HEADER  (kept unchanged)
# =========================

def print_header():
    print("=" * 78)
    print(r"""
 ████████╗██████╗ ██╗ ██████╗██╗  ██╗███████╗████████╗
 ╚══██╔══╝██╔══██╗██║██╔════╝██║ ██╔╝██╔════╝╚══██╔══╝
    ██║   ██████╔╝██║██║     █████╔╝ █████╗     ██║
    ██║   ██╔══██╗██║██║     ██╔═██╗ ██╔══╝     ██║
    ██║   ██║  ██║██║╚██████╗██║  ██╗███████╗   ██║
    ╚═╝   ╚═╝  ╚═╝╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝   ╚═╝
""")
    print("=" * 78)

# =========================
# MAIN MENU  (Image 1)
# =========================

def main_menu():
    while True:
        clear()
        print("=" * 78)
        ver  = "[ V 1.0.4 - CLI CRICKET SIMULATOR ]"
        user = "[ USER: PLAYER_1 ]"
        gap  = 78 - len(ver) - len(user)
        print(ver + " " * gap + user)
        print("=" * 78)
        print()
        draw_box([
            "",
            "  [1]   QUICK MATCH  (5 / 10 / 20 OVERS)",
            "",
            "  [2]   RECORDS  (MATCH HISTORY & PLAYER STATS)",
            "",
            "  [3]   QUIT GAME",
            "",
        ])
        print()
        print("-" * 78)
        print("TIP: " + random.choice(TIPS))
        print("-" * 78)
        print()
        choice = input(">> SELECT OPTION [1-3]: ").strip()
        if choice == "1":   return "play"
        elif choice == "2": return "records"
        elif choice == "3":
            print("\nGG! Thanks for playing.\n")
            sys.exit(0)

# =========================
# RECORDS
# =========================

def show_records(history):
    clear()
    print_header()
    print()
    if not history:
        print("  No match records yet. Play a game first!")
    else:
        print("  MATCH HISTORY")
        print("  " + "-" * 60)
        for i, rec in enumerate(history[-10:], 1):
            print(f"  {i:>2}. {rec}")
    print()
    input("  >> PRESS ENTER TO GO BACK...")

# =========================
# TEAM SELECTION
# =========================

def choose_team():
    teams = list(TEAMS.keys())
    clear()
    print_header()
    print("\n  SELECT YOUR TEAM:\n")
    for i, t in enumerate(teams, 1):
        print(f"    {i:>2}. {t}")
    print()
    while True:
        try:
            c = int(input("  Enter number: "))
            if 1 <= c <= len(teams):
                player = teams[c - 1]; break
            else: print("  Choose a number from the list.")
        except ValueError: print("  Invalid input.")
    computer = random.choice([t for t in teams if t != player])
    print(f"\n  Your team  : {player}")
    print(f"  Opponent   : {computer}")
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
        "Overcast": "Swing bowlers beware!",
        "Humid": "Some extra movement expected.",
        "Windy": "Gusty conditions at the ground.",
    }
    clear(); print_header()
    print("\n  === MATCH CONDITIONS ===\n")
    animate(f"  Pitch   : {pitch}  —  {desc.get(pitch,'')}")
    animate(f"  Weather : {weather}  —  {desc.get(weather,'')}")
    pause(1.5)
    return pitch, weather

# =========================
# TOSS
# =========================

def toss(player, computer):
    clear(); print_header()
    print("\n  === TOSS ===\n")
    while True:
        call = input("  Call Heads or Tails (H/T): ").strip().lower()
        if call in ["h","heads"]:   user_call="heads"; break
        elif call in ["t","tails"]: user_call="tails"; break
        else: print("  Type H or T.")
    result = random.choice(["heads","tails"])
    animate("  Coin flips...")
    animate(f"  Result: {result.upper()}!")
    if user_call == result:
        print(f"\n  You won the toss!\n")
        while True:
            c = input("  Bat or Bowl? (bat/bowl): ").strip().lower()
            if c in ["bat","b"]:
                animate(f"  {player} will BAT first.")
                input("\n>> PRESS [ENTER] TO CONTINUE...")
                return True
            elif c in ["bowl","bo"]:
                animate(f"  {player} will BOWL first.")
                input("\n>> PRESS [ENTER] TO CONTINUE...")
                return False
            else: print("  Invalid.")
    else:
        comp = random.choice(["bat","bowl"])
        animate(f"\n  {computer} won the toss and chose to {comp}.")
        input("\n>> PRESS [ENTER] TO CONTINUE...")
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
# OUTCOME ENGINE
# =========================

def compute_outcome(shot, batter, bowler, pitch, weather, bat_balls, bowl_balls):
    outcomes, base_w = SHOT_OUTCOMES[shot]
    weights = list(base_w)
    bat_skill  = get_stat(batter,"bat_skill",50) / 100.0
    aggression = min(get_stat(batter,"aggression",80),108) / 100.0
    bowl_skill = get_stat(bowler,"bowl_skill",50) / 100.0
    bowl_type  = get_stat(bowler,"bowl_type","medium")
    pm         = PITCH_TYPES.get(pitch,{})
    pace_mod   = pm.get("pace_mod",0)
    spin_mod   = pm.get("spin_mod",0)
    bat_mod    = pm.get("bat_mod",0)
    swing_m    = WEATHER_CONDITIONS.get(weather,{}).get("swing_mod",0)
    stamina    = get_stat(bowler,"stamina",80)/100.0
    fatigue    = min(0.15, max(0,(bowl_balls-24)*0.005/stamina)) if bowl_balls>24 else 0
    nerves     = max(0,(6-bat_balls)*0.015)
    for i, o in enumerate(outcomes):
        if o == "W":
            pitch_bonus = pace_mod if bowl_type=="pace" else spin_mod
            weights[i] *= (1 + bowl_skill*0.4 + pitch_bonus + swing_m - fatigue + nerves*0.5)
        elif isinstance(o,int) and o >= 4:
            weights[i] *= max(0.3,(aggression*bat_skill+bat_mod)*(1-bowl_skill*0.3))
        elif isinstance(o,int) and o > 0:
            weights[i] *= (bat_skill*0.8 + bat_mod*0.5)
        elif o == 0:
            weights[i] *= (1 + bowl_skill*0.3 - bat_skill*0.2)
    return random.choices(outcomes, [max(0.01,w) for w in weights])[0]

# =========================
# PLAY SCREEN  (Image 2)
# =========================

def render_play_screen(batting_team, bowling_team, score, wickets, overs,
                       balls, innings_num, lineup, striker, non_striker,
                       batter_runs, batter_balls, current_bowler,
                       bowler_stats, over_log, partnership_runs,
                       pitch, weather, target=None, free_hit=False):
    cur_ov = balls // 6
    cur_bl = balls % 6
    crr    = round((score/balls)*6, 2) if balls > 0 else 0.00
    total  = overs * 6

    clear()
    print_header()

    # ── TOP SCORE BAR ──────────────────────────────────────────────────
    left = f"  {batting_team}: {score}/{wickets} ({cur_ov}.{cur_bl})"
    if target is not None:
        balls_left = total - balls
        runs_left  = target - score
        rrr = round((runs_left/balls_left)*6,2) if balls_left > 0 else 0.00
        right = f"TARGET: {target}  (RR: {crr:.2f}, RRR: {rrr:.2f})  "
    else:
        right = f"RR: {crr:.2f}  "
    draw_box([left.ljust(40) + right.rjust(34)])
    print()

    # ── BATTING LEFT / BOWLING RIGHT ───────────────────────────────────
    inn_lbl  = f"BATTING: {batting_team} (Innings {innings_num})"
    bowl_lbl = f"BOWLING: {bowling_team}"
    print(f"  {inn_lbl:<38}  {bowl_lbl}")
    print(f"  {'─'*34}  {'─'*34}")

    s_r  = batter_runs.get(striker, 0)
    s_b  = batter_balls.get(striker, 0)
    ns_r = batter_runs.get(non_striker, 0)
    ns_b = batter_balls.get(non_striker, 0)
    bst  = bowler_stats.get(current_bowler, {"balls": 0, "runs": 0, "wickets": 0})

    # Bowler spell shown as:  J. Bumrah  35-3 (4.0)
    bow_balls = bst.get("balls", 0)
    bow_runs  = bst.get("runs", 0)
    bow_wkts  = bst.get("wickets", 0)
    bow_ov    = f"{bow_balls // 6}.{bow_balls % 6}"
    bow_spell = f"{bow_runs}-{bow_wkts} ({bow_ov})"

    over_sym = "  ".join(over_log) if over_log else "-"

    print(f"  \U0001f3cf STRIKER:  {short(lineup[striker]):<16} {s_r} ({s_b})"
          f"     BOWLER:  {short(current_bowler)}  {bow_spell}")
    print(f"    NON-STR: {short(lineup[non_striker]):<16} {ns_r} ({ns_b})"
          f"     OVER:    {over_sym}")
    print()

    # ── THIS OVER BOX ──────────────────────────────────────────────────
    balls_fmt = "  ".join(f"[ {s} ]" for s in over_log) if over_log else "[ - ]"
    draw_box([f"  THIS OVER:  {balls_fmt}"])
    print()

    # ── CHASE / PARTNERSHIP INFO ───────────────────────────────────────
    if target is not None:
        runs_left  = target - score
        balls_left = total - balls
        print(f"  >> {runs_left} RUNS REMAINING OFF {balls_left} BALLS")
    print(f"  >> CURRENT PARTNERSHIP: {partnership_runs} runs")
    if free_hit:
        print("  >> *** FREE HIT! ***")
    print()
    print(f"  Pitch: {pitch}   Weather: {weather}")
    print()
    print("-" * 78)

# =========================
# INNINGS SUMMARY SCREEN  (Image 3)
# =========================

def show_innings_summary(batting_team, bowling_team, score, wickets, balls,
                         overs, extras_detail, batter_runs, batter_balls,
                         batter_fours, batter_sixes, batter_dismissal,
                         bowler_stats, lineup, target=None):
    clear()
    print_header()

    crr    = round((score/balls)*6, 2) if balls > 0 else 0.00
    ov_str = f"{balls//6}.{balls%6}"
    w_cnt  = extras_detail.get("w",0)
    lb_cnt = extras_detail.get("lb",0)
    nb_cnt = extras_detail.get("nb",0)
    total_x = w_cnt + lb_cnt + nb_cnt

    # Top box (Image 3 style)
    draw_box([
        f"  INNINGS COMPLETE: {batting_team}".ljust(38) + f"TOTAL: {score}/{wickets} ({ov_str} Overs)".rjust(36),
        f"  RUN RATE: {crr:.2f}".ljust(38) + f"EXTRAS: {total_x} (w{w_cnt}, lb{lb_cnt}, nb{nb_cnt})".rjust(36),
    ])
    print()

    # ── BATTING SUMMARY ────────────────────────────────────────────────
    print("  BATTING SUMMARY" + " " * 35 + "S/R")
    print("  " + "-" * 74)
    shown = 0
    for i, name in enumerate(lineup):
        r = batter_runs.get(i, 0)
        b = batter_balls.get(i, 0)
        if b == 0 and i > wickets: continue
        sr   = round((r/b)*100,1) if b > 0 else 0.0
        dis  = batter_dismissal.get(i, "not out")
        f4   = batter_fours.get(i, 0)
        s6   = batter_sixes.get(i, 0)
        bdry = f"[4x{f4}, 6x{s6}]"
        print(f"  {short(name):<16}  {dis:<24}  {r} ({b:02d})  {bdry:<12}  {sr:.1f}")
        shown += 1
    if shown == 0:
        print("  (no batters recorded)")
    print()

    # ── BOWLING SUMMARY ────────────────────────────────────────────────
    print("  BOWLING SUMMARY" + " " * 8 +
          "O".rjust(5) + "M".rjust(5) + "R".rjust(5) + "W".rjust(5) + "  ECON")
    print("  " + "-" * 62)
    for bname, bst in bowler_stats.items():
        if bst["balls"] == 0: continue
        ov  = f"{bst['balls']//6}.{bst['balls']%6}"
        eco = round((bst["runs"]/bst["balls"])*6,2) if bst["balls"]>0 else 0.00
        print(f"  {short(bname):<20}  {ov:>5}  {bst['maidens']:>3}  "
              f"{bst['runs']:>4}  {bst['wickets']:>4}  {eco:>7.2f}")
    print()

    # ── TARGET BOX (Image 3) ───────────────────────────────────────────
    if target is not None:
        rrr = round((target / (overs*6)) * 6, 2)
        draw_box(["",
                  f"   TARGET: {target} RUNS TO WIN  (REQUIRED RATE: {rrr:.2f})",
                  ""])
        print()
        input(">> PRESS [ENTER] TO START THE CHASE...")
    else:
        print()
        input(">> PRESS [ENTER] TO CONTINUE...")

# =========================
# INNINGS ENGINE
# =========================

def play_innings(overs, batting_team, bowling_team, user_is_batting,
                 pitch, weather, innings_num, target=None):
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

    bowler_stats = {}
    bowler_overs = {}
    last_bowler  = None
    max_quota    = max(1, overs // 5)
    current_bowler = pick_bowler(bowling_team, bowler_overs, max_quota)

    extras_detail    = {"w": 0, "lb": 0, "nb": 0}
    partnership_runs = 0
    free_hit         = False
    user_drs         = 1
    play_innings._comp_drs = 1  # computer's DRS review for this innings

    def ensure_bowler(name):
        if name not in bowler_stats:
            bowler_stats[name] = {"balls":0,"runs":0,"wickets":0,
                                   "maidens":0,"over_runs":[]}

    ensure_bowler(current_bowler)

    while balls < total_balls and wickets < 10:
        if target is not None and score >= target:
            break

        bst = bowler_stats[current_bowler]

        # ── RENDER ────────────────────────────────────────────────────
        render_play_screen(
            batting_team, bowling_team, score, wickets, overs, balls,
            innings_num, lineup, striker, non_striker,
            batter_runs, batter_balls, current_bowler, bowler_stats,
            over_log, partnership_runs, pitch, weather, target, free_hit
        )

        # ── COMMAND BAR ───────────────────────────────────────────────
        if user_is_batting:
            print("  COMMANDS: [←] Defend  |  [→] Swing  |  [↑] Loft  |  [↓] Leave")
        else:
            print("  COMMANDS: [←] In-swing  |  [→] Out-swing  |  [↑] Reverse  |  [↓] Bouncer")
        print("-" * 78)

        # ── INPUT ─────────────────────────────────────────────────────
        shot = delivery = None
        if user_is_batting:
            while shot is None:
                k = get_key()
                if   k in ("S","RIGHT"): shot = "SWING"
                elif k in ("D","LEFT"):  shot = "DEFEND"
                elif k in ("L","UP"):    shot = "LOFT"
                elif k in ("Q","DOWN"):  shot = "LEAVE"
            delivery = random.choice(["IN","OUT","REVERSE","BOUNCER"])
        else:
            while delivery is None:
                k = get_key()
                if   k in ("I","LEFT"):    delivery = "IN"
                elif k in ("O","RIGHT"):   delivery = "OUT"
                elif k in ("R","UP"):      delivery = "REVERSE"
                elif k in ("B","DOWN"):    delivery = "BOUNCER"
            shot = random.choices(["DEFEND","SWING","LOFT","LEAVE"],
                                   BOWL_SHOT_BIAS[delivery])[0]

        print()
        animate("  Bowler runs in...", delay=0.02)
        pause(0.35)

        # ── NO-BALL ───────────────────────────────────────────────────
        if (not free_hit) and random.random() < 0.04:
            animate(f"  {random.choice(COMMENTARY['NB'])}")
            score += 1; extras_detail["nb"] += 1
            bst["runs"] += 1; over_log.append("nb")
            free_hit = True; pause(0.9); continue

        # ── WIDE ──────────────────────────────────────────────────────
        if delivery in ["IN","BOUNCER"] and random.random() < 0.04:
            animate(f"  {random.choice(COMMENTARY['WD'])}")
            score += 1; extras_detail["w"] += 1
            bst["runs"] += 1; over_log.append("wd")
            pause(0.9); continue

        # ── OUTCOME ───────────────────────────────────────────────────
        result = compute_outcome(shot, lineup[striker], current_bowler,
                                  pitch, weather,
                                  batter_balls[striker], bst["balls"])

        if free_hit and result == "W":
            animate("  FREE HIT saves him — cannot be dismissed!")
            result = 0
        free_hit = False

        # ── WICKET ────────────────────────────────────────────────────
        if result == "W":
            animate(f"  {random.choice(COMMENTARY['W'])}")

            # DRS — batting side always challenges (user if batting, computer if bowling)
            overturned = False
            if user_is_batting:
                # USER is batting → user decides whether to review
                if user_drs > 0:
                    yn = input("  Challenge with DRS? (Y/N): ").strip().upper()
                    if yn == "Y":
                        user_drs -= 1
                        if random.random() < 0.35:
                            animate("  DRS: Replays show it's missing — NOT OUT!")
                            overturned = True
                        else:
                            animate("  DRS: Ball-tracking confirms — OUT stands!")
            else:
                # USER is bowling → COMPUTER (batting side) decides to review
                comp_drs = getattr(play_innings, '_comp_drs', 1)
                if comp_drs > 0 and random.random() < 0.40:
                    animate("  Computer reviews the decision...")
                    pause(0.8)
                    play_innings._comp_drs = comp_drs - 1
                    if random.random() < 0.35:
                        animate("  DRS: Replays show it's missing — NOT OUT!")
                        overturned = True
                    else:
                        animate("  DRS: Ball-tracking confirms — OUT stands!")

            if overturned:
                result = 0
                animate("  Batter survives!")
            else:
                fielders = [p for p in TEAMS[bowling_team] if p != current_bowler]
                fielder  = short(random.choice(fielders)) if fielders else "sub"
                wk       = short(TEAMS[bowling_team][min(6,len(TEAMS[bowling_team])-1)])
                dis_str  = random.choice(DISMISSAL_METHODS).format(
                    bowler=short(current_bowler), fielder=fielder, wk=wk)
                batter_dismissal[striker] = dis_str

                print(f"\n  {lineup[striker]}: {batter_runs[striker]}"
                      f"({batter_balls[striker]}b) — {dis_str}")
                pause(1.5)

                bst["wickets"]   += 1
                bst["balls"]     += 1
                bst["over_runs"].append("W")
                over_log.append("W")
                batter_balls[striker] += 1
                balls     += 1
                wickets   += 1
                partnership_runs = 0

                if wickets >= 10: break

                striker = wickets + 1
                batter_runs.setdefault(striker, 0)
                batter_balls.setdefault(striker, 0)

                if balls % 6 == 0 and balls > 0:
                    striker, non_striker = non_striker, striker
                    _close_over(current_bowler, bowler_stats, bowler_overs)
                    last_bowler    = current_bowler
                    current_bowler = pick_bowler(bowling_team, bowler_overs,
                                                  max_quota, last_bowler)
                    ensure_bowler(current_bowler)
                    over_log = []
                    animate(f"\n  --- END OF OVER {balls//6} ---")
                    pause(1.2)
                continue

        # ── RUNS ──────────────────────────────────────────────────────
        if isinstance(result, int):
            animate(f"  {random.choice(COMMENTARY.get(result, [str(result)+' run(s).']))}")
            score               += result
            bst["runs"]         += result
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

        # ── END OF OVER ────────────────────────────────────────────────
        if balls % 6 == 0 and balls > 0:
            striker, non_striker = non_striker, striker
            _close_over(current_bowler, bowler_stats, bowler_overs)
            last_bowler    = current_bowler
            current_bowler = pick_bowler(bowling_team, bowler_overs,
                                          max_quota, last_bowler)
            ensure_bowler(current_bowler)
            over_log = []
            animate(f"\n  --- END OF OVER {balls//6} ---")
            pause(1.2)

        if target is not None and score >= target:
            break

    # ── INNINGS SUMMARY ───────────────────────────────────────────────
    show_innings_summary(
        batting_team, bowling_team, score, wickets, balls, overs,
        extras_detail, batter_runs, batter_balls,
        batter_fours, batter_sixes, batter_dismissal,
        bowler_stats, lineup, target
    )
    return score, wickets, balls, bowler_stats, batter_runs, batter_balls

def _close_over(bowler, bowler_stats, bowler_overs):
    if bowler not in bowler_stats: return
    bst = bowler_stats[bowler]
    if bst["over_runs"] and all(r in ["0","W","•"] for r in bst["over_runs"]):
        bst["maidens"] += 1
    bst["over_runs"] = []
    bowler_overs[bowler] = bowler_overs.get(bowler, 0) + 1

# =========================
# PLAYER OF THE MATCH
# =========================

def pick_potm(t1, t2, br1, bb1, bs1, br2, bb2, bs2):
    candidates = []
    for i, name in enumerate(TEAMS[t1]):
        sc = br1.get(i,0) + bs1.get(name,{}).get("wickets",0)*25
        candidates.append((sc, name, t1, bs1))
    for i, name in enumerate(TEAMS[t2]):
        sc = br2.get(i,0) + bs2.get(name,{}).get("wickets",0)*25
        candidates.append((sc, name, t2, bs2))
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0] if candidates else (0,"Unknown","",{})

# =========================
# FINAL RESULT SCREEN  (Image 4)
# =========================

def show_final_result(player_team, t1, s1, w1, b1,
                              t2, s2, w2, b2, overs,
                      bs1, br1, bb1, bs2, br2, bb2, history):
    clear()
    print_header()

    target = s1 + 1

    # ── WIN MESSAGE BOX ───────────────────────────────────────────────
    if s2 >= target:
        wkts_left = 10 - w2
        balls_rem  = overs * 6 - b2
        ovs_rem    = f"{balls_rem//6}.{balls_rem%6}"
        msg = f"  \U0001f389  {t2} WIN BY {wkts_left} WICKET(S)  ({ovs_rem} OVERS REMAINING)  \U0001f389"
        winner = t2
    elif s2 == s1:
        msg    = "  \U0001f3c6  IT'S A TIE! WHAT A MATCH!  \U0001f3c6"
        winner = "Tie"
    else:
        margin = s1 - s2
        msg    = f"  \U0001f389  {t1} WIN BY {margin} RUN(S)  \U0001f389"
        winner = t1

    draw_box(["", msg, ""])
    print()

    # ── FINAL RECAP ───────────────────────────────────────────────────
    rr1 = round((s1/(b1 if b1 else 1))*6, 2)
    rr2 = round((s2/(b2 if b2 else 1))*6, 2)
    ov1 = f"{b1//6}.{b1%6}"
    ov2 = f"{b2//6}.{b2%6}"

    print("  FINAL RECAP")
    print("  " + "-" * 70)
    print(f"  \U0001f3cf 1ST INNINGS ({t1}):   {s1}/{w1} ({ov1})   |  RR: {rr1}")
    print(f"  \U0001f3cf 2ND INNINGS ({t2}):   {s2}/{w2} ({ov2})   |  RR: {rr2}")
    print()

    # ── PLAYER OF THE MATCH ───────────────────────────────────────────
    potm_sc, potm_name, potm_team, potm_bst_dict = pick_potm(
        t1, t2, br1, bb1, bs1, br2, bb2, bs2)
    potm_bst = potm_bst_dict.get(potm_name, {})
    potm_idx = TEAMS.get(potm_team,[]).index(potm_name) \
               if potm_name in TEAMS.get(potm_team,[]) else 0
    potm_runs  = (br1 if potm_team==t1 else br2).get(potm_idx, 0)
    potm_bals  = (bb1 if potm_team==t1 else bb2).get(potm_idx, 0)
    potm_wkts  = potm_bst.get("wickets", 0)

    print("  \U0001f947 PLAYER OF THE MATCH")
    print("  " + "-" * 70)
    print(f"  >> {short(potm_name)} ({potm_team})")
    if potm_bst.get("balls",0) > 0:
        ov_s = f"{potm_bst['balls']//6}.{potm_bst['balls']%6}"
        print(f"  >> PERFORMANCE: {ov_s} - {potm_bst.get('maidens',0)} - "
              f"{potm_bst.get('runs',0)} - {potm_wkts}")
    else:
        print(f"  >> PERFORMANCE: {potm_runs} runs ({potm_bals} balls)")
    print()

    # ── LEADERS ───────────────────────────────────────────────────────
    print("  " + "-" * 70)
    all_bat = []
    for i, name in enumerate(TEAMS[t1]): all_bat.append((br1.get(i,0), bb1.get(i,0), name))
    for i, name in enumerate(TEAMS[t2]): all_bat.append((br2.get(i,0), bb2.get(i,0), name))
    all_bat.sort(key=lambda x: x[0], reverse=True)

    all_bowl = []
    for name, bst in {**bs1, **bs2}.items():
        if bst.get("balls",0) > 0:
            all_bowl.append((bst["wickets"], bst["runs"], bst["balls"], name))
    all_bowl.sort(key=lambda x: (-x[0], x[1]))

    left_rows  = ["[ BATTING LEADERS ]", "─"*28]
    right_rows = ["[ BOWLING LEADERS ]", "─"*28]
    for r, b, name in all_bat[:3]:
        left_rows.append(f"  {short(name):<18}  {r} ({b})")
    for wk, rns, bls, name in all_bowl[:3]:
        right_rows.append(f"  {short(name):<18}  {wk}/{rns}")

    mx = max(len(left_rows), len(right_rows))
    left_rows  += [""] * (mx - len(left_rows))
    right_rows += [""] * (mx - len(right_rows))
    for ll, rl in zip(left_rows, right_rows):
        print(f"  {ll:<35}  {rl}")
    print()

    # ── OPTIONS ───────────────────────────────────────────────────────
    print("-" * 78)
    print("  OPTIONS: [R]eplay  |  [Q]uit to Menu")
    print("-" * 78)
    print()

    history.append(f"{t1} {s1}/{w1}  vs  {t2} {s2}/{w2}  —  {winner} won")

    while True:
        choice = input(">> SELECT OPTION: ").strip().upper()
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
    history = []
    while True:
        action = main_menu()

        if action == "records":
            show_records(history)
            continue

        # Select overs
        clear(); print_header(); print()
        while True:
            try:
                overs = int(input("  Select overs (5 / 10 / 20): "))
                if overs in [5, 10, 20]: break
                else: print("  Choose 5, 10, or 20.")
            except ValueError: print("  Invalid input.")

        player, computer = choose_team()
        pitch, weather   = setup_conditions()
        user_bats_first  = toss(player, computer)

        t1 = player   if user_bats_first else computer
        t2 = computer if user_bats_first else player

        # ── INNINGS 1 ─────────────────────────────────────────────────
        clear(); print_header()
        animate(f"\n  {t1} will BAT FIRST\n")
        input(">> PRESS [ENTER] TO START THE INNINGS...")
        s1,w1,b1,bs1,br1,bb1 = play_innings(
            overs, t1, t2, t1==player, pitch, weather, 1)

        # ── INNINGS 2 ─────────────────────────────────────────────────
        target = s1 + 1
        clear(); print_header()
        animate(f"\n  {t2} need {target} to win\n")
        input(">> PRESS [ENTER] TO START THE CHASE...")
        s2,w2,b2,bs2,br2,bb2 = play_innings(
            overs, t2, t1, t2==player, pitch, weather, 2, target)

        # ── RESULT ────────────────────────────────────────────────────
        action = show_final_result(
            player, t1,s1,w1,b1, t2,s2,w2,b2, overs,
            bs1,br1,bb1, bs2,br2,bb2, history
        )
        if action == "menu":
            continue

main()