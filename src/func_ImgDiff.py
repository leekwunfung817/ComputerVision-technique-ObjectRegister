'''
pip install --upgrade opencv-python
pip install --upgrade matplotlib
pip install imutils
pip install --upgrade imutils
cd /Users/leekwunfung/Desktop/ObjExtractor
python3 app.py

'''

import cv2
import numpy as np
import matplotlib.pyplot as plt
from imutils.video import VideoStream
import imutils

import func_denoise

import sys
sys.path.insert(1, '../bin')
appName = sys.argv[0].replace('.py','')
# print(appName)
exec('import '+appName)
exec('config = '+appName+'.config')

def ExtractBackground():
	pass

def isSeemDiff(img1, img2,reverse=False):
	res = cv2.absdiff(img1, img2)

	res = res.astype(np.uint8)
	if reverse:
		res = cv2.bitwise_not(res)
	return res

def AlsoSame(background,frame):
	# print(config)
	rgbFrame = frame.copy()
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	img = None
	sameMask = None

	# array background 
	if len(background.shape)==4:
		for x in background:
			x = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
			if sameMask is None:
				sameMask = isSeemDiff(x, frame, True)
			else:
				sameMask = cv2.bitwise_and( sameMask, isSeemDiff(x, frame, True) )
		img=background[0]


	# background 
	elif len(background.shape)==3:
		background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
		# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		sameMask = isSeemDiff(background, frame, True)
		img=background

	# (h,w,d)=img.shape
	
	# filter frame that have not much same
	max_bri=np.max(sameMask)
	if max_bri<config['minSame']:
		# return black frame
		ret = func_denoise.fillBlack(frame)
		gray_ret = cv2.cvtColor(sameMask, cv2.COLOR_BGR2GRAY)
		return gray_ret,ret,sameMask,False
	
	# diff grey to white black
	sameMask = func_denoise.Binarization(sameMask,config['minSame'])
	# thresh_val,sameMask = cv2.threshold(sameMask,config['minSame'],255,cv2.THRESH_BINARY)

	# fill in color for moving area
	colorMask = cv2.bitwise_and(rgbFrame, sameMask)
	
	return colorMask,sameMask,True


def AlsoDiff(background,frame):
	img = None
	rgbDiffMask = None
	if len(background.shape)==4:
		for x in background:
			if config['debug_diff']: 
				cv2.imshow('compare from',x)
				cv2.imshow('compare to',frame)
				cv2.waitKey(1)
			if rgbDiffMask is None:
				rgbDiffMask = isSeemDiff(x, frame)
			else:
				rgbDiffMask = cv2.bitwise_and( rgbDiffMask , isSeemDiff(x, frame) )
		img=background[0]
		if config['debug_diff']: cv2.imshow('rgbDiffMask',rgbDiffMask);cv2.waitKey(1)
	elif len(background.shape)==3:
		rgbDiffMask = isSeemDiff(background, frame)
		img=background
	(h,w,d)=img.shape

	# filter frame that have not much movement
	max_bri=np.max(rgbDiffMask)
	if max_bri<config['minDiff']:
		ret = func_denoise.fillBlack(frame)
		gray_ret = cv2.cvtColor(rgbDiffMask, cv2.COLOR_BGR2GRAY)
		return gray_ret,ret,gray_ret,False
	
	# diff grey to white black
	greyDiffMask = cv2.cvtColor(rgbDiffMask, cv2.COLOR_BGR2GRAY)
	greyDiffMask = func_denoise.Binarization(greyDiffMask,config['minDiff'])
	# thresh_val,greyDiffMask = cv2.threshold(greyDiffMask,config['minDiff'],255,cv2.THRESH_BINARY)

	# fill in color for moving area
	g_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	colorMask = cv2.bitwise_and(g_frame, greyDiffMask)
	
	return colorMask,rgbDiffMask,greyDiffMask,True

def ObjectRecting(origin,thresh):
	frame = origin.copy()
	objs = []
	cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	i=0
	for c in cnts:
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		objs.append(origin[y:y+h,x:x+w])
		text = "Occupied"
		i+=1
	return (frame,objs)

def run(background,com):
	mask=[]
	move_areas,rgb_diff,diff,is_moving = AlsoDiff(background,com.copy())
	if is_moving:
		diff = func_denoise.Filtering(diff)
		diff = func_denoise.BiggerPixels(diff)
		originRect,objs = ObjectRecting(com,diff)
		filteredAlpha = cv2.bitwise_and(com, com, mask=diff)
		return (originRect,filteredAlpha,diff,objs)
	black_img=func_denoise.fillBlack(com)
	return (com,black_img,cv2.cvtColor(black_img,cv2.COLOR_RGB2GRAY),[])

'''
cd /Users/leekwunfung/Desktop/ObjExtractor
python3 ProgramThread2MovementCapture.py

'''
if __name__ == "__main__":
	(originRect,filteredAlpha,objs) = run(
		func_denoise.GaussianBlur( cv2.imread('1.jpg') ),
		func_denoise.GaussianBlur( cv2.imread('a.jpg') )
	)
	cv2.imwrite('originRect.jpg',originRect)
	cv2.imwrite('filteredAlpha.jpg',filteredAlpha)


