# Uso de APIs

## Instrucciones de DEMO
1. Instalar requests dentro del entorno
2. Usar requests para postear un mensaje en WebEx teams

### 1. Instalar requests dentro del entorno
Si listamos las librerias dentro del entorno virtual, nos daremos cuenta que no tiene ninguna libreria adicional instalada:

``` 
(venv) ➜  api_use_pillar pip freeze
(venv) ➜  api_use_pillar 
```

Instalaremos requests con el siguiente comando:

``` 
pip install requests
```

Una vez instalado, volvemos a listar las librerias:
``` 
(venv) ➜  api_use_pillar pip freeze          
certifi==2020.12.5
chardet==4.0.0
idna==2.10
requests==2.25.1
urllib3==1.26.4
(venv) ➜  api_use_pillar 
``` 
### 2. Usar requests para postear un mensaje en WebEx teams

Primero echemos un vistazo a la API de WebEx teams:
https://developer.webex.com/docs/api/v1/messages

Para crear un mensaje, ocuparemos el endpoint /messages

POST /v1/messages
> create_message.py

Nos pide dos cosas importantes, un BEARER ACCESS TOKEN y un ROOM ID

Para obtener el BEARER ACCESS TOKEN, creamos un bot y obtenemos el token:
https://developer.webex.com/my-apps/new/bot

Para obtener el room, podemos agregar el bot que recien creamos, y despues utilizamos la API para obtener el room ID:
https://developer.webex.com/docs/api/v1/rooms/list-rooms




