'''
crear libros

ejecutar:

python manage.py shell < datos/crear_libros.py
'''

from libros.models import Libro
from django.utils.text import slugify
import json
import os

#lista de libros del json
libros = json.load(open("datos_libros.json"))

'''
  {
    "title": "¿Dónde están los niños?",
    "author": "Mary Higgins Clark",
    "summary": "Nancy Harmon, joven casada y madre de dos hijos, es acusada injustamente del asesinato de los pequeños, pero el fiscal debe retirar los cargos tras la desaparición del único testigo. La pesadilla se vuelve más aterradora cuando el marido de Nancy se suicida y ella, destrozada, se traslada a Cape Cod. En su nueva residencia, Nancy conoce a Ray Eldredge, con quien se casa.",
    "imagen": "https://m.media-amazon.com/images/I/513wZ4KvnSL.jpg"
  },
'''

for l1 in libros:
    l = Libro()
    l.title = l1["title"]
    l.author = l1["author"]
    l.summary = l1["summary"]
    l.imagen = l1["imagen"]
    l.slug = slugify(f'{l.title} ({l.author})')
    l.save()
