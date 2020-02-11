library(jsonlite)

############################################################################
#Especifica directorio donde estan los JSON#
directorio = "C:/Users/Marcos/Desktop/Final/Tesis/Datos/prueba"

#Nombre del archivo json a deserializar#
archivo = "datosTimeline1.json"

 

########################################################################################
#ld <- list.dirs('C:/Users/Marcos/Desktop/Final/Tesis/Datos', recursive = FALSE)
#for (i in ld) {
#  lf <- list.files(i)
#  for (j in lf) {
    # Procesar el archivo j
#  archivo =  j
 # }
#}

#######################################################################
#Funcion para cargar directorio con archivo y deserializar#
Cargar<-function(directorio,datos){
  enlace <- file.path(directorio, datos)
  dataFile <- fromJSON(enlace)
}
#Guardamos el resultado de la funcion en una variable#
dataFile <- Cargar(directorio,archivo)


###############################################################################
#Guardamos las variables de primer nivel del JSON deserializado en variables con similar nombre#
#a como esta en las variables que proporciona el timeline de google#
timestampMs3 <- as.numeric(dataFile$locations$timestampMs)
timestampMs <- as.POSIXct(timestampMs3/1000, origin="1970-01-01") #esta forma solo muestra la fecha con la hora
#as.Date(as.POSIXct(value/1000, origin="1970-01-01")) #esta forma solo muestra la fecha
latitudeE7 <- dataFile$locations$latitudeE7/1e7  #1e7 = 10000000 eje y coordenadas
longitudeE7 <- dataFile$locations$longitudeE7/1e7 #1e7 = 10000000 eje x coordenadas
accuracy <- dataFile$locations$accuracy
#La precisión es la estimación de Google de la precisión de los datos.(metros)
#Una precisión de menos de 800 es alta y más de 5000 es baja.
altitude <- dataFile$locations$altitude
#Esto podría referirse a la altitud del dispositivo. 
#Supongo que se mide desde el nivel del mar
verticalAccuracy <- dataFile$locations$verticalAccuracy
#Esto podría referirse a la precisión de la ubicación vertical del dispositivo. (metros)
velocity <- dataFile$locations$velocity
#Esto podría referirse a la velocidad del dispositivo en el momento de la captura (metros/segundo)
heading <- dataFile$locations$heading
#La dirección en la que viaja el dispositivo.
#https://www.chipoglesby.com/2018/03/2018-analyzing-google-location-historyII/
#https://shiring.github.io/maps/2016/12/30/Standortverlauf_post

"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
#Bucle para guardar variables del JSON a partir del segundo nivel de vector V1 es el tiempo en que 
#se cogio la actividad 
v1 = NULL
for (i in 1:length(timestampMs)) {
  if (i <= length(timestampMs)) {
    timestampMs4 <- as.numeric(max(dataFile$locations$activity[[i]]$timestampMs[[1]]))
    timestampMs2 <- as.POSIXct(timestampMs4/1000, origin="1970-01-01") #esta forma solo muestra la fecha con la hora
      v1 = rbind(v1, data.frame(timestampMs2))
      i <- i + 1
    "print(timestampMs2)"
  }
  else{
    break
  }
}

"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
#Bucle para guardar variables del JSON a partir del segundo nivel de vector V2 y V3 que son los
#activides y su confiabilidad respectivamente
v2 = NULL
j = 1 #contador para ubicar la posicion de UNKNOWN
for (i in 1:length(timestampMs)) {
  if (i <= length(timestampMs)) {
    if (is.null(dataFile$locations$activity[[i]]$activity[[1]]$type)) {
      type <- max(dataFile$locations$activity[[i]]$type[[1]])
      confidence <-
        max(dataFile$locations$activity[[i]]$confidence[[1]])
      if (type == "-Inf") {
        type = NA
        confidence = NA
        v2 = rbind(v2, data.frame(type, confidence))
        i <- i + 1
      } else{
        if (type == "UNKNOWN") {
          while (type == "UNKNOWN") {
            j <- j + 1
            type <- max(dataFile$locations$activity[[i]]$type[[j]])
            confidence <-
              max(dataFile$locations$activity[[i]]$confidence[[j]])
            v2 = rbind(v2, data.frame(type, confidence))
            i <- i + 1
          }
          j = 1
        } else{
          v2 = rbind(v2, data.frame(type, confidence))
          i <- i + 1
        }
      }
    } else{
      type <-
        max(dataFile$locations$activity[[i]]$activity[[1]]$type[[1]])
      confidence <-
        max(dataFile$locations$activity[[i]]$activity[[1]]$confidence[[1]])
      if (type == "-Inf") {
        type = NA
        confidence = NA
        v2 = rbind(v2, data.frame(type, confidence))
        i <- i + 1
      } else{
        if (type == "UNKNOWN") {
          while (type == "UNKNOWN") {
            j <- j + 1
            type <-
              max(dataFile$locations$activity[[i]]$activity[[1]]$type[[j]])
            confidence <-
              max(dataFile$locations$activity[[i]]$activity[[1]]$confidence[[j]])
            v2 = rbind(v2, data.frame(type, confidence))
            i <- i + 1
          }
          j = 1
        } else{
          v2 = rbind(v2, data.frame(type, confidence))
          i <- i + 1
        }
      }
    }
    "print(type)"
  } else{
    break
  }
}


"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
#Parte 1 y Parte 2 son dataframes de las variables antes mencionadas
parte1 <-
  data.frame(
    timestampMs,
    latitudeE7,
    longitudeE7,
    accuracy,
    altitude,
    verticalAccuracy,
    velocity,
    heading
  )

parte2 <- data.frame(v1, v2)


##################################################################################################
#Funcion para crear una tabla general a partir de los dataframes anteriores#
#y luego de crearlo adjunta nuevos datos de distintos archivos en la misma tabla creada #
Proceso <- function(variables1,variables2){
  if(!exists("TablaFinal")){
    TablaFinal<- data.frame(variables1,variables2)
  }else{
    lista<- data.frame(variables1,variables2)
    TablaFinal <- rbind(TablaFinal,lista)
  }
}

#Invocamos y guardamos el resultado de la funcion en una variable#
TablaFinal <-Proceso(parte1,parte2)


"options(max.print=100)"
###############################################################################



