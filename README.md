## Table of Contents

* [Features](#features)
* [Installation](#installation)
* [Usage](#usage)
* [How to Play](#how-to-play)
* [Game Mechanics](#game-mechanics)
* [Tech Stack](#tech-stack)
* [Contributing](#contributing)
* [License](#license)

---

## Features

* Coin toss with bat/bowl election
* Two full innings with live scoreboard updates
* Current Run Rate (CRR) and Required Run Rate (RRR) display
* Over-by-over ball log tracking
* Four batting shot types with randomised outcomes
* Four bowling delivery types that influence batting results
* Wide ball handling (score +1, ball not counted)
* Animated text output for an immersive feel
* Supports multiple over formats: 1, 5, 10, 20, and 50 overs

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/tricket.git
cd tricket
```

### 2. Ensure Python is installed

Python 3.6+ is sufficient — no external libraries are required.

```bash
python --version
```

### 3. Run the game

```bash
python main.py
```

---

## Usage

On launch you will be asked to choose an over format:

```
Choose overs 1, 5, 10, 20, 50:
```

Enter one of the listed values to begin. The toss follows immediately.

---

## How to Play

### Toss

```
Heads or Tails?
```

Call it correctly to win the toss and choose to bat or bowl. Lose it and the computer decides.

---

### Batting (when you bat)

Each ball you choose a shot:

| Key | Shot    | Tendency                          |
|-----|---------|-----------------------------------|
| `S` | Swing   | Balanced — singles, twos, fours   |
| `D` | Defend  | Safe — mostly dots and singles    |
| `L` | Loft    | Aggressive — fours and sixes      |
| `Q` | Leave   | Quit the game                     |

The computer secretly selects a delivery type each ball which influences your outcome probabilities.

---

### Bowling (when you bowl)

Each ball you choose a delivery:

| Key | Delivery       |
|-----|----------------|
| `I` | In-Swing       |
| `O` | Out-Swing      |
| `R` | Reverse-Swing  |
| `B` | Bouncer        |

The computer randomly picks a shot in response. Swing deliveries increase the chance of a leave (dot or wicket). A bouncer can produce a wide ball.

---

### Scoreboard

The live scoreboard shows:

```
TEAM: 84/3 (10.2)      TARGET: 121
CRR: 8.17      RRR: 7.44
```

- **Score / Wickets (Overs.Balls)**
- **CRR** — Current Run Rate
- **RRR** — Required Run Rate (second innings only)
- **THIS OVER** — Ball-by-ball log for the current over, e.g. `[4] [0] [W] [1] [6]`

---

## Game Mechanics

### Batting Outcome Probabilities

| Shot    | 0   | 1   | 2   | 4   | 6   | W   |
|---------|-----|-----|-----|-----|-----|-----|
| Defend  | 60% | 30% | —   | —   | —   | 10% |
| Swing   | 20% | 25% | 25% | 20% | —   | 10% |
| Loft    | 15% | —   | —   | 40% | 30% | 15% |
| Leave vs Swing | 85% | — | — | — | — | 15% |
| Leave vs Bouncer | 70% | — | — | — | — | 30% (WD) |

A **Wide** (`WD`) adds 1 run to the batting team's total without consuming a ball.

### Innings End Conditions

An innings ends when any of the following occur:
* All allocated balls are bowled
* 10 wickets fall
* The target is reached (second innings only)

---

## Tech Stack

* **Python 3.6+**
* **Standard library only** — `random`, `os`, `time`

---

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes
4. Open a pull request

Ideas for improvement: player/team naming, innings scorecard summary, difficulty levels, or a high-score leaderboard.

---

## License

MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
