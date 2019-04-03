# TravelMate

## Setup del proyecto
---------------------
### 1) Base de datos PostgreSQL
1. Instalar la última versión de postgresql en la máquina (Es más sencillo si lo hacéis directamente en la máquina sin usar docker).

2. Una vez instalada, tendréis que ejecutar una consola psql con el superusuario postgres que te crea el instalador, en windows no recuerdo como se hace, para linux dejo los comandos:

    1.  su - postgres
    2.  psql
    
3. Una vez tenemos la consola psql en marcha hay que crearse el usuario travelmate:

    1. create user travelmate with password 'tRaV€lMAt€_$tRoNg';
    
4. Ejecutamos el comando \du y verificamos que el usuario se ha creado correctamente

5. Creamos la base de datos con el comando:

    1. create database travelmate with owner travelmate;
    
6. Ejecutamos el comando \l y verificamos que la base de datos se ha creado correctamente

7. Para salir de la consola psql \q

### 2) Back-end

Entramos en una consola en el directorio "TravelMateServer" desde aquí tenemos acceso al manage.py y al fichero requirements.txt para las dependencias del backend.

* #### Instalar todas las dependencias actuales del requirements.txt

pip3 install -r requirements.txt

* #### Al instalar una nueva dependencia al backend

Una vez que se instale una nueva dependencia al backend (porque necesitáis una app de django externa Ej: rest_framework)
es muy importante que la quedéis reflejada en el requirements.txt, si no, el resto del equipo no podrá ejecutar el backend.

Para ello, si estáis usando un entorno virtual para el proyecto simplemente usad: pip3 freeze > requirements.txt.
En caso de que no estéis usando entorno virtual no existe una manera de añadir una dependencia en concreto al fichero en pip que yo sepa, si alguien sabe que lo diga, pero no hagáis el comando anterior porque entonces pondréis todos los paquetes que tenéis instalado en el python de la propia máquina, probablemente muchos y prácticamente todos innecesarios para ejecutar el backend.

* #### Para ejecutar el backend

python3 ./manage.py runserver

* #### Crear super usuario para poder acceder a http://localhost:8000/admin

En la url especificada se pueden ver los modelos y los objetos que hay en la base de datos. Útil para crear usuarios con los que loguearte en el frontend, nuevos mensajes cuando haya...
    * python3 ./manage.py createsuperuser

* #### Cuando cambias cosas en los modelos

Cuando se cambian cosas en los modelos de django hay que hacer una migración. Para ello:
    * python3 ./manage.py makemigrations (Este solo hace falta si TÚ has hecho los cambios en modelos, si te haces pull de cambios de otra persona no hará falta)
    * python3 ./manage.py migrate


### 3) Front-end
Abrimos una consola en el directirio principal del proyecto

* #### Para ejecutar el frontend

ionic serve

* #### Para crear una nueva página, módulo, servicio, etc

ionic g

* #### Ruta para consumir la API
Creo que José Daniel usa docker por tanto su API del backend estará en la IP: http://192.168.1.135:8000/
Para el resto que no usamos docker nuestra API está en la ip normal: http://localhost:8000/

_¿Qué hay que hacer para que podamos trabajar todos?_

En el fichero src/app/services/restService.ts hay dos líneas de código:

        // this.path = this.config.config().restUrlPrefix;
            this.path = this.config.config().restUrlPrefixLocalhost;
            
Simplemente hay que comentar la 1ª línea si trabajas localhost o la 2ª en caso contrario como José daniel.

## Develop TravelMate
### Front-end
   In the root of the project, you should:
1. Install [node](https://nodejs.org/es/)
2. Next, run ```npm install```
3. And so, ```npm install -g ionic cordova```
4. At last, ```ionic serve```

### To build the app
1. Install [Android Studio](https://developer.android.com/studio)


## Deploy TravelMate
### Back-end
    Make sure you are on branch "master". Commit your changes and push them to the repository.
    Then, in the root of the project, type this command in the shell:
    
    git subtree push --prefix TravelMate-server heroku master

    This will push only the server folder to Heroku.
