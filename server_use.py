import threading
from server import Server

#Download       -   Instruction1
#Upload         -   Instruction2
#Remove         -   Instruction3
#Rename         -	Instruction4
#Move           -	Instruction5
#Back           -
#Forward		-
#Access_Folder  -
#file list      -   Instruction6
#Search			-	Instruction7

def start_responding(Client_socket ,Client_Adress):

	while True:
		current_directory = "./Local_server_files"
		print(f"Current Directory: {current_directory}")

		Instruction = Client_socket.recv(server.Instruction_Length).decode('utf-8').strip()
		# print(Instruction)
		if Instruction == "Instruction1":
			
			server.Send_requested_file(Client_socket)

		elif Instruction == "Instruction2":

			server.Receive_file(Client_socket)

		elif Instruction == "Instruction3":
			
			server.Remove_file(Client_socket)

		elif Instruction == "Instruction4":

			server.Rename_file(Client_socket)

		# elif Instruction == "Instruction5":	
		elif Instruction == "Instruction6":
			
			server.Send_file_list(Client_socket)

		elif Instruction == "Instruction7":
		
			server.Return_search(Client_socket)

server = Server()
server.Start_server()

Connections = 3
while True:
	try:
		print("we are in the while loop")
		print("trying to connect to clients")
		Client_socket, Client_Adress = server.Server_Socket.accept()
		print(f"Connection has been established with {Client_Adress}")
		threading._start_new_thread(start_responding, (Client_socket, Client_Adress))

	except KeyboardInterrupt as e:
		print(f"Gradually shutting down the server")
	except Exception as e:
		print(f"did not expected {e}!")
