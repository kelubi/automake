#!/bin/bash
#
DESCRIPTION="php running in fast cgi mode"
HOMEPAGE="http://php.net/"
SRC_URI="http://lnmpp.googlecode.com/files/php-5.2.13.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="php"
V="5.2.13"

if [ ! -d /opt/install ]; then
    mkdir -pv /opt/install
fi

ln -sv /usr/lib64/libjpeg.so /usr/lib
ln -sv /usr/lib64/libpng.so /usr/lib

echo "go to working dir"
cd /opt/install

if [ -s $PKG_NAME ]; then
  echo "$PKG_NAME [found]"
else
  echo "Error: $PKG_NAME not found!!!download now......"
  wget $SRC_URI
  wget http://lnmpp.googlecode.com/files/php-5.2.13-fpm-0.5.13.diff.gz
fi

echo "init $N-$V$R build script..."
#add web server running user
id www > /dev/null 2>&1
if [ $? -ne 0 ]; then
    useradd -s /sbin/nologin -M  www
fi
#unpard file from $XGPATH_SOURCE to current directory.
if [ -d "/opt/install/$N-$V$R" ]; then
    rm -rf "/opt/install/$N-$V$R"
fi
echo "Unpacking to `pwd`"
tar xf $PKG_NAME
if [ $? -ne 0 ]; then
    echo "$PKG_NAME upack error ABORT"
    exit
fi
echo "config $N-$V$R..."
#fist, cd build directory
gzip -cd php-5.2.13-fpm-0.5.13.diff.gz | patch -d $N-$V$R -p1
cd $N-$V$R
#second, add package specified config params to XGB_CONFIG
XGB_CONFIG+=" --prefix=/usr/local/php \
--with-config-file-path=/usr/local/php/etc \
--with-mysql=/usr/local/mysql \
--with-mysqli=/usr/local/mysql/bin/mysql_config \
--with-iconv-dir \
--with-freetype-dir \
--with-jpeg-dir \
--with-png-dir \
--with-zlib \
--with-libxml-dir=/usr --enable-xml --disable-rpath \
--enable-discard-path \
--enable-magic-quotes \
--enable-safe-mode \
--enable-bcmath \
--enable-shmop \
--enable-sysvsem \
--enable-inline-optimization \
--with-curl \
--with-curlwrappers \
--enable-mbregex \
--enable-fastcgi \
--enable-fpm \
--enable-force-cgi-redirect \
--enable-mbstring \
--with-mcrypt \
--enable-ftp \
--with-gd \
--enable-gd-native-ttf \
--with-openssl \
--with-mhash \
--enable-pcntl \
--enable-sockets \
--with-xmlrpc \
--enable-zip \
--enable-soap \
--without-pear \
--with-gettext \
--with-mime-magic  "
        
#Third, call configure with $XGB_CONFIG
./configure $XGB_CONFIG
echo "make $N-$V$R..."
CPU_NUM=$(cat /proc/cpuinfo | grep processor | wc -l)
if [ $CPU_NUM -gt 1 ];then
    make -j$CPU_NUM  ZEND_EXTRA_LIBS='-liconv'
else
   make ZEND_EXTRA_LIBS='-liconv'
fi

echo "checking $N-$V$R.."
echo "install to $XGPATH_DEST..."    
#install everything to $XGPATH_DEST
make  install

cp php.ini-dist /usr/local/php/etc/php.ini
echo "running after package installed..."
#adjust php.ini
sed -i 's#extension_dir = "./"#extension_dir = "/usr/local/php/lib/php/extensions/no-debug-non-zts-20060613/"#'  /usr/local/php/etc/php.ini
sed -i 's#output_buffering = Off#output_buffering = On#' /usr/local/php/etc/php.ini
sed -i 's/post_max_size = 8M/post_max_size = 64M/g' /usr/local/php/etc/php.ini
sed -i 's/upload_max_filesize = 2M/upload_max_filesize = 64M/g' /usr/local/php/etc/php.ini
sed -i 's/;date.timezone =/date.timezone = PRC/g' /usr/local/php/etc/php.ini
sed -i 's/; cgi.fix_pathinfo=0/cgi.fix_pathinfo=1/g' /usr/local/php/etc/php.ini
sed -i 's/max_execution_time = 30/max_execution_time = 300/g' /usr/local/php/etc/php.ini
#adjust php-fpm
sed -i 's,<!--.*<value name=\"user\">nobody</value>.*-->,<value name=\"user\">www</value>,g'  /usr/local/php/etc/php-fpm.conf
sed -i 's,<!--.*<value name=\"group\">nobody</value>.*-->,<value name=\"group">www</value>,g' /usr/local/php/etc/php-fpm.conf
#sed -i 's,<value name=\"listen_address\">127.0.0.1:9000</value>,<value name=\"listen_address\">/tmp/php_fcgi.sock</value>,g' /usr/local/php/etc/php-fpm.conf
sed -i 's,<value name=\"max_children\">5</value>,<value name=\"max_children\">128</value>,g' /usr/local/php/etc/php-fpm.conf
#self start 
install -v -m755 /usr/local/php/sbin/php-fpm /etc/init.d/php-fpm    
echo '# Comments to support chkconfig on RedHat Linux' >> /etc/init.d/php-fpm 
echo '# chkconfig: 2345 65 37' >> /etc/init.d/php-fpm 
echo '# description: A php fast cgi interface' >> /etc/init.d/php-fpm      
chkconfig --add php-fpm
service php-fpm start
if [  ! -d  /data/httpd ]; then
    mkdir -pv /data/httpd
fi
echo "<?php phpinfo();" > /data/httpd/info.php


