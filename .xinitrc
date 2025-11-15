# English and Czech QWERTY layout ALT+Shift toggle xkb fallback
# without IMF, load keys remap
keyboard-remap

[ -f ~/.Xresources ] && xrdb -merge ~/.Xresources

# Turn off monitors after 10 minutes
xset dpms 600 600 600

# Wallpaper
feh --bg-tile ~/Pictures/Wallpapers/wallpap1920x1080.jpg

#systemctl --user import-environment DISPLAY XAUTHORITY
#systemctl --user start copyq.service
#systemctl --user start autolock.service
#systemctl --user start flameshot.service
#systemctl --user start dunst.service
#systemctl --user start polybar.service
#systemctl --user start copyq autolock flameshot dunst polybar

# Networking
nm-applet &

# Sound
pasystray &

# Bluetooth
blueman-applet &

# Mounting
udiskie -c ~/.config/udiskie/config.yaml &

# Clipboard manager
copyq &

# Bug in copy to clipboard screenshot program
flameshot & disown

# Auto lock after 10 minutes
xautolock -time 10 -locker "xsecurelock" &

# Gamma step indicator
gammastep-indicator -l manual -l 50.43:16.15 &

# Notifications
dunst &

polybar-launch &

[ -z "$DBUS_SESSION_BUS_ADDRESS" ] && eval $(dbus-launch --sh-syntax --exit-with-session)
dbus-update-activation-environment DISPLAY

# IME
fcitx5 &

exec cwm -c ~/.config/cwm/cwmrc

