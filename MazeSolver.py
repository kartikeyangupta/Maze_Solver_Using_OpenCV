"""
Author : Kartikeyan Gupta
Date : 30-03-2019
"""

#use opencv 3.1.0.1 or bellow 4.0.0.1


#opencv
import cv2
import numpy as np
import image_utils as utils

image = cv2.imread("maze2.png") #input image

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #convering the image into b&w

thresholded_image = utils.adaptive_threshold(gray_image, cv2.THRESH_BINARY_INV)#thresholded helps distinguish in two images
cv2.imshow("Output", utils.image_resize(thresholded_image, height=600))#show the distinguished image
cv2.waitKey()#waits until closed
_, cnts, _ = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)#finds 2 curves or paths 

if len(cnts) != 2:#if more than 2 curves found error is raised
	print len(cnts)
	raise ValueError("Unable to solve maze - Failed at Contour finding!")

solution_image = np.zeros(gray_image.shape, dtype=np.uint8)#this is a numpy array of zeros
cv2.drawContours(solution_image, cnts, 0, (255,255,255),cv2.FILLED)#this will draw the two contours on zero numpy

cv2.imshow("Output", utils.image_resize(solution_image, height=600))#image with contours
cv2.waitKey()#wait until closed

kernel = np.ones((15, 15),  dtype=np.uint8)#numpy matrix of ones 
solution_image = cv2.dilate(solution_image, kernel)#kernel is then used to generate the contours to increase its width
eroded_image = cv2.erode(solution_image, kernel)#eroded image is like soil erotion wherein all the above image is eroded a lot
solution_image = cv2.absdiff(solution_image, eroded_image)#this image is now generated with the green line only

cv2.imshow("Output", utils.image_resize(solution_image, height=600))#this is the image
cv2.waitKey()
#the below block is to simply merge the given image and the image generated play with the b,g,r to change the path colour
b,g,r = cv2.split(image)
b &= ~solution_image
g |= solution_image
r &= ~solution_image

solution_image = cv2.merge([b,g,r]).astype(np.uint8)#merger
cv2.imshow("Output", utils.image_resize(solution_image, height=600))#output
cv2.waitKey()
cv2.destroyAllWindows()
cv2.imwrite("result.jpg", solution_image)#image writen