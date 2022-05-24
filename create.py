import os
import re
import cv2
import fitz
import numpy
import shutil
import webbrowser
from PIL import Image
from tkinter import filedialog
from PyPDF2 import PdfFileReader


def click(event, x, y, flags, param):
	global lines, x_value, y_value, edited

	if event == cv2.EVENT_MOUSEMOVE:
		y_value = y
	elif event == cv2.EVENT_LBUTTONDOWN:
		edited = True
		if y not in lines:
			lines.append(y)
		# y_value = 0
	x_value = x


# Temp folder
path = os.getcwd()
if not os.path.exists(os.path.join(path, "temp")):
	os.makedirs(os.path.join(path, "temp"))



# Input templates and images
template = os.path.join(path, "template.pdf")
textbook_dir = "/Users/keemeng/Library/Mobile Documents/com~apple~CloudDocs/School/Harrow/Textbooks/"
files = []


# Input modes
print("""
Mode 0: Input folder with screenshots
Mode 1: Input screenshots
Mode 2: Input PDF
Mode 3: Select File
Or type in textbook acroynm""")

mode = input("Mode: ")
if mode == "0":
	quality = 1
	thickness = quality
	folder = input("Input folder: ")
	files = [folder + "/" + i for i in os.listdir(folder) if i.endswith(".png")]
	files.sort(key=lambda f: int(re.sub('\D', '', f)))
	if files == []:
		exit()

elif mode == "1":
	quality = 1
	thickness = quality
	count = 1
	while True:
		screenshot = input(f"Input Image {count}: ")
		if screenshot == "":
			break
		else:
			files.append(screenshot)
		count += 1

	if files == []:
		exit()

else:
	quality = 3
	thickness = quality
	if mode == "2":
		pdffile = input("Input PDF: ")

	elif mode == "3":
		pdffile = ""
		while pdffile == "":
			pdffile = filedialog.askopenfilename(initialdir=textbook_dir)

	else:
		textbooks = {
			"p1":  "Math Textbooks/Pure Mathematics Year 1.pdf", 
			"p2":  "Math Textbooks/Pure Mathematics Year 2.pdf", 
			"sm1": "Math Textbooks/Statistics and Mechanics Year 1.pdf", 
			"sm2": "Math Textbooks/Statistics and Mechanics Year 2.pdf", 
			"cp1": "Further Maths Textbooks/Core Pure Mathematics 1.pdf", 
			"cp2": "Further Maths Textbooks/Core Pure Mathematics 2.pdf", 
			"fm1": "Math Textbooks/Further Mechanics 1", 
			"fm2": "Math Textbooks/Further Mechanics 2", 
			"fs1": "Math Textbooks/Further Statistics 1", 
			"fs2": "Math Textbooks/Further Statistics 2"}

		pdffile = textbook_dir + textbooks.get(mode)
		if not pdffile:
			exit()

	begin = int(input("Input number of introduction pages: "))
	file = fitz.open(pdffile)

	with open(pdffile, "rb") as pdf:
		reader = PdfFileReader(pdf, strict=False)
		end = reader.numPages

	print(f"There are {end} pages, Input 0 for all pages. ")


	if not os.path.exists(os.path.join(path, "temp", "input")):
		os.makedirs(os.path.join(path, "temp", "input"))


	individual_pages = []
	p = input("Pages: ")
	
	if p == "0":
		individual_pages = [i for i in range(1+begin, end+1)]
	else:
		for item in p.replace(" ", "").split(','):
			ranges = item.split('-')
			if len(ranges) == 1:
				individual_pages.append(int(ranges[0])+begin)
			else:
				[individual_pages.append(i+begin) for i in range(int(ranges[0]), int(ranges[-1]) + 1)]

	count = 0
	quality_matrix = fitz.Matrix(quality, quality)
	for num in individual_pages:
		page = file.load_page(num-1)
		pixels = page.get_pixmap(matrix=quality_matrix)
		output = os.path.join(path, "temp", "input", f"{count}.png")
		# output = os.path.join(path, "temp", "input", str(count)) + ".png"
		pixels.save(output)
		files.append(output)
		count += 1

