
'''
cd /Users/leekwunfung/Desktop/ObjExtractor/
python3 ProgramThread1BackgroundExtraction.py
'''

import cv2
import time
import Denoise
import Debug
import datetime

import sys
sys.path.insert(1, '../bin')
exec('import '+sys.argv[0].replace('.py',''))
exec('config = '+sys.argv[0].replace('.py','')+'.config')

import numpy


fail_count = 0
isIPCam = 0

# arr = []
com = None

var = {}

var['is_moving'] = None
var['had_object'] = None
var['had_stop'] = None

var['lastCaptureTime'] = None
var['lastMovingTime'] = None
var['lastMovingStage'] = None

var['pre_bg'] = None
var['bg'] = None

var['background'] = []
var['movingBackground'] = []

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

def dts():
	return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

# (Process 1) run each frame
def immediateBackgroundCapturing(okay, frame):
	# background.append(frame)
	var['pre_bg'] = frame
	return True

# (Process 2) run when buffer have three background images. Only for stopped stage.
def accumulateBackgroundCapturing(okay, frame):
	# 1. Stop capturing background when something moving
	if var['is_moving']:
		var['lastMovingTime'] = time.time()
		var['lastMovingStage'] = 'MV' # Moving
		if config['debug_t1']:
			Debug.log('2.Something moving')
		return False
	elif var['lastMovingTime'] != None:
		
		if (time.time() - var['lastMovingTime'])<config['backgroundMovementTimeout']:
			if config['debug_t1']:
				Debug.log('2.1 Movement timeout at'+str(config['backgroundMovementTimeout']-(time.time() - var['lastMovingTime'])))
			var['lastMovingStage'] = 'TO' # Timeout
			return False
		else:
			if config['debug_t1']:
				Debug.log('2.2 Moving stopped!!!')
			var['lastMovingStage'] = 'MD' # Moved			
			var['lastMovingTime'] = None

	# 2. Stop capture the background when too high frequent
	if var['lastCaptureTime']==None:
		var['lastCaptureTime'] = time.time()
		if config['debug_t1']:
			Debug.log('3.initialise capture time')
	elif (time.time() - var['lastCaptureTime'])<config['backgroundPerCapture']:
		# for background array appending (situation: last capture timeout)
		# Debug.log('3.Capture too high frequent, timeout at '+str(config['backgroundPerCapture']-(time.time() - var['lastCaptureTime']))+' second')
		return False
	else:
		var['lastCaptureTime'] = None

		if config['debug_t1']:
			Debug.log('3.Capture correctly, background len:'+str(len(var['background'])))
		var['lastCaptureTime'] = time.time()
		if len(var['background'])>3:
			cv2.imwrite('bg/'+dts()+'.jpg', var['background'][0])
			var['background'] = var['background'][1:]
		var['background'].append(frame)
		# Debug.log('3.1. background len:'+str(len(var['background'])))
	return True

# (Process 3) run when buffer have three background images. Only for moving stage.
def movingBackgroundCapturing(okay, frame):
	return True


def inputFrame(okay, frame, callbacks):

	OnCapture=callbacks['OnCapture']
	accumulateCapture=callbacks['accumulateCapture']
	movingCapture=callbacks['movingCapture']

	var['frame'] = frame
	(h,w,d)=frame.shape
	frame = Denoise.run(frame)
	if not okay:
		fail_count+=1
		if fail_count==3:
			exit()

	# (Process 1)
	if var['pre_bg'] is not None:
		var['is_moving'] = OnCapture(var)
		# if var['is_moving']:
			# Debug.log('background len '+str(len(var['background'])))
	
	# (Process 2)
	if len(var['background'])>=3:
		var['had_object'] = accumulateCapture(var)
		# if var['had_object']:
		# 	Debug.log('b:had_object')
		# 	pass

	# (Process 3)
	if len(var['movingBackground'])>=3:
		var['had_stop'] = movingCapture(var)

	# succeed = False
	# (Process 1)
	succeed = immediateBackgroundCapturing(okay, frame)
	# (Process 2)
	succeed = accumulateBackgroundCapturing(okay, frame)
	# (Process 3)
	succeed = movingBackgroundCapturing(okay, frame)


	# for background array appending (situation: start up)
	# initialise the background buffer

def IPCam():
	'''
"C:/Users/Administrator/AppData/Local/Programs/Python/Python36/python" app.py
"C:/Users/Administrator/AppData/Local/Programs/Python/Python36/Scripts/pip3.6" install opencv-python
	'''
	# cap = cv2.VideoCapture('rtsp://admin:yRpvx@192.168.1.197')
	return cv2.VideoCapture('rtsp://admin:@'+config['ip_cam'])

def webcam():
	return cv2.VideoCapture(0)

import os

def run(callbacks):
	if config['isIPCam']>0:
		cap = IPCam()
	else:
		cap = webcam()
	while True:
		okay, frame = cap.read()
		frame = cv2.bitwise_and(frame,config['ignore'])
		# if not os.path.isfile('curDemo.png'):
		# 	cv2.imwrite('curDemo.png',frame)
		inputFrame(okay, frame, callbacks)
	pass

if __name__ == "__main__":
	pass
