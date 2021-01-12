import cv2

img = cv2.imread(input())

color = [255, 255, 255]

top, bottom, left, right = [int(img.shape[0] * 0.04)]*4

img_with_border = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)

cv2.imshow("test", img_with_border)
