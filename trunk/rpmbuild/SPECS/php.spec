%global contentdir  /var/www
# API/ABI check
%global apiver      20090626
%global zendver     20090626
%global pdover      20080721
# Extension version
%global fileinfover 1.0.5-dev
%global pharver     2.0.1
%global zipver      1.9.1
%global jsonver     1.2.1

%ifarch ppc ppc64
%define oraclever 10.2.0.2
%else
%define oraclever 11.1.0.7
%endif

# Regression tests take a long time, you can skip 'em with this
%{!?runselftest: %{expand: %%global runselftest 1}}

%global phpversion 5.3.3

# Optional components; pass "--with mssql" etc to rpmbuild.
%define with_oci8 	%{?_with_oci8:1}%{!?_with_oci8:0}
%define with_ibase 	%{?_with_ibase:1}%{!?_with_ibase:0}
%define with_enchant 0
%define with_fpm 1

%define tidyver 	0.99.0-12.20070228

Summary: PHP scripting language for creating dynamic web sites
Name: php
Version: 5.3.3
Release: shopex
License: PHP
Group: Development/Languages
URL: http://www.php.net/

%if 0%{?snapdate:1}
Source0: http://www.php.net/distributions/php5.3-%{snapdate}.tar.bz2
%else
Source0: http://downloads.php.net/ilia/php-%{phpversion}.tar.bz2
%endif
Source1: php.conf
Source2: php-53-remi.ini
Source3: macros.php
Source4: php-fpm.conf
Source5: php-fpm-www.conf
Source6: php-fpm.init
Source7: php-fpm.logrotate
Source8: php-nginx.conf

# Build fixes
Patch1: php-5.3.3-gnusrc.patch
Patch2: php-5.3.0-install.patch
Patch3: php-5.2.4-norpath.patch
Patch4: php-5.3.0-phpize64.patch
Patch5: php-5.2.0-includedir.patch
Patch6: php-5.2.4-embed.patch
Patch7: php-5.3.0-recode.patch
Patch8: php-5.3.3-aconf26x.patch

# Fixes for extension modules
Patch20: php-4.3.11-shutdown.patch
Patch21: php-5.3.3-macropen.patch

# Functional changes
Patch40: php-5.0.4-dlopen.patch
Patch41: php-5.3.0-easter.patch
Patch42: php-5.3.1-systzdata-v7.patch

# Fixes for tests
Patch61: php-5.0.4-tests-wddx.patch

# RC Patch
Patch91: php-5.3.2-oci8conf.patch


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: bzip2-devel, curl-devel >= 7.9, db4-devel, gmp-devel
BuildRequires: libstdc++-devel, openssl-devel
BuildRequires: zlib-devel, smtpdaemon
%if 0%{?fedora} >= 8
BuildRequires: pcre-devel >= 7.3
%endif
BuildRequires: bzip2, perl, libtool >= 1.4.3, gcc-c++
Obsoletes: php-dbg, php3, phpfi, stronghold-php
Provides: mod_php = %{version}-%{release}
Requires: php-common = %{version}-%{release}
# For backwards-compatibility, require php-cli for the time being:
Requires: php-cli = %{version}-%{release}
# To ensure correct /var/lib/php/session ownership:

%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated webpages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts. 

The php package contains the module which adds support for the PHP
language to Apache HTTP Server.

%package cli
Group: Development/Languages
Summary: Command-line interface for PHP
Requires: php-common = %{version}-%{release}
Provides: php-cgi = %{version}-%{release}
Provides: php-pcntl, php-readline

%description cli
The php-cli package contains the command-line interface 
executing PHP scripts, /usr/bin/php, and the CGI interface.

%if %{with_fpm}
%package fpm
Group: Development/Languages
Summary: PHP FastCGI Process Manager
Requires: php-common = %{version}-%{release}
BuildRequires: libevent-devel >= 1.4.11

%description fpm
PHP-FPM (FastCGI Process Manager) is an alternative PHP FastCGI
implementation with some additional features useful for sites of
any size, especially busier sites.
%endif

