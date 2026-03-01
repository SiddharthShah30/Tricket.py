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

# =========================
# UTILITIES
# =========================

def clear():
    os.system("cls" if os.name == 'nt' else 'clear')

def animate(text, delay=0.04):
    for c in text:
        print(c, end='', flush=True)
        time.sleep(delay)
    print()

def pause(sec=1.5):
    time.sleep(sec)

# =========================
# ARROW KEY READER
# =========================

def get_arrow_key():
    if os.name == 'nt':
        import msvcrt
        while True:
            key = msvcrt.getch()
            if key == b'\xe0':
                key2 = msvcrt.getch()
                if key2 == b'K': return "LEFT"
                if key2 == b'M': return "RIGHT"
                if key2 == b'H': return "UP"
                if key2 == b'P': return "DOWN"
            elif key == b'\x1b':
                return "ESC"
    else:
        import tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(3)
            if key == '\x1b[A': return "UP"
            if key == '\x1b[B': return "DOWN"
            if key == '\x1b[C': return "RIGHT"
            if key == '\x1b[D': return "LEFT"
            if key[0] == '\x1b' and len(key) == 1: return "ESC"
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

# =========================
# TEAM SELECTION
# =========================

def choose_team():
    teams = list(TEAMS.keys())
    clear()
    print_header()
    print("\nSelect Your Team:\n")
    for i, t in enumerate(teams, 1):
        print(f"  {i:>2}. {t}")
    print()

    while True:
        try:
            choice = int(input("Enter number: "))
            if 1 <= choice <= len(teams):
                player = teams[choice - 1]
                break
            else:
                print("Please enter a number from the list.")
        except ValueError:
            print("Invalid input. Enter a number.")

    remaining = [t for t in teams if t != player]
    computer = random.choice(remaining)

    print(f"\nYour team  : {player}")
    print(f"Opponent   : {computer}")
    pause(1.5)

    return player, computer

# =========================
# UI
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

def print_scoreboard(score, wickets, overs, balls, batting_team, bowling_team, target=None):
    total_balls = overs * 6
    current_over = balls // 6
    current_ball = balls % 6
    crr = round((score / balls) * 6, 2) if balls > 0 else 0.00

    print(f"\n  {batting_team}: {score}/{wickets}  ({current_over}.{current_ball} ov)", end="")

    if target is not None:
        runs_needed = target - score
        balls_left = total_balls - balls
        rrr = round((runs_needed / balls_left) * 6, 2) if balls_left > 0 else 0.00
        print(f"      TARGET: {target}")
        print(f"  CRR: {crr:<8} RRR: {rrr}")
        print(f"  Need {runs_needed} run(s) in {balls_left} ball(s)")
    else:
        print()
        print(f"  CRR: {crr}")

    print("-" * 78)
    print(f"  BATTING : {batting_team}")
    print(f"  BOWLING : {bowling_team}")
    print("-" * 78)

# =========================
# TOSS
# =========================

def toss(player, computer):
    clear()
    print_header()
    print("\n  === TOSS ===\n")

    while True:
        call = input("  Call Heads or Tails (H/T): ").strip().lower()
        if call in ["h", "heads"]:
            user_call = "heads"
            break
        elif call in ["t", "tails"]:
            user_call = "tails"
            break
        else:
            print("  Invalid input. Type H or T.")

    result = random.choice(["heads", "tails"])
    print(f"\n  Coin flips...")
    pause(1)
    print(f"  Result: {result.upper()}!")
    pause(1)

    if user_call == result:
        print(f"\n  You won the toss!\n")
        while True:
            choice = input("  Bat or Bowl? (bat/bowl): ").strip().lower()
            if choice in ["bat", "b"]:
                print(f"\n  {player} will BAT first.")
                pause(1)
                return True
            elif choice in ["bowl", "bo"]:
                print(f"\n  {player} will BOWL first.")
                pause(1)
                return False
            else:
                print("  Invalid choice. Type 'bat' or 'bowl'.")
    else:
        comp_choice = random.choice(["bat", "bowl"])
        print(f"\n  {computer} won the toss and chose to {comp_choice}.")
        pause(1.5)
        return comp_choice != "bat"

