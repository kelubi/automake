#!/bin/bash
#

SRC_URI="http://www.erlang.org/download/otp_src_R16B.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="otp_src"
V="R16B"

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
cd otp_src_R16B
echo "make $N-$V$R..."
./configure --prefix=/usr/local/erlang
CPU_NUM=$(cat /proc/cpuinfo | grep processor | wc -l)
if [ $CPU_NUM -gt 1 ];then
    make -j$CPU_NUM
else
    make
fi
make install

ln -sv /usr/local/erlang/bin/erl /usr/bin
ln -sv /usr/local/erlang/bin/erlc /usr/bin

erl -v

echo "all done"

