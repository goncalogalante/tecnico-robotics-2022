import cv2
import numpy as np
from matplotlib import pyplot as plt
import numpy as np
import imutils

# This function returns the target points
def image_processing(image):
    """This function takes an image as input, finds
    its contours and calculates its
    target points. The return is a 
    vector of points with coordinates (x,y)"""
   
    # load the image and display it
    image = cv2.imread(image)

    # convert the image to grayscale and threshold it
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)[1]
 
    # find the contours of the image
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnts = imutils.grab_contours(cnts)

    # draw the contours finded
    img_contours = np.zeros(image.shape)
    cv2.drawContours(img_contours, cnts, -1, (0,255,0), 1)
    
    # saves the image of the draw containing the contours finded (uncomment the next line)
    # cv2.imwrite('contornos.png',img_contours)
    
    
    # if the image is just composed by one contour:
    if len(cnts) == 1:
        
        # get the draw with the final contour approximation
        for c in cnts:
            epsilon_aux = 0.0003 * cv2.arcLength(c, True)
            approx_aux = cv2.approxPolyDP(c, epsilon_aux,True)
            cv2.drawContours(img_contours, [approx_aux], -1, (0,255,0),3)
           
            # saves the image of the draw containing the contours approximation (uncomment the next line)
            # cv2.imwrite('contornos_approx.png'.format(c), img_contours)

        
        # get the final target points approximation vector
        k = 0.0003
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c,k*peri, True)

        # define the target points vector
        target_points = approx 
        
        # filter the target points in order to prevent duplicated points and backtracking
        counter = 0
        target_points_list = []
        if len(cnts)==1:
            for target_point in target_points:
                # (nº target_points / 2)+ 2 formula
                if counter < (len(target_points)/2)+2:
                    target_points_list.append(target_point)
                    counter += 1

        # convert target point list into a numpy array 
        target_points_list = np.asarray(target_points_list)
        
        """1) Plot the target points in pixels """ # uncomment until plt.show()
        # y, x = target_points_list.T
        # plt.scatter(x,y)
        # plt.xlim(0,image.shape[0])
        # plt.ylim(0,image.shape[1])
        # plt.title("Target points in pixels")
        # plt.show()

        """2) Plot the target points in centimeters """ # uncomment until plt.show()
        # y, x = target_points_list.T
        # y = y*0.0264583333
        # x = x*0.0264583333
        # plt.scatter(x,y)
        # plt.xlim(0,image.shape[0]*0.0264583333)
        # plt.ylim(0,image.shape[1]*0.0264583333)
        # plt.title("Target points in centimeters (cm)")
        # plt.show()

        """Transform the draw according to a 16x16 square"""
        y, x = target_points_list.T
        maximum = max(image.shape[0], image.shape[1])
        k = 1600/maximum
        y = y*k
        x = x*k
        y = np.round(y)
        x = np.round(x)

        # define the list of target points to be returned for the robot.
        pts=[i for i in zip(x[0], y[0])]
      
        return pts

    # if the image is composed by more than one contour (Test Draw 2)
    else:
        # delete the contour vector that is unused
        cnts = np.delete(cnts, 1, 0)

        # joins the two contours into a single vector
        points = [point for contour in cnts for point in contour]
        
        # get the draw with the single vector containing both contours
        img_contours = np.zeros(image.shape)
        cv2.drawContours(img_contours, points, -1, (0,255,0), 4)
        
        # saves the image of the draw containing the single vector defined above (uncomment the next line)
        # cv2.imwrite('contornos_case2.png', img_contours) 
        
        # convert all the points list into a numpy array
        points = np.asarray(points)
        
        # get the final target points approximation vector
        k = 0.0003
        peri = cv2.arcLength(points, True)
        approx = cv2.approxPolyDP(points,k*peri, True)
      
        # define the target points vector
        target_points_list = approx 
        
        """1) Plot the target points in pixels """ # uncomment until plt.show()
        # y, x = target_points_list.T
        # plt.scatter(x,y)
        # plt.xlim(0,image.shape[0])
        # plt.ylim(0,image.shape[1])
        # plt.title("Target points in pixels")
        # plt.show()

        """2) Plot the target points in centimeters """ # uncomment until plt.show()
        # y, x = target_points_list.T
        # y = y*0.0264583333
        # x = x*0.0264583333
        # plt.scatter(x,y)
        # plt.xlim(0,image.shape[0]*0.0264583333)
        # plt.ylim(0,image.shape[1]*0.0264583333)
        # plt.title("Target points in centimeters (cm)")
        # plt.show()

        """Transform the draw according to a 15x15 square"""
        y, x = target_points_list.T
        maximum = max(image.shape[0], image.shape[1])
        k = 1500/maximum
        y = y*k
        x = x*k
        y = np.round(y)
        x = np.round(x)

        # define the list of target points to be returned for the robot.
        pts=[i for i in zip(x[0], y[0])]
        
        return pts
        
