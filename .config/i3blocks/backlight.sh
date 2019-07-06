#!/bin/bash
val=$(xbacklight -get | cut -d'.' -f 1)
printf "%s%%\n" "$val" 