scale = float(input("Input size of images (~0.4): "))
erode_amount = 8 * quality


# Cheatsheet
print("""
┌──────────────────────────────────┐
│ Click to add a line              │
│ Press z to undo a line           │
│ Press x to delete a line         │
│ Press c to clear all lines       │
│ Press v to add vertical line     │
│ Press b to show vertical lines   │
│ Press n to not include a region  │
│ Press a to use AI to split lines │
│ Press w to change erode value +1 │
│ Press s to change erode value -1 │
│ Press spacebar to split at lines │
└──────────────────────────────────┘""")




# loop
total = 0
counter = 0
skip = False

print("[", end="")

for file in files:

	# horizontal lines
	crosshair = 1
	lines = []
	remove = []
	
	image_og = cv2.imread(file)
	width = image_og.shape[1]
	height = image_og.shape[0]
	ratio = width / height
	percentage = (counter) / len(files) * 100

	if mode != "0":
		x_value = 0
		y_value = 0
		edited = True

		name = f"Image {counter + 1} of {len(files)} ({int(percentage)}%)"
		cv2.namedWindow(name, cv2.WINDOW_NORMAL)
		cv2.resizeWindow(name, (int(1000*ratio), 1000))
		cv2.setMouseCallback(name, click)


		# show image
		while True:

			if edited:
				edited = False
				image_base = image_og.copy()

				for i in lines:
					cv2.line(image_base, (0, i), (width, i), (0, 0, 0), thickness * 2)

				copy = lines[:]
				copy.append(height)
				copy.sort()
				temp_bottom = 0

				for i in copy:
					bottom = temp_bottom
					top = i

					null = False
					for r in remove:
						if r > bottom and r < top:
							null = not null

					if null:
						cv2.rectangle(image_base, (0 + thickness, bottom + thickness), (width - thickness, top - thickness), (0, 0, 255), thickness)

					temp_bottom = i

				image = image_base.copy()

			else:
				image = image_base.copy()


			if y_value != 0:
				if crosshair == 1:
					cv2.line(image, (0, y_value), (width, y_value), (150, 150, 150), thickness)

				elif crosshair == 2:
					cv2.line(image, (x_value, 0), (x_value, height), (150, 150, 150), thickness)

				elif crosshair == 3:
					cv2.line(image, (0, y_value), (width, y_value), (150, 150, 150), thickness)
					cv2.line(image, (x_value, 0), (x_value, height), (150, 150, 150), thickness)

			cv2.imshow(name, image)
			
			key = cv2.waitKey(10) & 0xFF
			if key == ord(" "):
				break

			elif key == ord("z"):
				if lines != []:
					lines.pop()
				edited = True

			elif key == ord("x"):
				if lines != []:
					lines.remove(min(lines, key=lambda value: abs(value - y_value)))
				edited = True

			elif key == ord("c"):
				lines = []
				edited = True

			elif key == ord("v"):

				crop_image = Image.open(file, mode="r")

				left = crop_image.crop((0, 0, x_value, height))
				right = crop_image.crop((x_value, 0, width, height))
				right.save(file.replace(".png", "r.png"))
				left.save(file.replace(".png", "l.png"))

				files.insert(counter + 1, file.replace(".png", "r.png"))
				files.insert(counter + 1, file.replace(".png", "l.png"))


				cv2.destroyAllWindows()
				counter += 1
				skip = True
				break

			elif key == ord("b"):
				crosshair += 1
				if crosshair == 4:
					crosshair = 1

			elif key == ord("n"):
				remove.append(y_value)
				edited = True

			elif key == 27:
				exit()
				
			elif key == ord("w"):
				erode_amount += 1
				print(f"Erode value: {erode_amount}")

			elif key == ord("s"):
				erode_amount -= 1
				print(f"Erode value: {erode_amount}")
			
			elif key == ord("a"):

				img = cv2.imread(file)
				grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

				(thresh, blackwhite) = cv2.threshold(grayImage, 200, 255, cv2.THRESH_BINARY)

				kernel = numpy.ones((erode_amount, erode_amount), numpy.uint8)
				eroded = cv2.erode(blackwhite, kernel, iterations=1)

				cv2.imwrite(os.path.join(path, "temp", "erode.png"), eroded)


				img = Image.open(os.path.join(path, "temp", "erode.png"))
				w, h = img.size

				array = []
				for ypixel in range(h):
					black = False
					for xpixel in range(w):
						if img.getpixel((xpixel, ypixel)) == 0:
							black = True
							break
					if not black:
						array.append(ypixel)


				count = 1
				temp = []
				ranges = []
				while count <= len(array):
					if count == len(array) or array[count-1] + 1 != array[count]:
						temp.append(array[count-1])
						ranges.append(temp)
						temp = []
					else:
						temp.append(array[count-1])
					count += 1


				for i in ranges:
					lines.append(int(sum(i) / len(i)))

				edited = True




		cv2.destroyAllWindows()

		if skip:
			skip = False
			continue




	# split at lines
	lines.append(height)
	lines.sort()
	temp_bottom = 0
	for i in lines:
		image = Image.open(file, mode="r")
		bottom = temp_bottom
		height = i

		null = False
		for r in remove:
			if r > bottom and r < height:
				null = not null

		if not null:
			cropped = image.crop((0, bottom, width, height))
			cropped.save(os.path.join(path, "temp", f"{total}.png"))
			total += 1

		temp_bottom = i




	# shrink images
	count = 0
	count2 = 0
	total1 = total
	while count < total1:
		image = cv2.imread(os.path.join(path, "temp", f"{count}.png"))
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

		border_width = int(img.shape[1] * 0.01)
		shrink = cv2.copyMakeBorder(img, border_width, border_width, border_width, border_width, cv2.BORDER_CONSTANT, value=[255, 255, 255])

		if shrink.shape[0] > 4 and shrink.shape[1] > 4:
			cv2.imwrite(os.path.join(path, "temp", f"{count2}.png"), shrink)
			count2 += 1
		else:
			total -= 1
		count += 1

	counter += 1

	print(">", end="")
