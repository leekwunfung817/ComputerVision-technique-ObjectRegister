'''
pip3 install --upgrade opencv-python
pip3 install --upgrade matplotlib
pip3 install imutils
pip3 install --upgrade imutils
cd /Users/leekwunfung/Desktop/ObjExtractor
python3 app.py

'''

import cv2
import numpy as np
import matplotlib.pyplot as plt
from imutils.video import VideoStream
import imutils

import Denoise
import Debug

debug = False
minDiff = 50

def isSeemDiff(img1, img2):
	res = cv2.absdiff(img1, img2)
	res = res.astype(np.uint8)
	return res

def ThreeAlsoDiff(background,frame):
	img = None
	rgbDiffMask = None
	if len(background.shape)==4:
		for x in background:
			if rgbDiffMask is None:
				rgbDiffMask = isSeemDiff(x, frame)
			else:
				rgbDiffMask = rgbDiffMask + isSeemDiff(x, frame)
		img=background[0]
	elif len(background.shape)==3:
		rgbDiffMask = isSeemDiff(background, frame)
		img=background
	(h,w,d)=img.shape
	max_bri=np.max(rgbDiffMask)

	# filter frame that have not much movement
	if max_bri<minDiff:
		ret = Denoise.fillBlack(frame)
		gray_ret = cv2.cvtColor(rgbDiffMask, cv2.COLOR_BGR2GRAY)
		return gray_ret,ret,gray_ret,False
	
	# diff grey to white black
	greyDiffMask = cv2.cvtColor(rgbDiffMask, cv2.COLOR_BGR2GRAY)
	thresh_val,greyDiffMask = cv2.threshold(greyDiffMask,minDiff,255,cv2.THRESH_BINARY)

	# fill in color for moving area
	g_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	colorMask = cv2.bitwise_and(g_frame, greyDiffMask)
	
	return colorMask,rgbDiffMask,greyDiffMask,True

# area / height / weight
min_pixels = 300
def Filtering(thresh):
	cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	for c in cnts:
		(x, y, w, h) = cv2.boundingRect(c)
		# if the contour is too small
		if cv2.contourArea(c) < min_pixels:
		 # or w < min_pixels or h < min_pixels:
			# draw too small object to image
			cv2.drawContours(thresh, [c], -1, (0,0,0), -1)
			continue
	return thresh

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

def BiggerPixels(thresh):
	# pixels make bigger
	thresh = cv2.dilate(thresh, None, iterations=30)
	return thresh
	
def run(background,com):
	debug_1 = False
	mask=[]
	move_areas,rgb_diff,diff,is_moving = ThreeAlsoDiff(background,com.copy())
	if is_moving:
		diff = Filtering(diff)
		diff = BiggerPixels(diff)
		originRect,objs = ObjectRecting(com,diff)
		filteredAlpha = cv2.bitwise_and(com, com, mask=diff)
		return (originRect,filteredAlpha,diff,objs)
	black_img=Denoise.fillBlack(com)
	return (com,black_img,cv2.cvtColor(black_img,cv2.COLOR_RGB2GRAY),[])

'''
cd /Users/leekwunfung/Desktop/ObjExtractor
python3 ProgramThread2MovementCapture.py

'''
if __name__ == "__main__":
	(originRect,filteredAlpha,objs) = run(
		Denoise.run( cv2.imread('1.jpg') ),
		Denoise.run( cv2.imread('a.jpg') )
		)
	cv2.imwrite('originRect.jpg',originRect)
	cv2.imwrite('filteredAlpha.jpg',filteredAlpha)


