# Despliegue de sistemas
# Caso de uso: Montar un contenedor (Docker) con una aplicación web en Node.js

## Instrucciones de DEMO
1. Creación de la aplicación web
2. Creación del archivo Dockerfile
3. Creación del archivo .dockerignore
4. Creación de la imagen de nuestra aplicación web
5. Montar la imagen en un contenedor

### 1. Creación de la aplicación web

Los componentes mínimos de una aplicación web en Node.js son el archivo que define y ejecuta al servidor web, así como el archivo *package.json* el cual contiene las especificaciones de la aplicación. 

Para el propósito de esta demo. Ambos ya están creados.


### 2. Creación del archivo Dockerfile

¿Cómo le indicamos a Docker qué hacer? Es decir, ¿qué tipo de plataforma instalar para correr nuestra app, dónde montar la app, cuáles puertos abrir, etc? El archivo Dockerfile nos ayudará para dar dichas indicaciones. El contenido es el siguiente:

``` 
# La imagen en la cual queremos apoyarnos para que se ejecute nuestra app. En este caso es Node v.14. Esta es una imagen descargable y lista de Node. ¡No es necesario instalarlo en el host!
FROM node:14

# Directorio donde se alojará la webapp dentro del contenedor
WORKDIR /usr/src/app

# Copia del archivo package.json para la instalación de todas las dependencias necesarias en el directorio destino
COPY demo_web_app/package.json ./

# Instalación de todas las bibliotecas necesarias para nuestra web app con base en el archivo package.json
RUN npm install

#Copia de todo el contenido de nuestra carpeta demo_web_app a nuestro directorio destino
COPY demo_web_app/. .

#Habilitación del puerto 8080 para que se pueda acceder a nuestra web app
EXPOSE 8080

#Ejecución de la web app
CMD [ "node", "server.js" ]
```

### 3. Creación del archivo .dockerignore

El archivo .dockerignore es útil para no copiar determinados archivos o carpetas a nuestro directorio de la imagen. Normalmente se ignoran archivos como logs o los módulos de node per sé, ya que estos son instalados en el momento en el que se crea una imagen nueva, y copiarlos de la carpeta original puede ser muy tardado.

El contenido es el siguiente:

```
node_modules
npm-debug.log
```


### 4. Creación de la imagen de nuestra aplicación web

Es momento de crear una imagen de nuestra web app para tenerla en nuestro catálogo y poder hacer despliegue en un contenedor después. Para ello, es necesario ejecutar el siguiente comando en el mismo directorio de nuestro archivo *Dockerfile*:

```
docker build -t <tu_usuario>/demo_web_app .
```

Ahora, ¡la imagen existe en nuestro catálogo y está lista para usarse! Puedes revisar tu catálogo con el siguiente comando:

```
docker images
```


### 5. Montar la imagen en un contenedor

¡Traigamos a la vida a nuestro contenedor! Para ello, usaremos el puerto 4001 mapeado a nuestro puerto 8080 con el siguiente comando:

```
docker run -p 4001:8080 -d <tu_usuario>/demo_web_app
```

Al entrar a un navegador web en la dirección http://<ip_del_host>:4001, debe abrirse una página web con el mensaje *¡Saludos desde el webminar de Cisco DevNet! Soy una aplicación web de Nodejs montada en un contenedor de Docker ...*.

Es posible verificar detalles del contenedor con el siguiente comando:

```
docker ps
```

Finalmente, para detener este contenedor en específico, puede ocuparse el id o nombre recopilados del comando *docker ps* con el siguiente comando:

```
docker stop <id_o_nombre_del_contenedor>
```