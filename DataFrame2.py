# -*- coding: utf-8 -*-


import pandas as pd
import glob
import pyreadr


#tabla_variables=pd.DataFrame()

#directorio_entrada="C:/Users/Andres/Desktop/Tesis/Marcos/Pruebas/"
#directorio_salida="C:/Users/Andres/Desktop/Tesis/Marcos/Pruebas/"

directorio_entrada="/home/milton.moncayo/SmartGPS/timeline/"
directorio_salida="/home/milton.moncayo/SmartGPS/data/"
archivo_salida="DataSmart.dat"

for k in range(0,len(glob.glob(directorio_entrada+"*.RData")) ): 
    archivo="tld"+str(k)+".RData"
    enlace=directorio_entrada + archivo
    #Pongo try except.. xq existen archivos que dan error al momento de leerlos
    try:
       original = pyreadr.read_r(enlace)
    except:
        continue
        
    if('tabla_variables' not in globals() ):
         tabla_variables=pd.DataFrame()
         tabla_final_uce=pd.DataFrame()
         tabla_final_uce=pd.DataFrame(columns=[])
         tabla_variables = pd.DataFrame( columns=['dateTimeLine','latitude','longitude','accuracy','altitude','verticalAccuracy','velocity','heading','dateActivity','activity1','confidence1','activity2','confidence2','file'])
    for i in range(0,len(original['dataSource']['dateTimeLine'])): 
                    #existen archivos que solo tienen 3 parametros, que son, dateTimeLine,Latitude y Longitude
                    #se puede anexar estos datos de estos archivos o solo ignorarlos
                    if((original['dataSource'].shape[1])<4):
                     #tabla_variables = tabla_variables.append({'dateTimeLine':original['dataSource']['dateTimeLine'][i],'latitude':original['dataSource']['latitude'][i],'longitude':original['dataSource']['longitude'][i],'accuracy':None,'verticalAccuracy':None,'altitude':None,'velocity':None,'heading':None,'dateActivity':None,'activity1':None,'confidence1':None,'activity2':None,'confidence2':None,'file':archivo}, ignore_index=True)          
                     continue
                    else:                    
                     tabla_variables = tabla_variables.append({'dateTimeLine':original['dataSource']['dateTimeLine'][i],'latitude':original['dataSource']['latitude'][i],'longitude':original['dataSource']['longitude'][i],'accuracy':original['dataSource']['accuracy'][i],'verticalAccuracy':original['dataSource']['verticalAccuracy'][i],'altitude':original['dataSource']['altitude'][i],'velocity':original['dataSource']['velocity'][i],'heading':original['dataSource']['heading'][i],'dateActivity':original['dataSource']['dateActivity'][i],'activity1':original['dataSource']['activity1'][i],'confidence1':original['dataSource']['confidence1'][i],'activity2':original['dataSource']['activity2'][i],'confidence2':original['dataSource']['confidence2'][i],'file':archivo}, ignore_index=True)          

#Copiar dataframe
tabla_final_uce= pd.concat([tabla_variables], axis=1, sort=False)

#Delimitar dataframe al area de la Universidad
for p in range(0, len(tabla_final_uce)):
       if( ((-0.19425 >= tabla_final_uce['latitude'][p] >= -0.20341)and (-78.49805 >= tabla_final_uce['longitude'][p] >= -78.51377))):    
           continue
       else:
           tabla_final_uce.drop(index=[p], inplace=True)

#Guardar dataframe en un archivo dat
tabla_final_uce.to_csv(directorio_salida+archivo_salida)  
#tabla_cargada = pd.read_table(directorio_salida+archivo_salida, sep=",")