import cv2
import numpy as np

img = cv2.imread('test_draw_1.png', cv2.IMREAD_UNCHANGED)

img_edge = cv2.Canny(img,100,200)

thresh = 100
ret,thresh_img = cv2.threshold(img_edge, thresh, 255, cv2.THRESH_BINARY)

#find contours
contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#create an empty image for contours
img_contours = np.zeros(img.shape)

# draw the contours on the empty image
cv2.drawContours(img_contours, contours, -1, (0,255,0), 4)
cv2.imwrite('contornos.png',img_contours) 

contours = np.asarray(contours, dtype=object)
print(contours)
print(contours.shape)
