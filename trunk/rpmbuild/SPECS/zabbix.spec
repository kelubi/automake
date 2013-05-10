%define name zabbix
%define version 1.8.7
%define release 1

Summary: Zabbix is an enterprise-class open source distributed monitoring solution for networks and applications.
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.gz
Source1: zabbix.init
Source2: zabbix-agent.init
Source3: zabbix-proxy.init
License: LGPL
Group: Development/Tools
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
Url: http://www.zabbix.com/

BuildRequires: iksemel-devel postgresql 
BuildRequires: net-snmp OpenIPMI-devel
Requires: iksemel sqlite net-snmp OpenIPMI-libs
Requires: zabbix-tools

%description
Zabbix is an enterprise-class open source distributed monitoring solution for networks and applications.

%package tools
Summary: Zabbix tools
Group: Development/Tools
%description tools
zabbix_get zabbix_sender

%package proxy
Summary: Zabbix tools
Group: Development/Tools
%description proxy
zabbix proxy

%package agent
Summary: Zabbix tools
Group: Development/Tools
%description agent
zabbix agent
Requires: zabbix-tools

%package web
Summary: Zabbix tools
Group: Development/Tools
%description web
zabbix web

#%package pgsql
#Summary: Zabbix pgsql
#Group: Development/Tools
#%description pgsql
#zabbix pgsql
#
#%package: mysql
#%description
#zabbix mysql support
#Requires: mysql

%prep
%setup

%build
./configure --prefix=%{_prefix} \
	 --enable-server \
	--enable-proxy \
	--enable-agent \
	--with-pgsql \
	--with-libcurl \
	--with-jabber \
	 -with-net-snmp \
	--with-openipmi
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_prefix}/share $RPM_BUILD_ROOT/etc/init.d
cp %SOURCE1 $RPM_BUILD_ROOT/etc/init.d/zabbix
cp %SOURCE2 $RPM_BUILD_ROOT/etc/init.d/zabbix-agent
cp %SOURCE3 $RPM_BUILD_ROOT/etc/init.d/zabbix-proxy
cp -r misc/conf $RPM_BUILD_ROOT/etc/zabbix
rm -f $RPM_BUILD_ROOT/etc/zabbix/zabbix_agentd.win.conf
cp -r frontends/php $RPM_BUILD_ROOT%{_prefix}/share/zabbix
cp -r create $RPM_BUILD_ROOT%{_prefix}/share/zabbix/create
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/sbin/zabbix_server
/etc/zabbix/zabbix_server.conf
/usr/share/man/man8/zabbix_server.8.gz
/usr/share/zabbix/create
%attr(0755,root,root) /etc/init.d/zabbix

%files tools
%defattr(-,root,root)
/usr/bin/zabbix_get
/usr/bin/zabbix_sender
/usr/share/man/man1/zabbix_get.1.gz
/usr/share/man/man1/zabbix_sender.1.gz

%files agent
%defattr(-,root,root)
/usr/sbin/zabbix_agent
/usr/sbin/zabbix_agentd
/usr/share/man/man8/zabbix_agentd.8.gz
/etc/zabbix/zabbix_agent.conf
/etc/zabbix/zabbix_agentd.conf
/etc/zabbix/zabbix_agentd/userparameter_examples.conf
/etc/zabbix/zabbix_agentd/userparameter_mysql.conf
%attr(0755,root,root) /etc/init.d/zabbix-agent

%files proxy
%defattr(-,root,root)
/usr/sbin/zabbix_proxy
/etc/zabbix/zabbix_proxy.conf
/usr/share/man/man8/zabbix_proxy.8.gz
%attr(0755,root,root) /etc/init.d/zabbix-proxy

%files web
%defattr(-,root,root)
%{_prefix}/share/zabbix
