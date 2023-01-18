import cv2
import numpy as np
from matplotlib import pyplot as plt
import numpy as np
import imutils
import argparse

## Kiko o programa está com argumentos, ou seja, to run: python target_points.py --image "nome do ficheiro"
# O default está com test_draw_1.png
def image_processing(image):
    # argparser = argparse.ArgumentParser()
    # argparser.add_argument("--image", type=str, default="test_draw_1.png")
    # args = vars(argparser.parse_args())

    # load the image and display it
    image = cv2.imread(image)
    #cv2.imwrite("TESTE_IMAGE.png", image)

    # convert the image to grayscale and threshold it
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)[1]
    #cv2.imwrite("TESTE_THRESH.png", thresh)

    # find the largest contour in the threshold image
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnts = imutils.grab_contours(cnts)
    #c = max(cnts, key=cv2.contourArea)

    img_contours = np.zeros(image.shape)
    cv2.drawContours(img_contours, cnts, -1, (0,255,0), 1)
    cv2.imwrite('contornos.png',img_contours)
    # draw the shape of the contour on the output image, compute the
    # bounding box, and display the number of points in the contour
    #cv2.imwrite("TESTE_ORIGINAL_CONTOUR.png", output)
    if len(cnts) == 1:
        contornos_aproximados = []
        # test to various nº of target points (approx variable)
        for c in cnts:
            accuracy= 0.0003 * cv2.arcLength(c, True)
            approx1= cv2.approxPolyDP(c,accuracy,True)
            contornos_aproximados.append(approx1)
            cv2.drawContours(img_contours, [approx1], -1, (0,255,0),3)
            text = "eps={:.4f}, num_pts={}".format(0.0003, len(approx1))
            # print("[INFO] {}".format(text))
            cv2.imwrite('Contorno_okkk.png'.format(c), img_contours)

        # Best result with eps = 0.0003
        best_eps = 0.0003
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c,best_eps*peri, True)
        output = image.copy()
        cv2.drawContours(output, [approx], -1, (0, 255, 0), 3)
        cv2.imwrite("PLOTS.png", output)

        target_points = approx # defining target_points variable
        counter = 0
        target_points_list = []
        if len(cnts)==1:
            for target_point in target_points:
                if counter < (len(target_points)/2)+2:
                    target_points_list.append(target_point)
                    counter += 1

        target_points_list = np.asarray(target_points_list)
        text = "num_target_pts={}".format(len(target_points_list))
        # print("[INFO Final] {}".format(text))
        
        # x,y target points to pixels
        y, x = target_points.T
        # plt.scatter(x,y)
        # plt.xlim(0,image.shape[0])
        # plt.ylim(0,image.shape[1])
        # plt.title("Target points in pixels")
        # plt.show()

        # x,y target points to centimeters (cm)
        y, x = target_points.T
        y = y*0.0264583333
        x = x*0.0264583333
        # plt.scatter(x,y)
        # plt.xlim(0,image.shape[0]*0.0264583333)
        # plt.ylim(0,image.shape[1]*0.0264583333)
        # plt.title("Target points in centimeters (cm)")
        # plt.show()

        # x,y target points according to a 25x25 cm square
        cnt = 0
        target_points_new = []
        # alpha = 30
        # for target_point in target_points:
        #     if cnt < len(target_points)-alpha:
        #         target_points_new.append(target_point)
        #         cnt += 1
        # target_points_new = np.asarray(target_points_new)

        y, x = target_points_list.T
        maximum = max(image.shape[0], image.shape[1])
        k = 1600/maximum
        y = y*k
        x = x*k
        y = np.round(y)
        # y = int(y)
        x = np.round(x)
        # x = int(x)
        # plt.scatter(x,y)
        # plt.xlim(0,2500)
        # plt.ylim(0,2500)
        # plt.title("Target points in cm according to a 25x25 cm square")
        # plt.show()

        # target_points = target_points*k
        # target_points = np.round(target_points, 1)
        # target_points = target_points[:,0]
        # print(target_points)

        pts=[i for i in zip(x[0], y[0])]
        # pts=round(pts)
        # print(pts)
        return pts

    else:
        cnts = np.delete(cnts, 1, 0)

        points = [point for contour in cnts for point in contour]
        
        img_contours = np.zeros(image.shape)
        cv2.drawContours(img_contours, points, -1, (0,255,0), 4)
        cv2.imwrite('contornos_case2.png', img_contours)
        points = np.asarray(points)
        
        best_eps = 0.0003
        peri = cv2.arcLength(points, True)
        approx = cv2.approxPolyDP(points,best_eps*peri, True)
        output = image.copy()
        cv2.drawContours(output, [approx], -1, (0, 255, 0), 3)
        cv2.imwrite("PLOTS.png", output)
        points = [point for contour in cnts for point in contour]
        #raise NotImplementedError
        
        target_points_list = approx # defining Target_points variable
        text = "num_target_pts={}".format(len(target_points_list))
        # print("[INFO Final] {}".format(text))
        # x,y target points to pixels
        y, x = target_points_list.T
        # plt.scatter(x,y)
        # plt.xlim(0,image.shape[0])
        # plt.ylim(0,image.shape[1])
        # plt.title("Target points in pixels")
        # plt.show()

        # x,y target points to centimeters (cm)
        y, x = target_points_list.T
        y = y*0.0264583333
        x = x*0.0264583333
        # plt.scatter(x,y)
        # plt.xlim(0,image.shape[0]*0.0264583333)
        # plt.ylim(0,image.shape[1]*0.0264583333)
        # plt.title("Target points in centimeters (cm)")
        # plt.show()

        # x,y target points according to a 25x25 cm square
        cnt = 0
        target_points_new = []
        # alpha = 30
        # for target_point in target_points:
        #     if cnt < len(target_points)-alpha:
        #         target_points_new.append(target_point)
        #         cnt += 1
        # target_points_new = np.asarray(target_points_new)

        y, x = target_points_list.T
        maximum = max(image.shape[0], image.shape[1])
        k = 1500/maximum
        y = y*k
        x = x*k
        y = np.round(y)
        # y = int(y)
        x = np.round(x)
        # x = int(x)
        # plt.scatter(x,y)
        # plt.xlim(0,2500)
        # plt.ylim(0,2500)
        # plt.title("Target points in cm according to a 25x25 cm square")
        # plt.show()

        # target_points = target_points*k
        # target_points = np.round(target_points, 1)
        # target_points = target_points[:,0]
        # print(target_points)

        pts=[i for i in zip(x[0], y[0])]
        # pts=round(pts)
        # print(pts)
        return pts
        

# pts = image_processing("test_draw_2.png")
# print(pts)
