#!/bin/bash
#
# Xiange Linux build scripts

# Short one-line description of this package.
DESCRIPTION="This is scws extension for php"

# Homepage, not used by Portage directly but handy for developer reference
HOMEPAGE="http://ops.dev.shopex.cn/"

# Point to any required sources; these will be automatically downloaded by
# gpkg. 
# $N = package name, such as autoconf, x-org
# $V = package version, such as 2.6.10

#SRC_URI="http://mirrors.dev.shopex.cn/lnmpp/sources/scws-1.1.8.tar.bz2"
SRC_URI_SCWS="http://lnmpp.googlecode.com/files/scws-1.1.8.tar.bz2"
SRC_URI_DICT="http://lnmpp.googlecode.com/files/scws-dict-chs-utf8.tar.bz2"
PKG_NAME_SCWS=`basename $SRC_URI_SCWS`
PKG_NAME_DICT=`basename $SRC_URI_DICT`
N="scws"
V="1.1.8"

if [ ! -d /opt/install ]; then
	mkdir -pv /opt/install
fi
echo "go to working dir"
cd /opt/install

if [ -s $PKG_NAME_SCWS ]; then
	echo "$PKG_NAME_SCWS [found]"
else
	echo "Error: $PKG_NAME_SCWS not found!!!download now......"
	wget -c $SRC_URI_SCWS
fi

if [ -s $PKG_NAME_DICT ]; then
	echo "$PKG_NAME_DICT [found]"
else
	echo "Error: $PKG_NAME_DICT not found!!!download now......"
	wget -c $SRC_URI_DICT
fi

#init 
echo "Unpacking to `pwd`"
tar jxvf  $PKG_NAME_SCWS
#config
echo "config $N-$V..."
#fist, cd build directory
cd $N-$V
./configure --prefix=/usr/local/scws
echo "make $N-$V..."
make
make  install

mkdir /usr/local/scws/dict
tar jxvf /opt/install/$PKG_NAME_DICT -C /usr/local/scws/dict

cd phpext
/usr/local/php/bin/phpize
sleep 2
./configure --with-php-config=/usr/local/php/bin/php-config --with-scws=/usr/local/scws
make
make  install

PHPINI=$(/usr/local/php/bin/php -i | grep "Loaded Configuration File" | awk -F=\> '{print $2}')
PHPINI=$(echo $PHPINI;) 
EXTDIR=$(/usr/local/php/bin/php -i | grep extension_dir | awk -F=\> '{print $2}' | sed -n '1p')
EXTDIR=$(echo $EXTDIR;)
if [ -f "$EXTDIR/scws.so" ]; then
	sed -i '/\[scws\]/d' $PHPINI
	sed -i '/extension=scws.so/d' $PHPINI
	echo "[scws]" >> $PHPINI
	echo "extension=scws.so" >> $PHPINI
	echo "scws.default.charset = utf-8" >> $PHPINI
	echo "scws.default.fpath = /usr/local/scws/etc" >> $PHPINI
fi