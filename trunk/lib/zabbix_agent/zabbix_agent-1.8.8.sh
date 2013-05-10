#!/bin/bash
#
# Xiange Linux build scripts

# Short one-line description of this package.
DESCRIPTION="This is a sample skeleton xiange build script file"

# Homepage, not used by Portage directly but handy for developer reference
HOMEPAGE="http://ops.dev.shopex.cn/"

# Point to any required sources; these will be automatically downloaded by
# gpkg. 
# $N = package name, such as autoconf, x-org
# $V = package version, such as 2.6.10

#SRC_URI="http://foo.bar.com/$N-$V.tar.bz2"
#SRC_URI="http://mirrors.dev.shopex.cn/lnmpp/sources/libiconv-1.13.tar.gz"
SRC_URI="http://lnmpp.googlecode.com/files/zabbix-1.8.8.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="zabbix"
V="1.8.8"

if [ ! -d /opt/install ]; then
    mkdir -pv /opt/install
fi
echo "go to working dir"
cd /opt/install

if [ -s $PKG_NAME ]; then
  echo "$PKG_NAME [found]"
else
  echo "Error: $PKG_NAME not found!!!download now......"
  wget  $SRC_URI
fi

#init 
echo "init $N-$V$R build script..."
#unpack
#unpard file from $XGPATH_SOURCE to current directory.
echo "Unpacking to `pwd`"
tar xvf $PKG_NAME

echo "config $N-$V$R..."
cd $N-$V$R
./configure --prefix=/usr/local/zabbix --enable-agent  
sleep 1
echo "make $N-$V$R..."
make
make  install

if [ ! -d /etc/zabbix ]; then
    mkdir /etc/zabbix
fi
id zabbix > /dev/null 2>&1
if [ $? -ne 0 ]; then
useradd -s /sbin/nologin -M  zabbix
fi
install -v -m755 -o zabbix -g zabbix -d /var/run/zabbix
install -v -m755 -o zabbix -g zabbix -d /var/log/zabbix

cat >/etc/zabbix/zabbix_agentd.conf<<'EOF' 
ServerPort=10051
ListenPort=10050
ListenIP=0.0.0.0
StartAgents=5
DebugLevel=0
PidFile=/var/run/zabbix/zabbix_agentd.pid
LogFile=/var/log/zabbix/zabbix_agentd.log
Timeout=3
Server=60.191.142.3
Hostname=localhost.localdomain
EOF

install -v -m777 misc/init.d/fedora/core5/zabbix_agentd  /etc/init.d/zabbix_agentd
sed -i s,^ZABBIX_BIN=.*,ZABBIX_BIN="/usr/local/zabbix/sbin/zabbix_agentd",g  /etc/init.d/zabbix_agentd
/sbin/chkconfig zabbix_agentd --level 3 on
/sbin/service zabbix_agentd start
echo "all done"

