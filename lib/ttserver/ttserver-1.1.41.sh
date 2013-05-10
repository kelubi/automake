#!/bin/bash
#

# Homepage, not used by Portage directly but handy for developer reference

# Point to any required sources; these will be automatically downloaded by
# gpkg. 
# $N = package name, such as autoconf, x-org
# $V = package version, such as tokyocabinet-1.4.47 and tokyotyrant-1.1.41

SRC_URI1="http://fallabs.com/tokyocabinet/tokyocabinet-1.4.47.tar.gz"
SRC_URI2="http://fallabs.com/tokyotyrant/tokyotyrant-1.1.41.tar.gz"

PKG_NAME1=`basename $SRC_URI1`
PKG_NAME2=`basename $SRC_URI2`
N1="tokyocabinet"
V1="1.4.47"
N2="tokyotyrant"
V2="1.1.41"

if ! rpm -qa |grep bzip2-devel ; then 
   yum install bzip2-devel -y 
fi

if [ ! -d /opt/install ]; then
    mkdir -pv /opt/install
fi
echo "go to working dir"
cd /opt/install

if [ -s $PKG_NAME1 ]; then
  echo "$PKG_NAME1 [found]"
  else
  echo "Error: $PKG_NAME1 not found!!!download now......"
  wget -c $SRC_URI1
fi

#init 
echo "init $N1-$V1$R build script..."
#unpack
#unpard file from $XGPATH_SOURCE to current directory.
echo "Unpacking to `pwd`"
tar xvf $PKG_NAME1
cd $N1-$V1

./configure --prefix=/usr/local/tc
make
make  install

if [ -s $PKG_NAME2 ]; then
  echo "$PKG_NAME2 [found]"
  else
  echo "Error: $PKG_NAME1 not found!!!download now......"
  wget -c $SRC_URI2
fi

#init 
echo "init $N2-$V2$R build script..."
#unpack
#unpard file from $XGPATH_SOURCE to current directory.
echo "Unpacking to `pwd`"
tar xvf $PKG_NAME2
cd $N2-$V2

./configure --prefix=/usr/local/ttserver --with-tc=/usr/local/tc/
make
make  install

echo "start ttserver server"
/usr/local/ttserver/sbin/ttservctl start
