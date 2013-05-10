#!/bin/bash
#

DESCRIPTION="The Apache HTTP Server Project is a collaborative software development effort aimed at creating a robust, commercial-grade, featureful, and freely-available source code implementation of an HTTP (Web) server"
HOMEPAGE="http://httpd.apache.org"
SRC_URI="http://www.fayea.com/apache-mirror/httpd/httpd-2.4.3.tar.bz2"
PKG_NAME=`basename $SRC_URI`
N="httpd"
V="2.4.3"

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
./configure --prefix=/usr/local/httpd --with-apr=/usr/local/httpd/apr --with-apr-util=/usr/local/httpd/apr-util --with-mpm=prefork --enable-so --enable-rewrite=shared --enable-track-vars --enable-dav  --enable-maintainer-mode --enable-rewrite
make 
sudo make install
sudo cp support/apachectl /etc/rc.d/init.d/httpd
sudo chmod 0777 /etc/rc.d/init.d/httpd
sudo echo "#chkconfig: 345 85 15" >> /etc/rc.d/init.d/httpd
sudo echo "#description: Starts and stops the Apache HTTP Server." >> /etc/rc.d/init.d/httpd
sudo chown root:root /etc/rc.d/init.d/httpd
echo "all done"

#usage:

