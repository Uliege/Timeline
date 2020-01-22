# -*- coding: utf-8 -*-
import json
import pandas as pd
import glob

from datetime import datetime


directorio_entrada="/home/milton.moncayo/SmartGPS/timeline/"
directorio_salida="/home/milton.moncayo/SmartGPS/data/"
archivo_salida="DataSmart.dat"
archivo_salida_completo="DataSmartCompleto.dat"
tabla_variables=pd.DataFrame()
tabla_tiempo_actividades=pd.DataFrame()
tabla_actividades=pd.DataFrame()
tabla_final_uce=pd.DataFrame()
tabla_final_completa=pd.DataFrame()
for k in range(1,len(glob.glob(directorio_entrada+"*.json"))+1):        
        archivo="datosTimeline"+str(k)+".json"
        enlace=directorio_entrada + archivo
        if('tabla_variables' not in globals() and 'tabla_tiempo_actividades' not in globals() and 'tabla_actividades' not in globals() ):
                tabla_variables = pd.DataFrame(columns=['timestampMs','latitudeE7','longitudeE7','accuracy','altitude','verticalAccuracy','velocity','heading'])
                tabla_tiempo_actividades = pd.DataFrame(columns=['timestampMs2'])
                tabla_actividades= pd.DataFrame( columns=['type1','confidence1','type2','confidence2','type3','confidence3'])
                tabla_final_uce=pd.DataFrame(columns=[])
                tabla_final_completa=pd.DataFrame(columns=[])
        with open(enlace, "r") as read_file:
            data = json.load(read_file)
###############################################################################        
            for i in data['locations']:
                   tiempo=(int(i.get('timestampMs'))/1000)
                   tiempoformato = datetime.utcfromtimestamp(tiempo).strftime('%Y-%m-%d %H:%M:%S')
                   if(i.get('latitudeE7')==None):
                      latitude = None
                   else:
                      latitude=i.get('latitudeE7')/1e7
                      
                   if(i.get('longitudeE7')==None):
                      longitude = None
                   else:
                      longitude=i.get('longitudeE7')/1e7
                   
                   tabla_variables = tabla_variables.append({'timestampMs':tiempoformato,'latitudeE7':latitude,'longitudeE7':longitude,'accuracy':i.get('accuracy'),'altitude':i.get('altitude'),'verticalAccuracy':i.get('verticalAccuracy'),'velocity':i.get('velocity'),'heading':i.get('heading')}, ignore_index=True)          
###############################################################################
            for j in range(0,len(data['locations'])):
                      if('activity' not in data['locations'][j]): 
                         tabla_tiempo_actividades = tabla_tiempo_actividades.append({'timestampMs2':None}, ignore_index=True) 
                      else:
                             if('timestampMs' not in data['locations'][j]['activity'][0]): 
                                 tabla_tiempo_actividades = tabla_tiempo_actividades.append({'timestampMs2':None}, ignore_index=True) 
                             else:
                                tiempo2=(int(data['locations'][j]['activity'][0]['timestampMs'])/1000)
                                tiempoformato2 = datetime.utcfromtimestamp(tiempo2).strftime('%Y-%m-%d %H:%M:%S')
                                tabla_tiempo_actividades = tabla_tiempo_actividades.append({'timestampMs2':tiempoformato2}, ignore_index=True) 
