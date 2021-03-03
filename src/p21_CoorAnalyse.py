import cv2
import math
import func_any

import sys
py_name = sys.argv[0]
app_name = py_name.replace('.pyc','').replace('.py','')
exec('import '+app_name)
exec('config = '+app_name+'.config')

import func_colorArea

import json
# history var['movingCoor'] {
# 	ID { lostTime('lt'):0 , records('r'):[{ centerCoor:(x,y) },{ centerCoor (x,y), dis, dir },...], lastCenter('lc'):(x,y) },
# 	...
# }

totalMoveDebug = True
wholeMoveDebug = False

def OnObjectAppear(var,movingData,ID):
	if wholeMoveDebug:
		print('OnObjectAppear ',json.dumps(movingData, indent=4, sort_keys=True))
	pass

def OnObjectMoving(var,movingData,ID):
	if wholeMoveDebug:
		print('OnObjectMoving ',json.dumps(movingData, indent=4, sort_keys=True))
	pass

def OnObjectDisappearTimeout(var,movingData,ID):
	if wholeMoveDebug:
		print('OnObjectDisappearTimeout ',json.dumps(movingData, indent=4, sort_keys=True))
	pass

def OnObjectDisappear(var,movingData,ID):

	if wholeMoveDebug:
		print('OnObjectDisappear ',json.dumps(movingData, indent=4, sort_keys=True))

	if totalMoveDebug:
		begin = movingData['r'][0][0]
		last = movingData['lc']
		totalDir = getDirectionDes(getDirection(begin,last))
		totalDis = distanCoor(begin,last)

		froArea = func_colorArea.isPointInArea(var,begin)
		toArea = func_colorArea.isPointInArea(var,last)
		if totalDis>config['coorMinTotalDistan']:
			print('OnObjectDisappear:',json.dumps(movingData, indent=4, sort_keys=True),totalDir,totalDis)
			print('OnObjectDisappear Area:',' from: ',froArea,' to: ',toArea)

def distanCoor(p1,p2):
	(x1,y1)=p1
	(x2,y2)=p2
	distance = math.sqrt( ((x2-x1)**2)+((y2-y1)**2) )
	return distance

def getDirectionDes(des):

	if des=='0':return 'stay'

	if des=='10':return 'left'
	if des=='20':return 'right'
	if des=='03':return 'up'
	if des=='04':return 'down'

	if des=='13':return 'left-up'
	if des=='14':return 'left-down'
	if des=='23':return 'right-up'
	if des=='24': return 'right-down'

def getDirection(fro,to):

	(x1,y1)=fro
	(x2,y2)=to

	di = None
	if x2>x1:
		di = '2'
	elif x2<x1:
		di = '1'
	else:
		di = '0'

	if y2>y1:
		di += '4'
	elif y2<y1:
		di += '3'
	else:
		di += '0'

	return di

# history {
# 	ID { lostTime('lt'):0 , records('r'):[{ centerCoor:(x,y) },{ centerCoor (x,y), dis, dir },...], lastCenter('lc'):(x,y) },
# 	...
# }
def getHistoryIDByNewCenter(var,centerCoor):
	nearestCenter = None
	nearestDistance = None
	nearestDirect = None
	nearestID = None
	for ID in list(var['movingCoor'].keys()):
		ele = var['movingCoor'][ID]
		centerCur = ele['lc']
		distance = distanCoor(centerCur,centerCoor)
		if distance<=config['coorMaxDistan']:
			dirCode = getDirection(centerCur,centerCoor)
			direct = getDirectionDes(dirCode)
			if nearestDistance is None:
				nearestDistance = distance
				nearestCenter = centerCur
				nearestDirect = direct
				nearestID = ID
			elif distance<nearestDistance:
				nearestID = ID
				nearestCenter = centerCur
				nearestDistance = distance
				nearestDirect = direct
	if nearestID is None:
		return None
	return (nearestID,nearestCenter,nearestDistance,nearestDirect)
	# new_id=func_any.dts()

def processNewCenter(var,centerCoor):
	obj = getHistoryIDByNewCenter(var,centerCoor)
	if obj is None:
		new_id=func_any.dts()
		var['movingCoor'][new_id] = {
			'lt':0,
			'r':[(centerCoor,0,0)],
			'lc':centerCoor
		}
		OnObjectAppear(var,var['movingCoor'][new_id],new_id)
		return (True,new_id)
	else:
		(nearestID,nearestCenter,nearestDistance,nearestDirect) = obj
		var['movingCoor'][nearestID]['lt']=0
		var['movingCoor'][nearestID]['r'].append((centerCoor,nearestDistance,nearestDirect))
		var['movingCoor'][nearestID]['lc']=centerCoor
		OnObjectMoving(var,var['movingCoor'][nearestID],nearestID)
		return (False,nearestID)

def XYWH2Center(xywhi):
	(x,y,w,h,img) = xywhi
	return ( (x+(w/2)) , (y+(h/2)) )

def getCurrentMovingIDs(var,objs_coor):
	moveIDs = []
	for xywhi in objs_coor:
		centerCoor = XYWH2Center(xywhi)
		(isNew, ID) = processNewCenter(var,centerCoor)
		if not isNew:
			moveIDs.append(ID)
	return moveIDs
	

def processLostCenter(var,moveIDs):
	historyIDs = list(var['movingCoor'].keys())
	for ID in historyIDs:
		if ID not in moveIDs:
			if var['movingCoor'][ID]['lt']<3:
				var['movingCoor'][ID]['lt']+=1
				OnObjectDisappearTimeout(var,var['movingCoor'][ID],ID)
			else:
				OnObjectDisappear(var,var['movingCoor'][ID],ID)
				var['movingCoor'].pop(ID,None)

