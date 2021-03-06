%define ver R14B03

Name:           erlang
Version:        %{ver}
Release:        shopex
Summary:        General-purpose programming language and runtime environment

Group:          Development/Languages
License:        ERPL
URL:            http://www.erlang.org
Source:         http://www.erlang.org/download/otp_src_%{ver}.tar.gz
Source1:	http://www.erlang.org/download/otp_doc_html_%{ver}.tar.gz
Source2:	http://www.erlang.org/download/otp_doc_man_%{ver}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  unixODBC-devel
BuildRequires:	tcl-devel
BuildRequires:	tk-devel
BuildRequires:  gd-devel
BuildRequires:  flex
BuildRequires:	m4
Requires:	tk

%description 
Erlang is a general-purpose programming language and runtime
environment. Erlang has built-in support for concurrency, distribution
and fault tolerance. Erlang is used in several large telecommunication
systems from Ericsson.


%package doc
Summary:	Erlang documentation
Group:		Development/Languages

%description doc
Documentation for Erlang.


%prep
%setup -q -n otp_src_%{ver}

%build
CFLAGS="-fno-strict-aliasing" \
 ./configure --enable-hipe \
	 --enable-kernel-poll \
	 --enable-smp-support \
	 --enable-dynamic-ssl-lib \
	 --prefix=%{_prefix} \
	 --exec-prefix=%{_prefix} \
	 --bindir=%{_bindir} \
	 --libdir=%{_libdir}
chmod -R u+w .
make


%install
rm -rf $RPM_BUILD_ROOT
make INSTALL_PREFIX=$RPM_BUILD_ROOT install

# clean up
find $RPM_BUILD_ROOT%{_libdir}/erlang -perm 0775 | xargs chmod 755
find $RPM_BUILD_ROOT%{_libdir}/erlang -name Makefile | xargs chmod 644
find $RPM_BUILD_ROOT%{_libdir}/erlang -name \*.o | xargs chmod 644
find $RPM_BUILD_ROOT%{_libdir}/erlang -name \*.bat | xargs rm -f
find $RPM_BUILD_ROOT%{_libdir}/erlang -name index.txt.old | xargs rm -f

# doc
mkdir -p erlang_doc
tar -C erlang_doc -zxf %{SOURCE1}
tar -C $RPM_BUILD_ROOT/%{_libdir}/erlang -zxf %{SOURCE2}

# make links to binaries
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
cd $RPM_BUILD_ROOT/%{_bindir}
for file in erl erlc 
do
  ln -sf ../%{_lib}/erlang/bin/$file .
done
ln -sf ../%{_lib}/erlang/lib/erl_interface-3.7.4/bin/erl_call .

# remove buildroot from installed files
cd $RPM_BUILD_ROOT/%{_libdir}/erlang
sed -i "s|$RPM_BUILD_ROOT||" erts*/bin/{erl,start} releases/RELEASES bin/{erl,start}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc AUTHORS EPLICENCE
%{_bindir}/*
%{_libdir}/erlang


%files doc
%defattr(-,root,root)
%doc erlang_doc/*


%post
%{_libdir}/erlang/Install -minimal %{_libdir}/erlang >/dev/null 2>/dev/null


%changelog
* Mon Jul 11 2011 wanglei <flaboy@shopex.cn> - R14B03
- new release R14B03

* Mon Aug 11 2008 Peter Lemenkov <lemenkov@gmail.com> - R12B-3.3
- Force dynamic linking of crypto libs

* Thu Jul 17 2008 Tom "spot" Callaway <tcallawa@redhat.com> - R12B-3.2
- fix license tag

* Sun Jul  6 2008 Gerard Milmeister <gemi@bluewin.ch> - R12B-3.1
- new release R12B-3

* Thu Mar 27 2008 Gerard Milmeister <gemi@bluewin.ch> - R12B-1.1
- new release R12B-1

* Sat Feb 23 2008 Gerard Milmeister <gemi@bluewin.ch> - R12B-0.3
- disable strict aliasing optimization

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - R12B-0.2
- Autorebuild for GCC 4.3

* Sat Dec  8 2007 Gerard Milmeister <gemi@bluewin.ch> - R12B-0.1
- new release R12B-0

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - R11B-6
 - Rebuild for deps

* Sun Aug 19 2007 Gerard Milmeister <gemi@bluewin.ch> - R11B-5.3
- fix some permissions

* Sat Aug 18 2007 Gerard Milmeister <gemi@bluewin.ch> - R11B-5.2
- enable dynamic linking for ssl

* Sat Aug 18 2007 Gerard Milmeister <gemi@bluewin.ch> - R11B-5.1
- new release R11B-5

* Sat Mar 24 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - R11B-2.4
- Require java-1.5.0-gcj-devel for build.

* Sun Dec 31 2006 Gerard Milmeister <gemi@bluewin.ch> - R11B-2.3
- remove buildroot from installed files

* Sat Dec 30 2006 Gerard Milmeister <gemi@bluewin.ch> - R11B-2.2
- added patch for compiling with glibc 2.5

* Sat Dec 30 2006 Gerard Milmeister <gemi@bluewin.ch> - R11B-2.1
- new version R11B-2

* Mon Aug 28 2006 Gerard Milmeister <gemi@bluewin.ch> - R11B-0.3
- Rebuild for FE6

* Wed Jul  5 2006 Gerard Milmeister <gemi@bluewin.ch> - R11B-0.2
- add BR m4

* Thu May 18 2006 Gerard Milmeister <gemi@bluewin.ch> - R11B-0.1
- new version R11B-0

* Wed May  3 2006 Gerard Milmeister <gemi@bluewin.ch> - R10B-10.3
- added patch for run_erl by Knut-Håvard Aksnes

* Mon Mar 13 2006 Gerard Milmeister <gemi@bluewin.ch> - R10B-10.1
- new version R10B-10

* Thu Dec 29 2005 Gerard Milmeister <gemi@bluewin.ch> - R10B-9.1
- New Version R10B-9

* Sat Oct 29 2005 Gerard Milmeister <gemi@bluewin.ch> - R10B-8.2
- updated rpath patch

* Sat Oct 29 2005 Gerard Milmeister <gemi@bluewin.ch> - R10B-8.1
- New Version R10B-8

* Sat Oct  1 2005 Gerard Milmeister <gemi@bluewin.ch> - R10B-6.4
- Added tk-devel and tcl-devel to buildreq
- Added tk to req

* Tue Sep  6 2005 Gerard Milmeister <gemi@bluewin.ch> - R10B-6.3
- Remove perl BuildRequires

* Tue Aug 30 2005 Gerard Milmeister <gemi@bluewin.ch> - R10B-6.2
- change /usr/lib to %%{_libdir}
- redirect output in %%post to /dev/null
- add unixODBC-devel to BuildRequires
- split doc off to erlang-doc package

* Sat Jun 25 2005 Gerard Milmeister <gemi@bluewin.ch> - R10B-6.1
- New Version R10B-6

* Sun Feb 13 2005 Gerard Milmeister <gemi@bluewin.ch> - R10B-3.1
- New Version R10B-3

* Mon Dec 27 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:R10B-2-0.fdr.1
- New Version R10B-2

* Wed Oct  6 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:R10B-0.fdr.1
- New Version R10B

* Thu Oct 16 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:R9B-1.fdr.1
- First Fedora release
