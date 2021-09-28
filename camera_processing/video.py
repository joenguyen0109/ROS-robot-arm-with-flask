import cv2
import numpy as np
def cutImage(image):
    # Create ROI coordinates
    topLeft = (0, 0)
    bottomRight = (800, 160)
    x, y = topLeft[0], topLeft[1]
    w, h = bottomRight[0] - topLeft[0], bottomRight[1] - topLeft[1]

    image[y:y+h, x:x+w] = 0
    return image 

if __name__ == '__main__':
    image = cv2.imread('video_feed.jpg')
    cv2.imshow('Original Image',image)
    cutImage = cutImage(image=np.array(image, copy=True))
    blurImage = cv2.GaussianBlur(cutImage,(5,5),0)
    cv2.imshow('Blur image',blurImage)
        
    gray = cv2.cvtColor(cutImage, cv2.COLOR_BGR2GRAY)
    binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv2.imshow('Binary image',binary)
    contours , _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 10 and area < 10000: 
            (x,y,w,h) = cv2.boundingRect(cnt)
            cv2.rectangle(image,(x-5,y-5),(x+w+5,y+h+5),(0,255,0),2)
    
    cv2.imshow('Final image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    pass