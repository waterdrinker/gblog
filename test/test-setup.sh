#!/bin/sh

config_dir=~/.gblog

# 获取当前脚本的上层工作目录
proj_dir=$(cd $(dirname $0); cd ..; pwd)

#config_dir/data/gblog.conf ->  proj_dir/config
#config_dir/nginx.conf  ->  proj_dir/nginx.conf
#config_dir/supervisor.conf  ->  proj_dir/supervisor.conf

set -x

if [ ! -d $config_dir ]; then
    mkdir $config_dir
fi

if [ ! -L $proj_dir/data ]; then
    echo "data link doesn't exist"
    exit 1
fi

if [ ! -e $config_dir/config ]; then
    ln -s ${proj_dir}/data/gblog.conf $config_dir/config
fi

if [ ! -e $config_dir/supervisord.conf ]; then
    ln -s ${proj_dir}/supervisord.conf $config_dir
fi

if [ ! -e $config_dir/nginx.conf ]; then
    ln -s ${proj_dir}/nginx.conf $config_dir
fi

if [ ! -d /var/www ]; then
    mkdir /var/www
fi

if [ ! -d /var/www/http ]; then
    mkdir /var/www/http
fi

if [ ! -e /var/www/http/static ]; then
    ln -s ${proj_dir}/gblog/static /var/www/http/static
fi
