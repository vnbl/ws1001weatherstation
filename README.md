# ws1001weatherstation

this is code for reading a WS1001 weather station with a RaspberryPi and sending the info to a web server. It also contains code for doing the same with commecial gas sensors connected to the RPi

Instructions in Spanish - Instrucciones en español


# Instalaciones Previas: 

Instalar Pearl 6 (manualmente, NO CON CPAN)
Instalar la libreria del digitalizador MCP3008 de Adafruit
Abrir los puertos TCP de comunicacion. Esto se realiza modificando el archivo xserverrc.sh del sistema de la siguiente manera
#!/bin/sh

exec /usr/bin/X -nolisten tcp "$@" # COMENTAR ESTA LINEA

    El archivo xserverrc.sh del sistema se encuentra en la direcion /etc/X11/xinit/xserverrc

Instrucciones de Instalación
* Copiar todos los archivos en una carpeta en el raspberry pi.
* Buscar el IP del raspberry (en terminal: $ sudo ifconfig)
* Modificar el archivo run_ws.sh: En la línea 29: $wx_bin_dir/ws1001wxdata.pl -i 192.168.1.101 $data_dir/msg-udp-srch.dat $data_dir/msg-tcp-nowrec-req.dat $data_dir/ewpdata.json >> $log 2>&1 .
* Cambiar el IP anterior por el nuevo hallado en el paso 2. Asegurarse de que la red a la que esta conectada el Raspberry le de IP ESTATICA.
* Inicialización automática y checkeo de funcionamiento: Los procesos de inicialización y control de fallos se realizan cada 1 minuto utilizando la funcionalidad crontab de Linux. Los archivos de inicialización y checkeo son run_ws.sh y checkWS.sh respectivamente para la Estacion Meteorológica y estaciongases.py y checkGEI.sh para la Estación de Gases. 

# Como instalar: 

En terminal: crontab -e

Seleccionar editor nano 

En la última línea del archivo colocar:

1 * * * * sudo sh  /home/pi/estacion_digibox_v3/checkWS.sh

@reboot sudo sh /home/pi/estacion_digibox_v3/run_ws.sh

1 * * * * sudo sh /home/pi/estacion_digibox_v3/checkGEI.sh

@reboot sudo python /home/pi/estacion_digibox_v3/estaciongases.py

Rebootear el sistema >> En terminal: $ reboot

# Estación Meteorologica - Archivos

checkWS.sh

Control de funcionamiento del archivo ws1001wxdata.pl. El control de funcionamiento se realiza cada 1 minuto (crontab), el objetivo es volver a levantar el programa de control de la estacion meteorologica en caso de que este haya parado subitamente por algun error de conexion con la estacion.

Run_ws.sh

Este archivo se encarga de dar al archivo de control de la estacion ws1001wxdata los datos necesarios para empezar los protocolos TCP y UDP de comunicacion con la estacion, IP, direccionar los archivos de log de eventos y comenzar a correr la estacion.

ewpdata.json

Este archivo se actualiza continuamente con los datos del momento de la estacion y los coloca en formato JSON.

Msg-tcp-nowrec-req.dat

Mensaje record del protocolo TCP (NO MODIFICAR)

Msg-udp-srch.dat

Mensaje de busqueda del protocolo UDP (NO MODIFICAR)

Ws1001wxdata.pl

Este archivo se encarga de inicializar la estacion con los datos proveidos por el archivo run_ws.sh, generar los mensajes de correcto funcionamiento y errores de los logs de interconexion TCP y UDP y decodificar y formatear los datos traidos de la estacion. Tiempo de muestreo: 120 segundos

Estacion de Gases - Archivos

checkGEI.sh

Este archivo funciona de la misma manera que el archivo checkWS.sh con el mismo principio, aplicado al correcto funcionamiento del archivo estaciongases.py

Estaciongases.py

Este archivo se encarga de tomar los datos de la placa de GEI (con los protocolos propios del digitalizador MCP3008 de Adafruit). Los datos se toman en digital (valores de 0 a 1023) que corresponden por regla de 3 simple a valores de 0 a 5V en analogico. A partir de los valores en analogico se realizan los calculos de acuerdo a la configuracion del circuito que disenhe y el datasheet de los sensores MQ5, MQ7 y MQ135. Las ecuaciones de sensibilidad a los gases no estan en el datasheet, se sacaron haciendo regresion no lineal (yo elegi regresion logaritmica) de acuerdo a los datos de los graficos de sensibilidad. El muestreo se realiza cada 0.5s y se realiza un promedio de los valores de los gases cada 120s, y estos valores son los que se utilizan para hacer el POST.
