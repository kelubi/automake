#!/bin/bash

HOMEPAGE="http://help.aliyun.com/manual?spm=0.0.0.112.xvDYLb&helpId=779"
if [ ! -d /opt/install ]; then
    mkdir -pv /opt/install
fi
echo "go to working dir"
cd /opt/install


wget -c 'http://imgs-storage.cdn.aliyuncs.com/jiankongagent.i386.rpm?spm=0.0.0.111.00Deur&file=jiankongagent.'$(uname -m)'.rpm' -O jiankongagent.rpm

if [ ! -e jiankongagent.rpm ]; then
	echo "jiankongagent.rpm not found"
	return 1;
fi

rpm -ivh jiankongagent.rpm
#todo
#get token from aliyun cpanel
echo "all done"
