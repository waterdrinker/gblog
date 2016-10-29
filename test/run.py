#!/bin/python

import sys
import os
import subprocess


def check_setup():
    cmd = './setup.sh'
    status = subprocess.call(cmd, shell=True)
    if status == 1:
        print("check_setup: error")
        sys.exit(0)


def prompt_sudo():
    ret = 0
    if os.geteuid() != 0:
        args = [sys.executable] + sys.argv
        os.execlp('sudo', 'sudo', *args)
    return os.geteuid()


def process_exist(process):
    cmd = 'ps -ef|grep "%s"|grep -v grep|grep -v vim' % process
    result = b""
    #print(cmd)

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  
    while p.poll() == None:  
        line = p.stdout.readline()  
        result = result + line  

    if result:
        return True
    else:
        return False


def main():
    if prompt_sudo() != 0:
        print("the user wasn't authenticated as a sudoer, exit.")
        sys.exit(0)

    # check database
    if not process_exist("mysqld\\|mariadb"):
        print("no mysqld or mariadb is found")
        sys.exit(0)

    # search old process
    if process_exist("gblog"):
        print("gblog process find")

    # check configure files and links
    check_setup()

    # restart supervisord and nginx
    if process_exist("supervisord"):
        print("process supervisord exist, restart gblogs:*")
        cmd = 'supervisorctl restart gblogs:*'
        subprocess.call(cmd, shell=True)
    else:
        print('supervisord -c ~/.gblog/supervisord.conf')
        cmd = 'supervisord -c ~/.gblog/supervisord.conf'
        subprocess.call(cmd, shell=True)
        print("supervisorctl start gblogs:*")
        cmd = 'supervisorctl start gblogs:*'
        subprocess.call(cmd, shell=True)

    if process_exist("nginx"):
        print("process nginx exist, restart it")
        cmd = 'nginx -s reload'
        subprocess.call(cmd, shell=True)
    else:
        print('nginx -c ~/.gblog/nginx.conf')
        cmd = 'nginx -c ~/.gblog/nginx.conf'
        subprocess.call(cmd, shell=True)


if __name__ == "__main__":
    main()