# =========================
# BATTING LOGIC
# =========================

# Each delivery type biases which shot the computer picks,
# which in turn determines the run/wicket outcome.
#
# Delivery  → Forced tendency          → Effect
# IN        → tucked up, forced DEFEND → more dots/wickets, fewer boundaries
# OUT       → drives hard, forced SWING → more runs but wicket risk
# REVERSE   → confused, forced LEAVE   → most wicket-prone delivery
# BOUNCER   → tempted to LOFT          → big boundary or wicket gamble

BOWL_SHOT_BIAS = {
    #              DEFEND  SWING  LOFT  LEAVE
    "IN":         [55,     20,    5,    20],   # cramps batsman → defensive/leave
    "OUT":        [15,     50,    20,   15],   # full delivery → drives
    "REVERSE":    [20,     15,    10,   55],   # late movement → leaves/plays-on
    "BOUNCER":    [10,     20,    55,   15],   # short ball → tempts the pull
}

SHOT_OUTCOMES = {
    "DEFEND": ([0, 1, "W"],          [60, 30, 10]),
    "SWING":  ([0, 1, 2, 4, "W"],   [20, 25, 25, 20, 10]),
    "LOFT":   ([0, 4, 6, "W"],      [15, 40, 30, 15]),
    "LEAVE":  ([0, "W"],             [85, 15]),
}

def batting_outcome(delivery):
    """Used when USER is bowling — delivery biases computer's shot selection."""
    bias = BOWL_SHOT_BIAS[delivery]
    shot = random.choices(["DEFEND", "SWING", "LOFT", "LEAVE"], bias)[0]
    outcomes, weights = SHOT_OUTCOMES[shot]
    return random.choices(outcomes, weights)[0]

def batting_outcome_batting(shot):
    """Used when USER is batting — shot choice goes straight to outcome."""
    outcomes, weights = SHOT_OUTCOMES[shot]
    return random.choices(outcomes, weights)[0]

# =========================
# INNINGS ENGINE
# =========================

def play_innings(overs, batting_team, bowling_team, user_is_batting, target=None):
    lineup = TEAMS[batting_team]

    striker = 0
    non_striker = 1
    score = 0
    wickets = 0
    balls = 0
    over_log = []
    total_balls = overs * 6

    while balls < total_balls and wickets < 10:

        # Check win condition mid-innings (chasing)
        if target is not None and score >= target:
            break

        clear()
        print_header()
        print_scoreboard(score, wickets, overs, balls, batting_team, bowling_team, target)

        print(f"\n  STRIKER     : {lineup[striker]}")
        print(f"  NON-STRIKER : {lineup[non_striker]}")
        print(f"\n  THIS OVER   : {' '.join(over_log) if over_log else '-'}")
        print("-" * 78)

        shot = None
        delivery = None

        if user_is_batting:
            print("\n  [ ← DEFEND ]  [ → SWING ]  [ ↑ LOFT ]  [ ↓ LEAVE ]\n")
            while shot is None:
                key = get_arrow_key()
                if key == "LEFT":   shot = "DEFEND"
                elif key == "RIGHT": shot = "SWING"
                elif key == "UP":    shot = "LOFT"
                elif key == "DOWN":  shot = "LEAVE"
                elif key == "ESC":
                    input("\n  Paused. Press Enter to continue...")
                    clear()
                    print_header()
                    print_scoreboard(score, wickets, overs, balls, batting_team, bowling_team, target)
                    print(f"\n  STRIKER     : {lineup[striker]}")
                    print(f"  NON-STRIKER : {lineup[non_striker]}")
                    print(f"\n  THIS OVER   : {' '.join(over_log) if over_log else '-'}")
                    print("-" * 78)
                    print("\n  [ ← DEFEND ]  [ → SWING ]  [ ↑ LOFT ]  [ ↓ LEAVE ]\n")

        else:
            print("\n  [ ← IN ]  [ → OUT ]  [ ↑ REVERSE ]  [ ↓ BOUNCER ]\n")
            delivery = None
            while delivery is None:
                key = get_arrow_key()
                if key == "LEFT":    delivery = "IN"
                elif key == "RIGHT": delivery = "OUT"
                elif key == "UP":    delivery = "REVERSE"
                elif key == "DOWN":  delivery = "BOUNCER"
                elif key == "ESC":
                    input("\n  Paused. Press Enter to continue...")
                    clear()
                    print_header()
                    print_scoreboard(score, wickets, overs, balls, batting_team, bowling_team, target)
                    print(f"\n  STRIKER     : {lineup[striker]}")
                    print(f"  NON-STRIKER : {lineup[non_striker]}")
                    print(f"\n  THIS OVER   : {' '.join(over_log) if over_log else '-'}")
                    print("-" * 78)
                    print("\n  [ ← IN ]  [ → OUT ]  [ ↑ REVERSE ]  [ ↓ BOUNCER ]\n")

        print()
        animate("  Bowler runs in...")
        pause(0.6)
        if user_is_batting:
            animate("  Ball delivered!")
        else:
            animate(f"  Bowls a {delivery} delivery!")
        pause(0.4)

        result = batting_outcome(delivery) if not user_is_batting else batting_outcome_batting(shot)

        if result == "W":
            print()
            animate(f"  WICKET! {lineup[striker]} is OUT!")
            over_log.append("W")
            wickets += 1
            balls += 1
            pause(2)

            if wickets >= 10:
                break

            striker = wickets + 1

        elif isinstance(result, int):
            print()
            if result == 0:
                animate("  Dot ball. No run.")
            elif result == 4:
                animate("  FOUR! Cracking shot!")
            elif result == 6:
                animate("  SIX! Right out of the ground!")
            else:
                animate(f"  {result} run(s).")
            over_log.append(str(result))
            score += result
            balls += 1
            pause(1.2)

            if result % 2 == 1:
                striker, non_striker = non_striker, striker

        # End of over
        if balls % 6 == 0 and balls > 0:
            striker, non_striker = non_striker, striker
            over_log = []
            print()
            animate(f"  --- END OF OVER {balls // 6} ---")
            pause(1.5)

    return score

