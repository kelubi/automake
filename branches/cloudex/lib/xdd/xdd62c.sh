#!/bin/bash
#
# Xiange Linux build scripts

# Short one-line description of this package.
DESCRIPTION="fio is an I/O tool meant to be used both for benchmark and stress/hardware verificatio"
# Homepage, not used by Portage directly but handy for developer reference
HOMEPAGE="http://freshmeat.net/projects/fio/"
SRC_URI="http://lnmpp.googlecode.com/files/xdd62c.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="xdd62c"
V=""

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
echo "make $N..."
cd  $N
cp linux.makefile Makefile
make
install bin/xdd.linux /usr/bin/xdd 
echo "all done"

#usage:
#xdd -op rw -targets 2 /dev/sdb /dev/sdc -rwratio 80 -queuedepth 1 -blocksize 1024 -reqsize 128 -mbytes 2048 -passes 3 -verbose  -csvout /tmp/iotest.csv 