%package common
Group: Development/Languages
Summary: Common files for PHP
Provides: php-api = %{apiver}, php-zend-abi = %{zendver}
Provides: php(api) = %{apiver}, php(zend-abi) = %{zendver}
# Provides for all builtin modules:
Provides: php-bz2, php-calendar, php-ctype, php-curl, php-date, php-exif
Provides: php-ftp, php-gettext, php-gmp, php-hash, php-iconv, php-libxml
Provides: php-reflection, php-shmop, php-simplexml, php-sockets
Provides: php-spl, php-tokenizer, php-openssl, php-pcre
Provides: php-zlib, php-json, php-zip, php-fileinfo
Obsoletes: php-openssl, php-pecl-zip, php-pecl-json, php-json, php-pecl-phar, php-pecl-Fileinfo
# For obsoleted pecl extension
Provides: php-pecl-json = %{jsonver}, php-pecl(json) = %{jsonver}
Provides: php-pecl-zip = %{zipver}, php-pecl(zip) = %{zipver}
Provides: php-pecl-phar = %{pharver}, php-pecl(phar) = %{pharver}
Provides: php-pecl-Fileinfo = %{fileinfover}, php-pecl(Fileinfo) = %{fileinfover}

%description common
The php-common package contains files used by both the php
package and the php-cli package.

%package devel
Group: Development/Libraries
Summary: Files needed for building PHP extensions
Requires: php = %{version}-%{release}, autoconf, automake
Obsoletes: php-pecl-pdo-devel

%description devel
The php-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.

%package imap
Summary: A module for PHP applications that use IMAP
Group: Development/Languages
Requires: php-common = %{version}-%{release}
Obsoletes: mod_php3-imap, stronghold-php-imap
BuildRequires: krb5-devel, openssl-devel, libc-client-devel

%description imap
The php-imap package contains a dynamic shared object (DSO) for the
Apache Web server. When compiled into Apache, the php-imap module will
add IMAP (Internet Message Access Protocol) support to PHP. IMAP is a
protocol for retrieving and uploading e-mail messages on mail
servers. PHP is an HTML-embedded scripting language. If you need IMAP
support for PHP applications, you will need to install this package
and the php package.

%package ldap
Summary: A module for PHP applications that use LDAP
Group: Development/Languages
Requires: php-common = %{version}-%{release}
Obsoletes: mod_php3-ldap, stronghold-php-ldap
BuildRequires: cyrus-sasl-devel, openldap-devel, openssl-devel

%description ldap
The php-ldap package is a dynamic shared object (DSO) for the Apache
Web server that adds Lightweight Directory Access Protocol (LDAP)
support to PHP. LDAP is a set of protocols for accessing directory
services over the Internet. PHP is an HTML-embedded scripting
language. If you need LDAP support for PHP applications, you will
need to install this package in addition to the php package.

%package pdo
Summary: A database access abstraction module for PHP applications
Group: Development/Languages
Requires: php-common = %{version}-%{release}
Obsoletes: php-pecl-pdo
Provides: php-pdo-abi = %{pdover}

%description pdo
The php-pdo package contains a dynamic shared object that will add
a database access abstraction layer to PHP.  This module provides
a common interface for accessing MySQL, PostgreSQL or other 
databases.

%package mysql
Summary: A module for PHP applications that use MySQL databases
Group: Development/Languages
Requires: php-common = %{version}-%{release}, php-pdo
Provides: php_database, php-mysqli, php-pdo_mysql
Obsoletes: mod_php3-mysql, stronghold-php-mysql
BuildRequires: mysql-devel >= 4.1.0

%description mysql
The php-mysql package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php package.

%package pgsql
Summary: A PostgreSQL database module for PHP
Group: Development/Languages
Requires: php-common = %{version}-%{release}, php-pdo
Provides: php_database, php-pdo_pgsql
Obsoletes: mod_php3-pgsql, stronghold-php-pgsql
BuildRequires: krb5-devel, openssl-devel, postgresql-devel

%package hash
Summary: hash module for PHP
Group: Development/Languages
Requires: php-common = %{version}-%{release}

%description hash
php hash

%package tokenizer
Summary: Session module for PHP
Group: Development/Languages
Requires: php-common = %{version}-%{release}

%description tokenizer
php tokenizer


%package session
Summary: Session module for PHP
Group: Development/Languages
Requires: php-common = %{version}-%{release}

%description session
php session

%description pgsql
The php-pgsql package includes a dynamic shared object (DSO) that can
be compiled in to the Apache Web server to add PostgreSQL database
support to PHP. PostgreSQL is an object-relational database management
system that supports almost all SQL constructs. PHP is an
HTML-embedded scripting language. If you need back-end support for
PostgreSQL, you should install this package in addition to the main
php package.

