#!/bin/bash
#
# Xiange Linux build scripts

# Short one-line description of this package.
DESCRIPTION=" snmp agent"

# Homepage, not used by Portage directly but handy for developer reference
HOMEPAGE="http://ops.dev.shopex.cn/"

# Point to any required sources; these will be automatically downloaded by
# gpkg. 
# $N = package name, such as autoconf, x-org
# $V = package version, such as 2.6.10

#SRC_URI="http://foo.bar.com/$N-$V.tar.bz2"
SRC_URI=""


# Binary package URI.
BIN_URI=""


# Runtime Depend
RDEPEND=""

# Build time depend
DEPEND="${RDEPEND}"


echo "install to $XGPATH_DEST..."
#install everything to $XGPATH_DEST
yum -y remove net-snmp  net-snmp-utils
yum -y install net-snmp  net-snmp-utils
SNMP_PASSWORD=$(</dev/urandom tr -dc A-Za-z0-9 | head -c8)
cat >/etc/snmp/snmpd.conf << EOF
com2sec notConfigUser default $SNMP_PASSWORD 
group notConfigGroup v1 notConfigUser
group notConfigGroup v2c notConfigUser 
view systemview included .1.3.6.1.2.1.1
view systemview included .1.3.6.1.2.1.25.1.1 
access notConfigGroup "" any noauth exact all none none
view all included .1 80
view mib2 included .iso.org.dod.internet.mgmt.mib-2 fc
view all included .1
EOF

sed -i /snmp:default:/d /opt/install/password.txt
echo "snmp:default:"$SNMP_PASSWORD >> /opt/install/password.txt

/sbin/chkconfig --add snmpd 
/sbin/chkconfig snmpd --level 3 on
/sbin/service snmpd start    
snmpwalk -c $SNMP_PASSWORD -v 1 -m ALL localhost

echo "all done"