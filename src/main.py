import time
from rastreo import ProgramasTelevisivos

output_file = "dataset.csv"
output_file_total = "canales.csv"

rastreo = ProgramasTelevisivos();
rastreo.presentacion();
rastreo.mostrarArchivoRobots();

print("Obtenemos La lista de canales")
listaCanales = rastreo.buscaLista(); #Obtenemos el listado de los canales
lista = rastreo.urlListaAudiencia(listaCanales);
print("Buscamos el link por canal, fecha y descargamos la informacion")


# Recorremos el listado de audiencias
for link in lista:
	print(link.split(";")[0]) #Mostramos las url de los datos de las audiencias de los canales por fecha
	rastreo.descargaAudiencia(link) #guarda en array los datos obtenidos
	time.sleep(2) #Retrasa la busqueda en 2 segundos para que no nos bloqueen
	 

#rastreo.mostrarDatos();

rastreo.guardarDatos(output_file,output_file_total)
rastreo.fin();
