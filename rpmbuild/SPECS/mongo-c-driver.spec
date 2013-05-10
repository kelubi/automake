%define mongo_c_driver_ver 1.0
%define scons_ver 1.2.0

Name:           mongo-c-driver
Version:        %{mongo_c_driver_ver}
Release:        Mongodb
Summary:        mongo-c-driver

Group:          Development/Languages
License:        ERPL
URL:            http://www.mongodb.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source:         mongo-c-driver-%{mongo_c_driver_ver}.tar.gz

BuildRequires:  scons >= %{scons_ver}

%description 
mongo-c-driver

%prep
%setup -q -n mongo-c-driver-%{mongo_c_driver_ver}

%build
scons
#install -C libbson.* /usr/lib
#install -C libmongoc.* /usr/lib

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}
install -C libbson.* $RPM_BUILD_ROOT%{_libdir}
install -C libmongoc.* $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libdir}/*

%post
ldconfig

%changelog
* Thu Sep 01 2011 edwin <lvzhihao@shopex.cn> - 1.0
- new release 1.0
