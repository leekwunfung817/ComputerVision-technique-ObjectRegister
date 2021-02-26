import datetime
import cv2
import func_any

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
		fp = '../'+folder+"/"+func_any.dts()+'.mp4'
		# if config['debug_saveVideo']:
		# 	Debug.log('Create Video:'+fp+' '+str(video_frame.shape))
		write_object = cv2.VideoWriter(fp, cv2.VideoWriter_fourcc(*'mp4v'), 10.0, (w,h))
	if capture:
		# if config['debug_saveVideo']: Debug.log('Captured')
		write_object.write(video_frame)
	if finish:
		# if config['debug_saveVideo']: Debug.log('Release')
		write_object.release()
		write_object = None
	return write_object

def WriteVideo2(var,frame,folder):
	
	# if config['debug_flow']: func_any.log('<func> WriteVideo2')
	
	if var['lastMovingStage'] is not None:
		videoObjIndex = 'lastMovingMovie'+folder
		if videoObjIndex not in var: var[videoObjIndex] = None
		# if config['debug_saveVideo']:
		# 	Debug.log('lastMovingStage:'+var['lastMovingStage'])
		if var['lastMovingStage'] == 'MV':
			var[videoObjIndex] = WriteVideo(var[videoObjIndex],frame,folder)
		elif var['lastMovingStage'] == 'TO':
			var[videoObjIndex] = WriteVideo(var[videoObjIndex],frame,folder,capture=False)
		elif var['lastMovingStage'] == 'MD':
			var[videoObjIndex] = WriteVideo(var[videoObjIndex],frame,folder,finish=True,capture=False)
			var['lastMovingStage'] = None
