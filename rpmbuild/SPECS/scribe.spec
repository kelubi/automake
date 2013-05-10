#%define ver 2.2
#wget https:/ /download.github.com/facebook-scribe-2ee14d3.tar.gz
%define ver 20110812

Name:           scribe 
Version:        %{ver}
Release:        shopex
Summary:        facebook thrift
Group:          Development/Languages
License:        ERPL
URL:            http://www.mozilla.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source:         http://cloud.github.com/downloads/facebook/scribe/scribe.tar.gz

BuildRequires:	thrift thrift-fb303 boost141-devel libevent


%description 
facebook scribe

%package python
Summary:        scribe-python
Group:          Development/Languages
%description python
facebook scribe python

%prep
%setup -q -n scribe

%build
rm -rf $RPM_BUILD_ROOT
autoreconf --force --verbose --install
CPPFLAGS=-I%{_includedir}/boost141 \
LDFLAGS=-L%{_libdir}/boost141 \
 ./configure \
 --with-thriftpath=/usr \
 --with-fb303path=/usr \
 --prefix=%{_prefix} || zsh
make

%install
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/lib/*
%exclude /usr/lib/python*
%{_bindir}/*

%files python
/usr/lib/python*
