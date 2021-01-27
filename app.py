
'''
cd /Users/leekwunfung/Desktop/ObjExtractor/
python3 app.py

'''

import ProgramThread1BackgroundExtraction
import ProgramThread2MovementCapture
import cv2
import numpy

# immediately callback
def OnCapture(background,frame):
	# print('Received capture:',img)
	(originRect,filteredAlpha,moveMask,moving_objects) = ProgramThread2MovementCapture.run(background,frame)
	cv2.imshow('OnCapture - originRect',originRect)
	cv2.imshow('OnCapture - moveMask',moveMask)
	cv2.waitKey(1)
	return len(moving_objects) > 0

# three layers accumulate callback
def accumulateCapture(background,frame):
	(originRect,filteredAlpha,objectMask,moving_objects) = ProgramThread2MovementCapture.run(numpy.array(background),frame)
	cv2.imshow('accumulateCapture - originRect',originRect)
	cv2.imshow('accumulateCapture - moveMask',objectMask)
	cv2.waitKey(1)
	return len(moving_objects) > 0

if __name__ == "__main__":
	ProgramThread1BackgroundExtraction.run(OnCapture,accumulateCapture)
	pass
