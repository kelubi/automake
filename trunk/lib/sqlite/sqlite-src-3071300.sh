#!/bin/bash
#
# Xiange Linux build scripts

# Short one-line description of this package.
DESCRIPTION="SQLite is a in-process library that implements a self-contained, serverless, zero-configuration, transactional SQL database engine"
# Homepage, not used by Portage directly but handy for developer reference
HOMEPAGE="http://www.sqlite.org"
SRC_URI="http://www.sqlite.org/sqlite-src-3071300.zip"
PKG_NAME=`basename $SRC_URI`
N="sqlite-src"
V="3071300"

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
unzip $PKG_NAME
echo "make $N..."
cd $N-$V$R
./configure --prefix=/usr
echo "make $N-$V$R..."
CPU_NUM=$(cat /proc/cpuinfo | grep processor | wc -l)
if [ $CPU_NUM -gt 1 ];then
    make -j$CPU_NUM
else
    make
fi
make install

echo "all done"

