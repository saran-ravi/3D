﻿# Package importation
import numpy as np
import cv2
from sklearn.preprocessing import normalize
from matplotlib import pyplot as plt
# Filtering
kernel= np.ones((3,3),np.uint8) # 3x3 matrix values ranges from 0 - 255


#******************************************* 
#***** Parameters for the StereoVision *****
#*******************************************

# Create StereoSGBM and prepare all parameters
window_size = 5
min_disp = 2
num_disp = 130-min_disp
stereo = cv2.StereoSGBM_create(minDisparity = min_disp,
    numDisparities = num_disp,
    blockSize = window_size,
    uniquenessRatio = 10,
    speckleWindowSize = 100,
    speckleRange = 32,
    disp12MaxDiff = 5,
    P1 = 8*3*window_size**2,
    P2 = 32*3*window_size**2)

# Used for the filtered image
stereoR=cv2.ximgproc.createRightMatcher(stereo) # Create another stereo for right this time

# WLS FILTER Parameters
lmbda = 80000
sigma = 1.8
visual_multiplier = 1.0
 
wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=stereo)
wls_filter.setLambda(lmbda)
wls_filter.setSigmaColor(sigma)

#*************************************
#***** Starting the StereoVision *****
#*************************************

# Call the two cameras


# Start Reading Camera images
grayR= cv2.imread('right4_undist.png',0)
grayL= cv2.imread('left4_undist.png',0)
cv2.imshow('original',grayL)

### Rectify the images on rotation and alignement
##Left_nice= cv2.remap(frameL,Left_Stereo_Map[0],Left_Stereo_Map[1], cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)  # Rectify the image using the kalibration parameters founds during the initialisation
##Right_nice= cv2.remap(frameR,Right_Stereo_Map[0],Right_Stereo_Map[1], cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
##
####    # Draw Red lines
####    for line in range(0, int(Right_nice.shape[0]/20)): # Draw the Lines on the images Then numer of line is defines by the image Size/20
####        Left_nice[line*20,:]= (0,0,255)
####        Right_nice[line*20,:]= (0,0,255)
####
####    for line in range(0, int(frameR.shape[0]/20)): # Draw the Lines on the images Then numer of line is defines by the image Size/20
####        frameL[line*20,:]= (0,255,0)
####        frameR[line*20,:]= (0,255,0)    
##        
### Show the Undistorted images
###cv2.imshow('Both Images', np.hstack([Left_nice, Right_nice]))
###cv2.imshow('Normal', np.hstack([frameL, frameR]))
##
### Convert from color(BGR) to gray
##grayR= cv2.cvtColor(Right_nice,cv2.COLOR_BGR2GRAY)
##grayL= cv2.cvtColor(Left_nice,cv2.COLOR_BGR2GRAY)

# Compute the 2 images for the Depth_image
disp= stereo.compute(grayL,grayR)#.astype(np.float32)/ 16
dispL= disp
dispR= stereoR.compute(grayR,grayL)
dispL= np.int16(dispL)
dispR= np.int16(dispR)
print (disp)

# Using the WLS filter
filteredImg= wls_filter.filter(dispL,grayL,None,dispR)
filteredImg = cv2.normalize(src=filteredImg, dst=filteredImg, beta=0, alpha=255, norm_type=cv2.NORM_MINMAX);
filteredImg = np.uint8(filteredImg)
cv2.imshow('Disparity Map', filteredImg)
disp= ((disp.astype(np.float32)/ 16)-min_disp)/num_disp # Calculation allowing us to have 0 for the most distant object able to detect

##    # Resize the image for faster executions
##    dispR= cv2.resize(disp,None,fx=0.7, fy=0.7, interpolation = cv2.INTER_AREA)

# Filtering the Results with a closing filter
closing= cv2.morphologyEx(disp,cv2.MORPH_CLOSE, kernel) # Apply an morphological filter for closing little "black" holes in the picture(Remove noise) 

# Colors map
dispc= (closing-closing.min())*255
dispC= dispc.astype(np.uint8)                                   # Convert the type of the matrix from float32 to uint8, this way you can show the results with the function cv2.imshow()
#cv2.imshow('Map', dispC)
disp_Color= cv2.applyColorMap(dispC,cv2.COLORMAP_OCEAN)         # Change the Color of the Picture into an Ocean Color_Map
filt_Color= cv2.applyColorMap(filteredImg,cv2.COLORMAP_OCEAN) 

# Show the result for the Depth_image
#cv2.imshow('Disparity', disp)
#cv2.imshow('Closing',closing)
#cv2.imshow('Color Depth',disp_Color)


##plt.imshow(filt_Color, 'jet')
##plt.show()
cv2.imshow('Filtered Color Depth',filt_Color)



cv2.waitKey(0)
cv2.destroyAllWindows()
