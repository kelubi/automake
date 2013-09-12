Summary:   Package created with checkinstall 1.6.2
Name:      htop
Version:   1.0
Release:   shopex
License: GPL
Packager:  checkinstall-1.6.2
Group:     Applications/System          
BuildRoot: /var/tmp/tmp.mjFMF11850/package
Provides:  htop
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
%dir "/usr/bin/"
"/usr/bin/htop"
%dir "/usr/share/"
%dir "/usr/share/pixmaps/"
"/usr/share/pixmaps/htop.png"
%dir "/usr/share/man/"
%dir "/usr/share/man/man1/"
"/usr/share/man/man1/htop.1.gz"
%dir "/usr/share/applications/"
"/usr/share/applications/htop.desktop"

%changelog
* Sun Nov 20 2011 Ken Xu <ken@shopex.cn>
- just for shopex
