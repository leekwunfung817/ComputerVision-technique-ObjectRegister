
'''
cd /Users/leekwunfung/Desktop/ObjExtractor/src
python -m compileall
python3 app.py

Python version
3.6.4 (v3.6.4:d48ecebad5, Dec 18 2017, 21:07:28) 
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)]
Version info.
sys.version_info(major=3, minor=6, micro=4, releaselevel='final', serial=0)
app_name Cam1

pip install matplotlib==3.0.3

https://www.python.org/downloads/release/python-364/
https://github.com/leekwunfung817/ComputerVision-technique-ObjectRegister

'''
import sys
sys.path.insert(1, '../bin')
py_name = sys.argv[0]
app_name = py_name.replace('.pyc','').replace('.py','')
print('app_name',app_name)
print(sys.argv)
exec('import '+app_name)
exec('config = '+app_name+'.config')
import func_denoise
import os

# print("Python version")
# print (sys.version)
# print("Version info.")
# print (sys.version_info)
# import matplotlib
# print (matplotlib.__version__)
# import imutils
# print (imutils.__version__)
# import cv2
# print (cv2.__version__)

# 3.3.3
# 0.5.4
# 4.5.1

# print(config)

import cv2
import numpy
import datetime
import func_any

import p1_ImmediateCapture
import p2_StaticCapture
import p3_MvCapture
import func_any


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

# (Process 3) run when buffer have three background images. Only for moving stage.
var['mvBg'] = {}
var['lastMvBg'] = None

import func_camera

def OnCapture(frame):
	if not os.path.isfile('curDemo.png'):
		cv2.imwrite('curDemo.png',frame)
	frame = cv2.bitwise_and(frame,config['ignore'])

	# Step 1 - receive camera capture ( current python t1.py run() )
	var['frame'] = frame
	(h,w,d)=frame.shape
	frame = func_denoise.GaussianBlur(frame)

	# for background array appending (situation: start up)
	# initialise the background buffer
	if config['p1']:
		p1_ImmediateCapture.process(var)
	if config['p2']:
		p2_StaticCapture.process(var)
	if config['p3']:
		p3_MvCapture.process(var)

func_camera.CaptureLoop(OnCapture)
