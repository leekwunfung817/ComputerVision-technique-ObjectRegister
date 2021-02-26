import cv2
import sys
py_name = sys.argv[0]
app_name = py_name.replace('.pyc','').replace('.py','')
exec('import '+app_name)
exec('config = '+app_name+'.config')

import func_ImgDiff
import func_any
import time
# (Process 3) three layers accumulate callback (moving mode)
def movingCapture(var):
	# Debug.log('P3.movingCapture')
	background=var['movingBackground']
	frame=var['frame']
	# (originRect,filteredAlpha,objectMask,moving_objects) = func_ImgDiff.run(numpy.array(background),frame)
	return True


def movingBackgroundCapturing(var):
	frame=var['frame']
	var['fl'] = func_any.fold2FileList('../ImageMoveBackground')
	var['fll'] = len(var['fl'])

	if var['lastMvBg'] is None:
		var['lastMvBg'] = time.time()
		pass
	var['dur'] = (time.time() - var['lastMvBg'])
	if var['fll']<=3:
		if var['dur'] > 30:
			appendMvBg(frame)
	elif var['fll']<=10:
		if var['dur'] > 1800:
			appendMvBg(frame)
	else:
		if var['dur'] > 3600:
			appendMvBg(frame)
	return True

def process(var):
	frame=var['frame']
	if config['debug_flow']:print('p3_MvCapture 1')
	if 'p3_fgbg' not in var:
		if config['debug_flow']:print('p3_MvCapture 1.2')
		var['p3_fgbg'] = cv2.BackgroundSubtractorMOG2()

	print(var['p3_fgbg'])
	if config['debug_flow']:print('p3_MvCapture 2')
	fgmask = var['p3_fgbg'].apply(frame)
	if config['p3_debug']:
		if config['debug_flow']:print('p3_MvCapture 2.2')
		cv2.imshow('p3 fgmask', fgmask)
		cv2.waitKey(1)

	if config['debug_flow']:
		print('p3_MvCapture 3')
	# (Process 3) # Step 2 - compare between background and current capture ( main python app.py )
	if config['BgMode_MoveCapture']:
		if len(var['movingBackground'])>=3:
			var['had_stop'] = movingCapture(var)

	if config['debug_flow']:
		print('p3_MvCapture 4')
	# (Process 3) # Step 3 - process the background buffer ( current python t1.py )
	if config['BgMode_MoveCapture']:
		succeed = movingBackgroundCapturing(var)
