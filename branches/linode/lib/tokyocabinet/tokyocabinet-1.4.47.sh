#!/bin/bash
#

DESCRIPTION="Perl Compatible Regular Expressions"
HOMEPAGE="http://fallabs.com/tokyocabinet/"
SRC_URI="http://lnmpp.googlecode.com/files/tokyocabinet-1.4.47.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="tokyocabinet"
V="1.4.47"

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
echo "Unpacking to `pwd`"
tar xvf  $PKG_NAME
#config
echo "config $N-$V$R..."
#fist, cd build directory
cd $N-$V$R
#Third, call configure with $XGB_CONFIG
./configure
#build
echo "make $N-$V$R..."
make
echo "checking $N-$V$R.."
#install everything to $XGPATH_DEST
make  install
#post install
echo "running after package installed..."