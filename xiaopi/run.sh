#!/bin/sh
sed -i "s/flag{test}/$FLAG/g" /flag
export FLAG=not_flag
python3 /robot/robot.py &
/opt/main.sh