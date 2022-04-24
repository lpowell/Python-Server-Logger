# python server log

import socket, getopt, sys, time 
from datetime import datetime
from contextlib import closing
def ServerStart(HOST, PORT):
	try:
		while True:
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
				try:
					s.bind((HOST,PORT))
				except Exception as error:
					print("Error:", error, "has occured.")
				s.listen()
				conn, addr = s.accept()
				with conn:
					Log_Output("\n---------------------------")
					output = ("Connected by", addr)
					Log_Output("".join(str(output)))
					Log_Output("<-- Attempting to receive data -->\n")
					while True:
						try:
							data = conn.recv(1024)
							Log_Output(data.decode())
							nodata = 0
							conn.send("Connection Logged\n".encode())
							#print(nodata)
							if not data:
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
				#print("Address in use, attempting connection in 3 seconds")
				time.sleep(0.1)
				ServerStart(HOST, PORT)
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
	with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
		if s.connect_ex((host, port)) ==0:
			return 1 #open
		else:
			return 0 #in use/closed
def Main():
	global console
	console = True
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
