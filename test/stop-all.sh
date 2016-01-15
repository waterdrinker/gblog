#!/bin/sh


if [ ! -e /var/run/nginx.pid ]; then
    echo "/var/run/nginx.pid didn't exist"
else
    echo "sudo nginx -s quit"
    sudo nginx -s quit
    #ps -ef |grep nginx|grep -v grep|awk '{print $2}'|xargs sudo kill -9
fi

if [ ! -e /run/supervisord.pid ]; then
    echo "/var/run/supervisord.pid didn't exist"
else
    echo "sudo supervisorctl stop all"
    echo "sudo pkill -9 supervisord"
    sudo pkill -9 supervisord
fi

ps -ef |grep gblog|grep -v grep|grep -v vim|awk '{print $2}'|xargs sudo kill -9
