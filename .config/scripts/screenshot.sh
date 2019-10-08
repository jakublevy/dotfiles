#!/bin/sh

screenshot='/tmp/'$(date +%s)'.png'
key='' #insert your imgbb.com API key here

if [[ $# -eq 1 && "$1" == '-f' ]]; then
    maim "$screenshot"
elif [[ $# -eq 1 && "$1" == '-w' ]]; then
    maim -i $(xdotool getactivewindow) "$screenshot"
elif [[ $# -eq 1 && "$1" == '-e' ]]; then
    maim -i $(xdotool getactivewindow) "/home/jakub/Pictures/$(date +%s)-screenshot.png"
else
    exit 1
fi
result=$(curl --silent --location --request POST "https://api.imgbb.com/1/upload?key=$key" --form "image=@$screenshot")

if [[ "$1" == '-f' ]] || [["$1" == '-w' ]]; then
    rm "$screenshot"
fi

echo "$result" | jq -r '.data.image.url' | xsel -b
