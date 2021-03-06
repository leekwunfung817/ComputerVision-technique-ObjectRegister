import socket

def socket(ip,port,mystring):
	# host = socket.gethostname()
	# port = 12345
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((ip,port))
	s.sendall(bytes(mystring, 'utf-8'))
	# data = s.recv(1024)
	s.close()
	# print('Received', repr(data))
