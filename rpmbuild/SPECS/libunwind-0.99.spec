%define	prefix	/usr

Name: libunwind
Summary: define a portable and efficient C programming interface (API) to determine the call-chain of a program
Version: 0.99
Release: shopex
Group: ShopEx/Libraries
URL: http://www.nongnu.org/libunwind/
License: BSD
Vendor: Google
Packager: Google <google-perftools@googlegroups.com>
Source: libunwind-%{version}.tar.gz
Distribution: Redhat 7 and above.
Buildroot: %{_tmppath}/%{name}-root
Prefix: %prefix

%description
The API additionally provides the means to manipulate the preserved (callee-saved) state of each call-frame and to resume execution at any point in the call-chain (non-local goto). The API supports both local (same-process) and remote (across-process) operation. As such, the API is useful in a number of applications. 

%changelog
	* Sun Nov  27 2011  <ken@shopex.cn>
	- for shopex only

%prep
%setup

%build

./configure --prefix=%{_prefix} --exec-prefix=%{_exec_prefix} --bindir=%{_bindir} --sbindir=%{_sbindir} --sysconfdir=%{_sysconfdir} --datadir=%{_datadir} --includedir=%{_includedir} --libdir=%{_libdir} --libexecdir=%{_libexecdir} --localstatedir=%{_localstatedir} --sharedstatedir=%{_sharedstatedir} --mandir=%{_mandir} --infodir=%{_infodir}
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

/usr/include/libunwind*
/usr/include/unwind.h
/usr/lib64/libunwind*
/usr/share/man/man3/_U_dyn_*.gz
/usr/share/man/man3/libunwind*.gz
/usr/share/man/man3/unw_*.gz


