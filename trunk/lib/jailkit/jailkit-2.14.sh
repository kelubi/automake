#!/bin/bash

DESCRIPTION="jail shell toolkit"
HOMEPAGE="http://olivier.sessink.nl/jailkit/howtos_chroot_shell.html"
SRC_URI="http://lnmpp.googlecode.com/files/jailkit-2.14.tar.bz2"
PKG_NAME=`basename $SRC_URI`
N="jailkit"
V="2.14"

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
./configure
make 
make install
#
jk_init -v -j /home/jail basicshell editors extendedshell netutils ssh sftp scp
jk_init -v -j /home/jail jk_lsh
#jk_jailuser -v -m -j /home/jail  test
#sed -i s,/usr/sbin/jk_lsh,/bin/bash,g  /home/jail/etc/passwd 
#mkdir /home/jail/proc
#mount -v proc /home/jail/proc -t proc
echo "all done"
