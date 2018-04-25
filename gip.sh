#!/bin/bash

hostname=$1
hosts=/etc/hosts

if [ -z "$hostname" ];then
	echo "input null"
	exit 1
fi

if [ -n "`cat $hosts | grep $hostname`" ];then
	echo "find $hostname in $host"
	exit 1
fi

ip=`curl http://47.52.119.148:8999/hostname/$hostname`

if [ -z "$ip" ];then
	echo "curl $hostname null"
	exit 1
fi

echo "$ip $hostname" >> $hosts

echo "success"
