import urllib.request,unicodedata,_thread
import re
import time
from datetime import datetime,timedelta
from bs4 import BeautifulSoup
from dateutil import parser

class ProgramasTelevisivos():

	def __init__(self):
		self.url = "https://ecoteuve.eleconomista.es"
		self.subdomainCanales = "/canales/"
		self.subdomainProgramacion = "/audiencias-programas/"
		self.datos =[]
		self.datosTotales =[]
		self.k=0
		self.kTotales=0


	def presentacion(self):
		start_time = time.strftime("%H:%M:%S") 
		print("Bienvenidos al web scraping de " + self.url)
		print("Inicio del programa: " + str(start_time) + " hrs.")


	def fin(self):
		end_time = time.strftime("%H:%M:%S") 
		print("Fin del programa: " + str(end_time) + " hrs.")


	# Busca y muestra el archivo robot del sitio
	def mostrarArchivoRobots(self):
		html = self.descargar_html("https://www.eleconomista.es/robots.txt")
		soup  = BeautifulSoup(html, 'html.parser')
		print ("Archivo robots.txt")
		print (soup)
		print ("Fin archivo robots.txt")
		


	# Busca la lista de canales que se recorreran
	# para la obtencion de la informacion
	def buscaLista(self):
		html = self.descargar_html(self.url + self.subdomainCanales)
		soup  = BeautifulSoup(html, 'html.parser')
		#print (soup)

		listaCanales = re.findall('href="(/cadena/.*?)"', str(soup))

		#Mostramos en pantalla la lista de canales que analizaremos
		print("La lista de canales es la siguiente: ")

		tmLista = sorted(list(set(listaCanales)))
		for enlace in tmLista:
		    print (self.url + enlace)

		return tmLista


	# Obtiene el Html de la url consultada
	# Tambien cambiamos el user_agent que viene por defecto
	def descargar_html(self, url):
		user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
		headers = {'User-Agent': user_agent}
		request = urllib.request.Request(url,headers=headers)
		response = urllib.request.urlopen(request)
		html = response.read()
		return html
		

	# Guarda en un array los link de los distintos canales
	# que se recorreran para buscar la informacion
	def urlListaAudiencia(self,listaCanales):
		lista = []
		mesAnio = datetime.now().strftime("%Y-%m")
		dia = datetime.now()
		finDia = dia.strftime("%d") #Obtiene el dia de hoy

		inicio = int(finDia) - 3 # el valor 3 define la cantidad de dias en los cuales se obtendra la informacion
		if inicio < 1:
			inicio =1

		for link in listaCanales:
			for i in range(inicio,int(finDia)): #Obtiene los dias del mes que obtendra informacion
				if i < 10:
					strDia = "0"+str(i)
				else:
					strDia = str(i)
				fecha =  mesAnio+"-"+strDia
				linkAudiencias = self.url + link + self.subdomainProgramacion + fecha
				lista.append(linkAudiencias+";"+fecha+";"+link)
			 	
		return lista
		
	
	# Transformacion de dato a utf-8
	def byte_to_str(self,bytes_or_str):
		if isinstance(bytes_or_str, bytes): #check if its in bytes
			return bytes_or_str.decode('utf-8')
		else:
			return bytes_or_str


	# Obtiene la informacion del link que se le envia
	# Esta informacion es sobre la audiencia por canal 
	# y sobre los programas relacionados
	def descargaAudiencia(self,enlace):

		dat = enlace.split(";")
		link = dat[0]
		fecha = dat[1]
		canal = dat[2].split("/")[2]

		html = self.descargar_html(link)
		soup  = BeautifulSoup(html, 'html.parser')	
		mydiv = soup.findAll("div", {"class": "tabla2"})
		#k=0
		rows = mydiv[0].findAll('tr')
		for row in rows:
			tds = row.findAll('td')
			self.datos.append([])
			j=0
			for td in tds:
				if j==0:
					self.datos[self.k].append(fecha)
					self.datos[self.k].append(canal)
				self.datos[self.k].append(td.text.encode("utf-8") )
				j+=1
			self.k += 1

		myspan = soup.findAll("span", {"class": "share-acumulado"})	
		for row in myspan:
			print("myspan: "+self.byte_to_str(row.text.encode("utf-8")))
			porcentaje = ""
			porcentaje = row.text
			porcentaje = porcentaje.replace("Share día: ","").replace("Share dĂ­a: ","").replace("%","")
			self.datosTotales.append([])
			self.datosTotales[self.kTotales].append(fecha)
			self.datosTotales[self.kTotales].append(canal)
			self.datosTotales[self.kTotales].append(porcentaje.encode("utf-8") )
			self.kTotales += 1
			
		
	# Muestra en pantalla la informacion obtenida
	# de los distintos canales y sus programas
	def mostrarDatos(self):
		for i in range(len(self.datos)):
			for j in range(len(self.datos[i])):
				print(self.datos[i][j])


					
	# Guarda la informacion en archivos de salida
	# de tipo .csv
	def guardarDatos(self, filename,filename2):
		file = open("../csv/" + filename, "w+");
		i = 0;
		j = 0;
		file.write("Fecha;Canal;Hora;Programa;Espectadores;Share(%);\n");
		for i in range(len(self.datos)):
			count = 0
			for j in range(len(self.datos[i])):
				dd=self.byte_to_str((self.datos[i][j]))
				file.write(dd+ ';') 
				
				count+=1;
			if count > 0:
				file.write("\n");
			
		file = open("../csv/" + filename2, "w+");
		i = 0;
		j = 0;
	
		file.write("Fecha;Canal;Share(%);\n");
		for i in range(len(self.datosTotales)):
			count = 0
			for j in range(len(self.datosTotales[i])):
				dd=self.byte_to_str((self.datosTotales[i][j]))
				file.write(dd+ ';') 
				
				count+=1;
			if count > 0:
				file.write("\n");
