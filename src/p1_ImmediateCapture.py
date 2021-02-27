import sys
py_name = sys.argv[0]
app_name = py_name.replace('.pyc','').replace('.py','')
exec('import '+app_name)
exec('config = '+app_name+'.config')

import func_any
import func_video
import func_ImgDiff
import cv2
import func_denoise

# (Process 1) immediately callback
def IsMoving(var):
	
	# print('Received capture:',img)
	objs = func_ImgDiff.compareForMovementData(var['pre_bg'],var['frame'],var['com'],config['p2_dilate_enlarge'],config['p1_minDiff'])
	(originRect,filteredAlpha,moveMask,moving_objects) = objs
	# cv2.imshow('OnCapture - originRect',originRect)
	# cv2.imshow('OnCapture - moveMask',moveMask)
	if config['p1_demo']:
		cv2.imshow('p1 color',cv2.hconcat([originRect,filteredAlpha]))
		cv2.imshow('p1 gray',cv2.hconcat([moveMask]))

	if config['p1_debug_var']: func_any.log('P1.IsMoving('+str(len(moving_objects))+')')
	return len(moving_objects) > 0

def process(var):
	config['process']=1
	var['com'] = func_denoise.GaussianBlur(var['frame'])

	if config['p1_debug_flow']:
		print('P1.process')
	# (Process 1) # Step 2 - compare between background and current capture ( main python app.py )
	# (Process 1) # Step 3 - process the background buffer ( current python t1.py )
	if var['pre_bg'] is not None:

		

		var['is_moving'] = IsMoving(var)
		if var['is_moving']:
			if config['p1_debug_flow']: func_any.log('P1.IsMoving()')
	var['pre_bg'] = var['com']
	