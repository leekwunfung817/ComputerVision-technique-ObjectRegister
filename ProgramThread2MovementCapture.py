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

# import app
debug = False

def ThreeAlsoDiff(three_img,com):
	buf=None
	for i in three_img:
		img=three_img[i]
		# img = cv2.GaussianBlur(img, (21, 21), 0)
		# print(img.shape)
		# cv2.imshow('image',img)
		diff = cv2.absdiff(img, com)
		if debug:
			cv2.imwrite('a_'+str(i)+'.jpg',diff)
		diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
		if debug:
			cv2.imwrite('aa_'+str(i)+'.jpg',diff)
		thresh_val,thresh = cv2.threshold(diff,np.average(diff),255,cv2.THRESH_BINARY)
		if debug:
			cv2.imwrite('b_'+str(i)+'.jpg',thresh)
		if buf is None:
			buf=thresh
		else:
			buf = cv2.bitwise_and(buf, thresh)
	if debug:
		cv2.imwrite('bitwise_and.jpg',buf)
	return buf

def Filtering(origin,thresh):
	frame = origin.copy()
	cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	for c in cnts:
		# if the contour is too small
		if cv2.contourArea(c) < 500:
			# draw too small object to image
			cv2.drawContours(thresh, [c], -1, (0,0,0), -1)
			continue
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Occupied"
	# if debug:
	# 	cv2.imwrite('e_'+str(i)+'.jpg',frame)
	# if debug:
	# 	cv2.imwrite('f_'+str(i)+'.jpg',thresh)
	return (thresh,frame)

def BiggerPixels(thresh):
	# pixels make bigger
	thresh = cv2.dilate(thresh, None, iterations=15)

	# if debug: 
	# 	cv2.imwrite('g_'+str(i)+'.jpg',thresh)
	return thresh
	
def run(arr,com):
	move_areas = ThreeAlsoDiff(arr,com.copy())
	if debug:
		cv2.imwrite('move_areas.jpg',move_areas)

	(moveMask,originRect) = Filtering(com,move_areas)
	# cv2.imwrite('filteredAlpha_1.jpg',cv2.bitwise_or(com, com, mask=moveMask))

	moveMask = BiggerPixels(moveMask)
	if debug:
		cv2.imwrite('moveMask.jpg',moveMask)
	# if debug:
	cv2.imwrite('originRect.jpg',originRect)

	
	filteredAlpha = cv2.bitwise_or(com, com, mask=moveMask)
	# if debug: 
	cv2.imwrite('filteredAlpha.jpg',filteredAlpha)
	# return (move_areas,moveMask,originRect,filteredAlpha)
	return (originRect,filteredAlpha)
