import os
import cv2
import fitz
import numpy
import shutil
import webbrowser
from PIL import Image
from PyPDF2 import PdfFileReader




#Temp folder
path = os.getcwd()
if not os.path.exists(os.path.join(path, "temp")):
    os.makedirs(os.path.join(path, "temp"))



#Input templates and images

quality = 3

template = os.path.join(path, "template.pdf")

print("Mode 1: Input screenshots\nMode 2: Input PDF")
mode = 0
while mode != 1 and mode != 2:
    mode = int(input("Mode: "))




#Input
files = []

if mode == 1: 
    thickness = 1
    count = 1
    while True:
        infile = input("Input Image {}: ".format(count))
        if infile == "":
            break
        else:
            files.append(f)
        count += 1

    if files == []:
        exit()

elif mode == 2:
    thickness = quality
    pdffile = input("Input PDF: ")
    file = fitz.open(pdffile)

    with open(pdffile, "rb") as pdf:
        reader = PdfFileReader(pdf, strict=False)
        end = reader.numPages

    print("There are {} pages. \nInput 0 for all pages. ".format(end))

    mat = fitz.Matrix(quality, quality)

    if not os.path.exists(os.path.join(path, "temp", "input")):
        os.makedirs(os.path.join(path, "temp", "input"))


    # start = int(input("Page to start: ")) - 1
    # if start == -1:
    #     start = 0
    # else:
    #     end = int(input("Page to end: ")) - 1
        
    
    # while start <= end:
    #     page = file.loadPage(start)
    #     pixels = page.getPixmap(matrix = mat)
    #     output = os.path.join(path, "temp", "input", str(start)) + ".png"
    #     pixels.writePNG(output)
    #     files.append(output)
    #     start += 1


    p = input("Pages: ")
    single = []
    
    if p == "0":
        [single.append(i) for i in range(1, end + 1)]
    else:
        for item in p.replace(" ","").split(','):
            ranges = item.split('-')
            if len(ranges) == 1:
                single.append(int(ranges[0]))
            else:
                [single.append(i) for i in range(int(ranges[0]), int(ranges[-1]) + 1)]

    count = 0
    for num in single:
        page = file.loadPage(num-1)
        pixels = page.getPixmap(matrix = mat)
        output = os.path.join(path, "temp", "input", str(count)) + ".png"
        pixels.writePNG(output)
        files.append(output)
        count += 1



scale = float(input("Input size of images (~0.4): "))




#Cheatsheet
print("""
┌──────────────────────────────────┐
│ Click to add a line              │
│ Press z to undo a line           │
│ Press x to delete a line         │
│ Press c to clear all lines       │
│ Press v to add vertical line     │
│ Press b to show vertical lines   │
│ Press n to not include a region  │
│ Press spacebar to split at lines │
└──────────────────────────────────┘""")




#loop
total = 0
counter = 0
skip = False

for file in files:

#horizontal lines
    up = 1
    lines = []
    remove = []
    x_value = 0
    y_value = 0

    def click_and_crop(event, x, y, flags, param):
        global lines
        global x_value
        global y_value

        if event == cv2.EVENT_MOUSEMOVE:
            y_value = y
        elif event == cv2.EVENT_LBUTTONUP:
            lines.append(y)
            y_value = 0
        x_value = x

    image = cv2.imread(file)
    width = image.shape[1]
    height = image.shape[0]
    ratio = width / height
    percentage = (counter) / len(files) * 100
    name = "Image " + str(counter + 1) + " of " + str(len(files)) + " (" + str(int(percentage)) + "%)"
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name, (int(1000 * ratio), 1000))
    cv2.setMouseCallback(name, click_and_crop)




