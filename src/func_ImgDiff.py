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

def isSeemDiff(img1, img2,reverse=False):
	res = cv2.absdiff(img1, img2)

	res = res.astype(np.uint8)
	if reverse:
		res = cv2.bitwise_not(res)
	return res

def ObjectRecting(origin,thresh):
	frame = origin.copy()
	# objs = []

	cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	i=0
	objs_coor = []
	for c in cnts:
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		# objs.append(origin[y:y+h,x:x+w])
		objs_coor.append((x, y, w, h, origin[y:y+h,x:x+w]))
		text = "Occupied"
		i+=1
	return (frame,objs_coor)

# pre-define function
def diffWithBGArray(frame,background, inverse):
	sameMask = None
	grepFrame = func_denoise.toGray(frame)
	# array background 
	for x in background:
		x = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
		if sameMask is None:
			sameMask = isSeemDiff(x, grepFrame, inverse)
		else:
			sameMask = cv2.bitwise_and( sameMask, isSeemDiff(x, grepFrame, inverse) )
	return sameMask

def diffWithBG(frame,background, inverse):
	# background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
	# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	return isSeemDiff(background, frame, inverse)

def autoDiffBG(frame,background, inverse):
	sameMask = None
	if len(background.shape)==4:
		sameMask = diffWithBGArray(frame,background,inverse)
		img=background[0]
	elif len(background.shape)==3:
		sameMask = diffWithBG(frame,background,inverse)
		img=background
	return sameMask,func_denoise.toGray(sameMask)

def filterSimilarframe(com,greyDiffMask,minDiff):
	# filter frame that have not much movement
	max_bri=np.max(greyDiffMask)
	if max_bri<minDiff:
		ret = func_denoise.fillBlack(com)
		gray_ret = cv2.cvtColor(greyDiffMask, cv2.COLOR_BGR2GRAY)
		return gray_ret,ret,gray_ret,False
		# <No movement>
	return None

def diffPixel(bg,com,minDiff,inverseDiff):
	grayCom = cv2.cvtColor(com, cv2.COLOR_BGR2GRAY)

	rgbDiffMask,greyDiffMask = autoDiffBG(com,bg,inverseDiff)
	obj = filterSimilarframe(com,rgbDiffMask,minDiff)
	if obj is not None:
		return obj

	# diff grey to white black
	greyDiffMask = func_denoise.Binarization(greyDiffMask,minDiff)
	
	# fill in color for moving area
	colorMask = cv2.bitwise_and(grayCom, greyDiffMask)
	
	return colorMask,rgbDiffMask,greyDiffMask,True

def MovObjAnalyse(com,diff,enlargeSize):
	# cv2.imshow('bb',diff)
	diff = func_denoise.Filtering(diff)
	diff = func_denoise.BiggerPixels(diff,enlargeSize)
	# cv2.imshow('bb',diff)
	

	originRect,objs_coor = ObjectRecting(com,diff)
	filteredAlpha = cv2.bitwise_and(com, com, mask=diff)
	return (originRect,filteredAlpha,diff,objs_coor)

def compareForMovementData(background,frame,com,enlargeSize,movementMinimum):
	mask=[]
	move_areas,rgb_diff,diff,is_moving = diffPixel(background,com,movementMinimum,False)


	# if config['debug_diff']: 
	# 	cv2.imshow('compare from',x)
	# 	cv2.imshow('compare to',frame)
	
	

	if is_moving:
		(originRect,filteredAlpha,diff,objs_coor) = MovObjAnalyse(com,diff,enlargeSize)
		return (originRect,filteredAlpha,diff,objs_coor)
	else:
		# is not moving
		black_img=func_denoise.fillBlack(frame)
		return (frame,black_img,cv2.cvtColor(black_img,cv2.COLOR_RGB2GRAY),[])

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


