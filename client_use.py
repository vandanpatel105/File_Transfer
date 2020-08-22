from client import Client
import signal
import time
import sys

client = Client()
client.HOST_ADDRESS = input("Enter Server IP: ")


for i in range (1, len(sys.argv)):
#--PORT=
#--IP=
#--CONNECTIONS=


	if sys.argv[i][:5] == "--IP=":
		client.HOST_ADDRESS = sys.argv[i][5:]
	elif sys.argv[i][:7] == "--PORT=":
		client.PORT = int(sys.argv[i][7:])
	else:
		print("Invalid Argument")

def Start_client_and_talk_to_server():
	
	client.Connect_to_server()
	print("Succesfully connected")
	
	while True:

		client.refresh_current_hiararcy()
		print("Refreshed_Hiararcy")
		print(f"Port Id after refreshed hiararcy : {client.PORT}")
		print("1:Request a file\n2:Upload a file\n3:Remove a file\n4:Rename a file\n5:Back\n6:Forward\n7:Enter in a folder\n8:Search a file\n")
		action = int(input())
		
		# break
		if action == 1:
			
			client.Download_file()

		elif action == 2:

			client.Upload_file()

		elif action == 3:
			
			client.Remove_file()

		elif action == 4:

			client.Rename_file()

		elif action == 5:
			
			client.Back()

		elif action == 6:
			
			client.Forward()

		elif action == 7:
			
			client.Access_folder()

		elif action == 8:
			
			client.Search()

		else:
			print("please enter correct number!")

Start_client_and_talk_to_server()
