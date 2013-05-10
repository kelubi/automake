#!/bin/bash
#
# Xiange Linux build scripts

# Short one-line description of this package.
DESCRIPTION="optimizer for php"

# Homepage, not used by Portage directly but handy for developer reference
HOMEPAGE="http://ops.dev.shopex.cn/"

# Point to any required sources; these will be automatically downloaded by
# gpkg. 
# $N = package name, such as autoconf, x-org
# $V = package version, such as 2.6.10

#SRC_URI="http://foo.bar.com/$N-$V.tar.bz2"
#SRC_URI="http://mirrors.dev.shopex.cn/lnmpp/sources/zend-3.3.9.tar.gz"
SRC_URI="http://lnmpp.googlecode.com/files/zend-3.3.9.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="zend"
V="3.3.9"

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
F_DEST=/usr/local/zend
if [ ! -d $F_DEST ]; then
    mkdir -pv $F_DEST
fi
if [ `getconf WORD_BIT` = '32' ] && [ `getconf LONG_BIT` = '64' ] ; then
    cp 64/ZendOptimizer.so $F_DEST
else
    cp 32/ZendOptimizer.so $F_DEST
fi
echo "running after package installed..."
PHPINI=$(/usr/local/php/bin/php -i | grep "Loaded Configuration File" | awk -F=\> '{print $2}')
sed -i '/\[Zend Optimizer\]/d' $PHPINI
sed -i '/zend_optimizer.optimization_level=1/d' $PHPINI
sed -i '/zend_extension="\/usr\/local\/zend\/ZendOptimizer.so"/d' $PHPINI
#
echo "[Zend Optimizer]" >> $PHPINI
echo "zend_optimizer.optimization_level=1" >> $PHPINI
echo "zend_extension=\"/usr/local/zend/ZendOptimizer.so\"" >> $PHPINI
#
/sbin/service php-fpm stop
/sbin/service php-fpm start
#
echo "all done"
