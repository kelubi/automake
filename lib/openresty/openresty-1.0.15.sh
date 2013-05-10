#!/bin/bash
#

# Homepage, not used by Portage directly but handy for developer reference

# Point to any required sources; these will be automatically downloaded by
# gpkg. 
# $N = package name, such as autoconf, x-org
# $V = package version, such as 1.0.15
echo "redhat please : install readline-devel pcre-devel openssl-devel"

for i in readline-devel pcre-devel openssl-devel
do
  if ! rpm -qa | grep $i ; then 
    yum install readline-devel pcre-devel openssl-devel -y 
    break 
  fi
done 

for i in 3 2 1 
do
sleep 1
echo $i
done 

SRC_URI="http://lnmpp.googlecode.com/files/ngx_openresty-1.0.15.10.tar.gz "
PKG_NAME=`basename $SRC_URI`
N="openresty"
V="1.0.15.10"

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

if /usr/local/openresty ;then 
  mv /usr/local/openresty /usr/local/openresty_bak
fi

mv  ngx_openresty-1.0.15.10 /usr/local/openresty
cd /usr/local/openresty
./configure --with-luajit
make
make  install
