#!/bin/bash

# Define the menu options with Icons
# You can change the icons if you want to use Nerd Fonts
OPT_LOCK="Lock Screen"
OPT_SUSPEND="Suspend"
OPT_REBOOT="Reboot"
OPT_UEFI="Reboot (UEFI)"
OPT_OFF="Shutdown"
LOG_OUT="Log Out"

OPTIONS="""$OPT_LOCK
$OPT_SUSPEND
$OPT_REBOOT
$OPT_UEFI
$OPT_OFF
$LOG_OUT"""

CHOICE=$(echo -e "$OPTIONS" | wofi --dmenu --prompt "Power Menu" --width 250 --height 240 --style ~/.config/wofi/style.css)

# Execute the selected command
case "$CHOICE" in
    "$OPT_LOCK")
        swaylock -f -c 000000
        ;;
    "$OPT_SUSPEND")
        swaylock -f -c 000000 && systemctl suspend
        ;;
    "$OPT_REBOOT")
        reboot
        ;;
    "$OPT_UEFI")
        # 'reboot -- UEFI' translates to this systemctl command
        systemctl reboot --firmware-setup
        ;;
    "$OPT_OFF")
        shutdown now
        ;;
    "$LOG_OUT")
        swaymsg exit
        ;;
esac