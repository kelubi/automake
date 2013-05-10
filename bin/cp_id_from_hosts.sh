#!/bin/bash
# This program is part of LNNPP: http://code.google.com/p/lnmpp

ssh_port_ready=''
ip=''

main () {
    gen_rsa_id
    cat /etc/hosts | grep -v ^#  | grep -v ^$ | while read line
    do
        ip=$(echo $line | awk '{print $1}')
        check_ssh_port
        if [ ! $ssh_port_ready ]; then
            echo "can not connect to $ip on 22"
            return
        fi
        ssh-copy-id -i ~/.ssh/id_rsa.pub $(whoami)@$ip
    done
}

check_ssh_port ()
{
    port="22"      
    (
        sleep 3
        echo logout
    ) | nc $ip $port > /tmp/cpid_temp.txt
    cou=`grep -c Connected /tmp/cpid_temp.txt`
    if [ $cou -gt 0 ]; then
        ssh_port_ready=1
    else
        ssh_port_ready=0
    fi
    [ -f /tmp/cpid_temp.txt ] && rm -f /tmp/cpid_temp.txt
}

gen_rsa_id()
{
    if [ ! -f ~/.ssh/id_rsa ]; then
        ssh-keygen -t rsa  -N ' '  -f ~/.ssh/id_rsa
    fi
}

main $@