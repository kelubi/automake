%define prefix	/usr/local/mysql
%define user	mysql
%define datadir /data/mysql

Summary:   Package created with checkinstall 1.6.2
Name:       mysql
Version:     5.1.48
Release:     shopex
License:     GPL
Packager:  checkinstall-1.6.2
Group:      ShopEx/runtime          
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Provides:  mysql
Requires:  cmake
Source  : %{name}-%{version}.tar.gz

%description
Package created with checkinstall 1.6.2

%prep
%setup -q
id mysql > /dev/null 2>1
if [ $? -ne 0 ]; then
	useradd -s /sbin/nologin -M  %{user}
fi

%build

export DESTDIR=%{buildroot}
./configure --prefix=%{prefix} \
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
rm -fvr %{buildroot}%{prefix}/sql-bench
rm -fvr %{buildroot}%{prefix}/mysql-test
rm -fvr %{buildroot}%{prefix}/bin/ndb*
rm -fvr %{buildroot}%{prefix}/libexec/ndb*

%post

ln -sv /usr/local/mysql/bin/mysqlcheck /usr/bin
ln -sv /usr/local/mysql/bin/mysqlrepair /usr/bin
ln -sv /usr/local/mysql/bin/mysqloptimize /usr/bin
ln -sv /usr/local/mysql/bin/mysql /usr/bin
ln -sv /usr/local/mysql/bin/mysqladmin /usr/bin
#
mkdir -pv /var/run/mysql
install -v -m755 -o %{user} -g %{user} -d /var/run/mysql
mkdir -pv /var/log/mysql
install -v -m750 -o %{user} -g %{user} -d /var/log/mysql 
touch /var/log/mysql/mysql.{log,err} 
chown %{user}:%{user}  /var/log/mysql/mysql* 
chmod 0660 /var/log/mysql/mysql*
echo "running after package installed..."
echo "/usr/local/mysql/lib/mysql" >> /etc/ld.so.conf
echo "/usr/local/lib" >>/etc/ld.so.conf
ldconfig
ldconfig
if [ -d %{datadir} ]; then
    mv -fv %{datadir} %{datadir}.bak
fi
mkdir -pv %{datadir}
/usr/local/mysql/bin/mysql_install_db --user=mysql --datadir=%{datadir}
chgrp -v  %{user} %{datadir}{,/test,/mysql}
killall mysqld && sleep 3
/usr/local/mysql/bin/mysqld_safe --user=%{user}  --datadir=%{datadir} 2>1 >/dev/null  &
sleep 3
MYSQLD_PASSWORD=$(</dev/urandom tr -dc A-Za-z0-9 | head -c8)     
/usr/local/mysql/bin/mysqladmin -u root  password $MYSQLD_PASSWORD
echo "mysql:root:"$MYSQLD_PASSWORD >> %{datadir}/password.txt
echo "use mysql;delete  from user where password=''" | /usr/local/mysql/bin/mysql -uroot -p$MYSQLD_PASSWORD

install -v -m777 /usr/local/mysql/share/mysql/mysql.server /etc/init.d/mysqld
sed -i s,^basedir=$,basedir=/usr/local/mysql,g /etc/init.d/mysqld
sed -i s,^datadir=$,datadir=%{datadir},g /etc/init.d/mysqld
/sbin/chkconfig mysqld --level 3 on   
if [ -f /etc/my.cnf ] ; then
	mv /etc/my.cnf /etc/my.cnf.bak
fi    
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


%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}


%files
%dir "/usr/local/"
%dir "/usr/local/mysql/"
"/usr/local/mysql/include/*"
"/usr/local/mysql/lib/*"
"/usr/local/mysql/docs/*"
"/usr/local/mysql/share/*"
"/usr/local/mysql/libexec/*"

%attr(755, root, root)    /usr/local/mysql/bin/innochecksum
%attr(755, root, root)    /usr/local/mysql/bin/mysql_client_test
%attr(755, root, root)    /usr/local/mysql/bin/mysql_client_test_embedded
%attr(755, root, root)    /usr/local/mysql/bin/mysql_config
%attr(755, root, root)    /usr/local/mysql/bin/mysqltest_embedded

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

%changelog
* Fri Nov 18 2011 Ken Xu <ken@shopex.cn>
- modify for shopex runtime
