import cv2
import time
import math
import mediapipe as mp
class poseDetector():
    def __init__(self,mode=False,mcomp=1,smooth=True,eseg=False,sseg=True,
              detectionCon=0.5,trackingCon=0.5):
        self.mode=mode
        self.mcomp=1
        self.smooth = True
        self.eseg = False
        self.sseg = True
        self.detectionCon = 0.5
        self.trackingCon = 0.5
        self.mpDraw=mp.solutions.drawing_utils
        self.mpPose=mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode,self.mcomp,self.smooth,self.eseg,self.sseg,self.detectionCon,self.trackingCon)
    def findPose(self,img,draw=True):
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results= self.pose.process(imgRGB)
        if self.results.pose_landmarks and draw:
            self.mpDraw.draw_landmarks(img,self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
        return img
    def findPosition(self,img,draw=True):
         self.lmList=[]
         if self.results.pose_landmarks:
           for id,lm in enumerate(self.results.pose_landmarks.landmark):
               h,w,c =img.shape
               # print(id,lm)
               cx,cy=int(lm.x*w),int(lm.y*h)
               self.lmList.append([id,cx,cy])
               if draw:
                  cv2.circle(img,(cx,cy),5,(255,0,0),cv2.FILLED)
         return self.lmList
    def findAngle(self,img,p1,p2,p3,draw=True):
       # Get The landmarks
       x1,y1=self.lmList[p1][1:]
       x2, y2 = self.lmList[p2][1:]
       x3, y3 = self.lmList[p3][1:]
       #Calculate the angle
       angle=math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))
       if angle<0:
           angle=angle+360;
       # print(angle)
       #draw
       if draw:
           cv2.line(img,(x1,y1),(x2,y2),(0,255,0),3)
           cv2.line(img, (x3, y3), (x2, y2), (0, 255, 0), 3)
           cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
           cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
           cv2.circle(img, (x2, y2), 10, ( 0, 0,255), cv2.FILLED)
           cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
           cv2.circle(img, (x3, y3), 10, (0, 0,255), cv2.FILLED)
           cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
           # cv2.putText(img,str(int(angle)),(x2-80,y2-30),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)
       return angle
def main():
    cap = cv2.VideoCapture('PoseVideos/vid2.mp4')
    pTime = 0
    detector=poseDetector()

    while True:
        success, img = cap.read()
        detector.findPose(img)
        lmList = detector.findPosition(img,draw=False)
        # print(lmList[14])
        cv2.circle(img,(lmList[14][1],lmList[14][2]),15,(0,0,255),cv2.FILLED)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (30, 50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ =="__main__":
    main()