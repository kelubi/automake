#!/bin/bash
#

DESCRIPTION="Nginx a web server suitable from shopex ecos"
HOMEPAGE="http://nginx.org/"
#SRC_URI="http://mirrors.dev.shopex.cn/lnmpp/sources/nginx-0.8.41.tar.gz"
SRC_URI="http://lnmpp.googlecode.com/files/nginx-1.0.5.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="nginx"
V="1.0.5"

if [ ! -d /opt/install ]; then
    mkdir -pv /opt/install
fi
echo "go to working dir"
cd /opt/install

if [ -s $PKG_NAME ]; then
  echo "$PKG_NAME [found]"
else
  echo "Error: $PKG_NAME not found!!!download now......"
  wget  $SRC_URI
fi


#init 

echo "init $N-$V$R build script..."
#add web server running user
id www > /dev/null 2>&1
if [ $? -ne 0 ]; then
useradd -s /sbin/nologin -M  www
fi

#unpack

#unpard file from $XGPATH_SOURCE to current directory.
echo "Unpacking to `pwd`"
tar xvf $PKG_NAME


echo "config $N-$V$R..."
#fist, cd build directory
cd $N-$V$R
    
./configure --prefix=/usr/local/nginx \
--user=www \
--group=www \
--with-http_stub_status_module \
--with-http_ssl_module \
--with-http_gzip_static_module
echo "make $N-$V$R..."
CPU_NUM=$(cat /proc/cpuinfo | grep processor | wc -l)
if [ $CPU_NUM -gt 1 ];then
    make -j$CPU_NUM
else
    make
fi
echo "installing $N-$V$R.."
make  install        

F_DEST="/usr/local/nginx"
if [ ! -d $F_DEST/conf/vhosts ];then
    mkdir -v $F_DEST/conf/vhosts
fi
#
cat > $F_DEST/conf/nginx.conf<<'EOF'
user  www www;
worker_processes 4;
pid        /var/run/nginx.pid;
#Specifies the value for maximum file descriptors that can be opened by this process.
worker_rlimit_nofile 51200;
events
{
 use epoll;
 worker_connections 65532;
}