%package process
Summary: Modules for PHP script using system process interfaces
Group: Development/Languages
Requires: php-common = %{version}-%{release}
Provides: php-posix, php-sysvsem, php-sysvshm, php-sysvmsg

%description process
The php-process package contains dynamic shared objects which add
support to PHP using system interfaces for inter-process
communication.

%package odbc
Group: Development/Languages
Requires: php-common = %{version}-%{release}, php-pdo
Summary: A module for PHP applications that use ODBC databases
Provides: php_database, php-pdo_odbc
Obsoletes: stronghold-php-odbc
BuildRequires: unixODBC-devel

%description odbc
The php-odbc package contains a dynamic shared object that will add
database support through ODBC to PHP. ODBC is an open specification
which provides a consistent API for developers to use for accessing
data sources (which are often, but not always, databases). PHP is an
HTML-embeddable scripting language. If you need ODBC support for PHP
applications, you will need to install this package and the php
package.

%package soap
Group: Development/Languages
Requires: php-common = %{version}-%{release}
Summary: A module for PHP applications that use the SOAP protocol
BuildRequires: libxml2-devel

%description soap
The php-soap package contains a dynamic shared object that will add
support to PHP for using the SOAP web services protocol.

%if %{with_ibase}
%package interbase
Summary: 	A module for PHP applications that use Interbase/Firebird databases
Group: 		Development/Languages
BuildRequires:  firebird-devel
Requires: 	php-common = %{version}-%{release}, php-pdo
Provides: 	php_database, php-firebird, php-pdo_firebird

%description interbase
The php-interbase package contains a dynamic shared object that will add
database support through Interbase/Firebird to PHP.

InterBase is the name of the closed-source variant of this RDBMS that was
developed by Borland/Inprise. 

Firebird is a commercially independent project of C and C++ programmers, 
technical advisors and supporters developing and enhancing a multi-platform 
relational database management system based on the source code released by 
Inprise Corp (now known as Borland Software Corp) under the InterBase Public
License.
%endif

%if %{with_oci8}
%package oci8
Summary: 	A module for PHP applications that use OCI8 databases
Group: 		Development/Languages
BuildRequires: 	oracle-instantclient-devel = %{oraclever}
Requires: 	php-common = %{version}-%{release}, php-pdo
Provides: 	php_database, php-pdo_oci
# Should requires libclntsh.so.11.1, but it's not provided by Oracle RPM.
AutoReq: 	0

%description oci8
The php-oci8 package contains a dynamic shared object that will add
support for accessing OCI8 databases to PHP.
%endif

%package snmp
Summary: A module for PHP applications that query SNMP-managed devices
Group: Development/Languages
Requires: php-common = %{version}-%{release}, net-snmp
BuildRequires: net-snmp-devel

%description snmp
The php-snmp package contains a dynamic shared object that will add
support for querying SNMP devices to PHP.  PHP is an HTML-embeddable
scripting language. If you need SNMP support for PHP applications, you
will need to install this package and the php package.

%package xml
Summary: A module for PHP applications which use XML
Group: Development/Languages
Requires: php-common = %{version}-%{release}
Obsoletes: php-domxml, php-dom
Provides: php-dom, php-xsl, php-domxml, php-wddx
BuildRequires: libxslt-devel >= 1.0.18-1, libxml2-devel >= 2.4.14-1

%description xml
The php-xml package contains dynamic shared objects which add support
to PHP for manipulating XML documents using the DOM tree,
and performing XSL transformations on XML documents.

%package xmlrpc
Summary: A module for PHP applications which use the XML-RPC protocol
Group: Development/Languages
Requires: php-common = %{version}-%{release}

%description xmlrpc
The php-xmlrpc package contains a dynamic shared object that will add
support for the XML-RPC protocol to PHP.

%package mbstring
Summary: A module for PHP applications which need multi-byte string handling
Group: Development/Languages
Requires: php-common = %{version}-%{release}

%description mbstring
The php-mbstring package contains a dynamic shared object that will add
support for multi-byte string handling to PHP.

%package gd
Summary: A module for PHP applications for using the gd graphics library
Group: Development/Languages
Requires: php-common = %{version}-%{release}
# Required to build the bundled GD library
BuildRequires: libjpeg-devel, libpng-devel, freetype-devel
BuildRequires: libXpm-devel

%description gd
The php-gd package contains a dynamic shared object that will add
support for using the gd graphics library to PHP.

%package bcmath
Summary: A module for PHP applications for using the bcmath library
Group: Development/Languages
Requires: php-common = %{version}-%{release}

