#!/bin/bash
#
# Xiange Linux build scripts

# Short one-line description of this package.
DESCRIPTION="MySQL server  suitable from shopex ecos"

# Homepage, not used by Portage directly but handy for developer reference
HOMEPAGE="http://mysql.com/"

# Point to any required sources; these will be automatically downloaded by
# gpkg. 
# $N = package name, such as autoconf, x-org
# $V = package version, such as 2.6.10

#SRC_URI="http://foo.bar.com/$N-$V.tar.bz2"
#SRC_URI="http://mirrors.dev.shopex.cn/lnmpp/sources/mysql-5.1.48.tar.gz"
SRC_URI="http://lnmpp.googlecode.com/files/mysql-5.5.14.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="mysql"
V="5.5.14"

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
tar xf $PKG_NAME

if [ $? -ne 0 ]; then
    echo "$PKG_NAME upack error ABORT"
    exit
fi


echo "config $N-$V$R..."
#fist, cd build directory
cd $N-$V$R
cmake . -DCMAKE_INSTALL_PREFIX=/usr/local/mysql -DWITH_INNOBASE_STORAGE_ENGINE=1 -DENABLED_LOCAL_INFILE=1 -DEXTRA_CHARSETS=all -DDEFAULT_CHARSET=utf8 -DDEFAULT_COLLATION=utf8_general_ci  -DMYSQL_USER=mysql  -DWITH_DEBUG=0 -DENABLE_DTRACE=0

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
cat >/etc/ld.so.conf.d/"$N-$V".conf<<EOF
/usr/local/mysql/lib
EOF
ldconfig
ldconfig
if [ -d /data/mysql ]; then
    mv -v /data/mysql /data/mysql.bak
fi
mkdir -pv /data/mysql

pushd /usr/local/mysql && sh scripts/mysql_install_db --user=mysql --datadir=/data/mysql && popd
chgrp -v mysql /data/mysql{,/test,/mysql}
killall mysqld && sleep 3
/usr/local/mysql/bin/mysqld_safe --user=mysql  --datadir=/data/mysql 2>&1 >/dev/null  &
netstat -tnlp | grep 3306 > /dev/null
MYSQL_IS_RUN=$?
while [ $MYSQL_IS_RUN -ne 0 ]
do
    echo "wait 3 second……"
    sleep 3
    netstat -tnlp | grep 3306 > /dev/null
    MYSQL_IS_RUN=$?
done
MYSQLD_PASSWORD=$(</dev/urandom tr -dc A-Za-z0-9 | head -c8)     
/usr/local/mysql/bin/mysqladmin -u root  password $MYSQLD_PASSWORD
sed -i '/mysql:root:/d' /opt/install/password.txt
echo "mysql:root:"$MYSQLD_PASSWORD >> /opt/install/password.txt
echo "use mysql;delete  from user where password=''" | /usr/local/mysql/bin/mysql -uroot -p$MYSQLD_PASSWORD
install -v -m777 /usr/local/mysql/support-files/mysql.server /etc/init.d/mysqld
sed -i s,^basedir=$,basedir=/usr/local/mysql,g /etc/init.d/mysqld
sed -i s,^datadir=$,datadir=/data/mysql,g /etc/init.d/mysqld
/sbin/chkconfig mysqld --level 3 on       
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



