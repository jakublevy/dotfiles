#!/bin/sh
pacman -Rcs $(pacman -Qdtq)
