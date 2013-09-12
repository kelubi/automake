Summary     : A console application which for benchmarking hard drives and filesystems
Name           : fio
Version        : 1.57
Release        : shopex
License:        :BSD
Url                : http://freecode.com/projects/fio
Packager       : Ken Xu <ken@shopex.cn>
Group          :Utilities/Benchmarking
Source         : %{name}-%{version}.tar.gz
BuildRoot      : %{_tmppath}/%{name}-%{version}-root
Requires       : ncurses >= 5.0
BuildRequires  : ncurses-devel >= 5.0


%description
%{name}  is an I/O tool meant to be used both for benchmark and stress/hardware verification. It has support for 13 different types of I/O engines (sync, mmap, libaio, posixaio, SG v3, splice, null, network, syslet, guasi, solarisaio, and more), I/O priorities (for newer Linux kernels), rate I/O, forked or threaded jobs, and much more. It can work on block devices as well as files. fio accepts job descriptions in a simple-to-understand text format. Several example job files are included. fio displays all sorts of I/O performance information. Fio is in wide use in many places, for both benchmarking, QA, and verification purposes. It supports Linux, FreeBSD, NetBSD, OS X, OpenSolaris, AIX, HP-UX, and Windows.


%prep
%setup -q


%build
CFLAGS=${RPM_OPT_FLAGS} CXXFLAGS=${RPM_OPT_FLAGS} 
make


%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README
%attr(0755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz


%changelog
* Sun Nov 20 2011 Ken Xu <ken@shopex.cn>
- just for shopex
* Wed Aug 14 2002 Helder Correia <helder.correia@netcabo.pt>
- Initial RPM release.
