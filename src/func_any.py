from os import walk
import datetime
import func_any

def ymdhis():
	return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def log(st):
	print( ymdhis()+'>'+st )

def fold2FileList(mypath):
	f = []
	for (dirpath, dirnames, filenames) in walk(mypath):
		f.extend(filenames)
	return f
def fold2ImgList(mypath):
	f = []
	for (dirpath, dirnames, filenames) in walk(mypath):
		print((dirpath, dirnames, filenames))
		f.extend(filenames)
	return f


def appendMvBg(frame):
	func_any.log('BG count:'+str(var['fll']))
	func_any.log('BG last capture duration:'+str(var['dur']))
	fp = '../ImageMoveBackground/'+func_any.dts()+'.jpg'
	cv2.imwrite(fp,frame)
	var['lastMvBg'] = time.time()

# have used
def dts():
	return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
