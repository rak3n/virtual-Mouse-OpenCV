import cv2
import numpy as np

cam=cv2.VideoCapture(0)

h,s,v=0,0,0
hm,sm,vm=179,255,255
lower=np.array([h,s,v])
uper=np.array([hm,sm,vm])
kernelOpen=np.ones((5,5))
kernelClose=((20,20))

font=cv2.FONT_HERSHEY_SIMPLEX
while True:
    ret,img=cam.read()

    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    mask=cv2.inRange(imgHSV,lower,uper)

    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernelClose)
    maskClose=cv2.erode(maskClose,None,iterations=2)
    maskClose=cv2.dilate(maskClose,None,iterations=2)

    maskFinal=maskClose
    _,contours, hierarchy = cv2.findContours(maskFinal.copy(),1,2)
    
    cv2.putText(img,str(h)+","+str(s)+","+str(v),(100,400),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(img,str(hm)+","+str(sm)+","+str(vm),(100,450),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1,cv2.LINE_AA)
    cv2.imshow("msk",maskFinal)
    cv2.imshow("img",img)

    key=cv2.waitKey(40)
    if(key==97):
       if(h!=0):
           h-=1
    if (key==113):
       if(h!=179):
           h+=1
    if(key==119):
        if(s!=255):
           s+=1
    if(key==115):
        if(s!=0):
            s-=1
    if(key==101):
        if(v!=255):
            v+=1
    if(key==100):
        if(v!=0):
            v-=1
    if(key==114):
       if(hm!=0):
           hm-=1
    if (key==102):
       if(hm!=179):
           hm+=1
    if(key==116):
        if(sm!=255):
           sm+=1
    if(key==103):
        if(sm!=0):
            sm-=1
    if(key==121):
        if(vm!=255):
            vm+=1
    if(key==104):
        if(vm!=0):
            vm-=1
    if(key==13):
        break;
    lower=np.array([h,s,v])    
    uper=np.array([hm,sm,vm])
                  

cv2.destroyAllWindows()

