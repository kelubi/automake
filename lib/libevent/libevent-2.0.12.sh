#!/bin/bash
#
DESCRIPTION="This is a sample skeleton xiange build script file"
HOMEPAGE="http://ops.dev.shopex.cn/"
SRC_URI="http://lnmpp.googlecode.com/files/libevent-2.0.12-stable.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="libevent"
V="2.0.12-stable"

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
./configure --prefix=/usr
sleep 1
echo "make $N-$V$R..."
make
make  install
/sbin/ldconfig

echo "all done"

