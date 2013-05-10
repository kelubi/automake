#!/bin/bash
#
# Xiange Linux build scripts

# Short one-line description of this package.
DESCRIPTION="Automatically restart SSH sessions and tunnels"

# Homepage, not used by Portage directly but handy for developer reference
HOMEPAGE="http://www.harding.motd.ca/autossh/index.html"

# Point to any required sources; these will be automatically downloaded by
# gpkg. 
# $N = package name, such as autoconf, x-org
# $V = package version, such as 2.6.10

#SRC_URI="http://foo.bar.com/$N-$V.tar.bz2"
#SRC_URI="http://mirrors.dev.shopex.cn/lnmpp/sources/libiconv-1.13.tar.gz"
SRC_URI="http://www.harding.motd.ca/autossh/autossh-1.4b.tgz"
PKG_NAME=`basename $SRC_URI`
N="autossh"
V="1.4b"

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
echo "Unpacking to `pwd`"
tar xvf $PKG_NAME

echo "config $N-$V$R..."
cd $N-$V$R
./configure --prefix=/usr
sleep 1
echo "make $N-$V$R..."
make
make  install


echo "all done"

