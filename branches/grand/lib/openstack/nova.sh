#!/bin/sh

# This should get most (if not all of the dependencies for openstack on CentOS 5.5 installed for you
# Based on http://wiki.openstack.org/NovaInstall/CentOSNotes

# Define some constants
BASE=$( pwd )
BUILDDIR="nova-build"
RPMHOST="UPDATE THIS"
NOVACONF="nova.conf"

# Add the euca2ools repo
cat >/etc/yum.repos.d/euca2ools.repo << EUCA_REPO_CONF_EOF
[eucalyptus]
name=euca2ools
baseurl=http://www.eucalyptussoftware.com/downloads/repo/euca2ools/1.3.1/yum/centos/
enabled=1
gpgcheck=0

EUCA_REPO_CONF_EOF

# Add the epel repo
rpm -Uvh 'http://download.fedora.redhat.com/pub/epel/5/x86_64/epel-release-5-4.noarch.rpm'

# Install the necessary packages
yum -y install dnsmasq vblade kpartx kvm gawk iptables ebtables bzr screen euca2ools curl rabbitmq-server gcc gcc-c++ autoconf automake swig openldap openldap-servers python26 python26-devel python26-distribute git openssl-devel python26-tools mysql-server qemu kmod-kvm libxml2.x86_64 libxslt libxslt-devel mysql-devel libvirt vconfig lzop xz xen-devel sudo

# Create directories to build software that needs to be compile from source
mkdir -p $BUILDDIR && cd $BUILDDIR

# Build and install the AoE tools
wget -c http://sourceforge.net/projects/aoetools/files/aoetools/32/aoetools-32.tar.gz/download
tar -zxvf aoetools-32.tar.gz
cd aoetools-32
make
make install
cd $BASE

cat > /etc/udev/rules.d/60-aoe.rules << AOE_RULES_EOF
SUBSYSTEM=="aoe", KERNEL=="discover",    NAME="etherd/%k", GROUP="disk", MODE="0220"
SUBSYSTEM=="aoe", KERNEL=="err",    NAME="etherd/%k", GROUP="disk", MODE="0440"
SUBSYSTEM=="aoe", KERNEL=="interfaces",    NAME="etherd/%k", GROUP="disk", MODE="0220"
SUBSYSTEM=="aoe", KERNEL=="revalidate",    NAME="etherd/%k", GROUP="disk", MODE="0220"
# aoe block devices
KERNEL=="etherd*",       NAME="%k", GROUP="disk"
AOE_RULES_EOF

# Make sure the correct kernel modules are installed
modprobe aoe
modprobe kvm
modprobe nbd

# The qemu-img that comes with centos doesn't support the argument format openstack uses, so we have to replace it with a wrapper
mv -iv /usr/bin/qemu-img /usr/bin/qemu-img.bin
cat > /usr/bin/qemu-img <<EOF
#!/bin/sh

ARGS="\$*"

CHANGED_ARGS=\$(echo \$* | sed "s/-o cluster_size=2M,backing_file=/-b /g")

/usr/bin/qemu-img.bin  \$CHANGED_ARGS
EOF

chmod +x /usr/bin/qemu-img

# Install the necessary python modules
easy_install-2.6 twisted sqlalchemy mox greenlet carrot python-daemon eventlet tornado IPy routes lxml MySQL-python sphinx webob netaddr paste pastedeploy glance Cheetah
easy_install-2.6 python-daemon==1.5.5
easy_install-2.6 lockfile==0.8
easy_install-2.6 boto==1.9b
easy_install-2.6 python-gflags==1.4
easy_install-2.6 sqlalchemy-migrate==0.6

# Build and install the libxml2 2.7.3 for python 2.6 (the one that comes with RHEL/CentOS 5 is compiled for Python 2.4)
cd $BUILDDIR
wget -c "ftp://xmlsoft.org/libxml2/libxml2-2.7.3.tar.gz"
tar -zxvf libxml2-2.7.3.tar.gz
cd libxml2-2.7.3
./configure --with-python=/usr/bin/python26 --prefix=/usr
make all
make install
cd python
python2.6 setup.py install

cd $BASE

# Make a small change to the opensslconf header so that M2Crypto installs properly
sed -i  's_opensslconf-\(.*\)_/usr/include/openssl/opensslconf-\1_'  /usr/include/openssl/opensslconf.h 
easy_install-2.6 M2Crypto

# We have to build corutils so we can get the 'truncate' binary.  It is not included with the coreutils that comes with RHEL/CentOS 5
cd $BUILDDIR
wget http://ftp.gnu.org/gnu/coreutils/coreutils-8.9.tar.gz
tar -zxvf coreutils-8.9.tar.gz
cd coreutils-8.9
./configure
make
cp src/truncate /usr/bin/

cd $BASE

# We want to remove the libvirt that yum installed, as it is too old.  We'll add newer ones below
yum -y remove libvirt

# You will likely need to update the location of these RPMs
rpm -Uvh http://${RPMHOST}/libvirt/libvirt-0.8.7-2.x86_64.rpm http://{$RPMHOST}/libvirt/libvirt-client-0.8.7-2.x86_64.rpm http://${RPMHOST}/libvirt/libvirt-devel-0.8.7-2.x86_64.rpm http://${RPMHOST}/libvirt/libvirt-python26-0.8.7-2.x86_64.rpm

# Make sure it's started
/etc/init.d/libvirtd start

# Create the necessary directories for nova
mkdir -p /etc/nova /var/log/nova /var/lib/nova/CA

# Download, extract, and install nova
cd $BUILDDIR && wget http://openstack.org/projects/compute/latest-release/ -O nova.tar.gz
NOVADIR=$( tar -zxvf nova.tar.gz | awk -F\/ '{ print $1 }' | head -1 )
cd $NOVADIR && python2.6 setup.py install

# Copy the configuration files and CA templates into place
cp etc/nova-api.conf /etc/nova
rsync -av CA/ /var/lib/nova/CA/

# You'll want to change this to be the location of your nova.conf (check the variables at the top of this script), or comment it out and add /etc/nova/nova.conf manually
wget http://${RPMHOST}/${NOVACONF} -O /etc/nova/nova.conf

cd $BASE

# In our environment we use eth1 as our bridge device, so we need to make sure it comes up configured correctly.  You may need to edit this or take it out entirely
NETWORK_LOCATION="/etc/sysconfig/network-scripts"
NETWORK_DEVICES="eth1"
for i in $NETWORK_DEVICES; do
  mv $NETWORK_LOCATION/ifcfg-${i} $NETWORK_LOCATION/ifcfg-${i}.bak
  cat > $NETWORK_LOCATION/ifcfg-${i} << __EOF_
DEVICE=eth1
ONBOOT=yes
__EOF_
ifup ${i}
done
# Make sure libvirtd starts automatically at boot
chkconfig --add libvirtd