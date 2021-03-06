Name: tsar
Version: 2.1.0
Release: shopex
Summary: Taobao System Activity Reporter
URL: http://svn.simba.taobao.com/svn/cdn/trunk/tsar/Revision_SVN_REVISION
Group: ShopEx/tools
License: BSD
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source: tsar-%{version}.tar.gz

%description
tsar is Taobao monitor tool for collect system activity status, and report it.
It have a plugin system that is easy for collect plugin development. and may
setup different output target such as local logfile and remote nagios host.

%package devel
Summary: Taobao Tsar Devel
Group: ShopEx/tools
Requires:tsar
%description devel
devel package include tsar header files and module template for the development

%prep
%setup -q

%build
./configure;make clean;make

%install

rm -rf %{buildroot}
mkdir -p %{buildroot}
make install DESTDIR=%{buildroot}


%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}


%files
%defattr(-,root,root)
%config(noreplace) /etc/tsar/tsar.conf
%config(noreplace) /etc/tsar/nagios.conf
/usr/local/tsar/modules/*.so
/etc/cron.d/tsar.cron
/etc/tsar/conf.d
/etc/logrotate.d/tsar.logrotate
/usr/local/man/man8/*

%attr(755,root,root) %dir /usr/bin/tsar

%files devel
%defattr(-,root,root)
/usr/local/tsar/devel/tsar.h
/usr/local/tsar/devel/Makefile.test
/usr/local/tsar/devel/mod_test.c
/usr/local/tsar/devel/mod_test.conf
%attr(755,root,root) %dir /usr/bin/tsardevel

%changelog
* Sun Nov 11 2011 Ken Xu <ken@shopex.com>
- for shopex only
* Wed May 11 2011 Ke Li <kongjian@taobao.com>
- add devel for module develop
* Thu Mar 22 2011 Ke Li <kongjian@taobao.com>
- add nagios conf and include conf support
* Thu Dec  9 2010 Ke Li <kongjian@taobao.com>
- add logrotate for tsar.data
* Tue Apr 26 2010 Bin Chen <kuotai@taobao.com>
- first create tsar rpm package
