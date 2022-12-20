import cv2
import numpy as np
from matplotlib import pyplot as plt
import numpy as np
import imutils
import argparse

## Kiko o programa está com argumentos, ou seja, to run: python target_points.py --image "nome do ficheiro"
# O default está com test_draw_1.png

argparser = argparse.ArgumentParser()
argparser.add_argument("--image", type=str, default="test_draw_1.png")
args = vars(argparser.parse_args())

# load the image and display it
image = cv2.imread(args["image"])
#cv2.imwrite("TESTE_IMAGE.png", image)

# convert the image to grayscale and threshold it
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)[1]
#cv2.imwrite("TESTE_THRESH.png", thresh)

# find the largest contour in the threshold image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
c = max(cnts, key=cv2.contourArea)


# draw the shape of the contour on the output image, compute the
# bounding box, and display the number of points in the contour
output = image.copy()
cv2.drawContours(output, [c], -1, (0, 255, 0), 3)
#cv2.imwrite("TESTE_ORIGINAL_CONTOUR.png", output)

# test to various nº of target points (approx variable)
for eps in np.linspace(0.0001, 0.001, 5):
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, eps * peri, True)
    # draw the approximated contour on the image
    output = image.copy()
    cv2.drawContours(output, [approx], -1, (0, 255, 0), 3)
    text = "eps={:.4f}, num_pts={}".format(eps, len(approx))
    # show the approximated contour image
    print("[INFO] {}".format(text))
    #cv2.imwrite("{}.png".format(text), output)
    
    
# best result
best_eps = 0.0003 
peri = cv2.arcLength(c, True)
approx = cv2.approxPolyDP(c, best_eps * peri, True)
output = image.copy()
cv2.drawContours(output, [approx], -1, (0, 255, 0), 3)
text = "eps={:.4f}, num_pts={}".format(eps, len(approx))
#cv2.imwrite("Best Result{}.png".format(text), output)

target_points = approx # defining target_points variable

# x,y target points to pixels
y, x = target_points.T
plt.scatter(x,y)
plt.xlim(0,image.shape[0])
plt.ylim(0,image.shape[1])
plt.title("Target points in pixels")
plt.show()

# x,y target points to centimeters (cm)
y, x = target_points.T
y = y*0.0264583333
x = x*0.0264583333
plt.scatter(x,y)
plt.xlim(0,image.shape[0]*0.0264583333)
plt.ylim(0,image.shape[1]*0.0264583333)
plt.title("Target points in centimeters (cm)")
plt.show()

# x,y target points according to a 25x25 cm square
y, x = target_points.T
maximum = max(image.shape[0], image.shape[1])
k = 25/maximum
y = y*k
x = x*k
plt.scatter(x,y)
plt.xlim(0,25)
plt.ylim(0,25)
plt.title("Target points in cm according to a 25x25 cm square")
plt.show()

