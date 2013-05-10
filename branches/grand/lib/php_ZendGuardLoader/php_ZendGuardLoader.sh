#!/bin/bash
#
# Xiange Linux build scripts

# Short one-line description of this package.
DESCRIPTION="This is ZendGuardLoader extension for php5.3.6"

# Homepage, not used by Portage directly but handy for developer reference
HOMEPAGE="http://ops.dev.shopex.cn/"

# Point to any required sources; these will be automatically downloaded by
# gpkg. 
# $N = package name, such as autoconf, x-org
# $V = package version, such as 2.6.10

PLATFORM=`uname -i`
SRC_URI="http://lnmpp.googlecode.com/files/ZendGuardLoader-php-5.3-linux-glibc23-$PLATFORM.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="ZendGuardLoader-php-5.3-linux-glibc23-$PLATFORM"

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

#unpard file from $XGPATH_SOURCE to current directory.
echo "Unpacking to `pwd`"
tar xvf $PKG_NAME
mv $N /usr/local/ZendGuardLoader

PHPINI="/usr/local/php/etc/php.ini"
echo "config php.ini add ZendGuardLoader mod..."
echo "[Zend Optimizer]" >> $PHPINI
echo "zend_extension="/usr/local/ZendGuardLoader/php-5.3.x/ZendGuardLoader.so" >> $PHPINI
echo "zend_loader.enable=1" >> $PHPINI
echo "zend_loader.disable_licensing=0" >> $PHPINI
echo "zend_loader.obfuscation_level_support=3" $PHPINI

##restart php-fpm 
echo "Now restart php-fpm to reload $PKG_NAME.so"
/etc/init.d/php-fpm reload
