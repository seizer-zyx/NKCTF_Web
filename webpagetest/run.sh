#!/bin/sh
sed -i "s/flag{test}/$FLAG/g" /flag
export FLAG=not_flag
service apache2 start
tail -f /dev/null