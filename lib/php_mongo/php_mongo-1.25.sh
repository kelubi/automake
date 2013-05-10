#!/bin/bash
#

SRC_URI="http://lnmpp.googlecode.com/files/php-mongo-1.25.zip"
PKG_NAME=`basename $SRC_URI`
N="php-mongo"
V="1.25"

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
unzip $PKG_NAME

echo "config $N-$V$R..."
cd   $N-$V$R
/usr/local/php/bin/phpize
./configure  --with-php-config=/usr/local/php/bin/php-config
sleep 1
make
make  install

PHPINI=$(/usr/local/php/bin/php -i | grep "Loaded Configuration File" | awk -F=\> '{print $2}')
PHPINI=$(echo $PHPINI;) 
EXTDIR=$(/usr/local/php/bin/php -i | grep extension_dir | awk -F=\> '{print $2}' | head -n1)
EXTDIR=$(echo $EXTDIR;)
if [ -f "$EXTDIR/mongo.so" ]; then
sed -i '/\[mongo\]/d' $PHPINI
sed -i '/extension=mongo.so/d' $PHPINI
echo "[mongo]" >> $PHPINI
echo "extension=mongo.so" >> $PHPINI
fi
