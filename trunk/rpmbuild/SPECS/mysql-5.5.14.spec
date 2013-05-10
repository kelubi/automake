%define prefix			/usr/local/mysql
Summary:   Package created with checkinstall 1.6.2
Name:       mysql
Version:     5.5.14
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

%build

export DESTDIR=%{buildroot}
cmake . -DCMAKE_INSTALL_PREFIX=%{prefix} -DWITH_INNOBASE_STORAGE_ENGINE=1 -DENABLED_LOCAL_INFILE=1 -DEXTRA_CHARSETS=all -DDEFAULT_CHARSET=utf8 -DDEFAULT_COLLATION=utf8_general_ci  -DMYSQL_USER=mysql  -DWITH_DEBUG=0 -DENABLE_DTRACE=0

make %{?_smp_mflags} 

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALLDIRS=vendor
rm -fvr %{buildroot}%{prefix}/sql-bench
rm -fvr %{buildroot}%{prefix}/mysql-test

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}


%files
%dir "/usr/local/"
%dir "/usr/local/mysql/"
"/usr/local/mysql/INSTALL-BINARY"
"/usr/local/mysql/README"
"/usr/local/mysql/COPYING"
"/usr/local/mysql/support-files/*"
"/usr/local/mysql/scripts/*"
"/usr/local/mysql/include/*"
"/usr/local/mysql/lib/*"
"/usr/local/mysql/docs/*"
"/usr/local/mysql/data/*"
"/usr/local/mysql/bin/*"
"/usr/local/mysql/man/*"
"/usr/local/mysql/share/*"


%changelog
* Fri Nov 18 2011 Ken Xu <ken@shopex.cn>
- modify for shopex runtime
