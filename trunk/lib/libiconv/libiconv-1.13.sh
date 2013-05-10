#!/bin/bash
#

SRC_URI="http://lnmpp.googlecode.com/files/libiconv-1.13.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="libiconv"
V="1.13"

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


echo "init $N-$V$R build script..."

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

