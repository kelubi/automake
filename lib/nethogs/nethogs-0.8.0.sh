#!/bin/bash
#

DESCRIPTION="view bandwidth per process"
HOMEPAGE="http://freshmeat.net/projects/fio/"
SRC_URI="http://lnmpp.googlecode.com/files/nethogs-0.8.0.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="nethogs"
V="0.8.0"

yum install -y libpcap libpcap-devel 
if [ -d /usr/lib64 ]; then
	push /usr/lib64
	ln -sv libpcap.so.0.9.4 libpcap.so
fi

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
make
make install
echo "all done"

#usage:

