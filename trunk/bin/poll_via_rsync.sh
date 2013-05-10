#!/bin/bash
BackupFrom=linode
BackupPath=/var/www/html/
BackupTo=/data/backup/html
LogFile=/var/log/html_backup.log  


echo "-------------------------------------------" >> $LogFile  
echo $(date +"%Y-%m-%d %H:%M:%S") >> $LogFile  
echo "--------------------------" >> $LogFile  
rsync -a --delete -e ssh  root@$BackupFrom:$BackupPath $BackupTo
echo $(date +"%Y-%m-%d %H:%M:%S") >> $LogFile  
echo "-------------------------------------------" >> $LogFile  
popd >> $LogFile