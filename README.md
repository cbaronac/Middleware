# Middleware

Trabajo presentado por:
Camila Barona 
cbaronac@eafit.edu.co

Santiago Moreno
smorenor@eafit.edu.co

Introducción
En los temas principales que se han visto en la clase de Tópicos especiales en telemática, hemos podido aprender la manera cloud computing, sistemas on premise y servicios nube, además pudimos observar la manera en la cual se utilizaba e implementaba middleware por medio de sockets el cual se decido de esta manera debido a los conocimientos previos que se tenían de la materia Telemática, implementándolo en un proyecto el cual se evidencio el uso del MOM y la manera en la que se hacia el tras paso de mensajes.

Fase: Desarrollo y despliegue
Arquitectura del sistema

![image](https://user-images.githubusercontent.com/41337700/112260824-adfc9180-8c38-11eb-89d2-203cbe792d24.png)

Despliegue del Middleware en AWS

![image](https://user-images.githubusercontent.com/41337700/112260846-b9e85380-8c38-11eb-8f83-a0d1c2d75237.png)

Pruebas finales
Prueba de conexión

![image](https://user-images.githubusercontent.com/41337700/112260906-d4223180-8c38-11eb-9e4c-842d425e0a4b.png)

Pensamientos finales
• Al estructurar primero el problema logramos dar una solución acorde a lo que conocíamos, pero estructurarlo nos abrió el camino para poder lograr construir el proyecto 1.
• Se pudo evidenciar el uso de middleware y como este pudo ayudar al traspaso de mensajes entre productores y consumidores.
• Se facilita mucho el manejo de mensajes usando un middleware.

Detalles de uso/aplicación:
1. Debe correrse inicialmente con las credenciales de AWS el archivo de middleware.py para posteriormente permitir la conexión del productor y consumidor.
2. Debe ejecutarse el archivo de productor.py para acceder al productor donde se crean colas según el menú indicado en la ejecución.
3. Debe ejecutarse el archivo de consumidor.py para acceder al consumidor donde se listan y se conectan a las colas según el menú indicado en la ejecución.
