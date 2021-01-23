import cv2

def run(img):
	# print('denoising')
	# img = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)
	img = cv2.GaussianBlur(img, (21, 21), 0)
	# print('denoised')
	return img