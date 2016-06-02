#!/bin/sh

config_dir=~/.gblog

# 获取当前脚本的上层工作目录
proj_dir=$(cd $(dirname $0); cd ..; pwd)

#config_dir/data ->  proj_dir

set -x

if [ ! -L $config_dir ] && [ -e $config_dir ]; then
    rm $config_dir -rf
fi

if [ ! -L $proj_dir/data ]; then
    echo "data link doesn't exist"
    exit 1
fi

if [ ! -L $config_dir ]; then
    ln -s ${proj_dir}/data $config_dir
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
