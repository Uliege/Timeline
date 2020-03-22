# -*- coding: utf-8 -*-


import pandas as pd
import glob
import pyreadr


#tabla_variables=pd.DataFrame()

directorio_entrada="C:/Users/Andres/Desktop/Tesis/Marcos/Pruebas/"

for k in range(1,len(glob.glob(directorio_entrada+"*.RData"))+1 ): 
    archivo="tld"+str(k)+".RData"
    enlace=directorio_entrada + archivo
    #Pongo try except.. porque existen archivos que dan error al momento de leerlos
    try:
       original = pyreadr.read_r(enlace)
    except:
        continue
        
    if('tabla_variables' not in globals() ):
         tabla_variables=pd.DataFrame()
         tabla_variables = pd.DataFrame( columns=['dateTimeLine','latitude','longitude','accuracy','altitude','verticalAccuracy','velocity','heading','dateActivity','activity1','confidence1','activity2','confidence2','file'])
    for i in range(0,len(original['dataSource']['dateTimeLine'])): 
                    #existen archivos que solo tienen 3 parametros, que son, dateTimeLine,Latitude y Longitude
                    #se puede anexar estos datos de estos archivos o solo ignorarlos
                    if((original['dataSource'].shape[1])<4):
                     #tabla_variables = tabla_variables.append({'dateTimeLine':original['dataSource']['dateTimeLine'][i],'latitude':original['dataSource']['latitude'][i],'longitude':original['dataSource']['longitude'][i],'accuracy':None,'verticalAccuracy':None,'altitude':None,'velocity':None,'heading':None,'dateActivity':None,'activity1':None,'confidence1':None,'activity2':None,'confidence2':None,'file':archivo}, ignore_index=True)          
                     continue
                    else:                    
                     tabla_variables = tabla_variables.append({'dateTimeLine':original['dataSource']['dateTimeLine'][i],'latitude':original['dataSource']['latitude'][i],'longitude':original['dataSource']['longitude'][i],'accuracy':original['dataSource']['accuracy'][i],'verticalAccuracy':original['dataSource']['verticalAccuracy'][i],'altitude':original['dataSource']['altitude'][i],'velocity':original['dataSource']['velocity'][i],'heading':original['dataSource']['heading'][i],'dateActivity':original['dataSource']['dateActivity'][i],'activity1':original['dataSource']['activity1'][i],'confidence1':original['dataSource']['confidence1'][i],'activity2':original['dataSource']['activity2'][i],'confidence2':original['dataSource']['confidence2'][i],'file':archivo}, ignore_index=True)          
     