import numpy as np
import cv2

file = input()
img = cv2.imread(file) # Read in the image and convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = 255*(gray < 250).astype(np.uint8) # To invert the text to white


coords = cv2.findNonZero(gray) # Find all non-zero points (text)
x, y, w, h = cv2.boundingRect(coords) # Find minimum spanning bounding box
rect = img[y:y+h, x:x+w] # Crop the image - note we do this on the original image



##coords = cv2.findNonZero(gray) # Find all non-zero points (text)
##x, y, w, h = cv2.boundingRect(coords) # Find minimum spanning bounding box
##x -= 5
##y -= 5
##w += 10
##h += 10
##rect = img[y:y+h, x:x+w] # Crop the image - note we do this on the original image


cv2.imwrite(file, rect) # Save the image
