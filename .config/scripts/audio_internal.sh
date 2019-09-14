#!/bin/sh
rm ~/.asoundrc
alsactl restore &> /dev/null
