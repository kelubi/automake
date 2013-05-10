#!/bin/bash
#

# Homepage, not used by Portage directly but handy for developer reference

# Point to any required sources; these will be automatically downloaded by
# gpkg. 
# $N = package name, such as autoconf, x-org
# $V = package version, such as 2.6.10

SRC_URI="http://redis.googlecode.com/files/redis-2.4.7.tar.gz "
PKG_NAME=`basename $SRC_URI`
N="redis"
V="2.4.7"

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

mv redis-2.4.7 /usr/local/redis
cd /usr/local/redis
make
make  install

cat > /usr/local/redis/redis.conf <<'EOF'

daemonize yes 

pidfile /usr/local/redis/var/redis.pid 

port 6379 

timeout 300 

loglevel verbose 

logfile /usr/local/redis/var/redis.log 

databases 16 

#save 900 1 

#save 300 10 

#save 60 10000 

rdbcompression yes 

dbfilename dump.rdb 

dir /usr/local/redis/var 

dbfilename /usr/local/redis/var/dump.rdb

slave-serve-stale-data yes

appendonly yes 

appendfsync everysec 

no-appendfsync-on-rewrite no 

vm-enabled no 

vm-swap-file /tmp/redis.swap 

vm-max-memory 0 

vm-page-size 32 

vm-pages 134217728 

vm-max-threads 4 

hash-max-zipmap-entries 512 

hash-max-zipmap-value 64 

list-max-ziplist-entries 512 

list-max-ziplist-value 64 

set-max-intset-entries 512 

activerehashing yes
EOF

echo "start redis server"
redis-server /usr/local/redis/redis.conf