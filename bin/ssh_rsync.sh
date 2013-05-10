#!/bin/bash
BackupFrom=some.host.make.ssh.key.login.first
BackupPath=/data/httpd/
BackupTo=/data/backup/
LogFile=/var/log/backup.log  


echo "-------------------------------------------" >> $LogFile  
echo $(date +"%Y-%m-%d %H:%M:%S") >> $LogFile  
echo "--------------------------" >> $LogFile  
rsync -a --delete -e ssh  root@$BackupFrom:$BackupPath $BackupTo
echo $(date +"%Y-%m-%d %H:%M:%S") >> $LogFile  
echo "-------------------------------------------" >> $LogFile  
popd >> $LogFile