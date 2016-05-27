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

if [ ! -e $curdir/data ]; then
    echo "data link doesn't exist"
    return
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

if [ ! -e /var/www/http ]; then
    ln -s ${curdir}/gblog /var/www/http
fi
