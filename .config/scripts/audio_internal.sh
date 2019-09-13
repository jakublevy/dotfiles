#!/bin/sh
echo 'pcm.!default {
    type hw
    card 0
    device 0
}' > ~/.asoundrc
