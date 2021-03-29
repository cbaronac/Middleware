import _thread
import socket
import Queue
import threading
import sys
from collections import deque
import os
import os.path as path


class Mom:

    def __init__(self):
        self.MOMserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.colas = {}
        self.canales = {}
        self.contadorColas = 0

    def threaded(self, conexionAplicacion, direccionAplicacion):
        while True:
            datosRecibidos = conexionAplicacion.recv(1024)
            datosRecibidos = str(datosRecibidos.decode("utf-8"))
            arreglo = datosRecibidos.split()
            opcion = arreglo[0]

            if (opcion == "salir"):
                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                respuesta = f'Respuesta para: {direccionAplicacion[0]} Vuelva pronto\n'
                conexionAplicacion.sendall(respuesta.encode("utf-8"))
                print(f'La aplicación {direccionAplicacion[0]}:{direccionAplicacion[1]} se desconectó correctamente')
                break

            elif (opcion == "crearCola"):
                print("prueba")
                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                aplicacion = Queue.Queue(arreglo[1], arreglo[2])
                self.colas[self.contadorColas] = aplicacion
                respuesta = f'Respuesta para: {direccionAplicacion[0]} La cola fue creada correctamente\n con el nombre {arreglo[1]} No olvide el token de identificacion de la cola: {arreglo[2]}\n'
                conexionAplicacion.sendall(respuesta.encode("utf-8"))
                print(f'Se envio respuesta a: {direccionAplicacion[0]} por la solicitud: {opcion}')


            elif (opcion == "listarCola"):
                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                respuesta = f'Respuesta para: {direccionAplicacion[0]} Listado de colas\n'
                conexionAplicacion.sendall(respuesta.encode("utf-8"))
                respuesta = ''
                if (len(self.colas) == 0):
                    respuesta = 'No hay colas en el MOM\n'
                else:
                    for cola in self.colas:
                        idCola = cola
                        respuesta = respuesta + f'Cola, Token de identificación: {self.colas[idCola].getId()}: {self.colas[idCola].getNombre()} \n'

                conexionAplicacion.sendall(respuesta.encode("utf-8"))
                print(f'Se envio respuesta a: {direccionAplicacion[0]} por la solicitud: {opcion}')

        
            elif (opcion == "borrarCola"):
                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                idCola = arreglo[2]
                nombreCola = arreglo[1]
               
                try:
                    nombreAux = self.colas[int(idCola)].getNombre()

                    idAux = self.colas[int(idCola)].getId()
                    if (str(idCola) == str(idAux) and str(nombreCola) == str(nombreAux)):
                        respuesta = f'Respuesta para: {direccionAplicacion[0]} La cola fue eliminada correctamente\n'
                        self.colas.pop(int(idCola))
                except:
                    respuesta = f'Respuesta para: {direccionAplicacion[0]} Los datos son incorrectos, prueba nuevamente\n'
                print(f'Se envio respuesta a: {direccionAplicacion[0]} por la solicitud: {opcion}')
                conexionAplicacion.sendall(respuesta.encode("utf-8"))

           
            elif (opcion == "conectarCola"):
                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                idCola = arreglo[2]
                nombreCola = arreglo[1]
                
                try:
                    nombreAux = self.colas[int(idCola)].getNombre()
                    idAux = self.colas[int(idCola)].getId()
                   
                    if (str(idCola) == str(idAux) and str(nombreCola) == str(nombreAux) ):
                        respuesta = f'Respuesta para: {direccionAplicacion[0]} La conexión se establecio correctamente, ahora puedes enviar mensajes\n'
                        self.colas[int(idCola)].conectar()
                    else:
                        respuesta = f'Respuesta para: {direccionAplicacion[0]} La conexión no se pudo establecer, intenta nuevamente\n'
                except:
                    respuesta = f'Respuesta para: {direccionAplicacion[0]} Los datos son incorrectos, prueba nuevamente\n'
                print(f'Se envio respuesta a: {direccionAplicacion[0]} por la solicitud: {opcion}')
                conexionAplicacion.sendall(respuesta.encode("utf-8"))

            elif (opcion == "pullCola"):
                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                nombreCola = arreglo[1]
                idCola = arreglo[2]
                respuesta = ""
                try:
                    nombreAux = self.colas[int(idCola)].getNombre()
                    idAux = self.colas[int(idCola)].getId()
                    if (str(idCola) == str(idAux) and str(nombreCola) == str(nombreAux)):
                        if (self.colas[int(idCola)].getTamañoCola() == 0):
                            respuesta = f'Respuesta para: {direccionAplicacion[0]} No hay mensajes\n'
                            conexionAplicacion.sendall(respuesta.encode("utf-8"))
                        else:
                            mensajeEnviar = self.colas[int(idCola)].cambiarIndiceEnvio()
                            respuesta = f"Repsuesta para: {direccionAplicacion} Tiene un nuevo mensaje: {mensajeEnviar}\n"
                            conexionAplicacion.sendall(respuesta.encode("utf-8"))
                    else:
                        respuesta = f'Respuesta para: {direccionAplicacion[0]} Error al hacer Pull de la cola, los datos de acceso son erroneos\n'
                        conexionAplicacion.sendall(respuesta.encode("utf-8"))
                except:
                    respuesta = f'Respuesta para: {direccionAplicacion[0]} Error al hacer Pull de la cola, los datos de acceso son erroneos\n'
                    conexionAplicacion.sendall(respuesta.encode("utf-8"))

            elif (opcion == "desconectarCola"):
                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                idCola = arreglo[2]
                nombreCola = arreglo[1]
                try:
                    nombreAux = self.colas[int(idCola)].getNombre()
                    idAux = self.colas[int(idCola)].getId()
                    if (str(idCola) == str(idAux) and str(nombreCola) == str(nombreAux)):
                        respuesta = f'Respuesta para: {direccionAplicacion[0]} la conexión con el MOM para el envio de mensajes se cerró correctamente\n'
                        self.colas[int(idCola)].desconectar()
                    else:
                        respuesta = f'Respuesta para: {direccionAplicacion[0]} se desconecto correctamente\n'
                except:
                    respuesta = f'Respuesta para: {direccionAplicacion[0]} Ocurrio un error, prueba nuevamente\n'
                print(f'Se envio respuesta a: {direccionAplicacion[0]} por la solicitud: {opcion}')
                conexionAplicacion.sendall(respuesta.encode("utf-8"))

            elif (opcion == "mensajeCola"):
                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                nombreCola = arreglo[1]
                idCola = arreglo[2]
                mensaje = ""
                for i in range(3, len(arreglo)):
                    mensaje = mensaje + arreglo[i] + " "
                try:
                    nombreAux = self.colas[int(idCola)].getNombre()
                    idAux = self.colas[int(idCola)].getId()
                    estado = self.colas[int(idCola)].getEstado()
                    if (str(idCola) == str(idAux) and str(nombreCola) == str(nombreAux) and estado == True):
                        if (self.colas[int(idCola)].enviarMensaje(mensaje) == 1):
                            respuesta = f'Respuesta para: {direccionAplicacion[0]} El mensaje fue enviado correctamente\n'
                        else:
                            respuesta = f'Respuesta para: {direccionAplicacion[0]} Error al enviar el mensaje. La cola está llena\n'
                    else:
                        respuesta = f'Respuesta para: {direccionAplicacion[0]} Error al enviar el mensaje, los datos de la cola no coinciden\n'
                except:
                    respuesta = f'Respuesta para: {direccionAplicacion[0]} Error al enviar el mensaje, posiblemente no estés conectado a la cola\n'

                print(f'Se envio respuesta a: {direccionAplicacion[0]} por la solicitud: {opcion}')
                conexionAplicacion.sendall(respuesta.encode("utf-8"))

            elif (opcion == "crearSesion"):
                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                usuario = arreglo[1]
                contrasena = arreglo[2]
                if (path.exists("usuarios.txt")):
                    file = open("usuarios.txt", "r")
                    lineas = file.readlines()
                    if (usuario + "\n" in lineas):
                        respuesta = f'Respuesta para: {direccionAplicacion[0]} El usuario ya existe\n'
                        conexionAplicacion.sendall(respuesta.encode("utf-8"))
                    else:
                        file = open("usuarios.txt", "a")
                        file.write(usuario + "\n" + contrasena + "\n")
                        file.close()
                        respuesta = f'Respuesta para: {direccionAplicacion[0]} Sesión Creada\n'
                        conexionAplicacion.sendall(respuesta.encode("utf-8"))
                else:
                    file = open("usuarios.txt", "w")
                    file.write(usuario + "\n" + contrasena + "\n")
                    file.close()
                    respuesta = f'Respuesta para: {direccionAplicacion[0]} Sesión Creada\n'
                    conexionAplicacion.sendall(respuesta.encode("utf-8"))

            elif (opcion == "iniciarSesion"):
                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                usuario = arreglo[1]
                contrasena = arreglo[2]
                file = open("usuarios.txt", "r")
                lineas = file.readlines()
                if (usuario + "\n" in lineas):
                    posicion = lineas.index(usuario + "\n")
                    if (contrasena + "\n" == lineas[posicion + 1]):
                        respuesta = f'Respuesta para: {direccionAplicacion[0]} Sesión Iniciada\n'
                        conexionAplicacion.sendall(respuesta.encode("utf-8"))
                        respuesta = f'Ok'
                        conexionAplicacion.sendall(respuesta.encode("utf-8"))
                    else:
                        respuesta = f'Respuesta para: {direccionAplicacion[0]} Error al iniciar la sesión 1\n'
                        conexionAplicacion.sendall(respuesta.encode("utf-8"))
                        respuesta = f'No'
                        conexionAplicacion.sendall(respuesta.encode("utf-8"))
                else:
                    respuesta = f'Respuesta para: {direccionAplicacion[0]} Error al iniciar la sesión 2\n'
                    conexionAplicacion.sendall(respuesta.encode("utf-8"))
                    respuesta = f'No'
                    conexionAplicacion.sendall(respuesta.encode("utf-8"))

        try:
            print_lock.release()
        except BaseException:
            pass
        conexionAplicacion.close()

    def main(self):
        print('*' * 50)
        print('El MOM está encendido\n')
        print('El puerto por el cual está corriendo el servidor MOM es: ', 8080)
        tuplaConexion = ("0.0.0.0", 8080)
        self.MOMserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.MOMserver.bind(tuplaConexion)
        self.MOMserver.listen(5)
        while True:
            conexionAplicacion, direccionAplicacion = self.MOMserver.accept()

            print(f'Nueva aplicación conectada desde la dirección IP: {direccionAplicacion[0]}')
            _thread.start_new_thread(self.threaded, (conexionAplicacion, direccionAplicacion))
        self.MOMserver.close()


def mom():
    mom = Mom()
    mom.main()


if __name__ == '__main__':
    mom()