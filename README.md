# Triket Simulator

A fully-featured, terminal-based cricket simulation game written in Python. Play international matches across 5, 10, or 20-over formats with real player rosters, dynamic pitch and weather conditions, a DRS system, confidence mechanics, and full scorecards — all from your command line.

---

## Table of Contents

* [Features](#features)
* [Installation](#installation)
* [Usage](#usage)
* [How to Play](#how-to-play)
* [Game Mechanics](#game-mechanics)
* [Teams](#teams)
* [Tech Stack](#tech-stack)
* [Contributing](#contributing)
* [License](#license)

---

## Features

* **10 international teams** with real player lineups and individually tuned stats
* **Arrow key controls** — no typing mid-game, fully keyboard-driven
* **Player attributes** — each player has bat skill, aggression, bowl skill, bowl type, and stamina ratings that affect outcomes
* **Confidence mechanic** — new batters are vulnerable; set batters score freely and are harder to dismiss
* **Delivery-biased shot system** — your bowling type shifts the computer's shot selection
* **Dynamic pitch & weather conditions** — Flat, Green Top, Dusty, and Slow pitches combined with Sunny, Overcast, Humid, and Windy weather all affect outcomes
* **DRS system** — challenge LBW and caught-behind decisions; 1 review per innings for each side
* **Bowler management** — choose your own bowler each over, with quota limits and consecutive-over restrictions enforced
* **Free hits** — no-balls trigger a free hit on the next delivery
* Named batsmen displayed at the crease (striker and non-striker) with live run and ball counts
* Automatic batting rotation on odd runs and at the end of each over
* Live scoreboard with CRR, RRR, runs needed, and balls remaining
* Over-by-over ball log displayed in real time
* Full innings scorecard — batting and bowling figures shown after each innings
* **Player of the Match** awarded based on match performance
* Coin toss with bat/bowl election
* Tie detection alongside win/loss results
* Animated text and timed output for an immersive feel
* Match history saved for the current session
* Supports **5, 10, and 20 over** formats

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/cli-cricket-simulator.git
cd cli-cricket-simulator
```

### 2. Ensure Python is installed

Python 3.7+ is required. No external libraries are needed.

```bash
python --version
```

### 3. Run the game

```bash
python cricket.py
```

> **Linux/macOS note:** Arrow key input uses `tty` and `termios` from the standard library — run in a proper terminal (not an IDE console) for best results.

---

## Usage

On launch, select your over format:

```
Select overs (5 / 10 / 20):
```

Then choose your team from the numbered list, call the toss, and play.

---

## How to Play

### Team Selection

Pick one of 10 international teams. The computer randomly selects its opponent from the remaining nine.

---

### Toss

```
Call Heads or Tails (H/T):
```

Win the toss and choose to **Bat** or **Bowl**. Lose it and the computer decides.

---

### Batting Controls (when your team bats)

Use arrow keys to select your shot each ball:

| Key | Shot   | Tendency                             |
|-----|--------|--------------------------------------|
| `←` | Defend | Safe — dots and singles, low risk    |
| `→` | Swing  | Balanced — singles, twos, fours      |
| `↑` | Loft   | Aggressive — fours and sixes, risky  |
| `↓` | Leave  | Watchful — mostly dots, some wickets |

---

### Bowling Controls (when your team bowls)

**Pace bowlers:**

| Key | Delivery  | Effect on Computer's Batting                            |
|-----|-----------|---------------------------------------------------------|
| `←` | In-Swing  | Cramps the batter — more dots/wickets, fewer boundaries |
| `→` | Out-Swing | Full ball — tempts drives, more runs                    |
| `↑` | Yorker    | Hard to score off — lots of dot balls                   |
| `↓` | Bouncer   | Short ball — tempts the pull, six or wicket             |

**Spin bowlers:**

| Key | Delivery | Effect on Computer's Batting                    |
|-----|----------|-------------------------------------------------|
| `←` | Off-Spin | Turns in — batter defends or drives             |
| `→` | Leg-Spin | More temptation to drive, higher run risk       |
| `↑` | Flipper  | Skids through — hard to score                   |
| `↓` | Googly   | Mystery ball — batter often leaves or misjudges |

Your delivery biases the computer's shot selection, which then determines the outcome.

---

### Bowler Selection

At the start of each over when you're bowling, you'll be shown a selection screen listing eligible bowlers with their current spell figures, overs remaining, and bowling type. No bowler can bowl consecutive overs, and each bowler has a maximum quota of **total overs ÷ 5**.

---

### DRS

When a batter is given out LBW or caught behind, you'll be offered a DRS review. You have **1 review per innings**. There is a 35% chance of an overturn. The computer also has 1 review and may use it after one of its batters is dismissed.

---

### Scoreboard

```
  India: 142/4  (17.3)          TARGET: 187  (RR: 8.23, RRR: 9.18)

  BATTING: India                    BOWLING: Australia

  STRIKER  : Shreyas Iyer   54 (38)    BOWLER: M. Starc  28-2 (3.0)
  NON-STR  : Hardik Pandya  21 (14)    OVER:   1  4  0  W  6

  THIS OVER:  [ 1 ]  [ 4 ]  [ 0 ]  [ W ]  [ 6 ]

  >> 45 RUNS REMAINING OFF 15 BALLS
  >> CURRENT PARTNERSHIP: 31 runs
```

---

## Game Mechanics

### Confidence System

A batter's time at the crease directly affects their performance:

| Balls Faced | State    | Effect                                           |
|-------------|----------|--------------------------------------------------|
| 0–5         | Nervous  | Higher wicket risk, subdued scoring              |
| 6–15        | Settling | Risk fading back to baseline                     |
| 16–30       | Set      | Noticeably harder to dismiss, scores more freely |
| 31+         | Dominant | Very hard to remove, scoring prolifically        |

### Delivery → Shot Bias (when you bowl)

Each delivery shifts the probability of the computer choosing a particular shot:

| Delivery  | DEFEND | SWING | LOFT | LEAVE |
|-----------|--------|-------|------|-------|
| In-Swing  | 55%    | 20%   | 5%   | 20%   |
| Out-Swing | 15%    | 50%   | 20%  | 15%   |
| Yorker    | 40%    | 30%   | 5%   | 25%   |
| Bouncer   | 10%    | 20%   | 55%  | 15%   |
| Off-Spin  | 45%    | 25%   | 15%  | 15%   |
| Leg-Spin  | 30%    | 35%   | 20%  | 15%   |
| Flipper   | 50%    | 20%   | 10%  | 20%   |
| Googly    | 25%    | 20%   | 20%  | 35%   |

### Shot → Outcome Probabilities (base rates, modified by player stats)

| Shot   | 0   | 1   | 2   | 4   | 6   | W   |
|--------|-----|-----|-----|-----|-----|-----|
| Defend | 65% | 32% | —   | —   | —   | 3%  |
| Swing  | 22% | 28% | 24% | 20% | —   | 6%  |
| Loft   | 18% | —   | —   | 38% | 32% | 12% |
| Leave  | 92% | —   | —   | —   | —   | 8%  |

### Pitch Conditions

| Pitch     | Effect                                |
|-----------|---------------------------------------|
| Flat      | Batting paradise — high scores likely |
| Green Top | Pace bowlers dominate                 |
| Dusty     | Spin bowlers thrive                   |
| Slow      | Hard to time; scoring suppressed      |

### Weather Conditions

| Weather  | Effect                                 |
|----------|----------------------------------------|
| Sunny    | Minimal movement                       |
| Overcast | Significant swing for pace bowlers     |
| Humid    | Some extra movement expected           |
| Windy    | Slight movement in the air             |

### Innings End Conditions

An innings ends when any of these occur:

* All allocated balls are bowled
* 10 wickets fall
* The target is reached (second innings only)

---

## Teams

| Team         | Notable Players                                   |
|--------------|---------------------------------------------------|
| India        | Rohit Sharma, Virat Kohli, Jasprit Bumrah         |
| Australia    | Steve Smith, Pat Cummins, Mitchell Starc          |
| England      | Ben Stokes, Jos Buttler, Jofra Archer             |
| New Zealand  | Kane Williamson, Trent Boult, Tim Southee         |
| South Africa | Kagiso Rabada, Quinton de Kock, David Miller      |
| Pakistan     | Babar Azam, Shaheen Afridi, Mohammad Rizwan       |
| Sri Lanka    | Wanindu Hasaranga, Pathum Nissanka, Kusal Mendis  |
| West Indies  | Andre Russell, Nicholas Pooran, Alzarri Joseph    |
| Bangladesh   | Shakib Al Hasan, Taskin Ahmed, Litton Das         |
| Afghanistan  | Rashid Khan, Mujeeb Ur Rahman, Ibrahim Zadran     |

Each team has a full 11-player lineup. Batters are displayed by name at the crease and rotate through the batting order as wickets fall.

---

## Tech Stack

* **Python 3.7+**
* **Standard library only** — `os`, `sys`, `random`, `time`, `tty`, `termios` (Linux/macOS), `msvcrt` (Windows)

Cross-platform arrow key input is handled natively — no external packages required.

---

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes
4. Open a pull request

Ideas for improvement: tournament/series mode, a difficulty setting that adjusts computer shot selection, player form ratings, save/load match history, or a stats leaderboard across sessions.

---

## License

MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
