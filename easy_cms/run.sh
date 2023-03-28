#!/bin/sh
sed -i "s/flag{test}/$FLAG/g" /f1Aggg
export FLAG=not_flag
service apache2 start
service mysql start
tail -f /dev/null