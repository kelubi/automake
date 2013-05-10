#!/bin/bash
DESCRIPTION="Automatically restart SSH sessions and tunnels"
HOMEPAGE="http://www.harding.motd.ca/autossh/index.html"
SRC_URI="http://lnmpp.googlecode.com/files/autossh-1.4b.tgz"
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

