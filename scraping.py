#!/usr/bin/python
# *-encoding: utf8 -*


import datetime
import requests as rqs
from bs4 import BeautifulSoup


def unixTimeStampConvert(num):
    convert = datetime.datetime.fromtimestamp(int(num)).strftime('%Y-%m-%d %H:%M:%S')
    return convert


# CONEXION AL SERVIDOR (SITIO WEB), Y REQUEST (PETICION).
# **********************************************************
myurl = "https://votaciones.hcdn.gob.ar"

# Los siguientes datos los saque de la misma pagina, mirando el codigo fuente para ver
# como enviaba las peticiones y cual debia enviar para obtener todos los datos =)
formQuery = {'anoSearch': -1, 'txtSearch': ''}
endPoint = "https://votaciones.hcdn.gob.ar/votaciones/search"

# Peticion al servidor
r = rqs.post(endPoint, data=formQuery)

# Estado de la conexion
status = r.status_code

# Check del status code
if status == 200:
    print(f'Conectando a {myurl}')
    print(f'Estado de la conexion :: {status}')
else:
    print('La conexion no se establecio correctamente')
    print(f'Codigo estado : {status}')
    quit()
# **********************************************************

# Antes de empezar a programar el scraper debemos mirar con atencion el codigo de la pagina que vamos a escrapear.
# Es bueno tambien, ver como se comporta la pagina a partir de los eventos de click, scroll o cuando envia formularios. 
# Haciendo este analisis podemos detectar comportamientos que querriamos capturar o manipular con el objeto de llegar a la informacion necesaria.
# En este caso el objeto html o tag que contiene la informacion que queremos extraer. 
# Para este caso el elemento que tiene la informacion que quiero es el tag <tr></tr> con el attributo clase="row-acta"

clase = "row-acta"

# Creo el objeto BeautifulSoup
soup = BeautifulSoup(r.content, 'html.parser')

# Uso la libreria bs4 para buscar en el cuerpo html de la pagina el contenedor <tr> que tiene la clase que busco.
# El tipo de dato es un result set de beautiful soup, un iterable con el objeto y sus decendientes
datos = soup.find_all("tr", class_=clase)

# EXTRACCION DE LAS URLS DONDE ESTAN LOS DETALLES DE CADA VOTACION
# **********************************************************
urlActas = list()
for t in datos:
    # Columnas
    cols = t.find_all('td')
    idActa = t['id'],  # Seria Clave principal
    date = unixTimeStampConvert(t['data-date'])  # Tengo que convertir el formato de la fecha en human friendly =)
    # Me voy a guardar los datos que extraje en una lista de tuplas
    urlActas.append((myurl + cols[4].find('a')['href'], idActa, date))
# **********************************************************

# RECORRIDO DE LAS ACTAS Y SCRAPING DE LOS DETALLES - ACTAS Y VOTACION
# **********************************************************
actas = list()
votos = list()
count = 1
ctrlCount = 0
for a in urlActas:
    # Conexion a cada Acta # *********************************
    r = rqs.get(a[0])
    soup = BeautifulSoup(r.content, 'html.parser')

    # idActa = a[1] este es el id que figura en el sitio, pero voy a usar otro
    dateActa = a[2]
    urlActa = a[0]

    # VAmos a recuperar estos datos -> Período 123 - Reunión 40 - Acta 31
    try:
        text = soup.find('h5').text.split('-')
        checkPoint_1 = True
    except AttributeError:
        checkPoint_1 = False
        text = ['- None', '- None', '- None']

    periodo = text[0].split()[1]
    reunion = text[1].split()[1]
    numeroActa = text[2].split()[1]
    idSite = a[1]
    idActa = '{}-{}-{}'.format(periodo, reunion, numeroActa)

    # Acta # *********************************
    div = soup.find('div', class_='white-box')
    if div:
        h3 = div.find_all('h3')
        h4 = div.find_all('h4')
        try:
            titulo = h4[0].text.strip().lower()
            presidente = h4[1].find('b').text
            resolucion = h3[0].text
            checkPoint_2 = True
        except AttributeError:
            checkPoint_2 = False
            titulo = None
            presidente = None
            resolucion = None
    else:
        continue

    if not checkPoint_1:
        if not checkPoint_2:
            continue

    actas.append({
        'idActa': idActa,
        'fechaActa': dateActa,
        'periodo': periodo,
        'reunion': reunion,
        'numeroActa': numeroActa,
        'titulo': titulo,
        'presidente': presidente,
        'resolucion': resolucion,
        'urlActa': urlActa,
        'idSite': idSite
    }
    )

    # Votacion # *********************************
    tabla = soup.find('table', id='myTable')
    rows = tabla.find_all('tr')
    #     count = 1
    for r in rows:
        cols = [x for x in r.find_all('td')]
        if cols:
            try:
                idDip = cols[0].find('div')['id'].split('-')[1]
            except TypeError:
                idDip = None
                pass

            voto = cols[4].text.strip().lower()
            dichos = cols[5].text.strip().lower()

            votos.append({
                'idActa': idActa,
                'idVoto': count,
                'voto': voto,
                'numeroActa': numeroActa,
                'dip': idDip,
                'dichos': dichos
            })
            count += 1

    ctrlCount += 1

#     if not votos:
#         continue
#     else:
#         votaciones.append(votos)

#     time.sleep(1)
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

# Insersion de los registros en la Base de Datos.
diputados
actas
votos

# Output *****************************************************
# diputados_till_25012020 = pd.DataFrame([x for x in diputados])
# actas_till_25012020 = pd.DataFrame([x for x in actas])
# votos_till_25012020 = pd.DataFrame([x for x in votos]).rename(columns={'dip': 'idDip'})

# diputados_till_25012020.to_csv('diputados_till_25012020.csv', index=False)
# actas_till_25012020.to_csv('actas_till_25012020.csv', index=False)
# votos_till_25012020.to_csv('votos_till_25012020.csv', index=False)

