'''
crear películas
ejecutar:
python manage.py shell < datos/extraer_libros.py
'''

import requests
from lxml import html
import json

url = "https://mapadelibros.es/libros-recomendados/100-libros-llevados-al-cine/"
r = requests.get(url)
pagina = html.fromstring(r.text)

lista = pagina.xpath('.//div[@class="td-post-content tagdiv-type"]')
libros = lista[0].xpath('.//div[@class="wp-block-group"]')

def datos_libro(libro):

    tituloyautor = libro[0].xpath('.//h3[@class="has-text-align-center"]/text()')[0]
    descripcion = libro[0].xpath('.//div[@class="aawp-product__description"]/text()')[0]
    title = tituloyautor.partition("–")[0].strip()
    author = tituloyautor.partition("–")[2].strip()
    summary = descripcion.strip()
    imagen = libro[0].xpath(".//img/@src")[0]
   
    # datos a devolver
    datos = {}
    # titulo
    datos['title'] = title

    #autor
    datos['author'] = author

    #sinopsis
    datos['summary'] = summary
    
    #imagen
    datos['imagen'] = imagen

    return datos

datos = [datos_libro(l) for l in libros]
json.dump(datos, open('datos_libros.json', 'w'), ensure_ascii=False)

    