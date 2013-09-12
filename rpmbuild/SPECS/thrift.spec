%define ver 0.5.0

Name:           thrift 
Version:        %{ver}
Release:        shopex
Summary:        facebook thrift
Group:          Development/Languages
License:        ERPL
URL:            http://www.mozilla.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source:        http://archive.apache.org/dist/incubator/thrift/0.5.0-incubating/thrift-%{ver}.tar.gz

BuildRequires:	erlang python php boost-devel

%description 
facebook thrift

%package erlang
Requires: erlang
Summary: thrift erlang
Group: Development/Languages
%description erlang

%package python
Requires: python=2.4
Summary: thrift python
Group: Development/Languages
%description python

%package php
Requires: php=5.3.3
Summary: thrift php
Group: Development/Languages
%description php

%package fb303
Summary: thrift fb303
Group: Development/Languages
%description fb303




%prep
%setup -q

%build
rm -rf $RPM_BUILD_ROOT
./configure --prefix=%{_prefix} --with-python --with-php --with-erlang
make
make DESTDIR=$RPM_BUILD_ROOT install

cd contrib/fb303/
./bootstrap.sh
./configure --prefix=%{_prefix} --with-thriftpath=$RPM_BUILD_ROOT/usr
make
make DESTDIR=$RPM_BUILD_ROOT install

%install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_includedir}/*
/usr/lib/lib*
/usr/lib/pkgconfig
%exclude %{_includedir}/thrift/fb303*
%{_bindir}/*

%files fb303
/usr/include/thrift/fb303/*
/usr/share/fb303/*
/usr/lib/python*/site-packages/fb303/*
/usr/lib/python*/site-packages/fb303_scripts/*
/usr/lib/libfb303.a

%files python
%{_libdir}/python*

%files php
%{_libdir}/php/modules
/usr/lib/php
/etc/php.d

%files erlang
%{_libdir}/erlang/
