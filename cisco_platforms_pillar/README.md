# Plataformas de Cisco
# Caso de uso: Configuración de CallManager (CUCM) vía Cisco Administrative XML (AXL) y notificaciones de eventos vía Webex Teams

## Instrucciones de DEMO
1. Habilitar el servicio de Cisco AXL Web Service en CUCM
2. Crear un usuario con el Rol de Standard AXL API Access
3. Descargar el esquema (scheme) de nuestro CallManager
4. Crear un entorno virtual ad-hoc con las bibliotecas necesarias
5. Especificar los detalles del servidor de CUCM a configurar
6. Especificar los detalles del Room de Webex Teams en el cual se subirá el reporte de actividades


### 1. Habilitar el servicio de Cisco AXL Web Service en CUCM

El servicio de Cisco AXL Web Service necesita estar activo en el servidor de CUCM sobre el cual queremos ejecutar nuestra demo. Para ello, es necesario acceder a la siguiente ruta y activar el servicio:

``` 
Cisco Unified Serviceability > Service Activation > (Seleccionar nuestro Pub/Sub) >  Cisco AXL Web Service > Database and Admin Services > Cisco AXL Web Service ✅
```

¿Cómo saber si se activó exitosamente? Es posible acceder a la siguiente dirección en el navegador web: https://<ip_de_cucm>:8443/axl/

Si podemos leer el mensaje *Cisco CallManager: AXL Web Service - The AXL Web Service is working and accepting requests*, estamos listos para operar nuestra demo.


### 2. Crear un usuario con el Rol de Standard AXL API Access

El objetivo es crear un Application User que tenga el Rol de *Standard AXL API Access*. Esto puede lograrse ya sea mediante el Access Control Group preconfigurado de *Standard CCM Super Users*, aunque lo más recomendable es crear un nuevo grupo con dicho rol.

Para ello, es necesario navegar a la siguiente ruta y crear un nuevo Access Control Group con dicho rol:

``` 
Cisco Unified CM Administration > User Management > User settings > Access Control Group
```

Después de ello. Es posible crear un nuevo Application User y asignar dicho grupo en la siguiente rita:

``` 
Cisco Unified CM Administration > User Management > Application User > New User
```


### 3. Descargar el esquema (scheme) de nuestro CallManager

Para poder crear los envelopes SOAP y comunicarse con CUCM, es necesario descargar los archivos que definen cuáles son las operaciones que podemos realizar con esta interfaz. Para el propósito de esta demo, los archivos ya fueron descargados (se encuentran en el folder *schema*), aunque es importante saber que pueden descargarse en la siguiente dirección:

``` 
Cisco Unified CM Administration > Application > Plugins > Cisco AXL toolkit
```


### 4. Crear un entorno virtual ad-hoc con las bibliotecas necesarias

Ejecutaremos esta demo en el contexto de un entorno virtual, de manera que las bibliotecas necesarias solo existan en él.

Para ello, ejecutamos el siguiente comando:

``` 
virtualenv cisco_platforms_pillar_demo
```

Acto seguido, es necesario activarlo con el siguiente comando:

``` 
./cisco_platforms_pillar_demo/Scripts/activate
```

Finalmente, es necesario instalar las siguientes bibliotecas:

``` 
pip install urllib3, zeep, requests
```

¿Cómo corroboramos que se instaló todo lo que necesitamos en nuestro entorno virtual? El output del comando *pip freeze* debe verse así:

``` 
appdirs==1.4.4
attrs==20.3.0
cached-property==1.5.2
certifi==2020.12.5
chardet==4.0.0
defusedxml==0.7.1
idna==2.10
isodate==0.6.0
lxml==4.6.3
pytz==2021.1
requests==2.25.1
requests-file==1.5.1
requests-toolbelt==0.9.1
six==1.15.0
urllib3==1.26.4
zeep==4.0.0
``` 


### 5. Especificar los detalles del servidor de CUCM a configurar

La demo ocupa la clase base *CUCMConnectorAXL.py* para crear una conexión vía SOAP con nuestro CUCM. Puedes encontrar más información de esta clase en https://github.com/ponchotitlan/CUCM-AXL-Connector-class

Así mismo, esta clase está siendo heredada por una clase llamada *JabberCreator.py* para el propósito de esta demo. Los campos de la especificación AXL pueden consultarse en la siguiente liga:
https://developer.cisco.com/docs/axl-schema-reference/

Esta clase está siendo ocupada en el script *cucm_provisioning_teams_notification.py* para provisionar nuestros teléfonos Jabber. 

Lo único que necesitamos cambiar en este último archivo son las tres variables al principio del mismo:

``` 
#Target CUCM server details
CUCM_IP = '<your_cucm_ip>'
CUCM_USERNAME = '<your_cucm_username_AXL_enabled>'
CUCM_PASSWORD = '<your_cucm_password_AXL_enabled>'
``` 


### 6. Especificar los detalles del Room de Webex Teams en el cual se subirá el reporte de actividades

¡Casi listos para comenzar! Finalmente, es necesario especificar los detalles de nuestra conexión a Webex Teams en la misma cabecera del script:

``` 
#Webex Teams room details
TARGET_ROOM_NAME = '<your_room_name>'
GET_ROOMS_API_URL = 'https://webexapis.com/v1/rooms?max=200'
POST_MESSAGE_API_URL = 'https://webexapis.com/v1/messages'
WEBEX_ACCESS_TOKEN = '<your_access_token>'
``` 

¿Dónde consigo mi access token? Es necesario iniciar sesión en esta página para poder copiar un token de desarrollo válido por 12hrs: 

https://developer.webex.com/docs/api/getting-started

El token se encuentra en la sección de *Your Personal Access Token*.