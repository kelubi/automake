Summary:   Package created with checkinstall 1.6.2
Name:      libiconv
Version:   1.14
Release:   shopex
License: GPL
Packager:  checkinstall-1.6.2
Group:     Applications/shopex          
BuildRoot: /var/tmp/tmp.JjyCN12269/package
Provides:  libiconv
Requires:  ,/bin/sh
Source     :%{name}-%{version}.tar.gz

%description
Package created with checkinstall 1.6.2

%prep
%setup -q

%build
CFLAGS=${RPM_OPT_FLAGS} CXXFLAGS=${RPM_OPT_FLAGS} 
./configure --prefix=/usr/local
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
%dir "//usr/local/"
%dir "//usr/local/include/"
"//usr/local/include/localcharset.h"
"//usr/local/include/libcharset.h"
"//usr/local/include/iconv.h"
%dir "//usr/local/bin/"
"//usr/local/bin/iconv"
%dir "//usr/local/lib/"
%dir "//usr/local/lib/libcharset.so.1"
"//usr/local/lib/libiconv.la"
%dir "//usr/local/lib/libiconv.so.2"
"//usr/local/lib/preloadable_libiconv.so"
%dir "//usr/local/lib/libcharset.so"
"//usr/local/lib/libiconv.so.2.5.1"
"//usr/local/lib/libcharset.so.1.0.0"
"//usr/local/lib/libcharset.la"
"//usr/local/lib/charset.alias"
%dir "//usr/local/lib/libiconv.so"
"//usr/local/lib/libcharset.a"
%dir "//usr/local/share/"
%dir "//usr/local/share/man/"
%dir "//usr/local/share/man/man1/"
"/usr/local/share/man/man1/iconv.1"
"//usr/local/share/man/man1/iconv.1.gz"
%dir "//usr/local/share/man/man3/"
"//usr/local/share/man/man3/iconv_close.3.gz"
"//usr/local/share/man/man3/iconv_open_into.3.gz"
"//usr/local/share/man/man3/iconv_open.3.gz"
"//usr/local/share/man/man3/iconv.3.gz"
"//usr/local/share/man/man3/iconvctl.3.gz"
"/usr/local/share/man/man1/iconv.1"
"/usr/local/share/man/man3/iconv.3"
"/usr/local/share/man/man3/iconv_close.3"
"/usr/local/share/man/man3/iconv_open.3"
"/usr/local/share/man/man3/iconv_open_into.3"
"/usr/local/share/man/man3/iconvctl.3"
%dir "//usr/local/share/locale/"
%dir "//usr/local/share/locale/gl/"
%dir "//usr/local/share/locale/gl/LC_MESSAGES/"
"//usr/local/share/locale/gl/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/id/"
%dir "//usr/local/share/locale/id/LC_MESSAGES/"
"//usr/local/share/locale/id/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/af/"
%dir "//usr/local/share/locale/af/LC_MESSAGES/"
"//usr/local/share/locale/af/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/da/"
%dir "//usr/local/share/locale/da/LC_MESSAGES/"
"//usr/local/share/locale/da/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/sl/"
%dir "//usr/local/share/locale/sl/LC_MESSAGES/"
"//usr/local/share/locale/sl/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/el/"
%dir "//usr/local/share/locale/el/LC_MESSAGES/"
"//usr/local/share/locale/el/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/sr/"
%dir "//usr/local/share/locale/sr/LC_MESSAGES/"
"//usr/local/share/locale/sr/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/ca/"
%dir "//usr/local/share/locale/ca/LC_MESSAGES/"
"//usr/local/share/locale/ca/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/vi/"
%dir "//usr/local/share/locale/vi/LC_MESSAGES/"
"//usr/local/share/locale/vi/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/sv/"
%dir "//usr/local/share/locale/sv/LC_MESSAGES/"
"//usr/local/share/locale/sv/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/eo/"
%dir "//usr/local/share/locale/eo/LC_MESSAGES/"
"//usr/local/share/locale/eo/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/fr/"
%dir "//usr/local/share/locale/fr/LC_MESSAGES/"
"//usr/local/share/locale/fr/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/de/"
%dir "//usr/local/share/locale/de/LC_MESSAGES/"
"//usr/local/share/locale/de/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/rm/"
%dir "//usr/local/share/locale/rm/LC_MESSAGES/"
"//usr/local/share/locale/rm/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/it/"
%dir "//usr/local/share/locale/it/LC_MESSAGES/"
"//usr/local/share/locale/it/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/es/"
%dir "//usr/local/share/locale/es/LC_MESSAGES/"
"//usr/local/share/locale/es/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/zh_TW/"
%dir "//usr/local/share/locale/zh_TW/LC_MESSAGES/"
"//usr/local/share/locale/zh_TW/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/ja/"
%dir "//usr/local/share/locale/ja/LC_MESSAGES/"
"//usr/local/share/locale/ja/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/cs/"
%dir "//usr/local/share/locale/cs/LC_MESSAGES/"
"//usr/local/share/locale/cs/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/ro/"
%dir "//usr/local/share/locale/ro/LC_MESSAGES/"
"//usr/local/share/locale/ro/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/ga/"
%dir "//usr/local/share/locale/ga/LC_MESSAGES/"
"//usr/local/share/locale/ga/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/nl/"
%dir "//usr/local/share/locale/nl/LC_MESSAGES/"
"//usr/local/share/locale/nl/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/hu/"
%dir "//usr/local/share/locale/hu/LC_MESSAGES/"
"//usr/local/share/locale/hu/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/et/"
%dir "//usr/local/share/locale/et/LC_MESSAGES/"
"//usr/local/share/locale/et/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/pt_BR/"
%dir "//usr/local/share/locale/pt_BR/LC_MESSAGES/"
"//usr/local/share/locale/pt_BR/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/bg/"
%dir "//usr/local/share/locale/bg/LC_MESSAGES/"
"//usr/local/share/locale/bg/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/wa/"
%dir "//usr/local/share/locale/wa/LC_MESSAGES/"
"//usr/local/share/locale/wa/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/hr/"
%dir "//usr/local/share/locale/hr/LC_MESSAGES/"
"//usr/local/share/locale/hr/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/sk/"
%dir "//usr/local/share/locale/sk/LC_MESSAGES/"
"//usr/local/share/locale/sk/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/tr/"
%dir "//usr/local/share/locale/tr/LC_MESSAGES/"
"//usr/local/share/locale/tr/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/fi/"
%dir "//usr/local/share/locale/fi/LC_MESSAGES/"
"//usr/local/share/locale/fi/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/pl/"
%dir "//usr/local/share/locale/pl/LC_MESSAGES/"
"//usr/local/share/locale/pl/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/zh_CN/"
%dir "//usr/local/share/locale/zh_CN/LC_MESSAGES/"
"//usr/local/share/locale/zh_CN/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/sq/"
%dir "//usr/local/share/locale/sq/LC_MESSAGES/"
"//usr/local/share/locale/sq/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/uk/"
%dir "//usr/local/share/locale/uk/LC_MESSAGES/"
"//usr/local/share/locale/uk/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/locale/ru/"
%dir "//usr/local/share/locale/ru/LC_MESSAGES/"
"//usr/local/share/locale/ru/LC_MESSAGES/libiconv.mo"
%dir "//usr/local/share/doc/"
%dir "//usr/local/share/doc/libiconv/"
"//usr/local/share/doc/libiconv/iconv.3.html"
"//usr/local/share/doc/libiconv/iconv_open_into.3.html"
"//usr/local/share/doc/libiconv/iconv_close.3.html"
"//usr/local/share/doc/libiconv/iconv_open.3.html"
"//usr/local/share/doc/libiconv/iconv.1.html"
"//usr/local/share/doc/libiconv/iconvctl.3.html"
%dir "//usr/doc/"
%dir "//usr/doc/libiconv/"
"//usr/doc/libiconv/HACKING"
"//usr/doc/libiconv/THANKS"
"//usr/doc/libiconv/README.djgpp"
"//usr/doc/libiconv/COPYING.LIB"
"//usr/doc/libiconv/INSTALL.generic"
"//usr/doc/libiconv/README"
"//usr/doc/libiconv/NEWS"
"//usr/doc/libiconv/COPYING"
"//usr/doc/libiconv/ChangeLog"
"//usr/doc/libiconv/AUTHORS"
%dir "//usr/doc/libiconv/doc/"
"//usr/doc/libiconv/doc/relocatable.texi"
"//usr/doc/libiconv/README.woe32"
"//usr/doc/libiconv/ABOUT-NLS"

%changelog

* Tue Nov 30 2011 xiaquan <xiaquan@shopex.cn>
- update to shopex only
