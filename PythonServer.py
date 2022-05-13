# python server log

import socket, getopt, sys, time, os
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
					conn.send(">All connections Logged\n".encode())
					conn.send(">Only authorized users beyond this point\n".encode())
					conn.send("User: ".encode())
					uname = conn.recv(1024)
					if uname.decode().split()[0] != "admin":
						conn.send(">Login failed ... Closing server ...".encode())
						Log_Output("---------------------------")
						Log_Output("Failed Logon @ username")
						Log_Output("---------------------------")
						break
					conn.send("Pass: ".encode())
					passw = conn.recv(1024)
					if passw.decode().split()[0] != "Password!123":
						conn.send(">Login failed ... Closing server ...".encode())
						Log_Output("---------------------------")
						Log_Output("Failed Logon @ password")
						Log_Output("---------------------------")
						break
					conn.send(">Welcome, admin!\n".encode())
					while True:
						# while data exists
						try:
							data = conn.recv(1024)
							# data restructured into a more printable form
							Log_Output(data.decode())
							if data:
								# Data processing block 
								if data.decode().split()[0] == "close":
									conn.send(">Closing ... Goodbye ...\n".encode())
									Log_Output("<-- Connection closed via client -->")
									break
								elif data.decode().split()[0] == "do":
										if data.decode().split()[1] == "help":
											conn.send(">do\n\thelp\n\texit\n\tlist\n\ttransfer\n".encode())
										if data.decode().split()[1] == "exit":
											conn.send(">Closing server ... Goodbye ...\n".encode())
											Log_Output("---------------------------")
											Log_Output("Application closed by client")
											Log_Output("---------------------------")
											quit()
										if data.decode().split()[1] == "list":
											try:
												directory = data.decode().split()[2]
												# print(directory)
												dirout = os.listdir(directory)
												while True:
													for x in range(len(dirout)):
														output = "\t" + dirout[x] + "\n"
														conn.send(output.encode())
													break
												Log_Output(("Directory list for", directory, "sent to", addr))
											except (FileNotFoundError):
												conn.send(">Directory or file not found\n".encode()) 
												pass
											except (IndexError):
												conn.send(">Please specify a directory\n\t\"do list /home\"\n".encode())
												pass
											except Exception as error:
												conn.send(">Error, try again\n".encode())
										if data.decode().split()[1] == "transfer":
											conn.send("Not implemented\n".encode())
							# decode the data to print it
							nodata = 0
							# encode and reply to the data source ip
							if not data:
								# in the case of no data end data loop
								Log_Output("<-- DATA NOT RECIEVED -->")
								nodata = 1
								break
						except (BrokenPipeError):
							if nodata == 0:
								Log_Output("<-- Connection closed -->")
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
				time.sleep(0.1)
				ServerStart(HOST, PORT)
				# recursive function
	except (KeyboardInterrupt):
		Log_Output("---------------------------")
		Log_Output("Application closed by server")
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
	if os.name == 'nt':
		# env = os.environ['USERPROFILE'] +"/Documents/"
		d = datetime.now().strftime("%Y-%m-%d @ (%H-%M-%S)")
		f=open(d +'.txt', 'w')
	else:
		f=open(d+'.txt', 'w')
	Log_Output("Starting Log @ "+d)
def Log_Output(strToLog):
	if console:
		print(strToLog)
	print(strToLog, file=f)
Main()