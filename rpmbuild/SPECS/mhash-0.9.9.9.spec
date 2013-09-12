Summary:   Package created with checkinstall 1.6.2
Name:      mhash
Version:   0.9.9.9
Release:   shopex
License: GPL
Packager:  checkinstall-1.6.2
Group:     Applications/shopex          
BuildRoot: /var/tmp/tmp.ZINoXn7412/package
Provides:  mhash
Requires:  ,/bin/sh
Source:    %{name}-%{version}.tar.gz

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
"//usr/include/mutils/mhash_config.h"
"//usr/include/mutils/mhash.h"
"//usr/include/mutils/mtypes.h"
"//usr/include/mutils/mutils.h"
"//usr/include/mutils/mincludes.h"
"//usr/include/mutils/mglobal.h"
"//usr/include/mhash.h"
%dir "//usr/lib/"
%dir "//usr/lib/libmhash.so"
"//usr/lib/libmhash.la"
"//usr/lib/libmhash.a"
"//usr/lib/libmhash.so.2.0.1"
%dir "//usr/lib/libmhash.so.2"
%dir "//usr/doc/"
%dir "//usr/doc/mhash/"
"//usr/doc/mhash/THANKS"
"//usr/doc/mhash/TODO"
"//usr/doc/mhash/README"
"//usr/doc/mhash/NEWS"
"//usr/doc/mhash/INSTALL"
"//usr/doc/mhash/COPYING"
"//usr/doc/mhash/ChangeLog"
"//usr/doc/mhash/AUTHORS"
%dir "//usr/doc/mhash/doc/"
"//usr/doc/mhash/doc/Makefile.am"
"//usr/doc/mhash/doc/.cvsignore"
"//usr/doc/mhash/doc/Makefile"
"//usr/doc/mhash/doc/example.c"
%dir "//usr/doc/mhash/doc/CVS/"
"//usr/doc/mhash/doc/CVS/Root"
"//usr/doc/mhash/doc/CVS/Entries"
"//usr/doc/mhash/doc/CVS/Repository"
"//usr/doc/mhash/doc/Makefile.in"
"//usr/doc/mhash/doc/mhash.3"
"//usr/doc/mhash/doc/skid2-authentication"
"//usr/doc/mhash/doc/mhash.pod"
%dir "//usr/share/"
%dir "//usr/share/man/"
%dir "//usr/share/man/man3/"
"//usr/share/man/man3/mhash.3.gz"

%changelog

* Tue Nov 30 2011 xiaquan <xiaquan@shopex.cn>
- update to shopex only
