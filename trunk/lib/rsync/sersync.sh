#!/bin/bash
#
DESCRIPTION="Perl Compatible Regular Expressions"
SRC_URI32="http://lnmpp.googlecode.com/files/sersync2.5_32bit_binary_stable_final.tar.gz"
SRC_URI64="http://lnmpp.googlecode.com/files/sersync2.5_64bit_binary_stable_final.tar.gz"
PKG_NAME32=`basename ${SRC_URI32}`
PKG_NAME64=`basename ${SRC_URI64}`
N="serync"
V1="32"
V2="64"
WEIS=`uname -a | awk '{print $12}'`
CHECKRS=`rpm -qa | grep rsync`

if [ -n $CHECKRS ];then
   echo "rsync package is exists"
  else
   yum install rsync
fi

if [ ! -d /opt/install ]; then
    mkdir -pv /opt/install
fi
echo "go to working dir"
cd /opt/install

if [ -s $PKG_NAME ]; then
  echo "$PKG_NAME [found]"
  else
  echo "Error: $PKG_NAME not found!!!download now......"
fi
if [ $WEIS == "i686" ];then
   wget -c ${SRC_URI32}
  elif [ $WEIS == "x86_64" ];then
   wget -c ${SRC_URI64}
fi

tar -zxvf sersync2.5_*.tar.gz
mv GNU-Linux-x86 /usr/local/$N
cd /usr/local/$N
/usr/local/$N/sersync2 -d

echo "sersync已经安装完成。请修改需要被监控同步的目录."