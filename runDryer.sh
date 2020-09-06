#!/bin/bash
dryerScript="dryermonitor.py"
nohup python3 $dryerScript &
echo "Started $dryerScript with PID $(pgrep -f "python3 $dryerScript")"
