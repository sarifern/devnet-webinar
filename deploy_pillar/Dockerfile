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

# Habilitación del puerto 8080 para que se pueda acceder a nuestra web app
EXPOSE 8080

# Ejecución de la web app
CMD [ "node", "server.js" ]