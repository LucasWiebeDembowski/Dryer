#!/bin/bash
dryerScript="dryermonitor.py"
pkill -f "python3 $dryerScript" && echo "Successfully killed dryer" || echo "Could not kill dryer."
