# Copyright (c) 2000, 2011, Oracle and/or its affiliates. All rights reserved.
#
##############################################################################
#
# This is the spec file for the distribution specific RPM files
#
##############################################################################

##############################################################################
# Some common macro definitions
##############################################################################

# NOTE: "vendor" is used in upgrade/downgrade check, so you can't
# change these, has to be exactly as is.
%define mysql_old_vendor	MySQL AB
%define mysql_vendor_2		Sun Microsystems, Inc.
%define mysql_vendor		Oracle and/or its affiliates

%define mysql_version 5.1.59
%define distribution  rhel5
%define release       1.%{distribution}

%define mysqld_user    mysql
%define mysqld_group   mysql
%define mysqldatadir   /var/lib/mysql
%define see_base For a description of MySQL see the base MySQL RPM or http://www.mysql.com

# ------------------------------------------------------------------------------
# Meta information, don't remove!
# ------------------------------------------------------------------------------
# norootforbuild

# ------------------------------------------------------------------------------
# On SuSE 9 no separate "debuginfo" package is built. To enable basic
# debugging on that platform, we don't strip binaries on SuSE 9. We
# disable the strip of binaries by redefining the RPM macro
# "__os_install_post" leaving out the script calls that normally does
# this. We do this in all cases, as on platforms where "debuginfo" is
# created, a script "find-debuginfo.sh" will be called that will do
# the strip anyway, part of separating the executable and debug
# information into separate files put into separate packages.
#
# Some references (shows more advanced conditional usage):
# http://www.redhat.com/archives/rpm-list/2001-November/msg00257.html
# http://www.redhat.com/archives/rpm-list/2003-February/msg00275.html
# http://www.redhat.com/archives/rhl-devel-list/2004-January/msg01546.html
# http://lists.opensuse.org/archive/opensuse-commit/2006-May/1171.html
# ------------------------------------------------------------------------------
%define __os_install_post /usr/lib/rpm/brp-compress

# ------------------------------------------------------------------------------
# We don't package all files installed into the build root by intention -
# See BUG#998 for details.
# ------------------------------------------------------------------------------
%define _unpackaged_files_terminate_build 0

# ------------------------------------------------------------------------------
# RPM build tools now automatically detects Perl module dependencies. This
# detection gives problems as it is broken in some versions, and it also
# give unwanted dependencies from mandatory scripts in our package.
# Might not be possible to disable in all RPM tool versions, but here we
# try. We keep the "AutoReqProv: no" for the "test" sub package, as disabling
# here might fail, and that package has the most problems.
# See http://fedoraproject.org/wiki/Packaging/Perl#Filtering_Requires:_and_Provides
#     http://www.wideopen.com/archives/rpm-list/2002-October/msg00343.html
# ------------------------------------------------------------------------------
%undefine __perl_provides
%undefine __perl_requires

##############################################################################
# Command line handling
##############################################################################

# ----------------------------------------------------------------------
# use "rpmbuild --with yassl" or "rpm --define '_with_yassl 1'" (for RPM 3.x)
# to build with yaSSL support (off by default)
# ----------------------------------------------------------------------
%{?_with_yassl:%define YASSL_BUILD 1}
%{!?_with_yassl:%define YASSL_BUILD 0}

# ----------------------------------------------------------------------
# use "rpmbuild --without bundled_zlib" or "rpm --define '_without_bundled_zlib 1'"
# (for RPM 3.x) to not build using the bundled zlib (on by default)
# ----------------------------------------------------------------------
%{!?_with_bundled_zlib: %{!?_without_bundled_zlib: %define WITH_BUNDLED_ZLIB 1}}
%{?_with_bundled_zlib:%define WITH_BUNDLED_ZLIB 1}
%{?_without_bundled_zlib:%define WITH_BUNDLED_ZLIB 0}

# ----------------------------------------------------------------------
# use "rpmbuild --without innodb_plugin" or "rpm --define '_without_innodb_plugin 1'"
# (for RPM 3.x) to not build the innodb plugin (on by default with innodb builds)
# ----------------------------------------------------------------------
%{!?_with_innodb_plugin: %{!?_without_innodb_plugin: %define WITH_INNODB_PLUGIN 1}}
%{?_with_innodb_plugin:%define WITH_INNODB_PLUGIN 1}
%{?_without_innodb_plugin:%define WITH_INNODB_PLUGIN 0}

##############################################################################
# Product definitions - one of these has to be defined via the RPM build
# options, e.g. "--define 'enterprise 1'"
##############################################################################

%{!?enterprise_gpl_pro:%define enterprise_gpl_pro 0}
%{!?enterprise_commercial_pro:%define enterprise_commercial_pro 0}
%{!?enterprise_gpl_advanced:%define enterprise_gpl_advanced 0}
%{!?enterprise_commercial_advanced:%define enterprise_commercial_advanced 0}
%{!?enterprise_gpl_classic:%define enterprise_gpl_classic 0}
%{!?enterprise_commercial_classic:%define enterprise_commercial_classic 0}
%{!?cluster:%define cluster 0}
%{!?cluster_innodb:%define cluster_innodb 0}
%{!?cluster_gpl:%define cluster_gpl 0}
%{!?community:%define community 0}

%if %{community}
%define server_suffix  -community
%define package_suffix -community
%define ndbug_comment MySQL Community Server (GPL)
%define debug_comment MySQL Community Server - Debug (GPL)
%define commercial 0
%define EMBEDDED_BUILD 1
%define PARTITION_BUILD 1
%define CLUSTER_BUILD 0
%define COMMUNITY_BUILD 1
%define INNODB_BUILD 1
%define NORMAL_TEST_MODE test-bt
%define DEBUG_TEST_MODE test-bt-debug
%endif

%if %{enterprise_commercial_advanced}
%define server_suffix  -enterprise-commercial-advanced
%define package_suffix -advanced
%define ndbug_comment MySQL Enterprise Server - Advanced Edition (Commercial)
%define debug_comment MySQL Enterprise Server - Advanced Edition Debug (Commercial)
%define commercial 1
%define EMBEDDED_BUILD 1
%define PARTITION_BUILD 1
%define CLUSTER_BUILD 0
%define COMMUNITY_BUILD 0
%define INNODB_BUILD 1
%define NORMAL_TEST_MODE test-bt
%define DEBUG_TEST_MODE test-bt-debug
%endif

%if %{enterprise_gpl_advanced}
%define server_suffix  -enterprise-gpl-advanced
%define package_suffix -advanced-gpl
%define ndbug_comment MySQL Enterprise Server - Advanced Edition (GPL)
%define debug_comment MySQL Enterprise Server - Advanced Edition Debug (GPL)
%define commercial 0
%define EMBEDDED_BUILD 1
%define PARTITION_BUILD 1
%define CLUSTER_BUILD 0
%define COMMUNITY_BUILD 0
%define INNODB_BUILD 1
%define NORMAL_TEST_MODE test-bt-fast
%define DEBUG_TEST_MODE test-bt-debug-fast
%endif

%if %{enterprise_commercial_pro}
%define server_suffix  -enterprise-commercial-pro
%define package_suffix -enterprise
%define ndbug_comment MySQL Enterprise Server - Pro Edition (Commercial)
%define debug_comment MySQL Enterprise Server - Pro Edition Debug (Commercial)
%define commercial 1
%define EMBEDDED_BUILD 1
%define PARTITION_BUILD 0
%define CLUSTER_BUILD 0
%define COMMUNITY_BUILD 0
%define INNODB_BUILD 1
%define NORMAL_TEST_MODE test-bt-fast
%define DEBUG_TEST_MODE test-bt-debug-fast
%endif

%if %{enterprise_gpl_pro}
%define server_suffix  -enterprise-gpl-pro
%define package_suffix -enterprise-gpl
%define ndbug_comment MySQL Enterprise Server - Pro Edition (GPL)
%define debug_comment MySQL Enterprise Server - Pro Edition Debug (GPL)
%define commercial 0
%define EMBEDDED_BUILD 1
%define PARTITION_BUILD 0
%define CLUSTER_BUILD 0
%define COMMUNITY_BUILD 0
%define INNODB_BUILD 1
%define NORMAL_TEST_MODE test-bt
%define DEBUG_TEST_MODE test-bt-debug
%endif

%if %{enterprise_gpl_classic}
%define server_suffix  -enterprise-gpl-classic
%define package_suffix -classic-gpl
%define ndbug_comment MySQL Enterprise Server - Classic Edition (GPL)
%define debug_comment MySQL Enterprise Server - Classic Edition Debug (GPL)
%define commercial 0
%define EMBEDDED_BUILD 1
%define PARTITION_BUILD 1
%define CLUSTER_BUILD 0
%define COMMUNITY_BUILD 0
%define INNODB_BUILD 0
%define NORMAL_TEST_MODE test-bt-fast
%define DEBUG_TEST_MODE test-bt-debug-fast
%endif

%if %{enterprise_commercial_classic}
%define server_suffix  -enterprise-commercial-classic
%define package_suffix -classic
%define ndbug_comment MySQL Enterprise Server - Classic Edition (Commercial)
%define debug_comment MySQL Enterprise Server - Classic Edition Debug (Commercial)
%define commercial 1
%define EMBEDDED_BUILD 1
%define PARTITION_BUILD 0
%define CLUSTER_BUILD 0
%define COMMUNITY_BUILD 0
%define INNODB_BUILD 0
%define NORMAL_TEST_MODE test-bt-fast
%define DEBUG_TEST_MODE test-bt-debug-fast
%endif

%if %{cluster}
%define server_suffix  -cluster
%define package_suffix -cluster
%define ndbug_comment MySQL Cluster (Commercial)
%define debug_comment MySQL Cluster - Debug (Commercial)
%define commercial 1
%define EMBEDDED_BUILD 1
%define PARTITION_BUILD 0
%define CLUSTER_BUILD 1
%define COMMUNITY_BUILD 0
%define INNODB_BUILD 0
%define NORMAL_TEST_MODE test-bt
%define DEBUG_TEST_MODE test-bt-debug
%endif

