import fitz
import cv2
doc = fitz.open("template.pdf")

file = input()
image = cv2.imread(file)
w = image.shape[1] * 0.8
h = image.shape[0] * 0.8
rect = fitz.Rect(0, 0, w, h)

for page in doc:
    page.insertImage(rect, filename = file)

doc.saveIncr()
