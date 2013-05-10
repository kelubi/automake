#!/bin/bash
#
# Xiange Linux build scripts

# Short one-line description of this package.
DESCRIPTION="MySQL server  suitable from shopex ecos"

# Homepage, not used by Portage directly but handy for developer reference
HOMEPAGE="http://mysql.com/"

# Point to any required sources; these will be automatically downloaded by
# gpkg. 
# $N = package name, such as autoconf, x-org
# $V = package version, such as 2.6.10

#SRC_URI="http://foo.bar.com/$N-$V.tar.bz2"
SRC_URI="http://mirrors.dev.shopex.cn/lnmpp/sources/mysql-5.1.48.tar.gz"


# Binary package URI.
BIN_URI=""


# Runtime Depend
RDEPEND=""

# Build time depend
DEPEND="${RDEPEND}"



#init 
xgb_init()
{
    echo "init $N-$V$R build script..."
    #add  server running user
    id mysql > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        useradd -s /sbin/nologin -M  mysql
    fi
}

#unpack
xgb_unpack()
{
    #unpard file from $XGPATH_SOURCE to current directory.
    echo "Unpacking to `pwd`"
    tar xf $XGPATH_SOURCE/`basename $SRC_URI`
}

#config
xgb_config()
{
    echo "config $N-$V$R..."
    #fist, cd build directory
    cd $N-$V$R
    
    #second, add package specified config params to XGB_CONFIG
    XGB_CONFIG+=" --prefix=/usr/local/mysql \
    --with-extra-charsets=all  \
    --enable-thread-safe-client \
    --enable-assembler \
    --with-charset=utf8 \
    --enable-thread-safe-client \
    --with-readline  \
    --with-embedded-server \
    --enable-local-infile \
    --without-isam \
    --with-partition    \
    --with-plugins=csv,innobase,innodb_plugin,myisam,heap
    "
    
    #Third, call configure with $XGB_CONFIG
    ./configure $XGB_CONFIG
}

#build
xgb_build()
{
    echo "make $N-$V$R..."
    make 
}

#check
xgb_check()
{
    echo "checking $N-$V$R.."
    #make check
}

#install
xgb_install()
{
    echo "install to $XGPATH_DEST..."
    
    make  DESTDIR=$XGPATH_DEST install
    mv $XGPATH_DEST/usr/local/mysql/{mysql-test,sql-bench} $XGPATH_DEST/usr/local/mysql/share/mysql/
    mkdir -pv $XGPATH_DEST/usr/local/mysql/lib
    cd $XGPATH_DEST/usr/local/mysql/lib
    ln -v -sf mysql/libmysqlclient{,_r}.so* .
    cd -
    mkdir -pv $XGPATH_DEST/etc/init.d
    install -v -m644 $XGPATH_DEST/usr/local/mysql/share/mysql/my-medium.cnf $XGPATH_DEST/etc/my.cnf
    sed -i 's/skip-locking/skip-external-locking/g' $XGPATH_DEST/etc/my.cnf
    #    
    install -v -m777 $XGPATH_DEST/usr/local/mysql/share/mysql/mysql.server $XGPATH_DEST/etc/init.d/mysqld
    sed -i s,^basedir=$,basedir=/usr/local/mysql,g $XGPATH_DEST/etc/init.d/mysqld
    sed -i s,^datadir=$,datadir=/data/mysql,g $XGPATH_DEST/etc/init.d/mysqld
    #
    ln -sv /usr/local/mysql/bin/mysqlcheck $XGPATH_DEST/usr/local/mysql/bin/mysqlanalyze &&
    ln -sv /usr/local/mysql/bin/mysqlcheck $XGPATH_DEST/usr/local/mysql/bin/mysqlrepair &&
    ln -sv /usr/local/mysql/bin/mysqlcheck $XGPATH_DEST/usr/local/mysql/bin/mysqloptimize
    #
    mkdir -pv $XGPATH_DEST/usr/bin
    ln -sv /usr/local/mysql/bin/mysql $XGPATH_DEST/usr/bin/mysql
    ln -sv /usr/local/mysql/bin/mysqladmin $XGPATH_DEST/usr/bin/mysqladmin
    #
    mkdir -pv $XGPATH_DEST/var/run/mysql
    mkdir -pv $XGPATH_DEST/var/log/mysql
    install -v -m755 -o mysql -g mysql -d $XGPATH_DEST/var/run/mysql &&
    install -v -m750 -o mysql -g mysql -d $XGPATH_DEST/var/log/mysql &&
    touch $XGPATH_DEST/var/log/mysql/mysql.{log,err} &&
    chown mysql:mysql $XGPATH_DEST/var/log/mysql/mysql* &&
    chmod 0660 $XGPATH_DEST/var/log/mysql/mysql*
}

#post install
xgb_postinst()
{
    echo "running after package installed..."
    #
    ln -s /usr/local/mysql/lib/mysql /usr/lib/mysql
    ln -s /usr/local/mysql/include/mysql /usr/include/mysql
    echo "/usr/local/mysql/lib/mysql" >> /etc/ld.so.conf
    echo "/usr/local/lib" >>/etc/ld.so.conf
    ldconfig
    ldconfig
    if [ -d /data/mysql ]; then
        rm -rf /data/mysql
    fi
    mkdir -pv /data/mysql
    /usr/local/mysql/bin/mysql_install_db --user=mysql --datadir=/data/mysql
    chgrp -v mysql /data/mysql{,/test,/mysql}
    killall mysqld && sleep 3
    /usr/local/mysql/bin/mysqld_safe --user=mysql  --datadir=/data/mysql 2>&1 >/dev/null  &
    sleep 3
    MYSQLD_PASSWORD=$(</dev/urandom tr -dc A-Za-z0-9 | head -c8)     
    /usr/local/mysql/bin/mysqladmin -u root  password $MYSQLD_PASSWORD
    err_check "install  $N-$V$R fail!"
    echo "mysql:root:"$MYSQLD_PASSWORD >> $XGPATH/password.txt
    /usr/local/mysql/bin/mysql --user=root --password=$MYSQLD_PASSWORD  mysql < /usr/local/mysql/share/mysql/fill_help_tables.sql
    echo "use mysql;delete  from user where password=''" | /usr/local/mysql/bin/mysql -uroot -p$MYSQLD_PASSWORD
    chkconfig mysqld --level 3 on        
}

#pre remove
xgb_prerm()
{
    echo "running before package delete..."
}

#post remove
xgb_postrm()
{
    echo "running after package delete..."
}
