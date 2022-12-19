import cv2
import numpy as np
from matplotlib import pyplot as plt
import numpy as np
import random

img = cv2.imread('test_draw_1.png', cv2.IMREAD_UNCHANGED)
print(img.shape)
img_edge = cv2.Canny(img,100,200)

thresh = 100
ret,thresh_img = cv2.threshold(img_edge, thresh, 255, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)

img_contours = np.zeros(img.shape)


i = 1
cv2.drawContours(img_contours, contours[1], -1, (0,255,0), 4)
cv2.imwrite('contornos.png',img_contours)

contours = np.asarray(contours, dtype=object)

print("Number of Contours found = " + str(len(contours)))
print(contours.shape)
print("contornos", contours[i])


## Find the points with the maximum and minimum x and y coordinates
max_idx = np.argmax(contours[2], axis=0)
print(max_idx)
min_idx = np.argmin(contours[2], axis=0)
print(min_idx)

Max = contours[2][max_idx]
max_x = Max[0][0]
max_y = Max[0][1]
Min = contours[2][min_idx]
min_x = Min[0][0]
min_y = Min[0][1]
print("MAX X", max_x)
print("MAX Y", max_y)
print("MIN X", min_x)
print("MIN Y", min_y)


## Corner (best features) Detection

img_corner= cv2.imread('test_draw_1.png')
gray= cv2.cvtColor(img_corner, cv2.COLOR_BGR2GRAY)

corners= cv2.goodFeaturesToTrack(gray, 100, 0.01, 100) #CORNERS

for corner in corners:
    x,y= corner[0]
    x= int(x)
    y= int(y)
    cv2.rectangle(img_corner, (x-10,y-10),(x+10,y+10),(255,0,0),-1)
cv2.imshow("goodFeaturesToTrack Corner Detection", img_corner)
cv2.imwrite("corners_features.png", img_corner)
cv2.waitKey()
cv2.destroyAllWindows()

y, x = corners.T
y1, x1 = max_x.T
y2, x2 = max_y.T
y3, x3 = min_x.T
y4, x4 = min_y.T
plt.scatter(x1,y1)
plt.scatter(x2,y2)
plt.scatter(x3,y3)
plt.scatter(x4,y4)
plt.scatter(x,y)
plt.xlim(0,img.shape[0])
plt.ylim(0,img.shape[1])
plt.show()


# Target points = [corners, max_x, max_y, min_x, min_y]