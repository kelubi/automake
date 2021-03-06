#!/bin/sh

# This program is part of LNNPP: http://code.google.com/p/lnmpp
# See "COPYRIGHT, LICENSE, AND WARRANTY" at the end of this file for legal
# notices and disclaimers.

# ########################################################################
# Globals, settings, helper functions
# ########################################################################
POSIXLY_CORRECT=1
export POSIXLY_CORRECT


# ##############################################################################
# The main() function is called at the end of the script.  This makes it
# testable.  
# ##############################################################################
main () {

   # Begin by setting the $PATH to include some common locations that are not
   # always in the $PATH, including the "sbin" locations, and some common
   # locations for proprietary management software, such as RAID controllers.
   export PATH="${PATH}:/usr/local/bin:/usr/bin:/bin:/usr/libexec"
   export PATH="${PATH}:/usr/local/sbin:/usr/sbin:/sbin"

   #set shopex tty style
   set_tty
   #set yum update source
   set_yum_source

   yum update
   
}

check_require()
{

}

set_tty()
{
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

}

set_yum_source()
{
	grep "CentOS" /etc/issue
	if [ $? -eq 0 ]; then
  		rpm -Uvh http://apt.sw.be/redhat/el5/en/x86_64/rpmforge/RPMS//rpmforge-release-0.3.6-1.el5.rf.x86_64.rpm
	else
      rpm -Uvh http://apt.sw.be/redhat/el6/en/x86_64/rpmforge/RPMS/rpmforge-release-0.5.3-1.el6.rf.x86_64.rpm
  fi
}


set_parameters()
{
  yum install -y ntp
  /usr/sbin/ntpdate -d cn.pool.ntp.org
  date
  sed -i "/\*  \* \* \* \* /usr/sbin/ntpdate cn.pool.ntp.org/d" /var/spool/cron/root
  echo "* * * * * /usr/sbin/ntpdate cn.pool.ntp.org" >> /var/spool/cron/root
  crontab -l
  sleep 1

  #Disable SeLinux
  if [ -s /etc/selinux/config ]; then
  sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
  fi

  cat > /etc/sysconfig/iptables << 'EOF'
# Generated by iptables-save v1.3.5 on Tue Aug  2 02:00:13 2011
*filter
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [70202:5483561]
:RH-Firewall-1-INPUT - [0:0]
-A INPUT -j RH-Firewall-1-INPUT 
-A FORWARD -j RH-Firewall-1-INPUT 
-A RH-Firewall-1-INPUT -i lo -j ACCEPT 
-A RH-Firewall-1-INPUT -p icmp -m icmp --icmp-type any -j ACCEPT 
-A RH-Firewall-1-INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT 
-A RH-Firewall-1-INPUT -p tcp -m state --state NEW -m tcp --dport 21 -j ACCEPT 
-A RH-Firewall-1-INPUT -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT 
-A RH-Firewall-1-INPUT -p tcp -m state --state NEW -m tcp --dport 80 -j ACCEPT 
-A RH-Firewall-1-INPUT -p tcp -m state --state NEW -m tcp --dport 8081 -j ACCEPT 
-A RH-Firewall-1-INPUT -s 60.195.249.83 -p udp -m state --state NEW -m udp --dport 161 -j ACCEPT 
-A RH-Firewall-1-INPUT -s 60.195.252.107 -p udp -m state --state NEW -m udp --dport 161 -j ACCEPT 
-A RH-Firewall-1-INPUT -s 60.195.252.110 -p udp -m state --state NEW -m udp --dport 161 -j ACCEPT 
-A RH-Firewall-1-INPUT -s 60.195.252.106 -p tcp -m tcp --dport 3306 -j ACCEPT 
-A RH-Firewall-1-INPUT -s 60.195.249.83 -p tcp -m tcp --dport 3306 -j ACCEPT 
-A RH-Firewall-1-INPUT -j REJECT --reject-with icmp-host-prohibited 
COMMIT
# Completed on Tue Aug  2 02:00:13 2011

EOF

  iptables-restore < /etc/sysconfig/iptables
  service iptables save
  service iptables restart
  iptables -vnL
  sleep 1

  modprobe ip_conntrack_ftp
  if [ $? -eq 0 ]; then
      sed -i "/modprobe ip_conntrack_ftp/d" /etc/rc.d/rc.local 
      echo "modprobe ip_conntrack_ftp" >> /etc/rc.d/rc.local 
  fi
  modprobe ip_nat_ftp
  if [ $? -eq 0 ]; then
      sed -i "/modprobe ip_nat_ftp/d" /etc/rc.d/rc.local 
      echo "modprobe ip_nat_ftp" >> /etc/rc.d/rc.local 
  fi


  cat > /etc/sysctl.conf << 'EOF'
net.ipv4.ip_forward = 0
net.ipv4.conf.default.rp_filter = 1
net.ipv4.conf.default.accept_source_route = 0
kernel.sysrq = 0
kernel.core_uses_pid = 1
net.ipv4.tcp_syncookies = 1
kernel.msgmnb = 65536
kernel.msgmax = 65536
kernel.shmmax = 4294967295
kernel.shmall = 268435456
net.ipv4.tcp_max_syn_backlog = 65536
net.core.netdev_max_backlog = 32768
net.core.somaxconn = 32768
net.core.wmem_default = 8388608
net.core.rmem_default = 8388608
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_timestamps = 0
net.ipv4.tcp_synack_retries = 2
net.ipv4.tcp_syn_retries = 2
net.ipv4.tcp_tw_recycle = 1
net.ipv4.tcp_tw_reuse = 0
net.ipv4.tcp_mem = 94500000 915000000 927000000
net.ipv4.tcp_max_orphans = 3276800
net.ipv4.ip_local_port_range = 1024  65535
kernel.shmmax = 268435456
net.ipv4.ip_conntrack_max = 655360
net.ipv4.netfilter.ip_conntrack_tcp_timeout_established = 180

EOF

  /sbin/sysctl -p
  sleep 1

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
    smartd
    xfs 
    yum-updatesd 
    hplip
    hidd
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

  #set idle time
  sed -i 's,^#ClientAliveCountMax.*,ClientAliveCountMax 60,g' /etc/ssh/sshd_config
  /etc/init.d/sshd restart
}


# Execute the program if it was not included from another file.  This makes it
# possible to include without executing, and thus test.

main $@


# ############################################################################
# Documentation
# ############################################################################
:<<'DOCUMENTATION'

Usage: install

Download and run:

   wget http://lnmpp.googlecode.com/svn/trunk/install.sh
   bash ./install.sh

Download and run in a single step:

   wget -O- http://lnmpp.googlecode.com/svn/trunk/install.sh | bash


 last modified by ken@shopex.cn

DOCUMENTATION