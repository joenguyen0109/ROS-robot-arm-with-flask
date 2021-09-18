import cv2
import joblib

import numpy as np
from skimage.feature import hog

class ImageProcessing:
    @staticmethod
    def getObjectInfo(img):
        data = ImageProcessing.detectObject(img)
        return data

    @staticmethod
    def detectObject(img):
        return_data = {}
        copyImage = np.array(img, copy=True)  
        cutImage = ImageProcessing.cutImage(copyImage)
        blurImage = cv2.GaussianBlur(cutImage,(5,5),0)
        
        gray = cv2.cvtColor(blurImage, cv2.COLOR_BGR2GRAY)
        binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        contours , _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        i = 1
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 10 and area < 10000: 
                (x,y,w,h) = cv2.boundingRect(cnt)
                cv2.rectangle(img,(x-5,y-5),(x+w+5,y+h+5),(0,255,0),2)
                featureImage = cv2.resize(gray[y-10:y+h+10,x-10:x+w+10],(64,128))
                objectId = ImageProcessing.classifyObject(featureImage)

                objectName = "Object" + str(i)+ " " 
                zCoordinate = 0
                if objectId == 1:
                    objectName += "ball"
                    zCoordinate = 0.21
                elif objectId == 2:
                    objectName += "box"
                    zCoordinate = 0.15
                elif objectId == 3:
                    objectName += "gear"
                    zCoordinate = 0.15
                else:
                    objectName += "bowl"
                    zCoordinate = 0.17
                cv2.putText(img,objectName,(x,y-10),0,0.5,(0,255,0))
                midpoint1 = (x + x + w )/2
                midpoint2 = (y  + y + h )/2
                return_data[objectName] = np.append(ImageProcessing.convertCoordinate(midpoint1,midpoint2), [zCoordinate])
                i += 1

        path = r"/home/joe/Documents/github/ROS-Robot-arm-and-website/repo/camera_processing/static/image.png"
        cv2.imwrite(path,img) 
        return return_data 

    @staticmethod
    def classifyObject(img):
        load_model = joblib.load('classifyObject.pkl')
        hog_img = ImageProcessing.hogFeature(img)
        return load_model.predict(hog_img)[0]
    
    @staticmethod
    def hogFeature(img):
        data = []
        fd, hog_image = hog(img, orientations=9, pixels_per_cell=(8, 8),
                	cells_per_block=(2, 2), visualize=True)
        data.append(hog_image.flatten())
        return np.array(data)

    @staticmethod
    def cutImage(image):
        # Create ROI coordinates
        topLeft = (0, 0)
        bottomRight = (800, 160)
        x, y = topLeft[0], topLeft[1]
        w, h = bottomRight[0] - topLeft[0], bottomRight[1] - topLeft[1]

        image[y:y+h, x:x+w] = 0
        return image 

    @staticmethod
    def convertCoordinate(x,y):
        pts_src = np.array([[484.5, 523.0], [274.5, 368.5], [521.5, 321.5],[193.0, 286.5],[334.0, 251.0]])
        # corresponding points from image 2 (i.e. (154, 174) matches (212, 80))
        pts_dst = np.array([[1.8, 0.4],[1.5, 0],[1.4, 0.5],[1.3,-0.2],[1.2,0.1]])

        # calculate matrix H
        h, _ = cv2.findHomography(pts_src, pts_dst)

        a = np.array([[x, y]], dtype='float32')

        # Dont delete this line
        a = np.array([a])

        # finally, get the mapping
        pointsOut = cv2.perspectiveTransform(a, h)


        return pointsOut 