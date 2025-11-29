#!/usr/bin/env python3
import sys
import json
import subprocess

# --- CONFIGURATION ---
# Run 'swaymsg -t get_outputs' in a terminal to verify these names
PRIMARY_MONITOR = "DP-2"
SECONDARY_MONITOR = "HDMI-A-1" 
OFFSET = 10 # How much to add for the secondary monitor (1 -> 11)

def get_focused_output():
    try:
        # Get output info from Sway
        result = subprocess.run(['swaymsg', '-t', 'get_outputs'], capture_output=True, text=True)
        outputs = json.loads(result.stdout)
        
        # Find the one that has "focused": true
        for output in outputs:
            if output.get('focused'):
                return output['name']
    except Exception as e:
        print(f"Error getting outputs: {e}")
        return None
    return None

def move_container(target):
    output_name = get_focused_output()
    final_target = target

    # Logic: If we are on the secondary monitor, shift the workspace number
    if output_name == SECONDARY_MONITOR:
        final_target = target + OFFSET
    
    # Run the move command
    cmd = ['swaymsg', 'move', 'container', 'to', 'workspace', 'number', str(final_target)]
    subprocess.run(cmd)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: smart_move.py <workspace_number>")
        sys.exit(1)
    
    try:
        target_ws = int(sys.argv[1])
        move_container(target_ws)
    except ValueError:
        print("Error: Workspace must be an integer.")