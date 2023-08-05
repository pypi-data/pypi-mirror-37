import os
import threading
from inspect import signature

from simplestRPC.varenv import varenv
from simplestRPC.connector import Listener
from simplestRPC.auxiliar import aux


class SRPCServer:
	__con = None
	__listener = None
	__client_pool = {}
	__client_pool_lock = None
	__rpcs = {}
	__client_servers = {}
	__client_servers_lock = None
	debug = None

	def __init__(self, debug=False):
		self.debug = debug
		self.__con = Listener(os.getenv("SRPC_SERVER"), os.getenv("SRPC_SERVER_PORT"))
		if(self.debug):
			print('debug option is ' + str(self.debug))
			print('env var', os.getenv("SRPC_SERVER"), os.getenv("SRPC_SERVER_PORT"))
			print(self.__con)
		self.__con.listen()
		self.__client_pool_lock = threading.Lock()
		self.__client_servers_lock = threading.Lock()
		self.__listener = threading.Thread(target=self.__serve)

	def __del_(self):
		with self.__client_pool_lock:
			for client in self.__client_pool:
				self.disconnect_client(client, nolock=True)
		del self.__con
		self.__listener._stop()
		del self.__listener
		for server in self.__client_servers:
			self.__client_servers[server]._stop()
			del self.__client_servers

	def __delattr__(self, name):
		if(name == '__con'):
			self.__con.disconnect()

	def __str__(self):
		return 'client_pool: ' + str(self.__client_pool) + '\nconnection: ' + str(self.__con)

	def __serve(self):
		while True:
			if(self.debug):
				print("accpeting at ", self.__con)

			newClient = self.__con.accept()
			newClientKey = str(newClient)
			with self.__client_pool_lock:
				self.__client_pool[newClientKey] = newClient

			if(self.debug):
				print("new client detected at " + newClientKey)

			self.update_client_rpcs(newClientKey)
			self.__serve_clients(newClientKey)

	def __client_server(self, clientKey):
		client = None

		while True:
			with self.__client_servers_lock:
				if(clientKey in self.__client_pool):
					client = self.__client_pool[clientKey]
				else:
					if(self.debug):
						print('client ' + clientKey + ' was deleted. Ending thread')

					break

			try:
				msg = client.recv()[0]
			except Exception as err:
				self.disconnect_client(clientKey)
				break
			else:
				func, args = aux.func_args_separator(msg)
				response = self.__rpcs[func][0](*args)
				client.send(response)


	def disconnect_client(self, ipport, nolock=False):
		if(nolock):
			if(ipport in self.__client_pool):
				self.__client_pool[ipport].disconnect()
				del self.__client_pool[ipport]
		else:
			with self.__client_pool_lock:
				if(ipport in self.__client_pool):
					self.__client_pool[ipport].disconnect()
					del self.__client_pool[ipport]

	def serve(self):
		self.__listener.daemon = False
		self.__listener.start()

	def __serve_clients(self, clientKey):
		success = False

		if(clientKey in self.__client_pool):
			with self.__client_servers_lock:
				client = self.__client_pool[clientKey]
				aux = threading.Thread(target=self.__client_server, args=[clientKey])
				aux.daemon = False
				self.__client_servers[clientKey] = aux
				self.__client_servers[clientKey].start()

			success = True

		return success


	def add_rpc(self, func, name=None):
		if((name is None or type(name) == str) and callable(func)):
			if(name is None):
				self.__rpcs[func.__name__] = (func, len(list(signature(func).parameters)))
			else:
				self.__rpcs[name] = (func, len(list(signature(func).parameters)))

		if(self. debug):
			print('rpc added, current: ', self.__rpcs)

	def update_client_rpcs(self, clientKey):
		success = False

		if(clientKey in self.__client_pool):
			with self.__client_pool_lock:
				client = self.__client_pool[clientKey]
				sent = client.send([(rc, self.__rpcs[rc][1]) for rc in self.__rpcs])
				success = True

			if(self.debug):
				print("rpcs' sent, " + str(sent) + ' bytes')

		return success



# FOR DEV TESTING PROPOSE ONLY
if __name__ == '__main__':
	def newPrint(msg):
		print(msg)
		return msg
	# server = SRPCServer(debug=True)
	server = SRPCServer(debug=False)
	server.add_rpc(newPrint)
	server.serve()
