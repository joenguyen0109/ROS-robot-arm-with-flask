
import cv2
import numpy as np
path = r'/home/joe/Documents/github/ROS-Robot-arm-and-website/data/bowl2.jpg'
img = cv2.imread(path)

blurImage = cv2.GaussianBlur(img,(5,5),0)



gray = cv2.cvtColor(blurImage, cv2.COLOR_BGR2GRAY)
binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # # getting ROIs with findContours
        
contours , _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
i = 1 
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > 10: 
        (x,y,w,h) = cv2.boundingRect(cnt)
        middlePoint = np.array([(x+w), (y+h)], dtype=np.int)
        saveImage = gray[y-10:y+h+10,x-10:x+w+10]
        print(cv2.boundingRect(cnt))
        cv2.imwrite(str(i)+'.png',saveImage)
        i += 1
        # show_image = gray[y-20:y+h+20,x-20:x+w+20] 
        # show_image = cv2.resize(show_image,(64,128))
        # objectId = ImageProcessing.classifyObject(show_image)

        # objectName = ""
        # if objectId == 1:
        #     objectName = "phone"
        # elif objectId == 2:
        #     objectName = "coke"
        # elif objectId == 3:
        #     objectName = "ball"
        # cv2.putText(img,objectName,(x+w+25,y+h),0,0.5,(0,255,0))