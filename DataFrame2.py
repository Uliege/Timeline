# -*- coding: utf-8 -*-


import pandas as pd
import glob
import pyreadr


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
       original['dataSource']= original['dataSource'].drop( original['dataSource'][((original['dataSource']['latitude']>=-0.19425) | (original['dataSource']['latitude'] <= -0.20341))|(( original['dataSource']['longitude']>=-78.49805 )|(original['dataSource']['longitude'] <= -78.51377))].index)

         
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
tabla_final_uce["Segundo"]= separador[2] 
  

tabla_final_uce.drop(columns =["dateTimeLine"], inplace = True) 

#Etiquetar con el nombre del dia de la semana
Nombre_Dia=[]

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