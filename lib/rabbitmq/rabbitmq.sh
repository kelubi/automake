#!/bin/bash
SRC_URI="http://www.rabbitmq.com/releases/rabbitmq-server/v3.1.0/rabbitmq-server-3.1.0.tar.gz"
PKG_NAME=`basename $SRC_URI`
N="rabbitmq-server"
V="3.1.0"

yum install -y xmlto xmlto-devel

if [ ! -d /opt/install ]; then
    mkdir -pv /opt/install
fi
echo "go to working dir"
cd /opt/install

if [ -s $PKG_NAME ]; then
  echo "$PKG_NAME [found]"
  else
  echo "Error: $PKG_NAME not found!!!download now......"
  wget -c $SRC_URI
fi


#init 
echo "init $N-$V$R build script..."
#unpack
#unpard file from $XGPATH_SOURCE to current directory.
echo "Unpacking to `pwd`"
tar xvf $PKG_NAME

cd $N-$V$R
echo "make $N-$V$R..."

#
make TARGET_DIR=/usr/local/rabbitmq SBIN_DIR=/usr/local/rabbitmq/sbin MAN_DIR=/usr/local/rabbitmq/man install 

#init.d/rabbitmq
cat >/etc/init.d/rabbitmq<'EOF'
#!/bin/sh
#
# chkconfig: - 85 15
# description:  Startup script for the server of Rabbitmq
#

RABBITMQ=/usr/local/rabbitmq
SBIN=$RABBITMQ/sbin/rabbitmq-server
CONTROL=$RABBITMQ/sbin/rabbitmqctl
PID=$RABBITMQ/var/lib/rabbitmq/mnesia/rabbit@`hostname -s`.pid

RETVAL=0
#. /etc/rc.d/init.d/functions
#export HOME=/usr/local/lib/erlang

start(){
    [ -e $PID ] && [ -s $PID ] && {
    echo "rabbitmq is already running..."
    exit 1
    }

    echo -n "Starting rabbitmq: "
    $SBIN -detached
    RETVAL=$?
    [ $RETVAL -eq 0 ] && echo "rabbitmq is starting [OK]"
}

stop(){
    echo -n "Stopping rabbitmq: "
    $CONTROL stop
    RETVAL=$?
    if [ $RETVAL -eq 0 ] ;then
        [ -e $PID ] && rm -f $PID
        echo "rabbitmq is stopping [OK]"
    fi
}

restart(){
    stop
    sleep 2
    start
}

case "$1" in
    start) start
    ;;
    stop) stop
    ;;
    status) $CONTROL status
    ;;
    rotate_logs) $CONTROL rotate_logs
    ;;
    restart) restart
    ;;
    *) echo $"Usage: $0 {start|stop|status|restart|rotate_logs}"
       exit 1
esac

exit $?

EOF

chmod +x /etc/init.d/rabbitmq
 /sbin/chkconfig --add rabbitmq
/sbin/chkconfig rabbitmq --level 3 on

#enabel rabbitmq management
/usr/local/rabbitmq/sbin/rabbitmq-plugins enable rabbitmq_management