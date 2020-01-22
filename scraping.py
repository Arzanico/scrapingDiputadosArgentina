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
# Los siguientes datos los saque de la misma pagina, mirando el codigo fuente para ver
# como enviaba las peticiones y cual debia enviar para obtener todos los datos =)
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

# EXTRACCION DE LAS URLS DONDE ESTAN LOS DETALLES DE CADA VOTACION
# **********************************************************
urlActas = list()
for t in datos:
    # Columnas
    cols = t.find_all('td')
    idActa = t['id'],  # Seria Clave principal
    date = unixTimeStampConvert(t['data-date']) # Tengo que convertir el formato de la fecha en human friendly =)
    # Me voy a guardar los datos que extraje en una lista de tuplas
    urlActas.append((myurl + cols[4].find('a')['href'], idActa, date))
# **********************************************************

# RECORRIDO DE LAS ACTAS Y SCRAPING DE LOS DETALLES - ACTAS Y VOTACION
# **********************************************************
actas = list()
votaciones = list()
for a in urlActas:
    # Conexion a cada Acta # *********************************
    r = rqs.get(a[0])
    soup = BeautifulSoup(r.content, 'html.parser')

    # idActa = a[1] este es el id que figura en el sitio, pero voy a usar otro
    dateActa = a[2]
    urlActa = a[0]

    # VAmos a recuperar estos datos -> Período 123 - Reunión 40 - Acta 31
    text = soup.find('h5').text.split('-')
    periodo = text[0].split()[1]
    reunion = text[1].split()[1]
    numeroActa = text[2].split()[1]
    idSite = a[1]
    idActa = idVotacion = '{}-{}-{}'.format(periodo, reunion, numeroActa)

    # Acta # *********************************
    div = soup.find('div', class_='white-box')
    h3 = div.find_all('h3')
    h4 = div.find_all('h4')

    titulo = h4[0].text.strip().lower()
    presidente = h4[1].find('b').text
    resolucion = h3[0].text

    actas.append({
            'idActa': idActa,
            'periodo': periodo,
            'reunion': reunion,
            'numeroActa': numeroActa,
            'titulo': titulo,
            'presidente': presidente,
            'resolucion': resolucion,
            'urlActa': urlActa
        }
    )

    # Votacion # *********************************
    tabla = soup.find('table', id='myTable')
    rows = tabla.find_all('tr')
    count = 1
    votos = list()
    for r in rows:
        cols = [x for x in r.find_all('td')]
        if cols:
            try:
                idDip = cols[0].find('div')['id'].split('-')[1]
            except TypeError:
                pass

            voto = cols[4].text.strip().lower()
            dichos = cols[5].text.strip().lower()

            votos.append({
                'idVotacion': idVotacion,
                'idVoto': count,
                'voto': voto,
                'numeroActa': numeroActa,
                'dip': idDip,
                'dichos': dichos
            })
            count += 1

    if not votos:
        continue
    else:
        votaciones.append(votos)

    time.sleep(1)
# **********************************************************

# CONEXION A LA PAGINA DE DONDE VAMOS A SACAR LOS DATOS DE TODOS LOS DIPUTADOS
# Los datos de cada diputado estan en una pagina diferente, por eso voy a hacer nuevas peticiones
# **********************************************************
myurl = "https://votaciones.hcdn.gob.ar"
# Los siguientes datos los saque de la misma pagina, mirando el codigo fuente para ver
# como enviaba las peticiones y cual debia enviar para obtener todos los datos =)
formQuery = {'anoSearchEstadistica': -1}
endPoint = "https://votaciones.hcdn.gob.ar/estadisticas/search"

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

soup = BeautifulSoup(r.content, 'hmlt.parser')
table = soup.find('table', id='myTable')
rows = table.find_all('tr')

diputados = list()
for r in rows:
    cols = r('td')
    if cols:

        idDip = cols[0].find('div')['id'].split('-')[1]
        urlPerf = myurl + cols[1].find('a')['href']
        fullName = cols[1].text.strip()

        if len(fullName) > 0:
            apellido = fullName.split(',')[0]
            nombre = fullName.split(',')[1]
        else:
            apellido = ''
            nombre = ''

        estado = cols[2].text.strip()
        bloque = cols[3].text.strip()
        provincia = cols[4].text.strip()
        afirmativos = cols[5].text.strip()
        negativos = cols[6].text.strip()
        abstenciones = cols[7].text.strip()
        ausencias = cols[8].text.strip()
        presidencias = cols[9].text.strip()

        diputados.append({
                    'idDip': idDip,
                    'urlPerf': urlPerf,
                    'fullName': fullName,
                    'apellido': apellido,
                    'nombre': nombre,
                    'estado': estado,
                    'bloque': bloque,
                    'provincia': provincia,
                    'afirmativos': afirmativos,
                    'negativos': negativos,
                    'abstenciones': abstenciones,
                    'ausencias': ausencias,
                    'presidencias': presidencias
                    }
                )
# **********************************************************

#DETALLES Y ANOTACIONES
# **********************************************************
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

idDip = {
    'nombre': nomb,
    'apellido': ap,
    'bloque': bloque,
    'provincia': provincia,
}
# El idVotacion lo voy a contruir con estos datos Período 123 - Reunión 40 - Acta 31
# quedadando para cada votacion o sesion o acto o como quiera llamarse un idVotacion como este 123-40-31
# por ultimo el idVoto puede ser simplemente un autoincrementable ya que lo importante es el voto,
# y a que acta y diputado corresponde

idVotacion = {
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

