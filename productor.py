import socket


socketProductor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def main():
    print('*' * 50)
    print("Conectando productor al MOM\n")
    socketProductor.connect(("52.7.209.208", 8080))
    tuplaConexion = socketProductor.getsockname()
    print("Tu dirección de conexión es: ", tuplaConexion)
    opcion = menuInicial()
    idCola=0
   
    while opcion != "salir":
        print(f'opcionnnnn {opcion}')
        if opcion == '':
            print("Opcion invalida, intenta de nuevo\n")
            opcion = menuInicial()
        elif (opcion == "crearSesion"):
            crearSesion(opcion)
            opcion=menuInicial()
        elif (opcion == "iniciarSesion"):
            iniciarSesion(opcion)
            opcion=menu()
        elif (opcion == "crearCola"):
            crearCola(opcion,idCola)
            opcion = menu()
        elif (opcion == "listarCola"):
            listarCola(opcion)
            opcion = menu()
        elif (opcion == "borrarCola"):
            borrarCola(opcion)
            opcion = menu()
        elif (opcion == "conectarCola"):
            conectarCola(opcion)
            opcion = menu()
        elif (opcion == "desconectarCola"):
            desconectarCola(opcion)
            opcion = menu()
        elif (opcion == "mensajeCola"):
            mensajeCola(opcion)
            opcion = menu()
        else:
            print("Opcion invalida, intenta de nuevo\n")
            opcion = menu()

    socketProductor.send(bytes(opcion, "utf-8"))
    datosRecibidos = socketProductor.recv(1024)
    print(datosRecibidos.decode("utf-8"))
    socketProductor.close()

def menuInicial():
    print("crearSesion: Crear la sesión")
    print("iniciarSesion: Inicio de sesión")
    print("salir: Desconectar aplicación")
    opcion = input("Ingrese la opcion que quiere realizar ")
    return opcion

def menu():
    print("crearCola: Crear una nueva cola")
    print("listarCola: Listado de Colas en el MOM")
    print("borrarCola: Eliminar una Cola del MOM")
    print("conectarCola: Conexión a una Cola del MOM")
    print("desconectarCola: Desconexión una Cola del MOM")
    print("mensajeCola: Envio de un mensaje")
    print("salir: Desconectar aplicación")
    opcion = input("Ingrese la opcion que quiere realizar ")
    print (opcion)
    return opcion

def crearSesion(opcion):
     usuario = input("Usuario: ")
     contrasena = input("Contraseña: ")
     envioMOM = opcion + ' ' + usuario + ' ' + contrasena
     socketProductor.send(bytes(envioMOM, "utf-8"))
     datosRecibidos = socketProductor.recv(1024)
     print(datosRecibidos.decode("utf-8"))
     opcion = menuInicial()

def iniciarSesion(opcion):
    usuario = input("Usuario: ")
    contrasena = input("Contraseña: ")
    envioMOM = opcion + ' ' + usuario + ' ' + contrasena
    socketProductor.send(bytes(envioMOM, "utf-8"))
    datosRecibidos = socketProductor.recv(1024)
    print(datosRecibidos.decode("utf-8"))
    validar = socketProductor.recv(1024)
    validar = str(validar)
    
    

def crearCola(opcion,idCola):
    nombreAplicacion = input("Nombre de la cola:  ")
    envioMOM = opcion + ' ' + nombreAplicacion+ ' ' +str(idCola)
    socketProductor.send(bytes(envioMOM, "utf-8"))
    datosRecibidos = socketProductor.recv(1024)
    print(datosRecibidos.decode("utf-8"))
    print("El ID es: "+str(idCola))
    idCola=idCola+1
    
    

def listarCola(opcion):
    envioMOM = opcion
    socketProductor.send(bytes(envioMOM, "utf-8"))
    datosRecibidos = socketProductor.recv(1024)
    print(datosRecibidos.decode("utf-8"))
    datosRecibidos = socketProductor.recv(1024)
    print(datosRecibidos.decode("utf-8"))
    

def borrarCola(opcion):
    nombreAplicacion = input("Nombre de la cola: ")
    idCola = input("Ingrese el id de la cola: ")
    envioMOM = opcion + ' ' + nombreAplicacion + ' ' +str(idCola)
    socketProductor.send(bytes(envioMOM, "utf-8"))
    datosRecibidos = socketProductor.recv(1024)
    print(datosRecibidos.decode("utf-8"))
    

def conectarCola(opcion):
    nombreAplicacion = input("Nombre de la cola: ")
    idCola = input("Ingresa el token de la cola: ")
    envioMOM = opcion + ' ' + nombreAplicacion + ' ' + str(idCola)
    socketProductor.send(bytes(envioMOM, "utf-8"))
    datosRecibidos = socketProductor.recv(1024)
    print(datosRecibidos.decode("utf-8"))
    

def desconectarCola(opcion):
    nombreAplicacion = input("Nombre de la cola: ")
    idCola = input("Ingresa el token de la cola ")
    envioMOM = opcion + ' ' + nombreAplicacion + ' ' + str(idCola)
    socketProductor.send(bytes(envioMOM, "utf-8"))
    datosRecibidos = socketProductor.recv(1024)
    print(datosRecibidos.decode("utf-8"))
    

def mensajeCola(opcion):
    nombreAplicacion = input("Ingresa el nombre de la cola correspondiente ")
    idCola = input("Ingresa el token de identificacion de la cola ")
    mensaje = input("Mensaje a enviar ")
    envioMOM = opcion + ' ' + nombreAplicacion + ' ' + idCola + ' ' + mensaje
    socketProductor.send(bytes(envioMOM, "utf-8"))
    datosRecibidos = socketProductor.recv(1024)
    print(datosRecibidos.decode("utf-8"))
    opcion = menu()
    

if __name__ == '__main__':
    main()