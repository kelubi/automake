Summary:   Package created with checkinstall 1.6.2
Name:      libmcrypt
Version:   2.5.8
Release:   shopex
License: GPL
Packager:  checkinstall-1.6.2
Group:     Applications/shopex          
BuildRoot: /var/tmp/tmp.rHWxn10260/package
Provides:  libmcrypt
Requires:  ,/bin/sh
Source     : %{name}-%{version}.tar.gz

%description
Package created with checkinstall 1.6.2

%prep
%setup -q

%build
CFLAGS=${RPM_OPT_FLAGS} CXXFLAGS=${RPM_OPT_FLAGS} 
./configure --prefix=/usr
make

%install
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
%dir "//usr/include/mutils/"
"//usr/include/mutils/mcrypt.h"
"//usr/include/mcrypt.h"
%dir "//usr/man/"
%dir "//usr/man/man3/"
"//usr/man/man3/mcrypt.3.gz"
%dir "//usr/bin/"
"//usr/bin/libmcrypt-config"
%dir "//usr/lib/"
%dir "//usr/lib/libmcrypt.so"
"//usr/lib/libmcrypt.la"
"//usr/lib/libmcrypt.so.4.4.8"
%dir "//usr/lib/libmcrypt.so.4"
%dir "//usr/doc/"
%dir "//usr/doc/libmcrypt/"
"//usr/doc/libmcrypt/THANKS"
"//usr/doc/libmcrypt/KNOWN-BUGS"
"//usr/doc/libmcrypt/TODO"
"//usr/doc/libmcrypt/COPYING.LIB"
"//usr/doc/libmcrypt/README"
"//usr/doc/libmcrypt/NEWS"
"//usr/doc/libmcrypt/INSTALL"
"//usr/doc/libmcrypt/ChangeLog"
"//usr/doc/libmcrypt/AUTHORS"
%dir "//usr/doc/libmcrypt/doc/"
"//usr/doc/libmcrypt/doc/Makefile.am"
"//usr/doc/libmcrypt/doc/Makefile"
"//usr/doc/libmcrypt/doc/README.xtea"
"//usr/doc/libmcrypt/doc/README.config"
"//usr/doc/libmcrypt/doc/README.key"
"//usr/doc/libmcrypt/doc/example.c"
"//usr/doc/libmcrypt/doc/Makefile.in"
"//usr/doc/libmcrypt/doc/mcrypt.3"
%dir "//usr/share/"
%dir "//usr/share/aclocal/"
"//usr/share/aclocal/libmcrypt.m4"

%changelog

* Tue Nov 29 2011 xiaquan <xiaquan@shopex.cn>
- update to shopex only
