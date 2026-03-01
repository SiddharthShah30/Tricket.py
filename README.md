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

* **10 international teams** with real player lineups
* **Arrow key controls** — no typing mid-game, fully keyboard-driven
* **Delivery-biased shot system** — bowling type influences how the computer bats
* Named batsmen displayed at the crease (striker and non-striker)
* Automatic batting rotation on odd runs and at end of overs
* Live scoreboard with CRR, RRR, runs needed, and balls remaining
* Over-by-over ball log displayed in real time
* In-game **ESC pause** to take a breather
* Coin toss with bat/bowl election
* Tie detection alongside win/loss results
* Animated text and timed output for an immersive feel
* Supports **1, 5, 10, and 20 over** formats

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/tricket.git
cd tricket
```

### 2. Ensure Python is installed

Python 3.6+ is required. No external libraries are needed.

```bash
python --version
```

### 3. Run the game

```bash
python main.py
```

> **Linux/macOS note:** Arrow key input uses `tty` and `termios` from the standard library — run in a proper terminal (not an IDE console) for best results.

---

## Usage

On launch, select your over format:

```
Select overs (1 / 5 / 10 / 20):
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

| Key | Shot    | Tendency                              |
|-----|---------|---------------------------------------|
| `←` | Defend  | Safe — dots and singles, low risk     |
| `→` | Swing   | Balanced — singles, twos, fours       |
| `↑` | Loft    | Aggressive — fours and sixes, risky   |
| `↓` | Leave   | Watchful — mostly dots, some wickets  |

The computer bowls a random delivery type each ball, which does **not** affect your outcome when batting — your shot choice alone drives the result.

---

### Bowling Controls (when your team bowls)

Use arrow keys to select your delivery each ball:

| Key | Delivery       | Effect on Computer's Batting          |
|-----|----------------|---------------------------------------|
| `←` | In-Swing       | Cramps the batsman — more dots/wickets, fewer boundaries |
| `→` | Out-Swing      | Full ball — tempts drives, more runs  |
| `↑` | Reverse-Swing  | Late movement — most wicket-prone     |
| `↓` | Bouncer        | Short ball — tempts the pull, six or wicket |

Your delivery biases the computer's shot selection, which then determines the outcome.

---

### Pause

Press `ESC` at any point during ball selection to pause. Press `Enter` to resume.

---

### Scoreboard

```
  India: 142/4  (17.3 ov)      TARGET: 187
  CRR: 8.23      RRR: 9.18
  Need 45 run(s) in 15 ball(s)

  BATTING : India
  BOWLING : Australia

  STRIKER     : Shreyas Iyer
  NON-STRIKER : Hardik Pandya

  THIS OVER   : 1 4 0 W 6
```

---

## Game Mechanics

### Delivery → Shot Bias (when you bowl)

Each delivery type shifts the probability of the computer choosing a particular shot:

| Delivery      | DEFEND | SWING | LOFT | LEAVE |
|---------------|--------|-------|------|-------|
| In-Swing      | 55%    | 20%   | 5%   | 20%   |
| Out-Swing     | 15%    | 50%   | 20%  | 15%   |
| Reverse-Swing | 20%    | 15%   | 10%  | 55%   |
| Bouncer       | 10%    | 20%   | 55%  | 15%   |

### Shot → Outcome Probabilities

| Shot   | 0   | 1   | 2   | 4   | 6   | W   |
|--------|-----|-----|-----|-----|-----|-----|
| Defend | 60% | 30% | —   | —   | —   | 10% |
| Swing  | 20% | 25% | 25% | 20% | —   | 10% |
| Loft   | 15% | —   | —   | 40% | 30% | 15% |
| Leave  | 85% | —   | —   | —   | —   | 15% |

### Batting Rotation

* Batsmen swap ends on every **odd run** (1, 3)
* Batsmen swap ends at the **end of each over**
* On a wicket, the next batsman in the lineup takes the striker's position

### Innings End Conditions

An innings ends when any of these occur:

* All allocated balls are bowled
* 10 wickets fall
* The target is reached (second innings only)

---

## Teams

| Team          | Notable Players                                    |
|---------------|----------------------------------------------------|
| India         | Rohit Sharma, Virat Kohli, Jasprit Bumrah          |
| Australia     | Steve Smith, Pat Cummins, Mitchell Starc           |
| England       | Ben Stokes, Jos Buttler, Jofra Archer              |
| New Zealand   | Kane Williamson, Trent Boult, Tim Southee          |
| South Africa  | Kagiso Rabada, Quinton de Kock, David Miller       |
| Pakistan      | Babar Azam, Shaheen Afridi, Mohammad Rizwan        |
| Sri Lanka     | Wanindu Hasaranga, Pathum Nissanka, Kusal Mendis   |
| West Indies   | Andre Russell, Nicholas Pooran, Alzarri Joseph     |
| Bangladesh    | Shakib Al Hasan, Taskin Ahmed, Litton Das          |
| Afghanistan   | Rashid Khan, Mujeeb Ur Rahman, Ibrahim Zadran      |

Each team has a full 11-player lineup. Batsmen are shown by name at the crease and rotate through the batting order as wickets fall.

---

## Tech Stack

* **Python 3.6+**
* **Standard library only** — `os`, `sys`, `random`, `time`, `tty`, `termios` (Linux/macOS), `msvcrt` (Windows)

Cross-platform arrow key input is handled natively — no external packages required.

---

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes
4. Open a pull request

Ideas for improvement: innings scorecard with individual batting figures, bowling figures, player stamina/form ratings, tournament/series mode, or a difficulty setting that adjusts computer shot selection.

---

## License

MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