def drawDemo(var):
	demoImage = None
	if var['movingCoor'] is not None:
		historyIDs = list(var['movingCoor'].keys())
		for ID in historyIDs:
			records = var['movingCoor'][ID]['r']
			for recordIndex in range(1,len(records)):
				fro = records[recordIndex-1][0]
				to = records[recordIndex][0]
				print(fro,to)
				(frox,froy) = fro
				(tox,toy) = to
				fro = (int(frox),int(froy))
				to = (int(tox),int(toy))
				print(fro, to)
				demoImage = cv2.line((var['frame'] if demoImage is None else demoImage), fro, to, (0, 255, 0), thickness = 3)
	if demoImage is not None:
		cv2.imshow('CoorAnalyse:', demoImage)
	pass

def processNewCentersFroFrame(var,objs_coor):
	moveIDs = getCurrentMovingIDs(var,objs_coor)
	processLostCenter(var,moveIDs)
	drawDemo(var)
	return var['movingCoor']
	# 	pass

# history var['movingCoor'] {
# 	ID { 
# 		lostTime('lt'):0 , 
# 		records('r'):[{ centerCoor:(x,y) },{ centerCoor (x,y), dis, dir },...], 
# 		lastCenter('lc'):(x,y) 
# 	},
# 	...
# }
def run(var,objs_coor):
	return processNewCentersFroFrame(var,objs_coor)















# def coors2DisNDir(before,after):
# 	dirsDat = []
# 	if len(before)==0 or len(after)==0:
# 		return dirsDat

# 	relation_id=0
# 	for b in before:
# 		# minDistan = None
# 		# last_a = None

# 		# last_ID = None
# 		for a in after:
# 			distance = distanCoor(b,a)
# 			dirCode = getDirection(b,a)
# 			des = getDirectionDes(dirCode)
# 			dirsDat.append((str(relation_id),b,a,distance,des))
# 			relation_id+=1
# 	# return all combination of the center point (with distance and direction)
# 	return dirsDat



# def coorLostHandle(var,ID):
# 	if ID not in var['last_centerCoors']:
# 		if ID not in var['movingCoor_lostTime'] or var['movingCoor_lostTime'][ID] is None:
# 			var['movingCoor_lostTime'][ID] = 1
# 			print('Found ',ID,' object')
# 		else:
# 			var['movingCoor_lostTime'][ID] += 1
# 		print('Lost ',ID,var['movingCoor_lostTime'][ID],' time(s)')
# 		if var['movingCoor_lostTime'][ID]>=3:
# 			if var['movingCoor'].pop(ID,None) is None: print('Error remove coor')
# 			if var['movingCoor_lostTime'].pop(ID,None) is None: print('Error remove coor time out')
# 			print('Lost ',ID,' already')
			
			

# def skipLostMovObj(var):
# 	keys = list(var['movingCoor'].keys())
# 	print('movingCoor 1 ',keys)
# 	for ID in keys:
# 		coorLostHandle(var,ID)

# # input 
# # coor [(x,y,w,h,img)]

# # output 
# # center coor [(x,y)]

# def coors2Centers(objs_coor):
# 	centerCoors = []
# 	i=0
# 	for (x, y, w, h, obj_img) in objs_coor:
# 		center = ( (x+(w/2)) , (y+(h/2)) )
# 		centerCoors.append(center)
# 		cv2.imshow('Object '+str(i),obj_img)
# 		# func_video.WriteVideo2(var,obj_img,'ObjectVideo')
# 		i+=1
# 	return centerCoors

# def append2History(dirsDat,var):

# 	for ID in dirsDat:
# 		(fro,to,descript) = dirsDat[ID]
# 		if ID not in var['movingCoor']:
# 			var['movingCoor'][ID] = []
# 		var['movingCoor'][ID].append( (fro,to,descript) )

# def dataLabeling(var,dirsDat):
# 	for (relation_id,b,a,distance,des) in dirsDat:
		
# 		if minDistan is None:
# 			minDistan = distance
# 			last_a = a
# 			# last_ID = ID
# 		elif distance<minDistan:
# 			minDistan = distance
# 			last_a = a
# 			# last_ID = ID
# 		if minDistan<=config['coorMaxDistan']:
# 			print('Something move ',des,dirCode)
# 			dirsDat.append((b,last_a,des))
# 			print('Same Obj appeared from ',minDistan,' distance')
# 		else:
# 			new_id=func_any.dts()
# 			dirsDat.append((b,last_a,des))
# 			print('another Obj appeared from ',minDistan,' distance')
			
# 	pass

# # input 
# # coor [(x,y,w,h,img)]

# # output 
# # last frame coor [ID](brfore coor,after coor)
# # history [ID](brfore coor,after coor,distance,direction)

# def objsCoorAna(var,objs_coor):

# 	# input 
# 	# coor [(x,y,w,h,img)]
# 	centerCoors = coors2Centers(objs_coor)
# 	# output 
# 	# center coor [(x,y)]

# 	if var['last_centerCoors'] is not None: # skip first time
# 		skipLostMovObj(var)

# 		# input 
# 		# center coor [(x,y)]
# 		dirsDat = coors2DisNDir(var['last_centerCoors'],centerCoors)
# 		# output 
# 		# all combination of the center point (with distance and direction)
# 		# [(b,a,distance,des)]

# 		append2History(dirsDat,var)
# 		print('movingCoor',var['movingCoor'])
# 		print()

# 	var['last_centerCoors'] = centerCoors
# 	return centerCoors
