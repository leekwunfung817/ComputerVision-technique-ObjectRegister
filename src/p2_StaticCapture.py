import func_any

import sys
py_name = sys.argv[0]
app_name = py_name.replace('.pyc','').replace('.py','')
exec('import '+app_name)
exec('config = '+app_name+'.config')

import func_video
import func_ImgDiff
import time
import numpy
import cv2

import p21_CoorAnalyse

# pre-define method 
# movement
def whenMoving(var):
	if config['p2_debug_flow']:
		func_any.log('P2.Something moving')
	if config['debug_video']:func_any.log('P2.Video recording')
	var['lastMovingTime'] = time.time()
	var['lastMovingStage'] = 'MV' # Moving
	return False
def afterMoved(var):
	if config['p2_debug_flow']:
		func_any.log('P2.1 Movement timeout at'+str(config['backgroundMovementTimeout']-(time.time() - var['lastMovingTime'])))
	if config['debug_video']:func_any.log('P2.1 Video will stop at'+str(config['backgroundMovementTimeout']-(time.time() - var['lastMovingTime'])))
	var['lastMovingStage'] = 'TO' # Timeout
	return False
def finishMovement(var):
	if config['p2_debug_flow']:func_any.log('P2.2 Moving stopped!!!')
	if config['debug_video']:func_any.log('P2.2 Video capture stopped!!!')
	var['lastMovingStage'] = 'MD' # Moved			
	var['lastMovingTime'] = None
	# allow pass

# capture control
def firstCapture(var):
	var['lastCaptureTime'] = time.time()
	if config['p2_debug_flow']:
		func_any.log('P2.3.initialise capture time')
	# allow pass
def delayCapture(var):
	if config['p2_debug_flow']:
		func_any.log('P2.4.Capture too high frequent, timeout at '+str(config['backgroundPerCapture']-(time.time() - var['lastCaptureTime']))+' second')
	return False
def delayTimeoutCapture(var):
	var['lastCaptureTime'] = None
	if config['p2_debug_flow']:
		func_any.log('P2.3.Capture correctly, background len:'+str(len(var['background'])))
	var['lastCaptureTime'] = time.time()
	if len(var['background'])>=4:
		# cv2.imwrite('bg/'+func_any.dts()+'.jpg', var['background'][0])
		var['background'] = var['background'][1:]
	# print('bgl:',len(var['background']))
	var['background'].append(var['frame'])
	# func_any.log('3.1. background len:'+str(len(var['background'])))
	# allow pass

# (Process 2) run when buffer have three background images. Only for stopped stage.
def accumulateBackgroundCapturing(var):
	# 1. Stop capturing background when something moving
	if var['is_moving']:
		return whenMoving(var)
	elif var['lastMovingTime'] != None:
		if (time.time() - var['lastMovingTime'])<config['backgroundMovementTimeout']:
			return afterMoved(var)
		else:
			finishMovement(var)

	# 2. Stop capture the background when too high frequent
	if var['lastCaptureTime']==None:
		firstCapture(var)
	elif (time.time() - var['lastCaptureTime'])<config['backgroundPerCapture']:
		# for background array appending (situation: last capture timeout)
		return delayCapture(var)
	else:
		delayTimeoutCapture(var)
	return True


# (Process 2) three layers accumulate callback (stop mode)
def HaveObject(var):
	objs = func_ImgDiff.compareForMovementData(numpy.array(var['background']),var['frame'],var['com'],config['p2_dilate_enlarge'],config['p2_minDiff'])
	(originRect,filteredAlpha,objectMask,objs_coor) = objs

	# input 
	# coor [(x,y,w,h,img)]

	# output 
	# last frame coor [ID](brfore coor,after coor)
	# history [ID](brfore coor,after coor,distance,direction)
	
	centerCoors = p21_CoorAnalyse.run(var,objs_coor)
	if config['p2_demo']:
		cv2.imshow('HaveObject - originRect',originRect)
		cv2.imshow('HaveObject - moveMask',objectMask)
		cv2.imshow('HaveObject',cv2.hconcat([originRect,filteredAlpha]))
		
	# make decidion for write video or not
	# func_video.WriteVideo2(var,var['frame'],'VideoMovement')
	# func_video.WriteVideo2(var,originRect,'VideoObjects')
	func_video.WriteVideo2(var,filteredAlpha,'VideoMovement_filteredAlpha')

	if config['p2_debug_flow']:
		print('P2.'+str(len(objs_coor))+' object(s) detected.')
	return len(objs_coor) > 0

def process(var):
	config['process']=2
	# (Process 2) # Step 2 - compare between background and current capture ( main python app.py )
	if len(var['background'])>=3:
		# func_any.log('P2.enough 3 background frame')
		var['had_object'] = HaveObject(var)

	if var['had_object']:
		if config['p2_debug_flow']:print('P2.ObjectDetected')

	# (Process 2) # Step 3 - process the background buffer ( current python t1.py )
	succeed = accumulateBackgroundCapturing(var)
