#!/bin/sh

service_running() {
    systemctl is-active --quiet bluetooth.service
}

stop_service() {
    sudo systemctl stop bluetooth.service
}

power_off_bluetooth() {
    echo 'power off' | bluetoothctl &> /dev/null
}

service_running
if [ $? -eq 0 ]; then
    power_off_bluetooth
    stop_service
fi
