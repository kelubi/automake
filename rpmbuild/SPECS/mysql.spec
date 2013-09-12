%define mysql_user                mysql
%define mysql_group             %{mysql_user}
%define mysql_home              /usr/local/mysql
%define mysql_version		5.1.31
%define release			shopex

Name: MySQL
Summary:	MySQL: a very fast and reliable SQL database server
Group:		Applications/Databases
Version:	5.1.31
Release:	%{release}
License:	Copyright 2000-2008 MySQL AB, 2008 Sun Microsystems, Inc.  All rights reserved.  Use is subject to license terms.  Under %{license} license as shown in the Description field.
Source:		http://www.mysql.com/Downloads/MySQL-@MYSQL_BASE_VERSION@/mysql-%{mysql_version}.tar.gz
URL:		http://www.mysql.com/
Packager:	Sun Microsystems, Inc. Product Engineering Team <build@mysql.com>
Vendor:		%{mysql_vendor}
Provides:	msqlormysql MySQL-server mysql
BuildRequires: ncurses-devel
Obsoletes:	mysql


# configuration patch to match all the Fedora paths for logs, pid files
# etc.

%description
	The MySQL software has Dual Licensing, which means you can use the MySQL


%prep
%setup -D -T -a 0 -n mysql-%{mysql_version}

%build
export DESTDIR=%{buildroot}
./configure --prefix=/usr/local/mysql \
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
--with-plugins=max
   