#show image
    while True:
        image = cv2.imread(file)


        for i in lines:
            cv2.line(image, (0, i), (width, i), (0, 0, 0), thickness * 2)


        copy = lines[:]

        copy.append(height)
        copy.sort()
        old = 0
        for i in copy:
            bottom = old
            height = i

            null = False
            for r in remove:
                if r > bottom and r < height:
                    null = not null

            if null:
                cv2.rectangle(image, (0 + thickness, bottom + thickness), (width - thickness, height - thickness), (0, 0, 255), thickness)

            old = i


        if y_value != 0:
            if up == 1:
                cv2.line(image, (0, y_value), (width, y_value), (150, 150, 150), thickness)

            elif up == 2:
                cv2.line(image, (x_value, 0), (x_value, height), (150, 150, 150), thickness)

            elif up == 3:
                cv2.line(image, (0, y_value), (width, y_value), (150, 150, 150), thickness)
                cv2.line(image, (x_value, 0), (x_value, height), (150, 150, 150), thickness)

        cv2.imshow(name, image)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord(" "):
            break

        elif key == ord("z"):
            if lines != []:
                lines.pop()

        elif key == ord("x"):
            if lines != []:
                diff = lambda value: abs(value - y_value)
                lines.remove(min(lines, key=diff))

        elif key == ord("c"):
            lines = []

        elif key == ord("v"):

            image = Image.open(file, mode="r")

            left = image.crop((0, 0, x_value, height))
            right = image.crop((x_value, 0, width, height))
            right.save(file.replace(".png", "r.png"))
            left.save(file.replace(".png", "l.png"))

            files.insert(counter + 1, file.replace(".png", "r.png"))
            files.insert(counter + 1, file.replace(".png", "l.png"))

            #files.remove(file)

            cv2.destroyAllWindows()
            counter += 1
            skip = True
            break

        elif key == ord("b"):
            up += 1
            if up == 4:
                up = 1

        elif key == ord("n"):
            remove.append(y_value)


    cv2.destroyAllWindows()

    if skip:
        skip = False
        continue




#split at lines
    lines.append(height)
    lines.sort()
    old = 0
    for i in lines:
        image = Image.open(file, mode="r")
        bottom = old
        height = i

        null = False
        for r in remove:
            if r > bottom and r < height:
                null = not null

        if not null:
            cropped = image.crop((0, bottom, width, height))
            cropped.save(os.path.join(path, "temp", str(total)) + ".png")
            total += 1

        old = i




#shrink images
    count = 0
    while count < total:
        #+ total - len(lines)
        image = cv2.imread(os.path.join(path, "temp", str(count)) + ".png")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = 255 * (gray < 250).astype(numpy.uint8)
        coordinates = cv2.findNonZero(gray)
        x, y, w, h = cv2.boundingRect(coordinates)

        x -= 2
        y -= 2
        if x < 0:
            x = 0
        if y < 0:
            y = 0

        w += 4
        h += 4
        if w > image.shape[1]:
            w = image.shape[1]
        if h > image.shape[0]:
            h = image.shape[0]


        img = image[y:y+h, x:x+w]
        #cv2.imwrite(os.path.join(path, "temp", str(count + total - len(lines))) + "X.png", img)

        top, bottom, left, right = [int(img.shape[1] * 0.01)] * 4
        shrink = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        
        cv2.imwrite(os.path.join(path, "temp", str(count)) + ".png", shrink)
        count += 1

    counter += 1



#duplicate template
print("[", end="")
doc = fitz.open(template)
doc2 = fitz.open(template)
print(">", end="")
for i in range(1, total):
    doc.insertPDF(doc2)
    print(">", end="")
doc.save(os.path.join(path, "temp.pdf"))
print("]")




while True:

    #overlay
    count = 0
    doc = fitz.open(os.path.join(path, "temp.pdf"))
    print("[", end="")
    for page in doc:
        image = cv2.imread(os.path.join(path, "temp", str(count)) + ".png")

        w = image.shape[1] * scale
        h = image.shape[0] * scale
        if h > 842:
            percent = h / 842
            h = 842
            w = int(w/percent)
        if w > 595:
            percent = w / 595
            w = 595
            h = int(h/percent)
        rect = fitz.Rect(0, 0, w, h)
        page.insertImage(rect, filename = os.path.join(path, "temp", str(count)) + ".png")
        
        print(">", end="")
        count += 1

    doc.save(os.path.join(path, "output.pdf"))
    print("]")
    print("")


    webbrowser.open("file:///"+os.path.join(path, "output.pdf"))


    finish = input("Is the scale of the image ok? (Y/N): ")
    if finish.lower().startswith("y"):
        break
    elif finish == "0":
        cv2.destroyAllWindows()
        shutil.rmtree(os.path.join(path, "temp"))
        shutil.rmtree(os.path.join(path, "output.pdf"))
        os.remove(os.path.join(path, "temp.pdf"))
        exit()
    else:
        scale = float(input("Input size of images: "))




#clean up
cv2.destroyAllWindows()
shutil.rmtree(os.path.join(path, "temp"))
os.remove(os.path.join(path, "temp.pdf"))
print("Saved as: " + os.path.join(path, "output.pdf"))
#print("output.pdf is " + str(round(os.path.getsize(os.path.join(path, "output.pdf"))/1000000,2)) + "mb")
