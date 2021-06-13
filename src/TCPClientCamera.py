
#!/usr/bin/env python3
import io
import os 
import socket
import cv2
import numpy as np

def byte2CVImg(fdata):
	print('Show Image 1')
	imdata = np.frombuffer(fdata, np.uint8)
	print('imdata',imdata)
	decoded = cv2.imdecode(imdata, -1)
	print('Show Image 1.2')
	return decoded

def callback(decoded):
	print('Show Image 2')
	if decoded is None:
		print('Decode fail')
		return
	print('Show Image 2.1',decoded.shape)
	cv2.imshow('buf',decoded)
	cv2.waitKey(1)
	print('Show Image 3')

def writeOnce(fdata, filename='file.jpg'):
	print('Write file 1')
	if not os.path.isfile(filename):
		print('Write file 2')
		f = open(filename, 'wb')
		f.write(fdata)
		f.close()
	print('Write file 3')

def receiveBytes(conn):
	fdata = bytes()
	while True:
		data = conn.recv(1024*300000)
		# print('Received ',len(data))
		if not data:
			break
		fdata += data;
	print('Received ',len(fdata))
	if len(fdata)==0:
		return None
	return fdata

def capture(HOST,PORT,callback):
	while True:
		try:
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
				print(HOST,PORT)
				s.bind((HOST, PORT))
				s.listen()
				print('Accept')
				conn, addr = s.accept()
				print('Connected by', addr)
				with conn:
					fdata = receiveBytes(conn)
					if fdata is not None:
						decoded = byte2CVImg(fdata)
						callback(decoded)
						# conn.sendall('AB1234'.encode())
		except Exception as e:
			raise e