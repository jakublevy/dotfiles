#!/bin/sh
rm ~/.asoundrc
alsactl --file ~/.asound.state store &> /dev/null
alsactl --file ~/.asound.state restore &> /dev/null
