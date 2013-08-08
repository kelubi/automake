#!/bin/sh


#scp -r /usr/local/lib/* web-6:/usr/local/lib
#scp -r /usr/local/mysql web-6:/usr/local
#scp -r /usr/local/php web-6:/usr/local
#scp -r /usr/local/nginx web-6:/usr/local
#scp -r /usr/local/zabbix2 web-6:/usr/local
#scp -r /etc/init.d/zabbix_agentd2 web-6:/etc/init.d
#scp -r /etc/init.d/nginx web-6:/etc/init.d
#scp -r /etc/init.d/mysqld web-6:/etc/init.d
#scp -r /etc/init.d/php-fpm web-6:/etc/init.d
#scp -r /opt/munin/ web-6:/opt/
#scp -r /etc/opt/ web-6:/etc/


cat  >/etc/profile.d/shopex_tty.sh<<'EOF' 
#!/bin/bash

IPADDRS=`/sbin/ifconfig | grep -P -o "((eth[\w:]+)|(addr:[\d.]+)|(lo[\d:]*))" | perl -e '%face;foreach (<STDIN>){$int=$1 if (/((?:(?:eth)|(?:lo))[\d:]*)/);$face{$int}=$1 if (/addr:([\d.]+)/);};foreach $interf (sort keys %face){print "$interf = $face{$interf}\t" if ($interf !~ /^lo$/)}'`

if [ $UID -eq 0 ]
then
        PS1="\n\n\033[1;34m[\u@\H]\e[m  \033[1;33m$IPADDRS\e[m \n[\t] PWD => \033[1;35m\w\e[m\n\#># "
else
        PS1="\n\n\033[1;34m[\u@\H]\e[m  \033[1;33m$IPADDRS\e[m \n[\t] PWD => \033[1;35m\w\e[m\n\#>\$ "
fi

EOF

source /etc/profile




#Disable SeLinux
if [ -s /etc/selinux/config ]; then
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
fi


cat > /etc/sysctl.conf << 'EOF'
net.ipv4.ip_forward = 1
net.ipv4.conf.default.rp_filter = 1
net.ipv4.conf.default.accept_source_route = 0
kernel.sysrq = 0
kernel.core_uses_pid = 1
net.ipv4.tcp_syncookies = 1
kernel.msgmnb = 65536
kernel.msgmax = 65536
kernel.shmmax = 4294967295
kernel.shmall = 268435456
net.ipv4.tcp_keepalive_time =1200
net.ipv4.tcp_keepalive_probes =5
net.ipv4.tcp_keepalive_intvl =15
net.core.rmem_max =16777216
net.core.wmem_max =16777216
net.ipv4.tcp_rmem =4096 87380 16777216
net.ipv4.tcp_wmem =4096 65536 16777216
net.ipv4.tcp_fin_timeout = 60
net.ipv4.tcp_tw_recycle = 1
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_max_tw_buckets = 10000
net.core.netdev_max_backlog = 819200
net.ipv4.tcp_no_metrics_save =1
net.core.somaxconn = 262144
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_orphans = 262144
net.ipv4.tcp_max_syn_backlog = 262144
net.ipv4.tcp_synack_retries = 2
net.ipv4.tcp_syn_retries = 2
net.ipv4.tcp_max_syn_backlog = 8192
net.ipv4.tcp_window_scaling = 1
net.ipv4.ip_local_port_range = 1024    65000
net.ipv4.netfilter.ip_conntrack_max = 131072
net.nf_conntrack_max = 131072
net.ipv4.netfilter.ip_conntrack_tcp_timeout_established = 216000

EOF

/sbin/sysctl -p


cat > /etc/security/limits.conf <<'EOF'
*               soft    nofile          65532
*               hard    nofile          65532
EOF

ulimit -a
sleep 1

declare -a closelist
closelist=(
    avahi-daemon
    bluetooth
    cpuspeed 
    cups
    firstboot
    gpm 
    ip6tables
    isdn
    lvm2-monitor
    mdmonitor 
    netfs 
    nfslock
    pcscd
    portmap
    rhnsd
    rpcgssd 
    rpcidmapd 
    xfs 
    yum-updatesd 
    hplip
    hidd
    ntpd
)

