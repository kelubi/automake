Summary:   Package created with checkinstall 1.6.2
Name:      tokyocabinet
Version:   1.4.47
Release:   shopex
License: GPL
Packager:  checkinstall-1.6.2
Group:     Applications/shopex          
BuildRoot: /var/tmp/tmp.VbjCoA2770/package
Provides:  tokyocabinet
Requires:  ,/bin/sh
Source         : %{name}-%{version}.tar.gz

%description
Package created with checkinstall 1.6.2

%prep

%setup -q

%build
CFLAGS=${RPM_OPT_FLAGS} CXXFLAGS=${RPM_OPT_FLAGS} 
./configure
make

%install
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%dir "//usr/"
%dir "//usr/local/"
%dir "//usr/local/include/"
"//usr/local/include/tchdb.h"
"//usr/local/include/tcutil.h"
"//usr/local/include/tctdb.h"
"//usr/local/include/tcbdb.h"
"//usr/local/include/tcadb.h"
"//usr/local/include/tcfdb.h"
%dir "//usr/local/bin/"
"//usr/local/bin/tcatest"
"//usr/local/bin/tcbmgr"
"//usr/local/bin/tcttest"
"//usr/local/bin/tctmgr"
"//usr/local/bin/tcbmttest"
"//usr/local/bin/tcbtest"
"//usr/local/bin/tchmgr"
"//usr/local/bin/tchmttest"
"//usr/local/bin/tcumttest"
"//usr/local/bin/tcftest"
"//usr/local/bin/tcfmgr"
"//usr/local/bin/tcamttest"
"//usr/local/bin/tcutest"
"//usr/local/bin/tcucodec"
"//usr/local/bin/tctmttest"
"//usr/local/bin/tcfmttest"
"//usr/local/bin/tcamgr"
"//usr/local/bin/tchtest"
%dir "//usr/local/lib/"
%dir "//usr/local/lib/libtokyocabinet.so.9"
"//usr/local/lib/libtokyocabinet.so.9.10.0"
%dir "//usr/local/lib/libtokyocabinet.so"
%dir "//usr/local/lib/pkgconfig/"
"//usr/local/lib/pkgconfig/tokyocabinet.pc"
"//usr/local/lib/libtokyocabinet.a"
%dir "//usr/local/libexec/"
"//usr/local/libexec/tcawmgr.cgi"
%dir "//usr/local/share/"
%dir "//usr/local/share/tokyocabinet/"
"//usr/local/share/tokyocabinet/tokyocabinet.idl"
"//usr/local/share/tokyocabinet/COPYING"
"//usr/local/share/tokyocabinet/ChangeLog"
%dir "//usr/local/share/tokyocabinet/doc/"
"//usr/local/share/tokyocabinet/doc/index.html"
"//usr/local/share/tokyocabinet/doc/logo.png"
"//usr/local/share/tokyocabinet/doc/spex-en.html"
"//usr/local/share/tokyocabinet/doc/spex-ja.html"
"//usr/local/share/tokyocabinet/doc/index.ja.html"
"//usr/local/share/tokyocabinet/doc/logo-ja.png"
"//usr/local/share/tokyocabinet/doc/tokyoproducts.pdf"
"//usr/local/share/tokyocabinet/doc/tokyoproducts.ppt"
"//usr/local/share/tokyocabinet/doc/benchmark.pdf"
"//usr/local/share/tokyocabinet/doc/icon16.png"
"//usr/local/share/tokyocabinet/doc/common.css"
%dir "//usr/local/share/man/"
%dir "//usr/local/share/man/man1/"
"/usr/local/share/man/man1/tcamgr.1"
"/usr/local/share/man/man1/tcamttest.1"
"/usr/local/share/man/man1/tcatest.1"
"/usr/local/share/man/man1/tcbmgr.1"
"/usr/local/share/man/man1/tcbmttest.1"
"/usr/local/share/man/man1/tcbtest.1"
"/usr/local/share/man/man1/tcbtest.1.gz"
"/usr/local/share/man/man1/tcfmgr.1"
"/usr/local/share/man/man1/tcfmttest.1"
"/usr/local/share/man/man1/tcftest.1"
"/usr/local/share/man/man1/tchmgr.1"
"/usr/local/share/man/man1/tchmttest.1"
"/usr/local/share/man/man1/tchtest.1"
"/usr/local/share/man/man1/tctmgr.1"
"/usr/local/share/man/man1/tctmttest.1"
"/usr/local/share/man/man1/tcttest.1"
"/usr/local/share/man/man1/tcucodec.1"
"/usr/local/share/man/man1/tcumttest.1"
"/usr/local/share/man/man1/tcutest.1"
"//usr/local/share/man/man1/tcbmttest.1.gz"
"//usr/local/share/man/man1/tcutest.1.gz"
"//usr/local/share/man/man1/tcatest.1.gz"
"//usr/local/share/man/man1/tchtest.1.gz"
"//usr/local/share/man/man1/tcttest.1.gz"
"//usr/local/share/man/man1/tctmttest.1.gz"
"//usr/local/share/man/man1/tchmgr.1.gz"
"//usr/local/share/man/man1/tcumttest.1.gz"
"//usr/local/share/man/man1/tcbmgr.1.gz"
"//usr/local/share/man/man1/tcucodec.1.gz"
"//usr/local/share/man/man1/tcftest.1.gz"
"//usr/local/share/man/man1/tchmttest.1.gz"
"//usr/local/share/man/man1/tcfmgr.1.gz"
"//usr/local/share/man/man1/tcamgr.1.gz"
"//usr/local/share/man/man1/tcfmttest.1.gz"
"//usr/local/share/man/man1/tctmgr.1.gz"
"//usr/local/share/man/man1/tcamttest.1.gz"
%dir "//usr/local/share/man/man3/"
"/usr/local/share/man/man3/tcadb.3"
"/usr/local/share/man/man3/tcbdb.3"
"/usr/local/share/man/man3/tcfdb.3"
"/usr/local/share/man/man3/tchdb.3"
"/usr/local/share/man/man3/tclist.3"
"/usr/local/share/man/man3/tcmap.3"
"/usr/local/share/man/man3/tcmdb.3"
"/usr/local/share/man/man3/tcmpool.3"
"/usr/local/share/man/man3/tctdb.3"
"/usr/local/share/man/man3/tctree.3"
"/usr/local/share/man/man3/tcutil.3"
"/usr/local/share/man/man3/tcxstr.3"
"/usr/local/share/man/man3/tokyocabinet.3"
"//usr/local/share/man/man3/tcadb.3.gz"
"//usr/local/share/man/man3/tokyocabinet.3.gz"
"//usr/local/share/man/man3/tclist.3.gz"
"//usr/local/share/man/man3/tctree.3.gz"
"//usr/local/share/man/man3/tcmpool.3.gz"
"//usr/local/share/man/man3/tcxstr.3.gz"
"//usr/local/share/man/man3/tcbdb.3.gz"
"//usr/local/share/man/man3/tctdb.3.gz"
"//usr/local/share/man/man3/tchdb.3.gz"
"//usr/local/share/man/man3/tcfdb.3.gz"
"//usr/local/share/man/man3/tcutil.3.gz"
"//usr/local/share/man/man3/tcmap.3.gz"
"//usr/local/share/man/man3/tcmdb.3.gz"
%dir "//usr/doc/"
%dir "//usr/doc/tokyocabinet/"
"//usr/doc/tokyocabinet/README"
"//usr/doc/tokyocabinet/COPYING"
"//usr/doc/tokyocabinet/ChangeLog"
%dir "//usr/doc/tokyocabinet/doc/"
"//usr/doc/tokyocabinet/doc/index.html"
"//usr/doc/tokyocabinet/doc/logo.png"
"//usr/doc/tokyocabinet/doc/spex-en.html"
"//usr/doc/tokyocabinet/doc/spex-ja.html"
"//usr/doc/tokyocabinet/doc/index.ja.html"
"//usr/doc/tokyocabinet/doc/logo-ja.png"
"//usr/doc/tokyocabinet/doc/tokyoproducts.pdf"
"//usr/doc/tokyocabinet/doc/tokyoproducts.ppt"
"//usr/doc/tokyocabinet/doc/benchmark.pdf"
"//usr/doc/tokyocabinet/doc/icon16.png"
"//usr/doc/tokyocabinet/doc/common.css"

%changelog

* Tue Dec 1 2011 xiaquan <xiaquan@shopex.cn>
- update to shopex only
