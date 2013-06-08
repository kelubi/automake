#!/bin/bash
#
DESCRIPTION="This is a sample skeleton xiange build script file"
HOMEPAGE="http://ops.dev.shopex.cn/"
SRC_URI="https://launchpad.net/libmemcached/1.0/1.0.16/+download/libmemcached-1.0.16.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="libmemcached"
V="1.0.16"

yum install -y gcc44 gcc44-c++ libstdc++44-devel

export CC=/usr/bin/gcc44
export CXX=/usr/bin/g++44

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

#init 
echo "init $N-$V$R build script..."
#unpack
#unpard file from $XGPATH_SOURCE to current directory.
echo "Unpacking to `pwd`"
tar xvf $PKG_NAME

echo "config $N-$V$R..."
cd $N-$V$R
./configure --prefix=/usr --with-memcached=/usr/local/memcache/bin/memcached
sleep 1
echo "make $N-$V$R..."
make
make  install
ln -sv /usr/lib/libmemcached.so /usr/lib64
ln -sv /usr/lib/libmemcached.so.11 /usr/lib64
/sbin/ldconfig

echo "all done"

