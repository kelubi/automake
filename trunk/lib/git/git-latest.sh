#!/bin/bash
#

SRC_URI="http://www.codemonkey.org.uk/projects/git-snapshots/git/git-latest.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="git"
V="latest"

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
yum install -y zlib-devel
yum install -y openssl-devel
yum install -y perl
yum install -y cpio
yum install -y expat-devel
yum install -y gettext-devel

cat  >/etc/ld.so.conf.d/local.lib.conf<<'END'
/usr/local/lib
END
ldconfig

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

