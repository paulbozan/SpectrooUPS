#!/bin/bash

CONFIG=/boot/config.txt
echo "Adding gpio=25=op,dl config.txt if not exists"
    if grep -Fxq "gpio=25=op,dl" $CONFIG
    then
       echo "Key gpio=25=op,dl is already in config.txt"
       cat $CONFIG | grep -a "gpio"
    else
       echo "Key gpio=25=op,dl NOT FOUND in config.txt"
       echo "" | sudo tee -a $CONFIG
       echo "#Used for SpectrooUPS" | sudo tee -a $CONFIG
       echo "gpio=25=op,dl" | sudo tee -a $CONFIG
       echo "********cat*********"
       cat $CONFIG | grep -a "gpio"
    fi

echo "Installing systemd service"

mkdir /usr/share/spectrooups

cp spectroo_ups.py /usr/share/spectrooups/spectroo_ups.py

systemctl stop spectrooups.service

cp spectrooups.service /etc/systemd/system/spectrooups.service

systemctl daemon-reload

systemctl start spectrooups.service

systemctl enable spectrooups.service

systemctl status spectrooups.service
