#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
PS1='[\u@\h \W]\$ '

alias vim=nvim

#cabal installed binaries location
export PATH="$PATH:/home/jakub/.local/bin"

#bash vi mode
set -o vi

#make info page use vi keys by default
alias info='info --vi-keys'

#ed sane config
alias ed='ed -p "ed> " -v'
