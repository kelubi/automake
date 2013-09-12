Summary:   Package created with checkinstall 1.6.2
Name:      libevent-2.0.12
Version:   stable
Release:   shopex
License: GPL
Packager:  checkinstall-1.6.2
Group:     Applications/shopex          
BuildRoot: /var/tmp/tmp.RBayt18193/package
Provides:  libevent-2.0.12
Requires:  ,/bin/sh
Source         : %{name}-%{version}.tar.gz

%description
Package created with checkinstall 1.6.2

%prep
%setup -q

%build
CFLAGS=${RPM_OPT_FLAGS} CXXFLAGS=${RPM_OPT_FLAGS}
 ./configure --prefix=%{_prefix} --mandir=%{_mandir}
make

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%dir "/usr/"
%dir "/usr/include/"
"/usr/include/event.h"
"/usr/include/evutil.h"
"/usr/include/evhttp.h"
"/usr/include/evdns.h"
%dir "/usr/include/event2/"
"/usr/include/event2/event.h"
"/usr/include/event2/tag.h"
"/usr/include/event2/rpc.h"
"/usr/include/event2/rpc_struct.h"
"/usr/include/event2/listener.h"
"/usr/include/event2/bufferevent_compat.h"
"/usr/include/event2/event_struct.h"
"/usr/include/event2/tag_compat.h"
"/usr/include/event2/keyvalq_struct.h"
"/usr/include/event2/bufferevent.h"
"/usr/include/event2/bufferevent_struct.h"
"/usr/include/event2/dns.h"
"/usr/include/event2/http_struct.h"
"/usr/include/event2/http.h"
"/usr/include/event2/thread.h"
"/usr/include/event2/event-config.h"
"/usr/include/event2/dns_compat.h"
"/usr/include/event2/bufferevent_ssl.h"
"/usr/include/event2/buffer.h"
"/usr/include/event2/buffer_compat.h"
"/usr/include/event2/util.h"
"/usr/include/event2/dns_struct.h"
"/usr/include/event2/event_compat.h"
"/usr/include/event2/http_compat.h"
"/usr/include/event2/rpc_compat.h"
"/usr/include/evrpc.h"
%dir "/usr/lib/"
"/usr/lib/libevent_pthreads.la"
%dir "/usr/lib/libevent_openssl.so"
%dir "/usr/lib/libevent_extra-2.0.so.5"
%dir "/usr/lib/libevent-2.0.so.5"
%dir "/usr/lib/libevent_extra.so"
%dir "/usr/lib/libevent_core.so"
%dir "/usr/lib/libevent_pthreads.so"
"/usr/lib/libevent_core.la"
"/usr/lib/libevent_core-2.0.so.5.1.1"
"/usr/lib/libevent.a"
%dir "/usr/lib/libevent.so"
"/usr/lib/libevent_pthreads.a"
%dir "/usr/lib/libevent_core-2.0.so.5"
"/usr/lib/libevent_extra.la"
%dir "/usr/lib/libevent_openssl-2.0.so.5"
"/usr/lib/libevent_extra-2.0.so.5.1.1"
%dir "/usr/lib/libevent_pthreads-2.0.so.5"
"/usr/lib/libevent_openssl-2.0.so.5.1.1"
"/usr/lib/libevent.la"
"/usr/lib/libevent_openssl.la"
"/usr/lib/libevent_openssl.a"
"/usr/lib/libevent_pthreads-2.0.so.5.1.1"
"/usr/lib/libevent_core.a"
"/usr/lib/libevent-2.0.so.5.1.1"
%dir "/usr/lib/pkgconfig/"
"/usr/lib/pkgconfig/libevent.pc"
"/usr/lib/pkgconfig/libevent_pthreads.pc"
"/usr/lib/pkgconfig/libevent_openssl.pc"
"/usr/lib/libevent_extra.a"
%dir "/usr/bin/"
"/usr/bin/event_rpcgen.py"
"/usr/bin/event_rpcgen.pyc"
"/usr/bin/event_rpcgen.pyo"
