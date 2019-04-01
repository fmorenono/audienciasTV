import time
from rastreo import ProgramasTelevisivos

output_file = "dataset.csv"

rastreo = ProgramasTelevisivos();
rastreo.presentacion();
print "Obtenemos La lista de canales"
listaCanales = rastreo.buscaLista(); #Obtenemos el listado de los canales
lista = rastreo.urlListaAudiencia(listaCanales);
print "Buscamos el link por canal, fecha y descargamos la informacion"

#i=0
# Recorremos el listado de audiencias
for link in lista:
	print(link.split(";")[0]) #Mostramos las url de los datos de las audiencias de los canales por fecha
	rastreo.descargaAudiencia(link) #guarda en array los datos obtenidos
	time.sleep(2) #Retrasa la busqueda en 2 segundos para que no nos bloqueen
	#i+=1
	#if i > 100:
	#	break
	#break 

#rastreo.mostrarDatos();

rastreo.guardarDatos(output_file)
rastreo.fin();
