#!/bin/bash
##set -x

if [ $# -ne 0 ]
then
	echo usage: $0:
	exit 0
fi

bin_dir=/bin
data_dir=/home/pi/estacion_digibox_v3	
logs_dir=/home/pi/estacion_digibox_v3/logs		
wx_bin_dir=/home/pi/estacion_digibox_v3

ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1  -d'/' > /home/pi/estacion_digibox_v3/ip.dat



if [ ! -d $data_dir ]
then
	echo Data directory, $data_dir, does not exist.
	exit 0
fi

log=$logs_dir/ws1001wxdata-`${bin_dir}/date +%F`.log

echo Starting Weather Station.pl

$wx_bin_dir/ws1001wxdata.pl -i 192.168.1.101 $data_dir/msg-udp-srch.dat $data_dir/msg-tcp-nowrec-req.dat $data_dir/ewpdata.json >> $log 2>&1
