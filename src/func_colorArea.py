
# id_position.icfg - define captured area align with car-parking position. (For function 3)
#     1.red
#     2.orange
#     3.yellow
#     4.green
#     5.blue
#     6.purple
#     7.pink
#     8.brown
#     9.black
#     10.white
#     11.gray
import cv2  # Not actually necessary if you just want to create an image.
import numpy as np

colorArr = {
	'gray':(128,128,128),
	'red':(0,0,255),
	'orange':(0,147,255),
	'yellow':(0,255,255),
	'green':(0,255,0),
	'blue':(255,0,0),
	'purple':(254,78,135),
	'pink':(216,138,255),
	'brown':(66,121,170)
}

colorArrIndex = {
	'gray':0,
	'red':1,
	'orange':2,
	'yellow':3,
	'green':4,
	'blue':5,
	'purple':6,
	'pink':7,
	'brown':8
}


def generateDemo():
	height = 300
	width = 300
	for color in colorArr:
		blank_image = np.zeros((height,width,3), np.uint8)
		cv2.rectangle(blank_image, (0,0), (width, height), colorArr[color], -1)
		print('../ColorDemo/'+color,blank_image.shape)
		cv2.imwrite('../ColorDemo/'+color+'.png',blank_image)

def getIndexMasks(id_position):
	arr = {}
	for color in colorArr:
		bgr = colorArr[color]
		mask = cv2.inRange(id_position, bgr, bgr)
		arr[str(colorArrIndex[color])]=mask
	return arr

def isPointInArea(var,point):
	(x,y)=point
	(x,y)=(int(x),int(y))
	for MID in var['IDMasks']:
		mask = var['IDMasks'][MID]
		mColor = mask[y][x]
		if mColor==255:
			return MID
	return -1

# app_name='Cam1'
# id_position = cv2.imread('../bin/'+app_name+'.id_position.png')
# getIndexMasks(id_position)


'''
cd /Users/leekwunfung/Desktop/CPOS/
cd ObjExtractor/src
python3 func_colorArea.py

'''

# red_extract = 
# orange_extract = 
# yellow_extract = 
# green_extract = 
# blue_extract = 
# purple_extract = 
# pink_extract = 
# brown_extract = 
# black_extract = 
# white_extract = 
# gray_extract = 
