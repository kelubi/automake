#!/bin/sh
#00 02  * * * /bin/sh /home/magic/bin/mysql_per_db_backup.sh
PATH=$PATH:/usr/local/bin:/usr/local/sbin:/usr/sbin:/sbin:/home/magic/bin:/usr/local/mysql/bin

#static configure
local_mysql_backup_dir="/data/backup/local/mysql"
logfile="/var/log/mysql_local_backup.log"
mysql_data_dir="/data/mysql"
rotation_days=14
db_host="localhost"
db_port=3306
db_user="root"
db_pass="password"
ignore_db="mysql test"
#dynamic configure
backup_time=$(date +"%Y%m%d")
backup_dir_name="$local_mysql_backup_dir/$backup_time"
if [ ! -d $backup_dir_name ] ; then
    mkdir -pv $backup_dir_name  
fi
db_names=$(echo "show databases" | mysql -h$db_host -u$db_user -p$db_pass | grep -v "Database")
if [ $? -ne 0 ] ; then
    echo $(date +"%F %T ")" ERROR: get backup db names failure" >> $logfile
    exit
fi
#dump
for db_name in $db_names ; do
    if [[ $ignore_db == *$db_name* ]] ; then
        echo $(date +"%F %T")" NOTICE: $db_name has ignored" >> $logfile
    else
        sql_save_name="$backup_dir_name/$db_name".sql
        #echo $sql_save_name
        #backup  
        # --dump-slave ,see details in 
        #http://asmboy001.blog.51cto.com/340398/197750 
        #http://catch22.diandian.com/post/2012-03-03/16337297
        mysqldump -h"$db_host" -u"$db_user" -p"$db_pass" "$db_name"  --single-transaction --master-data > $sql_save_name 2>> $logfile
        if [ $? -eq 0 ];then
            echo $(date +"%F %T")" NOTICE: $db_name backup successfully" >> $logfile
        else
            echo $(date +"%F %T")" ERROR: $db_name backup failure" >> $logfile
        fi
    fi
done
#compress
pushd $local_mysql_backup_dir
tar -czf $backup_time".tgz" $backup_time
#clean
if [ $? -eq 0 ] ; then
    [ "$backup_dir_name" != "/" ] && [ -d $backup_dir_name ] && rm -rf $backup_dir_name;
else
    echo $(date +"%F %T")" ERROR: compress failure" >> $logfile
fi
popd
#delete old backup
find $local_mysql_backup_dir -name "*.tgz" -mtime +$rotation_days -exec rm -f {} \;

#-EOF-