#!/bin/bash

# Check if a recording is already running
# If yes, pressing PrintScreen again stops it.
if pgrep -x "wf-recorder" > /dev/null; then
    pkill -SIGINT wf-recorder
    notify-send "Recording Stopped" "Video saved to ~/Videos/Screencasts"
    exit
fi

# 1. Main Menu: Choose between Screenshot or Record
# We use emojis so it looks nice in Wofi
OPTS="Screenshot\n Record"
CHOICE=$(echo -e "$OPTS" | wofi --dmenu --prompt "Capture Mode" --width 200 --height 150 --style ~/.config/wofi/style.css)

# 2. Handle Selection
if [[ $CHOICE == *"Screenshot"* ]]; then
    # Sub-Menu for Screenshot
    TYPE="🖥️ Full Screen\n⛶ Area / Window"
    SHOT=$(echo -e "$TYPE" | wofi --dmenu --prompt "Screenshot Type" --width 200 --height 150)
    
    # Filename format
    FILE=~/Pictures/Screenshots/$(date +'%Y-%m-%d-%H%M%S.png')
    mkdir -p ~/Pictures/Screenshots

    if [[ $SHOT == *"Full"* ]]; then
        # Take full shot, save to file AND copy to clipboard
        grim "$FILE"
        cat "$FILE" | wl-copy
        notify-send "Screenshot Taken" "Saved to $FILE"
    elif [[ $SHOT == *"Area"* ]]; then
        # Take area shot
        grim -g "$(slurp)" "$FILE"
        cat "$FILE" | wl-copy
        notify-send "Screenshot Taken" "Saved to $FILE"
    fi

elif [[ $CHOICE == *"Record"* ]]; then
    # Sub-Menu for Recording
    TYPE="🖥️ Full Screen\n⛶ Area"
    REC=$(echo -e "$TYPE" | wofi --dmenu --prompt "Record Type" --width 200 --height 150)
    
    FILE=~/Videos/Screencasts/$(date +'%Y-%m-%d-%H%M%S.mp4')
    mkdir -p ~/Videos/Screencasts

    if [[ $REC == *"Full"* ]]; then
        # Record Full Screen in background (&)
        wf-recorder -f "$FILE" &
        notify-send "Recording Started" "Press PrtScn to stop"
    elif [[ $REC == *"Area"* ]]; then
        # Select area then record
        wf-recorder -g "$(slurp)" -f "$FILE" &
        notify-send "Recording Started" "Press PrtScn to stop"
    fi
fi