make %{?_smp_mflags} 

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALLDIRS=vendor
find %{buildroot} -type f -empty -exec rm -f {} \;
find %{buildroot} -type f -exec chmod 0644 {} \;
find %{buildroot} -type f -name '*.so' -exec chmod 0755 {} \;
chmod 0755 %{buildroot}%{mysql_home}/bin/*

%clean
rm -rf %{buildroot}

%pre
id mysql > /dev/null 2>&1
if [ $? -ne 0 ]; then
/usr/local/mysql/bin/useradd -c "mysqld service  user" -s /bin/false -r -d %{mysql_home} %{mysql_user} 2>/dev/null || :
fi

%post
#make soft link 
ln -sv /usr/local/mysql/bin/mysqlcheck /usr/bin
ln -sv /usr/local/mysql/bin/mysqlrepair /usr/bin
ln -sv /usr/local/mysql/bin/mysqloptimize /usr/bin
ln -sv /usr/local/mysql/bin/mysql /usr/bin
ln -sv /usr/local/mysql/bin/mysqladmin /usr/bin
#
mkdir -pv /var/run/mysql
install -v -m755 -o mysql -g mysql -d /var/run/mysql
mkdir -pv /var/log/mysql
install -v -m750 -o mysql -g mysql -d /var/log/mysql 
touch /var/log/mysql/mysql.{log,err} 
chown mysql:mysql  /var/log/mysql/mysql* 
chmod 0660 /var/log/mysql/mysql*
echo "/usr/local/mysql/lib/mysql" >> /etc/ld.so.conf
echo "/usr/local/lib" >>/etc/ld.so.conf
ldconfig
if [ -d /data/mysql ]; then
    mv -v /data/mysql /data/mysql.bak
fi
mkdir -pv /data/mysql
/usr/local/mysql/bin/mysql_install_db --user=mysql --datadir=/data/mysql
chgrp -v mysql /data/mysql{,/test,/mysql}
killall mysqld && sleep 3
/usr/local/mysql/bin/mysqld_safe --user=mysql  --datadir=/data/mysql 2>&1 >/dev/null  &
sleep 3
MYSQLD_PASSWORD=$(</dev/urandom tr -dc A-Za-z0-9 | head -c8)     
/usr/local/mysql/bin/mysqladmin -u root  password $MYSQLD_PASSWORD
echo "mysql:root:"$MYSQLD_PASSWORD >> /data/mysql/password.txt
echo "use mysql;delete  from user where password=''" | /usr/local/mysql/bin/mysql -uroot -p$MYSQLD_PASSWORD

install -v -m777 /usr/local/mysql/share/mysql/mysql.server /etc/init.d/mysqld
sed -i s,^basedir=$,basedir=/usr/local/mysql,g /etc/init.d/mysqld
sed -i s,^datadir=$,datadir=/data/mysql,g /etc/init.d/mysqld
/sbin/chkconfig --add mysqld
/sbin/chkconfig mysqld --level 3 on       
cat >/etc/my.cnf<<'EOF'
[client]
port            = 3306
socket          = /tmp/mysql.sock
[mysqld]
port            = 3306
socket          = /tmp/mysql.sock
skip-external-locking
key_buffer_size = 16M
max_allowed_packet = 1M
table_open_cache = 64
sort_buffer_size = 512K
net_buffer_length = 8K
read_buffer_size = 256K
read_rnd_buffer_size = 512K
myisam_sort_buffer_size = 8M
innodb_buffer_pool_size=512M
innodb_flush_log_at_trx_commit=2
innodb_file_per_table=1
slow_query_log=1
general_log=0
expire-logs-days = 31
log-bin=mysql-bin
binlog_format=mixed
server-id       = 1
[mysqldump]
quick
max_allowed_packet = 16M
[mysql]
no-auto-rehash
[myisamchk]
key_buffer_size = 20M
sort_buffer_size = 20M
read_buffer = 2M
write_buffer = 2M
[mysqlhotcopy]
interactive-timeout
EOF
%preun
if [ $1 = 0 ]; then
    /sbin/service mysqld stop >/dev/null 2>&1
    /sbin/chkconfig --del mysqld
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi

%files 
%defattr(-,root,root,0755)

%ghost %config(noreplace,missingok) %{_sysconfdir}/my.cnf
%ghost %config(noreplace,missingok) %{_sysconfdir}/mysqlmanager.passwd

%attr(755, root, root) /usr/local/mysql/bin/innochecksum
%attr(755, root, root) /usr/local/mysql/bin/my_print_defaults
%attr(755, root, root) /usr/local/mysql/bin/myisam_ftdump
%attr(755, root, root) /usr/local/mysql/bin/myisamchk
%attr(755, root, root) /usr/local/mysql/bin/myisamlog
%attr(755, root, root) /usr/local/mysql/bin/myisampack
%attr(755, root, root) /usr/local/mysql/bin/mysql_convert_table_format
%attr(755, root, root) /usr/local/mysql/bin/mysql_fix_extensions
%attr(755, root, root) /usr/local/mysql/bin/mysql_fix_privilege_tables
%attr(755, root, root) /usr/local/mysql/bin/mysql_install_db
%attr(755, root, root) /usr/local/mysql/bin/mysql_secure_installation
%attr(755, root, root) /usr/local/mysql/bin/mysql_setpermission
%attr(755, root, root) /usr/local/mysql/bin/mysql_tzinfo_to_sql
%attr(755, root, root) /usr/local/mysql/bin/mysql_upgrade
%attr(755, root, root) /usr/local/mysql/bin/mysql_zap
%attr(755, root, root) /usr/local/mysql/bin/mysqlbug
%attr(755, root, root) /usr/local/mysql/bin/mysqld_multi
%attr(755, root, root) /usr/local/mysql/bin/mysqld_safe
%attr(755, root, root) /usr/local/mysql/bin/mysqldumpslow
%attr(755, root, root) /usr/local/mysql/bin/mysqlhotcopy
%attr(755, root, root) /usr/local/mysql/bin/mysqltest
%attr(755, root, root) /usr/local/mysql/bin/perror
%attr(755, root, root) /usr/local/mysql/bin/replace
%attr(755, root, root) /usr/local/mysql/bin/resolve_stack_dump
%attr(755, root, root) /usr/local/mysql/bin/resolveip

%attr(755, root, root) /usr/local/mysql/bin/mysqld
%attr(755, root, root) /usr/local/mysql/bin/mysqld-debug
%attr(755, root, root) /usr/local/mysql/bin/mysqlmanager
%attr(755, root, root) /usr/local/mysql/bin/rcmysql

%attr(644, root, root) %config(noreplace,missingok) %{_sysconfdir}/logrotate.d/mysql
%attr(755, root, root) %{_sysconfdir}/init.d/mysql

%attr(755, root, root) %{_datadir}/mysql/

%attr(755, root, root) /usr/local/mysql/bin/msql2mysql
%attr(755, root, root) /usr/local/mysql/bin/mysql
%attr(755, root, root) /usr/local/mysql/bin/mysql_find_rows
%attr(755, root, root) /usr/local/mysql/bin/mysql_waitpid
%attr(755, root, root) /usr/local/mysql/bin/mysqlaccess
%attr(755, root, root) /usr/local/mysql/bin/mysqladmin
%attr(755, root, root) /usr/local/mysql/bin/mysqlbinlog
%attr(755, root, root) /usr/local/mysql/bin/mysqlcheck
%attr(755, root, root) /usr/local/mysql/bin/mysqldump
%attr(755, root, root) /usr/local/mysql/bin/mysqlimport
%attr(755, root, root) /usr/local/mysql/bin/mysqlshow
%attr(755, root, root) /usr/local/mysql/bin/mysqlslap

%attr(755, root, root) /usr/local/mysql/bin/mysql_config
%dir %attr(755, root, root) /usr/local/mysql/include/mysql
%dir %attr(755, root, root) /usr/local/mysql/lib/mysql
/usr/local/mysql/include/mysql/mysql/*
/usr/local/mysql/lib/mysql/libdbug.a
/usr/local/mysql/lib/mysql/libheap.a
%if %{have_libgcc}
/usr/local/mysql/lib/mysql/libmygcc.a
%endif
/usr/local/mysql/lib/mysql/libmyisam.a
/usr/local/mysql/lib/mysql/libmyisammrg.a
/usr/local/mysql/lib/mysql/libmysqlclient.a
/usr/local/mysql/lib/mysql/libmysqlclient.la
/usr/local/mysql/lib/mysql/libmysqlclient_r.a
/usr/local/mysql/lib/mysql/libmysqlclient_r.la
/usr/local/mysql/lib/mysql/libmystrings.a
/usr/local/mysql/lib/mysql/libmysys.a
/usr/local/mysql/lib/mysql/libvio.a
/usr/local/mysql/lib/mysql/libz.a
/usr/local/mysql/lib/mysql/libz.la


/usr/local/mysql/lib/mysql/libmysql*.so*


%changelog
* Sun Nov 12 2011 Ken <ken@shopex.cn> - 5.1.48
- new release  5.1.48

