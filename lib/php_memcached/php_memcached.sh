#!/bin/bash
#
# Xiange Linux build scripts

# Short one-line description of this package.
DESCRIPTION="This is memcached extension for php"

# Homepage, not used by Portage directly but handy for developer reference
HOMEPAGE="http://ops.dev.shopex.cn/"

# Point to any required sources; these will be automatically downloaded by
# gpkg. 
# $N = package name, such as autoconf, x-org
# $V = package version, such as 2.6.10


SRC_URI="http://pecl.php.net/get/memcached-2.1.0.tgz"
PKG_NAME=`basename $SRC_URI`
N="memcached"
V="2.1.0"

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
cd   $N-$V$R
/usr/local/php/bin/phpize
./configure  --with-php-config=/usr/local/php/bin/php-config
make
make  install

PHPINI=$(/usr/local/php/bin/php -i | grep "Loaded Configuration File" | awk -F=\> '{print $2}')
PHPINI=$(echo $PHPINI;) 
EXTDIR=$(/usr/local/php/bin/php -i | grep extension_dir | awk -F=\> '{print $2}' | sed -n '1p')
EXTDIR=$(echo $EXTDIR;)
if [ -f "$EXTDIR/memcached.so" ]; then
    sed -i '/\[memcached\]/d' $PHPINI
    sed -i '/extension=memcached.so/d' $PHPINI
    echo "[memcached]" >> $PHPINI
    echo "extension=memcached.so" >> $PHPINI
fi
