#!/bin/sh

screenshot='/tmp/'$(date +%s)'.png'
key='' #insert your imgbb.com API key here

if [ $# -eq 1 && "$1" == '-f' ]; then
    maim "$screenshot"
elif [ $# -eq 1 && "$1" == '-w' ]; then
    maim -i $(xdotool getactivewindow) "$screenshot"
else
    exit 1
fi
result=$(curl --silent --location --request POST "https://api.imgbb.com/1/upload?key=$key" --form "image=@$screenshot")
rm "$screenshot"

echo "$result" | jq -r '.data.image.url' | xsel -b
