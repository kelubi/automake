#!/bin/bash
#
# Xiange Linux build scripts

# Short one-line description of this package.
DESCRIPTION="This is sphinx extension for php"

# Homepage, not used by Portage directly but handy for developer reference
HOMEPAGE="http://ops.dev.shopex.cn/"

# Point to any required sources; these will be automatically downloaded by
# gpkg. 
# $N = package name, such as autoconf, x-org
# $V = package version, such as 2.6.10

#SRC_URI="http://foo.bar.com/$N-$V.tar.bz2"
#SRC_URI="http://mirrors.dev.shopex.cn/lnmpp/sources/sphinx-1.1.0.tgz"
SRC_URI="http://lnmpp.googlecode.com/files/sphinx-1.1.0.tgz"
PKG_NAME=`basename $SRC_URI`
N="sphinx"
V="1.1.0"

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

#install libsphinxclient
curl  http://lnmpp.googlecode.com/svn/trunk/lib/libsphinxclient/libsphinxclient-0.9.9.sh | sh

#init 
echo "init $N-$V build script..."
#unpack
#unpard file from $XGPATH_SOURCE to current directory.
echo "Unpacking to `pwd`"
tar xvf $PKG_NAME

echo "config $N-$V..."
cd  $N-$V
/usr/local/php/bin/phpize
sleep 2
./configure --with-php-config=/usr/local/php/bin/php-config --with-sphinx
make
make  install

PHPINI=$(/usr/local/php/bin/php -i | grep "Loaded Configuration File" | awk -F=\> '{print $2}')
PHPINI=$(echo $PHPINI;) 
EXTDIR=$(/usr/local/php/bin/php -i | grep extension_dir | awk -F=\> '{print $2}' | sed -n '1p')
EXTDIR=$(echo $EXTDIR;)
if [ -f "$EXTDIR/sphinx.so" ]; then
	sed -i '/\[sphinx\]/d' $PHPINI
	sed -i '/extension=sphinx.so/d' $PHPINI
	echo "[sphinx]" >> $PHPINI
	echo "extension=sphinx.so" >> $PHPINI
fi