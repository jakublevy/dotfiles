#!/bin/sh

service_running() {
    systemctl is-active --quiet bluetooth.service
}

run_service() {
    sudo systemctl start bluetooth.service
}

power_on_bluetooth() {
    echo 'power on' | bluetoothctl &> /dev/null ; sleep 0.3 
}

connect_to_wacom() {
    echo 'connect DC:2C:26:DD:58:B4' | bluetoothctl &> /dev/null
}

service_running
if [ $? -ne 0 ]; then
    run_service
fi

power_on_bluetooth
connect_to_wacom
