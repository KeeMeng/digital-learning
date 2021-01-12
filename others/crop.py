# from PIL import Image
# image = Image.open(r"/Users/TanKeeMeng/Downloads/oxbridge project/backup/input1.png") 
 
 
##x = 0
##y = 0
##width = 100
##height = 100
## 
##  
##cropped = image.crop((x, y, x + width, y + height))
##
##cropped.show()

import cv2
import numpy as np

img = cv2.imread(input())

def draw_circle(event,x,y,flags,param):
    global mouseX,mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img,(x,y),100,(255,0,0),-1)
        mouseX,mouseY = x,y

img = np.zeros((512,512,3), np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)

while True:
    cv2.imshow('image',img)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break
    elif k == ord('a'):
        print(f"{mouseX} {mouseY}")
