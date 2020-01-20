#! venv/bin/ python3
# *-encoding: utf8 -*

import requests as rqs
from bs4 import BeautifulSoup
import datetime
import time


def unixTimeStampConvert(num):
    convert = datetime.datetime.fromtimestamp(int(num)).strftime('%Y-%m-%d %H:%M:%S')
    return convert


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

# Antes de programar el scraper deberiamos saber bien cuanl es el objeto html que contiene la informacion que
# queremos y cuanta inforamcion estamos necesitando, por ejemplo, cual es el tag que contiene la info y cuantos tags
# vamos a scrapear Si lo sabemos, vamos a definir el id del objeto que buscamos

# este es un ejemplo sacado de la pagina que voy a scrrapear
# <tr id="3951" class="row-acta" data-date="1576842624" row-number="9" style="display: none">

clase = "row-acta"
print(f'La clase buscada es {clase}')
# Creo el objeto BeautifulSoup
soup = BeautifulSoup(r.content, 'html.parser')

# El tipo de dato es un resutl set de beautiful soup, es un iterable
datos = soup.find_all("tr", class_=clase)
print(f'La longitud del set de resultados es {len(datos)}')

# Por cada "tr" tag tenemos sus atributos id, class, data-date, row-number etc
urlActas = list()

for t in datos:
    # Columnas
    cols = t.find_all('td')
    idActa = t['id'],  # Seria Clave principal
    date = unixTimeStampConvert(t['data-date'])

    urlActas.append((myurl + cols[4].find('a')['href'], idActa, date))

for a in urlActas:

    r = rqs.get(a[0])
    idActa = a[1]
    dateActa = a[2]

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
    h5 = div.find_all('h5')

    titulo = h4[0].text.strip().lower()
    presidente = h4[1].find('b').text
    resolucion = h3[0].text

    ul = div.find_all('ul')
    afirmativos = ul[2].find('h3').text
    negativos = ul[3].find('h3').text
    abstenciones = ul[4].find('h3').text
    ausentes = ul[5].find('h3').text

    print(titulo)
    print(presidente)
    print(resolucion)
    print(afirmativos)
    print(negativos)
    print(abstenciones)
    print(ausentes)

    #     print(ul)

    print('*********')
    break

    # Diputados
    tabla = soup.find('table', id='myTable')
    rows = tabla.find_all('tr')

    for r in rows:
        cols = [x.text.strip().lower() for x in r.find_all('td')]
        if cols:
            fullNomb = cols[1].split(',')
            nomb = fullNomb[0]
            ap = fullNomb[1]
            bloque = cols[2]
            provincia = cols[3]
            voto = cols[4]
            dichos = cols[5]

            print(nomb)
            print(ap)
            print(bloque)
            print(provincia)
            print(voto)
            print('**********')

    break

