import cv2
import sys
sys.path.insert(1, '../src')
app_name = sys.argv[0].replace('.py','')
global config
config = {}

# p all
config['debug_main']=False
config['debug_flow']=False

config['debug_video']=False

# p1
config['p1']=True
config['p1_debug_flow']=False
config['p1_debug_var']=False
config['p1_demo']=False

config['p1_minDiff']=30

# p2
config['p2']=True
config['p2_debug_flow']=False
config['p2_debug_var']=False
config['p2_demo']=True

config['p2_minDiff']=15

config['p2_dilate_enlarge']=300

config['backgroundMovementTimeout']=3
config['backgroundPerCapture']=3

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

import app

'''

cd /Users/leekwunfung/Desktop/CPOS/ObjExtractor/bin 
python3 Cam1.py

cd /Users/leekwunfung/Desktop/ObjExtractor_/bin
python3 Cam1.pyc

'''