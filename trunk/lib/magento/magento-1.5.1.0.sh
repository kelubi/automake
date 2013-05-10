#!/bin/bash
#
# Xiange Linux build scripts

# Short one-line description of this package.
DESCRIPTION="This is a sample skeleton xiange build script file"

# Homepage, not used by Portage directly but handy for developer reference
HOMEPAGE="http://ops.dev.shopex.cn/"

# Point to any required sources; these will be automatically downloaded by
# gpkg. 
# $N = package name, such as autoconf, x-org
# $V = package version, such as 2.6.10

#SRC_URI="http://foo.bar.com/$N-$V.tar.bz2"
#SRC_URI="http://mirrors.dev.shopex.cn/lnmpp/sources/libmcrypt-2.5.8.tar.gz"
SRC_URI="http://lnmpp.googlecode.com/files/magento-1.5.1.0.tar.bz2"
PKG_NAME=`basename $SRC_URI`
N="magento"
V="1.5.1.0"


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
mv magento/* .
rm -rf magento
chown ftpd:ftpd . -R
chown www:www app/etc   app skin var var/.htaccess js downloader
chown www:www -R media

echo "all done"
