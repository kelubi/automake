#!/bin/bash
#

DESCRIPTION="The Apache HTTP Server Project is a collaborative software development effort aimed at creating a robust, commercial-grade, featureful, and freely-available source code implementation of an HTTP (Web) server"
HOMEPAGE="http://httpd.apache.org"
SRC_URI="http://labs.mop.com/apache-mirror/apr/apr-util-1.4.1.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="apr-util"
V="1.4.1"

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
./configure --prefix=/usr/local/httpd/apr-util --with-apr=/usr/local/httpd/apr/bin/apr-1-config
make && make install

echo "all done"

#usage:

 