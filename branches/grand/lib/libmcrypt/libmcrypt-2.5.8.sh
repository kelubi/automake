#!/bin/bash
#
# Xiange Linux build scripts

# Short one-line description of this package.
DESCRIPTION="This is a sample skeleton xiange build script file"

# Homepage, not used by Portage directly but handy for developer reference
HOMEPAGE="http://ops.dev.shopex.cn/"

# Point to any required sources; these will be automatically downloaded by
# gpkg. 
# $N = package name, such as autoconf, x-org
# $V = package version, such as 2.6.10

#SRC_URI="http://foo.bar.com/$N-$V.tar.bz2"
#SRC_URI="http://mirrors.dev.shopex.cn/lnmpp/sources/libmcrypt-2.5.8.tar.gz"
SRC_URI="http://lnmpp.googlecode.com/files/libmcrypt-2.5.8.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="libmcrypt"
V="2.5.8"

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
S_DIR=$(pwd)
./configure --prefix=/usr
sleep 1
echo "make $N-$V$R..."
make 
echo "install to $XGPATH_DEST..."
make  install

echo "running after package installed..."
/sbin/ldconfig
/sbin/ldconfig
cd $S_DIR/libltdl/
./configure --prefix=/usr --enable-ltdl-install
make && make install
/sbin/ldconfig
/sbin/ldconfig
echo "all done"
