%define pkg_ver 1.2.2
%define php_ver 5.3.3

Name:           php-mongo
Version:        %{php_ver}
Release:        shopex
Summary:        php-mongo

Group:          Development/Languages
License:        ERPL
URL:            http://www.mongodb.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source:         http://pecl.php.net/get/mongo-%{pkg_ver}.tgz

BuildRequires:	php-devel = %{php_ver}

%description 
php-mongo

%prep
%setup -q -n mongo-%{pkg_ver}

%build
phpize
./configure
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/php.d
INSTALL_ROOT=$RPM_BUILD_ROOT make install
echo 'extension=mongo.so' > $RPM_BUILD_ROOT/etc/php.d/mongo.ini

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/etc/php.d/mongo.ini
%{_libdir}/php/modules/mongo.so

%changelog
* Mon Jul 11 2011 wanglei <flaboy@shopex.cn> - R14B03
- new release R14B03
