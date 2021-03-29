'use strict';

const express = require('express');

// Configuración de red
const PORT = 8080;
const HOST = '0.0.0.0';

// Ejecución de la aplicación web
const app = express();
app.get('/', (req, res) => {
  res.send('¡Saludos desde el webminar de Cisco DevNet! Soy una aplicación web de Nodejs montada en un contenedor de Docker ...');
});

app.listen(PORT, HOST);
console.log(`Web app activa en http://${HOST}:${PORT}`);