###############################################################################
            for l in range(0,len(data['locations'])):
                      if('activity' not in data['locations'][l]): 
                          tabla_actividades = tabla_actividades.append({'type1':None}, ignore_index=True) 
                      else:
                            if('timestampMs' not in data['locations'][l]['activity'][0]): 
                                            if(len(data['locations'][l]['activity'])==1): 
                                                tabla_actividades = tabla_actividades.append({'type1':data['locations'][l]['activity'][0]['type'],'confidence1':data['locations'][l]['activity'][0]['confidence'],'type2':None,'confidence2':None,'type3':None,'confidence3':None}, ignore_index=True)         
                                            elif(len(data['locations'][l]['activity'])==2):
                                                tabla_actividades = tabla_actividades.append({'type1':data['locations'][l]['activity'][0]['type'],'confidence1':data['locations'][l]['activity'][0]['confidence'],'type2':data['locations'][l]['activity'][1]['type'],'confidence2':data['locations'][l]['activity'][1]['confidence'],'type3':None,'confidence3':None}, ignore_index=True) 
                                            elif(len(data['locations'][l]['activity'])>=3):
                                                tabla_actividades = tabla_actividades.append({'type1':data['locations'][l]['activity'][0]['type'],'confidence1':data['locations'][l]['activity'][0]['confidence'],'type2':data['locations'][l]['activity'][1]['type'],'confidence2':data['locations'][l]['activity'][1]['confidence'],'type3':data['locations'][l]['activity'][2]['type'],'confidence3':data['locations'][l]['activity'][2]['confidence']}, ignore_index=True) 
                                            elif(len(data['locations'][l]['activity'])is None):
                                                tabla_actividades = tabla_actividades.append({'type1':None,'confidence1':None,'type2':None,'confidence2':None,'type3':None,'confidence3':None}, ignore_index=True) 
                            else:
                                      for m in range(0,len(data['locations'][l]['activity'])):
                                               if(len(data['locations'][l]['activity'])==1):                  
                                                        if(len(data['locations'][l]['activity'][m]['activity'])==1):
                                                            tabla_actividades = tabla_actividades.append({'type1':data['locations'][l]['activity'][m]['activity'][0]['type'],'confidence1':data['locations'][l]['activity'][m]['activity'][0]['confidence'],'type2':None,'confidence2':None,'type3':None,'confidence3':None}, ignore_index=True)         
                                                        elif(len(data['locations'][l]['activity'][m]['activity'])==2):
                                                            tabla_actividades = tabla_actividades.append({'type1':data['locations'][l]['activity'][m]['activity'][0]['type'],'confidence1':data['locations'][l]['activity'][m]['activity'][0]['confidence'],'type2':data['locations'][l]['activity'][m]['activity'][1]['type'],'confidence2':data['locations'][l]['activity'][m]['activity'][1]['confidence'],'type3':None,'confidence3':None}, ignore_index=True) 
                                                        elif(len(data['locations'][l]['activity'][m]['activity'])>=3):
                                                            tabla_actividades = tabla_actividades.append({'type1':data['locations'][l]['activity'][m]['activity'][0]['type'],'confidence1':data['locations'][l]['activity'][m]['activity'][0]['confidence'],'type2':data['locations'][l]['activity'][m]['activity'][1]['type'],'confidence2':data['locations'][l]['activity'][m]['activity'][1]['confidence'],'type3':data['locations'][l]['activity'][m]['activity'][2]['type'],'confidence3':data['locations'][l]['activity'][m]['activity'][2]['confidence']}, ignore_index=True)                                         
                                               else:                                           
                                                        if(len(data['locations'][l]['activity'][m]['activity'])==1):
                                                            tabla_actividades = tabla_actividades.append({'type1':data['locations'][l]['activity'][m]['activity'][0]['type'],'confidence1':data['locations'][l]['activity'][m]['activity'][0]['confidence'],'type2':None,'confidence2':None,'type3':None,'confidence3':None}, ignore_index=True)         
                                                            break;
                                                        elif(len(data['locations'][l]['activity'][m]['activity'])==2):
                                                            tabla_actividades = tabla_actividades.append({'type1':data['locations'][l]['activity'][m]['activity'][0]['type'],'confidence1':data['locations'][l]['activity'][m]['activity'][0]['confidence'],'type2':data['locations'][l]['activity'][m]['activity'][1]['type'],'confidence2':data['locations'][l]['activity'][m]['activity'][1]['confidence'],'type3':None,'confidence3':None}, ignore_index=True) 
                                                            break;
                                                        elif(len(data['locations'][l]['activity'][m]['activity'])>=3):
                                                            tabla_actividades = tabla_actividades.append({'type1':data['locations'][l]['activity'][m]['activity'][0]['type'],'confidence1':data['locations'][l]['activity'][m]['activity'][0]['confidence'],'type2':data['locations'][l]['activity'][m]['activity'][1]['type'],'confidence2':data['locations'][l]['activity'][m]['activity'][1]['confidence'],'type3':data['locations'][l]['activity'][m]['activity'][2]['type'],'confidence3':data['locations'][l]['activity'][m]['activity'][2]['confidence']}, ignore_index=True) 
                                                            break;
                                     
######################################################################################
tabla_final_completa= pd.concat([tabla_variables,tabla_tiempo_actividades, tabla_actividades], axis=1, sort=False)                                                            
tabla_final_uce= pd.concat([tabla_variables,tabla_tiempo_actividades, tabla_actividades], axis=1, sort=False)
for p in range(0, len(tabla_final_uce)):
     # if( ((-0.1987368 >= tabla_final['latitudeE7'][p] >= -0.2033572)and (-78.4988855 >= tabla_final['longitudeE7'][p] >= -78.5007168))or((-0.1987368 >= tabla_final['latitudeE7'][p] >= -0.1954364)and (-78.4988855 >= tabla_final['longitudeE7'][p] >= -78.5106577))or((-0.1954364 >= tabla_final['latitudeE7'][p] >= -0.2013516)and (-78.5106577 >= tabla_final['longitudeE7'][p] >= -78.5106805))or((-0.2013516 >= tabla_final['latitudeE7'][p] >= -0.2033572)and(-78.5007168 >= tabla_final['longitudeE7'][p] >=  -78.5106805))):    
       if( ((-0.19425 >= tabla_final_uce['latitudeE7'][p] >= -0.20341)and (-78.49805 >= tabla_final_uce['longitudeE7'][p] >= -78.51377))):    
     
          print(tabla_final_uce['latitudeE7'][p])
       else:
          tabla_final_uce.drop(index=[p], inplace=True)
        #  print("vacio")


tabla_final_uce.to_csv(directorio_salida+archivo_salida) 
tabla_final_completa.to_csv(directorio_salida+archivo_salida_completo)  
#tabla_cargada = pd.read_table(directorio_salida+archivo_salida, sep=",")        
