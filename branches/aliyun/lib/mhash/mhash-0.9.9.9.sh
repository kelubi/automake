#!/bin/bash
#
# Xiange Linux build scripts

# Short one-line description of this package.
DESCRIPTION="This is a sample skeleton xiange build script file"

# Homepage, not used by Portage directly but handy for developer reference
HOMEPAGE="http://ops.dev.shopex.cn/"

#SRC_URI="http://mirrors.dev.shopex.cn/lnmpp/sources/mhash-0.9.9.9.tar.gz"
SRC_URI="http://lnmpp.googlecode.com/files/mhash-0.9.9.9.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="mhash"
V="0.9.9.9"

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
./configure --prefix=/usr

echo "make $N-$V$R..."
CPU_NUM=$(cat /proc/cpuinfo | grep processor | wc -l)
if [ $CPU_NUM -gt 1 ];then
    make -j$CPU_NUM
else
    make
fi
make  install
#echo "running after package installed..."
#ln -s /usr/local/lib/libmcrypt.la /usr/lib/libmcrypt.la
#ln -s /usr/local/lib/libmcrypt.so /usr/lib/libmcrypt.so
#ln -s /usr/local/lib/libmcrypt.so.4 /usr/lib/libmcrypt.so.4
#ln -s /usr/local/lib/libmcrypt.so.4.4.8 /usr/lib/libmcrypt.so.4.4.8
#ln -s /usr/local/lib/libmhash.a /usr/lib/libmhash.a
#ln -s /usr/local/lib/libmhash.la /usr/lib/libmhash.la
#ln -s /usr/local/lib/libmhash.so /usr/lib/libmhash.so
#ln -s /usr/local/lib/libmhash.so.2 /usr/lib/libmhash.so.2
#ln -s /usr/local/lib/libmhash.so.2.0.1 /usr/lib/libmhash.so.2.0.1
/sbin/ldconfig
/sbin/ldconfig
echo "'all done"
