#!/bin/bash
# Must be run as sudo or root.
if [ $(id -u) -eq 0 ]; then
    dryerScript="dryerV2.py"
    nohup python3 $dryerScript &
    echo "Started $dryerScript with PID $(pgrep -f "python3 $dryerScript")"
else
    echo "Error. Must be run as root."
    exit 1
fi
