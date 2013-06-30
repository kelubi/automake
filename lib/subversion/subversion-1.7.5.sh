#!/bin/bash
#
# Xiange Linux build scripts

# Short one-line description of this package.
DESCRIPTION="Subversion is an open source version control system. Founded in 2000 by CollabNet, Inc., the Subversion project and software have seen incredible success over the past decade"
# Homepage, not used by Portage directly but handy for developer reference
HOMEPAGE="http://subversion.apache.org/"
SRC_URI="http://www.fayea.com/apache-mirror/subversion/subversion-1.7.6.tar.bz2"
PKG_NAME=`basename $SRC_URI`
N="subversion"
V="1.7.6"

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
tar xf $PKG_NAME
echo "make $N..."
cd $N-$V$R
wget http://www.sqlite.org/sqlite-amalgamation-3071300.zip
unzip sqlite-amalgamation-3071300.zip 
if [ -d sqlite-amalgamation ]; then
	rm -rf sqlite-amalgamation
fi
mv sqlite-amalgamation-3071300 sqlite-amalgamation
./configure LDFLAGS="-L/usr/lib64 -L/lib64"  --with-ssl -with-zlib=/usr --enable-shared --enable-static --prefix=/usr --with-apr=/usr/local/httpd/apr --with-apr-util=/usr/local/httpd/apr-util --with-apxs=/usr/local/httpd/bin/apxs --with-neon 
echo "make $N-$V$R..."
CPU_NUM=$(cat /proc/cpuinfo | grep processor | wc -l)
if [ $CPU_NUM -gt 1 ];then
    make -j$CPU_NUM
else
    make
fi
make install

echo "all done"

