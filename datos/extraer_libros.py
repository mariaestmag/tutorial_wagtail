import requests
from lxml import html
import json

url = "https://mapadelibros.es/libros-recomendados/100-libros-llevados-al-cine/"
r = requests.get(url)
pagina = html.fromstring(r.text)

lista = pagina.xpath('//div[@class="td-post-content tagdiv-type"]')[0]
libro = lista.xpath('//div[@class="wp-block-group"]')[0]
tituloyautor = libro.xpath('.//h3[@class="has-text-align-center"]')[0] 
tituloyautor.text_content() #van separados por espacio-espacio
titulo = tituloyautor.text_content().split('-')[0]
autor = tituloyautor.text_content().split('-')[1]
imagen = libro.xpath(".//img/@src")[0] #ya contiene la url
descripcion = libro.xpath('.//div[@class="aawp-product__description"]')[0]
resumen = descripcion.text_content().split('\n')