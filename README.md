# Triket Simulator

A terminal-based cricket simulation game written in Python.

The latest version adds deeper game logic with timing-based batting, zone-based tactics, difficulty and AI personality controls, a tactical insight panel, and persistent career stats.

---

## Features

- 10 international teams with full XI lineups and tuned player attributes
- Match formats: 1, 5, 10, and 20 overs
- Difficulty modes: Easy, Normal, Hard
- AI personalities: Defensive, Balanced, Aggressive
- Real-time batting timing gauge (PERFECT, GOOD, EARLY/LATE, MISS)
- Batting target-zone system (zones 1-9) with field-aware outcomes
- Bowling plan zones (zones 1-9) with off/leg/straight tactical effects
- Delivery impact model for pace and spin variations
- Tactical insight panel with phase, pressure/momentum, projections, and win estimate
- DRS flow for eligible dismissals with limited reviews
- Free-hit, wide, and no-ball handling
- Over-by-over logs and richer score HUD
- Pause/resume support during live gameplay
- Persistent records in records.json

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/triket.git
cd triket
```

2. Ensure Python 3.8+ is installed:

```bash
python --version
```

3. Run the game:

```bash
python main.py
```

---

## Quick Start

When starting a match, configure:

- Overs: 1, 5, 10, or 20
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

- A or Left Arrow: Defend
- D or Right Arrow: Swing
- W or Up Arrow: Loft
- S or Down Arrow: Leave
- 1-9: Choose target zone
- Space: Timing hit on the gauge
- Esc: Pause

### Bowling (pace)

- A or Left Arrow: In-swing
- D or Right Arrow: Out-swing
- W or Up Arrow: Yorker
- S or Down Arrow: Bouncer
- 1-9: Choose bowling zone
- Esc: Pause

### Bowling (spin)

- A or Left Arrow: Off-spin
- D or Right Arrow: Leg-spin
- W or Up Arrow: Flipper
- S or Down Arrow: Googly
- 1-9: Choose bowling zone
- Esc: Pause

---

## Game Logic Highlights

- Timing challenge affects final ball outcome after base simulation.
- Zone compatibility rewards matching shot type to target area.
- AI field setup adapts to personality, phase, wickets, and chase pressure.
- Delivery type modifies wicket, run, and boundary tendencies.
- Difficulty adjusts user and AI scoring/wicket balance.
- AI shot and delivery choices adapt to match context.

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
- Standard library only (os, sys, time, random, json, math, plus platform-specific input handling)

No third-party dependencies are required.

---

## License

MIT License