%if %{cluster_innodb}
%define server_suffix  -cluster-innodb
%define package_suffix -cluster-innodb
%define ndbug_comment MySQL Cluster+InnoDB (Commercial)
%define debug_comment MySQL Cluster+InnoDB - Debug (Commercial)
%define commercial 1
%define EMBEDDED_BUILD 1
%define PARTITION_BUILD 0
%define CLUSTER_BUILD 1
%define COMMUNITY_BUILD 0
%define INNODB_BUILD 1
%define NORMAL_TEST_MODE test-bt
%define DEBUG_TEST_MODE test-bt-debug
%endif

%if %{cluster_gpl}
%define server_suffix  -cluster-gpl
%define package_suffix -cluster-gpl
%define ndbug_comment MySQL Cluster Server (GPL)
%define debug_comment MySQL Cluster Server - Debug (GPL)
%define commercial 0
%define EMBEDDED_BUILD 1
%define PARTITION_BUILD 0
%define CLUSTER_BUILD 1
%define COMMUNITY_BUILD 0
%define INNODB_BUILD 1
%define NORMAL_TEST_MODE test-bt
%define DEBUG_TEST_MODE test-bt-debug
%endif

%if %{commercial}
%define lic_type Commercial
%define lic_files LICENSE.mysql
%if %{INNODB_BUILD}
%define src_dir mysqlcom-pro-%{mysql_version}
%else
%define src_dir mysqlcom-%{mysql_version}
%endif
%else
%define lic_type GPL
%define lic_files COPYING README
%define src_dir mysql-%{mysql_version}
%endif

%if %{COMMUNITY_BUILD}
%define cluster_package_prefix -cluster
%else
%define cluster_package_prefix -
%endif

##############################################################################
# Main spec file section
##############################################################################

Name:		MySQL%{package_suffix}
Summary:	MySQL: a very fast and reliable SQL database server
Group:		Applications/Databases
Version:	5.1.59
Release:	%{release}
Distribution:	Red Hat Enterprise Linux 5
License:	Copyright 2000-2008 MySQL AB, 2008-2011 %{mysql_vendor}  All rights reserved.  Use is subject to license terms.  Under %{lic_type} license as shown in the Description field.
Source:		%{src_dir}.tar.gz
URL:		http://www.mysql.com/
Packager:	%{mysql_vendor} Product Engineering Team <build@mysql.com>
Vendor:		%{mysql_vendor}
Provides:	msqlormysql MySQL-server mysql
BuildRequires:  gperf perl readline-devel gcc-c++ ncurses-devel zlib-devel libtool automake autoconf time

# Think about what you use here since the first step is to
# run a rm -rf
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

# From the manual
%description
The MySQL(TM) software delivers a very fast, multi-threaded, multi-user,
and robust SQL (Structured Query Language) database server. MySQL Server
is intended for mission-critical, heavy-load production systems as well
as for embedding into mass-deployed software. MySQL is a trademark of
%{mysql_vendor}

