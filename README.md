

## Proyecto 2º trimestre

 **Enunciado**

Actualizar el proyecto "Blog de clase" (*fork del tutorial de wagtail del profesor*) y añadir varios apartados.

Todo el esqueleto de la web está en el *base.html* que a su vez va incluyendo al resto de plantillas. En el navbar encontraremos los distintos apartados por los que movernos. La propia página principal, a modo de imitar a un Blog, ya muestra todos los post originados en el mismo. Además, en la parte inferior tendremos las 5 últimas noticias. Entre las pestañas para navegar encontramos: Home (página principal), Blogs (con diferentes entradas entre las que están: genéricas, de libros, de películas y de viajes), Noticias, Peliculas (listado de películas), Libros (listado de libros) y Contacto (formulario web para enviar peticiones).

***  

## **Instalación**

user:mariaestmag pass:password

1) Clona el repositorio o descárgalo directamente:  
   
  ```bash 
  https://github.com/mariaestmag/tutorial_wagtail.git 
  ```

2) Una vez desargado, ábrelo, crea tu propio entorno virtual y actívalo:

```bash 
python3 -m venv env

source env/bin/activate
  ```

3) Instala los requisitos:

```bash
pip install -r requirements.txt
```   
4) Generar la estructura de la base de datos:   

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```  

5) Despliega el servidor:
   
```bash
python3 manage.py runserver
```  


***
