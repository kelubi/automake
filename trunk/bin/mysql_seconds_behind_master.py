<span style="font-size:16px;">#filename: run_mysql_replication_heartbeat.py
#encoding=gbk
import datetime,time
import os,sys
from public import db

import db_conf

source_folder = db_conf.SOURCE_FOLDER


def init_eviroment_path():
    print sys.path
    python_path = (source_folder)
    
    for i in python_path:
        if i not in sys.path:
            sys.path.append(i)
    
    print sys.path

def main():
    conn, cursor = db.GetMysqlCursor('update')
    
    cursor.execute("insert into heartbeat (master_datetime,slave_datetime) values(now(),sysdate())")
    
    cursor.close()
    conn.close()

if __name__ == '__main__':
    init_eviroment_path()
    os.system("title MySQL Replication心跳")
    count = 1
    while True:
        main()
        print "(%d)%s"%(count,datetime.datetime.now())
        count+=1
        time.sleep(60)</span><span style="font-size: 24px;">
</span>