# python server log

import socket, getopt, sys, time 
from datetime import datetime
from contextlib import closing
# import libraries
def ServerStart(HOST, PORT):
	# Create the server
	try:
		while True:
			# forever loop
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
				# using s as socket object 
				try:
					s.bind((HOST,PORT))
					# bind to the specified port and address 'Listening'
				except Exception as error:
					print("Error:", error, "has occured.")
				s.listen()
				# listen to the bound port
				conn, addr = s.accept()
				# accept the connection ip and data
				with conn:
					# using the data
					Log_Output("\n---------------------------")
					output = ("Connected by", addr)
					Log_Output("".join(str(output)))
					Log_Output("<-- Attempting to receive data -->\n")
					while True:
						# while data exists
						try:
							data = conn.recv(1024)
							# data restructured into a more printable form
							Log_Output(data.decode())
							# decode the data to print it
							nodata = 0
							conn.send("Connection Logged\n".encode())
							# encode and reply to the data source ip
							#print(nodata)
							if not data:
								# in the case of no data end data loop
								Log_Output("<-- DATA NOT RECIEVED -->")
								nodata = 1
								break
							#conn.sendall(data)
						except (BrokenPipeError):
							#print("BP ERROR: "+nodata)
							if nodata == 0:
								Log_Output("<-- Connection closed -->")
							#else:
							#	Log_Output("Cannot send data to client.\n")
							pass
							break
						except (ConnectionResetError) as error:
							try:
								if nodata == 0:
									Log_Output("<-- Connection closed -->")									
							except:
								Log_Output("<-- Connection has been reset -->")
							pass
							break
						except Exception as error:
							Log_Output(("Connection error: ", error, " has occured.\n"))
							pass
			if check_socket(HOST, PORT) == 0:
				# check and see if the socket is still in use and sleep for .1 if it is
				#print("Address in use, attempting connection in 3 seconds")
				time.sleep(0.1)
				ServerStart(HOST, PORT)
				# recursive function
	except (KeyboardInterrupt):
		Log_Output("---------------------------")
		Log_Output("Application closed by user")
		Log_Output("---------------------------")
		pass
		quit()
	except Exception as error:
		Log_Output(("Error: ", error, " has occured."))
		pass
def check_socket(host, port):
	# function to check if socket is in use
	with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
		# using s as socket object
		if s.connect_ex((host, port)) ==0:
			return 1 #open
		else:
			return 0 #in use/closed
def Main():
	global console
	console = True
	# getopts work around for console output
	arguments=sys.argv[1:]
	options ="ha::p::b"
	try:
		ArgV, Value = getopt.getopt(arguments, options)
		for CurrentARG, CurrentVAL in ArgV:
			if CurrentARG in ('-h'):
				print("PYTHON SERVER & CONNECTION LOGGER\
						\n-a Host Address\
						\n-p Port to run on\
						\n-b Hide console output\
						\n-h Display this help page")
				quit()
			elif CurrentARG in ('-a'):
				host = CurrentVAL
			elif CurrentARG in ('-p'):
				port = int(CurrentVAL)
			#elif CurrentARG in ('-l'):
			#	Log_Init()
			elif CurrentARG in ('-b'):
				console = False
	except getopt.GetoptError:
		print("-h for help" )
	Log_Init()
	ServerStart(host,port)
def Log_Init():
	# log file creation
	global f
	d = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	f=open(d+'.txt', 'w')
	Log_Output("Starting Log @ "+d)
def Log_Output(strToLog):
	if console:
		print(strToLog)
	else:
		print(strToLog, file=f)
Main()