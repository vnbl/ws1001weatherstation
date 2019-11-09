#!/bin/sh
if ps -ef | grep -v grep | grep ws1001wxdata.pl ; then
        exit 0
else
        $sudo sh /home/pi/estacion_digibox_v3/run_ws.sh
         
        exit 0
fi