%description bcmath
The php-bcmath package contains a dynamic shared object that will add
support for using the bcmath library to PHP.

%package dba
Summary: A database abstraction layer module for PHP applications
Group: Development/Languages
Requires: php-common = %{version}-%{release}

%description dba
The php-dba package contains a dynamic shared object that will add
support for using the DBA database abstraction layer to PHP.

%package mcrypt
Summary: Standard PHP module provides mcrypt library support
Group: Development/Languages
Requires: php-common = %{version}-%{release}
BuildRequires: libmcrypt-devel

%description mcrypt
The php-mcrypt package contains a dynamic shared object that will add
support for using the mcrypt library to PHP.

%package tidy
Summary: Standard PHP module provides tidy library support
Group: Development/Languages
Requires: php-common = %{version}-%{release}
BuildRequires: libtidy-devel

%description tidy
The php-tidy package contains a dynamic shared object that will add
support for using the tidy library to PHP.

%package mssql
Summary: MSSQL database module for PHP
Group: Development/Languages
Requires: php-common = %{version}-%{release}, php-pdo
BuildRequires: freetds-devel
Provides: php-pdo_dblib

%description mssql
The php-mssql package contains a dynamic shared object that will
add MSSQL database support to PHP.  It uses the TDS (Tabular
DataStream) protocol through the freetds library, hence any
database server which supports TDS can be accessed.

%package embedded
Summary: PHP library for embedding in applications
Group: System Environment/Libraries
Requires: php-common = %{version}-%{release}
# doing a real -devel package for just the .so symlink is a bit overkill
Provides: php-embedded-devel = %{version}-%{release}

%description embedded
The php-embedded package contains a library which can be embedded
into applications to provide PHP scripting language support.

%package pspell
Summary: A module for PHP applications for using pspell interfaces
Group: System Environment/Libraries
Requires: php-common = %{version}-%{release}
BuildRequires: aspell-devel >= 0.50.0

%description pspell
The php-pspell package contains a dynamic shared object that will add
support for using the pspell library to PHP.

%package recode
Summary: A module for PHP applications for using the recode library
Group: System Environment/Libraries
Requires: php-common = %{version}-%{release}
BuildRequires: recode-devel

%description recode
The php-recode package contains a dynamic shared object that will add
support for using the recode library to PHP.

%package intl
Summary: Internationalization extension for PHP applications
Group: System Environment/Libraries
Requires: php-common = %{version}-%{release}
BuildRequires: libicu-devel >= 3.6

%description intl
The php-intl package contains a dynamic shared object that will add
support for using the ICU library to PHP.

%if %{with_enchant}
%package enchant
Summary: Human Language and Character Encoding Support
Group: System Environment/Libraries
Requires: php-common = %{version}-%{release}
BuildRequires: enchant-devel >= 1.2.4

%description enchant
The php-intl package contains a dynamic shared object that will add
support for using the enchant library to PHP.
%endif


%prep
echo CIBLE = %{name}-%{version}-%{release}
%if 0%{?snapdate:1}
%setup -q -n php5.3-%{snapdate}
%else
%setup -q -n php-%{phpversion}
%endif

%patch1 -p1 -b .gnusrc
%patch2 -p1 -b .install
%patch3 -p1 -b .norpath
%patch4 -p1 -b .phpize64
%patch5 -p1 -b .includedir
%patch6 -p1 -b .embed
%patch7 -p1 -b .recode
%if 0%{?fedora} >= 13
%patch8 -p1 -b .aconf26x
%endif

%patch20 -p1 -b .shutdown
%patch21 -p1 -b .macropen

%patch40 -p1 -b .dlopen
%patch41 -p1 -b .easter
%patch42 -p1 -b .systzdata

#%patch60 -p1 -b .tests-dashn
%patch61 -p1 -b .tests-wddx

%patch91 -p0 -b .remi-oci8


# Awful hack for mysqlnd driver default mysql socket patch
sed -i -e s#/tmp/mysql.sock#%{_localstatedir}/lib/mysql/mysql.sock# ext/pdo_mysql/pdo_mysql.c
sed -i -e s#/tmp/mysql.sock#%{_localstatedir}/lib/mysql/mysql.sock# ext/mysqlnd/mysqlnd.c


# Prevent %%doc confusion over LICENSE files
cp Zend/LICENSE Zend/ZEND_LICENSE
cp TSRM/LICENSE TSRM_LICENSE
cp ext/ereg/regex/COPYRIGHT regex_COPYRIGHT
cp ext/gd/libgd/README gd_README

