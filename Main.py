import cv2
import math
import numpy as np
from pynput.mouse import Button,Controller

mouse=Controller()

#################################
#   Where trackers accordingly  #
#   Red  :- Middle              #
#################################
(wx,wy)=(600,500)

#differs from montor to monitor#
resx,resy=1400,900             
################################


#####################Constants############################
cam=cv2.VideoCapture(0)
l_blue=np.array([18,74,106])                           #100,192,63])
u_blue=np.array([93,255,255])                         #117,255,189])

l_red=np.array([0,164,123])                           #21,255,90])
u_red=np.array([9,255,255])                           #126,255,103])

l_green=np.array([49,101,37])
u_green=np.array([99,255,255])

kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))

right,left=False,False
bcx,bcy=0,0
rcx,rcy=0,0
gcx,gcy=0,0
rd_b,rd_g,rd_r=0,0,0
dx,dy=0,0
dist2,dist1=0,0
d="NULL"
scroll_x,scroll_y=1,1
speed=5

prev_x,prev_y=0,0
##########################################################
while True:
    ret,img=cam.read()
    img=cv2.flip(img,1)
    cv2.resize(img,(wx,wy))
    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #::::::::::::::::HSV calc::::::::::::::::::::::::::::::::::::::;
    mask_b=cv2.inRange(imgHSV,l_blue,u_blue)
    mask_r=cv2.inRange(imgHSV,l_red,u_red)
    mask_g=cv2.inRange(imgHSV,l_green,u_green)

    #:::::::::::::::Tracker Identification Unit:::::::::::::::::::::::
    mask_b=cv2.morphologyEx(mask_b,cv2.MORPH_OPEN,kernelOpen)
    mask_b=cv2.morphologyEx(mask_b,cv2.MORPH_CLOSE,kernelClose)
    mask_b=cv2.erode(mask_b,None,iterations=2)
    mask_b=cv2.dilate(mask_b,None,iterations=2)
    _,contsBlue,h=cv2.findContours(mask_b.copy(),1,2)
    MaxA,MaxB,pos1,pos2=0,0,-1,-1

    
    if(len(contsBlue)>0):
     for i in range(len(contsBlue)):
       M=cv2.moments(contsBlue[i])
       if(cv2.contourArea(contsBlue[i])>MaxA):
           MaxB=MaxA
           MaxA=cv2.contourArea(contsBlue[i])
           pos2=pos1
           pos1=i
     contsBlue[0]=contsBlue[pos1]

    mask_r=cv2.morphologyEx(mask_r,cv2.MORPH_OPEN,kernelOpen)
    mask_r=cv2.morphologyEx(mask_r,cv2.MORPH_CLOSE,kernelClose)
    mask_r=cv2.erode(mask_r,None,iterations=2)
    mask_r=cv2.dilate(mask_r,None,iterations=2)
    _,contsRed,h=cv2.findContours(mask_r.copy(),1,2)
    MaxA,MaxB,pos1,pos2=0,0,-1,-1
    if(len(contsRed)>0):
     for i in range(len(contsRed)):
       M=cv2.moments(contsRed[i])
       if(cv2.contourArea(contsRed[i])>MaxA):
           MaxB=MaxA
           MaxA=cv2.contourArea(contsRed[i])
           pos2=pos1
           pos1=i
     contsRed[0]=contsRed[pos1]
    
    mask_g=cv2.morphologyEx(mask_g,cv2.MORPH_OPEN,kernelOpen)
    mask_g=cv2.morphologyEx(mask_g,cv2.MORPH_CLOSE,kernelClose)
    mask_g=cv2.erode(mask_g,None,iterations=2)
    mask_g=cv2.dilate(mask_g,None,iterations=2)
    _,contsGreen,h=cv2.findContours(mask_g.copy(),1,2)
    MaxA,MaxB,pos1,pos2=0,0,-1,-1
    if(len(contsGreen)>0):
      for i in range(len(contsGreen)):
        M=cv2.moments(contsGreen[i])
        if(cv2.contourArea(contsGreen[i])>MaxA):
            MaxB=MaxA
            MaxA=cv2.contourArea(contsGreen[i])
            pos2=pos1
            pos1=i
      contsGreen[0]=contsGreen[pos1]
    #::::::::::Tracking Unit:::::::::::::::::::::::
    if(len(contsGreen)>0):
         x,y,w,h=cv2.boundingRect(contsGreen[0])
         gcx=x+w//2
         gcy=y+h//2
         rd_g=w+h//4
         cv2.circle(img,(gcx,gcy),(w+h)//4,(0,255,0),2)

    if(len(contsRed)>0):
         x,y,w,h=cv2.boundingRect(contsRed[0])
         rcx=x+w//2
         rcy=y+h//2
         rd_r=w+h//2
         cv2.circle(img,(rcx,rcy),(w+h)//4,(0,0,255),2)
    if(len(contsBlue)>0):
         x,y,w,h=cv2.boundingRect(contsBlue[0])
         bcx=x+w//2
         bcy=y+h//2
         rd_b=w+h//4
         cv2.circle(img,(bcx,bcy),(w+h)//4,(255,0,0),2)
    cv2.putText(img,str(d),(50,450),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1,cv2.LINE_AA)
    #:::::::::::Debugging Palace:::::::::::::::::::::::
    #cv2.imshow("blue",mask_b)
    #cv2.imshow("green",mask_g)
    #cv2.imshow("red",mask_r)
    cv2.imshow("Project Mice",img) 

    #:::::::::Gesture determining Unit:::::::::::::
    if(len(contsGreen) and len(contsBlue) and len(contsRed)):
        d="Mouse moving"
        if(left==True):
            mouse.release(Button.left)
            left=False
        if(right==True):
            mouse.release(Button.right)
            right=False
        dx=(resx*rcx//wx)
        dy=(resy*rcy//wy)
        if(math.sqrt((prev_x-dx)**2) >1 and math.sqrt((prev_y-dy)**2) > 1 ):
            mouse.position=(dx,dy)
        scroll_x,scroll_y=rcx,rcy
        dist1=math.sqrt(((gcx-rcx)**2)+((gcy-rcy)**2))
        dist2=math.sqrt(((bcx-rcx)**2)+((bcy-rcy)**2))
        if((dist1)<((rd_g+rd_r)/2+10)): #Standard distance Formula
            d="left click"
            mouse.press(Button.left)
            left=True
        if( (dist2) < ((rd_b+rd_r)/2+10)):   #Standard distance Formula
            d="right click"
            mouse.press(Button.right)
            right=True
    #print(str(dist1)+','+str(rd_g+rd_r))
    if(len(contsBlue) and len(contsRed) and len(contsGreen)==0):
        d="Let's Scroll"
        per_y=(rcy/scroll_y)*speed
        mouse.scroll(0,per_y)
    
    prev_x=dx
    prev_y=dy
    
    key=cv2.waitKey(60)
    if(key==13):
        break
cv2.destroyAllWindows()


    
