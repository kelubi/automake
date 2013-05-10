#!/bin/bash

DESCRIPTION="MySQL server  suitable from shopex ecos"
HOMEPAGE="http://mysql.com/"
SRC_URI="http://mirrors.dev.shopex.cn/lnmpp/sources/mysql-5.1.48.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="mysql"
V="5.1.48"

if [ ! -d /opt/install ]; then
    mkdir -pv /opt/install
fi
echo "go to working dir"
cd /opt/install

if [ -s $PKG_NAME ]; then
  echo "$PKG_NAME [found]"
  else
  echo "Error: $PKG_NAME not found!!!download now......"
  wget  $SRC_URI
fi

echo "init $N-$V$R build script..."
#add  server running user
id mysql > /dev/null 2>&1
if [ $? -ne 0 ]; then
useradd -s /sbin/nologin -M  mysql
fi

echo "Unpacking to `pwd`"
tar xvf $PKG_NAME

echo "config $N-$V$R..."
#fist, cd build directory
cd $N-$V$R
./configure --prefix=/usr/local/mysql \
--with-server-suffix=" - ShopEX-MySQL" \
--with-mysqld-user=mysql \
--with-plugins=partition,blackhole,csv,heap,innobase,myisam,myisammrg \
--with-charset=utf8 \
--with-collation=utf8_general_ci \
--with-extra-charsets=all \
--with-big-tables \
--with-fast-mutexes \
--with-zlib-dir=bundled \
--enable-assembler \
--enable-profiling \
--enable-local-infile \
--enable-thread-safe-client \
--with-readline \
--with-pthread \
--with-embedded-server \
--with-client-ldflags=-all-static \
--with-mysqld-ldflags=-all-static \
--without-geometry \
--without-debug \
--without-ndb-debug

echo "make $N-$V$R..."
CPU_NUM=$(cat /proc/cpuinfo | grep processor | wc -l)
if [ $CPU_NUM -gt 1 ];then
    make -j$CPU_NUM
else
    make
fi
echo "installing $N-$V$R.."
echo "install to $XGPATH_DEST..."
make  install
#
ln -sv /usr/local/mysql/bin/mysqlcheck /usr/bin
ln -sv /usr/local/mysql/bin/mysqlrepair /usr/bin
ln -sv /usr/local/mysql/bin/mysqloptimize /usr/bin
ln -sv /usr/local/mysql/bin/mysql /usr/bin
ln -sv /usr/local/mysql/bin/mysqladmin /usr/bin
#
mkdir -pv /var/run/mysql
install -v -m755 -o mysql -g mysql -d /var/run/mysql
mkdir -pv /var/log/mysql
install -v -m750 -o mysql -g mysql -d /var/log/mysql 
touch /var/log/mysql/mysql.{log,err} 
chown mysql:mysql  /var/log/mysql/mysql* 
chmod 0660 /var/log/mysql/mysql*
echo "running after package installed..."
echo "/usr/local/mysql/lib/mysql" >> /etc/ld.so.conf
echo "/usr/local/lib" >>/etc/ld.so.conf
ldconfig
ldconfig
if [ -d /data/mysql ]; then
    mv -v /data/mysql /data/mysql.bak
fi
mkdir -pv /data/mysql
/usr/local/mysql/bin/mysql_install_db --user=mysql --datadir=/data/mysql
chgrp -v mysql /data/mysql{,/test,/mysql}
killall mysqld && sleep 3
/usr/local/mysql/bin/mysqld_safe --user=mysql  --datadir=/data/mysql 2>&1 >/dev/null  &
sleep 3
MYSQLD_PASSWORD=$(</dev/urandom tr -dc A-Za-z0-9 | head -c8)     
/usr/local/mysql/bin/mysqladmin -u root  password $MYSQLD_PASSWORD
echo "mysql:root:"$MYSQLD_PASSWORD >> /opt/install/password.txt
echo "use mysql;delete  from user where password=''" | /usr/local/mysql/bin/mysql -uroot -p$MYSQLD_PASSWORD

install -v -m777 /usr/local/mysql/share/mysql/mysql.server /etc/init.d/mysqld
sed -i s,^basedir=$,basedir=/usr/local/mysql,g /etc/init.d/mysqld
sed -i s,^datadir=$,datadir=/data/mysql,g /etc/init.d/mysqld
chkconfig mysqld --level 3 on       
cat >/etc/my.cnf<<'EOF'
[client]
port            = 3306
socket          = /tmp/mysql.sock
[mysqld]
port            = 3306
socket          = /tmp/mysql.sock
skip-external-locking
key_buffer_size = 16M
max_allowed_packet = 1M
table_open_cache = 64
sort_buffer_size = 512K
net_buffer_length = 8K
read_buffer_size = 256K
read_rnd_buffer_size = 512K
myisam_sort_buffer_size = 8M
innodb_buffer_pool_size=512M
innodb_flush_log_at_trx_commit=2
innodb_file_per_table=1
slow_query_log=1
general_log=0
expire-logs-days = 31
log-bin=mysql-bin
binlog_format=mixed
server-id       = 1
[mysqldump]
quick
max_allowed_packet = 16M
[mysql]
no-auto-rehash
[myisamchk]
key_buffer_size = 20M
sort_buffer_size = 20M
read_buffer = 2M
write_buffer = 2M
[mysqlhotcopy]
interactive-timeout
EOF
/sbin/service mysqld restart

echo "all done" 



