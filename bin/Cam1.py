import cv2
import sys
sys.path.insert(1, '../src')
app_name = sys.argv[0].replace('.py','')
global config
config = {}
config['backgroundMovementTimeout']=3
config['backgroundPerCapture']=3

config['isIPCam']=0
config['ip_cam']='192.168.1.197'

config['debug']=False

config['debug_t1']=True
config['debug_main']=False
config['debug_saveVideo']=False
config['debug_structure']=False
config['debug_diff']=True

config['minDiff']=30
config['min_pixels']=300 # area / height / weight


config['ignore']=cv2.imread(app_name+'.ignore.png')
config['id_position']=cv2.imread(app_name+'.id_position.png')
	# return config
import app
# app.main(set_config)


'''

cd /Users/leekwunfung/Desktop/ObjExtractor/bin
python3 Cam1.py



cd /Users/leekwunfung/Desktop/ObjExtractor_/bin
python3 Cam1.pyc

'''