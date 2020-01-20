#! venv/bin/ python3
# *-encoding: utf8 -*

import requests as rqs
from bs4 import BeautifulSoup
import datetime
import time


def unixTimeStampConvert(num):
    convert = datetime.datetime.fromtimestamp(int(num)).strftime('%Y-%m-%d %H:%M:%S')
    return convert

# CONEXION AL SERVIDOR (SITIO WEB), Y REQUEST (PETICION).
# **********************************************************
# A que sitio me quiero conectar, parametro y URI
myurl = "https://votaciones.hcdn.gob.ar"
formQuery = {'anoSearch': -1, 'txtSearch': ''}
endPoint = "https://votaciones.hcdn.gob.ar/votaciones/search"

# Peticion al servidor
r = rqs.post(endPoint, data=formQuery)

# Estado de la conexion
status = r.status_code

if status == 200:
    print(f'Conectando a {myurl}')
    print(f'Estado de la conexion :: {status}')
else:
    print('La conexion no se establecio correctamente')
    print(f'Codigo estado : {status}')
    quit()
# **********************************************************


# Antes de programar el scraper deberiamos saber bien cuanl es el objeto html que contiene la informacion que
# queremos por ejemplo, cual es el tag que contiene la info que queremos.
# podemos identificar el objeto con la informacion a traves del nombre del Tag, del selctor css, "class", del id, etc

# El elemento que me interesa tiene la clase "row-acta"
clase = "row-acta"

# Creo el objeto BeautifulSoup
soup = BeautifulSoup(r.content, 'html.parser')

# El tipo de dato es un result set de beautiful soup, es un iterable, algo asi como una lista
datos = soup.find_all("tr", class_=clase)

# Por cada "tr" tag tenemos sus atributos id, class, data-date, row-number etc
urlActas = list()
for t in datos:
    # Columnas
    cols = t.find_all('td')
    idActa = t['id'],  # Seria Clave principal
    date = unixTimeStampConvert(t['data-date']) # Tengo que convertir el formato de la fecha en human friendly =)
    # Me voy a guardar los datos que extraje en una lista de tuplas
    urlActas.append((myurl + cols[4].find('a')['href'], idActa, date))

actas = list()
diputados = list()
votaciones = list()
for a in urlActas:

    r = rqs.get(a[0])
    idActa = a[1]
    dateActa = a[2]
    urlActa = a[0]
    
    soup = BeautifulSoup(r.content, 'html.parser')

    # VAmos a recuperar estos datos -> Período 123 - Reunión 40 - Acta 31
    text = soup.find('h5').text.split('-')
    periodo = text[0].split()[1]
    reunion = text[1].split()[1]
    acta = text[2].split()[1]


    # Acta
    div = soup.find('div', class_='white-box')
    h3 = div.find_all('h3')
    h4 = div.find_all('h4')

    titulo = h4[0].text.strip().lower()
    presidente = h4[1].find('b').text
    resolucion = h3[0].text

#    ul = div.find_all('ul')
#    afirmativos = ul[2].find('h3').text
#    negativos = ul[3].find('h3').text
#    abstenciones = ul[4].find('h3').text
#    ausentes = ul[5].find('h3').text

    actas.append({
        idActa:{
            'periodo': periodo,
            'reunion': reunion,
            'acta': acta,
            'titulo': titulo,
            'presidente': presidente,
            'resolucion': resolucion
            }}
    )

    # Votacion
    tabla = soup.find('table', id='myTable')
    rows = tabla.find_all('tr')
    idVotacion = '{}-{}-{}'.format(periodo, reunion, acta)
    cunt = 1
    for r in rows:
        cols = [x.text.strip().lower() for x in r.find_all('td')]
        if cols:
            voto = cols[4]
            dichos = cols[5]

        votaciones.append({
            idVotacion: {
                'idVoto': count,
                'voto': voto,
                'acta': idActa,
                'dip': idDip
                'dichos': dichos
                }
            }
        )
        count += 1




# *************************************************+
# END
# Realmente no se como lo manejan desde Nacion, pero se me ocurre para mi trabajo que esta es la mejor
# manera de ordenar los datos y claves para generar las tablas

"idActa": {
    'periodo': periodo,
    'reunion': reunion,
    'acta': acta,
    'titulo': titulo,
    'presidente': presidente,
    'resolucion': resolucion
}

"idDip": {
    'nombre': nomb,
    'apellido': ap,
    'bloque': bloque,
    'provincia': provincia,
}
# El idVotacion lo voy a contruir con estos datos Período 123 - Reunión 40 - Acta 31
# quedadando para cada votacion o sesion o acto o como quiera llamarse un idVotacion como este 123-40-31
# por ultimo el idVoto puede ser simplemente un autoincrementable ya que lo importante es el voto,
# y a que acta y diputado corresponde

"idVotacion": {
    'idVoto': idVoto,
    'voto': voto,
    'acta': idActa,
    'user': idDip
}

bloques = {
    'idBloque': {
        'nombre': 'nombreBloque'
    }
}
provincias={
    'idProvicia':{
        'nombre':'nobre'
    }
}