print("]")


# duplicate template
print("[", end="")
doc = fitz.open(template)
doc2 = fitz.open(template)
print(">", end="")
for i in range(1, total):
	doc.insert_pdf(doc2)
	print(">", end="")
doc.save(os.path.join(path, "base.pdf"))
print("]")




while True:
	# overlay
	doc = fitz.open(os.path.join(path, "base.pdf"))
	print("[", end="")
	for (page_number, page) in enumerate(doc):
		image = cv2.imread(os.path.join(path, "temp", f"{page_number}.png"))

		w = image.shape[1] * scale
		h = image.shape[0] * scale
		if h > 842:
			percent = h / 842
			h = 842
			w = int(w / percent)
		if w > 595:
			percent = w / 595
			w = 595
			h = int(h / percent)
		rect = fitz.Rect(0, 0, w, h)
		page.insert_image(rect, filename = os.path.join(path, "temp", f"{page_number}.png"))
		
		print(">", end="")

	doc.save(os.path.join(path, "output.pdf"))
	print("]")
	print("")


	webbrowser.open("file:///" + os.path.join(path, "output.pdf"))


	finish = input("Is the scale of the image ok? (Y/N): ")
	if finish.lower().startswith("y"):
		break
	elif finish == "0":
		shutil.rmtree(os.path.join(path, "output.pdf"))
		break
	else:
		scale = float(input("Input size of images: "))




# clean up
cv2.destroyAllWindows()
shutil.rmtree(os.path.join(path, "temp"))
os.remove(os.path.join(path, "base.pdf"))
print("Saved as: " + os.path.join(path, "output.pdf"))
