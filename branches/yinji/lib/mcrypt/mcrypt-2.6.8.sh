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
#SRC_URI="http://mirrors.dev.shopex.cn/lnmpp/sources/mcrypt-2.6.8.tar.gz"
SRC_URI="http://lnmpp.googlecode.com/files/mcrypt-2.6.8.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="mcrypt"
V="2.6.8"

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
echo "Unpacking to `pwd`"
tar xvf $PKG_NAME

echo "config $N-$V$R..."
cd $N-$V$R
./configure --prefix=/usr
sleep 1

echo "make $N-$V$R..."
cd $N-$V$R
make CC="$CC" CFLAGS="$CFLAGS"
echo "install to $XGPATH_DEST..."    
#install everything to $XGPATH_DEST
make install
/sbin/ldconfig
/sbin/ldconfig
echo "all done"