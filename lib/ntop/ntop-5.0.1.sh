#!/bin/bash
#

DESCRIPTION="view bandwidth per process"
HOMEPAGE="http://freshmeat.net/projects/fio/"
SRC_URI="http://lnmpp.googlecode.com/files/ntop-5.0.1.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="ntop"
V="5.0.1"

yum install -y gdbm gdbm-devel 

ln -sv /usr/lib64/libgdbm.so.2.0.0  /usr/lib64/libgdbm.so

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

