#!/bin/bash
#
# Homepage, not used by Portage directly but handy for developer reference

# Point to any required sources; these will be automatically downloaded by
# gpkg. 
# $N = package name, such as autoconf, x-org
# $V = package version, such as Python-2.7.3

SRC_URI="http://www.python.org/ftp/python/2.7.5/Python-2.7.5.tar.xz"
PKG_NAME=`basename $SRC_URI`
N="Python"
V="2.7.5"

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
echo "init $N-$V build script..."
#unpack
#unpard file from $XGPATH_SOURCE to current directory.
echo "Unpacking to `pwd`"
tar xvf $PKG_NAME
cd $N-$V

./configure --prefix=/usr/local/python2.7
echo "make $N-$V..."
make
echo "installing $N-$V..."
make  install      

mv -f /usr/bin/python  /usr/bin/python.bak
ln  -sv /usr/local/python2.7/bin/python /usr/bin/python

echo "python version:"
python -V 
#do some fix operation
sed -i "s,\#\!/usr/bin/python,\#\!/usr/bin/python2.4,g"  $(which yum)
#install pip
curl http://peak.telecommunity.com/dist/ez_setup.py | python
curl  https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python 