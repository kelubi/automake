#!/bin/bash
# Short one-line description of this package.
DESCRIPTION="proftpd ftp server"
# Homepage, not used by Portage directly but handy for developer reference
HOMEPAGE="http://www.proftpd.org/"
SRC_URI="http://lnmpp.googlecode.com/files/proftpd-1.3.3d.tar.bz2"
PKG_NAME=$(basename $SRC_URI)
N="proftpd"
V="1.3.3d"

if [ ! -d /opt/install ]; then
    mkdir -pv /opt/install
fi
echo "go to working dir"
cd /opt/install


id ftpd > /dev/null 2>&1
if [ $? -ne 0 ]; then
    useradd -s /sbin/nologin -M  ftpd
fi

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
echo "Unpacking to pwd"
tar xvf $PKG_NAME

echo "config $N-$V$R..."
cd $N-$V$R
./configure --prefix=/usr/local/proftpd --with-modules=mod_sql:mod_sql_mysql:mod_quotatab:mod_quotatab_sql --with-includes=/usr/local/mysql/include  --with-libraries=/usr/local/mysql/lib
echo "make $N-$V$R..."
CPU_NUM=$(cat /proc/cpuinfo | grep processor | wc -l)
if [ $CPU_NUM -gt 1 ];then
    make -j$CPU_NUM
else
    make
fi
#install
echo "install to $XGPATH_DEST..."
make  install    
cat >/usr/local/proftpd/etc/proftpd.conf<<'EOF'
#Basic setting
ServerName    "FTP Server"
ServerType    standalone
ServerAdmin    root@localhost
DefaultServer   On
ServerIdent    Off
DisplayLogin   /usr/local/proftpd/etc/ftplogin.msg
Port     21
Umask     022
MaxLoginAttempts  5
TimeoutStalled   600
TimeoutLogin   900
TimeoutIdle    600
TimeoutNoTransfer  600
User     ftpd
Group     ftpd
DefaultRoot    ~
RequireValidShell  off
UseReverseDNS   off
IdentLookups   off
AllowStoreRestart  on
AllowRetrieveRestart on
MaxInstances   30
#Access control
<Limit LOGIN>
    AllowAll
</Limit>
<Directory />
    AllowOverwrite on
</Directory>
#MySQL connection setting
SQLConnectInfo  proftpd@127.0.0.1  proftpd PROFTPD_PASSWORD
SQLAuthTypes   Plaintext
SQLUserInfo    ftpusers userid passwd uid gid homedir shell
SQLGroupInfo   ftpgroups groupname gid members
SQLAuthenticate   users groups
SQLNegativeCache  on
#SQLHomedirOnDemand  on
SQLDefaultGID   PROFTPD_GID
SQLDefaultUID   PROFTPD_UID
SQLNamedQuery getcount SELECT "count from ftpusers where userid='%u'"
SQLNamedQuery getlastlogin SELECT "lastlogin from ftpusers where userid='%u'"
SQLNamedQuery updatelogininfo UPDATE "count=count+1,host='%h',lastlogin=current_timestamp() WHERE userid='%u'" ftpusers
SQLShowInfo PASS "230" "You've logged on %{getcount} times,last login at %{getlastlogin}"
SQLLog PASS updatelogininfo
#Disk quota seeting
QuotaDirectoryTally  on
QuotaDisplayUnits  "Mb"
QuotaEngine    on
QuotaShowQuotas   on
SQLNamedQuery get-quota-limit SELECT "name,quota_type,per_session,limit_type,bytes_in_avail,bytes_out_avail,bytes_xfer_avail,files_in_avail,files_out_avail,files_xfer_avail FROM quotalimits WHERE name = '%{0}' AND quota_type='%{1}'"
SQLNamedQuery get-quota-tally SELECT "name,quota_type,bytes_in_used,bytes_out_used,bytes_xfer_used,files_in_used,files_out_used,files_xfer_used FROM quotatallies WHERE name = '%{0}' AND quota_type = '%{1}'"
SQLNamedQuery update-quota-tally UPDATE "bytes_in_used = bytes_in_used + %{0},bytes_out_used = bytes_out_used + %{1},bytes_xfer_used = bytes_xfer_used + %{2},files_in_used = files_in_used + %{3},files_out_used = files_out_used + %{4},files_xfer_used = files_xfer_used + %{5} WHERE name = '%{6}' AND quota_type = '%{7}'" quotatallies
SQLNamedQuery insert-quota-tally INSERT "%{0},%{1},%{2},%{3},%{4},%{5},%{6},%{7}" quotatallies
#QuotaLimitTable sql:/get-quota-limit
#QuotaTallyTable sql:/get-quota-tally/update-quota-tally/insert-quota-tally
EOF

