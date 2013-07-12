#!/bin/bash
#

SRC_URI="http://downloads.sourceforge.net/project/gnuplot/gnuplot/4.6.3/gnuplot-4.6.3.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="gnuplot"
V="4.6.3"

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


#unpack
#unpard file from $XGPATH_SOURCE to current directory.
echo "Unpacking to `pwd`"
tar xvf $PKG_NAME
echo "config $N-$V$R..."
cd $N-$(date  +"%Y-%m-%d")
echo "make $N-$V$R..."
autoconf
./configure --prefix=/usr 
make
make install

echo "all done"

