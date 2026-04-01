# Triket Simulator

A terminal-based cricket simulation game written in Python.

The latest version features a complete retro TUI redesign across menus, modernized match presentation, flexible match setup, and deeper tactical gameplay.

---

## Features

- 10 international teams with full XI lineups and tuned player attributes
- Flexible innings length: choose any overs from 1 to 50
- Difficulty modes: Easy, Normal, Hard
- AI personalities: Defensive, Balanced, Aggressive
- Red-ball themed retro menu UI with centered ladder navigation
- Dedicated Team Select screen with large ASCII header and rhythmic [[ nn ]] selector
- Consistent pre-match and post-match screen styling (records, conditions, toss, summaries, result)
- Cleaner Match Start presentation with direct "WILL BAT FIRST" opener card
- Real-time batting timing gauge (PERFECT, GOOD, EARLY/LATE, MISS)
- Number-first batting field radar (zones 1-9) with facing indicator and gap awareness
- Number-first bowling target grid (zones 1-9) unified with batting layout
- Live bowling line/length + release feedback with numeric target lock-in
- Delivery impact model for pace and spin variations
- Match HUD with overs-left, projected score/required chase info, and win prediction
- DRS flow for eligible dismissals with limited reviews
- Free-hit, wide, and no-ball handling
- Over-by-over logs and richer score HUD
- Pause/resume support during live gameplay
- Spacebar and Enter action handling stabilized for timing/release actions
- Persistent records in records.json

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/SiddharthShah30/Tricket.py.git
cd Tricket.py
```

2. Ensure Python 3.8+ is installed:

```bash
python --version
```

3. (Optional but recommended on Windows) Install Colorama for better ANSI color handling:

```bash
pip install colorama
```

4. Run the game:

```bash
python main.py
```

---

## Quick Start

When starting a match, configure:

- Overs: any value from 1 to 50
- Difficulty: Easy, Normal, or Hard
- AI personality: Defensive, Balanced, or Aggressive

Then:

1. Select your team
2. Complete the toss
3. Play innings 1 and innings 2
4. View summary and records

---

## Controls

### Batting

- 1-9: Choose shot direction/target zone on the radar
- Q / E: Decrease / increase aggression (power)
- L: Toggle loft mode
- Space or Enter: Play shot and lock timing
- Esc: Pause

### Bowling

- 1-4: Choose bowling plan/type (Normal, Short, Full, Yorker)
- 1-9 or Arrow Keys: Choose bowling target on the numeric target grid
- Space or Enter: Start and lock release meter
- Esc: Pause

### Menus

- W/S or Up/Down: Navigate options
- Enter: Select
- Esc: Back (where applicable) / Exit in main menu

---

## Game Logic Highlights

- Timing challenge affects final ball outcome after base simulation.
- Zone compatibility rewards matching shot type to target area.
- Batting and bowling share a unified numeric 1-9 targeting model for consistency.
- AI field setup adapts to personality, phase, wickets, and chase pressure.
- Delivery type modifies wicket, run, and boundary tendencies.
- Difficulty adjusts user and AI scoring/wicket balance.
- AI shot and delivery choices adapt to match context.
- Bowler over quota automatically adjusts to match length.

---

## Persistence

Game data is saved to records.json and includes:

- Recent match history (up to 100 entries)
- Matches, wins, losses, ties
- Aggregate runs and wickets
- Highest combined match total

---

## Tech Stack

- Python
- Standard library (os, sys, time, random, json, math, shutil, re, plus platform-specific input handling)
- Optional: Colorama (for improved terminal color behavior)

No hard third-party dependency is required to run.

---

## License

MIT License
