Summary:   Package created with checkinstall 1.6.2
Name:      mcrypt
Version:   2.6.8
Release:   shopex
License: GPL
Packager:  checkinstall-1.6.2
Group:     Applications/shopex          
BuildRoot: /var/tmp/tmp.LtmEO29612/package
Provides:  mcrypt
Requires:  libmcrypt,mhash
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
%dir "//usr/bin/"
"//usr/bin/mcrypt"
%dir "//usr/bin/mdecrypt"
%dir "//usr/doc/"
%dir "//usr/doc/mcrypt/"
"//usr/doc/mcrypt/THANKS"
"//usr/doc/mcrypt/TODO"
"//usr/doc/mcrypt/INSTALL.generic"
"//usr/doc/mcrypt/README"
"//usr/doc/mcrypt/NEWS"
"//usr/doc/mcrypt/INSTALL"
"//usr/doc/mcrypt/COPYING"
"//usr/doc/mcrypt/ChangeLog"
"//usr/doc/mcrypt/AUTHORS"
%dir "//usr/doc/mcrypt/doc/"
"//usr/doc/mcrypt/doc/Makefile.am"
"//usr/doc/mcrypt/doc/magic"
"//usr/doc/mcrypt/doc/Makefile"
"//usr/doc/mcrypt/doc/Makefile.in"
"//usr/doc/mcrypt/doc/sample.mcryptrc"
"//usr/doc/mcrypt/doc/mcrypt.1"
"//usr/doc/mcrypt/doc/FORMAT"
"//usr/doc/mcrypt/ABOUT-NLS"
%dir "//usr/share/"
%dir "//usr/share/man/"
%dir "//usr/share/man/man1/"
"//usr/share/man/man1/mcrypt.1.gz"
%dir "//usr/share/locale/"
%dir "//usr/share/locale/es_AR/"
%dir "//usr/share/locale/es_AR/LC_MESSAGES/"
"//usr/share/locale/es_AR/LC_MESSAGES/mcrypt.mo"
%dir "//usr/share/locale/el/"
%dir "//usr/share/locale/el/LC_MESSAGES/"
"//usr/share/locale/el/LC_MESSAGES/mcrypt.mo"
%dir "//usr/share/locale/de/"
%dir "//usr/share/locale/de/LC_MESSAGES/"
"//usr/share/locale/de/LC_MESSAGES/mcrypt.mo"
%dir "//usr/share/locale/cs/"
%dir "//usr/share/locale/cs/LC_MESSAGES/"
"//usr/share/locale/cs/LC_MESSAGES/mcrypt.mo"
%dir "//usr/share/locale/pl/"
%dir "//usr/share/locale/pl/LC_MESSAGES/"
"//usr/share/locale/pl/LC_MESSAGES/mcrypt.mo"

%changelog

* Tue Nov 30 2011 xiaquan <xiaquan@shopex.cn>
- update to shopex only