# Multiple builds for multiple SAPIs
mkdir build-cgi build-embedded \
%if %{with_fpm}
    build-fpm
%endif

# Remove bogus test; position of read position after fopen(, "a+")
# is not defined by C standard, so don't presume anything.
rm -f ext/standard/tests/file/bug21131.phpt
# php_egg_logo_guid() removed by patch41
rm -f tests/basic/php_egg_logo_guid.phpt


# Tests that fail.
rm -f ext/standard/tests/file/bug22414.phpt \
      ext/iconv/tests/bug16069.phpt

# Safety check for API version change.
pver=$(sed -n '/#define PHP_VERSION /{s/.* "//;s/".*$//;p}' main/php_version.h)
if test "x${pver}" != "x%{phpversion}"; then
   : Error: Upstream PHP version is now ${pver}, expecting %{phpversion}.
   : Update the phpversion macro and rebuild.
   exit 1
fi

vapi=`sed -n '/#define PHP_API_VERSION/{s/.* //;p}' main/php.h`
if test "x${vapi}" != "x%{apiver}"; then
   : Error: Upstream API version is now ${vapi}, expecting %{apiver}.
   : Update the apiver macro and rebuild.
   exit 1
fi

vzend=`sed -n '/#define ZEND_MODULE_API_NO/{s/^[^0-9]*//;p;}' Zend/zend_modules.h`
if test "x${vzend}" != "x%{zendver}"; then
   : Error: Upstream Zend ABI version is now ${vzend}, expecting %{zendver}.
   : Update the zendver macro and rebuild.
   exit 1
fi

# Safety check for PDO ABI version change
vpdo=`sed -n '/#define PDO_DRIVER_API/{s/.*[ 	]//;p}' ext/pdo/php_pdo_driver.h`
if test "x${vpdo}" != "x%{pdover}"; then
   : Error: Upstream PDO ABI version is now ${vpdo}, expecting %{pdover}.
   : Update the pdover macro and rebuild.
   exit 1
fi

# Check for some extension version
ver=$(sed -n '/#define PHP_FILEINFO_VERSION /{s/.* "//;s/".*$//;p}' ext/fileinfo/php_fileinfo.h)
if test "$ver" != "%{fileinfover}"; then
   : Error: Upstream FILEINFO version is now ${ver}, expecting %{fileinfover}.
   : Update the fileinfover macro and rebuild.
   exit 1
fi
ver=$(sed -n '/#define PHP_PHAR_VERSION /{s/.* "//;s/".*$//;p}' ext/phar/php_phar.h)
if test "$ver" != "%{pharver}"; then
   : Error: Upstream PHAR version is now ${ver}, expecting %{pharver}.
   : Update the pharver macro and rebuild.
   exit 1
fi
ver=$(sed -n '/#define PHP_ZIP_VERSION_STRING /{s/.* "//;s/".*$//;p}' ext/zip/php_zip.h)
if test "$ver" != "%{zipver}"; then
   : Error: Upstream ZIP version is now ${ver}, expecting %{zipver}.
   : Update the zipver macro and rebuild.
   exit 1
fi
ver=$(sed -n '/#define PHP_JSON_VERSION /{s/.* "//;s/".*$//;p}' ext/json/php_json.h)
if test "$ver" != "%{jsonver}"; then
   : Error: Upstream JSON version is now ${ver}, expecting %{jsonver}.
   : Update the jsonver macro and rebuild.
   exit 1
fi


: Build for oci8=%{with_oci8} ibase=%{with_ibase}

%build
%if 0%{?fedora} >= 11
# aclocal workaround - to be improved
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >>aclocal.m4
%endif

# Force use of system libtool:
libtoolize --force --copy
%if 0%{?fedora} >= 11
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >build/libtool.m4
%else
cat `aclocal --print-ac-dir`/libtool.m4 > build/libtool.m4
%endif

# Regenerate configure scripts (patches change config.m4's)
./buildconf --force
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign"
%if 0%{?rhel} < 5
	CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%endif
export CFLAGS

# Install extension modules in %{_libdir}/php/modules.
EXTENSION_DIR=%{_libdir}/php/modules; export EXTENSION_DIR

# Set PEAR_INSTALLDIR to ensure that the hard-coded include_path
# includes the PEAR directory even though pear is packaged
# separately.
PEAR_INSTALLDIR=%{_datadir}/pear; export PEAR_INSTALLDIR

