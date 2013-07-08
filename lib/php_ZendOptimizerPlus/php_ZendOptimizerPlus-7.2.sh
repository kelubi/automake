#!/bin/bash
#
SRC_URI="https://github.com/zendtech/ZendOptimizerPlus/archive/master.zip"
PKG_NAME='master'


if [ ! -d /opt/install ]; then
    mkdir -pv /opt/install
fi
echo "go to working dir"
cd /opt/install

mkdir zendoptimizerplus
cd zendoptimizerplus/

if [ -s $PKG_NAME ]; then
  echo "$PKG_NAME [found]"
else
  echo "Error: $PKG_NAME not found!!!download now......"
  wget -c $SRC_URI
fi


unzip master
cd ZendOptimizerPlus-master/
/usr/local/php/bin/phpize
./configure --with-php-config=/usr/local/php/bin/php-config
make
make  install

PHPINI=$(/usr/local/php/bin/php -i | grep "Loaded Configuration File" | awk -F=\> '{print $2}')
PHPINI=$(echo $PHPINI;) 
EXTDIR=$(/usr/local/php/bin/php -i | grep extension_dir | awk -F=\> '{print $2}')
EXTDIR=$(echo $EXTDIR;)
if [ -f "$EXTDIR/eaccelerator.so" ]; then
	#clean up first
	sed -i '/\[ZendOptimizerPlus\]/d' $PHPINI
	sed -i '/zend_extension= "/usr/local/php/lib/php/extensions/no-debug-non-zts-20090626/opcache.so"/d' $PHPINI
	sed -i '/opcache.memory_consumption=128/d' $PHPINI
	sed -i '/opcache.interned_strings_buffer=8/d' $PHPINI
	sed -i '/opcache.max_accelerated_files=4000/d' $PHPINI
	sed -i '/opcache.revalidate_freq=60/d' $PHPINI
	sed -i '/opcache.fast_shutdown=1/d' $PHPINI
	sed -i '/opcache.enable_cli=1/d' $PHPINI
	#write new configure
	echo '[ZendOptimizerPlus]' >> $PHPINI
	echo 'zend_extension= "/usr/local/php/lib/php/extensions/no-debug-non-zts-20090626/opcache.so"' >> $PHPINI
	echo 'opcache.memory_consumption=128' >> $PHPINI
	echo 'opcache.interned_strings_buffer=8' >> $PHPINI
	echo 'opcache.max_accelerated_files=4000' >> $PHPINI
	echo 'opcache.revalidate_freq=60' >> $PHPINI
	echo 'opcache.fast_shutdown=1' >> $PHPINI
	echo 'opcache.enable_cli=1' >> $PHPINI
fi
