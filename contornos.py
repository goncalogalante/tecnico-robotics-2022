import cv2 as cv
import numpy as np
import serial

# Convert image to xy coordinates equivalent to our 25x25 cm square

# Determine our 25x25 cm square in the lab xyz coordinates

# Find segment defining points in our image

# Write all Python-ACL connections (CON, SPEED)

# Determine the possible points in the lab referential



img = cv.imread('test_draw_1.png', cv.IMREAD_UNCHANGED)

img_edge = cv.Canny(img,100,200)

thresh = 100
ret,thresh_img = cv.threshold(img_edge, thresh, 255, cv.THRESH_BINARY)

#find contours
contours, hierarchy = cv.findContours(thresh_img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

#create an empty image for contours
img_contours = np.zeros(img.shape)

# draw the contours on the empty image
cv.drawContours(img_contours, contours, -1, (0,255,0), 4)
cv.imwrite('contornos.png',img_contours)

contours = np.asarray(contours, dtype=object)
print(contours)
print(contours.shape)
