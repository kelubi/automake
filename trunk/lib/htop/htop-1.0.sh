#!/bin/bash
#

DESCRIPTION="fio is an I/O tool meant to be used both for benchmark and stress/hardware verificatio"
HOMEPAGE="http://freshmeat.net/projects/fio/"
SRC_URI="http://lnmpp.googlecode.com/files/htop-1.0.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="htop"
V="1.0"

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

