import fitz

pages = int(input("Pages: "))
doc = fitz.open("template.pdf")
doc2 = fitz.open("template.pdf")
for i in range(1, pages):
    doc.insertPDF(doc2)
doc.save("template2.pdf")