# Shell function to configure and build a PHP tree.
build() {
# bison-1.875-2 seems to produce a broken parser; workaround.
mkdir Zend && cp ../Zend/zend_{language,ini}_{parser,scanner}.[ch] Zend
ln -sf ../configure
%configure \
	--cache-file=../config.cache \
        --with-libdir=%{_lib} \
	--with-config-file-path=%{_sysconfdir} \
	--with-config-file-scan-dir=%{_sysconfdir}/php.d \
	--disable-debug \
	--with-pic \
	--enable-libxml \
	--disable-rpath \
	--without-pear \
	--with-bz2 \
	--with-exec-dir=%{_bindir} \
	--with-freetype-dir=%{_prefix} \
	--with-png-dir=%{_prefix} \
	--with-xpm-dir=%{_prefix} \
	--enable-gd-native-ttf \
	--without-gdbm \
	--with-gettext \
	--with-gmp \
	--with-iconv \
	--with-jpeg-dir=%{_prefix} \
	--with-openssl \
%if 0%{?fedora} >= 8
        --with-pcre-regex=%{_prefix} \
%endif
	--with-zlib \
	--with-layout=GNU \
	--enable-exif \
	--enable-ftp \
	--enable-magic-quotes \
	--enable-sockets \
	--enable-sysvsem --enable-sysvshm --enable-sysvmsg \
	--with-kerberos \
	--enable-ucd-snmp-hack \
	--enable-shmop \
	--enable-calendar \
        --with-libxml-dir=%{_prefix} \
	--enable-xml \
        --with-system-tzdata \
	$* 
if test $? != 0; then 
  tail -500 config.log
  : configure failed
  exit 1
fi

make %{?_smp_mflags}
}

# Build /usr/bin/php-cgi with the CGI SAPI, and all the shared extensions
pushd build-cgi

# RC patch ??? (only for EL-5 ??)

build --enable-force-cgi-redirect \
      --disable-all \
      --enable-pcntl \
      --enable-tokenizer=shared \
      --enable-session=shared \
      --enable-hash=shared \
      --with-imap=shared --with-imap-ssl \
      --enable-mbstring=shared \
      --enable-mbregex \
      --with-gd=shared \
      --enable-bcmath=shared \
      --enable-dba=shared --with-db4=%{_prefix} \
      --with-xmlrpc=shared \
      --with-ldap=shared --with-ldap-sasl \
      --with-mysql=shared,%{_prefix} \
      --with-mysqli=shared,%{_bindir}/mysql_config \
%ifarch x86_64
      %{?_with_oci8:--with-oci8=shared,instantclient,%{_libdir}/oracle/%{oraclever}/client64/lib,%{oraclever}} \
%else
      %{?_with_oci8:--with-oci8=shared,instantclient,%{_libdir}/oracle/%{oraclever}/client/lib,%{oraclever}} \
%endif
      %{?_with_oci8:--with-pdo-oci=shared,instantclient,/usr,%{oraclever}} \
      %{?_with_ibase:--with-interbase=shared,%{_libdir}/firebird} \
      %{?_with_ibase:--with-pdo-firebird=shared,%{_libdir}/firebird} \
      --enable-dom=shared \
      --with-pgsql=shared \
      --enable-wddx=shared \
      --with-snmp=shared,%{_prefix} \
      --enable-soap=shared \
      --with-xsl=shared,%{_prefix} \
      --enable-xmlreader=shared --enable-xmlwriter=shared \
      --with-curl=shared,%{_prefix} \
      --enable-fastcgi \
      --enable-pdo=shared \
      --with-pdo-odbc=shared,unixODBC,%{_prefix} \
      --with-pdo-mysql=shared,%{_prefix} \
      --with-pdo-pgsql=shared,%{_prefix} \
      --with-pdo-dblib=shared,%{_prefix} \
      --enable-json=shared \
      --enable-zip=shared \
      --without-readline \
      --with-pspell=shared \
      --enable-phar=shared \
      --with-mcrypt=shared,%{_prefix} \
      --with-tidy=shared,%{_prefix} \
      --with-mssql=shared,%{_prefix} \
      --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
      --enable-posix=shared \
      --with-unixODBC=shared,%{_prefix} \
      --enable-fileinfo=shared \
      --enable-intl=shared \
      --with-icu-dir=%{_prefix} \
%if %{with_enchant}
      --with-enchant=shared,%{_prefix} \
