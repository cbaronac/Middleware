import _thread 
import socket
from collections import deque
import os.path as path
import Queue

class Mom:

    def __init__(self):
        self.MOMserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.contadorColas = 0
        self.colas = {}
            
    def threaded(self, conexionApp, direccionApp):
        while True:
            datosRecibidos = conexionApp.recv(1024)
            datosRecibidos = str(datosRecibidos.decode("utf-8"))
            arreglo = datosRecibidos.split()
            opcion = arreglo[0]

            if (opcion == "salir"):
                salir(conexionApp,direccionApp,opcion)
                break

            elif (opcion == "crearCola"):
                crearCola(conexionApp,direccionApp,opcion,arreglo,self)

            elif (opcion == "listarCola"):
                listarCola(conexionApp,direccionApp,opcion,self)

            elif (opcion == "borrarCola"):
                borrarCola(conexionApp,direccionApp,arreglo,self,opcion)

            elif (opcion == "conectarCola"):
                conectarCola(conexionApp,direccionApp,opcion,self,arreglo)

            elif (opcion == "pullCola"):
                pullCola(conexionApp,self,direccionApp,arreglo)

            elif (opcion == "desconectarCola"):
                desconectarCola(conexionApp,direccionApp,self,arreglo,opcion)
                
            elif (opcion == "mensajeCola"):
                mensajeCola(conexionApp,direccionApp,arreglo,self,opcion)

            elif (opcion == "crearSesion"):
                crearSesion(conexionApp,direccionApp,opcion,arreglo)

            elif (opcion == "iniciarSesion"):
                iniciarSesion(direccionApp,conexionApp,arreglo,opcion)
                
    

    def main(self):
            print('*' * 50)
            print('El MOM está encendido\n')
            tuplaConexion = ("0.0.0.0", 8080)
            self.MOMserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.MOMserver.bind(tuplaConexion)
            self.MOMserver.listen(5)
            while True:
                conexionApp, direccionApp = self.MOMserver.accept()

                print(f'Nueva app conectada desde la dirección IP: {direccionApp[0]}')
                _thread.start_new_thread(self.threaded, (conexionApp, direccionApp))
            self.MOMserver.close()

def salir(conexionApp,direccionApp,opcion):
    print(f'{direccionApp[0]} solicita: {opcion}')
    respuesta = f'Respuesta para: {direccionApp[0]} Vuelva pronto\n'
    conexionApp.sendall(respuesta.encode("utf-8"))
    print(f'La aplicación {direccionApp[0]}:{direccionApp[1]} se desconectó correctamente')

def crearCola(conexionApp,direccionApp,opcion,arreglo,self):
    print("prueba")
    print(f'{direccionApp[0]} solicita: {opcion}')
    aplicacion = Queue.Queue(arreglo[1], arreglo[2])
    self.colas[self.contadorColas] = aplicacion
    respuesta = f'Respuesta para: {direccionApp[0]} La cola fue creada correctamente\n con el nombre {arreglo[1]}'
    
    conexionApp.sendall(respuesta.encode("utf-8"))
    print(f'Se envio respuesta a: {direccionApp[0]} por la solicitud: {opcion}')

def listarCola(conexionApp,direccionApp,opcion,self):
        print(f'{direccionApp[0]} solicita: {opcion}')
        respuesta = f'Respuesta para: {direccionApp[0]} Listado de colas\n'
        conexionApp.sendall(respuesta.encode("utf-8"))
        respuesta = ''
        if (len(self.colas) == 0):
            respuesta = 'No hay colas en el MOM\n'
        else:
            for cola in self.colas:
                idCola = cola
                respuesta = respuesta + f'Cola, Token de identificación: {self.colas[idCola].getId()}: {self.colas[idCola].getNombre()} \n'

        conexionApp.sendall(respuesta.encode("utf-8"))
        print(f'Se envio respuesta a: {direccionApp[0]} por la solicitud: {opcion}')

def borrarCola(conexionApp,direccionApp,arreglo,self,opcion):
        print(f'{direccionApp[0]} solicita: {opcion}')
        idCola = arreglo[2]
        nombreCola = arreglo[1]
        respuesta = f'Respuesta para: {direccionApp[0]} La cola fue eliminada correctamente\n'
        self.colas.pop(int(idCola))

        
        print(f'Se envio respuesta a: {direccionApp[0]} por la solicitud: {opcion}')
        conexionApp.sendall(respuesta.encode("utf-8"))

def conectarCola(conexionApp,direccionApp,opcion,self,arreglo):
        print(f'{direccionApp[0]} solicita: {opcion}')
        idCola = arreglo[2]
        nombreCola = arreglo[1]
        
        try:
            nombreAux = self.colas[int(idCola)].getNombre()
            idAux = self.colas[int(idCola)].getId()
            if (str(idCola) == str(idAux) and str(nombreCola) == str(nombreAux)):
                respuesta = f'Respuesta para: {direccionApp[0]} La conexión se establecio correctamente, ahora puedes enviar mensajes\n'
                self.colas[int(idCola)].conectar()
        except:
            respuesta = f'Respuesta para: {direccionApp[0]} Los datos son incorrectos, prueba nuevamente\n'
            print(f'Se envio respuesta a: {direccionApp[0]} por la solicitud: {opcion}')
            conexionApp.sendall(respuesta.encode("utf-8"))
    
