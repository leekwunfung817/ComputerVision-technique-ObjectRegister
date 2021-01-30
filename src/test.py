'''
cd /Users/leekwunfung/Desktop/ObjExtractor
python3 test.py


'''
# Test ignore principle
# import cv2
# a = cv2.imread('curDemo.png')
# # ignore = cv2.cvtColor(cv2.imread('ignore.icfg.png'),cv2.COLOR_RGB2GRAY)
# ignore = cv2.imread('ignore.icfg.png')
# print(a.shape,ignore.shape)
# b = cv2.bitwise_and(a,ignore)
# # cv2.imshow('ignore', ignore)
# cv2.imwrite('test.png', b)
# # cv2.waitKey(0)

# Test brightness addition
# import numpy
# arr = numpy.array([[10,20,30],[10,20,30]]) + numpy.array([[3,2,1],[1,2,3]])
# print(arr)