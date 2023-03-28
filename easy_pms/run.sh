#!/bin/sh
sed -i "s/flag{test}/$FLAG/g" /flag
export FLAG=not_flag
/.docker_init.sh