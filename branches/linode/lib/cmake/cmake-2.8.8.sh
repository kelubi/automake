#!/bin/bash


# Short one-line description of this package.
DESCRIPTION="CMake is a family of tools designed to build, test and package software. CMake is used to control the software compilation process using simple platform and compiler independent configuration files"
# Homepage, not used by Portage directly but handy for developer reference
HOMEPAGE="http://www.cmake.org/"
SRC_URI="http://www.cmake.org/files/v2.8/cmake-2.8.8.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="cmake"
V="2.8.8"

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
echo "make $N-$V$R..."
./configure --prefix=/usr
make
make install
echo "all done"

