#!/bin/bash
#

SRC_URI="http://phantomjs.googlecode.com/files/phantomjs-1.7.0-source.zip"
PKG_NAME=`basename $SRC_URI`
N="phantomjs"
V="1.7.0"



if [ ! -d /opt/install ]; then
    mkdir -pv /opt/install
fi
echo "go to working dir"
cd /opt/install

if [ -s $PKG_NAME ]; then
  echo "$PKG_NAME [found]"
else
  echo "Error: $PKG_NAME not found!!!download now......"
  wget --no-check-certificate -c $SRC_URI
fi

#init 
echo "init $N-$V$R build script..."
#unpack
#unpard file from $XGPATH_SOURCE to current directory.
echo "Unpacking to `pwd`"
unzip $PKG_NAME
echo "config $N-$V$R..."
cd $N-$V$R
echo "make $N-$V$R..."
./configure 
make
make install

echo "all done"

