# -*- coding: utf-8 -*-


import pandas as pd
import glob
import pyreadr


#tabla_variables=pd.DataFrame()

directorio_entrada="C:/Users/Andres/Desktop/Tesis/Marcos/Pruebas/"
directorio_salida="C:/Users/Andres/Desktop/Tesis/Marcos/Pruebas/"

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
       original['dataSource']= original['dataSource'].drop( original['dataSource'][((original['dataSource']['latitude']>=-0.19425) | (original['dataSource']['latitude'] <= -0.20341))|(( original['dataSource']['longitude']>=-78.49805 )|(original['dataSource']['longitude'] <= -78.51377))].index)

            
    tabla_final_uce=  tabla_final_uce.append([ original['dataSource']], ignore_index=True)
  
    
#Guardar dataframe en un archivo dat
tabla_final_uce.to_csv(directorio_salida+archivo_salida)  
#tabla_cargada = pd.read_table(directorio_salida+archivo_salida, sep=",")