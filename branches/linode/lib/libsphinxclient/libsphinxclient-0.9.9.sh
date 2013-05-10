#!/bin/bash
#
# Xiange Linux build scripts

# Short one-line description of this package.
DESCRIPTION="This is sphinx extension for php"

# Homepage, not used by Portage directly but handy for developer reference
HOMEPAGE="http://ops.dev.shopex.cn/"

# Point to any required sources; these will be automatically downloaded by
# gpkg. 
# $N = package name, such as autoconf, x-org
# $V = package version, such as 2.6.10

#SRC_URI="http://mirrors.dev.shopex.cn/lnmpp/sources/sphinx-0.9.9.tar.gz"
SRC_URI="http://lnmpp.googlecode.com/files/sphinx-0.9.9.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="sphinx"
V="0.9.9"

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
tar xvf $PKG_NAME
echo "config $N-$V..."
cd $N-$V/api/libsphinxclient
sed -i 's,static void sock_close ( int sock ),void sock_close ( int sock ),'  sphinxclient.c
./configure
make
make  install
echo "running after package installed..."