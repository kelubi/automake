#!/bin/bash
#
DESCRIPTION="will create a Slackware, RPM or Debian compatible package and install"
HOMEPAGE="http://asic-linux.com.mx/~izto/checkinstall/index.php"
SRC_URI="http://lnmpp.googlecode.com/files/checkinstall-1.6.2.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="checkinstall"
V="1.6.2"

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
echo "Unpacking to `pwd`"
tar xf $PKG_NAME
echo "config $N-$V$R..."
cd $N-$V$R
echo "make $N-$V$R..."
./configure --prefix=/usr
make
make install
[ -d /usr/local/lib64 ] && ln -sv /usr/local/lib/installwatch.so /usr/local/lib64/installwatch.so

cat >/usr/local/lib/checkinstall/checkinstallrc <<'EOF'
DEBUG=0
INSTALLWATCH_PREFIX="/usr/local"
INSTALLWATCH=${INSTALLWATCH_PREFIX}/bin/installwatch
MAKEPKG=/sbin/makepkg
MAKEPKG_FLAGS="-l y -c n"
SHOW_MAKEPKG=0
BASE_TMP_DIR=/var/tmp   ##  Don't set this to /tmp or / !! 
DOC_DIR=""
ARCHITECTURE=""
INSTYPE="R"
PAK_DIR=""
RPM_FLAGS=" --force --nodeps --replacepkgs "
DPKG_FLAGS=""
SHOW_INSTALL=1
SHOW_SLACK_INSTALL=0
DEL_DOCPAK=1
DEL_SPEC=0
DEL_DESC=1
STRIP_ELF=1
STRIP_SO_ELF=1
ADD_SO=0
COMPRESS_MAN=1
CKUMASK=0022
BACKUP=1 
AUTODOINST=1
TRANSLATE=1            
RESET_UIDS=0               
NEW_SLACK=1
EXCLUDE=""
ACCEPT_DEFAULT=0
RPM_IU=U
CK_INSPECT=1 
REVIEW_SPEC=1      
REVIEW_CONTROL=0      
INSTALL=0
EOF

echo "all done"

#usage:
#checkinstall -R --fstrans=no --inspect --review-spec --review-control
#checkinstall -R -y -d2 --pkgrelease=shopex --pkggroup="ShopEx/common"