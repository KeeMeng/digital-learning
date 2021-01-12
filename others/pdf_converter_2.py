import fitz

pdffile = input()
doc = fitz.open(pdffile)

zoom = 2    # zoom factor
mat = fitz.Matrix(zoom, zoom)
#pix = page.getPixmap(matrix = mat, <...>)

page = doc.loadPage(0)  # number of page
pix = page.getPixmap(matrix = mat)
pix.writePNG("output.png")
