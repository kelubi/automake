#!/bin/bash
#
# Xiange Linux build scripts

# Short one-line description of this package.
DESCRIPTION="This is fast memcached server"

# Homepage, not used by Portage directly but handy for developer reference
HOMEPAGE="http://ops.dev.shopex.cn/"

# Point to any required sources; these will be automatically downloaded by
# gpkg. 
# $N = package name, such as autoconf, x-org
# $V = package version, such as 2.6.10

#SRC_URI="http://foo.bar.com/$N-$V.tar.bz2"
#SRC_URI="http://mirrors.dev.shopex.cn/lnmpp/sources/memcached-1.4.5.tar.gz"
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
