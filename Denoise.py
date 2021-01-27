import cv2

def fillBlack(img,reference=None):
	ret = None
	if img is None:
		ret = reference.copy()
	else:
		ret = img.copy()
	(h,w,d)=ret.shape
	cv2.rectangle(ret, (0,0), (w, h), (0, 0, 0), -1)
	return ret

def run(img):
	# print('denoising')
	# img = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)
	img = cv2.GaussianBlur(img, (21, 21), 0)
	# print('denoised')
	return img