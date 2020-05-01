#!/bin/sh
gcc -march=native -Q --help=target | grep -m 1 march | while read a b; do echo "$b"; done
