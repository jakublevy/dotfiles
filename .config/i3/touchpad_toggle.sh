#!/bin/sh
device='SYN1B7F:00 06CB:CD41 Touchpad'
state = $(xinput list-props "$device" | grep "Device Enabled" | grep -o 
"[01]$")

if [ $state == '1' ]; then
   xinput set-prop "$device" "Device Enabled" 0
else
   xinput set-prop "$device" "Device Enabled" 1

