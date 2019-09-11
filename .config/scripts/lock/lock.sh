#!/bin/bash
 
dir='/home/jakub/.config/scripts/lock/'
screen='/tmp/lockscreen.png'
lock="$dir"'lock.png'

if [ -f "$screen" ]; then
    exit 0
fi

maim "$screen"
gm convert "$screen" -scale 10% -scale 1000% "$screen"
#convert "$screen" -filter Gaussian -blur 0x3 "$screen"
 
if [ -f "$lock" ]; then
    # placement x/y
    PX=0
    PY=0
    # lockscreen image info
    R=$(file "$lock" | grep -o '[0-9]* x [0-9]*')
    RX=$(echo $R | cut -d' ' -f 1)
    RY=$(echo $R | cut -d' ' -f 3)
 
    SR=$(xrandr --query | grep ' connected' | sed 's/primary //' | cut -f3 -d' ')
    for RES in $SR
    do
        # monitor position/offset
        SRX=$(echo $RES | cut -d'x' -f 1)                   # x pos
        SRY=$(echo $RES | cut -d'x' -f 2 | cut -d'+' -f 1)  # y pos
        SROX=$(echo $RES | cut -d'x' -f 2 | cut -d'+' -f 2) # x offset
        SROY=$(echo $RES | cut -d'x' -f 2 | cut -d'+' -f 3) # y offset
        PX=$(($SROX + $SRX/2 - $RX/2))
        PY=$(($SROY + $SRY/2 - $RY/2))
 
        gm convert "$screen" "$lock" -geometry +$PX+$PY - | gm composite -geometry +$PX+$PY -matte "$lock" - "$screen"
        #echo "done"
    done
fi
# dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Stop
#i3lock  -I 10 -d -e -u -n -i "$screen"

#forks or do not forks depending on whether systemd called this script or not
#forking is required for not blocking the sleeping
#not forking is required for deletion of file after unlocking pc
if [ $# -eq 0 ]; then
    i3lock -n -e -u -i "$screen"
elif [ "$1" -eq '-f' ]; then
    i3lock -e -u -i "$screen"
fi

rm "$screen"
