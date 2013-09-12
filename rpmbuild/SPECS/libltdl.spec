%define real_name       libmcrypt

Summary:   Package created with checkinstall 1.6.2
Name:      libmcrypt-libltdl
Version:   2.5.8
Release:   shopex
License: GPL
Packager:  checkinstall-1.6.2
Group:     Applications/shopex          
BuildRoot: /var/tmp/tmp.OplPV27439/package
Provides:  libltdl
Requires:  ,/bin/sh
Source     : %{real_name}-%{version}.tar.gz

%description
Package created with checkinstall 1.6.2

%prep
%setup -q -n %{real_name}-%{version}

%build
CFLAGS=${RPM_OPT_FLAGS} CXXFLAGS=${RPM_OPT_FLAGS}
cd libltdl
./configure --prefix=/usr --enable-ltdl-install

%install
cd libltdl
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%post
ldconfig

%postun
ldconfig

%files
%dir "//usr/"
%dir "//usr/include/"
"//usr/include/ltdl.h"
%dir "//usr/lib/"
"//usr/lib/libltdl.la"
"//usr/lib/libltdl.a"
%dir "//usr/doc/"
%dir "//usr/doc/libltdl/"
"//usr/doc/libltdl/COPYING.LIB"
"//usr/doc/libltdl/README"

%changelog

* Tue Nov 29 2011 xiaquan <xiaquan@shopex.cn>
- add libltdl.so file 
- update to shopex only
