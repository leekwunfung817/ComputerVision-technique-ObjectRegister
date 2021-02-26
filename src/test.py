'''

cd /Users/leekwunfung/Desktop/CPOS/ObjExtractor/src
python3 test.py


'''
# Test ignore principle
# import cv2
# a = cv2.imread('curDemo.png')
# # ignore = cv2.cvtColor(cv2.imread('ignore.icfg.png'),cv2.COLOR_RGB2GRAY)
# ignore = cv2.imread('ignore.icfg.png')
# print(a.shape,ignore.shape)
# b = cv2.bitwise_and(a,ignore)
# # cv2.imshow('ignore', ignore)
# cv2.imwrite('test.png', b)
# # cv2.waitKey(0)

# Test brightness addition
# import numpy
# arr = numpy.array([[10,20,30],[10,20,30]]) + numpy.array([[3,2,1],[1,2,3]])
# print(arr)

import cv2
import time
import func_denoise
import func_any

import func_unique_BgExtract

# print(func_unique_BgExtract)
bg = func_unique_BgExtract.ExtractBgFromImgFolder(fp = '../DiscontinuousCapture/', last=9)

# cv2.imwrite('../DiscontinuousBG/'+func_any.ymdhis()+'.png',frame)
exit()


var = {}
var['p3_fgbg'] = cv2.createBackgroundSubtractorMOG2(history = 500,varThreshold = 16, detectShadows = False)

cap = cv2.VideoCapture(0)
while(1):
	
	ret, frame = cap.read()
	cv2.imwrite('../StaticCapture/'+func_any.ymdhis()+'.png',frame)
	
	fgmask = var['p3_fgbg'].apply(frame)
	fgmask = func_denoise.GroupDiff(fgmask)
	cv2.imshow('frame',fgmask)
	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break
	time.sleep(3)

cap.release()
cv2.destroyAllWindows()
