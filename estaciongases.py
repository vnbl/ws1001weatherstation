#### Programa de recoleccion de datos de sensores de GEI

# Este programa recolecta la informacion de los sensores MQ5, MQ7 Y MQ135 en digital
# a traves del ADC MCP3008 (PARA LA PLACA FINAL UTILIZAMOS MCP3004)
# y formatea los datos a ser presentados de la siguiente manera para todos los sensores
# 0. Muestreo
# 1. Conversion de Voltaje Digital a Voltaje Analogico
# 2. De acuerdo al Voltaje Analogico, deducimos la Resistencia de Carga
# 3. De acuerdo a las curvas de sensibilidad de cada sensor, deducimos la presencia de Gases
# 4. Hallamos un promedio en un tiempo de 2min de la presencia de gases
# 5. Posteamos los datos


from __future__ import division

import time
import datetime
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import requests
import json

# Configuracion tipo SOFTWARE SPI:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

intervalo_lectura = 0.5
intervalo = 120


# Funciones Auxiliares
def redondeo(x):
    r = int(x*10000)/10000
    return r

def tiempo2d(x):
    if x < 10:
        t2d = str(0) + str(x)
    else:
        t2d = str(x)
    return t2d


def rsro(dV):
    Ro = 3
    Vo = (dV/1023)*3.3
    Rs = ((5/Vo)-1)*22 - 3.3
    print Rs
    x = Rs/Ro
    return x

def CH4(x):
    if x > 0:
        CH4 = 7.6368761455*(x**-0.3902048509)
    else:
        CH4 = 0
    return CH4

def LPG(x):
    if x > 0:
        LPG = 5.661663422*(x**-0.3960685242)
    else:
        LPG = 0
    return LPG

def CO(x):
    if x > 0:
        CO = 21.3353219536*(x**-0.6712705276)
    else:
        CO = 0
    return CO

def CO2(x):
    if x > 0:
        CO2 = 4.7674628141*(x**-0.333550268)
    else:
        CO2 = 0
    return CO2

def NH3(x):
    if x > 0:
        NH3 = 6.1884838844*(x**-0.3943237561)
    else:
        NH3 = 0
    return NH3
    
        


while True: # Muestreo

    intervalo_aux = 0
    MQ5 = 0
    MQ7 = 0
    MQ135 = 0

    while intervalo_aux < intervalo:


        MQ5 = MQ5 + mcp.read_adc(0)
        MQ7 = MQ7 + mcp.read_adc(1)
        MQ135 = MQ135 + mcp.read_adc(2)

        intervalo_aux = intervalo_aux + intervalo_lectura
        time.sleep(intervalo_lectura)

    intervalo_aux = 0
    
    # Promedio 

    dMQ5 = MQ5 / (2*intervalo)
    dMQ7 = MQ7 / (2*intervalo)
    dMQ135 = MQ135 / (2*intervalo)

    # Conversion D>A

    LPGppm = str(redondeo(LPG(rsro(dMQ5))))
    CH4ppm = str(redondeo(CH4(rsro(dMQ5))))
    COppm  = str(redondeo(CO(rsro(dMQ7))))
    CO2ppm = str(redondeo(CO2(rsro(dMQ135))))
    NH3ppm = str(redondeo(NH3(rsro(dMQ135))))

    print LPGppm
    print CH4ppm
    print COppm
    print CO2ppm
    print NH3ppm
    print "-----------------------------"
    
    # POST

    url = "TU URL AQUÍ"
    
    data = '{ "NOMBRE_ESTACION": "ESTACION FECOPROD", "LPG": ' + LPGppm + ', "CH4": '+CH4ppm+', "CO": '+COppm+', "CO2": '+CO2ppm+', "NH3": '+NH3ppm+', "LATITUD": -25.26303300,  "LONGITUD": -57.58180900, "FECHA": "'+time.strftime("%Y-%m-%dT%T")+'", "ID": 1}'

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=data, headers=headers)
    

    
        

