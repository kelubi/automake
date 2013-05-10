#!/bin/bash
#

DESCRIPTION="eAccelerator is a free open-source PHP accelerator & optimizer. It increases the performance of PHP scripts by caching them in their compiled state, so that the overhead of compiling is almost completely eliminated."
HOMEPAGE="http://eaccelerator.net/"
SRC_URI="http://lnmpp.googlecode.com/files/eaccelerator-0.9.6.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="eaccelerator"
V="eaccelerator-42067ac"

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
sleep 1
make
make  install

PHPINI=$(/usr/local/php/bin/php -i | grep "Loaded Configuration File" | awk -F=\> '{print $2}')
PHPINI=$(echo $PHPINI;) 
EXTDIR=$(/usr/local/php/bin/php -i | grep extension_dir | awk -F=\> '{print $2}')
EXTDIR=$(echo $EXTDIR;)
if [ -f "$EXTDIR/eaccelerator.so" ]; then
	#clean up first
	sed -i '/\[eaccelerator\]/d' $PHPINI
	sed -i '/extension=eaccelerator.so/d' $PHPINI
	sed -i '/eaccelerator.shm_size = "16"/d' $PHPINI
	sed -i '/eaccelerator.cache_dir = "/tmp/eaccelerator"/d' $PHPINI
	sed -i '/eaccelerator.enable = "1"/d' $PHPINI
	sed -i '/eaccelerator.optimizer = "1"/d' $PHPINI
	sed -i '/eaccelerator.check_mtime = "1"/d' $PHPINI
	sed -i '/eaccelerator.debug = "0"/d' $PHPINI
	sed -i '/eaccelerator.filter = ""/d' $PHPINI
	sed -i '/eaccelerator.shm_max = "0"/d' $PHPINI
	sed -i '/eaccelerator.shm_ttl = "0"/d' $PHPINI
	sed -i '/eaccelerator.prune_period = "0"/d' $PHPINI
	sed -i '/eaccelerator.shm_only = "0"/d' $PHPINI
	sed -i '/eaccelerator.compress = "1"/d' $PHPINI
	sed -i '/eaccelerator.compress_level = "9"/d' $PHPINI
	#write new configure
	echo "[eaccelerator]" >> $PHPINI
	echo "extension=eaccelerator.so" >> $PHPINI
	echo 'eaccelerator.shm_size = "16"' >> $PHPINI
	echo 'eaccelerator.cache_dir = "/tmp/eaccelerator"' >> $PHPINI
	echo 'eaccelerator.enable = "1"' >> $PHPINI
	echo 'eaccelerator.optimizer = "1"' >> $PHPINI
	echo 'eaccelerator.check_mtime = "1"' >> $PHPINI
	echo 'eaccelerator.debug = "0"' >> $PHPINI
	echo 'eaccelerator.filter = ""' >> $PHPINI
	echo 'eaccelerator.shm_max = "0"' >> $PHPINI
	echo 'eaccelerator.shm_ttl = "0"' >> $PHPINI
	echo 'eaccelerator.prune_period = "0"' >> $PHPINI
	echo 'eaccelerator.shm_only = "0"' >> $PHPINI
	echo 'eaccelerator.compress = "1"' >> $PHPINI
	echo 'eaccelerator.compress_level = "9"' >> $PHPINI
fi
