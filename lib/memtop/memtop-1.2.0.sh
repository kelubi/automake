#!/bin/bash
#
# Homepage, not used by Portage directly but handy for developer reference

# Point to any required sources; these will be automatically downloaded by
# gpkg. 
# $N = package name, such as autoconf, x-org
# $V = package version, such as Python-2.7.3

SRC_URI="http://memtop.googlecode.com/files/memtop-1.0.2.py"
PKG_NAME=`basename $SRC_URI`
N="memtop"
V="1.0.2"

if [ ! -d /opt/install ]; then
    mkdir -pv /opt/install
fi
echo "go to working dir"
cd /opt/install

#Python version Verification 
echo `python -V 2>&1` | awk '{print $2}' > install_tmp
echo "2.7.0" >> install_tmp

T=`cat install_tmp |sort -nr  |head -n 1`
if [ "$T" == "2.7.0" ];then 
  curl http://lnmpp.googlecode.com/svn/trunk/lib/python/python-2.7.3.sh | sh 
fi

if [ -s $PKG_NAME ]; then
  echo "$PKG_NAME [found]"
  else
  echo "Error: $PKG_NAME not found!!!download now......"
  wget -c $SRC_URI
fi

cp memtop-1.0.2.py /usr/local/bin/memtop
chmod u+x /usr/local/bin/memtop

echo "memtop 1.0.2 install ok!!"
echo "Command:"
echo "        memtop"