The MySQL software has Dual Licensing, which means you can use the MySQL
software free of charge under the GNU General Public License
(http://www.gnu.org/licenses/). You can also purchase commercial MySQL
licenses from %{mysql_vendor} if you do not wish to be bound by the terms of
the GPL. See the chapter "Licensing and Support" in the manual for
further info.

The MySQL web site (http://www.mysql.com/) provides the latest
news and information about the MySQL software. Also please see the
documentation and the manual for more information.

##############################################################################
# Sub package definition
##############################################################################

%package -n MySQL-server%{package_suffix}
Summary:	@COMMENT@ for Red Hat Enterprise Linux 5
Group:		Applications/Databases
Requires:	 chkconfig coreutils shadow-utils grep procps
Provides:	msqlormysql mysql-server mysql MySQL MySQL-server
Obsoletes:	MySQL mysql mysql-server MySQL-server

%description -n MySQL-server%{package_suffix}
The MySQL(TM) software delivers a very fast, multi-threaded, multi-user,
and robust SQL (Structured Query Language) database server. MySQL Server
is intended for mission-critical, heavy-load production systems as well
as for embedding into mass-deployed software. MySQL is a trademark of
%{mysql_vendor}

The MySQL software has Dual Licensing, which means you can use the MySQL
software free of charge under the GNU General Public License
(http://www.gnu.org/licenses/). You can also purchase commercial MySQL
licenses from %{mysql_vendor} if you do not wish to be bound by the terms of
the GPL. See the chapter "Licensing and Support" in the manual for
further info.

The MySQL web site (http://www.mysql.com/) provides the latest
news and information about the MySQL software. Also please see the
documentation and the manual for more information.

This package includes the MySQL server binary
%if %{INNODB_BUILD}
(configured including InnoDB)
%endif
as well as related utilities to run and administer a MySQL server.

If you want to access and work with the database, you have to install
package "MySQL-client%{package_suffix}" as well!

# ------------------------------------------------------------------------------

%package -n MySQL-client%{package_suffix}
Summary: MySQL - Client
Group: Applications/Databases
Obsoletes: mysql-client MySQL-client
Provides: mysql-client MySQL-client

%description -n MySQL-client%{package_suffix}
This package contains the standard MySQL clients and administration tools.

%{see_base}

# ------------------------------------------------------------------------------

%if %{CLUSTER_BUILD}
%package -n MySQL%{cluster_package_prefix}storage%{package_suffix}
Summary:	MySQL - ndbcluster storage engine
Group:		Applications/Databases
Obsoletes:	ndb-storage
Provides:	ndb-storage

%description -n MySQL%{cluster_package_prefix}storage%{package_suffix}
This package contains the ndbcluster storage engine.
It is necessary to have this package installed on all
computers that should store ndbcluster table data.

%{see_base}

# ------------------------------------------------------------------------------

%package -n MySQL%{cluster_package_prefix}management%{package_suffix}
Summary:	MySQL - ndbcluster storage engine management
Group:		Applications/Databases
Obsoletes:	ndb-management
Provides:	ndb-management

%description -n MySQL%{cluster_package_prefix}management%{package_suffix}
This package contains ndbcluster storage engine management.
It is necessary to have this package installed on at least
one computer in the cluster.

%{see_base}

# ------------------------------------------------------------------------------

%package -n MySQL%{cluster_package_prefix}tools%{package_suffix}
Summary:	MySQL - ndbcluster storage engine basic tools
Group:		Applications/Databases
Obsoletes:	ndb-tools
Provides:	ndb-tools

%description -n MySQL%{cluster_package_prefix}tools%{package_suffix}
This package contains ndbcluster storage engine basic tools.

%{see_base}

# ------------------------------------------------------------------------------

%package -n MySQL%{cluster_package_prefix}extra%{package_suffix}
Summary:	MySQL - ndbcluster storage engine extra tools
Group:		Applications/Databases
Obsoletes:	ndb-extra
Provides:	ndb-extra

%description -n MySQL%{cluster_package_prefix}extra%{package_suffix}
This package contains some extra ndbcluster storage engine tools for the advanced user.
They should be used with caution.

%{see_base}
%endif

# ------------------------------------------------------------------------------

%package -n MySQL-test%{package_suffix}
Requires: mysql-client perl
Summary: MySQL - Test suite
Group: Applications/Databases
Provides: mysql-test MySQL-test
Obsoletes: mysql-test MySQL-test
AutoReqProv: no

%description -n MySQL-test%{package_suffix}
This package contains the MySQL regression test suite.

%{see_base}

# ------------------------------------------------------------------------------

%package -n MySQL-devel%{package_suffix}
Summary: MySQL - Development header files and libraries
Group: Applications/Databases
Provides: mysql-devel MySQL-devel
Obsoletes: mysql-devel MySQL-devel

%description -n MySQL-devel%{package_suffix}
This package contains the development header files and libraries
necessary to develop MySQL client applications.

%{see_base}

# ------------------------------------------------------------------------------

%package -n MySQL-shared%{package_suffix}
Summary: MySQL - Shared libraries
Group: Applications/Databases
Provides: mysql-shared MySQL-shared
# Obsoletes below to correct old missing Provides:/Obsoletes
Obsoletes: mysql-shared MySQL-shared-standard MySQL-shared-pro
Obsoletes: MySQL-shared-pro-cert MySQL-shared-pro-gpl
Obsoletes: MySQL-shared-pro-gpl-cert MySQL-shared

%description -n MySQL-shared%{package_suffix}
This package contains the shared libraries (*.so*) which certain
languages and applications need to dynamically load and use MySQL.

# ------------------------------------------------------------------------------

%if %{EMBEDDED_BUILD}

%package -n MySQL-embedded%{package_suffix}
Requires: mysql-devel
Summary: MySQL - Embedded library
Group: Applications/Databases
Provides: mysql-embedded MySQL-embedded
Obsoletes: mysql-embedded MySQL-embedded
Obsoletes: MySQL-embedded-classic MySQL-embedded-pro

%description -n MySQL-embedded%{package_suffix}
This package contains the MySQL server as an embedded library.

The embedded MySQL server library makes it possible to run a
full-featured MySQL server inside the client application.
The main benefits are increased speed and more simple management
for embedded applications.

The API is identical for the embedded MySQL version and the
client/server version.

%{see_base}

%endif

##############################################################################
#
##############################################################################

%prep
%setup -n %{src_dir}

##############################################################################
# The actual build
##############################################################################

%build

# Optional package files
touch optional-files-devel

BuildMySQL() {
# Fall back on RPM_OPT_FLAGS (part of RPM environment) if no flags are given.
CFLAGS=${CFLAGS:-$RPM_OPT_FLAGS}
CXXFLAGS=${CXXFLAGS:-$RPM_OPT_FLAGS -felide-constructors -fno-exceptions -fno-rtti }
# Evaluate current setting of $DEBUG
if [ $DEBUG -gt 0 ] ; then
	OPT_COMMENT='--with-comment="%{debug_comment}"'
	OPT_DEBUG='--with-debug --enable-mysql-maintainer-mode=no'
	CFLAGS=`echo   " $CFLAGS "   | \
	    sed -e 's/ -O[0-9]* / /' -e 's/ -unroll2 / /' -e 's/ -ip / /' \
	        -e 's/^ //' -e 's/ $//'`
	CXXFLAGS=`echo " $CXXFLAGS " | \
	    sed -e 's/ -O[0-9]* / /' -e 's/ -unroll2 / /' -e 's/ -ip / /' \
	        -e 's/^ //' -e 's/ $//'`
else
	OPT_COMMENT='--with-comment="%{ndbug_comment}"'
	OPT_DEBUG=''
fi
# The --enable-assembler simply does nothing on systems that does not
# support assembler speedups.
sh -c  "PATH=\"${MYSQL_BUILD_PATH:-$PATH}\" \
	CC=\"${MYSQL_BUILD_CC:-$CC}\" \
	CXX=\"${MYSQL_BUILD_CXX:-$CXX}\" \
	CFLAGS=\"$CFLAGS\" \
	CXXFLAGS=\"$CXXFLAGS\" \
	LDFLAGS=\"$LDFLAGS\" \
	./configure \
 	    $* \
	    --enable-assembler \
	    --enable-local-infile \
	    --with-mysqld-user=%{mysqld_user} \
	    --with-unix-socket-path=/var/lib/mysql/mysql.sock \
	    --with-pic \
	    --prefix=/ \
%if %{CLUSTER_BUILD}
	    --with-extra-charsets=all \
%else
	    --with-extra-charsets=complex \
%endif
%if %{YASSL_BUILD}
	    --with-ssl \
%else
	    --without-ssl \
%endif
	    --exec-prefix=%{_exec_prefix} \
	    --libexecdir=%{_sbindir} \
	    --libdir=%{_libdir} \
	    --sysconfdir=%{_sysconfdir} \
	    --datadir=%{_datadir} \
	    --localstatedir=%{mysqldatadir} \
	    --infodir=%{_infodir} \
	    --includedir=%{_includedir} \
	    --mandir=%{_mandir} \
	    --enable-thread-safe-client \
	    $OPT_COMMENT \
	    $OPT_DEBUG \
%if %{commercial}
	    --with-libedit \
%else
	    --with-readline \
%endif
%if %{WITH_BUNDLED_ZLIB}
	    --with-zlib-dir=bundled \
%endif
	    ; make"
}
# end of function definition "BuildMySQL"


BuildServer() {
BuildMySQL " \
                $* \
%if %{?server_suffix:1}0
		--with-server-suffix='%{server_suffix}' \
%endif
%if %{CLUSTER_BUILD}
		--with-plugin-ndbcluster \
%else
		--without-plugin-ndbcluster \
%endif
%if %{INNODB_BUILD}
		--with-plugin-innobase \
%if %{WITH_INNODB_PLUGIN}
%else
		--without-plugin-innodb_plugin \
%endif
%else
		--without-plugin-innobase \
		--without-plugin-innodb_plugin \
%endif
%if %{PARTITION_BUILD}
		--with-plugin-partition \
%else
		--without-plugin-partition \
%endif
		--with-plugin-csv \
		--with-plugin-archive \
		--with-plugin-blackhole \
		--with-plugin-federated \
		--without-plugin-daemon_example \
		--without-plugin-ftexample \
		--without-plugin-example \
%if %{EMBEDDED_BUILD}
		--with-embedded-server \
%else
		--without-embedded-server \
%endif
		--without-bench \
		--with-big-tables"

if [ -n "$MYSQL_CONFLOG_DEST" ] ; then
	cp -fp config.log "$MYSQL_CONFLOG_DEST"
fi

if [ -f sql/.libs/mysqld ] ; then
	nm --numeric-sort sql/.libs/mysqld > sql/mysqld.sym
else
	nm --numeric-sort sql/mysqld > sql/mysqld.sym
fi
}
# end of function definition "BuildServer"


RBR=$RPM_BUILD_ROOT
MBD=$RPM_BUILD_DIR/%{src_dir}

# Clean up the BuildRoot first
[ "$RBR" != "/" ] && [ -d $RBR ] && rm -rf $RBR;
mkdir -p $RBR%{_libdir}/mysql $RBR%{_sbindir}

# Use gcc for C and C++ code (to avoid a dependency on libstdc++ and
# including exceptions into the code
if [ -z "$CXX" -a -z "$CC" ] ; then
	export CC="gcc" CXX="gcc"
fi

# Create the shared libs seperately to avoid a dependency for the client utilities
DEBUG=0
BuildMySQL "--enable-shared --without-server"

# Save shared libraries for putting in place later
mkdir -p $RBR/%{_libdir}/saved
mkdir -p $RBR/%{_libdir}/saved/mysql
cp -av libmysql/.libs/*.so*   $RBR/%{_libdir}/saved/
cp -av libmysql_r/.libs/*.so* $RBR/%{_libdir}/saved/

##############################################################################

#
# The shipped server is statically linked against the client libraries to
# avoid requiring the dependancy, however this means that any pluggable storage
# engines will not be built.  Thus we need yet another build phase where we
# enable shared then save them for later packing.
#
make clean
BuildServer "--enable-shared"
mkdir -p $RBR/%{_libdir}/saved/mysql/plugin/
%if %{INNODB_BUILD}
%if %{WITH_INNODB_PLUGIN}
cp -av storage/innodb_plugin/.libs/*.so* $RBR/%{_libdir}/saved/mysql/plugin
%endif
%endif

# Now create a debug server
DEBUG=1
make clean

( BuildServer "--disable-shared" )   # subshell, so that CFLAGS + CXXFLAGS are modified only locally

if [ "$MYSQL_RPMBUILD_TEST" != "no" ] ; then
	MTR_BUILD_THREAD=auto make test-bt-debug
fi

# Get the debug server and its .sym file from the build tree
if [ -f sql/.libs/mysqld ] ; then
	cp sql/.libs/mysqld $RBR%{_sbindir}/mysqld-debug
else
	cp sql/mysqld       $RBR%{_sbindir}/mysqld-debug
fi
%if %{EMBEDDED_BUILD}
cp libmysqld/libmysqld.a    $RBR%{_libdir}/mysql/libmysqld-debug.a
%endif
cp sql/mysqld.sym           $RBR%{_libdir}/mysql/mysqld-debug.sym

##############################################################################
#
#  Build the release binary
#
##############################################################################

DEBUG=0
make clean

BuildServer "--disable-shared"

if [ "$MYSQL_RPMBUILD_TEST" != "no" ] ; then
	MTR_BUILD_THREAD=auto make test-bt
fi

##############################################################################

# For gcc builds, include libgcc.a in the devel subpackage (BUG 4921).  This
# needs to be during build phase as $CC is not set during install.
if "$CC" -v 2>&1 | grep '^gcc.version' >/dev/null 2>&1
then
  libgcc=`$CC $CFLAGS --print-libgcc-file`
  if [ -f "$libgcc" ]
  then
    mkdir -p $RBR%{_libdir}/mysql
    install -m 644 $libgcc $RBR%{_libdir}/mysql/libmygcc.a
    echo "%{_libdir}/mysql/libmygcc.a" >>optional-files-devel
  fi
fi

##############################################################################

%install
RBR=$RPM_BUILD_ROOT
MBD=$RPM_BUILD_DIR/%{src_dir}

# Ensure that needed directories exists
install -d $RBR%{_sysconfdir}/{logrotate.d,init.d}
install -d $RBR%{mysqldatadir}/mysql
install -d $RBR%{_datadir}/mysql-test
install -d $RBR%{_datadir}/mysql/SELinux/RHEL4
install -d $RBR%{_includedir}
install -d $RBR%{_libdir}
install -d $RBR%{_mandir}
install -d $RBR%{_sbindir}

make DESTDIR=$RBR benchdir_root=%{_datadir} testroot=%{_datadir} install

# install symbol files ( for stack trace resolution)
install -m 644 $MBD/sql/mysqld.sym $RBR%{_libdir}/mysql/mysqld.sym

# Install logrotate and autostart
install -m 644 $MBD/support-files/mysql-log-rotate $RBR%{_sysconfdir}/logrotate.d/mysql
install -m 755 $MBD/support-files/mysql.server $RBR%{_sysconfdir}/init.d/mysql

# in RPMs, it is unlikely that anybody should use "sql-bench"
rm -fr $RBR%{_datadir}/sql-bench

# Create a symlink "rcmysql", pointing to the init.script. SuSE users
# will appreciate that, as all services usually offer this.
ln -s %{_sysconfdir}/init.d/mysql $RBR%{_sbindir}/rcmysql

# Touch the place where the my.cnf config file and mysqlmanager.passwd
# (MySQL Instance Manager password file) might be located
# Just to make sure it's in the file list and marked as a config file
touch $RBR%{_sysconfdir}/my.cnf
touch $RBR%{_sysconfdir}/mysqlmanager.passwd

# Install SELinux files in datadir
install -m 600 $MBD/support-files/RHEL4-SElinux/mysql.{fc,te} \
	$RBR%{_datadir}/mysql/SELinux/RHEL4

# Now put saved shared libraries back into place
mv $RBR%{_libdir}/saved/*.so*   $RBR%{_libdir}/
%if %{INNODB_BUILD}
%if %{WITH_INNODB_PLUGIN}
mv $RBR%{_libdir}/saved/mysql/plugin/*.so* $RBR%{_libdir}/mysql/plugin/
%endif
%endif
rm -rf $RBR%{_libdir}/saved

##############################################################################
#  Post processing actions, i.e. when installed
##############################################################################

%pre -n MySQL-server%{package_suffix}
mysql_datadir=%{mysqldatadir}
# Check if we can safely upgrade.  An upgrade is only safe if it's from one
# of our RPMs in the same version family.

installed=`rpm -q --whatprovides mysql-server 2> /dev/null`
if [ $? -eq 0 -a -n "$installed" ]; then
  vendor=`rpm -q --queryformat='%{VENDOR}' "$installed" 2>&1`
  version=`rpm -q --queryformat='%{VERSION}' "$installed" 2>&1`
  myoldvendor='%{mysql_old_vendor}'
  myvendor_2='%{mysql_vendor_2}'
  myvendor='%{mysql_vendor}'
  myversion='%{mysql_version}'

  old_family=`echo $version   | sed -n -e 's,^\([1-9][0-9]*\.[0-9][0-9]*\)\..*$,\1,p'`
  new_family=`echo $myversion | sed -n -e 's,^\([1-9][0-9]*\.[0-9][0-9]*\)\..*$,\1,p'`

  [ -z "$vendor" ] && vendor='<unknown>'
  [ -z "$old_family" ] && old_family="<unrecognized version $version>"
  [ -z "$new_family" ] && new_family="<bad package specification: version $myversion>"

  error_text=
  if [ "$vendor" != "$myoldvendor" -a "$vendor" != "$myvendor_2" -a "$vendor" != "$myvendor" ]; then
    error_text="$error_text
The current MySQL server package is provided by a different
vendor ($vendor) than $myoldvendor, $myvendor_2, or $myvendor.
Some files may be installed to different locations, including log
files and the service startup script in %{_sysconfdir}/init.d/.
"
  fi

  if [ "$old_family" != "$new_family" ]; then
    error_text="$error_text
Upgrading directly from MySQL $old_family to MySQL $new_family may not
be safe in all cases.  A manual dump and restore using mysqldump is
recommended.  It is important to review the MySQL manual's Upgrading
section for version-specific incompatibilities.
"
  fi

  if [ -n "$error_text" ]; then
    cat <<HERE >&2

******************************************************************
A MySQL server package ($installed) is installed.
$error_text
A manual upgrade is required.

- Ensure that you have a complete, working backup of your data and my.cnf
  files
- Shut down the MySQL server cleanly
- Remove the existing MySQL packages.  Usually this command will
  list the packages you should remove:
  rpm -qa | grep -i '^mysql-'

  You may choose to use 'rpm --nodeps -ev <package-name>' to remove
  the package which contains the mysqlclient shared library.  The
  library will be reinstalled by the MySQL-shared-compat package.
- Install the new MySQL packages supplied by $myvendor
- Ensure that the MySQL server is started
- Run the 'mysql_upgrade' program

This is a brief description of the upgrade process.  Important details
can be found in the MySQL manual, in the Upgrading section.
******************************************************************
HERE
    exit 1
  fi
fi

# We assume that if there is exactly one ".pid" file,
# it contains the valid PID of a running MySQL server.
NR_PID_FILES=`ls $mysql_datadir/*.pid 2>/dev/null | wc -l`
case $NR_PID_FILES in
	0 ) SERVER_TO_START=''  ;;  # No "*.pid" file == no running server
	1 ) SERVER_TO_START='true' ;;
	* ) SERVER_TO_START=''      # Situation not clear
	    SEVERAL_PID_FILES=true ;;
esac
# That logic may be debated: We might check whether it is non-empty,
# contains exactly one number (possibly a PID), and whether "ps" finds it.
# OTOH, if there is no such process, it means a crash without a cleanup -
# is that a reason not to start a new server after upgrade?

STATUS_FILE=$mysql_datadir/RPM_UPGRADE_MARKER

if [ -f $STATUS_FILE ]; then
	echo "Some previous upgrade was not finished:"
	ls -ld $STATUS_FILE
	echo "Please check its status, then do"
	echo "    rm $STATUS_FILE"
	echo "before repeating the MySQL upgrade."
	exit 1
elif [ -n "$SEVERAL_PID_FILES" ] ; then
	echo "Your MySQL directory '$mysql_datadir' has more than one PID file:"
	ls -ld $mysql_datadir/*.pid
	echo "Please check which one (if any) corresponds to a running server"
	echo "and delete all others before repeating the MySQL upgrade."
	exit 1
fi

NEW_VERSION=%{mysql_version}-%{release}

# The "pre" section code is also run on a first installation,
# when there  is no data directory yet. Protect against error messages.
if [ -d $mysql_datadir ] ; then
	echo "MySQL RPM upgrade to version $NEW_VERSION"  > $STATUS_FILE
	echo "'pre' step running at `date`"          >> $STATUS_FILE
	echo                                         >> $STATUS_FILE
	echo "ERR file(s):"                          >> $STATUS_FILE
	ls -ltr $mysql_datadir/*.err                 >> $STATUS_FILE
	echo                                         >> $STATUS_FILE
	echo "Latest 'Version' line in latest file:" >> $STATUS_FILE
	grep '^Version' `ls -tr $mysql_datadir/*.err | tail -1` | \
		tail -1                              >> $STATUS_FILE
	echo                                         >> $STATUS_FILE

	if [ -n "$SERVER_TO_START" ] ; then
		# There is only one PID file, race possibility ignored
		echo "PID file:"                           >> $STATUS_FILE
		ls -l   $mysql_datadir/*.pid               >> $STATUS_FILE
		cat     $mysql_datadir/*.pid               >> $STATUS_FILE
		echo                                       >> $STATUS_FILE
		echo "Server process:"                     >> $STATUS_FILE
		ps -fp `cat $mysql_datadir/*.pid`          >> $STATUS_FILE
		echo                                       >> $STATUS_FILE
		echo "SERVER_TO_START=$SERVER_TO_START"    >> $STATUS_FILE
	else
		# Take a note we checked it ...
		echo "PID file:"                           >> $STATUS_FILE
		ls -l   $mysql_datadir/*.pid               >> $STATUS_FILE 2>&1
	fi
fi

# Shut down a previously installed server first
# Note we *could* make that depend on $SERVER_TO_START, but we rather don't,
# so a "stop" is attempted even if there is no PID file.
# (Maybe the "stop" doesn't work then, but we might fix that in itself.)
if [ -x %{_sysconfdir}/init.d/mysql ] ; then
	%{_sysconfdir}/init.d/mysql stop > /dev/null 2>&1
	echo "Giving mysqld 5 seconds to exit nicely"
	sleep 5
fi

%post -n MySQL-server%{package_suffix}
mysql_datadir=%{mysqldatadir}
NEW_VERSION=%{mysql_version}-%{release}
STATUS_FILE=$mysql_datadir/RPM_UPGRADE_MARKER

# ----------------------------------------------------------------------
# Create data directory if needed, check whether upgrade or install
# ----------------------------------------------------------------------
if [ ! -d $mysql_datadir ] ; then mkdir -m 755 $mysql_datadir; fi
if [ -f $STATUS_FILE ] ; then
	SERVER_TO_START=`grep '^SERVER_TO_START=' $STATUS_FILE | cut -c17-`
else
	SERVER_TO_START='true'   # This is for 5.1 only, to not change behavior
fi
# echo "Analyzed: SERVER_TO_START=$SERVER_TO_START"
if [ ! -d $mysql_datadir/mysql ] ; then
	mkdir $mysql_datadir/mysql $mysql_datadir/test
	echo "MySQL RPM installation of version $NEW_VERSION" >> $STATUS_FILE
else
	# If the directory exists, we may assume it is an upgrade.
	echo "MySQL RPM upgrade to version $NEW_VERSION" >> $STATUS_FILE
fi


# ----------------------------------------------------------------------
# Make MySQL start/shutdown automatically when the machine does it.
# ----------------------------------------------------------------------
# NOTE: This still needs to be debated. Should we check whether these links
# for the other run levels exist(ed) before the upgrade?
if [ -x /sbin/chkconfig ] ; then
	/sbin/chkconfig --add mysql
fi

# ----------------------------------------------------------------------
# Create a MySQL user and group. Do not report any problems if it already
# exists.
# ----------------------------------------------------------------------
groupadd -r %{mysqld_group} 2> /dev/null || true
useradd -M -r -d $mysql_datadir -s /bin/bash -c "MySQL server" -g %{mysqld_group} %{mysqld_user} 2> /dev/null || true
# The user may already exist, make sure it has the proper group nevertheless (BUG#12823)
usermod -g %{mysqld_group} %{mysqld_user} 2> /dev/null || true

# ----------------------------------------------------------------------
# Change permissions so that the user that will run the MySQL daemon
# owns all database files.
# ----------------------------------------------------------------------
chown -R %{mysqld_user}:%{mysqld_group} $mysql_datadir

# ----------------------------------------------------------------------
# Initiate databases if needed
# ----------------------------------------------------------------------
if ! grep '^MySQL RPM upgrade' $STATUS_FILE >/dev/null 2>&1 ; then
	# Fix bug#45415: no "mysql_install_db" on an upgrade
	# Do this as a negative to err towards more "install" runs
	# rather than to miss one.
	%{_bindir}/mysql_install_db --rpm --user=%{mysqld_user}
fi

# ----------------------------------------------------------------------
# Upgrade databases if needed would go here - but it cannot be automated yet
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# Change permissions again to fix any new files.
# ----------------------------------------------------------------------
chown -R %{mysqld_user}:%{mysqld_group} $mysql_datadir

# ----------------------------------------------------------------------
# Fix permissions for the permission database so that only the user
# can read them.
# ----------------------------------------------------------------------
chmod -R og-rw $mysql_datadir/mysql

# ----------------------------------------------------------------------
# install SELinux files - but don't override existing ones
# ----------------------------------------------------------------------
SETARGETDIR=/etc/selinux/targeted/src/policy
SEDOMPROG=$SETARGETDIR/domains/program
SECONPROG=$SETARGETDIR/file_contexts/program
if [ -f /etc/redhat-release ] && \
   (grep -q "Red Hat Enterprise Linux .. release 4" /etc/redhat-release \
    || grep -q "CentOS release 4" /etc/redhat-release) ; then
   echo
   echo
   echo 'Notes regarding SELinux on this platform:'
   echo '========================================='
   echo
   echo 'The default policy might cause server startup to fail because it is '
   echo 'not allowed to access critical files. In this case, please update '
   echo 'your installation. '
   echo
   echo 'The default policy might also cause inavailability of SSL related '
   echo 'features because the server is not allowed to access /dev/random '
   echo 'and /dev/urandom. If this is a problem, please do the following: '
   echo
   echo '  1) install selinux-policy-targeted-sources from your OS vendor'
   echo '  2) add the following two lines to '$SEDOMPROG/mysqld.te':'
   echo '       allow mysqld_t random_device_t:chr_file read;'
   echo '       allow mysqld_t urandom_device_t:chr_file read;'
   echo '  3) cd to '$SETARGETDIR' and issue the following command:'
   echo '       make load'
   echo
   echo
fi

if [ -x sbin/restorecon ] ; then
	sbin/restorecon -R var/lib/mysql
fi

# Was the server running before the upgrade? If so, restart the new one.
if [ "$SERVER_TO_START" = "true" ] ; then
	# Restart in the same way that mysqld will be started normally.
	if [ -x %{_sysconfdir}/init.d/mysql ] ; then
		%{_sysconfdir}/init.d/mysql start
		echo "Giving mysqld 2 seconds to start"
		sleep 2
	fi
	
	# Allow mysqld_safe to start mysqld and print a message before we exit
	sleep 2
fi

# Collect an upgrade history ...
echo "Upgrade/install finished at `date`"        >> $STATUS_FILE
echo                                             >> $STATUS_FILE
echo "====="                                     >> $STATUS_FILE
STATUS_HISTORY=$mysql_datadir/RPM_UPGRADE_HISTORY
cat $STATUS_FILE >> $STATUS_HISTORY
rm  $STATUS_FILE

%if %{CLUSTER_BUILD}
%post -n MySQL%{cluster_package_prefix}storage%{package_suffix}
# Create cluster directory if needed
mkdir -p /var/lib/mysql-cluster
%endif

%preun -n MySQL-server%{package_suffix}
if [ $1 = 0 ] ; then
	# Stop MySQL before uninstalling it
	if [ -x %{_sysconfdir}/init.d/mysql ] ; then
		%{_sysconfdir}/init.d/mysql stop > /dev/null
		# Remove autostart of MySQL
		if [ -x /sbin/chkconfig ] ; then
			/sbin/chkconfig --del mysql
		fi
	fi
fi

# We do not remove the mysql user since it may still own a lot of
# database files.

# ----------------------------------------------------------------------
# Clean up the BuildRoot after build is done
# ----------------------------------------------------------------------
%clean
[ "$RPM_BUILD_ROOT" != "/" ] && [ -d $RPM_BUILD_ROOT ] && rm -rf $RPM_BUILD_ROOT;

##############################################################################
#  Files section
##############################################################################

%files -n MySQL-server%{package_suffix}
%defattr(-,root,root,0755)

%doc %{lic_files}
%doc support-files/my-*.cnf
%if %{CLUSTER_BUILD}
%doc support-files/ndb-*.ini
%endif

%doc %attr(644, root, root) %{_infodir}/mysql.info*

%if %{INNODB_BUILD}
%doc %attr(644, root, man) %{_mandir}/man1/innochecksum.1*
%endif
%doc %attr(644, root, man) %{_mandir}/man1/my_print_defaults.1*
%doc %attr(644, root, man) %{_mandir}/man1/myisam_ftdump.1*
%doc %attr(644, root, man) %{_mandir}/man1/myisamchk.1*
%doc %attr(644, root, man) %{_mandir}/man1/myisamlog.1*
%doc %attr(644, root, man) %{_mandir}/man1/myisampack.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_convert_table_format.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_fix_extensions.1*
%doc %attr(644, root, man) %{_mandir}/man8/mysqld.8*
%doc %attr(644, root, man) %{_mandir}/man1/mysqld_multi.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqld_safe.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqldumpslow.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_fix_privilege_tables.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_install_db.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_secure_installation.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_setpermission.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_upgrade.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqlhotcopy.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqlman.1*
%doc %attr(644, root, man) %{_mandir}/man8/mysqlmanager.8*
%doc %attr(644, root, man) %{_mandir}/man1/mysql.server.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqltest.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_tzinfo_to_sql.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_zap.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqlbug.1*
%doc %attr(644, root, man) %{_mandir}/man1/perror.1*
%doc %attr(644, root, man) %{_mandir}/man1/replace.1*
%doc %attr(644, root, man) %{_mandir}/man1/resolve_stack_dump.1*
%doc %attr(644, root, man) %{_mandir}/man1/resolveip.1*

%ghost %config(noreplace,missingok) %{_sysconfdir}/my.cnf
%ghost %config(noreplace,missingok) %{_sysconfdir}/mysqlmanager.passwd

%if %{INNODB_BUILD}
%attr(755, root, root) %{_bindir}/innochecksum
%endif
%attr(755, root, root) %{_bindir}/my_print_defaults
%attr(755, root, root) %{_bindir}/myisam_ftdump
%attr(755, root, root) %{_bindir}/myisamchk
%attr(755, root, root) %{_bindir}/myisamlog
%attr(755, root, root) %{_bindir}/myisampack
%attr(755, root, root) %{_bindir}/mysql_convert_table_format
%attr(755, root, root) %{_bindir}/mysql_fix_extensions
%attr(755, root, root) %{_bindir}/mysql_fix_privilege_tables
%attr(755, root, root) %{_bindir}/mysql_install_db
%attr(755, root, root) %{_bindir}/mysql_secure_installation
%attr(755, root, root) %{_bindir}/mysql_setpermission
%attr(755, root, root) %{_bindir}/mysql_tzinfo_to_sql
%attr(755, root, root) %{_bindir}/mysql_upgrade
%attr(755, root, root) %{_bindir}/mysql_zap
%attr(755, root, root) %{_bindir}/mysqlbug
%attr(755, root, root) %{_bindir}/mysqld_multi
%attr(755, root, root) %{_bindir}/mysqld_safe
%attr(755, root, root) %{_bindir}/mysqldumpslow
%attr(755, root, root) %{_bindir}/mysqlhotcopy
%attr(755, root, root) %{_bindir}/mysqltest
%attr(755, root, root) %{_bindir}/perror
%attr(755, root, root) %{_bindir}/replace
%attr(755, root, root) %{_bindir}/resolve_stack_dump
%attr(755, root, root) %{_bindir}/resolveip

%attr(755, root, root) %{_sbindir}/mysqld
%attr(755, root, root) %{_sbindir}/mysqld-debug
%attr(755, root, root) %{_sbindir}/mysqlmanager
%attr(755, root, root) %{_sbindir}/rcmysql
%attr(644, root, root) %{_libdir}/mysql/mysqld.sym
%attr(644, root, root) %{_libdir}/mysql/mysqld-debug.sym
%if %{INNODB_BUILD}
%if %{WITH_INNODB_PLUGIN}
%attr(755, root, root) %{_libdir}/mysql/plugin/ha_innodb_plugin.so*
%endif
%endif

%attr(644, root, root) %config(noreplace,missingok) %{_sysconfdir}/logrotate.d/mysql
%attr(755, root, root) %{_sysconfdir}/init.d/mysql

%attr(755, root, root) %{_datadir}/mysql/

%files -n MySQL-client%{package_suffix}
%defattr(-, root, root, 0755)
%attr(755, root, root) %{_bindir}/msql2mysql
%attr(755, root, root) %{_bindir}/mysql
%attr(755, root, root) %{_bindir}/mysql_find_rows
%attr(755, root, root) %{_bindir}/mysql_waitpid
%attr(755, root, root) %{_bindir}/mysqlaccess
%attr(755, root, root) %{_bindir}/mysqladmin
%attr(755, root, root) %{_bindir}/mysqlbinlog
%attr(755, root, root) %{_bindir}/mysqlcheck
%attr(755, root, root) %{_bindir}/mysqldump
%attr(755, root, root) %{_bindir}/mysqlimport
%attr(755, root, root) %{_bindir}/mysqlshow
%attr(755, root, root) %{_bindir}/mysqlslap

%doc %attr(644, root, man) %{_mandir}/man1/msql2mysql.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_find_rows.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_waitpid.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqlaccess.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqladmin.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqlbinlog.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqlcheck.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqldump.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqlimport.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqlshow.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqlslap.1*

%post -n MySQL-shared%{package_suffix}
/sbin/ldconfig

%postun -n MySQL-shared%{package_suffix}
/sbin/ldconfig

%if %{CLUSTER_BUILD}
%files -n MySQL%{cluster_package_prefix}storage%{package_suffix}
%defattr(-,root,root,0755)
%attr(755, root, root) %{_sbindir}/ndbd
%doc %attr(644, root, man) %{_mandir}/man8/ndbd.8*

%files -n MySQL%{cluster_package_prefix}management%{package_suffix}
%defattr(-,root,root,0755)
%attr(755, root, root) %{_sbindir}/ndb_mgmd
%doc %attr(644, root, man) %{_mandir}/man8/ndb_mgmd.8*

%files -n MySQL%{cluster_package_prefix}tools%{package_suffix}
%defattr(-,root,root,0755)
%attr(755, root, root) %{_bindir}/ndb_config
%attr(755, root, root) %{_bindir}/ndb_desc
%attr(755, root, root) %{_bindir}/ndb_error_reporter
%attr(755, root, root) %{_bindir}/ndb_mgm
%attr(755, root, root) %{_bindir}/ndb_restore
%attr(755, root, root) %{_bindir}/ndb_select_all
%attr(755, root, root) %{_bindir}/ndb_select_count
%attr(755, root, root) %{_bindir}/ndb_show_tables
%attr(755, root, root) %{_bindir}/ndb_size.pl
%attr(755, root, root) %{_bindir}/ndb_test_platform
%attr(755, root, root) %{_bindir}/ndb_waiter
%doc %attr(644, root, man) %{_mandir}/man1/ndb_config.1*
%doc %attr(644, root, man) %{_mandir}/man1/ndb_desc.1*
%doc %attr(644, root, man) %{_mandir}/man1/ndb_error_reporter.1*
%doc %attr(644, root, man) %{_mandir}/man1/ndb_mgm.1*
%doc %attr(644, root, man) %{_mandir}/man1/ndb_restore.1*
%doc %attr(644, root, man) %{_mandir}/man1/ndb_select_all.1*
%doc %attr(644, root, man) %{_mandir}/man1/ndb_select_count.1*
%doc %attr(644, root, man) %{_mandir}/man1/ndb_show_tables.1*
%doc %attr(644, root, man) %{_mandir}/man1/ndb_size.pl.1*
%doc %attr(644, root, man) %{_mandir}/man1/ndb_waiter.1*

%files -n MySQL%{cluster_package_prefix}extra%{package_suffix}
%defattr(-,root,root,0755)
%attr(755, root, root) %{_bindir}/ndb_delete_all
%attr(755, root, root) %{_bindir}/ndb_drop_index
%attr(755, root, root) %{_bindir}/ndb_drop_table
%attr(755, root, root) %{_sbindir}/ndb_cpcd
%doc %attr(644, root, man) %{_mandir}/man1/ndb_delete_all.1*
%doc %attr(644, root, man) %{_mandir}/man1/ndb_drop_index.1*
%doc %attr(644, root, man) %{_mandir}/man1/ndb_drop_table.1*
%doc %attr(644, root, man) %{_mandir}/man1/ndb_cpcd.1*
%endif

%files -n MySQL-devel%{package_suffix} -f optional-files-devel
%defattr(-, root, root, 0755)
%doc %attr(644, root, man) %{_mandir}/man1/comp_err.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql_config.1*
%attr(755, root, root) %{_bindir}/mysql_config
%dir %attr(755, root, root) %{_libdir}/mysql
%{_includedir}/mysql
%{_datadir}/aclocal/mysql.m4
%{_libdir}/mysql/libdbug.a
%{_libdir}/mysql/libheap.a
%{_libdir}/mysql/libmyisam.a
%{_libdir}/mysql/libmyisammrg.a
%{_libdir}/mysql/libmysqlclient.a
%{_libdir}/mysql/libmysqlclient.la
%{_libdir}/mysql/libmysqlclient_r.a
%{_libdir}/mysql/libmysqlclient_r.la
%{_libdir}/mysql/libmystrings.a
%{_libdir}/mysql/libmysys.a
%if %{CLUSTER_BUILD}
%{_libdir}/mysql/libndbclient.a
%{_libdir}/mysql/libndbclient.la
%endif
%{_libdir}/mysql/libvio.a
%{_libdir}/mysql/libz.a
%{_libdir}/mysql/libz.la
%if %{INNODB_BUILD}
%if %{WITH_INNODB_PLUGIN}
%{_libdir}/mysql/plugin/ha_innodb_plugin.a
%{_libdir}/mysql/plugin/ha_innodb_plugin.la
%endif
%endif

%files -n MySQL-shared%{package_suffix}
%defattr(-, root, root, 0755)
# Shared libraries (omit for architectures that don't support them)
%{_libdir}/*.so*

%files -n MySQL-test%{package_suffix}
%defattr(-, root, root, 0755)
%{_datadir}/mysql-test
%attr(755, root, root) %{_bindir}/mysql_client_test
%doc %attr(644, root, man) %{_mandir}/man1/mysql_client_test.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql-stress-test.pl.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysql-test-run.pl.1*
%if %{EMBEDDED_BUILD}
%attr(755, root, root) %{_bindir}/mysql_client_test_embedded
%attr(755, root, root) %{_bindir}/mysqltest_embedded
%doc %attr(644, root, man) %{_mandir}/man1/mysql_client_test_embedded.1*
%doc %attr(644, root, man) %{_mandir}/man1/mysqltest_embedded.1*
%endif

%if %{EMBEDDED_BUILD}
%files -n MySQL-embedded%{package_suffix}
%defattr(-, root, root, 0755)
%attr(644, root, root) %{_libdir}/mysql/libmysqld.a
%attr(644, root, root) %{_libdir}/mysql/libmysqld-debug.a
%endif

##############################################################################
# The spec file changelog only includes changes made to the spec file
# itself - note that they must be ordered by date (important when
# merging BK trees)
##############################################################################
%changelog
* Thu Jul 07 2011 Joerg Bruehe <joerg.bruehe@oracle.com>>

- Fix bug#45415: "rpm upgrade recreates test database"
  Let the creation of the "test" database happen only during a new installation,
  not in an RPM upgrade.
  This affects both the "mkdir" and the call of "mysql_install_db".

* Tue Dec 14 2010 Kent Boortz <kent.boortz@oracle.com>

- Removed EXCEPTIONS-CLIENT

* Thu Jul 29 2010 Kent Boortz <kent.boortz@sun.com>

- Merged in code from the MySQL Server 5.5 spec file, that corrects
  the handling of "libmygcc.a"

- Corrected problem that the "lib/mysql/plugin" directory might be
  empty, making the copy of plugins fail

* Tue Jun 15 2010 Joerg Bruehe <joerg.bruehe@sun.com>

- Change the behaviour on upgrade:
  *Iff* the server was stopped before the upgrade is started, this is taken as a
  sign the administrator is handling that manually, and so the new server will
  not be started automatically at the end of the upgrade.
  The start/stop scripts will still be installed, so the server will be started
  on the next machine boot.
  This is the 5.1 version of fixing bug#27072 (RPM autostarting the server).

* Thu May 02 2010 Kent Boortz <kent.boortz@sun.com>

- Removed the Example storage engine, it is not to be in products

* Fri Apr 02 2010 Joerg Bruehe <joerg.bruehe@sun.com>

- "percent define" must not be used in the Changelog section.

* Mon Mar 01 2010 Joerg Bruehe <joerg.bruehe@sun.com>

- Set "Oracle and/or its affiliates" as the vendor and copyright owner,
  accept upgrading from packages showing MySQL or Sun as vendor.
- Fix a shell syntax error: "define" is not executable, add a ":" statement.

* Fri Feb 05 2010 Joerg Bruehe <joerg.bruehe@sun.com>

- Formatting changes:
  Have a consistent structure of separator lines and of indentation
  (8 leading blanks => tab).
- Some other cleanup to bring "specific" and "generic" spec files
  better in sync, as written in bug#33248.
- Remove handling the "maria" engine, that is too far off.
- Make "--with-zlib-dir=bundled" the default, add an option to disable it.
- Improve the runtime check for "libgcc.a", protect it against being tried
  with the Intel compiler "icc".
- Alignment with generic: ensure some C++ flags.

* Fri Aug 21 2009 Jonathan Perkin <jperkin@sun.com>

- Install innodb_plugin.
- Correctly package missing libraries.
- Disable the libdaemon_example and ftexample plugins.

* Thu Jul 30 2009 Joerg Bruehe <joerg.bruehe@sun.com>

- Add the "old vendor" (= "MySQL AB") and expand the upgrade check
  so that "MySQL" packages can be upgraded by "Sun" ones.
  This fixes bug#45534, with its duplicates #42953 and #46174.

* Tue Mar 31 2009 Joerg Bruehe <joerg@mysql.com>

- Differ between commercial sources with and without InnoDB.

* Mon Jan 12 2009 Jonathan Perkin <jperkin@sun.com>

- Support MYSQL_BUILD_* variables.

* Fri Nov 07 2008 Joerg Bruehe <joerg@mysql.com>

- Modify CFLAGS and CXXFLAGS such that a debug build is not optimized.
  This should cover both gcc and icc flags.  Fixes bug#40546.

* Mon Aug 18 2008 Joerg Bruehe <joerg@mysql.com>

- Get rid of the "warning: Installed (but unpackaged) file(s) found:"
  Some generated files aren't needed in RPMs:
  - the "sql-bench/" subdirectory
  Some files were missing:
  - /usr/share/aclocal/mysql.m4  ("devel" subpackage)
  - Manuals for embedded tests   ("test" subpackage)
  - Manual "mysqlbug" ("server" subpackage)
  - Manual "mysql_find_rows" ("client" subpackage)

* Wed Jun 11 2008 Kent Boortz <kent@mysql.com>

- Removed the Example storage engine, it is not to be in products

* Fri Apr 04 2008 Daniel Fischer <df@mysql.com>

- Added Cluster+InnoDB product

* Mon Mar 31 2008 Kent Boortz <kent@mysql.com>

- Made the "Federated" storage engine an option

* Tue Mar 11 2008 Joerg Bruehe <joerg@mysql.com>

- Cleanup: Remove manual file "mysql_tableinfo.1".

* Mon Feb 18 2008 Timothy Smith <tim@mysql.com>

- Require a manual upgrade if the alread-installed mysql-server is
  from another vendor, or is of a different major version.

* Fri Dec 14 2007 Joerg Bruehe <joerg@mysql.com>

- Add the "%doc" directive for all man pages and other documentation;
  also, some re-ordering to reduce differences between spec files.

* Fri Dec 14 2007 Joerg Bruehe <joerg@mysql.com>

- Added "client/mysqlslap" (bug#32077)

* Wed Oct 31 2007 Joerg Bruehe <joerg@mysql.com>

- Explicitly handle InnoDB using its own variable and "--with"/"--without"
  options, because the "configure" default is "yes".
  Also, fix the specification of "community" to include "partitioning".

* Mon Sep 03 2007 Kent Boortz <kent@mysql.com>

- Let libmygcc be included unless "--without libgcc" is given.

* Sun Sep 02 2007 Kent Boortz <kent@mysql.com>

- Changed SSL flag given to configure to "--with-ssl"
- Removed symbolic link "safe_mysqld"
- Removed script and man page for "mysql_explain_log"
- Removed scripts "mysql_tableinfo" and "mysql_upgrade_shell"
- Removed "comp_err" from list to install
- Removed duplicates of "libndbclient.a" and "libndbclient.la"

* Tue Jul 17 2007 Joerg Bruehe <joerg@mysql.com>

- Add the man page for "mysql-stress-test.pl" to the "test" RPM
  (consistency in fixing bug#21023, the script is handled by "Makefile.am")

* Wed Jul 11 2007 Daniel Fischer <df@mysql.com>

- Change the way broken SELinux policies on RHEL4 and CentOS 4
  are handled to be more likely to actually work

* Thu Jun 05 2007 kent Boortz <kent@mysql.com>

- Enabled the CSV engine in all builds

* Thu May  3 2007 Mads Martin Joergensen <mmj@mysql.com>

- Spring cleanup

* Thu Apr 19 2007 Mads Martin Joergensen <mmj@mysql.com>

- If sbin/restorecon exists then run it

* Wed Apr 18 2007 Kent Boortz <kent@mysql.com>

- Packed unpacked files

   /usr/sbin/ndb_cpcd
   /usr/bin/mysql_upgrade_shell
   /usr/bin/innochecksum
   /usr/share/man/man1/ndb_cpcd.1.gz
   /usr/share/man/man1/innochecksum.1.gz
   /usr/share/man/man1/mysql_fix_extensions.1.gz
   /usr/share/man/man1/mysql_secure_installation.1.gz
   /usr/share/man/man1/mysql_tableinfo.1.gz
   /usr/share/man/man1/mysql_waitpid.1.gz

- Commands currently not installed but that has man pages

   /usr/share/man/man1/make_win_bin_dist.1.gz
   /usr/share/man/man1/make_win_src_distribution.1.gz
   /usr/share/man/man1/mysql-stress-test.pl.1.gz
   /usr/share/man/man1/ndb_print_backup_file.1.gz
   /usr/share/man/man1/ndb_print_schema_file.1.gz
   /usr/share/man/man1/ndb_print_sys_file.1.gz

* Thu Mar 22 2007 Joerg Bruehe <joerg@mysql.com>

- Add "comment" options to the test runs, for better log analysis.

* Wed Mar 21 2007 Joerg Bruehe <joerg@mysql.com>

- Add even more man pages.

* Fri Mar 16 2007 Joerg Bruehe <joerg@mysql.com>

- Build the server twice, once as "mysqld-debug" and once as "mysqld";
  test them both, and include them in the resulting file.
- Consequences of the fix for bug#20166:
  Remove "mysql_create_system_tables",
  new "mysql_fix_privilege_tables.sql" is included implicitly.

* Wed Mar 14 2007 Daniel Fischer <df@mysql.com>

- Adjust compile options some more and change naming of community
  cluster RPMs to explicitly say 'cluster'.

* Mon Mar 12 2007 Daniel Fischer <df@mysql.com>

- Adjust compile options and other settings for 5.0 community builds.

* Fri Mar 02 2007 Joerg Bruehe <joerg@mysql.com>

- Add several man pages which are now created.

* Mon Jan 29 2007 Mads Martin Joergensen <mmj@mysql.com>

- Make sure SELinux works correctly. Files from Colin Charles.

* Fri Jan 05 2007 Kent Boortz <kent@mysql.com>

- Add CFLAGS to gcc call with --print-libgcc-file, to make sure the
  correct "libgcc.a" path is returned for the 32/64 bit architecture.

* Tue Dec 19 2006 Joerg Bruehe <joerg@mysql.com>

- The man page for "mysqld" is now in section 8.

* Thu Dec 14 2006 Joerg Bruehe <joerg@mysql.com>

- Include the new man pages for "my_print_defaults" and "mysql_tzinfo_to_sql"
  in the server RPM.
- The "mysqlmanager" man page was relocated to section 8, reflect that.

* Fri Nov 17 2006 Mads Martin Joergensen <mmj@mysql.com>

- Really fix obsoletes/provides for community -> this
- Make it possible to not run test by setting
  MYSQL_RPMBUILD_TEST to "no"

* Wed Nov 15 2006 Joerg Bruehe <joerg@mysql.com>

- Switch from "make test*" to explicit calls of the test suite,
  so that "report features" can be used.

* Wed Nov 15 2006 Kent Boortz <kent@mysql.com>

- Added "--with cluster" and "--define cluster{_gpl}"

* Tue Oct 24 2006 Mads Martin Joergensen <mmj@mysql.com>

- Shared need to Provide/Obsolete mysql-shared

* Mon Oct 23 2006 Mads Martin Joergensen <mmj@mysql.com>

- Run sbin/restorecon after db init (Bug#12676)

* Thu Jul 06 2006 Joerg Bruehe <joerg@mysql.com>

- Correct a typing error in my previous change.

* Tue Jul 04 2006 Joerg Bruehe <joerg@mysql.com>

- Use the Perl script to run the tests, because it will automatically check
  whether the server is configured with SSL.

* Wed Jun 28 2006 Joerg Bruehe <joerg@mysql.com>

- Revert all previous attempts to call "mysql_upgrade" during RPM upgrade,
  there are some more aspects which need to be solved before this is possible.
  For now, just ensure the binary "mysql_upgrade" is delivered and installed.

* Wed Jun 28 2006 Joerg Bruehe <joerg@mysql.com>

- Move "mysqldumpslow" from the client RPM to the server RPM (bug#20216).

* Wed Jun 21 2006 Joerg Bruehe <joerg@mysql.com>

- To run "mysql_upgrade", we need a running server;
  start it in isolation and skip password checks.

* Sat May 23 2006 Kent Boortz <kent@mysql.com>

- Always compile for PIC, position independent code.

* Fri Apr 28 2006 Kent Boortz <kent@mysql.com>

- Install and run "mysql_upgrade"

* Sat Apr 01 2006 Kent Boortz <kent@mysql.com>

- Allow to override $LDFLAGS

* Fri Jan 06 2006 Lenz Grimmer <lenz@mysql.com>

- added a MySQL-test subpackage (BUG#16070)

* Tue Dec 27 2005 Joerg Bruehe <joerg@mysql.com>

- Some minor alignment with the 4.1 version

* Wed Dec 14 2005 Rodrigo Novo <rodrigo@mysql.com>

- Cosmetic changes: source code location & rpm packager
- Protect "nm -D" against libtool weirdness
- Add libz.a & libz.la to the list of files for subpackage -devel
- moved --with-zlib-dir=bundled out of BuildMySQL, as it doesn't makes
  sense for the shared package

* Tue Nov 22 2005 Joerg Bruehe <joerg@mysql.com>

- Extend the file existence check for "init.d/mysql" on un-install
  to also guard the call to "insserv"/"chkconfig".

* Wed Nov 16 2005 Lenz Grimmer <lenz@mysql.com>

- added mysql_client_test to the "client" subpackage (BUG#14546)

* Tue Nov 15 2005 Lenz Grimmer <lenz@mysql.com>

- changed default definitions to build a standard GPL release when not
  defining anything else
- install the shared libs more elegantly by using "make install"

* Wed Oct 19 2005 Kent Boortz <kent@mysql.com>

- Made yaSSL support an option (off by default)

* Wed Oct 19 2005 Kent Boortz <kent@mysql.com>

- Enabled yaSSL support

* Thu Oct 13 2005 Lenz Grimmer <lenz@mysql.com>

- added a usermod call to assign a potential existing mysql user to the
  correct user group (BUG#12823)
- added a separate macro "mysqld_group" to be able to define the
  user group of the mysql user seperately, if desired.

* Fri Oct 1 2005 Kent Boortz <kent@mysql.com>

- Copy the config.log file to location outside
  the build tree

* Fri Sep 30 2005 Lenz Grimmer <lenz@mysql.com>

- don't use install-strip to install the binaries (strip segfaults on
  icc-compiled binaries on IA64)

* Thu Sep 22 2005 Lenz Grimmer <lenz@mysql.com>

- allow overriding the CFLAGS (needed for Intel icc compiles)
- replace the CPPFLAGS=-DBIG_TABLES with "--with-big-tables" configure option

* Fri Aug 19 2005 Joerg Bruehe <joerg@mysql.com>

- Protect against failing tests.

* Thu Aug 04 2005 Lenz Grimmer <lenz@mysql.com>

- Fixed the creation of the mysql user group account in the postinstall
  section (BUG 12348)

* Fri Jul 29 2005 Lenz Grimmer <lenz@mysql.com>

- Fixed external RPM Requirements to better suit the target distribution
  (BUG 12233)

* Fri Jul 15 2005 Lenz Grimmer <lenz@mysql.com>

- create a "mysql" user group and assign the mysql user account to that group
  in the server postinstall section. (BUG 10984)

* Wed Jun 01 2005 Lenz Grimmer <lenz@mysql.com>

- use "mysqldatadir" variable instead of hard-coding the path multiple times
- use the "mysqld_user" variable on all occasions a user name is referenced
- removed (incomplete) Brazilian translations
- removed redundant release tags from the subpackage descriptions

* Fri May 27 2005 Lenz Grimmer <lenz@mysql.com>

- fixed file list (removed libnisam.a and libmerge.a from the devel subpackage)
- force running the test suite

* Wed Apr 20 2005 Lenz Grimmer <lenz@mysql.com>

- Enabled the "blackhole" storage engine for the Max RPM

* Wed Apr 13 2005 Lenz Grimmer <lenz@mysql.com>

- removed the MySQL manual files (html/ps/texi) - they have been removed
  from the MySQL sources and are now available seperately.

* Mon Apr 4 2005 Petr Chardin <petr@mysql.com>

- old mysqlmanager, mysqlmanagerc and mysqlmanager-pwger renamed into
  mysqltestmanager, mysqltestmanager and mysqltestmanager-pwgen respectively

* Fri Mar 18 2005 Lenz Grimmer <lenz@mysql.com>

- Disabled RAID in the Max binaries once and for all (it has finally been
  removed from the source tree)

* Sun Feb 20 2005 Petr Chardin <petr@mysql.com>

- Install MySQL Instance Manager together with mysqld, touch mysqlmanager
  password file

* Mon Feb 14 2005 Lenz Grimmer <lenz@mysql.com>

- Fixed the compilation comments and moved them into the separate build sections
  for Max and Standard

* Mon Feb 7 2005 Tomas Ulin <tomas@mysql.com>

- enabled the "Ndbcluster" storage engine for the max binary
- added extra make install in ndb subdir after Max build to get ndb binaries
- added packages for ndbcluster storage engine

* Fri Jan 14 2005 Lenz Grimmer <lenz@mysql.com>

- replaced obsoleted "BuildPrereq" with "BuildRequires" instead

* Thu Jan 13 2005 Lenz Grimmer <lenz@mysql.com>

- enabled the "Federated" storage engine for the max binary

* Tue Jan 04 2005 Petr Chardin <petr@mysql.com>

- ISAM and merge storage engines were purged. As well as appropriate
  tools and manpages (isamchk and isamlog)

* Thu Dec 31 2004 Lenz Grimmer <lenz@mysql.com>

- enabled the "Archive" storage engine for the max binary
- enabled the "CSV" storage engine for the max binary
- enabled the "Example" storage engine for the max binary

* Thu Aug 26 2004 Lenz Grimmer <lenz@mysql.com>

- MySQL-Max now requires MySQL-server instead of MySQL (BUG 3860)

* Fri Aug 20 2004 Lenz Grimmer <lenz@mysql.com>

- do not link statically on IA64/AMD64 as these systems do not have
  a patched glibc installed

* Tue Aug 10 2004 Lenz Grimmer <lenz@mysql.com>

- Added libmygcc.a to the devel subpackage (required to link applications
  against the the embedded server libmysqld.a) (BUG 4921)

* Mon Aug 09 2004 Lenz Grimmer <lenz@mysql.com>

- Added EXCEPTIONS-CLIENT to the "devel" package

* Thu Jul 29 2004 Lenz Grimmer <lenz@mysql.com>

- disabled OpenSSL in the Max binaries again (the RPM packages were the
  only exception to this anyway) (BUG 1043)

* Wed Jun 30 2004 Lenz Grimmer <lenz@mysql.com>

- fixed server postinstall (mysql_install_db was called with the wrong
  parameter)

* Thu Jun 24 2004 Lenz Grimmer <lenz@mysql.com>

- added mysql_tzinfo_to_sql to the server subpackage
- run "make clean" instead of "make distclean"

* Mon Apr 05 2004 Lenz Grimmer <lenz@mysql.com>

- added ncurses-devel to the build prerequisites (BUG 3377)

* Thu Feb 12 2004 Lenz Grimmer <lenz@mysql.com>

- when using gcc, _always_ use CXX=gcc
- replaced Copyright with License field (Copyright is obsolete)

* Tue Feb 03 2004 Lenz Grimmer <lenz@mysql.com>

- added myisam_ftdump to the Server package

* Tue Jan 13 2004 Lenz Grimmer <lenz@mysql.com>

- link the mysql client against libreadline instead of libedit (BUG 2289)

* Mon Dec 22 2003 Lenz Grimmer <lenz@mysql.com>

- marked /etc/logrotate.d/mysql as a config file (BUG 2156)

* Fri Dec 13 2003 Lenz Grimmer <lenz@mysql.com>

- fixed file permissions (BUG 1672)

* Thu Dec 11 2003 Lenz Grimmer <lenz@mysql.com>

- made testing for gcc3 a bit more robust

* Fri Dec 05 2003 Lenz Grimmer <lenz@mysql.com>

- added missing file mysql_create_system_tables to the server subpackage

* Fri Nov 21 2003 Lenz Grimmer <lenz@mysql.com>

- removed dependency on MySQL-client from the MySQL-devel subpackage
  as it is not really required. (BUG 1610)

* Fri Aug 29 2003 Lenz Grimmer <lenz@mysql.com>

- Fixed BUG 1162 (removed macro names from the changelog)
- Really fixed BUG 998 (disable the checking for installed but
  unpackaged files)

* Tue Aug 05 2003 Lenz Grimmer <lenz@mysql.com>

- Fixed BUG 959 (libmysqld not being compiled properly)
- Fixed BUG 998 (RPM build errors): added missing files to the
  distribution (mysql_fix_extensions, mysql_tableinfo, mysqldumpslow,
  mysql_fix_privilege_tables.1), removed "-n" from install section.

* Wed Jul 09 2003 Lenz Grimmer <lenz@mysql.com>

- removed the GIF Icon (file was not included in the sources anyway)
- removed unused variable shared_lib_version
- do not run automake before building the standard binary
  (should not be necessary)
- add server suffix '-standard' to standard binary (to be in line
  with the binary tarball distributions)
- Use more RPM macros (_exec_prefix, _sbindir, _libdir, _sysconfdir,
  _datadir, _includedir) throughout the spec file.
- allow overriding CC and CXX (required when building with other compilers)

* Fri May 16 2003 Lenz Grimmer <lenz@mysql.com>

- re-enabled RAID again

* Wed Apr 30 2003 Lenz Grimmer <lenz@mysql.com>

- disabled MyISAM RAID (--with-raid) - it throws an assertion which
  needs to be investigated first.

* Mon Mar 10 2003 Lenz Grimmer <lenz@mysql.com>

- added missing file mysql_secure_installation to server subpackage
  (BUG 141)

* Tue Feb 11 2003 Lenz Grimmer <lenz@mysql.com>

- re-added missing pre- and post(un)install scripts to server subpackage
- added config file /etc/my.cnf to the file list (just for completeness)
- make sure to create the datadir with 755 permissions

* Mon Jan 27 2003 Lenz Grimmer <lenz@mysql.com>

- removed unused CC and CXX variables
- CFLAGS and CXXFLAGS should honor RPM_OPT_FLAGS

* Fri Jan 24 2003 Lenz Grimmer <lenz@mysql.com>

- renamed package "MySQL" to "MySQL-server"
- fixed Copyright tag
- added mysql_waitpid to client subpackage (required for mysql-test-run)

* Wed Nov 27 2002 Lenz Grimmer <lenz@mysql.com>

- moved init script from /etc/rc.d/init.d to /etc/init.d (the majority of
  Linux distributions now support this scheme as proposed by the LSB either
  directly or via a compatibility symlink)
- Use new "restart" init script action instead of starting and stopping
  separately
- Be more flexible in activating the automatic bootup - use insserv (on
  older SuSE versions) or chkconfig (Red Hat, newer SuSE versions and
  others) to create the respective symlinks

* Wed Sep 25 2002 Lenz Grimmer <lenz@mysql.com>

- MySQL-Max now requires MySQL >= 4.0 to avoid version mismatches
  (mixing 3.23 and 4.0 packages)

* Fri Aug 09 2002 Lenz Grimmer <lenz@mysql.com>

- Turn off OpenSSL in MySQL-Max for now until it works properly again
- enable RAID for the Max binary instead
- added compatibility link: safe_mysqld -> mysqld_safe to ease the
  transition from 3.23

* Thu Jul 18 2002 Lenz Grimmer <lenz@mysql.com>

- Reworked the build steps a little bit: the Max binary is supposed
  to include OpenSSL, which cannot be linked statically, thus trying
	to statically link against a special glibc is futile anyway
- because of this, it is not required to make yet another build run
  just to compile the shared libs (saves a lot of time)
- updated package description of the Max subpackage
- clean up the BuildRoot directory afterwards

* Mon Jul 15 2002 Lenz Grimmer <lenz@mysql.com>

- Updated Packager information
- Fixed the build options: the regular package is supposed to
  include InnoDB and linked statically, while the Max package
	should include BDB and SSL support

* Fri May 03 2002 Lenz Grimmer <lenz@mysql.com>

- Use more RPM macros (e.g. infodir, mandir) to make the spec
  file more portable
- reorganized the installation of documentation files: let RPM
  take care of this
- reorganized the file list: actually install man pages along
  with the binaries of the respective subpackage
- do not include libmysqld.a in the devel subpackage as well, if we
  have a special "embedded" subpackage
- reworked the package descriptions

* Mon Oct  8 2001 Monty

- Added embedded server as a separate RPM

* Fri Apr 13 2001 Monty

- Added mysqld-max to the distribution

* Tue Jan 2  2001  Monty

- Added mysql-test to the bench package

* Fri Aug 18 2000 Tim Smith <tim@mysql.com>

- Added separate libmysql_r directory; now both a threaded
  and non-threaded library is shipped.

* Wed Sep 28 1999 David Axmark <davida@mysql.com>

- Added the support-files/my-example.cnf to the docs directory.

- Removed devel dependency on base since it is about client
  development.

* Wed Sep 8 1999 David Axmark <davida@mysql.com>

- Cleaned up some for 3.23.

* Thu Jul 1 1999 David Axmark <davida@mysql.com>

- Added support for shared libraries in a separate sub
  package. Original fix by David Fox (dsfox@cogsci.ucsd.edu)

- The --enable-assembler switch is now automatically disables on
  platforms there assembler code is unavailable. This should allow
  building this RPM on non i386 systems.

* Mon Feb 22 1999 David Axmark <david@detron.se>

- Removed unportable cc switches from the spec file. The defaults can
  now be overridden with environment variables. This feature is used
  to compile the official RPM with optimal (but compiler version
  specific) switches.

- Removed the repetitive description parts for the sub rpms. Maybe add
  again if RPM gets a multiline macro capability.

- Added support for a pt_BR translation. Translation contributed by
  Jorge Godoy <jorge@bestway.com.br>.

* Wed Nov 4 1998 David Axmark <david@detron.se>

- A lot of changes in all the rpm and install scripts. This may even
  be a working RPM :-)

* Sun Aug 16 1998 David Axmark <david@detron.se>

- A developers changelog for MySQL is available in the source RPM. And
  there is a history of major user visible changed in the Reference
  Manual.  Only RPM specific changes will be documented here.
