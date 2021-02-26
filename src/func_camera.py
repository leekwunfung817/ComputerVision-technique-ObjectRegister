import sys
py_name = sys.argv[0]
app_name = py_name.replace('.pyc','').replace('.py','')
exec('import '+app_name)
exec('config = '+app_name+'.config')

import time
import cv2
import func_any

fail_count = 0
def IPCam():
	'''
"C:/Users/Administrator/AppData/Local/Programs/Python/Python36/python" app.py
"C:/Users/Administrator/AppData/Local/Programs/Python/Python36/Scripts/pip3.6" install opencv-python
	'''
	# cap = cv2.VideoCapture('rtsp://admin:yRpvx@192.168.1.197')
	func_any.log('IP cam capture')
	return cv2.VideoCapture(config['ip_cam'])

def webcam():
	func_any.log('Webcam capture')
	return cv2.VideoCapture(0)


def reloadCapture():
	if config['isIPCam']>0:
		return IPCam()
	else:
		return webcam()

def CaptureLoop(callback):
	cap = None
	while True:
		while cap is None:
			cap = reloadCapture()
		okay, frame = cap.read()
		if not okay:
			time.sleep(3)
			cap = reloadCapture()
			continue
		callback(frame)
		if not okay:
			fail_count+=1
			if fail_count==3:
				exit()