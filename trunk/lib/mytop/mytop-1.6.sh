#!/bin/bash
#

DESCRIPTION="mytop is a console-based (non-gui) tool for monitoring the threads and overall performance of a MySQL 3.22.x, 3.23.x, and 4.x server"
HOMEPAGE="http://jeremy.zawodny.com/mysql/mytop/"
SRC_URI="http://jeremy.zawodny.com/mysql/mytop/mytop-1.6.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="mytop"
V="1.6"

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

#prepare 
wget http://search.cpan.org/CPAN/authors/id/S/ST/STSI/TermReadKey-2.30.02.tar.gz
tar xf TermReadKey-2.30.02.tar.gz 
cd TermReadKey-2.30.02
perl Makefile.PL 
make
make install
perl -MCPAN -e 'install DBI'
perl -MCPAN -e 'install DBD::mysql'
#

#init 
echo "init $N-$V$R build script..."
#unpack
#unpard file from $XGPATH_SOURCE to current directory.
echo "Unpacking to `pwd`"
tar xvf $PKG_NAME

echo "config $N-$V$R..."
cd $N-$V$R
perl Makefile.PL 
make
make install

echo "all done"

#usage
#mytop -h127.0.0.1 -uroot -pxxxxxx