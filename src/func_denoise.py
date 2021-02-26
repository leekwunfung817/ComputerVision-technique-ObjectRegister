import cv2
import imutils
import numpy as np

def toGray(mask):
	return cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

def toRGB(mask):
	return cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

# for gray
def Binarization(mask,min_brightness=None,max_brightness=255):
	if min_brightness is None:
		min_brightness = np.average(mask)
	thresh_val,mask = cv2.threshold(mask,min_brightness,255,cv2.THRESH_BINARY)
	return mask

# ignore all things, just fill whole image black
def fillBlack(img,reference=None):
	ret = None
	if img is None:
		ret = reference.copy()
	else:
		ret = img.copy()
	(h,w,d)=ret.shape
	cv2.rectangle(ret, (0,0), (w, h), (0, 0, 0), -1)
	return ret

# for gray only
kernel = np.ones((17,17),np.uint8)
def Filtering(thresh):
	# pixels make smaller then enlarge
	thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
	return thresh

# def Filtering(thresh,min_pixels):
	# cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	# cnts = imutils.grab_contours(cnts)
	# for c in cnts:
	# 	(x, y, w, h) = cv2.boundingRect(c)
	# 	# if the contour is too small
	# 	if cv2.contourArea(c) < min_pixels:
	# 	 # or w < config['min_pixels'] or h < config['min_pixels']:
	# 		# draw too small object to image
	# 		cv2.drawContours(thresh, [c], -1, (0,0,0), -1)
	# 		continue
	# return thresh

# for gray only
def BiggerPixels(thresh, iterations=30):
	# pixels make bigger
	thresh = cv2.dilate(thresh, None, iterations)
	return thresh

# def GroupDiff(thresh,min_pixels):
	# Filtering(thresh,min_pixels)
	# thresh = BiggerPixels(thresh)
	# ,min_pixels

def GroupDiff(thresh):
	thresh = Filtering(thresh)
	return thresh


def GaussianBlur(img):
	# print('denoising')
	# img = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)
	img = cv2.GaussianBlur(img, (21, 21), 0)
	# print('denoised')
	return img
