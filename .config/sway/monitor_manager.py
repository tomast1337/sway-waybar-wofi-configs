#!/usr/bin/env python3
import subprocess
import argparse
import sys
import time

# --- CONFIGURATION ---
MAIN_MONITOR = "DP-2"
SIDE_MONITOR = "HDMI-A-1"
TV_MONITOR   = "DP-3"

# List of workspaces that belong to the Side Monitor
SIDE_WORKSPACES = range(11, 21) # 11 through 20

def run_sway_cmd(cmd):
    """Runs a swaymsg command silently."""
    try:
        subprocess.run(["swaymsg", cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Error running {cmd}: {e}")

def move_workspaces_to(output_name):
    """
    Moves workspaces 11-20 to a specific output without flashing the screen too much.
    """
    print(f"Migrating workspaces 11-20 to {output_name}...")
    for i in SIDE_WORKSPACES:
        # Syntax: [workspace=11] move workspace to output DP-2
        cmd = f"[workspace={i}] move workspace to output {output_name}"
        run_sway_cmd(cmd)

def set_work_mode():
    """
    1. Configure screens first (so the side monitor exists in the right place).
    2. Move workspaces 11-20 BACK to the Side Monitor.
    """
    # 1. Apply Screen Layout
    commands = [
        f"output {MAIN_MONITOR} mode 1920x1080@165Hz scale 1 position 0 0 enable",
        f"output {SIDE_MONITOR} mode 2560x1080@75Hz scale 1 position 1920 0 enable",
        f"output {TV_MONITOR} disable"
    ]
    run_sway_cmd("; ".join(commands))
    
    # 2. Migrate Workspaces back to side monitor
    # We wait a tiny bit to ensure Sway has registered the new monitor layout
    time.sleep(0.5)
    move_workspaces_to(SIDE_MONITOR)
    
    # 3. Notify
    subprocess.run(["notify-send", "Monitor Mode", "Work Setup Applied (Dual Screen)"])

def set_movie_mode():
    """
    1. Move workspaces 11-20 to the MAIN monitor (Safe keeping).
    2. Then collapse the screens into Mirror Mode.
    """
    # 1. Migrate Workspaces to Main Monitor FIRST
    move_workspaces_to(MAIN_MONITOR)
    
    # 2. Apply Mirror Layout
    commands = [
        f"output {MAIN_MONITOR} mode 1920x1080@60Hz position 0 0 enable",
        f"output {SIDE_MONITOR} mode 1920x1080@60Hz position 0 0 enable",
        f"output {TV_MONITOR}   mode 1920x1080@60Hz position 0 0 enable"
    ]
    run_sway_cmd("; ".join(commands))

    # 3. Notify
    subprocess.run(["notify-send", "Monitor Mode", "Movie Mode Applied (Mirroring)"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["work", "movie"], help="Mode to apply")
    args = parser.parse_args()
    
    if args.mode == "work":
        set_work_mode()
    elif args.mode == "movie":
        set_movie_mode()