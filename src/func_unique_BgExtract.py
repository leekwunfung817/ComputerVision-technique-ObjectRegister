
import numpy as np
import cv2
import time
import func_denoise
import func_any
import os

def CapOne():
	cap = cv2.VideoCapture(0)
	ret, frame = cap.read()
	cv2.imwrite('../DiscontinuousCapture/'+func_any.ymdhis()+'.png',frame)
	exit()

def getLastGroupDiscon(last=3, fp=None):
	fl = func_any.fold2FileList(fp)
	fl.sort()
	fl=fl[0:last]
	return fl
# print(fl)

def appendCompond(lis,e1,e2):
	if (e1,e2) not in lis and (e2,e1) not in lis and e2!=e1:
		lis.append( (e1,e2) )
	return lis

def FileLis2ComLis(fl, fp=None):
	lis = []
	for fn1 in fl:
		for fn2 in fl:
			fp1 = fp+fn1
			fp2 = fp+fn2
			lis = appendCompond(lis,fp1,fp2)
	return lis

def isSeemDiff(img1, img2,reverse=False):
	res = cv2.absdiff(img1, img2)

	res = res.astype(np.uint8)
	if reverse:
		cv2.bitwise_not(res)
	return res

def ExtractBgFrom2Img(img1,img2,i=1):
	finalBg = img1
	bg = img2
	detectedBlack = cv2.inRange( finalBg, np.array([0,0,0]), np.array([0,0,0]) )
	

	remainRGB = cv2.bitwise_and( bg, func_denoise.toRGB(detectedBlack) )

	combined = cv2.bitwise_or( remainRGB, finalBg )
	finalBg = combined
	print('Hi')
	cv2.imwrite('demo_'+str(i)+'_'+'A'+'_'+'detectedBlack'+'.png',detectedBlack)
	cv2.imwrite('demo_'+str(i)+'_'+'B'+'_'+'remainRGB'+'.png',remainRGB)
	cv2.imwrite('demo_'+str(i)+'_'+'C'+'_'+'finalBg'+'.png',finalBg)
	cv2.imwrite('demo_'+str(i)+'_'+'D'+'_'+'combined'+'.png',combined)
	cv2.imwrite('demo_'+str(i)+'_'+'E'+'_'+'finalBg'+'.png',finalBg)
	return finalBg

# def ImgArrToBg(lis,last=2):

def ExtractBgFromImgFolder(fp,last=2):
	fl=getLastGroupDiscon(last,fp)
	print(fl)
	lis=FileLis2ComLis(fl,fp)
	list_pair = []

	for (e1,e2) in lis:
		img1 = cv2.imread(e1)
		img2 = cv2.imread(e2)
		dif = isSeemDiff(img1, img2)
		dif = func_denoise.toGray(dif)
		dif = func_denoise.Binarization(mask=dif,min_brightness=10)
		dif = func_denoise.Filtering(dif)
		dif = cv2.bitwise_not(dif)
		bg = cv2.bitwise_and(img1,func_denoise.toRGB(dif))
		list_pair.append( ( os.path.basename(e1) , os.path.basename(e2), img1, img2, bg, dif) )
	bgs=[]
	i = 0
	finalBg = None
	lastDif = None
	# print(len(list_pair))
	for ( e1 , e2, e1_img, e2_img , bg , dif) in list_pair:

		if finalBg is None:
			print('p1')
			finalBg = bg
		else:
			print('p2')
			if lastDif is not None:
				print('p3')
				finalBg=ExtractBgFrom2Img(finalBg,bg,i)
		lastDif = dif
		i+=1
	return finalBg

if __name__ == '__main__':
	# CapOne()
	bg = ExtractBgFromImgFolder(fp = '../DiscontinuousCapture/',last=9)
