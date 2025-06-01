PS1='[${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]\[\033[01;34m\] \W\[\033[00m\]]\$ ' 

alias ls='ls --color' 
alias grep='grep --color' 

[ -f /etc/bash_completion ] && . /etc/bash_completion
