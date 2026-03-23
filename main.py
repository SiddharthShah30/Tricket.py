import os
import random
import sys
import time
import json
import math
from typing import Any

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
    """Draw aligned ASCII cricket field mini-map in a Cricket 19/26 style."""
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


def run_timing_challenge(delivery, batter_skill, difficulty):
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

    travel_time = max(0.85, 1.25 / speed_factor)
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
    print("  BATTING TARGET: Choose zone [1-9]. [ENTER] keeps center (5).")
    draw_field_map(field_setup, selected_zone="5")
    while True:
        k = get_key()
        if k in FIELD_ZONES:
            return k
        if k == "ENTER":
            return "5"
        if k == "ESC":
            pause_game()


def choose_bowling_zone():
    print("  BOWLING PLAN: Choose zone [1-9] for line/length intent. [ENTER] keeps 5.")
    fake_setup = {z: "ring" for z in FIELD_ZONES}
    draw_field_map(fake_setup, selected_zone="5")
    while True:
        k = get_key()
        if k in FIELD_ZONES:
            return k
        if k == "ENTER":
            return "5"
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

    zone_kind = ZONE_PROFILE.get(zone, "straight")
    death_phase = (balls / total_balls) >= 0.8 if total_balls else False

    # Outside/off-stump plans generally squeeze scoring and induce mistakes.
    if zone_kind == "off":
        if isinstance(result, int) and result >= 4 and random.random() < 0.35:
            result = 2
        if isinstance(result, int) and result in (1, 2) and random.random() < 0.18:
            result = 0
        if result != "W" and random.random() < 0.06:
            result = "W"

    # Leg-side plans can leak boundaries if missed, especially in death.
    elif zone_kind == "leg":
        if isinstance(result, int) and result == 0 and random.random() < 0.20:
            result = 1
        if death_phase and isinstance(result, int) and result in (1, 2) and random.random() < 0.22:
            result = min(4, result + 2)

    # Straight plans are high-variance yorker channels in death overs.
    else:
        if delivery == "YORKER" and death_phase:
            if result != "W" and random.random() < 0.10:
                result = "W"
            elif isinstance(result, int) and result >= 2 and random.random() < 0.30:
                result = 1

    return result

def safe_input(prompt, default=""):
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        return default

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
# HEADER
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
# MAIN MENU
# =========================

