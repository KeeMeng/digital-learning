import os
import math
import numpy
import matplotlib
import statistics
import matplotlib.pyplot as plt
from PyPDF2 import PdfFileReader


path = input("Path: ").strip()

while not os.path.exists(path):
	path = input("Path: ").strip()

#count pages
count = 0
total = 0
pages = []
for root, dirs, files in os.walk(path):
	for file in files:
		if file != ".DS_Store" and file.endswith(".pdf"):
			with open(os.path.join(root, file), "rb") as pdf:
				reader = PdfFileReader(pdf, strict=False)

				count += 1
				total += reader.numPages
				pages.append(reader.numPages)


pages.sort()



#statistics
array = numpy.array(pages)
mean = int(numpy.mean(array))
median = int(numpy.median(array))
mode = int(statistics.mode(array))
minimum = int(pages[0])
maximum = int(pages[-1])
stdev = numpy.std(array)
distance = abs(array - mean)
not_outlier = distance < 2 * stdev
array = array[not_outlier]

plt.hist(array, bins=numpy.arange(array[-1]+array[-1]-array[-2])-0.5, edgecolor="black", linewidth=1, color="#4DBD33")
plt.xlabel("Pages")
plt.xticks(numpy.arange(0, array[-1]+2, step=1))
plt.xlim(0, array[-1]+1)
plt.grid(axis='y', alpha=0.7)
outliers = len(pages) - len(array)
if outliers != 0:
	plt.title("Pages in PDF (Excluding {} outliers)".format(str(outliers)), size = 15, pad = 10)
else:
	plt.title("Pages in PDF", size = 15, pad = 10)


print("Statistics: ")
print("Files: {}".format(count+1))
print("Mean: {}".format(mean))
print("Mode: {}".format(mode))
print("Median: {}".format(median))
print("Minimum: {}".format(minimum))
print("Maximum: {}".format(maximum))
print("Standard Deviation: {}".format(round(stdev,2)))
print("")
print("Pieces Of Paper Saved: {}".format(total))
print("Trees Saved: {}".format(round(total/10000,2)))

plt.show()
