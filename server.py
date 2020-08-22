import socket
import os
import pickle
import select
import time
import re

class Server():
	
	def __init__(self):
		os.system("ipconfig >> IpDetails.txt")
		with open("IpDetails.txt") as f:
			self.HOST_ADDRESS = f.read().split("Wireless LAN adapter Wi-Fi:")[1].split("\n")[4].split(":")[1].strip()
		# self.HOST_ADDRESS = socket.gethostbyname(socket.gethostname())
		# self.HOST_ADDRESS = "192.168.0.111"
		self.PORT = 4444
		self.HEADER_LENGTH = 50
		self.MAX_CONNECTION = 10
		self.current_directory = "./Local_server_files"
		self.Instruction_Length = 12
		self.MAX_SIZE_MB = 256
		self.MAX_SIZE = self.MAX_SIZE_MB*1024*1024

	def Start_server(self):

		self.Server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.Server_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		self.Server_Socket.bind((self.HOST_ADDRESS, self.PORT))
		self.Server_Socket.listen(self.MAX_CONNECTION)

		print(f"Server is running on {self.HOST_ADDRESS}:{self.PORT}")

	def Send_requested_file(self, Client_socket):
		file_name_length = int(Client_socket.recv(self.HEADER_LENGTH).decode('utf-8').strip())
		print(f"file name length: {file_name_length}")
		file_name = Client_socket.recv(file_name_length).decode('utf-8').strip()
		print(f"file_name: {file_name}")
		print(f"{file_name} is requested to download")


		# if file is a file
		if os.path.isdir(self.current_directory+"/"+file_name) == False:
			f = open(self.current_directory+"/"+file_name, 'rb')

			file_size = os.stat(self.current_directory+"/"+file_name).st_size
			Client_socket.send(bytes(f"{file_size:<{self.HEADER_LENGTH}}", "utf-8"))

			print(f"size of file {file_size//(1024*1024)} MB!")
			Total_data_send = 0
			for segments in range (file_size//self.MAX_SIZE):
				file_data = f.read(self.MAX_SIZE)
				# print(f"length of data we are gonna send: {len(file_data)//(1024*1024)} MB")
				Client_socket.send(file_data)
				Total_data_send += self.MAX_SIZE
				print(f"Data Sent: {Total_data_send//(1024*1024)} MB/{file_size//(1024*1024)} MB", end = "\r")

			if file_size % self.MAX_SIZE != 0:
				file_data = f.read(file_size%self.MAX_SIZE)
				# print(f"length of data we are gonna send: {len(file_data)//(1024*1024)} MB")
				Client_socket.send(file_data)
				Total_data_send += len(file_data)
				print(f"Data Sent: {Total_data_send//(1024*1024)} MB/{file_size//(1024*1024)} MB", end = "\r")

			f.close()
		#if file is a folder
		else:
			
			time.sleep(1)
		
		print(f"{file_name} has been sent!")

	def Receive_file(self, Client_socket):

		file_name_length = int(Client_socket.recv(self.HEADER_LENGTH).decode('utf-8').strip())
		file_name = Client_socket.recv(file_name_length).decode('utf-8')
		print(f"redirecting {file_name} to function Download_file")
		#Send an indicator to prepare server to send file
		print(f"{file_name} will be received from Client")
		receivable_file_length = int(Client_socket.recv(self.HEADER_LENGTH).decode('utf-8').strip())
		print(f"receivable_file_length: {receivable_file_length//(1024*1024)} MB")
		f = open("./Local_server_files/copy_"+file_name, "wb")
		received_file_length = 0
		t0 = time.time()
		while(receivable_file_length > received_file_length):
			received_data = Client_socket.recv(receivable_file_length)
			length_recevied_data = len(received_data)
			t1 = time.time()
			if (t1-t0>1):
				print(f"length of data received: {received_file_length//(1024*1024):>6} MB/{receivable_file_length//(1024*1024):>6} MB", end="\r")
				t0 = t1
			received_file_length += length_recevied_data
			f.write(received_data)
		f.close()

	def Remove_file(self, Client_socket):
	
		file_name_length = int(Client_socket.recv(self.HEADER_LENGTH).decode('utf-8').strip())
		print(f"file name length: {file_name_length}")
		file_name = Client_socket.recv(file_name_length).decode('utf-8').strip()
		print(f"{file_name} is requested to be deleted")
		try:
			os.remove(os.path.join(self.current_directory, file_name))
			Client_socket.send(b'1')
			print(f"{file_name} Successfully removed")
		except:
			Client_socket.send(b'0')
			print(f"can not remove {file_name}")

	def Rename_file(self, Client_socket):

		file_name_length = int(Client_socket.recv(self.HEADER_LENGTH).decode('utf-8').strip())
		print(f"file name length: {file_name_length}")
		file_name = Client_socket.recv(file_name_length).decode('utf-8').strip()
		print(f"old file name: {file_name}")
		new_name_length = int(Client_socket.recv(self.HEADER_LENGTH).decode('utf-8').strip())
		print(f"new file name length: {new_name_length}")
		new_name = Client_socket.recv(new_name_length).decode('utf-8').strip()
		print(f"name of {file_name} is requested to change into {new_name}")

		try:
			os.rename(os.path.join(self.current_directory, file_name), os.path.join(self.current_directory, new_name))
			Client_socket.send(b'1')
			print(f"{file_name} successfully renamed to {new_name}!")

		except:
			Client_socket.send(b'0')
			print(f"Could not rename {file_name}!")

	# def Move_file(Client_socket,)

	def Send_file_list(self, Client_socket):

		file_name_length = int(Client_socket.recv(self.HEADER_LENGTH).decode('utf-8').strip())
		# print(f"file_name_length: {file_name_length}")
		file_name = Client_socket.recv(file_name_length).decode('utf-8').strip()
		print(f"file_name: {file_name}")
		file_list = os.listdir(file_name)
		# print(f"file List: {file_list}")
		pickled_file_list = pickle.dumps(file_list)
		Client_socket.send(bytes(f"{len(pickled_file_list):<{self.HEADER_LENGTH}}", 'utf-8'))
		Client_socket.send(pickled_file_list)

	def Search_(self, current_directory, reg_ex_string):
	
		matching_list = []
		file_folder_list = os.listdir(current_directory)
		for file_name in file_folder_list:
			file_name_path = os.path.join(current_directory, file_name)
			if re.search(reg_ex_string, file_name):
				matching_list.append(file_name_path)
			if os.path.isdir(file_name_path):
				matching_list += self.Search_(current_directory+'/'+file_name, reg_ex_string)
		return matching_list

	def Return_search(self, Client_socket):
		#Current Directory
		current_directory_length = int(Client_socket.recv(self.HEADER_LENGTH).decode('utf-8'))
		current_directory = Client_socket.recv(current_directory_length).decode('utf-8')
		#String
		String_length = int(Client_socket.recv(self.HEADER_LENGTH).decode('utf-8'))
		String = Client_socket.recv(String_length).decode('utf-8')

		reg_ex_string = re.compile(String, re.IGNORECASE)
		search_list = self.Search_(current_directory, reg_ex_string)

		pickled_search_list = pickle.dumps(search_list)
		Client_socket.send(bytes(f"{len(pickled_search_list):<{self.HEADER_LENGTH}}", 'utf-8'))
		Client_socket.send(pickled_search_list)
	
