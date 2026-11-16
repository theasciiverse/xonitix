"""Plays Xonitix for the catalog preview (asciiverse/record-preview.sh).

Reads the tmux pane and presses keys: in the hero's stretch of the line
it builds a barrier when the dots are all to one side and far enough
away (which fills the dot-free side), splits a stretch with dots on both
sides, and walks to the widest open stretch when its own is done. Plays
RUNS games, quitting each with q after about RUN_LENGTH seconds if the
dots have not got the hero first.
    python3 -I drive.py <tmux socket> <session> [debug]
"""
import subprocess
import sys
import time

SOCK, SESS = sys.argv[1], sys.argv[2]
DEBUG = len(sys.argv) > 3
RUNS = 3
RUN_LENGTH = 13.0
SAFE = 7                   # cells between the hero and the nearest dot
T0 = time.time()


def tmux(*args):
    return subprocess.run(["tmux", "-L", SOCK, *args], capture_output=True,
                          text=True).stdout


def key(k, wait=0.0):
    if DEBUG:
        print(round(time.time() - T0, 2), k, file=sys.stderr)
    tmux("send-keys", "-t", SESS, k)
    if wait:
        time.sleep(wait)


def game_overs():
    return tmux("capture-pane", "-p", "-t", SESS).count("G A M E")


def game_line():
    """The line being played (hero, walls, dots), or None."""
    rows = tmux("capture-pane", "-p", "-t", SESS).split("\n")
    for row in reversed(rows):
        if "G A M E" in row:
            return None
        end = row.rfind("| Level")
        if end > 0:
            return row[:end]
    return None


def stretch(line, x):
    """The open stretch around x: (left wall, right wall)."""
    left = x - 1
    while left > 0 and line[left] not in "|L":
        left -= 1
    right = x + 1
    while right < len(line) - 1 and line[right] not in "|L":
        right += 1
    return max(left, 0), min(right, len(line) - 1)


def widest_open(line):
    """Middle of the widest stretch with no barrier."""
    best, start, best_mid = 0, None, None
    for i, c in enumerate(line + "|"):
        if c in "|L":
            if start is not None and i - start > best:
                best, best_mid = i - start, (start + i - 1) // 2
            start = None
        elif start is None:
            start = i
    return best_mid, best


def play_run():
    start = time.time()
    moving = None
    over = game_overs()
    while time.time() - start < RUN_LENGTH:
        if game_overs() > over:        # the dots got the hero
            return
        line = game_line()
        if line is None:
            time.sleep(0.05)
            continue
        hero = max(line.find("_"), line.find("L"))
        if hero < 0:
            time.sleep(0.02)
            continue
        dots = [i for i, c in enumerate(line) if c in ".:"]
        if line[hero] == "L":          # on a barrier: go somewhere open
            target = widest_open(line)[0]
        else:
            left, right = stretch(line, hero)
            inside = [d for d in dots if left < d < right]
            near = min((abs(d - hero) for d in inside), default=99)
            one_side = all(d < hero for d in inside) or all(d > hero for d in inside)
            target = None
            if near >= SAFE and (one_side or right - left > 12):
                if moving:
                    key("Down")
                    moving = None
                key("Space", 0.12)
                continue
            if right - left <= 4:      # too narrow to bother with
                target = widest_open(line)[0]
            elif near < SAFE:          # step away from the closest dot
                closest = min(inside, key=lambda d: abs(d - hero))
                target = left + 1 if closest > hero else right - 1
                target = (hero + target) // 2
        if target is None:
            time.sleep(0.03)
            continue
        want = "Right" if target > hero else "Left"
        if abs(target - hero) <= 2:
            if moving:
                key("Down")
                moving = None
        elif moving != want:
            key(want)
            moving = want
        time.sleep(0.02)
    key("q")


for run in range(RUNS):
    time.sleep(1.5)                    # the hint line, then play
    play_run()
    time.sleep(2.8)                    # GAME OVER
