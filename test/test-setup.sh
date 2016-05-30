#!/bin/sh

config_dir=~/.gblog

# 获取当前脚本的上层工作目录
curdir=$(cd $(dirname $0); cd ..; pwd)

#config_dir/data/gblog.conf ->  curdir/config
#config_dir/nginx.conf  ->  curdir/nginx.conf
#config_dir/supervisor.conf  ->  curdir/supervisor.conf

set -x

if [ ! -d $config_dir ]; then
    mkdir $config_dir
fi

if [ ! -L $curdir/data ]; then
    echo "data link doesn't exist"
    exit 1
fi

if [ ! -e $config_dir/config ]; then
    ln -s ${curdir}/data/gblog.conf $config_dir/config
fi

if [ ! -e $config_dir/supervisord.conf ]; then
    ln -s ${curdir}/supervisord.conf $config_dir
fi

if [ ! -e $config_dir/nginx.conf ]; then
    ln -s ${curdir}/nginx.conf $config_dir
fi

if [ ! -d /var/www ]; then
    mkdir /var/www
fi

if [ ! -d /var/www/http ]; then
    mkdir /var/www/http
fi

if [ ! -e /var/www/http/static ]; then
    ln -s ${curdir}/gblog/static /var/www/http/static
fi
