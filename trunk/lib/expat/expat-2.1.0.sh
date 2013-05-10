#!/bin/bash
#
# Xiange Linux build scripts

# Short one-line description of this package.
DESCRIPTION="Expat is an XML parser library written in C"
# Homepage, not used by Portage directly but handy for developer reference
HOMEPAGE="http://expat.sourceforge.net/"
SRC_URI="http://lnmpp.googlecode.com/files/expat-2.1.0.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="expat"
V="2.1.0"

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
./configure --prefix=/usr
make
make install
echo "all done"

