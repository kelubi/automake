#!/bin/bash
#

SRC_URI="http://nodejs.org/dist/v0.8.16/node-v0.8.16.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="node"
V="v0.8.16"



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
tar xvf $PKG_NAME
echo "config $N-$V$R..."
cd $N-$V$R
echo "make $N-$V$R..."
./configure --prefix=/usr/local/node 
make
make install
ln -sv /usr/local/node/bin/node /usr/bin

echo "all done"