PROFTPD_PASSWORD=$(</dev/urandom tr -dc A-Za-z0-9 | head -c8) 
sed -i "/proftpd:proftpd:/d" /opt/install/password.txt 
echo "proftpd:proftpd:"$PROFTPD_PASSWORD >> /opt/install/password.txt
sed -i  s,PROFTPD_PASSWORD,$PROFTPD_PASSWORD,g /usr/local/proftpd/etc/proftpd.conf
sed -i  s,PROFTPD_UID,$(id ftpd | sed 's,uid=\([0-9]*\)\((.*\),\1,g' ),g /usr/local/proftpd/etc/proftpd.conf
sed -i  s,PROFTPD_GID,$(id ftpd | sed 's,\(.*\) gid=\([0-9]*\)\((.*\),\2,g'),g /usr/local/proftpd/etc/proftpd.conf
#self start
echo "running after package installed..."
PROFTPD_PASSWORD=$(grep "proftpd:proftpd:" /opt/install/password.txt | awk -F: '{print $3}')
MYSQLD_PASSWORD=$(grep "mysql:root:" /opt/install/password.txt | awk -F: '{print $3}')
/usr/local/mysql/bin/mysql  -h127.0.0.1 -uroot  -p$MYSQLD_PASSWORD <<EOF
DROP database IF EXISTS proftpd;
CREATE DATABASE proftpd ;
grant all on proftpd.* to proftpd@127.0.0.1 identified by "$PROFTPD_PASSWORD";
USE proftpd;

CREATE TABLE IF NOT EXISTS ftpgroups (  
    groupname varchar(30) NOT NULL,  
    gid int(11) NOT NULL DEFAULT '1000',  
    members varchar(255) NOT NULL
)ENGINE=MyISAM;

CREATE TABLE IF NOT EXISTS ftpusers (      
    userid varchar(30) NOT NULL,     
    passwd varchar(80) NOT NULL,     
    uid int(10) unsigned NOT NULL DEFAULT '48',     
    gid int(10) unsigned NOT NULL DEFAULT '48',     
    homedir varchar(255) NOT NULL,     
    shell varchar(255) NOT NULL DEFAULT '/sbin/nologin',     
    count int(10) unsigned NOT NULL DEFAULT '0',    
    host varchar(30) NOT NULL,     
    lastlogin varchar(30) NOT NULL,    
    UNIQUE KEY userid (userid)
 ) ENGINE=MyISAM;

CREATE TABLE IF NOT EXISTS quotalimits (     
    name varchar(30) DEFAULT NULL, 
    quota_type enum('user','group','class','all') NOT NULL DEFAULT 'user', 
    per_session enum('false','true') NOT NULL DEFAULT 'false', 
    limit_type enum('soft','hard') NOT NULL DEFAULT 'soft', 
    bytes_in_avail float NOT NULL DEFAULT '0',  bytes_out_avail float NOT NULL DEFAULT '0', 
    bytes_xfer_avail float NOT NULL DEFAULT '0',  
    files_in_avail int(10) unsigned NOT NULL DEFAULT '0', 
    files_out_avail int(10) unsigned NOT NULL DEFAULT '0', 
    files_xfer_avail int(10) unsigned NOT NULL DEFAULT '0'
) ENGINE=MyISAM;

CREATE TABLE IF NOT EXISTS quotatallies (    
    name varchar(30) NOT NULL, 
    quota_type enum('user','group','class','all') NOT NULL DEFAULT 'user', 
    bytes_in_used float NOT NULL DEFAULT '0', 
    bytes_out_used float NOT NULL DEFAULT '0', 
    bytes_xfer_used float NOT NULL DEFAULT '0', 
    files_in_used int(10) unsigned NOT NULL DEFAULT '0', 
    files_out_used int(10) unsigned NOT NULL DEFAULT '0', 
    files_xfer_used int(10) unsigned NOT NULL DEFAULT '0'
) ENGINE=MyISAM;
EOF

install -v -m777 contrib/dist/rpm/proftpd.init.d  /etc/rc.d/init.d/proftpd
sed  -i s,/usr/local/sbin,/usr/local/proftpd/sbin,g /etc/rc.d/init.d/proftpd 
/sbin/chkconfig proftpd --level 3 on
if [ -d /data/httpd ]; then
    chown ftpd:ftpd /data/httpd        
fi
/sbin/service proftpd start

echo "all done"

#调试模式
#/usr/local/proftpd/sbin/proftpd -d9 -n