def pullCola(conexionApp,self,direccionApp,arreglo,opcion):
        print(f'{direccionApp[0]} solicita: {opcion}')
        nombreCola = arreglo[1]
        idCola = arreglo[2]
        respuesta = ""
        try:
            nombreAux = self.colas[int(idCola)].getNombre()
            idAux = self.colas[int(idCola)].getId()
            if (str(idCola) == str(idAux) and str(nombreCola) == str(nombreAux)):
                if (self.colas[int(idCola)].getTamañoCola() == 0):
                    respuesta = f'Respuesta para: {direccionApp[0]} No hay mensajes\n'
                    conexionApp.sendall(respuesta.encode("utf-8"))
                else:
                    mensajeEnviar = self.colas[int(idCola)].cambiarIndiceEnvio()
                    respuesta = f"Repsuesta para: {direccionApp} Tiene un nuevo mensaje: {mensajeEnviar}\n"
                    conexionApp.sendall(respuesta.encode("utf-8"))
            else:
                    respuesta = f'Respuesta para: {direccionApp[0]} Error al hacer Pull de la cola, los datos de acceso son erroneos\n'
                    conexionApp.sendall(respuesta.encode("utf-8"))
        except:
            respuesta = f'Respuesta para: {direccionApp[0]} Error al hacer Pull de la cola, los datos de acceso son erroneos\n'
            conexionApp.sendall(respuesta.encode("utf-8"))

def desconectarCola(conexionApp,direccionApp,self,arreglo,opcion):
        print(f'{direccionApp[0]} solicita: {opcion}')
        idCola = arreglo[2]
        nombreCola = arreglo[1]
        try:
            nombreAux = self.colas[int(idCola)].getNombre()
            idAux = self.colas[int(idCola)].getId()
            if (str(idCola) == str(idAux) and str(nombreCola) == str(nombreAux)):
                respuesta = f'Respuesta para: {direccionApp[0]} la conexión con el MOM para el envio de mensajes se cerró correctamente\n'
                self.colas[int(idCola)].desconectar()
        except:
            respuesta = f'Respuesta para: {direccionApp[0]} Ocurrio un error, prueba nuevamente\n'
        print(f'Se envio respuesta a: {direccionApp[0]} por la solicitud: {opcion}')
        conexionApp.sendall(respuesta.encode("utf-8"))

def mensajeCola(conexionApp,direccionApp,arreglo,self,opcion):
        print(f'{direccionApp[0]} solicita: {opcion}')
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
                        respuesta = f'Respuesta para: {direccionApp[0]} El mensaje fue enviado correctamente\n'
                    else:
                        respuesta = f'Respuesta para: {direccionApp[0]} Error al enviar el mensaje. La cola está llena\n'
                else:
                    respuesta = f'Respuesta para: {direccionApp[0]} Error al enviar el mensaje, los datos de la cola no coinciden\n'
            except:
                respuesta = f'Respuesta para: {direccionApp[0]} Error al enviar el mensaje, posiblemente no estés conectado a la cola\n'

        print(f'Se envio respuesta a: {direccionApp[0]} por la solicitud: {opcion}')
        conexionApp.sendall(respuesta.encode("utf-8"))

def crearSesion(conexionApp,direccionApp,opcion,arreglo):
        print(f'{direccionApp[0]} solicita: {opcion}')
        usuario = arreglo[1]
        contrasena = arreglo[2]
        if (path.exists("usuarios.txt")):
            file = open("usuarios.txt", "r")
            lineas = file.readlines()
            if (usuario + "\n" in lineas):
                respuesta = f'Respuesta para: {direccionApp[0]} El usuario ya existe\n'
                conexionApp.sendall(respuesta.encode("utf-8"))
            else:
                file = open("usuarios.txt", "a")
                file.write(usuario + "\n" + contrasena + "\n")
                file.close()
                respuesta = f'Respuesta para: {direccionApp[0]} Sesión Creada\n'
                conexionApp.sendall(respuesta.encode("utf-8"))
        else:
            file = open("usuarios.txt", "w")
            file.write(usuario + "\n" + contrasena + "\n")
            file.close()
            respuesta = f'Respuesta para: {direccionApp[0]} Sesión Creada\n'
            conexionApp.sendall(respuesta.encode("utf-8"))

def iniciarSesion(direccionApp,conexionApp,arreglo,opcion):
    print(f'{direccionApp[0]} solicita: {opcion}')
    usuario = arreglo[1]
    contrasena = arreglo[2]
    file = open("usuarios.txt", "r")
    lineas = file.readlines()
    if (usuario + "\n" in lineas):
        posicion = lineas.index(usuario + "\n")
        if (contrasena + "\n" == lineas[posicion + 1]):
            respuesta = f'Respuesta para: {direccionApp[0]} Sesión Iniciada\n'
            conexionApp.sendall(respuesta.encode("utf-8"))
            respuesta = f'Ok'
            conexionApp.sendall(respuesta.encode("utf-8"))
        else:
            respuesta = f'Respuesta para: {direccionApp[0]} Error al iniciar la sesión 1\n'
            conexionApp.sendall(respuesta.encode("utf-8"))
            respuesta = f'No'
            conexionApp.sendall(respuesta.encode("utf-8"))
    else:
        respuesta = f'Respuesta para: {direccionApp[0]} Error al iniciar la sesión 2\n'
        conexionApp.sendall(respuesta.encode("utf-8"))
        respuesta = f'No'
        conexionApp.sendall(respuesta.encode("utf-8"))

    

def mom():
    mom = Mom()
    mom.main()


if __name__ == '__main__':
    mom()