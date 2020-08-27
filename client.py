import socket
import pickle
import time
import os
import select
# import tqdm


#Download       								-   Instruction1
#Upload         								-   Instruction2
#Remove         								-   Instruction3
#Rename         								-	Instruction4
#Move           								-	Instruction5
#Back           								-	
#Forward										-
#Access_Folder  								-	
#file list      								-   Instruction6
#Search_pericular_string_in_given_directory		-	Instruction7

class Client:

	def __init__(self):
		# self.HOST_ADDRESS = socket.gethostbyname(socket.gethostname())
		self.HOST_ADDRESS = "192.168.0.111"
		self.PORT = 4444
		self.HEADER_LENGTH = 50
		self.current_directory = "./Local_server_files"
		self.previous_directory = ["./Local_server_files"]
		self.file_list = []
		self.BUFFER = 4
		self.MAX_SIZE = self.BUFFER*1024*1024

	def Connect_to_server(self):
		self.Client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.Client_socket.connect((self.HOST_ADDRESS, self.PORT))

	def Download_file(self):
		for i in range (len(self.file_list)):
			print((i+1), self.file_list[i])

		file_name = self.file_list[int(input("Enter The Number Corresponding to the file name: "))-1]
		print(f"redirecting {file_name} to function Download_file")
		#Send an indicator to prepare server to send file
		self.Client_socket.sendall(bytes("Instruction1", 'utf-8'))
		self.Client_socket.sendall(bytes(f"{len(file_name):<{self.HEADER_LENGTH}}", 'utf-8'))
		self.Client_socket.sendall(bytes(file_name, 'utf-8'))
		print(f"{file_name} request sent to server")
		filetype = 0
		#if file is a file
		if filetype == 0:
			file_size = int(self.Client_socket.recv(self.HEADER_LENGTH).decode('utf-8').strip())
			print(f"receivable_file_length: {file_size//(1024*1024)} MB")
			
			f = open("download_"+file_name, "wb")
			
			# progress = tqdm.tqdm(range(file_size), f"Receiving {file_name}", unit="B", unit_scale=True, unit_divisor=self.MAX_SIZE/4)
			# for _ in progress:
			# 	# time.sleep(0.1)
			# 	received_data = self.Client_socket.recv(self.MAX_SIZE)
			# 	if not received_data:
			# 		break
			# 	f.write(received_data)
			# 	progress.update(len(received_data))
			
			# total_data_received = 0
			# for segments in range (file_size//self.MAX_SIZE):
			# 	received_data = self.Client_socket.recv(self.MAX_SIZE)
			# 	# print(f"Length of data received: {len(received_data)//(1024*1024)} MB")
			# 	f.write(received_data)
			# 	total_data_received += self.MAX_SIZE
			# 	print(f"Data Received: {total_data_received//(1024*1024)} MB/{file_size//(1024*1024)} MB", end = "\r")

			# if file_size % self.MAX_SIZE != 0:
			# 	received_data = self.Client_socket.recv(file_size%self.MAX_SIZE)
			# 	# print(f"Length of data received: {len(received_data)//(1024*1024)} MB")
			# 	f.write(received_data)
			# 	total_data_received += len(received_data)
			# 	print(f"Data Received: {total_data_received//(1024*1024)} MB/{file_size//(1024*1024)} MB", end = "\r")

			total_data_received = 0
			for segments in range (file_size//self.MAX_SIZE):

				Client_socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				Client_socket_.connect((self.HOST_ADDRESS, self.PORT+1+segments))

				received_data = Client_socket_.recv(self.MAX_SIZE)
				# print(f"Length of data received: {len(received_data)//(1024*1024)} MB")

				f.write(received_data)
				total_data_received += self.MAX_SIZE
				print(f"Data Received: {total_data_received//(1024*1024)} MB/{file_size//(1024*1024)} MB", end = "\r")

			if file_size % self.MAX_SIZE != 0:
				Client_socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				Client_socket_.connect((self.HOST_ADDRESS, self.PORT+1+(file_size//self.MAX_SIZE)))

				received_data = Client_socket_.recv(file_size%self.MAX_SIZE)
				# print(f"Length of data received: {len(received_data)//(1024*1024)} MB")
				f.write(received_data)
				total_data_received += len(received_data)
				print(f"Data Received: {total_data_received//(1024*1024)} MB/{file_size//(1024*1024)} MB", end = "\r")

			f.close()


			print(f"{file_name} successfully received!")
		
		#if file is a folder
		else:
			time.sleep(1)


	def Upload_file(self):
		#Send an indicator to prepare server to receive file
		self.Client_socket.sendall(bytes("Instruction2", 'utf-8'))
		#File Path will be entered using Tkinter
		file_name = "The_Social_Network.mkv"
		file_name_with_path = "./The_Social_Network.mkv"
		self.Client_socket.sendall(bytes(f"{len(file_name):<{self.HEADER_LENGTH}}", 'utf-8'))
		self.Client_socket.sendall(bytes(file_name, 'utf-8'))
		print(f"{file_name} is requested to upload")
		f = open(self.current_directory+"/"+file_name, 'rb')
		file_data = f.read()
		file_length = len(file_data)
		print(f"size of file {file_length//(1024*1024)} MB!")
		print(f"length of data we are gonna send: {len(file_data)}")
		self.Client_socket.sendall(bytes(f"{file_length:<{self.HEADER_LENGTH}}", "utf-8"))
		self.Client_socket.sendall(file_data)
		f.close()
		print(f"{file_name} has been sent!")

	def Remove_file(self):
		for i in range (len(self.file_list)):
			print((i+1), self.file_list[i])

		file_name = self.file_list[int(input())-1]
		self.Client_socket.sendall(bytes("Instruction3", 'utf-8'))
		self.Client_socket.sendall(bytes(f"{len(file_name):>{self.HEADER_LENGTH}}", 'utf-8'))
		self.Client_socket.sendall(bytes(file_name, 'utf-8'))

		success = self.Client_socket.recv(1)
		if success == b'1':
			print(f"{file_name} successfully deleted!")
		else:
			print(f"Could not delete {file_name}!")

	def Rename_file(self):
		for i in range (len(self.file_list)):
			print((i+1), self.file_list[i])
	
		file_name = self.file_list[int(input())-1]
		new_name = input("Please enter renamed name: ")

		self.Client_socket.sendall(bytes("Instruction4", 'utf-8'))
		self.Client_socket.sendall(bytes(f"{len(file_name):>{self.HEADER_LENGTH}}", 'utf-8'))
		self.Client_socket.sendall(bytes(file_name, 'utf-8'))
		self.Client_socket.sendall(bytes(f"{len(new_name):>{self.HEADER_LENGTH}}", 'utf-8'))
		self.Client_socket.sendall(bytes(new_name, 'utf-8'))
		
		success = self.Client_socket.recv(1)
		if success == b'1':
			print(f"{file_name} successfully renamed to {new_name}!")
		else:
			print(f"Could not rename {file_name}!")

	# def Move_file(Client_socket,):
		# Client_socket.send(bytes("Instruction5", 'utf-8'))
	def Back(self):
		if self.current_directory == "./Local_server_files":
			print("You are already at home Directory")
		else:
			self.previous_directory.append(self.current_directory)
			self.current_directory = self.current_directory[:((self.current_directory[::-1].find('/')+1)*-1)]

	def Forward(self):
		if self.previous_directory == ["./Local_server_files"]:
			print("Can't go forward")
		else:
			self.current_directory = self.previous_directory[-1]
			self.previous_directory.pop(-1)

	def Access_folder(self):
		for i in range (len(self.file_list)):
			print((i+1), self.file_list[i])
	
		print("Please enter folder number: ")
		folder = self.file_list[int(input())-1]
		if folder in self.file_list:
			self.current_directory = os.path.join(self.current_directory, folder)
		else:
			print(f"{folder} does not exist")

	def refresh_current_hiararcy(self):
		# print("refresh_current_hiararcy Function")
		self.Client_socket.sendall(bytes("Instruction6", 'utf-8'))
		# print("able to send first message")
		self.Client_socket.sendall(bytes(f"{len(self.current_directory):>{self.HEADER_LENGTH}}", 'utf-8'))	
		self.Client_socket.sendall(bytes(f"{self.current_directory}", 'utf-8'))
		list_data_length = int(self.Client_socket.recv(self.HEADER_LENGTH).decode('utf-8').strip())
		self.file_list = pickle.loads(self.Client_socket.recv(list_data_length))

	def Search(self):
		print(f"{self.current_directory} is your current directory!")
		string = input("please enter: ")
		self.Client_socket.sendall(bytes("Instruction7", 'utf-8'))
		#Sending Current Directory
		self.Client_socket.sendall(bytes(f"{len(self.current_directory):>{self.HEADER_LENGTH}}", 'utf-8'))	
		self.Client_socket.sendall(bytes(f"{self.current_directory}", 'utf-8'))
		#Sending String
		self.Client_socket.sendall(bytes(f"{len(string):>{self.HEADER_LENGTH}}", 'utf-8'))	
		self.Client_socket.sendall(bytes(f"{string}", 'utf-8'))
		#Expecting Pickled List
		list_data_length = int(self.Client_socket.recv(self.HEADER_LENGTH).decode('utf-8').strip())
		Search_list = pickle.loads(self.Client_socket.recv(list_data_length))
		for data in Search_list:
			print(data)

	def Close_connection(self):
		self.Client_socket.close()
