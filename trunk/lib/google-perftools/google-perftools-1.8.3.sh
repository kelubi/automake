#!/bin/bash

DESCRIPTION=""
HOMEPAGE=""
SRC_URI="http://lnmpp.googlecode.com/files/google-perftools-1.8.3.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="google-perftools"
V="1.8.3"

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
CHOST="x86_64-pc-linux-gnu" \
CFLAGS="-O3 \
-lstdc++ \
-fomit-frame-pointer \
-pipe \
-march=nocona \
-mfpmath=sse \
-m128bit-long-double \
-mmmx \
-msse \
-msse2 \
-maccumulate-outgoing-args \
-m64 \
-ftree-loop-linear \
-fprefetch-loop-arrays \
-freg-struct-return \
-fgcse-sm \
-fgcse-las \
-frename-registers \
-fforce-addr \
-fivopts \
-ftree-vectorize \
-ftracer \
-frename-registers \
-minline-all-stringops \
-fbranch-target-load-optimize2" \
CXXFLAGS="${CFLAGS}" \
./configure
echo "make $N-$V$R..."
make
make install
echo "all done"

