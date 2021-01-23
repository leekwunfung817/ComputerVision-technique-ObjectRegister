
'''
cd /Users/leekwunfung/Desktop/ObjExtractor/
python3 ProgramThread1BackgroundExtraction.py
'''

import cv2
import time

fail_count = 0
isIPCam = 0

arr = []
com = None

var = {}

var['lastCaptureTime'] = None
var['lastMovingTime'] = None

var['pre_bg'] = None

backgroundMovementTimeout = 3
backgroundPerCapture = 3


def immediatelyMode(okay, frame, callback):
	is_moving = callback(var['pre_bg'],com,frame)
	

def delayMode(okay, frame, callback):

	# for background array appending (situation: last capture timeout)
	is_moving = callback(var['pre_bg'],com,frame)
	# 2. Stop capturing background when something moving
	if is_moving:
		var['lastMovingTime'] = time.time()
		print('2.Something moving')
		return
	elif var['lastMovingTime'] != None:
		print('2.Something just moved')
		if (time.time() - var['lastMovingTime'])<backgroundMovementTimeout:
			return
		else:
			print('2.Moving stopped!!!')
			var['lastMovingTime'] = None

	# 3. Stop capture the background when too high frequent
	if var['lastCaptureTime']==None:
		var['lastCaptureTime'] = time.time()
		print('3.initialise capture time')
	elif (time.time() - var['lastCaptureTime'])<backgroundPerCapture:
		print('3.Capture too high frequent ',(time.time() - var['lastCaptureTime']),' second')
		return
	else:
		print('3.Capture correctly')
		arr.pop()
		arr.append(frame)
		var['lastCaptureTime'] = time.time()
	
import Denoise
def inputFrame(okay, frame, callback):
	frame = Denoise.run(frame)
	if not okay:
		fail_count+=1
		if fail_count==3:
			exit()

	# for background array appending (situation: start up)
	# 1. initialise the background buffer
	if var['pre_bg'] is not None:
		# cv2.imshow('bg', var['pre_bg'])
		# cv2.imshow('frame', frame)
		# cv2.waitKey(1)

		delayMode(okay, frame, callback)
	# immediatelyMode(okay, frame, callback)

	var['pre_bg']=frame
	


def IPCam(callback):
	inputFrame(True, None, callback)
	pass

def webcam(callback):
	camera = cv2.VideoCapture(0)
	while True:
		okay, frame = camera.read()
		inputFrame(okay, frame, callback)
		# cv2.imshow('video', frame)
		# cv2.waitKey(1)
	pass

def run(callback):
	if isIPCam:
		IPCam(callback)
	else:
		webcam(callback)
		
if __name__ == "__main__":
	pass
