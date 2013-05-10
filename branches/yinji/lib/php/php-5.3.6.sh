#!/bin/bash
#
DESCRIPTION="php running in fast cgi mode"
HOMEPAGE="http://php.net/"
SRC_URI="http://lnmpp.googlecode.com/files/php-5.3.6.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="php"
V="5.3.6"

if [ ! -d /opt/install ]; then
    mkdir -pv /opt/install
fi
echo "go to working dir"
cd /opt/install

if [ -s $PKG_NAME ]; then
  echo "$PKG_NAME [found]"
else
  echo "Error: $PKG_NAME not found!!!download now......"
  wget $SRC_URI
fi

echo "init $N-$V$R build script..."
#add web server running user
id www > /dev/null 2>&1
if [ $? -ne 0 ]; then
    useradd -s /sbin/nologin -M  www
fi
#unpard file from $XGPATH_SOURCE to current directory.
echo "Unpacking to `pwd`"
tar xf $PKG_NAME
if [ $? -ne 0 ]; then
    echo "$PKG_NAME upack error ABORT"
    exit
fi
echo "config $N-$V$R..."
cd $N-$V$R
#second, add package specified config params to XGB_CONFIG
XGB_CONFIG="--prefix=/usr/local/php \
--with-config-file-path=/usr/local/php/etc \
--with-mysql=/usr/local/mysql \
--with-mysqli=/usr/local/mysql/bin/mysql_config \
--with-iconv-dir \
--with-freetype-dir \
--with-jpeg-dir \
--with-png-dir \
--with-zlib \
--with-libxml-dir=/usr \
--enable-xml \
--disable-rpath \
--enable-magic-quotes \
--enable-safe-mode \
--enable-bcmath \
--enable-shmop \
--enable-sysvsem \
--enable-inline-optimization \
--with-curl \
--with-curlwrappers \
--enable-mbregex \
--enable-fpm \
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
--with-gettext  \
--with-pdo \
--with-pdo-mysql=/usr/local/mysql
"
        
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


echo "running after package installed..."
if [ ! -d /var/log/php ];then
    install -v -m755 -o www -g www -d /var/log/php 
fi
cp php.ini-production /usr/local/php/etc/php.ini
#adjust php.ini
sed -i 's#;extension_dir = "./"#extension_dir = "/usr/local/php/lib/php/extensions/no-debug-non-zts-20090626/"#'  /usr/local/php/etc/php.ini
sed -i 's#output_buffering = Off#output_buffering = On#' /usr/local/php/etc/php.ini
sed -i 's/post_max_size = 8M/post_max_size = 64M/g' /usr/local/php/etc/php.ini
sed -i 's/upload_max_filesize = 2M/upload_max_filesize = 64M/g' /usr/local/php/etc/php.ini
sed -i 's/;date.timezone =/date.timezone = PRC/g' /usr/local/php/etc/php.ini
sed -i '/cgi.fix_pathinfo=0/s/^;//g' /usr/local/php/etc/php.ini
sed -i 's/max_execution_time = 30/max_execution_time = 300/g' /usr/local/php/etc/php.ini
#adjust php-fpm
cp /usr/local/php/etc/php-fpm.conf.default /usr/local/php/etc/php-fpm.conf
sed -i 's,user = nobody,user=www,g'   /usr/local/php/etc/php-fpm.conf
sed -i 's,group = nobody,group=www,g'   /usr/local/php/etc/php-fpm.conf
sed -i 's,;pm.min_spare_servers = 5,pm.min_spare_servers = 5,g'   /usr/local/php/etc/php-fpm.conf
sed -i 's,;pm.max_spare_servers = 35,pm.max_spare_servers = 35,g'   /usr/local/php/etc/php-fpm.conf
sed -i 's,;pm.start_servers = 20,pm.start_servers = 20,g'   /usr/local/php/etc/php-fpm.conf
sed -i 's,;pid = run/php-fpm.pid,pid = run/php-fpm.pid,g'   /usr/local/php/etc/php-fpm.conf
sed -i 's,;error_log = log/php-fpm.log,error_log = /var/log/php/php-fpm.log,g'   /usr/local/php/etc/php-fpm.conf
sed -i 's,;slowlog = log/$pool.log.slow,slowlog = /var/log/php/\$pool.log.slow,g'   /usr/local/php/etc/php-fpm.conf
#self start 
install -v -m755 sapi/fpm/init.d.php-fpm  /etc/init.d/php-fpm       
/sbin/chkconfig --add php-fpm 
/sbin/chkconfig php-fpm --level 3 on
/sbin/service php-fpm start
echo "<?php phpinfo();" > /data/httpd/info.php


