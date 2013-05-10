%define ver 1.7.0

Name:           js-devel
Version:        %{ver}
Release:        shopex
Summary:        mozilla spider monkey js

Group:          Development/Languages
License:        ERPL
URL:            http://www.mozilla.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source:         ftp://ftp.mozilla.org/pub/mozilla.org/js/js-%{ver}.tar.gz

BuildRequires:	m4

%description 
mozilla spider monkey js

%prep
%setup -q -n js

%build
cd src
export CFLAGS="-DJS_C_STRINGS_ARE_UTF8"
make -f Makefile.ref


%install
cd src
JS_DIST=$RPM_BUILD_ROOT/usr make -f Makefile.ref export

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*
%{_bindir}/*

%changelog
* Mon Jul 11 2011 wanglei <flaboy@shopex.cn> - R14B03
- new release R14B03

%changelog
* Mon Jul 11 2011 wanglei <flaboy@shopex.cn> - R14B03
- new release R14B03
