%define ver 2.0.2
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
Source0:        http://fastdl.mongodb.org/linux/mongodb-linux-%{type}-%{ver}.tgz
Source1:        init.d-mongod
Source2:        mongod.conf
Source3:        mongod.sysconfig

%description 
mongodb

%prep
%setup -q -n mongodb-linux-%{type}-%{ver}

%build

%install
mkdir -p $RPM_BUILD_ROOT/usr/local/mongodb
mv * $RPM_BUILD_ROOT/usr/local/mongodb
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
cp %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/mongod
chmod a+x $RPM_BUILD_ROOT/etc/rc.d/init.d/mongod
mkdir -p $RPM_BUILD_ROOT/usr/local/mongodb/etc
cp %{SOURCE2} $RPM_BUILD_ROOT/usr/local/mongodb/etc/mongod.conf
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
cp %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/mongod
mkdir -p $RPM_BUILD_ROOT/data/mongo
mkdir -p $RPM_BUILD_ROOT/var/log/mongo
touch $RPM_BUILD_ROOT/var/log/mongo/mongod.log

%clean
rm -rf $RPM_BUILD_ROOT

%pre 
if ! /usr/bin/id -g mongod &>/dev/null; then
    /usr/sbin/groupadd -r mongod
fi
if ! /usr/bin/id mongod &>/dev/null; then
    /usr/sbin/useradd -M -r -g mongod -d /data/mongo -s /bin/false \
	-c mongod mongod > /dev/null 2>&1
fi

%post 
if test $1 = 1
then
  /sbin/chkconfig --add mongod
fi

%preun 
if test $1 = 0
then
  /sbin/chkconfig --del mongod
fi

%postun 
if test $1 -ge 1
then
  /sbin/service mongod condrestart >/dev/null 2>&1 || :
fi


%files
%defattr(-,root,root)
/usr/local/mongodb/*
/etc/rc.d/init.d/mongod
%config(noreplace) /etc/sysconfig/mongod
#/etc/rc.d/init.d/mongos
%attr(0755,mongod,mongod) %dir /data/mongo
%attr(0755,mongod,mongod) %dir /var/log/mongo
%attr(0640,mongod,mongod) %config(noreplace) %verify(not md5 size mtime) /var/log/mongo/mongod.log

%changelog
* Wed Feb 23 2012 summerspring <summer.xia.613@gmail.com>
- update release 2.0.2

* Mon Jul 11 2011 wanglei <flaboy@shopex.cn> - R14B03
- new release R14B03

