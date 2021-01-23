
'''
cd /Users/leekwunfung/Desktop/ObjExtractor/
python3 app.py

'''

import ProgramThread1BackgroundExtraction
import ProgramThread2MovementCapture
import cv2


def OnCapture(arr,com,frame):
	# print('Received capture:',frame.shape)
	(originRect,filteredAlpha,moving_objects) = ProgramThread2MovementCapture.run(arr,frame)

	# cv2.imshow('originRect', originRect)
	# cv2.imshow('filteredAlpha', filteredAlpha)
	# cv2.waitKey(1)

	return len(moving_objects) > 0



if __name__ == "__main__":
	ProgramThread1BackgroundExtraction.run(OnCapture)
	pass
