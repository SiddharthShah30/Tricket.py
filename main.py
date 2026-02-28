import random
import os
import time

# The Utility Functions

def clear():
    os.system("cls" if os.name == 'nt' else 'clear')
def animate(text, delay = 0.02):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def pause(sec=1):
    time.sleep(sec)

# The UI

def print_header():
    print("-" * 78)
    print("TRICKET")
    print("-" * 78)

def print_scoreboard(score, wickets, overs, balls, target=None):
    total_balls = overs * 6
    current_over = balls // 6
    current_ball = balls % 6

    crr = round((score / balls) * 6, 2) if balls > 0 else 0

    if target:
        runs_needed = target - score
        balls_left = total_balls - balls
        rrr = round((runs_needed / balls_left) * 6, 2) if balls_left > 0 else 0
    else:
        rrr = 0
    
    print (f"TEAM: {score}/{wickets} ({current_over}.{current_ball})", end="")
    if target:
        print(f"      TARGET: {target}")
        print(f"CRR: {crr}      RRR: {rrr}")
    else:
        print()
        print(f"CRR:  {crr}")
    
    print("-" * 78)

def print_commands(user_batting):
    if user_batting:
        print("BATTING OPTION: ")
        print("[S]wing  [D]efend  [L]oft  [Q]Leave")
    else:
        print("BOWLING OPTIONS: ")
        print("[I]n-Swing  [O]ut-Swing  [R]everse-Swing [B]ouncer")
    
    print("-" * 78)

# Game Logic

def toss():
    clear()
    print_header()
    animate("=== TOSS TIME ===")
    call = input("Heads or Tails? ").lower()
    result = random.choice(["heads", "tails"])
    animate(f"Toss Result: {result}")
    pause(1)

    if call == result:
        choice = input("You won! Bat or Bowl? ").lower()
        return choice == "bat"
    else:
        comp_choice = random.choice(["bat", "bowl"])
        animate(f"Computer chose to {comp_choice}")
        return comp_choice != "bat"

def batting_outcome(shot, bowl_type):
    if shot == "D":
        return random.choices([0, 1, "W"], [60, 30, 10])[0]
    if shot == "S":
        return random.choices([0, 1, 2, 4, "W"], [20, 25, 25, 20, 10])[0]
    if shot == "L":
        return random.choices([0, 4, 6, "W"], [15, 40, 30, 15])[0]
    if shot == "E":
        if bowl_type in ["I", "O", "R"]:
            return random.choices([0, "W"], [85, 15])[0]
        if bowl_type == "B":
            return random.choices([0, "WD"], [70, 30])[0]

def play_innings(overs, user_batting, target=None):
    score = 0
    wickets = 0
    balls = 0
    over_log = []

    total_balls = overs * 6

    while balls < total_balls and wickets < 10:

        clear()
        print_header()
        print_scoreboard(score, wickets, overs, balls, target)

        print("THIS OVER:"," ".join(over_log))
        print("-" * 78)

        print_commands(user_batting)

        if user_batting:
            shot = input("Choose Shot: ").upper()
            if shot == 'Q':
                exit()
            if shot not in ['S', 'D', 'L', 'E']:
                shot = 'S'
            bowl_type = random.choice(['I', 'O', 'R', 'B'])
        else:
            bowl_type = input("Choose Delivery: ").upper()
            if bowl_type not in ['I', 'O', 'R', 'B']:
                bowl_type = 'I'
            shot = random.choice(['S', 'D', 'L', 'E'])
        
        animate("Bowler runs in...")
        pause(int(0.5))

        result = batting_outcome(shot, bowl_type)

        if result == "W":
            animate("WICKET !!!")
            wickets += 1
            over_log.append("[W]")
        elif result == "WD":
            animate("Wide Ball!")
            score += 1
            over_log.append("[WD]")
            continue
        elif isinstance(result, int):
            animate(f"{result} runs(s)!")
            score += result
            over_log.append(f"[{result}]")
        
        balls += 1

        if balls % 6 == 0:
            over_log = []
            animate("END OF OVER")
            pause(1)
        
        if target and score >= target:
            break

        pause(1)
    
    return score

# Main Game

def main():
    overs = int(input("Choose overs 1, 5, 10, 20, 50: "))
    user_batting_first = toss()

    first_score = play_innings(overs, user_batting_first)

    target = first_score + 1

    animate(f"Target: {target}")
    pause(2)

    second_score = play_innings(overs, not user_batting_first, target)

    clear()
    print_header()

    print(f"FIRST INNINGS: {first_score}")
    print(f"SEONCD INNINGS: {second_score}")
    print("-" * 78)

    if second_score >= target:
        if user_batting_first:
            print("COMPUTER WINS !!!")
        else:
            print("YOU WIN !!!")
    else:
        if user_batting_first:
            print("YOU WIN !!!")
        else:
            print("COMPUTER WINS !!!")

main()