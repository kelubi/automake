#!/bin/bash
# Short one-line description of this package.
DESCRIPTION="proftpd ftp server"
# Homepage, not used by Portage directly but handy for developer reference
HOMEPAGE="http://www.proftpd.org/"
SRC_URI="http://downloads.sourceforge.net/project/phpmyadmin/phpMyAdmin/3.5.1/phpMyAdmin-3.5.1-all-languages.tar.bz2"
PKG_NAME=$(basename $SRC_URI)
N="phpMyAdmin"
V="3.5.1"

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
echo "Unpacking to pwd"
tar xvf $PKG_NAME



echo "all done"