def main_menu():
    while True:
        clear()
        print("=" * 78)
        ver  = "[ V 1.1.0 - CLI CRICKET SIMULATOR ]"
        user = "[ USER: PLAYER_1 ]"
        gap  = 78 - len(ver) - len(user)
        print(ver + " " * gap + user)
        print("=" * 78)
        print()
        draw_box([
            "",
            "  [1]   QUICK MATCH  (1 / 5 / 10 / 20 OVERS)",
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
        choice = safe_input(">> SELECT OPTION [1-3]: ", "3").strip()
        if choice == "1":   return "play"
        elif choice == "2": return "records"
        elif choice == "3":
            print("\nGG! Thanks for playing.\n")
            sys.exit(0)

# =========================
# RECORDS
# =========================

def show_records(history, stats):
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
    print("  CAREER SNAPSHOT")
    print("  " + "-" * 60)
    print(f"  Matches: {stats.get('matches', 0)}   Wins: {stats.get('user_wins', 0)}   "
          f"Losses: {stats.get('user_losses', 0)}   Ties: {stats.get('ties', 0)}")
    print(f"  Total Runs (all innings): {stats.get('total_runs', 0)}")
    print(f"  Total Wickets Fallen: {stats.get('total_wickets', 0)}")
    print(f"  Highest Combined Match Total: {stats.get('highest_match_total', 0)}")
    print()
    safe_input("  >> PRESS ENTER TO GO BACK...", "")


def choose_match_settings():
    clear()
    print_header()
    print("\n  MATCH SETTINGS\n")

    while True:
        try:
            overs = int(safe_input("  Select overs (1 / 5 / 10 / 20): ", "5"))
            if overs in [1, 5, 10, 20]:
                break
            print("  Choose 1, 5, 10, or 20.")
        except ValueError:
            print("  Invalid input.")

    print("\n  Difficulty Levels:")
    print("    [1] Easy   - More forgiving batting outcomes")
    print("    [2] Normal - Balanced simulation")
    print("    [3] Hard   - Tougher AI and tighter outcomes")

    while True:
        d = safe_input("\n  Select difficulty [1-3]: ", "2").strip()
        if d == "1":
            difficulty = "Easy"
            break
        if d == "2":
            difficulty = "Normal"
            break
        if d == "3":
            difficulty = "Hard"
            break
        print("  Enter 1, 2, or 3.")

    print("\n  AI Personality:")
    print("    [1] Defensive - Protects wickets, calmer chasing")
    print("    [2] Balanced  - Mixed tactics")
    print("    [3] Aggressive - Boundary hunting, higher risk")

    while True:
        p = safe_input("\n  Select AI personality [1-3]: ", "2").strip()
        if p == "1":
            personality = "Defensive"
            break
        if p == "2":
            personality = "Balanced"
            break
        if p == "3":
            personality = "Aggressive"
            break
        print("  Enter 1, 2, or 3.")

    return overs, difficulty, personality

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
            c = int(safe_input("  Enter number: ", "1"))
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
        "Overcast": "Swing bowlers will be dangerous!",
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
        call = safe_input("  Call Heads or Tails (H/T): ", "h").strip().lower()
        if call in ["h","heads"]:   user_call="heads"; break
        elif call in ["t","tails"]: user_call="tails"; break
        else: print("  Type H or T.")
    result = random.choice(["heads","tails"])
    animate("  Coin flips...")
    animate(f"  Result: {result.upper()}!")
    if user_call == result:
        print(f"\n  You won the toss!\n")
        while True:
            c = safe_input("  Bat or Bowl? (bat/bowl): ", "bat").strip().lower()
            if c in ["bat","b"]:
                animate(f"  {player} will BAT first.")
                safe_input("\n>> PRESS [ENTER] TO CONTINUE...", "")
                return True
            elif c in ["bowl","bo"]:
                animate(f"  {player} will BOWL first.")
                safe_input("\n>> PRESS [ENTER] TO CONTINUE...", "")
                return False
            else: print("  Invalid.")
    else:
        comp = random.choice(["bat","bowl"])
        animate(f"\n  {computer} won the toss and chose to {comp}.")
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

    type_icon = {"pace": "⚡ PACE", "spin": "🌀 SPIN",
                 "medium": "〰 MED", "bat": "🏏 BAT"}

    clear()
    print_header()
    print(f"\n  === OVER {over_num} — CHOOSE YOUR BOWLER ===\n")
    print(f"  {'#':<4} {'BOWLER':<22} {'TYPE':<10} {'OV DONE':<10} {'REMAINING':<12} {'SPELL'}")
    print("  " + "─" * 68)

    for i, p in enumerate(candidates, 1):
        btype    = get_stat(p, "bowl_type", "bat")
        ov_done  = bowler_overs.get(p, 0)
        remaining = max_quota - ov_done
        bst       = bowler_stats.get(p, {"balls": 0, "runs": 0, "wickets": 0})
        ov_str    = f"{bst['balls']//6}.{bst['balls']%6}"
        spell     = f"{bst['runs']}-{bst['wickets']} ({ov_str})"
        tlabel    = type_icon.get(btype, btype.upper())
        print(f"  [{i}]  {short(p):<22} {tlabel:<10} {ov_done:<10} {remaining} left         {spell}")

    print()
    while True:
        try:
            c = int(safe_input(f"  >> SELECT BOWLER [1-{len(candidates)}]: ", "1"))
            if 1 <= c <= len(candidates):
                chosen = candidates[c - 1]
                animate(f"\n  {short(chosen)} will bowl over {over_num}.")
                pause(0.5)
                return chosen
            else:
                print(f"  Enter a number between 1 and {len(candidates)}.")
        except ValueError:
            print("  Invalid input.")


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
                       bowling_zone="5", target=None, free_hit=False,
                       user_is_batting=True):
    cur_ov = balls // 6
    cur_bl = balls % 6
    crr    = round((score / balls) * 6, 2) if balls > 0 else 0.00
    total  = overs * 6

    clear()
    print_header()

    left = f"  {batting_team}: {score}/{wickets} ({cur_ov}.{cur_bl})"
    if target is not None:
        balls_left = total - balls
        runs_left  = target - score
        rrr = round((runs_left / balls_left) * 6, 2) if balls_left > 0 else 0.00
        right = f"TARGET: {target}  (RR: {crr:.2f}, RRR: {rrr:.2f})  "
    else:
        right = f"RR: {crr:.2f}  "
    draw_box([left.ljust(40) + right.rjust(34)])
    print()

    s_r  = batter_runs.get(striker, 0)
    s_b  = batter_balls.get(striker, 0)
    ns_r = batter_runs.get(non_striker, 0)
    ns_b = batter_balls.get(non_striker, 0)
    bst  = bowler_stats.get(current_bowler,
                             {"balls": 0, "runs": 0, "wickets": 0})

    bow_balls = bst.get("balls",   0)
    bow_runs  = bst.get("runs",    0)
    bow_wkts  = bst.get("wickets", 0)
    bow_ov    = f"{bow_balls // 6}.{bow_balls % 6}"
    bow_spell = f"{bow_runs}-{bow_wkts} ({bow_ov})"

    over_sym = "  ".join(over_log) if over_log else "-"

    timing_label, timing_note = timing_feedback(timing_grade, timing_quality)
    role = "BATTING" if user_is_batting else "BOWLING"
    role_line = f"  YOU ARE {role} | Innings {innings_num}"
    if user_is_batting:
        zone_line = (f"  TARGET ZONE: {selected_zone} - {FIELD_ZONES.get(selected_zone, 'Straight')}"
                     if selected_zone else "  TARGET ZONE: 5 - Straight")
    else:
        zone_line = f"  BOWLING ZONE: {bowling_zone} - {FIELD_ZONES.get(bowling_zone, 'Straight')}"

    draw_box([
        role_line,
        zone_line,
        f"  TIMING RESULT: {timing_label:<8} ({timing_note})",
        "  TIMING SCALE: PERFECT > GOOD > AVERAGE > BAD > MISS",
    ])

    tactical_lines = tactical_insight(score, wickets, balls, total, target, partnership_runs, over_log)
    draw_box(tactical_lines)

    print()
    print("  CENTER PLAY ZONE")
    print("  " + "-" * 60)
    if user_is_batting and field_setup:
        draw_field_map(field_setup, selected_zone)
    elif not user_is_batting:
        guide = [
            "  BOWLING EFFECT GUIDE",
            "  Off zones (1/2/3): tighter lines, dots/wickets",
            "  Leg zones (4/6/7): boundary risk if missed",
            "  Straight (5/8/9): yorker channel in death overs",
        ]
        for ln in guide:
            print(ln)

    print()
    print("  BOTTOM SCOREBOARD")
    print("  " + "-" * 60)
    print(f"  STRIKER   : {short(lineup[striker]):<18} {s_r:>3} ({s_b})")
    print(f"  NON-STR   : {short(lineup[non_striker]):<18} {ns_r:>3} ({ns_b})")
    print(f"  BOWLER    : {short(current_bowler):<18} {bow_spell}")
    print(f"  LAST OVER : {over_sym}")

    if target is not None:
        runs_left = target - score
        balls_left = total - balls
        print(f"  CHASE     : Need {runs_left} off {balls_left}")
    print(f"  PARTNER   : {partnership_runs} runs")
    if free_hit:
        print("  ALERT     : FREE HIT")

    print()
    print(f"  Pitch: {pitch}   Weather: {weather}   Difficulty: {difficulty}   AI: {personality}")
    print()
    print("-" * 78)

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
    clear()
    print_header()

    crr     = round((score / balls) * 6, 2) if balls > 0 else 0.00
    ov_str  = f"{balls // 6}.{balls % 6}"
    w_cnt   = extras_detail.get("w",  0)
    lb_cnt  = extras_detail.get("lb", 0)
    nb_cnt  = extras_detail.get("nb", 0)
    total_x = w_cnt + lb_cnt + nb_cnt

    draw_box([
        f"  INNINGS COMPLETE: {batting_team}".ljust(38)
            + f"TOTAL: {score}/{wickets} ({ov_str} Overs)".rjust(36),
        f"  RUN RATE: {crr:.2f}".ljust(38)
            + f"EXTRAS: {total_x} (w{w_cnt}, lb{lb_cnt}, nb{nb_cnt})".rjust(36),
    ])
    print()

    # Batting summary
    print("  BATTING SUMMARY" + " " * 35 + "S/R")
    print("  " + "-" * 74)
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
        print(f"  {short(name):<16}  {dis:<24}  {r} ({b:02d})  {bdry:<12}  {sr:.1f}")
        shown += 1
    if shown == 0:
        print("  (no batters recorded)")
    print()

    # Bowling summary
    print("  BOWLING SUMMARY"
          + "O".rjust(13) + "M".rjust(5) + "R".rjust(5)
          + "W".rjust(5) + "  ECON")
    print("  " + "-" * 62)
    for bname, bst in bowler_stats.items():
        if bst["balls"] == 0:
            continue
        ov  = f"{bst['balls'] // 6}.{bst['balls'] % 6}"
        eco = round((bst["runs"] / bst["balls"]) * 6, 2) \
              if bst["balls"] > 0 else 0.00
        print(f"  {short(bname):<20}  {ov:>5}  {bst['maidens']:>3}  "
              f"{bst['runs']:>4}  {bst['wickets']:>4}  {eco:>7.2f}")
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
    max_quota      = max(1, overs // 5)
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
    bowling_zone     = "5"

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
        field_setup = (get_ai_field_setup(personality, balls, total_balls, wickets, target, score)
                   if user_is_batting else None)

        render_play_screen(
            batting_team, bowling_team, score, wickets, overs, balls,
            innings_num, lineup, striker, non_striker,
            batter_runs, batter_balls, current_bowler, bowler_stats,
            over_log, partnership_runs, pitch, weather, difficulty, personality,
            field_setup, selected_zone, timing_grade, timing_quality,
            bowling_zone, target, free_hit, user_is_batting
        )

        # Show correct commands based on current bowler type
        b_type = get_stat(current_bowler, "bowl_type", "medium")
        if user_is_batting:
            print("  COMMANDS: [A/←] Defend  |  [D/→] Swing  |  [W/↑] Loft  |  [S/↓] Leave")
            print("  SKILL:    Choose target zone [1-9], then press [SPACE] for timing")
        else:
            if b_type == "spin":
                print("  COMMANDS: [A/←] Off-spin  |  [D/→] Leg-spin  |  [W/↑] Flipper  |  [S/↓] Googly")
            else:
                print("  COMMANDS: [A/←] In-swing  |  [D/→] Out-swing  |  [W/↑] Yorker  |  [S/↓] Bouncer")
        print("  SYSTEM:   [ESC] Pause / Resume")
        print("-" * 78)

        # Input
        shot = delivery = None
        timing_quality = 1.0
        timing_grade = "-"
        if user_is_batting:
            while shot is None:
                k = get_key()
                if k == "ESC":
                    pause_game()
                    continue
                if   k in ("D", "RIGHT"): shot = "SWING"
                elif k in ("A", "LEFT"):  shot = "DEFEND"
                elif k in ("W", "UP", "L"):    shot = "LOFT"
                elif k in ("S", "DOWN", "Q"):  shot = "LEAVE"

            selected_zone = choose_target_zone(field_setup)

            # Computer bowler picks delivery based on their type
            delivery = choose_ai_delivery(b_type, balls, total_balls, target, score, personality)
        else:
            bowling_zone = choose_bowling_zone()
            if b_type == "spin":
                while delivery is None:
                    k = get_key()
                    if k == "ESC":
                        pause_game()
                        continue
                    if   k in ("LEFT", "A"):  delivery = "OFF_SPIN"
                    elif k in ("RIGHT", "D"): delivery = "LEG_SPIN"
                    elif k in ("UP", "W"):    delivery = "FLIPPER"
                    elif k in ("DOWN", "S"):  delivery = "GOOGLY"
            else:
                while delivery is None:
                    k = get_key()
                    if k == "ESC":
                        pause_game()
                        continue
                    if   k in ("LEFT", "A"):  delivery = "IN"
                    elif k in ("RIGHT", "D"): delivery = "OUT"
                    elif k in ("UP", "W"):    delivery = "YORKER"
                    elif k in ("DOWN", "S"):  delivery = "BOUNCER"
            shot = choose_ai_shot(delivery, target, score, balls, total_balls, wickets, difficulty, personality)

        print()
        animate("  Bowler runs in...", delay=0.02)
        pause(0.35)

        if user_is_batting:
            timing_grade, timing_quality = run_timing_challenge(
                delivery, get_stat(lineup[striker], "bat_skill", 50), difficulty
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
    clear()
    print_header()

    target = s1 + 1

    if s2 >= target:
        wkts_left = 10 - w2
        balls_rem  = overs * 6 - b2
        ovs_rem    = f"{balls_rem // 6}.{balls_rem % 6}"
        msg    = (f"  \U0001f389  {t2} WIN BY {wkts_left} WICKET(S)"
                  f"  ({ovs_rem} OVERS REMAINING)  \U0001f389")
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

    rr1 = round((s1 / (b1 if b1 else 1)) * 6, 2)
    rr2 = round((s2 / (b2 if b2 else 1)) * 6, 2)
    ov1 = f"{b1 // 6}.{b1 % 6}"
    ov2 = f"{b2 // 6}.{b2 % 6}"

    print("  FINAL RECAP")
    print("  " + "-" * 70)
    print(f"  \U0001f3cf 1ST INNINGS ({t1}):   {s1}/{w1} ({ov1})   |  RR: {rr1}")
    print(f"  \U0001f3cf 2ND INNINGS ({t2}):   {s2}/{w2} ({ov2})   |  RR: {rr2}")
    print()

    potm_sc, potm_name, potm_team, potm_bst_dict = pick_potm(
        t1, t2, br1, bb1, bs1, br2, bb2, bs2)
    potm_bst   = potm_bst_dict.get(potm_name, {})
    potm_idx   = (TEAMS.get(potm_team, []).index(potm_name)
                  if potm_name in TEAMS.get(potm_team, []) else 0)
    potm_runs  = (br1 if potm_team == t1 else br2).get(potm_idx, 0)
    potm_bals  = (bb1 if potm_team == t1 else bb2).get(potm_idx, 0)
    potm_wkts  = potm_bst.get("wickets", 0)

    print("  \U0001f947 PLAYER OF THE MATCH")
    print("  " + "-" * 70)
    print(f"  >> {short(potm_name)} ({potm_team})")
    if potm_bst.get("balls", 0) > 0:
        ov_s = f"{potm_bst['balls'] // 6}.{potm_bst['balls'] % 6}"
        print(f"  >> PERFORMANCE: {ov_s} - {potm_bst.get('maidens',0)} - "
              f"{potm_bst.get('runs',0)} - {potm_wkts}")
    else:
        print(f"  >> PERFORMANCE: {potm_runs} runs ({potm_bals} balls)")
    print()

    print("  " + "-" * 70)
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

    left_rows  = ["[ BATTING LEADERS ]", "─" * 28]
    right_rows = ["[ BOWLING LEADERS ]", "─" * 28]
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

    print("-" * 78)
    print("  OPTIONS: [R]eplay  |  [Q]uit to Menu")
    print("-" * 78)
    print()

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
    game_data = load_game_data()
    history = game_data["history"]
    stats = game_data["stats"]
    while True:
        action = main_menu()

        if action == "records":
            show_records(history, stats)
            continue

        overs, difficulty, personality = choose_match_settings()

        player, computer = choose_team()
        pitch, weather   = setup_conditions()
        user_bats_first  = toss(player, computer)

        t1 = player   if user_bats_first else computer
        t2 = computer if user_bats_first else player

        # Innings 1 — summary shown inside play_innings, user presses Enter
        clear(); print_header()
        animate(f"\n  {t1} will BAT FIRST  |  Difficulty: {difficulty}  |  AI: {personality}\n")
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