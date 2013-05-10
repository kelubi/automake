DROP database IF EXISTS proftpd;
CREATE DATABASE `proftpd` ;
grant all on proftpd.* to proftpd@127.0.0.1 identified by 'PROFTPD_PASSWORD';
USE `proftpd`;

CREATE TABLE IF NOT EXISTS `ftpgroups` (  
    `groupname` varchar(30) NOT NULL,  
    `gid` int(11) NOT NULL DEFAULT '1000',  
    `members` varchar(255) NOT NULL
)ENGINE=MyISAM;

CREATE TABLE IF NOT EXISTS `ftpusers` (      
    `userid` varchar(30) NOT NULL,     
    `passwd` varchar(80) NOT NULL,     
    `uid` int(10) unsigned NOT NULL DEFAULT '48',     
    `gid` int(10) unsigned NOT NULL DEFAULT '48',     
    `homedir` varchar(255) NOT NULL,     
    `shell` varchar(255) NOT NULL DEFAULT '/sbin/nologin',     
    `count` int(10) unsigned NOT NULL DEFAULT '0',    
    `host` varchar(30) NOT NULL,     
    `lastlogin` varchar(30) NOT NULL,    
    UNIQUE KEY `userid` (`userid`)
 ) ENGINE=MyISAM;

CREATE TABLE IF NOT EXISTS `quotalimits` (     
    `name` varchar(30) DEFAULT NULL, 
    `quota_type` enum('user','group','class','all') NOT NULL DEFAULT 'user', 
    `per_session` enum('false','true') NOT NULL DEFAULT 'false', 
    `limit_type` enum('soft','hard') NOT NULL DEFAULT 'soft', 
    `bytes_in_avail` float NOT NULL DEFAULT '0',  `bytes_out_avail` float NOT NULL DEFAULT '0', 
    `bytes_xfer_avail` float NOT NULL DEFAULT '0',  
    `files_in_avail` int(10) unsigned NOT NULL DEFAULT '0', 
    `files_out_avail` int(10) unsigned NOT NULL DEFAULT '0', 
    `files_xfer_avail` int(10) unsigned NOT NULL DEFAULT '0'
) ENGINE=MyISAM;

CREATE TABLE IF NOT EXISTS `quotatallies` (    
    `name` varchar(30) NOT NULL, 
    `quota_type` enum('user','group','class','all') NOT NULL DEFAULT 'user', 
    `bytes_in_used` float NOT NULL DEFAULT '0', 
    `bytes_out_used` float NOT NULL DEFAULT '0', 
    `bytes_xfer_used` float NOT NULL DEFAULT '0', 
    `files_in_used` int(10) unsigned NOT NULL DEFAULT '0', 
    `files_out_used` int(10) unsigned NOT NULL DEFAULT '0', 
    `files_xfer_used` int(10) unsigned NOT NULL DEFAULT '0'
) ENGINE=MyISAM;