#!/bin/bash
#######################################################################
#    MySQL + Tcmalloc
#    
#    Author by : Daniel zhu
#    2011-11-16
#
#    If  you already complied mysql in /usr/local/mysql/ 
#    just install libwind and google-prefrmonce-tools
#   
#    my.cnf need to copy from mysql dir
#
#  全新安装MYSQL+TCMALLOC 脚本可直接执行
#  根据需求选择mysqld_mutli或者mysqld
#  拷贝 my.cnf 或mysqld 启动MYSQL
#   若不添加Tcmalloc则删除--with-mysqld-ldflags=-ltcmalloc_minimal \ 参数
#########################################################################




#for libwind


wget http://download.savannah.gnu.org/releases/libunwind/libunwind-0.99.tar.gz


tar zxvf libunwind-0.99.tar.gz


cd libunwind-0.99


CXX=gcc \
CHOST="x86_64-pc-linux-gnu" \
CFLAGS="-O3 \
-fomit-frame-pointer \
-pipe \
-march=nocona \
-mfpmath=sse \
-m128bit-long-double \
-mmmx \
-msse \
-msse2 \
-maccumulate-outgoing-args \
-m64 \
-ftree-loop-linear \
-fprefetch-loop-arrays \
-freg-struct-return \
-fgcse-sm \
-fgcse-las \
-frename-registers \
-fforce-addr \
-fivopts \
-ftree-vectorize \
-ftracer \
-frename-registers \
-minline-all-stringops \
-fbranch-target-load-optimize2" \
CXXFLAGS="${CFLAGS}" \
./configure && make && make install


cd ..


#for google-prefrmonce-tools


wget http://google-perftools.googlecode.com/files/google-perftools-1.8.3.tar.gz
tar zxvf google-perftools-1.8.3.tar.gz
cd google-perftools-1.8.3
#CXX=gcc \
CHOST="x86_64-pc-linux-gnu" \
CFLAGS="-O3 \
-lstdc++ \
-fomit-frame-pointer \
-pipe \
-march=nocona \
-mfpmath=sse \
-m128bit-long-double \
-mmmx \
-msse \
-msse2 \
-maccumulate-outgoing-args \
-m64 \
-ftree-loop-linear \
-fprefetch-loop-arrays \
-freg-struct-return \
-fgcse-sm \
-fgcse-las \
-frename-registers \
-fforce-addr \
-fivopts \
-ftree-vectorize \
-ftracer \
-frename-registers \
-minline-all-stringops \
-fbranch-target-load-optimize2" \
CXXFLAGS="${CFLAGS}" \
./configure \
--disable-heap-profiler \
--disable-heap-checker \
--disable-debugalloc \
--enable-minimal \
--enable-frame-pointers && make && make install


echo "/usr/local/lib" > /etc/ld.so.conf.d/usr_local_lib.conf
/sbin/ldconfig


#for MySQL


cd ..
wget http://mirrors.sohu.com/mysql/MySQL-5.1/mysql-5.1.59.tar.gz
tar -zxvf mysql-5.1.59.tar.gz
cd mysql-5.1.59


CXX=gcc \
CHOST="x86_64-pc-linux-gnu" \
CFLAGS="-O3 \
-fomit-frame-pointer \
-pipe \
-march=nocona \
-mfpmath=sse \
-m128bit-long-double \
-mmmx \
-msse \
-msse2 \
-maccumulate-outgoing-args \
-m64 \
-ftree-loop-linear \
-fprefetch-loop-arrays \
-freg-struct-return \
-fgcse-sm \
-fgcse-las \
-frename-registers \
-fforce-addr \
-fivopts \
-ftree-vectorize \
-ftracer \
-frename-registers \
-minline-all-stringops \
-felide-constructors \
-fno-exceptions \
-fno-rtti \
-fbranch-target-load-optimize2" \
CXXFLAGS="${CFLAGS}" \
./configure --prefix=/usr/local/mysql \
--with-server-suffix=" - ShopEX-MySQL" \
--with-mysqld-user=mysql \
--with-plugins=partition,blackhole,csv,heap,innobase,myisam,myisammrg \
--with-charset=utf8 \
--with-collation=utf8_general_ci \
--with-extra-charsets=all \
--with-big-tables \
--with-fast-mutexes \
--with-zlib-dir=bundled \
--enable-assembler \
--enable-profiling \
--enable-local-infile \
--enable-thread-safe-client \
--with-readline \
--with-pthread \
--with-embedded-server \
--with-client-ldflags=-all-static \
--with-mysqld-ldflags=-all-static \
--with-mysqld-ldflags=-ltcmalloc_minimal \
--without-geometry \
--without-debug \
--without-ndb-debug


make  && make install




mkdir -p /usr/local/mysql/data


useradd mysql
chown -R mysql.mysql /usr/local/mysql/


/usr/local/mysql/bin/mysql_install_db --basedir=/usr/local/mysql --datadir=/usr/local/mysql/data --user=mysql


echo "PATH=\"/usr/local/mysql/bin:/data/bin/:\$PATH\"" >> /etc/profile && export PATH="/usr/local/mysql/bin:/data/bin/:$PATH"
source /etc/profile
echo   -e /usr/local/mysql/lib/mysql "\n"/usr/local/lib >>/etc/ld.so.conf
ldconfig