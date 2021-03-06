import cv2
import sys
sys.path.insert(1, '../src')
# sys.path.insert(1, '../compiled')

app_name = sys.argv[0].replace('.py','')
global config
config = {}

# p all
config['debug_main']=False
config['debug_flow']=False

config['debug_video']=False

config['db']={
	'host':'127.0.0.1',
	# 'host':'127.0.0.1:3306',
	'user':'root',
	'password':'',
	'database':'ai'
}
# config['db'] = None

config['socket']={
	'ip':'127.0.0.1',
	'port':1234
}
config['socket']=None

# p1
config['p1']=True
config['p1_debug_flow']=False
config['p1_debug_var']=False
config['p1_demo']=False

config['p1_minDiff']=30

# p2
config['p2']=True
config['p2_debug_flow']=True
config['p2_debug_var']=False
config['p2_demo']=False

config['p2_minDiff']=10

config['p2_dilate_enlarge']=300

config['backgroundMovementTimeout']=9
config['backgroundPerCapture']=3

config['coorMaxDistan']=200
config['coorMinTotalDistan']=100

# p3
config['p3']=False
config['p3_debug']=False
config['BgMode_MoveCapture']=True

# func_camera
config['isIPCam']=0
config['ip_cam']='rtsp://admin:@192.168.1.197'

# func_video
config['debug_saveVideo']=False

# func_ImgDiff
config['debug_diff']=True
config['minDiff']=30
config['minSame']=config['minDiff']
config['min_pixels']=150 # area / height / weight

# app
config['ignore']=cv2.imread(app_name+'.ignore.png')

config['id_position']=cv2.imread(app_name+'.id_position.png')


# show before license 
config['lc1']=None

# show license
config['lc2']=None

# config['lc1']='Ivan'
# config['lc2']='Lee'

import app

'''
cd /Users/leekwunfung/Desktop/CPOS/
python3 -m compileall -b ObjExtractor

cd ObjExtractor/bin 
python3 Cam1.py

'''