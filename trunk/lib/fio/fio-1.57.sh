#!/bin/bash
#
# Xiange Linux build scripts

# Short one-line description of this package.
DESCRIPTION="fio is an I/O tool meant to be used both for benchmark and stress/hardware verificatio"
# Homepage, not used by Portage directly but handy for developer reference
HOMEPAGE="http://freshmeat.net/projects/fio/"
SRC_URI="http://lnmpp.googlecode.com/files/fio-1.57.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="fio"
V="1.57"

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
echo "make $N-$V$R..."
make
ln -sv /usr/local/bin/fio /usr/bin/
echo "all done"

