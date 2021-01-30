
'''
cd /Users/leekwunfung/Desktop/ObjExtractor/src
python3 app.py

'''
import sys

print("Python version")
print (sys.version)
print("Version info.")
print (sys.version_info)

sys.path.insert(1, '../bin')
py_name = sys.argv[0]
app_name = py_name.replace('.py','')
print('app_name',app_name)
print(sys.argv)
exec('import '+sys.argv[0].replace('.py',''))
exec('config = '+sys.argv[0].replace('.py','')+'.config')

# print(config)



import ProgramThread1BackgroundExtraction
import ProgramThread2MovementCapture
import cv2
import numpy
import datetime
import Debug

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX 
def WriteVideo(write_object,frame,folder=None,finish=False,capture=True):
	video_frame = frame.copy()
	dt = str(datetime.datetime.now()) 
	video_frame = cv2.putText(video_frame, dt, (10, 100), font, 1, (0, 0, 255), 4, cv2.LINE_8) 
	if write_object is None:
		(h,w,d)=video_frame.shape
		write_object = cv2.VideoWriter(folder+"/"+ProgramThread1BackgroundExtraction.dts()+'.mp4', fourcc, 10.0, (w,h))
	if capture:
		write_object.write(video_frame)
	if finish:
		write_object.release()
	return write_object


# (Process 1) immediately callback
def OnCapture(var):
	# Debug.log('P1.OnCapture')
	background=var['pre_bg']
	frame=var['frame']
	# print('Received capture:',img)
	(originRect,filteredAlpha,moveMask,moving_objects) = ProgramThread2MovementCapture.run(background,frame)
	# cv2.imshow('OnCapture - originRect',originRect)
	# cv2.imshow('OnCapture - moveMask',moveMask)
	cv2.imshow('OnCapture',cv2.hconcat([originRect,filteredAlpha]))
	cv2.waitKey(1)


	if var['lastMovingStage'] == 'MV':
		var['lastMovingMovie'] = WriteVideo(var['lastMovingMovie'],frame,'VideoMovement')
	elif var['lastMovingStage'] == 'TO':
		var['lastMovingMovie'] = WriteVideo(var['lastMovingMovie'],frame,'VideoMovement',capture=False)
	elif var['lastMovingStage'] == 'MD':
		var['lastMovingMovie'] = WriteVideo(var['lastMovingMovie'],frame,'VideoMovement',finish=True,capture=False)


	return len(moving_objects) > 0

# (Process 2) three layers accumulate callback (stop mode)
def accumulateCapture(var):
	# Debug.log('P2.accumulateCapture')
	background=var['background']
	frame=var['frame']
	(originRect,filteredAlpha,objectMask,moving_objects) = ProgramThread2MovementCapture.run(numpy.array(background),frame)
	# cv2.imshow('accumulateCapture - originRect',originRect)
	# cv2.imshow('accumulateCapture - moveMask',objectMask)
	cv2.imshow('accumulateCapture',cv2.hconcat([originRect,filteredAlpha]))
	cv2.waitKey(1)


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
