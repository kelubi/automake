%define pid_dir %{_localstatedir}/run/redis
%define pid_file %{pid_dir}/redis.pid

Summary: redis
Name: redis
Version: 2.4.7
Release: shopex
License: BSD
Group: Applications/Multimedia
URL: http://lnmpp.googlecode.com/files/redis-2.4.7.tar.gz

Source0: redis-%{version}.tar.gz
Source1: redis.conf
Source2: redis.init

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gcc, make
Requires(post): /sbin/chkconfig /usr/sbin/useradd
Requires(preun): /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service
Provides: redis

Packager: William Gregorian &lt;dev-null@will-bloggs-too.com&gt;

%description
Redis is a key-value database. It is similar to memcached but the dataset is
not volatile, and values can be strings, exactly like in memcached, but also
lists and sets with atomic operations to push/pop elements.

In order to be very fast but at the same time persistent the whole dataset is
taken in memory and from time to time and/or when a number of changes to the
dataset are performed it is written asynchronously on disk. You may lose the
last few queries that is acceptable in many applications but it is as fast
as an in memory DB (beta 6 of Redis includes initial support for master-slave
replication in order to solve this problem by redundancy).

Compression and other interesting features are a work in progress. Redis is
written in ANSI C and works in most POSIX systems like Linux, *BSD, Mac OS X,
and so on. Redis is free software released under the very liberal BSD license.

%prep
%setup

#%{__cat} &lt;&lt;EOF &gt;redis.logrotate
%{__cat} > redis.logrotate <<EOF 
%{_localstatedir}/log/redis/*log {
    missingok
}
EOF

%build
%{__make}

%install
%{__rm} -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
%{__install} -Dp -m 0755 src/redis-server %{buildroot}%{_sbindir}/redis-server
%{__install} -Dp -m 0755 src/redis-benchmark %{buildroot}%{_bindir}/redis-benchmark
%{__install} -Dp -m 0755 src/redis-cli %{buildroot}%{_bindir}/redis-cli

%{__install} -Dp -m 0755 redis.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/redis
%{__install} -Dp -m 0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/init.d/redis
%{__install} -Dp -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/redis.conf
%{__install} -p -d -m 0755 %{buildroot}%{_localstatedir}/lib/redis
%{__install} -p -d -m 0755 %{buildroot}%{_localstatedir}/log/redis
%{__install} -p -d -m 0755 %{buildroot}%{_localstatedir}/redis
%{__install} -p -d -m 0755 %{buildroot}%{pid_dir}

%pre
/usr/sbin/useradd -c 'User for Redis key-value store' -s /bin/false -r -d %{_localstatedir}/lib/redis redis &> /dev/null

%preun
if [ $1 = 0 ]; then
    # make sure redis service is not running before uninstalling

    # when the preun section is run, we've got stdin attached.  If we
    # call stop() in the redis init script, it will pass stdin along to
    # the redis-cli script; this will cause redis-cli to read an extraneous
    # argument, and the redis-cli shutdown will fail due to the wrong number
    # of arguments.  So we do this little bit of magic to reconnect stdin
    # to the terminal
    term="/dev/$(ps -p$$ --no-heading | awk '{print $2}')"
    exec &lt; $term

    /sbin/service redis stop &gt; /dev/null 2&gt;&amp;1 || :
    /sbin/chkconfig --del redis
fi

%post
/sbin/chkconfig --add redis

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%{_sbindir}/redis-server
%{_bindir}/redis-benchmark
%{_bindir}/redis-cli
%{_sysconfdir}/init.d/redis
%config(noreplace) %{_sysconfdir}/redis.conf
%{_sysconfdir}/logrotate.d/redis
%dir %attr(0770,redis,redis) %{_localstatedir}/lib/redis
%dir %attr(0755,redis,redis) %{_localstatedir}/log/redis
%dir %attr(0755,redis,redis) %{_localstatedir}/run/redis
%dir %attr(0755,redis,redis) %{_localstatedir}/redis

%changelog
* Thu Sep 07 2011 - William Gregorian
- pid file path modified to /var/run/redis/
- modified redis.conf vm-max-memory to 1
- modified redis.conf commented out sharedobjects
- modified redis.conf pointed the logs to /var/log/redis/redis.log
