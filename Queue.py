from collections import deque


class Queue:

	def __init__(self, nombre, idCola):
		self.id = idCola
		self.nombre = nombre
		self.estado = False
		self.clientes = []
		self.estadoClientes = []
		self.cola = deque()

	def getClientes(self):
		return self.clientes

	def setConsumidores(self, arreglo):
		self.clientes = arreglo

	def actualizarTodosConsumidores(self):
		for i in range(0,len(self.estadoClientes)):
			self.estadoClientes[i] = False

	def agregarCliente(self, cliente):
		self.clientes.append(cliente)
		self.estadoClientes.append(False)

	def cambiarEstadoCliente(self,i):
		self.estadoClientes[i] = True

	def getEstadosClientes(self):
		return self.estadoClientes

	def setEstados(self, arreglo):
		self.estadoClientes = arreglo


	def cambiarIndiceEnvio(self):
		mensaje = self.cola.popleft()
		return mensaje


	def getId(self):
		return self.id

	def getNombre(self):
		return self.nombre

	def getCola(self):
		return self.cola

	def enviarMensaje(self, mensaje):
		if (len(self.cola) < 2):
			self.cola.append(mensaje)
			return 1
		else:
			return 0

	def conectar(self):
		self.estado = True

	def desconectar(self):
		self.estado = False

	def getTamañoCola(self):
		return len(self.cola)

	def vaciarCola(self):
		self.cola = deque()
	
	def getEstado(self):
    		return self.estado
	