http
{
    include       mime.types;
    default_type  application/octet-stream;
    
    server_names_hash_bucket_size 128;
    client_max_body_size  16m;
    #ShopEx Cookie compatible
    client_header_buffer_size 128k;
    large_client_header_buffers 4 64k;
    #open send file to NIC directly
    sendfile   on;
    tcp_nopush   on;
    tcp_nodelay   on;
    #process life time(s)
    keepalive_timeout  90;
    #fastcgi expire time control
    fastcgi_connect_timeout 60;
    fastcgi_send_timeout 180;
    fastcgi_read_timeout 180;
    fastcgi_buffer_size 128k;
    fastcgi_buffers 4 128k;
    fastcgi_busy_buffers_size 128k;
    fastcgi_temp_file_write_size 128k;
    fastcgi_temp_path /dev/shm;
    #zip compress setting
    gzip    on;
    gzip_min_length   1k;
    gzip_buffers   4 8k;
    gzip_http_version  1.1;
    gzip_types   text/plain application/x-javascript text/css  application/xml;
    gzip_disable "MSIE [1-6]\.";
    
    log_format  access  '$remote_addr - $remote_user [$time_local] "$request" '
    '$status $body_bytes_sent "$http_referer" '
    '"$http_user_agent" $http_x_forwarded_for';
    
    include vhosts/*.conf;
}

EOF

cat > $F_DEST/conf/deny_admin.conf<<'EOF'
#jiangkongbao
allow 60.195.252.106;
allow 60.195.249.83;
#
deny all; 
EOF
cat  > $F_DEST/conf/php_fcgi.conf<<'EOF'
fastcgi_pass  127.0.0.1:9000;
fastcgi_index index.php;

fastcgi_param  GATEWAY_INTERFACE  CGI/1.1;
fastcgi_param  SERVER_SOFTWARE    nginx;

fastcgi_param  QUERY_STRING       $query_string;
fastcgi_param  REQUEST_METHOD     $request_method;
fastcgi_param  CONTENT_TYPE       $content_type;
fastcgi_param  CONTENT_LENGTH     $content_length;

fastcgi_param  SCRIPT_FILENAME    $document_root$fastcgi_script_name;
fastcgi_param  SCRIPT_NAME        $fastcgi_script_name;
fastcgi_param  REQUEST_URI        $request_uri;
fastcgi_param  DOCUMENT_URI       $document_uri;
fastcgi_param  DOCUMENT_ROOT      $document_root;
fastcgi_param  SERVER_PROTOCOL    $server_protocol;

fastcgi_param  REMOTE_ADDR        $remote_addr;
fastcgi_param  REMOTE_PORT        $remote_port;
fastcgi_param  SERVER_ADDR        $server_addr;
fastcgi_param  SERVER_PORT        $server_port;
fastcgi_param  SERVER_NAME        $server_name;

# PHP only, required if PHP was built with --enable-force-cgi-redirect
fastcgi_param  REDIRECT_STATUS    200;
EOF

cat > $F_DEST/conf/pathinfo.conf<<'EOF'
set $real_script_name $fastcgi_script_name;
if ($fastcgi_script_name ~ "^(.+?\.php)(/.+)$") {
    set $real_script_name $1;
    set $path_info $2;
}
fastcgi_param SCRIPT_FILENAME $document_root$real_script_name;
fastcgi_param SCRIPT_NAME $real_script_name;
fastcgi_param PATH_INFO $path_info;
EOF

cat > $F_DEST/conf/error_pages.conf<<'EOF'
error_page   500 502 503 504  /50x.html;
location = /50x.html {
    root   html;
}
EOF

cat > $F_DEST/conf/server_flag.conf<<'EOF'    
#add_header spot 002;
add_header spot 001;
EOF

cat > $F_DEST/conf/vhosts/default.conf<<'EOF'
server
{
    listen       80 default;
    server_name  _;
    index index.html index.htm index.php;
    root  /data/httpd/;
        
    location ~ .*\.php.*
    {
        include php_fcgi.conf;
        include pathinfo.conf;
    }
    
    location ~ .*\.(gif|jpg|jpeg|png|bmp|swf)$
    {
        expires      30d;
    }
        
    location ~ .*\.(js|css)?$
    {
        expires      1h;
    }
    access_log /var/log/nginx/access.log;
    #access_log off;
}
EOF

cat > $F_DEST/conf/vhosts/status.conf<<'EOF'
server
{
        listen       8081 default;
           
        location / {
            stub_status     on;
        }

        access_log off;
}
EOF

#self start script
cat  > /etc/init.d/nginx<<'EOF'
#!/bin/bash
# nginx Startup script for the Nginx HTTP Server
# this script create it by jackbillow at 2007.10.15.
# it is v.0.0.2 version.
# if you find any errors on this scripts,please contact jackbillow.
# and send mail to jackbillow at gmail dot com.
#
# chkconfig: - 85 15
# description: Nginx is a high-performance web and proxy server.
#              It has a lot of features, but it's not for everyone.
# processname: nginx
# pidfile: /var/run/nginx.pid
# config: /usr/local/nginx/conf/nginx.conf

nginxd=/usr/local/nginx/sbin/nginx
nginx_config=/usr/local/nginx/conf/nginx.conf
nginx_pid=/var/run/nginx.pid

RETVAL=0
prog="nginx"

# Source function library.
. /etc/rc.d/init.d/functions

# Source networking configuration.
. /etc/sysconfig/network

# Check that networking is up.
[ ${NETWORKING} = "no" ] && exit 0

[ -x $nginxd ] || exit 0


# Start nginx daemons functions.
start() {
    
    if [ -e $nginx_pid ];then
        echo "nginx already running...."
        exit 1
    fi
        
    echo -n $"Starting $prog: "
    daemon $nginxd -c ${nginx_config}
    RETVAL=$?
    echo
    [ $RETVAL = 0 ] && touch /var/lock/subsys/nginx
    return $RETVAL
}


# Stop nginx daemons functions.
stop() {
    echo -n $"Stopping $prog: "
    killproc $nginxd
    RETVAL=$?
    echo
    [ $RETVAL = 0 ] && rm -f /var/lock/subsys/nginx /var/run/nginx.pid
}


# reload nginx service functions.
reload() {

    echo -n $"Reloading $prog: "
    #kill -HUP `cat ${nginx_pid}`
    killproc $nginxd -HUP
    RETVAL=$?
    echo

}

# See how we were called.
case "$1" in
start)
        start
        ;;

stop)
        stop
        ;;

reload)
        reload
        ;;

restart)
        stop
        start
        ;;

status)
        status $prog
        RETVAL=$?
        ;;
*)
        echo $"Usage: $prog {start|stop|restart|reload|status|help}"
        exit 1
esac

exit $RETVAL
EOF

chmod +x /etc/init.d/nginx
echo "running after package installed..."
if [ ! -d /var/log/nginx ];then
    mkdir -v /var/log/nginx
fi
if [ ! -d /data/httpd ]; then
    mkdir -v /data/httpd
fi

echo "make logrotate"
cat >/etc/logrotate.d/nginx<<'EOF'
/var/log/nginx/*log {
        daily 
        missingok
        rotate 30
        #compress
        #delaycompress
        notifempty
        create 640 root adm
        sharedscripts
        postrotate
                if [ -f /var/run/nginx.pid  ]; then
                        kill -HUP `cat /var/run/nginx.pid` > /dev/null
                fi
        endscript
}
EOF
/sbin/chkconfig nginx --level 3 on    
if [ -f /var/run/nginx.pid ]; then
	/sbin/service nginx restart
else
	/sbin/service nginx start
fi
echo "all done"
