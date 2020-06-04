from client import Client
import signal
import time

# try:
#     loop_forever()
# except Exception as exc:
#     print(exc)

client = Client()

# def Start_client_and_talk_to_server(PORT_NO):
def Start_client_and_talk_to_server():
	
	# try:
	# client.PORT = PORT_NO
	# try:
	client.Connect_to_server()
	print("Succesfully connected")
	# except:
	# 	print("Not Possible")
	# 	print("Trying again with different port")
	# 	print(f"Current Client Port {client.PORT}")
	# 	client.PORT = client.PORT + 1
	# 	print(client.PORT)
	# 	client.Connect_to_server()
	
	
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

# signal.signal(signal.SIGALRM, Start_client_and_talk_to_server)
# signal.alarm(5)

Start_client_and_talk_to_server()