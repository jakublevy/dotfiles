#!/bin/sh
echo 'pcm.!default {
    type hw
    card 0
    device 7
}' > ~/.asoundrc
alsactl --file ~/.asound.state store &> /dev/null
alsactl --file ~/.asound.state restore &> /dev/null
