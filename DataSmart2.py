# -*- coding: utf-8 -*-


import pandas as pd
import glob
import pyreadr


#tabla_variables=pd.DataFrame()

directorio_entrada="C:/Users/Andres/Desktop/Tesis/Marcos/Pruebas/"

for k in range(0,len(glob.glob(directorio_entrada+"*.RData")) ): 
    archivo="tld"+str(k)+".RData"
    enlace=directorio_entrada + archivo
    original = pyreadr.read_r(enlace)
    if('tabla_variables' not in globals() ):
         tabla_variables=pd.DataFrame()
         tabla_variables = pd.DataFrame( columns=['dateTimeLine','latitude','longitude','accuracy','altitude','verticalAccuracy','velocity','heading','dateActivity','activity1','confidence1','activity2','confidence2','file'])
    for i in range(0,len(original['dataSource']['dateTimeLine'])): 
                tabla_variables = tabla_variables.append({'dateTimeLine':original['dataSource']['dateTimeLine'][i],'latitude':original['dataSource']['latitude'][i],'longitude':original['dataSource']['longitude'][i],'accuracy':original['dataSource']['accuracy'][i],'verticalAccuracy':original['dataSource']['verticalAccuracy'][i],'altitude':original['dataSource']['altitude'][i],'velocity':original['dataSource']['velocity'][i],'heading':original['dataSource']['heading'][i],'dateActivity':original['dataSource']['dateActivity'][i],'activity1':original['dataSource']['activity1'][i],'confidence1':original['dataSource']['confidence1'][i],'activity2':original['dataSource']['activity2'][i],'confidence2':original['dataSource']['confidence2'][i],'file':archivo}, ignore_index=True)          
     