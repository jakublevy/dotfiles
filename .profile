#!/bin/sh 

[ -z "$SSH_AUTH_SOCK" ] && eval `ssh-agent -s` > /dev/null 2>&1
[ -z $DISPLAY ] && [ $XDG_VTNR -eq 1 ] && exec startx
