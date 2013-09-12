%define	prefix	/usr

Name: google-perftools
Summary: Performance tools for C++
Version: 1.8.3
Release: shopex
Group: ShopEx/Libraries
URL: http://code.google.com/p/google-perftools/
License: BSD
Vendor: Google
Packager: Google <google-perftools@googlegroups.com>
Source: google-perftools-%{version}.tar.gz
Distribution: Redhat 7 and above.
Buildroot: %{_tmppath}/%{name}-root
Prefix: %prefix

%description
The %name packages contains some utilities to improve and analyze the
performance of C++ programs.  This includes an optimized thread-caching
malloc() and cpu and heap profiling utilities.

%changelog
	* Sun Nov  27 2011  <ken@shopex.cn>
	- for shopex only
	
	* Mon Apr 20 2009  <opensource@google.com>
	- Change build rule to use a configure line more like '%configure'
	- Change install to use DESTDIR instead of prefix for configure
	- Use wildcards for doc/ and lib/ directories

	* Fri Mar 11 2005  <opensource@google.com>
	- First draft

%prep
%setup

%build
# I can't use '% configure', because it defines -m32 which breaks some
# of the low-level atomicops files in this package.  But I do take
# as much from % configure (in /usr/lib/rpm/macros) as I can.
./configure --prefix=%{_prefix} --exec-prefix=%{_exec_prefix} --bindir=%{_bindir} --sbindir=%{_sbindir} --sysconfdir=%{_sysconfdir} --datadir=%{_datadir} --includedir=%{_includedir} --libdir=%{_libdir} --libexecdir=%{_libexecdir} --localstatedir=%{_localstatedir} --sharedstatedir=%{_sharedstatedir} --mandir=%{_mandir} --infodir=%{_infodir}
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%docdir %{prefix}/share/doc/%{name}-%{version}
%{prefix}/share/doc/%{name}-%{version}/*

%{_libdir}/*.so.*
%{_bindir}/pprof
%{_mandir}/man1/pprof.1*

%{_includedir}/google
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
