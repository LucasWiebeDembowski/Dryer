#!/bin/bash
# Must be run as sudo or root.
if [ $(id -u) -eq 0 ]; then
    dryerScript="dryerV2.py"
    nohup python3 $dryerScript &
    echo "Started $dryerScript with PID $(ps -ef | awk '/root.*dryerV2.py/ {printf "%s\n", $2}' | head -n1)"
else
    echo "Error. Must be run as sudo or root."
    exit 1
fi
