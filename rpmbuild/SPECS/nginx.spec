%define nginx_user                www
%define nginx_group             %{nginx_user}
%define nginx_home              /usr/local/nginx
%define nginx_home_tmp      /var/spool/nginx/tmp
%define nginx_logdir              /var/log/nginx
%define nginx_confdir           %{nginx_home}/conf
%define nginx_webroot          /data/httpd   

Name:                 nginx
Version:              1.0.8
Release:              shopex
Summary:            Robust, small and high performance http and reverse proxy server
Group:                 System Environment/Daemons  
License:                BSD
URL:                      http://nginx.net/ 
BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
BuildRequires:      pcre-devel,zlib-devel,openssl-devel,perl(ExtUtils::Embed)
Requires:               pcre,zlib,openssl
Requires:               perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires(pre):       shadow-utils
Requires(post):      chkconfig
Requires(preun):    chkconfig, initscripts
Requires(postun):   initscripts

Source0:      http://nginx.org/download/nginx-%{version}.tar.gz 
Source1:      %{name}.init
Source2:      %{name}.logrotate
Source100:  %{name}.index.html
Source102:  %{name}.nginx-logo.png
Source103:  %{name}.50x.html
Source104:  %{name}.404.html
Source106:  %{name}.bots.conf
Source107:  %{name}.status.conf
Source108:  %{name}.php_fcgi.conf
Source109:  %{name}.conf
Source110:  %{name}.pathinfo.conf
Source111:  %{name}.server_flag.conf
Source112:  %{name}.default.conf


# configuration patch to match all the Fedora paths for logs, pid files
# etc.

%description
Nginx [engine x] is an HTTP(S) server, HTTP(S) reverse proxy and IMAP/POP3
proxy server written by Igor Sysoev.

One third party module, nginx-upstream-fair has been added.

%prep
%setup -q

%build
export DESTDIR=%{buildroot}
./configure \
--user=%{nginx_user} \
--group=%{nginx_group} \
--prefix=%{nginx_home} \
--conf-path=%{nginx_confdir}/%{name}.conf \
--error-log-path=%{nginx_logdir}/error.log \
--http-log-path=%{nginx_logdir}/access.log \
--http-client-body-temp-path=%{nginx_home_tmp}/client_body \
--http-proxy-temp-path=%{nginx_home_tmp}/proxy \
--http-fastcgi-temp-path=%{nginx_home_tmp}/fastcgi \
--pid-path=%{_localstatedir}/run/%{name}.pid \
--lock-path=%{_localstatedir}/lock/subsys/%{name} \
--with-http_ssl_module \
--with-http_gzip_static_module \
--with-http_stub_status_module 
   
make %{?_smp_mflags} 

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALLDIRS=vendor
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -type f -name perllocal.pod -exec rm -f {} \;
find %{buildroot} -type f -empty -exec rm -f {} \;
find %{buildroot} -type f -exec chmod 0644 {} \;
find %{buildroot} -type f -name '*.so' -exec chmod 0755 {} \;
chmod 0755 %{buildroot}%{nginx_home}/sbin/nginx

%{__install} -p -D -m 0755 %{SOURCE1}  %{buildroot}%{_initrddir}/%{name}
%{__install} -p -D -m 0644 %{SOURCE2}   %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%{__install} -p -d -m 0755 %{buildroot}%{nginx_home}
%{__install} -p -d -m 0755 %{buildroot}%{nginx_home_tmp}
%{__install} -p -d -m 0755 %{buildroot}%{nginx_logdir}
%{__install} -p -d -m 0755 %{buildroot}%{nginx_webroot}
%{__install} -p -d -m 0755 %{buildroot}%{nginx_confdir}

%{__install} -p -m 0644 %{SOURCE100}  %{buildroot}%{nginx_webroot}/index.html
%{__install} -p -m 0644 %{SOURCE102}  %{buildroot}%{nginx_webroot}/nginx-logo.png 
%{__install} -p -m 0644 %{SOURCE103}  %{buildroot}%{nginx_webroot}/50x.html
%{__install} -p -m 0644 %{SOURCE104}  %{buildroot}%{nginx_webroot}/404.html

%{__install} -p -m 0644 %{SOURCE106}    %{buildroot}%{nginx_confdir}/bots.conf
%{__install} -p -m 0644 %{SOURCE108}    %{buildroot}%{nginx_confdir}/php_fcgi.conf
%{__install} -p -m 0644 %{SOURCE109}    %{buildroot}%{nginx_confdir}/%{name}.conf
%{__install} -p -m 0644 %{SOURCE110}    %{buildroot}%{nginx_confdir}/pathinfo.conf
%{__install} -p -m 0644 %{SOURCE111}    %{buildroot}%{nginx_confdir}/server_flag.conf

%{__install} -p -d -m 0755 %{buildroot}%{nginx_confdir}/vhosts

%{__install} -p -m 0644 %{SOURCE112}    %{buildroot}%{nginx_confdir}/vhosts/default.conf
%{__install} -p -m 0644 %{SOURCE107}    %{buildroot}%{nginx_confdir}/vhosts/status.conf


# convert to UTF-8 all files that give warnings.
for textfile in CHANGES
do
    mv $textfile $textfile.old
    iconv --from-code ISO8859-1 --to-code UTF-8 --output $textfile $textfile.old
    rm -f $textfile.old
done

%clean
rm -rf %{buildroot}

%pre
%{_sbindir}/useradd -c "web service  user" -s /bin/false -r -d %{nginx_home} %{nginx_user} 2>/dev/null || :

%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%{nginx_home}
%{nginx_home_tmp}
%{nginx_webroot}
%dir %{nginx_logdir}
%{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}


%attr(-,%{nginx_user},%{nginx_group}) %dir %{nginx_home}
%attr(-,%{nginx_user},%{nginx_group}) %dir %{nginx_home_tmp}
%attr(-,%{nginx_user},%{nginx_group}) %dir %{nginx_logdir}


%changelog

