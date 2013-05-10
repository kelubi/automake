#!/bin/bash

DESCRIPTION="This is fast memcached server"
HOMEPAGE="http://ops.dev.shopex.cn/"
SRC_URI="http://lnmpp.googlecode.com/files/memcached-1.4.6.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="memcached"
V="1.4.6"

if [ ! -d /opt/install ]; then
    mkdir -pv /opt/install
fi
echo "go to working dir"
cd /opt/install

if [ -s $PKG_NAME ]; then
  echo "$PKG_NAME [found]"
else
  echo "Error: $PKG_NAME not found!!!download now......"
  wget -c $SRC_URI
fi
echo "Unpacking to `pwd`"
tar xvf $PKG_NAME

echo "config $N-$V$R..."
cd $N-$V$R
./configure --prefix=/usr/local/memcached
sleep 1
echo "make $N-$V$R..."
make
echo "install to $XGPATH_DEST..."    
make  install
id www > /dev/null 2>&1
if [ $? -ne 0 ]; then
useradd -s /sbin/nologin -M  www
fi
/usr/local/memcached/bin/memcached -d -m 64  -uwww -p 11211
sed -i "\/usr\/local\/memcached\/bin\/memcached -d -m 64  -uwww -p 11211/d" /etc/rc.d/rc.local 
echo "/usr/local/memcached/bin/memcached -d -m 64  -uwww -p 11211" >> /etc/rc.local
echo "all done"
