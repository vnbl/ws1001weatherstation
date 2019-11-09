#!/bin/sh
if ps -ef | grep -v grep | grep estaciongases.py ; then
        exit 0
else
        $sudo sh /home/pi/estacion_digibox_v3/run_estaciongases.sh
         
        exit 0
fi