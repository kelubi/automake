#!/bin/bash
#

if [ $(uname -m) = "i686" ]; then
    SRC_URI="http://lnmpp.googlecode.com/files/mongodb-linux-i686-2.0.0.tgz"
    PKG_NAME=`basename $SRC_URI`
    N="mongodb-linux-i686"
    V="2.0.0"
else
    SRC_URI="http://lnmpp.googlecode.com/files/mongodb-linux-x86_64-2.0.0.tgz"
    PKG_NAME=`basename $SRC_URI`
    N="mongodb-linux-x86_64"
    V="2.0.0"
fi

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

echo "config $N-$V$R..."
/bin/cp -rvf $N-$V$R /usr/local/mongodb
mkdir -pv /data/mongodb

cat >/etc/init.d/mongodb<<'EOF'
#!/bin/bash
#
# mongodb     Startup script for the mongodb server
#
# chkconfig: - 64 36
# description: MongoDB Database Server
#
# processname: mongodb
#

# Source function library
. /etc/rc.d/init.d/functions

if [ -f /etc/sysconfig/mongodb ]; then
	. /etc/sysconfig/mongodb
fi

prog="mongod"
mongod="/usr/local/mongodb/bin/mongod"
RETVAL=0

start() {
	echo -n $"Starting $prog: "
	daemon $mongod "--fork --dbpath /data/mongodb --logpath /data/mongodb/mongodb.log --logappend 2>&1 >>/data/mongodb/mongodb.log"
	RETVAL=$?
	echo
	[ $RETVAL -eq 0 ] && touch /var/lock/subsys/$prog
	return $RETVAL
}

stop() {
	echo -n $"Stopping $prog: "
	killproc $prog
	RETVAL=$?
	echo
	[ $RETVAL -eq 0 ] && rm -f /var/lock/subsys/$prog
	return $RETVAL
}

reload() {
	echo -n $"Reloading $prog: "
	killproc $prog -HUP
	RETVAL=$?
	echo
	return $RETVAL
}

case "$1" in
	start)
		start
		;;
	stop)
		stop
		;;
	restart)
		stop
		start
		;;
	condrestart)
		if [ -f /var/lock/subsys/$prog ]; then
			stop
			start
		fi
		;;
	reload)
		reload
		;;
	status)
		status $mongod
		RETVAL=$?
		;;
	*)
		echo $"Usage: $0 {start|stop|restart|condrestart|reload|status}"
		RETVAL=1
esac

exit $RETVAL
EOF

echo "all done"
