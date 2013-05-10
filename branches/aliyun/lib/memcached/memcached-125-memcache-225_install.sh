#!/bin/bash 
# memcache memcache-2.2.5.tgz
# memcached memcached-1.2.5.tar.gz

#install memcached 
PREFIX="/usr/local/memcached"
PHPCONFIG="/usr/local/php/bin/php-config"
PHPIZE="/usr/local/php/bin/phpize"
PHPINI="/usr/local/php/etc/php.ini"
START="/usr/local/memcached/bin/memcached -d -p 11211 -u www -P /var/run/memcached/memcached.pid"
#IP=`ifconfig eth0 |awk '/inet addr/ {print $2}' |cut -d: -f2`
EXTENION="extension = memcache.so"
#APPCONFIG="/data/httpd/example.com/config/config.php"

SRC_URI_memcached="http://lnmpp.googlecode.com/files/memcached-1.2.5.tar.gz"
SRC_URI_memcache="http://lnmpp.googlecode.com/files/memcache-2.2.5.tgz"
memcached_name=`basename ${SRC_URI_memcached}`
memcache_name=`basename ${SRC_URI_memcache}`

if [ ! -d /opt/install ]; then
    mkdir -pv /opt/install
fi
echo "go to working dir"
cd /opt/install

if [ -s $memcached_name ]; then
  echo "$memcached_name [found]"
  else
  echo "Error: $memcached_name not found!!!download now......"
  wget -c ${SRC_URI_memcached}
fi

if [ -s $memcache_name ]; then
  echo "$memcache_name [found]"
  else
  echo "Error: $memcache_name not found!!!download now......"
  wget -c ${SRC_URI_memcache}
fi


tar zxf $memcached_name && cd memcached-1.2.5
./configure --prefix="$PREFIX" --with-php-config="PHPCONFIG" && make && make install
if [ $? -eq 0 ];then 
   echo "$memcached_name is installed !"
else 
   echo "$memcached_name is not installed well,now exit"
   exit 1
fi

#install memcache 
cd /opt/install
tar zxf $memcache_name && cd memcache-2.2.5
$PHPIZE && sleep 1
./configure --enable-memcache="$PREFIX/bin/memcached" --with-php-config="$PHPCONFIG" && make && make install
if [ $? -eq 0 ];then 
   echo "$memcache_name is installed !"
else 
   echo "$memcache_name is not installed well,now exit"
   exit 2
fi

#start memcached
$START
if [ $? -eq 0 ];then
   echo "memcached is started !"
else
   echo "memcached is not startetd,now exit"
   exit 3
fi
echo -e "$START" >> /etc/rc.local

#config php.ini
echo -e "$EXTENION" >> $PHPINI
/etc/init.d/php-fpm restart

echo "php-memcache is done ,please test the web if OK!!!!"


