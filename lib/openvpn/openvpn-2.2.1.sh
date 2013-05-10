#!/bin/bash

SRC_URI="http://lnmpp.googlecode.com/files/openvpn-2.2.1.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="openvpn"
V="2.2.1"

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
tar xf $PKG_NAME
echo "config $N-$V$R..."
cd $N-$V$R
echo "make $N-$V$R..."
./configure
make && make install
cd easy-rsa/2.0
sed -i 's/OpenVPN-TEST/ops@shopex.cn/g' vars
sed -i 's/me@myhost.mydomain/ops@shopex.cn/g' vars
. vars
sh clean-all
sh build-ca
sh build-key-server server
sh build-dh
/usr/local/sbin/openvpn --genkey --secret ta.key
mkdir -pv /etc/openvpn
for item in ca.crt server.crt server.key  dh1024.pem; do cp -v keys/$item /etc/openvpn; done
cp ta.key /etc/openvpn/
cd ..
cd ..

cat  >/etc/openvpn/server.conf<<'EOF'
port 1194
proto tcp
dev tun
ca /etc/openvpn/ca.crt
cert /etc/openvpn/server.crt
key /etc/openvpn/server.key
dh /etc/openvpn/dh1024.pem
server 10.99.0.0 255.255.255.0
ifconfig-pool-persist ipp.txt
push "route 10.99.0.0 255.255.255.0"
ping-timer-rem
group nobody
daemon
keepalive 10 120
max-clients 100
user nobody
group nobody
persist-key
persist-tun
status openvpn-status.log
log /var/log/openvpn.log
log-append /var/log/openvpn.log
verb 4
mute 20
EOF

#/sbin/iptables -A POSTROUTING -s 10.99.0.0/255.255.255.0 -j SNAT --to-source  192.1680.1 

echo "all done"

#usage:

