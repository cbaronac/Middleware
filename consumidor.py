import socket

socketConsumidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def main():
    print('*' * 50)
    print("Conectando consumidor al MOM\n")
    socketConsumidor.connect(("52.7.209.208", 8080))
    tuplaConexion = socketConsumidor.getsockname()
    print("Tu dirección de conexión es: ", tuplaConexion)
    opcion = menu()

    while opcion != "salir":
        if opcion == '':
            print("Opcion invalida, intenta de nuevo\n")
            opcion = menu()
        elif (opcion == "listarCola"):
            listarCola(opcion)
            opcion=menu()
        elif (opcion == "pullCola"):
            pullCola(opcion)
            opcion=menu()
        else:
            print("Opcion invalida, intenta de nuevo\n")
            opcion = menu()

    socketConsumidor.send(bytes(opcion, "utf-8"))
    datosRecibidos = socketConsumidor.recv(1024)
    print(datosRecibidos.decode("utf-8"))
    socketConsumidor.close()


def menu():

    print("listarCola: Listado de Colas en el MOM")
    print("pullCola: Conexión a una Cola del MOM")
    print("salir: Desconectar aplicación")
    opcion = input("Ingrece la opcion que quiere realizar ")
    return opcion

def listarCola(opcion):
    envioMOM = opcion
    socketConsumidor.send(bytes(envioMOM, "utf-8"))
    datosRecibidos = socketConsumidor.recv(1024)
    print(datosRecibidos.decode("utf-8"))
    datosRecibidos = socketConsumidor.recv(1024)
    print(datosRecibidos.decode("utf-8"))
    

def pullCola(opcion):
    nombreAplicacion = input("Nombre de la cola a conectarse: ")
    idCola = input("Token de identificación: ")
    envioMOM = opcion + ' ' + nombreAplicacion + ' ' + str(idCola)
    socketConsumidor.send(bytes(envioMOM, "utf-8"))
    datosRecibidos = socketConsumidor.recv(1024)
    print(datosRecibidos.decode("utf-8"))
    


if __name__ == '__main__':
    main()