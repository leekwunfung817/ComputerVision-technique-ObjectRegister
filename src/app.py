
'''
cd /Users/leekwunfung/Desktop/ObjExtractor/src
python -m compileall
python3 app.py


Python version
3.6.4 (v3.6.4:d48ecebad5, Dec 18 2017, 21:07:28) 
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)]
Version info.
sys.version_info(major=3, minor=6, micro=4, releaselevel='final', serial=0)
app_name Cam1

https://www.python.org/downloads/release/python-364/
https://github.com/leekwunfung817/ComputerVision-technique-ObjectRegister

'''
import sys

print("Python version")
print (sys.version)
print("Version info.")
print (sys.version_info)

sys.path.insert(1, '../bin')
py_name = sys.argv[0]
app_name = py_name.replace('.pyc','').replace('.py','')
print('app_name',app_name)
print(sys.argv)
exec('import '+app_name)
exec('config = '+app_name+'.config')

# print(config)



import ProgramThread1BackgroundExtraction
import ProgramThread2MovementCapture
import cv2
import numpy
import datetime
import Debug

# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX 
def WriteVideo(write_object,frame,folder=None,finish=False,capture=True):
	# if finish:
	# 	write_object.release()
	# 	write_object = None
	# 	return write_object
	video_frame = frame.copy()
	dt = str(datetime.datetime.now()) 
	video_frame = cv2.putText(video_frame, dt, (10, 100), font, 1, (0, 0, 255), 4, cv2.LINE_8) 
	if write_object is None:
		(h,w,d)=video_frame.shape
		fp = '../'+folder+"/"+ProgramThread1BackgroundExtraction.dts()+'.mp4'
		if config['debug_saveVideo']:
			Debug.log('Create Video:'+fp+' '+str(video_frame.shape))
		write_object = cv2.VideoWriter(fp, cv2.VideoWriter_fourcc(*'mp4v'), 10.0, (w,h))
	if capture:
		if config['debug_saveVideo']: Debug.log('Captured')
		write_object.write(video_frame)
	if finish:
		if config['debug_saveVideo']: Debug.log('Release')
		write_object.release()
		write_object = None
	return write_object

def WriteVideo2(var,frame,folder):
	if var['lastMovingStage'] is not None:
		videoObjIndex = 'lastMovingMovie'+folder
		if videoObjIndex not in var: var[videoObjIndex] = None
		if config['debug_saveVideo']:
			Debug.log('lastMovingStage:'+var['lastMovingStage'])
		if var['lastMovingStage'] == 'MV':
			var[videoObjIndex] = WriteVideo(var[videoObjIndex],frame,folder)
		elif var['lastMovingStage'] == 'TO':
			var[videoObjIndex] = WriteVideo(var[videoObjIndex],frame,folder,capture=False)
		elif var['lastMovingStage'] == 'MD':
			var[videoObjIndex] = WriteVideo(var[videoObjIndex],frame,folder,finish=True,capture=False)
			var['lastMovingStage'] = None

# (Process 1) immediately callback
def OnCapture(var):
	if config['debug_structure']: Debug.log('P1.OnCapture')
	background=var['pre_bg']
	frame=var['frame']
	# print('Received capture:',img)
	(originRect,filteredAlpha,moveMask,moving_objects) = ProgramThread2MovementCapture.run(background,frame)
	# cv2.imshow('OnCapture - originRect',originRect)
	# cv2.imshow('OnCapture - moveMask',moveMask)
	if config['debug_main']:
		cv2.imshow('OnCapture',cv2.hconcat([originRect,filteredAlpha]))
		cv2.waitKey(1)

	WriteVideo2(var,frame,'VideoMovement')
	

	return len(moving_objects) > 0

# (Process 2) three layers accumulate callback (stop mode)
def accumulateCapture(var):
	# Debug.log('P2.accumulateCapture')
	background=var['background']
	frame=var['frame']
	(originRect,filteredAlpha,objectMask,moving_objects) = ProgramThread2MovementCapture.run(numpy.array(background),frame)
	# cv2.imshow('accumulateCapture - originRect',originRect)
	# cv2.imshow('accumulateCapture - moveMask',objectMask)
	if config['debug_main']:
		cv2.imshow('accumulateCapture',cv2.hconcat([originRect,filteredAlpha]))
		cv2.waitKey(1)

	WriteVideo2(var,filteredAlpha,'VideoMovement_filteredAlpha')

	return len(moving_objects) > 0

# (Process 3) three layers accumulate callback (moving mode)
def movingCapture(var):
	# Debug.log('P3.movingCapture')
	background=var['movingBackground']
	frame=var['frame']
	# (originRect,filteredAlpha,objectMask,moving_objects) = ProgramThread2MovementCapture.run(numpy.array(background),frame)
	return True




# def main(set_config):
# config = set_config(config)

callbacks = {}
callbacks['OnCapture'] = OnCapture
callbacks['accumulateCapture'] = accumulateCapture
callbacks['movingCapture'] = movingCapture
ProgramThread1BackgroundExtraction.run(callbacks)
pass