%endif
      --with-recode=shared,%{_prefix}
popd

without_shared="--without-mysql --without-gd \
      --disable-dom --disable-dba --without-unixODBC \
      --disable-pdo --disable-xmlreader --disable-xmlwriter \
      --without-sqlite \
      --without-sqlite3 --disable-phar --disable-fileinfo \
      --disable-json --without-pspell --disable-wddx \
      --without-curl --disable-posix \
      --disable-sysvmsg --disable-sysvshm --disable-sysvsem"

# Build Apache module, and the CLI SAPI, /usr/bin/php

%if %{with_fpm}
# Build php-fpm
pushd build-fpm
build --enable-fpm ${without_shared}
popd
%endif

# Build for inclusion as embedded script language into applications,
# /usr/lib[64]/libphp5.so
pushd build-embedded
build --enable-embed ${without_shared}
popd

%check
%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# Install the version for embedded script language in applications + php_embed.h
make -C build-embedded install-sapi install-headers INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with_fpm}
# Install the php-fpm binary
make -C build-fpm install-fpm INSTALL_ROOT=$RPM_BUILD_ROOT 
%endif

# Install everything from the CGI SAPI build
make -C build-cgi install INSTALL_ROOT=$RPM_BUILD_ROOT 

# Install the default configuration file and icons
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/php.ini
install -m 755 -d $RPM_BUILD_ROOT%{contentdir}/icons
install -m 644    *.gif $RPM_BUILD_ROOT%{contentdir}/icons/

# For third-party packaging:
install -m 755 -d $RPM_BUILD_ROOT%{_libdir}/php/pear \
                  $RPM_BUILD_ROOT%{_datadir}/php

install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php.d
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/session

%if %{with_fpm}
# PHP-FPM stuff
# Log
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/log/php-fpm
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/run/php-fpm
# Config
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d/www.conf
mv $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf.default .
# Service
install -m 755 -d $RPM_BUILD_ROOT%{_initrddir}
install -m 755 %{SOURCE6} $RPM_BUILD_ROOT%{_initrddir}/php-fpm
# LogRotate
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/php-fpm
# nginx
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/nginx/
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/php.conf
%endif


# Fix the link
(cd $RPM_BUILD_ROOT%{_bindir}; ln -sfn phar.phar phar)

# Generate files lists and stub .ini files for each subpackage
for mod in pgsql hash tokenizer session mysql mysqli odbc ldap snmp xmlrpc imap \
    mbstring gd dom xsl soap bcmath dba xmlreader xmlwriter \
    %{?_with_oci8:oci8} %{?_with_oci8:pdo_oci} %{?_with_ibase:interbase} %{?_with_ibase:pdo_firebird} \
    pdo pdo_mysql pdo_pgsql pdo_odbc json zip \
%if %{with_enchant}
    enchant \
%endif
    phar fileinfo intl \
    mcrypt tidy pdo_dblib mssql pspell curl wddx \
    posix sysvshm sysvsem sysvmsg recode; do
    cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/${mod}.ini <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF
    cat > files.${mod} <<EOF
%attr(755,root,root) %{_libdir}/php/modules/${mod}.so
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/php.d/${mod}.ini
EOF
done

# The dom, xsl and xml* modules are all packaged in php-xml
cat files.dom files.xsl files.xml{reader,writer} files.wddx > files.xml

# The mysql and mysqli modules are both packaged in php-mysql
cat files.mysqli >> files.mysql

# Split out the PDO modules
cat files.pdo_dblib >> files.mssql
cat files.pdo_mysql >> files.mysql
cat files.pdo_pgsql >> files.pgsql
cat files.pdo_odbc >> files.odbc
%if %{with_oci8}
cat files.pdo_oci >> files.oci8
%endif
%if %{with_ibase}
cat files.pdo_firebird >> files.interbase
%endif

# sysv* and posix in packaged in php-process
cat files.sysv* files.posix > files.process

# Package json, zip, curl, phar and fileinfo in -common.
cat files.json files.zip files.curl files.phar files.fileinfo > files.common

# Install the macros file:
install -d $RPM_BUILD_ROOT%{_sysconfdir}/rpm
sed -e "s/@PHP_APIVER@/%{apiver}/;s/@PHP_ZENDVER@/%{zendver}/;s/@PHP_PDOVER@/%{pdover}/" \
    < $RPM_SOURCE_DIR/macros.php > macros.php
