#!/bin/sh
echo 'pcm.!default {
    type hw
    card 0
    device 7
}' > ~/.asoundrc
