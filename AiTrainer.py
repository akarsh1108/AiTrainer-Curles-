import cv2
import numpy
import time

import numpy as np

import PoseEstimationModule as pm
cap=cv2.VideoCapture(0)
cap.set(3,1720)
cap.set(4,1080)
detector= pm.poseDetector()
count = 0
dir = 0
pTime=0
while True:
    success,img=cap.read()
    img=cv2.flip(img,90)
    # img=cv2.resize(img,(720,880))
    # img = cv2.imread("resources/test.jpg")
    img = detector.findPose(img,False)
    lmList=detector.findPosition(img,False)
    # print(lmList)
    if len(lmList)!=0:
        # Left Arm
        angle=detector.findAngle(img,11,13,15)
        #Right Arm
        # angle = detector.findAngle(img, 12, 14, 16)
        per=np.interp(angle,(240,280),(0,100))
        bar = np.interp(angle, (240, 280), (650, 100))

        # print(angle,per)
        #check for the dumble curls
        if per==100:
            color =(0,255,0)
            if dir==0:
                count +=0.5
                dir=1
        if per==0:
            color = (0,255,0)
            if dir==1:
                count +=0.5
                dir=0
        print (count)


        cv2.rectangle(img,(0,450),(250,780),(0,255,0),cv2.FILLED)
        cv2.putText(img,f'{int(count)}',(15,630),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),20)

        cTime=time.time()
        fps =1/(cTime-pTime)
        pTime=cTime
        cv2.putText(img, str(int(fps)), (30, 50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (255, 0, 0), 2)

    cv2.imshow("image",img)
    cv2.waitKey(1)

