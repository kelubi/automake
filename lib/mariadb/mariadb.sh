#!/bin/bash
#

if [ $(uname -m) = 'x86_64' ] &&  grep "CentOS" /etc/issue > /dev/null ; then
    cat > /etc/yum.repos.d/mariadb.repo <<'EOF'
# MariaDB 10.0 CentOS repository list - created 2013-05-21 10:28 UTC
# # http://mariadb.org/mariadb/repositories/
[mariadb]
name = MariaDB
baseurl = http://yum.mariadb.org/10.0/centos6-amd64
gpgkey=https://yum.mariadb.org/RPM-GPG-KEY-MariaDB
gpgcheck=1

EOF
fi

if [ $(uname -m) = 'x86_64' ] grep -E "CentOS release 5" /etc/issue > /dev/null ;then
    cat > /etc/yum.repos.d/mariadb.repo <<'EOF'
# MariaDB 10.0 CentOS repository list - created 2013-05-21 11:11 UTC
# http://mariadb.org/mariadb/repositories/
[mariadb]
name = MariaDB
baseurl = http://yum.mariadb.org/10.0/centos5-amd64
gpgkey=https://yum.mariadb.org/RPM-GPG-KEY-MariaDB
gpgcheck=1

EOF
fi


sudo yum install MariaDB-server MariaDB-client

#usage
