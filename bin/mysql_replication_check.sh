#!/bin/sh
#
# created by joyce, 2011/03/04
# modified by ken, 2012/12/24

DBUser=root
DBPasswd=passwd
Port=3306
Host=localhost
LOGDIR=/var/log/mysql
StatFile=$LOGDIR/"slave_status"
LogFile=$LOGDIR/repl_result.log


pushd $LOGDIR

echo `date +"%Y-%m-%d %H:%M:%S"` > $LogFile
echo "show slave status\G" | /usr/local/mysql/bin/mysql -u$DBUser -p$DBPasswd -P $Port -h$Host > $StatFile

#?? io_thread, sql_thread, last_errno ???
IoStat=`cat $StatFile | grep Slave_IO_Running | awk '{print $2}'`
SqlStat=`cat $StatFile | grep Slave_SQL_Running | awk '{ print $2}'`
Last_Errno=`cat $StatFile | grep Last_Errno`
Last_Error=`cat $StatFile | grep Last_Error`
Behind=`cat $StatFile | grep Seconds_Behind_Master | awk '{print $2}'`

if [ $IoStat = 'No' ] || [ $SqlStat = 'No' ] || [ $Behind -gt 5 ] ; then
    echo $Host  "rep is error !!" >> $LogFile
else
    echo $Host  "rep is ok !" >> $LogFile
fi

echo "IoStat="$IoStat >> $LogFile
echo "SqlStat="$SqlStat >> $LogFile
echo $Last_Errno >> $LogFile
echo $Last_Error >> $LogFile
echo "Behind time="$Behind >> $LogFile

Result=`cat $LogFile | grep  $Host | awk '{print $4}'`

if [ $Result = 'error' ] ;
then
    cat $LogFile | mail -s "robin.no.3 rep error"  ken@yiyiee.com
fi

popd