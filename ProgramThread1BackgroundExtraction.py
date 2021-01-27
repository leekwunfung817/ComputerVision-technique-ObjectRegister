
'''
cd /Users/leekwunfung/Desktop/ObjExtractor/
python3 ProgramThread1BackgroundExtraction.py
'''

import cv2
import time
import Denoise
import Debug
import datetime

import numpy

fail_count = 0
isIPCam = 0

# arr = []
com = None

var = {}

var['is_moving'] = None

var['lastCaptureTime'] = None
var['lastMovingTime'] = None

var['pre_bg'] = None
var['bg'] = None

var['background'] = []
backgroundMovementTimeout = 3
backgroundPerCapture = 10

ip_cam = '192.168.1.197'

ignore = cv2.imread('ignore.icfg.png')

id_position = cv2.imread('id_position.icfg.png')

# id_position.icfg - define captured area align with car-parking position. (For function 3)
#     1.red
#     2.orange
#     3.yellow
#     4.green
#     5.blue
#     6.purple
#     7.pink
#     8.brown
#     9.black
#     10.white
#     11.gray

red = (255,0,0)
orange = (255,147,0)
yellow = (255,255,0)
green = (0,255,0)
blue = (0,0,255)
purple = (135,78,254)
pink = (255,138,216)
brown = (170,121,66)
black = (0,0,0)
white = (255,255,255)
gray = (128,128,128)

# red_extract = 
# orange_extract = 
# yellow_extract = 
# green_extract = 
# blue_extract = 
# purple_extract = 
# pink_extract = 
# brown_extract = 
# black_extract = 
# white_extract = 
# gray_extract = 


def immediateBackgroundCapturing(okay, frame):
	# background.append(frame)
	var['pre_bg'] = frame
	return True

def accumulateBackgroundCapturing(okay, frame):
	# 1. Stop capturing background when something moving
	if var['is_moving']:
		var['lastMovingTime'] = time.time()
		Debug.log('2.Something moving')
		return False
	elif var['lastMovingTime'] != None:
		
		if (time.time() - var['lastMovingTime'])<backgroundMovementTimeout:
			Debug.log('2.1 Movement timeout at'+str(backgroundMovementTimeout-(time.time() - var['lastMovingTime'])))
			return False
		else:
			Debug.log('2.2 Moving stopped!!!')
			var['lastMovingTime'] = None

	# 2. Stop capture the background when too high frequent
	if var['lastCaptureTime']==None:
		var['lastCaptureTime'] = time.time()
		Debug.log('3.initialise capture time')
	elif (time.time() - var['lastCaptureTime'])<backgroundPerCapture:
		# for background array appending (situation: last capture timeout)
		# Debug.log('3.Capture too high frequent, timeout at '+str(backgroundPerCapture-(time.time() - var['lastCaptureTime']))+' second')
		return False
	else:
		var['lastCaptureTime'] = None
		Debug.log('3.Capture correctly, background len:'+str(len(var['background'])))
		var['lastCaptureTime'] = time.time()
		if len(var['background'])>3:
			cv2.imwrite('bg/'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+'.jpg', var['background'][0])
			var['background'] = var['background'][1:]
		var['background'].append(frame)
		Debug.log('3.1. background len:'+str(len(var['background'])))
	return True
	
def inputFrame(okay, frame, callback, accumulateCallback):
	(h,w,d)=frame.shape
	frame = Denoise.run(frame)
	if not okay:
		fail_count+=1
		if fail_count==3:
			exit()

	if var['pre_bg'] is not None:
		var['is_moving'] = callback(var['pre_bg'],frame)
		if var['is_moving']:
			Debug.log('background len '+str(len(var['background'])))
	
	if len(var['background'])>=3:
		var['had_object'] = accumulateCallback(var['background'],frame)
		if var['had_object']:
			Debug.log('b:had_object')
			pass

	succeed = False
	succeed = immediateBackgroundCapturing(okay, frame)
	succeed = accumulateBackgroundCapturing(okay, frame)



	# for background array appending (situation: start up)
	# initialise the background buffer

def IPCam(callback):
	'''
"C:/Users/Administrator/AppData/Local/Programs/Python/Python36/python" app.py
"C:/Users/Administrator/AppData/Local/Programs/Python/Python36/Scripts/pip3.6" install opencv-python
	'''
	# cap = cv2.VideoCapture('rtsp://admin:yRpvx@192.168.1.197')
	return cv2.VideoCapture('rtsp://admin:@'+ip_cam)

def webcam(callback):
	return cv2.VideoCapture(0)
import os

def run(callback,accumulateCallback):
	if isIPCam:
		cap = IPCam(callback)
	else:
		cap = webcam(callback)
	while True:
		okay, frame = cap.read()
		frame = cv2.bitwise_and(frame,ignore)
		if not os.path.isfile('curDemo.png'):
			cv2.imwrite('curDemo.png',frame)
		inputFrame(okay, frame, callback, accumulateCallback)
	pass

if __name__ == "__main__":
	pass
