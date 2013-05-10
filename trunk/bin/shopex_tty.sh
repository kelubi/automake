#!/bin/bash

IPADDRS=`/sbin/ifconfig | grep -P -o "((eth[\w:]+)|(addr:[\d.]+)|(lo[\d:]*))" | perl -e '%face;foreach (<STDIN>){$int=$1 if (/((?:(?:eth)|(?:lo))[\d:]*)/);$face{$int}=$1 if (/addr:([\d.]+)/);};foreach $interf (sort keys %face){print "$interf = $face{$interf}\t" if ($interf !~ /^lo$/)}'`

if [ $UID -eq 0 ]
then
        PS1="\n\n\033[1;34m[\u@\H]\e[m  \033[1;33m$IPADDRS\e[m \n[\t] PWD => \033[1;35m\w\e[m\n\#># "
else
        PS1="\n\n\033[1;34m[\u@\H]\e[m  \033[1;33m$IPADDRS\e[m \n[\t] PWD => \033[1;35m\w\e[m\n\#>\$ "
fi