Summary:   Package created with checkinstall 1.6.2
Name:      lzo
Version:   2.00
Release:   shopex
License: GPL
Packager:  checkinstall-1.6.2
Group:     Applications/shopex          
BuildRoot: /var/tmp/tmp.KueSmoV583/package
Provides:  lzo
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
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%dir "/usr/"
%dir "/usr/local/"
%dir "/usr/local/include/"
%dir "/usr/local/include/lzo/"
"/usr/local/include/lzo/lzo1x.h"
"/usr/local/include/lzo/lzo2a.h"
"/usr/local/include/lzo/lzodefs.h"
"/usr/local/include/lzo/lzo1b.h"
"/usr/local/include/lzo/lzo1.h"
"/usr/local/include/lzo/lzo_asm.h"
"/usr/local/include/lzo/lzo1y.h"
"/usr/local/include/lzo/lzo1f.h"
"/usr/local/include/lzo/lzo1a.h"
"/usr/local/include/lzo/lzo1c.h"
"/usr/local/include/lzo/lzoutil.h"
"/usr/local/include/lzo/lzo1z.h"
"/usr/local/include/lzo/lzoconf.h"
%dir "/usr/local/lib/"
"/usr/local/lib/liblzo.la"
"/usr/local/lib/liblzo.a"

%changelog

* Sun Nov 20 2011 Ken Xu <ken@shopex.cn>
- update to shopex only
