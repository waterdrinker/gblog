#!/bin/sh

if [ $(id -u) -ne 0 ]; then
    echo "please re-run $(basename $0) as root!"
    exit 1
fi

# configure files dir
config_dir=~/.gblog
# obtain the parent dir of this script
proj_dir=$(cd $(dirname $0); cd ..; pwd)

if [ ! -L $config_dir ]; then
    echo "Please create a link \"~/.gblog\" to your configure files directory!"
    exit 1
fi

# link static files to /var/www/http
if [ ! -d /var/www ]; then
    mkdir /var/www
fi

if [ ! -d /var/www/http ]; then
    mkdir /var/www/http
fi

if [ ! -e /var/www/http/static ]; then
    ln -s ${proj_dir}/gblog/static /var/www/http/static
fi
