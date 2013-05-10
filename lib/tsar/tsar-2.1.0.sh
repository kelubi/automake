#!/bin/bash
#

DESCRIPTION=""
HOMEPAGE="http://tsar.taobao.org/"
SRC_URI="http://lnmpp.googlecode.com/files/tsar-2.1.0.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="tsar"
V="2.1.0"

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
tar xf $PKG_NAME
echo "config $N-$V$R..."
cd $N-$V$R
echo "make $N-$V$R..."
./configure --prefix=/usr
make
make install
echo "all done"

#usage:
#tsar --load --live 
