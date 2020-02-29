import numpy as np
import cv2
import glob

nffile = np.load('Camera.npz')

mtx = nffile['mtx'] #camera matrix

dist =  nffile['dist'] #
print(mtx,dist)



cap = cv2.VideoCapture(0)
ret,img=cap.read()
input()
cap = cv2.VideoCapture(0)
ret,img1=cap.read()
input()
#img = cv2.imread('l1.jpg')
##img = cv2.resize(img, (640, 480))
##img1 = cv2.imread('r1.jpg')
##img1 = cv2.resize(img1, (640, 480)) 
h,  w = img.shape[:2]
#print(h,w)
cv2.imshow("Original",img)
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
print(roi)
#print(newcameramtx)

mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
dst = cv2.remap(img,mapx,mapy,cv2.INTER_LINEAR)
dst1 = cv2.remap(img1,mapx,mapy,cv2.INTER_LINEAR)
# undistort
dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
dst1 = cv2.undistort(img1, mtx, dist, None, newcameramtx)
# crop the image
x, y, w, h = roi
dst2 = dst[y:y+h, x:x+w]

dst3 = dst1[y:y+h, x:x+w]
#cv2.imwrite('right1.png', dst1)
##cv2.imshow('left1.png', dst2)
##cv2.imshow('right1.png', dst3)
cv2.imshow('left1.png', dst2)
cv2.imshow('right1.png', dst)


cv2.imwrite('left5_undist.png',dst2)
cv2.imwrite('right5_undist.png',dst3)
cv2.waitKey()
cap.release()
cv2.destroyAllWindows()
