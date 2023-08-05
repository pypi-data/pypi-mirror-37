**************
API MIDDLEWARE
**************
La aplicacion utiliza la libreria `PYJWT <https://github.com/jpadilla/pyjwt/>`_ para agregar un token a cada request y a cada response mediante un middleware personalizado.

Instalacion
============
Agregar a la lista de aplicaciones.

.. code-block::

    INSTALLED_APPS = [
        ...
        'authorized'
    ]

Agregar el middleware **al inicio** de la lista.

.. code-block::

    MIDDLEWARE = [
        'authorized.middleware.APIAuthRequestMiddleware',
        ...
    ]

Agregar las variables ***Requerido**

En el archivo `settings.py` agregar las variables.

.. code-block::

    APP_NAME = 'Awesome App'
    IGNORED_PATHS = []

En el archivo `docker-compose.yml`

.. code-block::

    service:
    ...
    environment:
        - APP_KEY=secret

Aplicar las migraciones del middleware.

.. code-block::

    $ python manage.py migrate authorized

Uso
=====
Requests
########
Para que el middleware funcione se necesita agregar el header
:: 

    'Application-Token':token 

Para evitar hacerlo se creo una "mascara" de la libreria `python requests <http://docs.python-requests.org/en/master/>`_ que agrega el token automaticamente, sin alterar su funcionalidad.
Importar el modulo.
::

    from authorized import api_request

hacer los request de forma normal, ie.
::
    
    api_request.get('url', params)

Todos los metodos de python requests estan disponibles en el modulo api_request:

- get
- post
- put
- patch
- delete
- options
- head

Para peticiones a aplicaciones externas se debe especificar en cada metodo el parametro `is_external=True`, por defecto el valor es `False`, esto previene que el middleware evalue que la respuesta provenga de una fuente confiable.

.. code-block::
    
    api_request.get('https://jsonplaceholder.typicode.com/posts/1', is_external=True)


Informacion adicional sobre python requests consultar `Aqui <http://docs.python-requests.org/en/master/>`_

Correr Tests
=============
Para ejecutar los tests de la aplicacion `authorized`, ejecutar el comando.

.. code-block::

    python manage.py test authorized
