#!/bin/sh

config_dir=$1

# 获取当前脚本的上层工作目录
curdir=$(cd $(dirname $0); cd ..; pwd)

if [ ! -d $config_dir ]; then
    mkdir $config_dir
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