# =========================
# MAIN
# =========================

def main():
    clear()
    print_header()
    print()

    while True:
        try:
            overs = int(input("  Select overs (1 / 5 / 10 / 20): "))
            if overs in [1, 5, 10, 20]:
                break
            else:
                print("  Please choose 1, 5, 10, or 20.")
        except ValueError:
            print("  Invalid input. Enter a number.")

    player, computer = choose_team()
    user_bats_first = toss(player, computer)

    # ---- INNINGS 1 ----
    if user_bats_first:
        clear()
        print_header()
        animate(f"\n  {player} batting first...\n")
        pause(1)
        first_score = play_innings(overs, player, computer, True)

        clear()
        print_header()
        print(f"\n  Innings Over!")
        print(f"  {player}: {first_score}")
        target = first_score + 1
        print(f"  {computer} need {target} to win.\n")
        pause(2)

        second_score = play_innings(overs, computer, player, False, target)

    else:
        clear()
        print_header()
        animate(f"\n  {computer} batting first...\n")
        pause(1)
        first_score = play_innings(overs, computer, player, False)

        clear()
        print_header()
        print(f"\n  Innings Over!")
        print(f"  {computer}: {first_score}")
        target = first_score + 1
        print(f"  {player} need {target} to win.\n")
        pause(2)

        second_score = play_innings(overs, player, computer, True, target)

    # ---- RESULT ----
    clear()
    print_header()
    print("\n" + "=" * 78)
    print("  MATCH RESULT")
    print("=" * 78)

    if user_bats_first:
        print(f"\n  {player:<20}: {first_score}")
        print(f"  {computer:<20}: {second_score}")
        print()
        if second_score >= target:
            animate(f"  {computer} wins! Better luck next time.")
        else:
            animate(f"  {player} wins! Well played!")
    else:
        print(f"\n  {computer:<20}: {first_score}")
        print(f"  {player:<20}: {second_score}")
        print()
        if second_score >= target:
            animate(f"  {player} wins! Well played!")
        else:
            animate(f"  {computer} wins! Better luck next time.")

    if second_score == first_score:
        animate("  It's a TIE! What a match!")

    print("\n" + "=" * 78)
    print()

main()