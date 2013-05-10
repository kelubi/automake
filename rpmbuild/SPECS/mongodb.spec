%define ver 1.8.2
###%define type i686
%define type x86_64

Name:           mongodb
Version:        %{ver}
Release:        shopex
Summary:        mongodb

Group:          Development/Languages
License:        ERPL
URL:            http://www.mongodb.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source:         http://fastdl.mongodb.org/linux/mongodb-linux-%{type}-%{ver}.tgz

%description 
mongodb

%prep
%setup -q -n mongodb-linux-%{type}-%{ver}

%build
rm bin/mongosniff

%install
rm -rf $RPM_BUILD_ROOT/usr
mkdir -p $RPM_BUILD_ROOT/usr
cp -rf bin $RPM_BUILD_ROOT/usr/bin

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/*

%changelog
* Mon Jul 11 2011 wanglei <flaboy@shopex.cn> - R14B03
- new release R14B03
