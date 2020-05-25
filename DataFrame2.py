# -*- coding: utf-8 -*-


import pandas as pd
import glob
import pyreadr
from haversine import haversine, Unit
from datetime import datetime, timedelta



conmov=30  #condicion de movimiento

Nombre_Dia=[] #arreglo que guarda el nombre del dia de la semana de cada fila
acumulador1=0 #acumulador del tiempo acumulado
acumulador2=1 #acumulador de las etiquetas de viaje
tiempo=60*60 #minutos en segundos

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
       separador = original['dataSource']['dateTimeLine'].astype(str).str.split(" ", n = 1, expand = True)  
       original['dataSource']['Fecha2']=separador[0] 
       original['dataSource']= original['dataSource'].drop( original['dataSource'][((original['dataSource']['latitude']>=-0.19425) | (original['dataSource']['latitude'] <= -0.20341))|(( original['dataSource']['longitude']>=-78.49805 )|(original['dataSource']['longitude'] <= -78.51377))].index)
               
   
    original['dataSource'] = original['dataSource'].reset_index()
    
#######################################################################################
###########################################################################################    
    #Colocar Etiqueta de movimiento (Verificar si esta cerca o no del mismo punto)
    distancias=[] #arreglo para guardar distancias en metros
    movimientos=[] #arreglo para guardar distancias validada por la constante conmov
    for i in range(0,len(original['dataSource'])):      
                 #en la primera iteracion guardo directamente los datos
                 if(i==0):
                      distancia_haversine=0
                      distancias.append(distancia_haversine)
                      movimientos.append(0)
                 else:          
                    punto1 = (original['dataSource']['latitude'][i-1], original['dataSource']['longitude'][i-1]) # (lat, lon)
                    punto2 = (original['dataSource']['latitude'][i], original['dataSource']['longitude'][i])
                    
                    distancia_haversine= haversine(punto1, punto2,unit=Unit.METERS) #distancia con formula de harservine
                    distancias.append(distancia_haversine)
                    
                    if(distancia_haversine<=conmov):  #condicion para etiquetar si esta en movimiento o no
                      movimientos.append(0)   # no se movio =0
                    else:
                      movimientos.append(1)  # se movio=1
                    
                    
    #se anexa los resultados al dataframe                
    original['dataSource']["DistMetros"]= distancias  
    original['dataSource']["Movimiento"]= movimientos 
    
##################################################################################################  
##################################################################################################  
    #Poner etiquetas de viajes
    acumulador2=1  #Reinicio contador de viajes para cada nuevo archivo
    etiquetas=[]  #arreglo para guardar la etiqueta de cada viaje
    acumulador3=0  #acumulador del campo Ruta
    reco=[]   #Arreglo para guardar el seguimiento de cada punto generado por acumulador 3
    for i in range(0,len(original['dataSource'])):
            #en la primera iteracion guardo directamente los datos
            if (i==0):
                etiquetas.append(acumulador2)
                reco.append(acumulador3)
            else:
                #fecha3 y fecha4 son las fecha en formato año-mes-dia para comparar fechas
                fecha3 = datetime.strptime(original['dataSource']["Fecha2"][i-1], '%Y-%m-%d')
                fecha4 = datetime.strptime(original['dataSource']["Fecha2"][i], '%Y-%m-%d')  
                if(fecha3!=fecha4):
                    #Los contadores se reinician en cada nuevo dia 
                    acumulador1=0
                    acumulador2=1
                    acumulador3=0  
                    reco.append(acumulador3)
                    etiquetas.append(acumulador2)      
                    
                #Cuando Movimiento es 0 se acumula el tiempo en el acumulador1
                elif(original['dataSource']["Movimiento"][i]==0):
                    #fecha1 y fecha2 son redimensionados en formato año-mes-dia Hora-min-seg
                    fecha1 = datetime.strptime(original['dataSource']["Fecha"][i-1], '%Y-%m-%d %H:%M:%S')
                    fecha2 = datetime.strptime(original['dataSource']["Fecha"][i], '%Y-%m-%d %H:%M:%S')                     
                    #Para luego ser restados entre si y el resultado es transformado en segundos
                    Total=(fecha2-fecha1)/timedelta(seconds=1)
                    acumulador1=acumulador1+Total   
                    reco.append(acumulador3)
                    etiquetas.append(acumulador2)
                #Cuando el tiempo acumulador es mayor o igual que la constante tiempo y Movimiento es 1 se 
                #concluye el viaje y se inicia uno nuevo aumentando en 1 el acumulador2 y reiniciando
                #Acumulador 1 y 3
                elif(original['dataSource']["Movimiento"][i]==1 and acumulador1 >= tiempo):      
                    acumulador1=0                   
                    acumulador2=acumulador2+1
                    acumulador3=0  
                    reco.append(acumulador3)
                    etiquetas.append(acumulador2) 
                
                #Si Movimiento es 1 se mantiene acumulador 2 y se aumenta acumulador 3
                #Acumulador 1 se mantiene en 0
                else:
                    acumulador1=0    
                    acumulador3=acumulador3+1
                    reco.append(acumulador3)
                    etiquetas.append(acumulador2)  
                    
    #se anexa los resultados al dataframe                 
    original['dataSource']["Viaje"]= etiquetas
    original['dataSource']["Ruta"]= reco
    
    original['dataSource'].drop(columns =["index","Fecha2"], inplace = True) 
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