
import ProgramThread2MovementCapture
import cv2

arr = {
	1:cv2.imread('1.jpg'),
	2:cv2.imread('2.jpg'),
	3:cv2.imread('3.jpg')
}

com = cv2.imread('a.jpg')
(originRect,filteredAlpha) = ProgramThread2MovementCapture.run(arr,com)