install -m 644 -c macros.php \
           $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.php

# Remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_libdir}/php/modules/*.a \
       $RPM_BUILD_ROOT%{_bindir}/{phptar} \
       $RPM_BUILD_ROOT%{_datadir}/pear \
       $RPM_BUILD_ROOT%{_libdir}/libphp5.la

# Remove irrelevant docs
rm -f README.{Zeus,QNX,CVS-RULES}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
rm files.* macros.php

%pre common
echo -e "\nWARNING : This %{name}-* RPM are not official Fedora/Redhat build and"
echo -e "overrides the official ones. Don't file bugs on Fedora Project nor Redhat.\n"
echo -e "Use dedicated forums http://forums.famillecollet.com/\n"

%if %{?fedora}%{!?fedora:99} <= 11
echo -e "WARNING : Fedora %{fedora} is now EOL :"
echo -e "You should consider upgrading to a supported release.\n"
%endif


%if %{with_fpm}
%post fpm
/sbin/chkconfig --add php-fpm

%preun fpm
if [ "$1" = 0 ] ; then
    /sbin/service php-fpm stop >/dev/null 2>&1
    /sbin/chkconfig --del php-fpm
fi
%endif

%post embedded -p /sbin/ldconfig
%postun embedded -p /sbin/ldconfig

%files
%defattr(-,root,root)
%attr(0770,root,www) %dir %{_localstatedir}/lib/php/session
%{contentdir}/icons/php.gif

%files common -f files.common
%defattr(-,root,root)
%doc CODING_STANDARDS CREDITS EXTENSIONS INSTALL LICENSE NEWS README*
%doc Zend/ZEND_* TSRM_LICENSE regex_COPYRIGHT
%doc php.ini-*
%config(noreplace) %{_sysconfdir}/php.ini
%dir %{_sysconfdir}/php.d
%dir %{_libdir}/php
%dir %{_libdir}/php/modules
%dir %{_localstatedir}/lib/php
%dir %{_libdir}/php/pear
%dir %{_datadir}/php

%files cli
%defattr(-,root,root)
%{_bindir}/php
%{_bindir}/php-cgi
%{_bindir}/phar.phar
%{_bindir}/phar
%{_mandir}/man1/php.1*
%doc sapi/cgi/README* sapi/cli/README

%if %{with_fpm}
%files fpm
%defattr(-,root,root)
%doc php-fpm.conf.default
%config(noreplace) %{_sysconfdir}/php-fpm.conf
%config(noreplace) %{_sysconfdir}/php-fpm.d/www.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/php-fpm
%config(noreplace) %{_sysconfdir}/nginx/php.conf
%{_sbindir}/php-fpm
%{_initrddir}/php-fpm
%dir %{_sysconfdir}/php-fpm.d
%attr(770,www,www) %dir %{_localstatedir}/log/php-fpm
%dir %{_localstatedir}/run/php-fpm
%{_mandir}/man1/php-fpm.1*
%endif

%files devel
%defattr(-,root,root)
%{_bindir}/php-config
%{_bindir}/phpize
%{_includedir}/php
%{_libdir}/php/build
%{_mandir}/man1/php-config.1*
%{_mandir}/man1/phpize.1*
%config %{_sysconfdir}/rpm/macros.php

%files embedded
%defattr(-,root,root,-)
%{_libdir}/libphp5.so
%{_libdir}/libphp5-%{phpversion}.so

%files tokenizer -f files.tokenizer
%files session -f files.session
%files hash -f files.hash
%files pgsql -f files.pgsql
%files mysql -f files.mysql
%files odbc -f files.odbc
%files imap -f files.imap
%files ldap -f files.ldap
%files snmp -f files.snmp
%files xml -f files.xml
%files xmlrpc -f files.xmlrpc
%files mbstring -f files.mbstring
%files gd -f files.gd
%defattr(-,root,root,-)
%doc gd_README
%files soap -f files.soap
%files bcmath -f files.bcmath
%files dba -f files.dba
%files pdo -f files.pdo
%files mcrypt -f files.mcrypt
%files tidy -f files.tidy
%files mssql -f files.mssql
%files pspell -f files.pspell
%files intl -f files.intl
%files process -f files.process
%files recode -f files.recode
%if %{with_enchant}
%files enchant -f files.enchant
%endif

%if %{with_oci8}
%files oci8 -f files.oci8
%endif

%if %{with_ibase}
%files interbase -f files.interbase
%endif

%changelog