for((count=0,i=0;count<${#closelist[@]};i++))
do
    script_name=${closelist[i]}
    /sbin/chkconfig --list | grep $script_name
    if [ $? -eq 0 ]; then
        if [ -f /etc/init.d/$script_name ]; then
            /etc/init.d/$script_name stop
        fi     
        cmd="/sbin/chkconfig $script_name --level 3 off"
        echo $cmd
        `$cmd`
    fi
    let count+=1
done

grep "unset MAILCHECK" /etc/profile
if [ $? -ne 0 ]; then
    sed -i "/unset MAILCHECK/d" /etc/profile
    echo "unset MAILCHECK"  >> /etc/profile
fi

rpm -Uvh http://apt.sw.be/redhat/el5/en/x86_64/rpmforge/RPMS//rpmforge-release-0.3.6-1.el5.rf.x86_64.rpm
rpm -ivh http://mirrors.sohu.com/fedora-epel/5/x86_64/epel-release-5-4.noarch.rpm


yum install -y ntp
/usr/sbin/ntpdate -d cn.pool.ntp.org
date
sed -i "/\*  \* \* \* \* /usr/sbin/ntpdate cn.pool.ntp.org/d" /var/spool/cron/root
echo "* * * * * /usr/sbin/ntpdate cn.pool.ntp.org" >> /var/spool/cron/root
crontab -l
sleep 1

yum install -y salt-minion
sed  -i 's,#master: salt,master: BD,g' /etc/salt/minion
/etc/init.d/salt-minion start


#uninstall useless package
rpm -qa|grep  httpd
rpm -e httpd
rpm -qa|grep mysql
rpm -e mysql
rpm -qa|grep php
rpm -e php

yum -y remove httpd
yum -y remove php
yum -y remove mysql-server mysql
yum -y remove php-mysql

yum -y install yum-fastestmirror
yum -y remove httpd
yum -y update

#install base
for packages in patch make gcc gcc-c++ gcc-g77 flex bison file libtool libtool-libs autoconf kernel-devel libjpeg libjpeg-devel libpng libpng-devel libpng10 libpng10-devel gd gd-devel freetype freetype-devel libxml2 libxml2-devel zlib zlib-devel glib2 glib2-devel bzip2 bzip2-devel libevent libevent-devel ncurses ncurses-devel curl curl-devel e2fsprogs e2fsprogs-devel krb5 krb5-devel libidn libidn-devel openssl openssl-devel vim-minimal nano fonts-chinese gettext gettext-devel ncurses-devel gmp-devel pspell-devel unzip;
do yum -y install $packages; done


curl  http://lnmpp.googlecode.com/svn/trunk/lib/libmcrypt/libmcrypt-2.5.8.sh | sh
curl  http://lnmpp.googlecode.com/svn/trunk/lib/mhash/mhash-0.9.9.9.sh | sh
curl  http://lnmpp.googlecode.com/svn/trunk/lib/mcrypt/mcrypt-2.6.8.sh | sh
curl  http://lnmpp.googlecode.com/svn/trunk/lib/libiconv/libiconv-1.13.sh | sh
curl  https://raw.github.com/kenee/automake/master/lib/libmemcached/libmemcached-1.0.16.sh| sh


id www > /dev/null 2>&1
if [ $? -ne 0 ]; then
useradd -s /sbin/nologin -M  www
fi

id zabbix > /dev/null 2>&1
if [ $? -ne 0 ]; then
useradd -s /sbin/nologin -M  zabbix
fi

mkdir -pv /data/httpd && mkdir -pv /var/log/nginx && mkdir -pv /var/log/php



eth0=$(ifconfig eth0 | grep "inet addr:" | awk '{print $2}' | awk  -F: '{print $2}')
sed -i 's,10.10.0.2,'$eth0',g' /usr/local/nginx/conf/vhosts/lto2013.nuskin.com.tw.conf

echo "/usr/local/lib" >> /etc/ld.so.conf
ldconfig


#for i in $(netstat -tunlp | grep ^tcp | awk '{print $4}' | awk -F: '{print $2}' | sort -n | uniq | grep -v ^$) ;do  
#/sbin/iptables -A RH-Firewall-1-INPUT -s 10.10.0.0/16 -i eth0 -p tcp -m tcp --dport $i -j ACCEPT
#done


#munin
perl -MCPAN -e 'install Template'
perl -MCPAN -e 'install Net::Server'
echo "/opt/munin/sbin/munin-node --config /etc/opt/munin/munin-node.conf" >> /etc/rc.local
mkdir -pv /var/log/munin
mkdir -pv /var/run/munin
sed -i 's,host_name BD,host_name '$(hostname)',g' /etc/opt/munin/munin-node.conf
/opt/munin/sbin/munin-node --config /etc/opt/munin/munin-node.conf




