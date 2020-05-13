# -*- coding: utf-8 -*-


import pandas as pd
import glob
import pyreadr
from haversine import haversine, Unit
from datetime import datetime, timedelta

conmov=2  #condicion de movimiento

Nombre_Dia=[]
acumulador1=0
acumulador2=1
tiempo=5*60 #minutos en segundos

#tabla_variables=pd.DataFrame()

directorio_entrada="C:/Users/User/Desktop/TesisPrincipal/Marcos/Pruebas/"
directorio_salida="C:/Users/User/Desktop/TesisPrincipal/Marcos/Pruebas/"

#directorio_entrada="/home/milton.moncayo/SmartGPS/timeline/"
#directorio_salida="/home/milton.moncayo/SmartGPS/data/"
archivo_salida="DataSmart.dat"

for k in range(0,len(glob.glob(directorio_entrada+"*.RData")) ): 
    archivo="tld"+str(k)+".RData"
    enlace=directorio_entrada + archivo
    print("sigue---> " +str(archivo) )
    #Pongo try except.. xq existen archivos que dan error al momento de leerlos
    try:
       original = pyreadr.read_r(enlace)
    except:
        print("archivo dañado---> " +str(archivo) )
        continue
    print("Tamaño del archivo: "+str(len(original['dataSource'])))
    
    #Inicializa dataframe y comprueba si ya existe
    if('tabla_final_uce' not in globals() and 'tabla_final_todo' not in globals() ):
         tabla_final_uce=pd.DataFrame()
         tabla_final_uce=pd.DataFrame(columns=[])
    #Comprueba numero de columnas del dataframe original y lo concatena a un nuevo dataframe    
    if((original['dataSource'].shape[1])<13):    
           continue
    else:
       original['dataSource']['file']=archivo
       separador = original['dataSource']['dateTimeLine'].astype(str).str.split(".", n = 1, expand = True) 
       original['dataSource']['Fecha']=separador[0] 
       original['dataSource']= original['dataSource'].drop( original['dataSource'][((original['dataSource']['latitude']>=-0.19425) | (original['dataSource']['latitude'] <= -0.20341))|(( original['dataSource']['longitude']>=-78.49805 )|(original['dataSource']['longitude'] <= -78.51377))].index)
               
   
    original['dataSource'] = original['dataSource'].reset_index()
    
    
    #Colocar Etiqueta de movimiento
    distancias=[]
    movimientos=[]
    
    for i in range(0,len(original['dataSource'])):       
                 if(i==0):
                      distancia=0
                      distancias.append(distancia)
                      movimientos.append(0)
                 else:          
                    punto1 = (original['dataSource']['latitude'][i-1], original['dataSource']['longitude'][i-1]) # (lat, lon)
                    punto2 = (original['dataSource']['latitude'][i], original['dataSource']['longitude'][i])
                    
                    distancia= haversine(punto1, punto2,unit=Unit.METERS)      
                    distancias.append(distancia)
                    
                    if(distancia<=conmov):
                      movimientos.append(0)
                    else:
                      movimientos.append(1)
                      
    original['dataSource']["DistMetros"]= distancias
    original['dataSource']["Movimiento"]= movimientos #se movio=1 no se movio =0
    
    
    #Poner etiquetas de viajes
    acumulador2=1  #Reinicio contador de viajes para cada nuevo archivo
    etiquetas=[] 
    for i in range(0,len(original['dataSource'])):
                 
            if (i==0):
                viaje="Viaje "+ str(acumulador2)
                etiquetas.append(viaje)
            else:
                if(original['dataSource']["Movimiento"][i]==0):
                    fecha1 = datetime.strptime(original['dataSource']["Fecha"][i-1], '%Y-%m-%d %H:%M:%S')
                    fecha2 = datetime.strptime(original['dataSource']["Fecha"][i], '%Y-%m-%d %H:%M:%S')
                    Total=(fecha2-fecha1)/timedelta(seconds=1)
                    acumulador1=acumulador1+Total              
                    viaje="Viaje "+ str(acumulador2)
                    etiquetas.append(viaje)
                    
                elif(original['dataSource']["Movimiento"][i]==1 and acumulador1 >= tiempo):      
                    acumulador1=0
                   
                    acumulador2=acumulador2+1
                    viaje="Viaje "+ str(acumulador2)
                    etiquetas.append(viaje) 
                else:
                    viaje="Viaje "+ str(acumulador2)
                    etiquetas.append(viaje)  
                    
    original['dataSource']["Etiqueta"]= etiquetas
    original['dataSource'].drop(columns =["index"], inplace = True) 
    tabla_final_uce=  tabla_final_uce.append([ original['dataSource']], ignore_index=True)
    
    
#Separa fecha y hora    
separador = tabla_final_uce['dateTimeLine'].astype(str).str.split(" ", n = 1, expand = True) 

separador = separador[0].astype(str).str.split("-", n = 3, expand = True) 

tabla_final_uce["Año"]= separador[0] 
tabla_final_uce["Mes"]= separador[1] 
tabla_final_uce["Dia"]= separador[2] 

separador = tabla_final_uce['dateTimeLine'].astype(str).str.split(" ", n = 1, expand = True) 

separador = separador[1].astype(str).str.split(":", n = 2, expand = True) 

tabla_final_uce["Hora"]= separador[0] 
tabla_final_uce["Minuto"]= separador[1] 

separador = separador[2].astype(str).str.split(".", n = 2, expand = True) 
tabla_final_uce["Segundo"]= separador[0] 

tabla_final_uce.drop(columns =["dateTimeLine"], inplace = True) 


#Etiquetar con el nombre del dia de la semana
for i in range(0,len(tabla_final_uce)):

    dia = int(tabla_final_uce["Dia"][i])

    mes = int(tabla_final_uce["Mes"][i])

    year = int(tabla_final_uce["Año"][i])
    
    a = (14 - mes) // 12
    
    y = year - a
    
    m = mes + 12 * a - 2
    
    d = (dia + year + (year//4) - (year//100) + (year//400) + ((31 * m)//12)) % 7      
    if d == 0:    
        diaSemana = 'Domingo'   
    elif d == 1:    
        diaSemana = 'Lunes'    
    elif d == 2:    
        diaSemana = 'Martes'    
    elif d == 3:    
        diaSemana = 'Miércoles'    
    elif d == 4:    
        diaSemana = 'Jueves'    
    elif d == 5:    
        diaSemana = 'Viernes'    
    else:    
        diaSemana = 'Sábado'
    
    Nombre_Dia.append(diaSemana)

tabla_final_uce["Ndia"]= Nombre_Dia


#Guardar dataframe en un archivo dat
tabla_final_uce.to_csv(directorio_salida+archivo_salida)  
#tabla_cargada = pd.read_table(directorio_salida+archivo_salida, sep=",")